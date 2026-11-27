# Designing for decisions we haven't made yet

*What it costs to keep a choice open*

Because code is getting cheaper to rewrite, it is tempting to assume architectural decisions matter less than they used to. That mixes up replacing an implementation with undoing a commitment.

Take a stylized example: a document editor needs comments attached to text. For the first release, each comment stores start and end character offsets for the selected passage. The code is tiny; an agent can rewrite the anchoring engine before dinner.

Six months later, customers have left a million comments, rewritten half their documents, exported them, and wired integrations around the comment IDs. Now comments need to survive heavy edits.

Swapping out the matching code is still cheap. Recovering what an old comment pointed to is impossible if the service never saved the quoted passage or the document version it came from. The cheap half got cheaper. The expensive half was never the code.

## Where commitments stick

Internal choices stay cheap as long as nothing outside the team notices. Swap one in-memory search index for another and, if latency and memory hold up, nobody cares.

External choices harden into other people's work. A customer pastes your comment IDs into a spreadsheet. A downstream pipeline parses your export schema. Support writes a runbook assuming webhooks arrive in a particular order. Once outside work leans on a shape, changing it is a negotiation, not a refactor.

Stored data locks you in just as hard. A schema picked for week-one convenience throws away facts you cannot conjure back later. Migrations reshape data you kept; they can't invent distinctions you discarded.

Stripe's [API versioning design](https://stripe.com/blog/api-versioning) is a well-documented example of treating that boundary seriously. Rather than forcing customers through painful `v1`-to-`v2` rewrites or letting old response shapes leak through the entire codebase, Stripe pins each account to a date-based version on its first request and isolates backwards-incompatible changes in small version-change modules applied backwards from the current schema. Core product code only speaks the latest model, while old callers keep working. That machinery isn't free to maintain; it only pays off because payment integrations are long-lived external commitments that customers refuse to rewrite every year.

Inside the document editor, the same split applies. The matching algorithm can be crude on day one and replaced on day ninety. What a comment ID means, what context gets saved alongside a selection, and what the API returns when an anchor disappears all deserve real care upfront. Calling the whole feature "easy to change" because the code is easy to regenerate hides the parts that aren't.

## Boundaries around uncertainty

David Parnas's [1972 paper on modular decomposition](https://doi.org/10.1145/361598.361623) argued for hiding design decisions that are hard or likely to shift. A clean interface limits how much of the codebase cares about an implementation, though it can only shield what its contract allows.

Putting comment matching behind an interface lets you swap algorithms freely, right up until the interface promises the wrong thing. If the contract always returns one exact character range, it has already outlawed ambiguity, no matter how cleanly the implementation sits behind it.

After a heavy edit, a quoted paragraph may show up twice or vanish completely. The product has to decide what happens then: pin the comment to an older revision, ask the reader to re-attach it, or park it in an "orphaned" thread. A smarter matching algorithm won't settle that product question, and a generic wrapper won't rescue an interface that pretended ambiguity couldn't happen.

You don't need to predict next year's matching algorithm to draw an honest boundary. Knowing that *some* anchors will fail to match is enough.

## Pricing an option

Carliss Baldwin and Kim Clark treat modular replaceability as a real option in [The Option Value of Modularity in Design](https://scholarsarchive.byu.edu/facpub/8944/): its value depends on how much better a future replacement could be, how cheaply you can test alternatives, and what it costs to maintain the structure that lets you swap.

Engineers are great at talking up the upside and forgetting the carrying cost. Compare three ways to store comment anchors on day one:

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

Option B buys most of the future room at a fraction of Option C's carrying cost. The real point isn't that Option B wins everywhere, only that every option carries a bill you pay whether you exercise it or not.

Cheap implementation actually pulls in opposite directions here. Inside a stateless module with no external callers, building a flexible framework upfront makes *less* sense when rewriting a simple version later takes an hour. At a public API or persistent data boundary, the same shift makes early care *more* important, because generated code can ship bad commitments faster than before. Put the careful design at the edges where commitments stick.

## Buying information instead of keeping every door open

Sometimes the cheapest way to handle an open choice is to gather enough evidence to close it.

Before freezing the comment API, pull a sample of real document edits and run plain offsets against quoted-text matching. An agent can script that comparison across a thousand documents in an hour. Someone still has to check whether the sample reflects real editing habits rather than tidy typo fixes, and whether the failure cases actually annoy users. If readers mainly want the conversation preserved, showing the original quote beside an orphaned comment may matter far more than a clever relocation algorithm.

Stop once the remaining uncertainty isn't worth delaying shipment, or once you have an acceptable fallback for the ugly cases. Write the boundary down beside the choice, following [What software should remember](./what-software-should-remember.md): *"offsets plus quoted text handle the edits seen so far; revisit if customers start reorganizing multi-section drafts heavily."*

## Reversibility you haven't tested is a wish

A rollback plan you have never run is just an optimistic story.

Suppose the editor migrates to the richer comment schema. The new release deploys and starts writing new rows. Next morning a bug lands, the team rolls back to yesterday's binary, and the old binary crashes on every comment created overnight. They kept the old build while quietly breaking their ability to go back to it.

Sandeep Pokkunuri's writeup on [rollback safety at Amazon](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/) puts a finger directly on this: testing version N and version N+1 in isolation proves nothing about stepping backward from N+1 to N. A real rehearsal writes new-format comments, edits documents, and runs the *previous* release against that live state. If it breaks, split the rollout: ship readers that understand the new format first, and only start writing it once rollback actually works.

Rehearsing reversal also forces an expiration date. Keeping a backward-compatible path open for a week during rollout is sensible; nursing two storage formats for five years is self-inflicted drag.

## When refusing to choose becomes the trap

Teams burned once by a rigid schema often swing too far the other way until nothing ever settles. The document service ends up carrying three anchor formats, two API versions, and four relocation flags because nobody wanted to close a door. Every engineer (and every agent) now has to reason through their cross-product, and documents behave differently depending on the month they were created.

An option you never retire turns into a liability. Early commitment has real value: a firm contract lets neighboring teams build without constant sync meetings, and one data representation keeps tooling sane. Keep a door open while real information is still coming in; once the evidence lands, make the call and close the spare exits.

Four questions catch most bad commitments during a design review: what does this write into lasting data, who outside the team will end up depending on it, what evidence would make us replace it, and have we actually rehearsed the rollback we claim is easy? You rarely end up with a grand architecture. You end up with a retained quote, a narrower promise, or a deleted extension point that keeps next year's hard decision from becoming an impossible one.
