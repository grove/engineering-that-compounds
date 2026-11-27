# What software should remember

*Keeping reasons available, and open to revision*

```text
# Wait 20 minutes before exporting; partner sometimes revises files after upload.
EXPORT_DELAY_MINUTES = 20
```

Picture opening a scheduler file in a fictional export service and finding those two lines. The code tells you *how* it waits, and the tests confirm *that* it waits.

Then the partner ships an `upload_complete` webhook. Can you drop the twenty-minute delay?

The code won't tell you. Did the partner contractually guarantee no edits after that webhook, or did someone see clean behavior during a staging run? Were late revisions the only reason for the buffer, or does a downstream accounting job also rely on it? Was twenty minutes measured from production logs, written into an SLA, or picked because it sounded safe on a Friday afternoon?

A coding agent can trace every caller of `EXPORT_DELAY_MINUTES` in seconds. What it cannot pull out of the repository is evidence nobody wrote down. Worse, if you ask why the delay exists, it will happily produce a confident explanation that gets the real reason wrong.

That is the job of engineering memory: giving whoever opens this file next year enough of the past to decide whether the rule still applies.

## Reasons that outlive the choice

Michael Nygard's [architecture decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) remain hard to beat for this: a short file recording context, decision, status, and consequences. When facts change, you supersede the old record instead of editing it in place, so a reader can separate what is live from what used to be true.

Ordinary wiki pages fail the opposite way. A page about the export job starts out accurate. Five edits later, it blends the original incident with current implementation details and an unchecked hunch copied from Slack. Nothing looks broken, yet nobody can tell which sentences still have evidence behind them.

A useful record for the twenty-minute delay fits on half a screen. The parts that earn their keep are where each claim came from and what should reopen the decision:

