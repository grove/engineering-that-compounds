# Designing for decisions we haven't made yet

*What it costs to keep a choice open*

Because code is getting cheaper to rewrite, it is easy to assume architectural decisions matter less than they used to. That confuses replacing an implementation with undoing a commitment.

Stripe's [API versioning design](https://stripe.com/blog/api-versioning) is a clear example of the difference. Rather than forcing merchants through `v1`-to-`v2` migrations or letting legacy response shapes bleed across the whole codebase, Stripe pins each account to a date-based API version on its first request and isolates backwards-incompatible changes in small transformation modules applied backwards from the current schema. Core product code speaks only the latest model while old callers keep working. That machinery has real carrying cost; it pays off because payment integrations are long-lived external promises that customers will not rewrite on your schedule.

Internal choices stay cheap as long as nothing outside the team notices. Swap one in-memory search index for another and, if latency and memory hold up, nobody cares. External choices harden into other people's work: a spreadsheet referencing your IDs, a downstream pipeline parsing your export schema, a support runbook assuming webhooks arrive in order. Once outside work leans on a shape, changing it becomes a negotiation.

## Stored data commits harder than code

Persistent schemas lock you in just as firmly as public APIs, and cheaper coding does not rescue them.

Consider a hypothetical document editor adding inline comments. For the first release, each comment stores start and end character offsets for the selected passage. The code is tiny; an agent can rewrite the anchoring engine before dinner.

Six months later, customers have left a million comments, rewritten half their documents, exported them, and built integrations around the comment IDs. Now comments need to survive heavy edits.

Swapping the matching algorithm is still cheap. Recovering what an old comment pointed to is impossible if the service never saved the quoted passage or the document version it belonged to. The cheap half got cheaper; the expensive half was never the code. Migrations can reshape data you kept, not invent facts you threw away.

Inside that editor, the matching algorithm can be crude on day one and replaced on day ninety. What a comment ID means, what context gets saved beside a selection, and what the API returns when an anchor disappears all need care upfront. Calling the whole feature "easy to change" because the implementation is easy to regenerate hides the pieces that aren't.

## Boundaries around uncertainty

David Parnas's [1972 paper on modular decomposition](https://doi.org/10.1145/361598.361623) argued for hiding design decisions that are hard or likely to change. A clean interface limits how much of the codebase cares about an implementation, up to the point where the interface contract itself promises the wrong thing.

Putting comment matching behind an interface lets you swap algorithms freely, until the contract promises to always return one exact character range. Once it does, it has outlawed ambiguity no matter how cleanly the implementation hides behind it.

After a heavy edit, a quoted paragraph may appear twice or disappear altogether. The product has to decide what happens then: pin the comment to an older revision, ask the reader to re-attach it, or park it in an "orphaned" thread. A better matching algorithm won't settle that product question, and a generic wrapper won't save an interface that pretended ambiguity could not occur.

You don't need to guess next year's matching algorithm to draw an honest boundary. Knowing that *some* anchors will fail to match is enough.

## Pricing an option, and noticing what it closes

Carliss Baldwin and Kim Clark treat modular replaceability as a real option in [The Option Value of Modularity in Design](https://scholarsarchive.byu.edu/facpub/8944/): its value depends on how much better a future replacement could be, how cheaply you can test alternatives, and what it costs to maintain the structure that lets you swap.

Engineers are good at talking up the upside and forgetting the carrying cost. Compare three ways to store comment anchors on day one:

```text
Option A: Character offsets only
  Keeps open: Nothing once text is heavily edited.
  Carrying cost: Minimal storage, simplest schema.
  Risk: Permanent loss of intent for existing comments.

Option B: Offsets + quoted passage + short surrounding context + doc version
  Keeps open: Fuzzy matching, orphan display, future re-anchoring.
  Carrying cost: Extra storage; deletion and privacy sweeps must scrub quotes too.
  Risk: Modest; unused fields can be dropped once one scheme settles.

Option C: Full immutable revision history of every edited document
  Keeps open: Exact historical replay and diff-based re-anchoring.
  Carrying cost: Heavy storage, retention complexity, legal exposure.
  Risk: Permanent obligation built for an unproven requirement.
```

Option B buys most of the room to maneuver at a fraction of Option C's cost. Even there, notice something easy to miss: *optionality is not always additive.* Keeping quoted passages preserves technical freedom to re-anchor comments later, while creating a new privacy and deletion obligation, since redacting sensitive text from a document now also means scrubbing every comment that copied it. Preserving one option can box you in somewhere else.

Cheap implementation pulls in opposite directions here. Inside a stateless module with no external callers, building a flexible framework upfront makes *less* sense when rewriting a plain version later takes an hour. At a public API or persistent data boundary, the same shift makes early care *more* important, because generated code can ship bad commitments faster than before. Put the careful design at the edges where commitments stick.

## Buying information instead of keeping every door open

Often the cheapest way to handle an open choice is to gather enough evidence to close it.

Before freezing the comment API, pull a sample of real document edits and compare plain offsets against quoted-text matching. An agent can script that run across a thousand documents in an hour. You still have to check whether the sample reflects messy real-world editing rather than minor typo fixes, and whether the failure cases actually bother users. If readers mostly want the conversation preserved, showing the original quote beside an orphaned comment may matter more than a clever relocation algorithm.

Stop once the remaining uncertainty isn't worth delaying shipment, or once you have a decent fallback for the ugly cases. Write the boundary down beside the choice, following [What software should remember](./what-software-should-remember.md): *"offsets plus quoted text handle the edits seen so far; revisit if customers start reorganizing multi-section drafts heavily."*

## Reversibility you haven't tested is a wish

A rollback plan you have never run is just an optimistic story.

Suppose the editor migrates to the richer comment schema. The new release deploys and starts writing new rows. Next morning a bug lands, the team rolls back to yesterday's binary, and the old binary crashes on every comment created overnight. They kept the old build while breaking their ability to go back to it.

Sandeep Pokkunuri's writeup on [rollback safety at Amazon](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/) puts a finger on why: testing version N and version N+1 in isolation proves nothing about stepping backward from N+1 to N. A real rehearsal writes new-format comments, edits documents, and runs the *previous* release against that live state. If it breaks, split the rollout: ship readers that understand the new format first, and only start writing it once rollback works.

Rehearsing reversal also forces an expiration date. Keeping a backward-compatible path open for a week during rollout is sensible; carrying two storage formats for five years is self-inflicted drag.

## When refusing to choose becomes the trap

Teams burned once by a rigid schema often swing too far the other way until nothing ever settles. The document service ends up carrying three anchor formats, two API versions, and four relocation flags because nobody wanted to close a door. Every engineer and every agent now has to reason through their combinations, and documents behave differently depending on the month they were created.

An option you never retire turns into a liability. Early commitment has real value: a firm contract lets neighboring teams build without constant sync meetings, and one data representation keeps tooling sane. Keep a door open while real information is still arriving; once the evidence lands, make the call and close the spare exits.

Four questions catch most bad commitments in a design review: what does this write into lasting data, who outside the team will depend on it, what evidence would make us replace it, and have we actually rehearsed the rollback we claim is easy? Most of the time the answer isn't a grand architecture. It is a retained quote, a narrower promise, or a deleted extension point that keeps a future change possible without paying for it forever.
