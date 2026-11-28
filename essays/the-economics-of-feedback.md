# The economics of feedback

*What changes when a useful answer is cheap enough to ask for*

Imagine an engineer checking a cancellation calculation. The calculation takes milliseconds. Finding out whether a proposed change works requires a shared database, a deployment to staging and a place in the test queue. By the time the result arrives, the engineer is reviewing something else.

An agent could generate three variations of the patch while the first waits. That would create more unfinished work. The immediate opportunity is to make one important question easier to answer.

In this hypothetical team, extracting the calculation behind a small interface might allow a local check. The change is worthwhile only if the check answers a useful question reliably. A fast simulation of the wrong billing rule would make mistakes easier to repeat.

## Follow the question all the way to a decision

The feedback loop begins when somebody has a question and ends when the answer can change what they do. Execution time is one part. Preparing the environment, waiting for access, interpreting the result and finding someone who can act on it also belong in the account.

Tim Cochran's [Maximizing Developer Effectiveness](https://martinfowler.com/articles/developer-effectiveness.html) examines the many feedback loops in an engineer's day, including the small ones whose repeated friction is easy to overlook. Donald Reinertsen's work on product development flow examines the economics of queues, batch sizes and work in progress; his [presentation on second-generation lean development](https://www.infoq.com/presentations/2nd-gen-lean/) gives an accessible introduction to those tradeoffs.

For the billing team, a useful observation is concrete: when did the engineer decide to check the cancellation, when did they get an interpretable result, and what happened between those moments? Keep waiting separate from effort. A twenty-minute automated run may consume little attention if its result arrives at the right time. A quick run that needs repeated repair can be far more disruptive.

There are several possible repairs. A local calculation check can answer arithmetic questions. A contract test can catch disagreement at an interface. A production observation may be needed to discover whether customers understand the credit. Each shortens a different loop. None replaces all the others.

## Faster feedback can change the work people attempt

When every experiment requires a deployment, an engineer has a reason to choose a promising design early and avoid reopening it. If meaningful alternatives are cheap to check, trying a second design may become sensible. The possible benefit is a better decision as well as time saved.

That is a hypothesis to observe. After building the local check, did the team investigate a useful alternative? Did a defect become visible before the implementation grew around it? Did another person use the check without recreating the original setup? A higher test count alone answers none of these questions.

Faster feedback can also increase noise. An agent may generate many superficial alternatives because it can. Somebody then has to compare them. Before starting, name the disagreement the experiment should resolve and the result that would change the choice. Stop generating variants once that question has a sufficient answer.

For example, suppose the team is deciding whether to calculate a credit at cancellation time or at the next invoice. Test a case where the price changes between those events. Ask the policy owner what result is intended, then compare the designs against it. Running ordinary same-price cases a thousand times would not resolve that disagreement.

## Leave capacity to receive the answer

Queues can form even when average demand is below average capacity, because arrivals and task durations vary. As utilization approaches the available capacity, that variability can make waiting much worse. The [Open University's queueing explanation](https://www.open.edu/openlearn/society-politics-law/criminology/capacity-and-demand-management/content-section-11/) demonstrates the distinction between a persistent overload and queues caused by variation.

This is a reason to examine capacity, not a universal utilization target. A team handling unpredictable support escalations may need more room than one running a stable batch process. Reserving some specialist time for questions can shorten the loop if those questions are what hold useful work up. Filling the specialist's calendar because there was a quiet afternoon can undo that benefit.

For AI-assisted work, limit how much uncertain work is admitted to review. If agents can produce changes faster than the team can evaluate them, more generation can lengthen the delay before anyone learns that an assumption was wrong. Have the agent prepare a smaller change, obtain evidence during execution and pause when a necessary decision is missing.

## Check whether the answer deserves trust

A useful feedback loop distinguishes alternatives. If the implementation and its expected results were generated from the same mistaken interpretation, agreement between them proves little about the intended behavior. The billing expectation should come from a reviewed policy and cases that would expose the relevant mistake.

Ask what a passing check leaves open. A local calculation check may say nothing about issuing a credit twice after a restart. A staging exercise may use a dataset too small to expose a lock problem. Keep those limits beside the command so that a quicker answer does not become broader confidence than the evidence supports.

There is a cost to adding scrutiny too. Requiring a full staging run for every wording change might delay useful feedback without reducing a relevant risk. Match the check to the decision and retain the more expensive evidence where its coverage matters.

## Try one shorter loop

The [Shorten the learning loop pattern](https://grove.github.io/patterns-of-compounding-engineering/patterns/shorten-the-learning-loop.html) starts with one repeated question. Observe the current route to an answer, make a bounded change, and try it on later work. Include setup, interpretation, false alarms and upkeep when deciding whether to keep it.

Then look for a second question the new capability might help answer. The cancellation check could supply inputs and expectations for a recovery experiment. That would be a possible compounding effect, separate from the recurring benefit of faster checks. It deserves its own investigation.

If the team now gets a reliable answer quickly but still waits days for a policy decision, follow that delay. Making the test another second faster would be easy to measure. It would also leave the engineer waiting for the same person.