```text
Decision: Wait 20 minutes after upload visibility before exporting.
Status: Active (adopted 2024-03; linked from export/scheduler.py)
Owner: Integrations team (partner-feed channel)

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

That last block does the heavy lifting. Without reconsideration triggers, decision records turn into monuments warning future engineers not to touch anything. With them, the new webhook tells a maintainer right away that the original premise has cracked.

You won't foresee every future shift, and you don't need to. Even a plain line (*"assumes uploads can be overwritten after they first appear"*) gives the next person far more to work with than *"required for reliability."*

## An observation is not a promise

Three statements might show up in notes about the export pipeline:

- The partner's API contract promises a completed upload will never be revised.
- Last month's logs show zero revisions after completion.
- Our importer ignores any revision arriving after the first read.

All three describe the same surface behavior, yet they authorize completely different choices. The first is an external obligation you can verify and enforce. The second is a finite sample. The third is our own design choice. Flattening them into *"completed uploads never change"* erases the exact distinction you need when deciding whether to delete the timer.

Busy engineers compress things like that out of habit. LLMs do it by default; turning messy, hedged notes into clean prose is what they are trained for. The smoother a summary reads, the harder it is to see what got dropped.

The [W3C provenance model](https://www.w3.org/TR/prov-overview/) formalizes this by tying claims to the entities, activities, and agents that produced them. You don't need RDF graphs on an application team, just the habit of keeping a conclusion attached to its source. For a benchmark, point to the commit, workload, and hardware. For a business rule, name the owner and policy. For a guess, call it a guess.

And when two authoritative sources contradict each other (say the partner's API docs promise atomic uploads while their integration lead's email warns about placeholders), record the contradiction plainly instead of picking a winner behind the scenes. An unresolved conflict you can see is safer than false certainty. Provenance won't prove a claim is true, and it isn't worth maintaining for a trivial local constant you could rewrite in five minutes. Save the trail for decisions whose reversal is expensive, where a rough observation with visible limits beats a confident sentence with nothing behind it.

## Finding the right record, and hearing when a trigger fires

Writing a good record is the easy half. Two harder problems kill most documentation efforts once a codebase accumulates hundreds of them.

The first is surfacing the right record when someone touches the code. For local choices, wire the link in both directions: `EXPORT_DELAY_MINUTES` points to the decision record, and the record names the scheduler and the tests that enforce it. When a protocol test breaks, its failure message points straight to the assumption it guards, so the engineer learns *why* the behavior existed before deciding whether to fix the code or change the test. Short cross-references beat copying explanations into five files, because copies drift on their own schedules.

Cross-cutting decisions (*"no synchronous calls across billing and fulfillment,"* or *"all customer-facing IDs must stay opaque"*) don't belong to a single constant. Dump them into a flat `docs/adr/` directory beside three hundred narrow choices and neither a human nor a coding agent will reliably find them before crossing the line. Two low-tech habits help: turn enforceable cross-cutting rules into automated checks (linters, contract tests, dependency boundaries) whose error output links back to the rationale, and keep a short, actively pruned index of *live* architectural constraints per domain (ten lines, not a hundred), moving superseded records out of the default search path. Both people and retrieval-augmented coding agents drown when live rules and retired ones share the same folder.

The second problem is trickier, and documentation frameworks rarely mention it: code links only fire when someone edits the code. Putting *"Revisit when the partner introduces a completion webhook"* inside a markdown file does nothing if the partner announces that webhook in a changelog email that a solutions engineer reads and archives without knowing ADR-047 exists. External triggers are a routing and ownership problem, not a writing problem. Every external trigger needs a real home where the news lands: a named team channel, a partner-integration checklist, an alert on post-20-minute overwrites, or a quarterly SLA review. If nobody owns watching for a trigger, writing it down is wishful thinking.

Plenty of crucial knowledge still lives outside code. No test suite can tell you whether a partner's commercial promise is credible, or whether a twenty-minute delay is starting to cost deals. Turning a judgment into a constant only hides it unless the reasoning, and who owns revisiting it, stay within reach. The same holds for [abandoned experiments](./the-value-of-forgotten-alternatives.md).

## Give the next session a way in

A long debugging conversation can leave an agent unusually well informed about an integration. The next session does not inherit that understanding merely because the team merged its patch. The repository needs an entry point that survives the conversation.

Use the project's agent instructions as a short route to the relevant knowledge. For the export service, point to the decision record, the partner evidence it relies on and the test that exercises partial uploads. Another paragraph saying “be careful with partner files” gives the next session little to act on. Keep the detailed explanation in the record. Repeating it in `AGENTS.md`, a service README and a prompt creates three versions to maintain.

Then test the route with an ordinary task. Give a fresh session a request to change the exporter, with its usual repository access but no hint about the timer note. Check whether it finds the current rationale, distinguishes the partner's promise from observations in logs, and notices the unanswered question about downstream consumers. Ask it to point to evidence for its proposed change. Saying it has read the documentation is not enough.

If it misses something, inspect the miss before adding another instruction. The note may be poorly named, disconnected from the relevant code or contradicted by an obsolete summary. Repair that fault and try again. A successful rehearsal shows that this route worked for this task; later changes will reveal whether the record remains useful. The essay [Engineering that compounds](./engineering-that-compounds.md), follows this habit through a complete change.

## Memory goes stale, and silent rewrites make it worse

Automation can check the mechanical parts of memory: that a linked file still exists, a reproduction still runs, or a documented schema still matches production.

The harder claims don't stay fresh because a quarterly reminder fired and someone clicked "reviewed." An agent comparing a decision record against the code can confirm they still agree while having no idea that the partner rewrote its uploader three months ago.

Revisit a record when something relevant moves: a completion webhook ships, a second downstream team starts reading the files, or sales starts promising five-minute exports. When new evidence overturns an old record, leave the seam visible. Silently editing history to match today's view makes the docs neater while erasing the fact that an earlier assumption failed. Mark the old note superseded, link the change or incident that overturned it, and keep the current summary short.

Here it helps to separate four roles that get blurred whenever people argue about AI and documentation:

- *Producing a claim* (a patch, a summary, a proposed rule)
- *Establishing evidence* (checking logs, surfacing contradictions, running reproductions)
- *Judging sufficiency* (deciding whether the evidence is strong enough to bet on)
- *Accepting accountability* (owning the fallout if the call goes wrong)

Agents are already useful for the first two. Deciding whether an informal partner email is good enough to bet customer data on, and owning the consequences if it isn't, takes someone with real authority, and occasionally a phone call outside engineering.

## The discipline of forgetting

Archiving every prompt, scratch command, and Tuesday afternoon debugging detour builds sediment, not memory. The next maintainer needs the question, the decisive evidence, the call that was made, and its boundaries, not a transcript of three hours spent chasing the wrong log line.

Raw production dumps and huge traces are usually too sensitive or expensive to keep anyway. Reduce them to a minimal synthetic reproduction, and verify that the reduction didn't strip out the quirk that triggered the bug. Deleting duplicate explanations, swapping unsupported rules for explicit open questions, and retiring dead records are all real maintenance.

You can tell whether your memory is working the next time an external change lands, like that `upload_complete` webhook. Does the team quickly spot the gap between an informal email and a contract, notice the open question about downstream consumers, and know who to ask before dropping the timer? Or do they leave the delay untouched because three wiki pages echo the same unverified claim? Memory earns its keep when it makes revising an old choice safer than working around it.
