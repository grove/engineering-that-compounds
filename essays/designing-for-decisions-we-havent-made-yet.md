# Designing for decisions we haven't made yet

*What it costs to keep a choice open*

One of the quieter mistakes in the current enthusiasm for AI-assisted development is assuming that because code is cheap to rewrite, architectural decisions matter less. That confuses replacing an implementation with undoing a commitment.

In a hypothetical document editor, a team has to decide how to attach comments to text. For the first release, each comment stores the start and end character offsets of the selected passage. The code is tiny; an agent could write a completely different anchoring engine before dinner.

Six months later, customers have written a million comments, edited their documents, exported them, and built integrations around the comment IDs. Now the team wants comments to survive heavy edits to the text.

Swapping out the matching code is still easy. Recovering what an old comment pointed to is impossible if the service never stored the quoted text or the document version it came from. The cheap part of the decision got cheaper. The expensive part was never the code.

## Where commitments stick

Some choices stay safely inside the codebase. Swap one internal search index for another and, as long as latency and memory hold up, nobody outside the team needs to know.

Other choices leak past your boundary and harden into other people's work. A customer stores your comment IDs in a spreadsheet. A downstream pipeline parses your export schema. Support engineers build a runbook around the order in which webhooks fire. Once external work depends on a shape, changing it is no longer a software edit; it is a negotiation.

Stored data locks you in just as tightly. A schema chosen for week-one convenience discards details you cannot conjure back later. Migrations rearrange information you kept; they cannot invent distinctions you threw away.

That splits the document service's decision into pieces with completely different reversal costs. The matching algorithm can be crude on day one and replaced on day ninety. The meaning of a comment ID, the context saved alongside a selection, and what the API returns when an anchor can no longer be found all deserve real thought upfront. Calling the whole feature "easy to change" because the code is easy to regenerate hides the exact parts that are not.

## Boundaries around uncertainty

David Parnas's [1972 paper on modular decomposition](https://doi.org/10.1145/361598.361623) argued for hiding design decisions that are hard or likely to shift. A good boundary limits how much of the system cares about a choice, though it can only protect what its contract allows.

Putting comment matching behind an interface lets the team swap algorithms freely, until the interface itself promises the wrong thing. If the contract always returns a single exact character range, it has already ruled out ambiguity, no matter how nicely the implementation is encapsulated.

After a heavy edit, a quoted paragraph might appear twice, or disappear altogether. The product has to decide what happens then: keep the comment pinned to an older revision, ask the reader to re-attach it, or display it in a separate "orphaned" thread. No cleverer matching algorithm settles that product question, and no generic wrapper rescues an interface that pretended ambiguity could not happen.

Keeping a choice open does not mean predicting every future implementation. It means recognizing where the uncertainty sits. You can be unsure how you will relocate anchors next year while being fairly sure that some anchors will fail to match. That is enough to design an honest boundary.

## Pricing an option

Carliss Baldwin and Kim Clark treat modular replaceability as a financial option in [The Option Value of Modularity in Design](https://scholarsarchive.byu.edu/facpub/8944/): its worth depends on how much better a future replacement could be, how cheaply you can test alternatives, and what it costs to maintain the architecture that makes swapping possible.

That last term is the one engineers love to ignore. Compare three ways the document team might store comment anchors on day one:

```text
Option A: Character offsets only
  Keeps open: Nothing once text is heavily edited.
  Carrying cost: Minimal storage, simplest schema.
  Risk: Permanent loss of intent for existing comments.

Option B: Offsets + quoted passage + short surrounding context + doc version
  Keeps open: Better fuzzy matching, orphan display, future re-anchoring.
  Carrying cost: Extra storage; deletion and privacy sweeps must scrub quotes too.
  Risk: Modest; easy to drop unused fields once one scheme settles.

Option C: Full immutable revision history of every edited document
  Keeps open: Exact historical replay and diff-based re-anchoring.
  Carrying cost: High storage, retention policy complexity, legal exposure.
  Risk: Heavy ongoing obligation built for a requirement not yet proven.
```

Looking at them side by side makes the tradeoff plain. Option B buys most of the future freedom at a fraction of Option C's carrying cost. The point is not that Option B always wins, but that you should price the carrying cost against a concrete future need instead of bragging about how many hypothetical designs an architecture supports.

Cheap implementation actually pulls *both* ways here. Inside a stateless internal module with no external callers, writing a flexible framework upfront makes *less* sense when rewriting a simple version later is cheap. At a public API or persistent data boundary, the exact same shift makes early care *more* important, because generated code can ship bad commitments faster than before. Effort belongs unevenly at the edges where commitments stick.

## Buying information instead of keeping every door open

Sometimes the smartest way to handle an open choice is to buy enough evidence to close it.

Before freezing the comment API, the team can pull a sample of real document edits and test plain offsets against quoted-text matching. An agent can script the comparison across a thousand documents in an hour. Humans still have to check whether the corpus reflects real customer edits rather than tidy typo fixes, and whether the failure cases actually bother users. If readers mostly care about preserving the conversation thread, showing the original quoted passage next to an orphaned comment may matter far more than a heroic relocation algorithm.

Stop experimenting once the remaining uncertainty no longer justifies delaying the ship date, or once you have an acceptable fallback for the ambiguous cases. Then record the boundary alongside the decision, following the habit from [What software should remember](./what-software-should-remember.md): *"offsets plus quoted text cover the editing patterns seen so far; revisit if customers adopt heavy multi-section reorganization."*

## Reversibility you haven't tested is a wish

A rollback plan is just another unverified assumption until you run it.

Suppose the document service migrates to a richer comment schema. The new release deploys and begins writing new records. The next morning a bug surfaces, the team rolls back to yesterday's binary, and the old binary crashes on every comment created overnight. The team kept the old artifact while breaking its ability to go back to it.

Sandeep Pokkunuri's writeup on [rollback safety at Amazon](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/) points straight at this gap: testing version N and version N+1 separately proves nothing about moving backward from N+1 to N. A real rehearsal writes new-format comments, edits documents, and then runs the *previous* release against that live state. If it breaks, split the change: deploy readers that understand the new format first, and only start writing it once rollback is safe.

Rehearsing reversibility also forces you to pick an expiration date. Keeping an escape hatch open for a week during rollout is prudence; supporting two storage models for five years is self-inflicted pain.

## When refusing to choose becomes the trap

Teams burned once by a rigid schema often overcorrect until every decision stays provisional forever. The document service ends up with three anchor formats, two API versions and four relocation flags, each preserved to avoid committing too soon. Every engineer (and every agent) now has to reason through their cross-product, and documents behave differently depending on the month they were created.

An option that once had value can become an obligation.

Early commitment is not the enemy of good design. A stable public contract lets neighboring teams build without constant coordination; a single data representation keeps tooling simple. Keeping a door open only earns its keep when real information is still on the way. Once the evidence lands, make the call and close the spare exits.

When reviewing any consequential design, four questions cut through most of the fog: what does this write into lasting data, who outside the team will come to depend on it, what evidence would make us replace it, and have we actually rehearsed the reversal we claim is easy? Answering them rarely produces a grand architecture that anticipates everything. It produces a few modest safeguards (a retained quote, a narrower promise, a deleted extension point) that keep next year's hard decisions from becoming impossible ones.
