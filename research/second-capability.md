# Does one capability help build the next?

*A proposed pilot for testing a specific compounding mechanism*

**Status: proposed protocol. No participants, runs or results are reported here.** This is a plan someone can adapt and register before collecting evidence. The [measurement essay](../essays/measuring-the-capacity-for-change.md) explains the broader argument and a lighter field check for ordinary team work.

The question is narrow: does retaining a reproducible scenario make a later recovery check cheaper to build, or better at detecting faults, after counting the work of adapting that scenario? A useful second step need not repay the first investment. Measure both.

## Prepare the comparison

Start with one small application and two successive tasks. The first asks participants to fix an observable failure. The second asks them to build a new verification capability for a related but previously undisclosed requirement. A restart or interrupted transaction is one possible setting.

The [evolving billing lab](https://grove.github.io/patterns-of-compounding-engineering/examples/evolving-billing/) can teach participants the kind of work involved. Its published sequence and solutions are unsuitable as hidden evaluation tasks. Have a reviewer prepare fresh variants, independent acceptance cases and a final maintenance change before any participant begins. Keep the task packages sealed until their rounds, record their hashes in the protocol, then release them with the results. Record prior exposure to related examples.

For a diagnostic pilot, plan four independent pairs of runs on the same starting revision. A pair can be two similarly experienced engineers or two fresh agent sessions with the same model, tools and resource limits. Use one participant type for a comparison; do not pool human and agent results. Randomize the assignment within each pair. A person should not attempt both conditions on the same application, and an agent session must not see another run's conversation or files.

- **Ordinary practice:** complete the first task using the participant's usual development approach. Permit normal tests, refactoring and incidental helpers.
- **Deliberate investment:** complete the same task and retain the smallest reusable scenario and check likely to help related work. An existing test may be enough; do not require a new framework.

Both conditions receive the same acceptance rules and total resource budget. This compares development strategies. It does not isolate the artifact from what its author learned while building it.

## Fix the budget and acceptance rules before starting

Choose the time cap for each round, total inference allowance where applicable, and allowed tools before assigning conditions. Record model and harness versions, repository revision, participant experience and any permitted help. Keep the limits identical within each pair. A dry run with separate participants can establish whether the tasks fit the caps; exclude it from the comparison and document any revisions.

Agree on what the second capability must demonstrate: for example, reject a handler that records an event before applying its effect, reject one that applies the effect before recording it, and accept an atomic correction. Include a valid case that resembles the failure so an overbroad check cannot succeed by rejecting everything. Specify the recovery contract independently of both implementations.

Use an assessor who did not produce either solution. Where practical, hide the assigned condition during scoring. Freeze the acceptance cases; preserve changes to them as protocol deviations rather than silently correcting an inconvenient test after seeing results.

## Run three rounds

1. **Fix and retain.** Give both conditions the initial failure and the same deadline. Record feature correctness, verification, review and any reusable work. Preserve unsuccessful attempts and unfinished work. The ordinary-practice condition may produce a good harness too; record that overlap.
2. **Build the second capability.** Reveal the new requirement. Allow each participant to use only its own earlier output and the common starting resources. Count discovery, implementation, adaptation, debugging, review and help through independent acceptance or the cap. Record which earlier assets were actually used and which were bypassed.
3. **Maintain it.** Reveal the prepared change to a relevant input or contract. Ask participants to adapt the new check without weakening the revised acceptance standard. Count the repairs and assess the result again. This gives one observation of upkeep; it does not estimate a lifetime maintenance bill.

Do not extend a cap to rescue one condition. Retain a failed or timed-out run in the report. If a protocol defect makes a run invalid, give the reason and report it alongside any replacement. Do not stop collection when the preferred result appears.

## Report quality and cost separately

For each run, report acceptance outcomes and elapsed and active effort for each round. Include all participants' review and support time, inference use, abandoned attempts and repairs. Keep waiting time separate. Report which work was displaced by the initial investment, if the first round included optional delivery work.

Use the same small record for every run:

```text
Run / condition / starting revision:
Participant or model and harness version:
Round caps / inference allowance:
Round 1: correctness; active effort; retained assets
Round 2: acceptance results; effort; reused assets; adaptation and help
Round 3: acceptance results; repair effort
Failed attempts, bypasses and protocol deviations:
Total effort / elapsed time / inference use:
```

Show every pair, including failures, before summarizing. Do not average successful runs alone, turn a timeout into a fast completion, or combine correctness and speed into an unexplained score. Four pairs can expose feasibility problems and suggest what to investigate next; they are not a basis for a broad productivity claim. A larger study needs a sample-size and analysis plan appropriate to its question.

## Decide what the result supports

A cheaper second capability at the same acceptance standard supports the proposed mechanism in this setting. Better fault detection for comparable effort may support it too. If total effort remains higher, report that the second step benefited while the overall investment has not paid back within the study.

If adaptation erases the benefit, or ordinary practice produces equally useful capabilities, report that result. If differences are too variable to distinguish, call the pilot inconclusive. Decide whether to narrow the investment, try another task family or stop. None of those decisions needs a success story.

The pilot tests one connection between two capabilities. It does not demonstrate sustained compounding, production reliability or AI amplification. Testing whether the effect carries into a third capability needs another unforeseen task; testing AI interaction needs the separate comparison described in the [measurement essay](../essays/measuring-the-capacity-for-change.md).
