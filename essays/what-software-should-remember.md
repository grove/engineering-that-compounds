# What software should remember

*Keeping reasons available, and open to revision*

```text
# Wait 20 minutes before exporting; partner sometimes revises files after upload.
EXPORT_DELAY_MINUTES = 20
```

Take a made-up export service with that line sitting in its scheduler. The code explains *how* it waits, and the test suite confirms *that* it waits.

Then the partner ships an `upload_complete` webhook. Can we drop the twenty-minute delay?

Staring at the code won't tell you. Did the partner contractually guarantee no edits after that webhook, or did someone just see clean behavior in a staging run? Were late revisions the only reason for the buffer, or does a downstream accounting job quietly depend on it? Was twenty minutes measured from production logs, written into an SLA, or picked because it sounded safe on a Friday afternoon?

A coding agent can trace every caller of `EXPORT_DELAY_MINUTES` in seconds. What it cannot pull out of the repository is evidence nobody recorded. Worse, if you ask why the delay is there, it will gladly produce a smooth, confident answer that gets the actual reason wrong.

That is what engineering memory is for: giving whoever opens this file next year enough of the past to decide whether the rule still holds.

## Reasons that outlive the choice

Michael Nygard's [architecture decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) are still hard to beat for this: a short file recording context, decision, status, and consequences. When facts change, you supersede the old record instead of editing it in place, so a reader can tell what is still live from what used to be true.

Ordinary wiki pages fail in the opposite direction. A page about the export job starts out accurate. Five edits later, it mixes the original incident with current implementation details and an unchecked hunch copied out of Slack. Nothing looks broken, yet nobody can tell which sentences still have evidence underneath them.

A useful record for the twenty-minute delay fits on half a screen. The parts that matter most are where the claim came from and what should make someone reopen it:

```text
Decision: Wait 20 minutes after upload visibility before exporting.
Status: Active (adopted 2024-03; linked from export/scheduler.py)

Why:
- Observed: In 2024-02 logs (incident #412), 14 of 3,200 partner uploads
  were overwritten within 11 minutes of first appearing in the bucket.
- Partner statement: Integration lead confirmed via email (2024-02-19)
  that their uploader writes a placeholder before streaming the full file.
- Choice: 20 minutes was chosen with margin; no SLA requires faster export.

Not established:
- Whether any downstream consumer relies on the 20-minute gap.

Revisit when:
- The partner introduces an atomic upload or explicit completion signal.
- Export latency becomes a customer commitment (< 20 minutes).
- Overwrites appear after 20 minutes in production logs.
```

That last block does the heavy lifting. Without reconsideration triggers, decision records turn into polite monuments warning future engineers not to touch anything. With them, the new webhook immediately tells a maintainer that the old premise just cracked.

You won't foresee every future shift, and you don't need to. Even a plain sentence (*"assumes uploads can be overwritten after they first appear"*) gives the next person far more to work with than *"required for reliability."*

## An observation is not a promise

Three statements might show up in notes about the export pipeline:

- The partner's API contract promises a completed upload will never be revised.
- Last month's logs show zero revisions after completion.
- Our importer ignores any revision arriving after the first read.

All three describe the same surface behavior, yet they license completely different choices. The first is an external obligation you can verify and hold someone to. The second is a finite sample. The third is our own design choice. Flattening them into *"completed uploads never change"* erases the exact distinction you need when deciding whether to delete the timer.

Busy engineers do that compression out of habit. LLMs do it by default; turning messy, hedged notes into crisp prose is literally what they are trained for. The cleaner a summary reads, the harder it is to see what got dropped.

The [W3C provenance model](https://www.w3.org/TR/prov-overview/) formalizes this by tying claims to the entities, activities, and agents that produced them. You don't need RDF graphs on an application team, just the habit of keeping a conclusion attached to its source. For a benchmark, point to the commit, workload, and hardware. For a business rule, name the owner and policy. For a guess, call it a guess.

Provenance won't guarantee a claim is true. It makes the claim inspectable, and a rough observation with visible limits is far safer than a confident sentence with no trail behind it.

## Finding the right record when there are hundreds

Writing a good record is the easy half. Surfacing it at the right moment, once a codebase has four hundred of them, is where most documentation efforts quietly die.

For local choices, wire the link in both directions. `EXPORT_DELAY_MINUTES` points to the decision record; the record names the scheduler and the tests that enforce it. When a protocol test breaks, its failure message points straight to the assumption it guards, so the engineer learns *why* the behavior existed before deciding whether to fix the code or change the test. Short cross-references beat duplicating explanations across five files, because copies drift on their own schedules.

Cross-cutting decisions are harder. A rule like *"no synchronous calls across billing and fulfillment"* or *"all customer-facing IDs must stay opaque"* doesn't belong to a single constant. If you dump it into a flat `docs/adr/` directory beside three hundred narrow choices, neither a human nor a coding agent will reliably pull it into context before violating it.

Two low-tech habits help at scale. First, turn enforceable cross-cutting rules into automated checks (linters, contract tests, dependency boundaries) whose error output links back to the rationale. If a rule matters across twenty services, the build should surface it when someone crosses the line. Second, keep a tiny, ruthlessly curated index of *active* architectural constraints per domain (ten lines, not a hundred), and move superseded records out of the default search path. Both humans and retrieval-augmented coding agents drown in old history when active rules and retired ones sit side by side in the same folder.

Plenty of crucial knowledge still lives outside code. No test suite can tell you whether a partner's commercial promise is credible, or whether a twenty-minute delay is starting to cost deals. Turning a judgment into a constant merely hides it unless the reasoning stays within reach. The same applies to [abandoned experiments](./the-value-of-forgotten-alternatives.md): keep the road short from the question to the evidence that settled it.

## Memory goes stale, and silent rewrites make it worse

Automation can verify the mechanical bits of memory: that a linked file still exists, a reproduction still runs, or a documented schema still matches production.

The harder claims don't stay fresh just because a quarterly reminder fired and someone clicked "reviewed." An agent comparing a decision record against the code can confirm they still agree while having no idea that the partner rewrote its uploader three months ago.

Revisit a record when something relevant actually moves: a completion webhook ships, a second downstream team starts reading the files, or sales starts promising five-minute exports. And when new evidence contradicts an old record, leave the seam visible. Silently rewriting history to match today's view makes the docs tidier while wiping out the fact that the team's earlier assumption broke. Mark the old note superseded, link the change or incident that overturned it, and keep the current summary short.

This is also where automated memory upkeep hits a wall. An agent can flag that a claim looks stale or contradicted. Deciding whether an external partner's guarantee still holds takes a human with authority, and occasionally a phone call outside engineering.

## The discipline of forgetting

Archiving every prompt, scratch command, and Tuesday afternoon debugging detour creates sediment rather than institutional memory. The next maintainer needs the question, the decisive evidence, the call that was made, and its edges, not a transcript of how someone spent three hours chasing the wrong log line.

Raw production dumps and huge traces are usually too sensitive or expensive to keep anyway. Boil them down to a minimal synthetic reproduction, provided someone checks that the reduction didn't strip out the quirk that triggered the bug. Deleting duplicate explanations, swapping unsupported rules for explicit open questions, and retiring dead records are all real maintenance.

Want to know whether your system remembers the right things? Hand the export job to an engineer who has never seen it and ask one question: *can we remove the twenty-minute delay?*

Watch where they go. If they find the original incident, notice the gap between an informal email and a contract, and see what needs checking before the webhook can replace the timer, the memory is earning its keep. If they can only tell you what the code currently does, or leave the delay alone because three wiki pages echo the same unverified claim, the memory is working against you.
