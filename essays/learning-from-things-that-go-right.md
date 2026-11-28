# Learning from things that go right

*What an uneventful migration can teach us*

Consider two hypothetical database migrations. In the first, a lock holds up customer requests and causes an incident. In the second, an engineer notices the same kind of lock beginning to form, pauses the rollout and changes the sequence. The migration finishes later that afternoon. No incident is declared.

The first team has an obvious reason to investigate. The second may close the ticket and move on. Yet the second migration contains questions worth asking. What made the lock visible? Why did someone recognize it as unusual? Could they pause without asking three other teams? What options remained once they did?

The successful outcome does not tell us whether the process was dependable or the team was fortunate. Reconstructing the work can help distinguish them.

## Success contains work we rarely record

Erik Hollnagel's Safety-II approach asks how everyday work achieves acceptable outcomes under changing conditions. In his [account of resilient safety management](https://webdeva.flightsafety.org/wp-content/uploads/2017/10/Hollnagel.pdf), understanding the adjustments people make is part of understanding safety. Examining failures remains necessary; examining ordinary success supplies evidence that failures alone cannot provide.

For the migration team, the written procedure might say to watch database latency. The engineer actually watches the age of waiting transactions because latency has not moved yet. They learned that distinction during an earlier investigation. Another colleague knows which service can tolerate a pause and is available to confirm the choice.

Some of the capability lives in the dashboard. Some lives in experience, working relationships and permission to act. Keeping only the final migration command would lose most of what made the adjustment possible.

This broadens what counts as a useful starting point for Compounding Engineering. A failure, a repeated interruption and a difficult review can all reveal an investment. So can an ordinary piece of work in which someone noticed a change, understood its significance and had room to respond.

## Reconstruct what people knew at the time

Begin with one moment when the work departed from expectation. Ask the participants to walk through what they could see, what they were trying to accomplish and which alternatives they considered. Bring the logs, messages or screens that informed the decision where those are available and appropriate to inspect.

Keep observation separate from interpretation. The queue grew; the engineer thought the migration might block a busy table; they paused. We know the queue then cleared. We do not know from that sequence alone how severe an incident would otherwise have been, or whether the chosen pause was the only effective response.

Ask what was difficult to see. Perhaps the dashboard had the right signal but the engineer needed three separate views to interpret it. Perhaps the pause command was undocumented. Perhaps a person who happened to be online supplied the missing context. These details suggest investments without turning a successful engineer into the subject of a performance assessment.

Also ask about uneventful cases where no adjustment was needed. If we study only dramatic saves, we can mistake exceptional improvisation for the normal way work succeeds. Choose examples that represent ordinary variation, including awkward cases with no heroic moment.

## Preserve the ability to respond

David Woods distinguishes *graceful extensibility* from simply surviving a familiar disturbance. His [theory of adaptive systems](https://doi.org/10.1007/s10669-018-9708-3) examines how systems extend their capacity to adapt when unexpected demands challenge their boundaries.

In the migration example, a rehearsed rollback may handle a known failure. Recognizing a new lock pattern and finding a different sequence requires more: useful signals, relevant expertise, available people and enough time to choose. Those resources cost something even on days when no incident occurs.

This makes spare capacity and overlapping knowledge legitimate investment questions. The second engineer's availability may look idle in a utilization report. It may also make an unfamiliar decision possible. That does not justify unlimited slack or duplicate teams. Ask which surprises the capacity helps handle, what it costs and what happens when it is unavailable.

Shared platforms can help by supplying reliable signals and reversible actions. They can also remove options if every team must follow the same sequence or wait for one central operator. A standard should make its exceptions workable as well as its ordinary path easy.

## Improve the conditions, then test the improvement

The team might retain a transaction-wait view, document the pause conditions or build a small rehearsal for the lock behavior. Pick the change that addresses the difficulty observed. A thirty-page account of a successful afternoon may be harder to use than an annotated trace and a runnable case.

Before automating the intervention, understand what the person was judging. Pausing whenever a transaction exceeds a fixed age might disrupt harmless workloads. The engineer may have considered the trend, the affected tables and the time left in the maintenance window. A proposed rule should be tried against cases where pausing would be unnecessary as well as cases where it would help.

AI can assemble a timeline and suggest questions, provided participants can correct its account. It can help prepare variations for a safe rehearsal. It cannot infer an avoided catastrophe from a tidy sequence of log messages, or decide that a workaround is expendable because it looks inefficient.

The [Successful work investigation pattern](https://grove.github.io/patterns-of-compounding-engineering/patterns/successful-work-investigation.html) describes a small way to try this. Use an existing review when possible. The purpose is to understand one consequential adjustment, not to require a report after every successful deployment.

On a later rehearsal, let another engineer encounter a changed version of the scenario. Can they find the signal, explain the uncertainty and choose an appropriate action? If they need the original operator to supply every judgment, the transfer remains incomplete. If the retained trace helps the team develop a new rehearsal, there is also a possible compounding link to investigate. Neither claim follows merely from the next migration finishing without an outage.
