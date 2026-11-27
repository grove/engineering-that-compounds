# What software should remember

*Keeping reasons available, and open to revision*

```text
# Wait 20 minutes before exporting; partner sometimes revises files after upload.
EXPORT_DELAY_MINUTES = 20
```

Every mature codebase has a line like this: a constant, a sleep, or a defensive branch paired with a one-sentence comment that looks reasonable enough to leave alone. In a hypothetical export service holding that delay, the code explains *how* it waits and the tests confirm *that* it waits.

Then the partner adds an explicit `upload_complete` webhook. Can the twenty-minute delay go?

Reading the code will not tell you. Did the partner actually guarantee no edits after that webhook, or did someone merely notice it in a test run? Were late file revisions the only reason for waiting, or does an accounting job downstream lean on the gap? Was twenty minutes measured from real upload logs, written into a contract, or plucked out of thin air because it felt generous?

A good coding agent can trace every caller of `EXPORT_DELAY_MINUTES` in seconds. What it cannot recover is evidence that was never written down. Worse, if asked why the delay exists, it will happily synthesize a fluent explanation that sounds authoritative and gets the real reason wrong.

That is the job of engineering memory: leaving a future maintainer enough of the past to decide what can safely change today.

## Reasons that outlive the choice

Michael Nygard's [architecture decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) remain one of the cleanest tools for this: a short note capturing context, decision, status and consequences. When circumstances change, you supersede the old record rather than silently editing history, so a reader can tell what is still in force from what used to be true.

Ordinary wiki pages fail in the opposite way. A page about the export job starts out accurate. Five edits later, it blends the original rationale with current implementation details and an untested guess from a Slack thread. Nothing looks obviously broken, yet nobody can tell which sentences still have evidence behind them.

A decision record for the twenty-minute delay does not need to be long. What it needs is the basis for the claim and the conditions that should make someone reopen it:

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

That last section does the real work. Without reconsideration triggers, a decision record turns into a polite monument telling future engineers not to touch anything. With them, the new webhook immediately tells a maintainer that the original assumption has broken and deserves a fresh look.

You will never anticipate every future shift, and you do not have to. Even a plain sentence ("assumes uploads can be overwritten after they first appear") gives the next person far more traction than "required for reliability."

## An observation is not a promise

Look at three statements that might turn up in notes about the export pipeline:

- The partner's API contract promises a completed upload will never be revised.
- Last month's logs show zero revisions after completion.
- Our importer ignores any revision arriving after the first read.

All three describe the same surface behavior, yet they license completely different decisions. The first is an external obligation whose scope you can verify. The second is a limited sample. The third is our own design choice. Collapsing them into *"completed uploads never change"* destroys the exact distinction a future engineer needs when deciding whether to drop the delay.

Busy humans perform that compression all the time. LLMs perform it automatically; smoothing messy, qualified notes into clean prose is what they are tuned to do. The cleaner the summary reads, the harder it becomes to spot what was dropped.

The [W3C provenance model](https://www.w3.org/TR/prov-overview/) puts a formal vocabulary on this by tracking the entities, activities and agents behind a claim. You do not need the XML or RDF machinery on an application team; you only need the habit of keeping a conclusion tied to how it was produced. For a benchmark, point to the commit, workload and hardware. For a business rule, name the owner and policy document. For an inference, label it as an inference.

Provenance does not make a claim true. It makes the claim inspectable, and a rough observation with visible limits is far safer to work with than a confident assertion with no visible origin.

## Keep memory near the question

A thoughtful decision record buried in a separate portal might as well not exist. Engineers look for reasons at the point where they are about to change something.

Wire the link in both directions. The constant `EXPORT_DELAY_MINUTES` points to the decision record; the record names the scheduler and the tests that enforce it. When a protocol test fails, it links straight to the assumption it checks, so the maintainer learns *why* the behavior mattered before deciding whether to fix the code or update the test.

Short cross-references beat copying explanations into five files, because copies drift on their own schedules.

Put whatever can be checked mechanically into executable tests, such as verifying that duplicate deliveries of a completed upload remain idempotent across worker restarts. Just make sure the test checks the contract we intend to honor rather than mirroring whatever the current implementation happens to do.

Plenty of crucial knowledge will still stay outside code. No test suite can tell you whether a partner's commercial promise is credible, or whether a twenty-minute delay annoys customers. Turning a judgment into a constant does not eliminate the judgment; it only hides it unless you keep the reasoning nearby. The same discipline applies to [abandoned experiments](./the-value-of-forgotten-alternatives.md): keep the path from the question to the evidence that settled it.

## Memory goes stale, and silent rewrites make it worse

Automated checks can verify the easy parts of memory: that a linked file still exists, a reproduction still runs, or a documented schema still matches production.

The harder claims do not become current just because a calendar reminder fired and someone clicked "reviewed." An agent comparing the decision record against the code can verify that both still match while completely missing that the partner changed its upload process three months ago.

The right time to revisit a record is when something relevant shifts: a completion signal arrives, a new downstream team starts reading the files, or a customer asks for five-minute latency.

When fresh evidence contradicts an old record, leave the friction visible. Rewriting the earlier explanation to match today's understanding makes the docs look tidier while erasing the trail that something unexpected happened. Mark the older record superseded, link the incident or change that challenged it, and keep the current summary brief.

This is also where automated memory maintenance hits a wall. An agent can flag that a claim looks contradicted or stale. Deciding whether an external partner guarantee still holds usually requires a human with authority, and sometimes a phone call outside engineering.

## The discipline of forgetting

Logging every prompt, scratch command and half-baked hypothesis does not create institutional memory. It creates sediment. Future maintainers drown in the story of how someone happened to spend Tuesday afternoon when all they needed was the question, the decisive evidence, the conclusion and its boundary.

Raw production traces and huge datasets are often too sensitive or expensive to keep anyway. Reduce them to a minimal synthetic reproduction, provided someone verifies that the reduction didn't strip out the exact quirk causing the bug.

Separate history from active guidance. Archived decisions belong out of the default search path, clearly flagged as superseded, for both humans and coding agents reading the repo. Deleting duplicate explanations, replacing unsupported rules with explicit open questions, and retiring dead records are all forms of maintenance.

## A simple test

You do not need a knowledge platform to find out whether your system remembers the right things. Hand the export job to an engineer who has never touched it and ask one question: *can we remove the twenty-minute delay?*

Watch where they go. If they find the original failure, see the difference between the partner's email and a formal guarantee, and spot what needs checking before the webhook can replace the timer, the memory is doing its job. If they can only read back what the code currently does, or worse, leave the delay untouched because three wiki pages repeat the same unverified claim, the memory is getting in the way.

Good memory does not tell the next maintainer what to conclude. It gives them enough ground to ask a better question, and enough honesty about past uncertainty to change the answer.
