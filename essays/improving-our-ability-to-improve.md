# Improving our ability to improve

*When one useful capability helps us build another*

Imagine a billing team investigating a duplicate credit. They keep the account state, the cancellation event and the expected result. A small replay catches the bug. On the next cancellation change, it catches a regression too. Keeping it has earned a return.

A month later, the team wants to know what happens if the worker stops after recording the cancellation but before issuing the credit. The earlier replay gives them a starting account and an agreed answer. They still have to add an interruption mechanism, inspect the storage guarantees and decide how recovery should work. But they can begin with a question about recovery instead of another afternoon reconstructing a customer account.

This hypothetical sequence contains the claim behind Compounding Engineering: work done to improve one task can make a later improvement easier. The second improvement matters because it develops something the team could not previously do.

## A capability needs somebody who can use it

The replay is an asset. The capability is being able to investigate a cancellation and reach a justified conclusion. That also takes an engineer who understands the result, access to the relevant environment and a way to resolve disagreements about the billing rule.

The distinction becomes obvious when a tool's author leaves. The repository may be intact, yet nobody can tell whether a failed check indicates a defect, an obsolete expectation or a broken fixture. The asset survived. The capability did not survive in full.

Describe a proposed capability as a job someone can do under named conditions: another billing engineer can investigate an interrupted cancellation in an isolated environment and explain which guarantees remain untested. That is more useful than saying the team owns a recovery framework. It tells us what to try and whom to involve.

## Two ways investments can reinforce one another

A scenario builder can increase the value of investing in independent billing checks: the checks have meaningful states to examine. Those checks can, in turn, make a better scenario builder worth developing, because the team can distinguish useful cases from misleading ones. Economists call this relationship *complementarity*: having one capability increases the value of investing in the other. Milgrom and Roberts examined how [complementary organizational choices](https://doi.org/10.1016/0165-4101(94)00382-F) can reinforce one another.

Complementarity describes how things work together. Compounding adds a claim about development over time: the capabilities we have make the next capability less costly or more effective to develop. The recovery example could show both, but we should investigate them separately. A useful combination might take so much work to assemble that it provides no advantage in building the next one.

Bruce Kogut and Udo Zander's [account of combinative capabilities](https://doi.org/10.1287/orsc.3.3.383) is a close theoretical relative. They describe organizations learning new skills by recombining existing capabilities, including the ways people cooperate. Martin Weitzman's [Recombinant Growth](https://doi.org/10.1162/003355398555595) studies the possibilities opened by combining ideas and the difficulty of finding useful combinations. These theories give us reasons to examine the mechanism. They do not establish that our billing team's investment will work.

For a team, the practical starting point is small. Pick a valuable task it cannot yet handle well. Name two or three existing capabilities that might help. Then identify what is missing between them: a shared identifier, a reviewed expectation, an interface, permission to use an environment, or somebody's understanding. The missing connection is often more consequential than another tool.

## Three kinds of work

Douglas Engelbart distinguished three activities in [Toward High-Performance Organizations](https://dougengelbart.org/content/view/116/): doing the organization's work, improving how it does that work, and improving how it improves. He called them A, B and C.

For the billing team, issuing a correct credit is A. Building a recovery check is B. Making it easier to design and evaluate the next kind of check is C. The same work can contribute at more than one level. A well-understood replay may help the engineer shipping a fix and the colleague developing a new experiment.

C does not deserve an automatic budget preference. A team with one awkward migration may need a disposable script and a clear decision. An elaborate method for improving migration tools would consume effort without a plausible next use. Improving improvement earns its place when it helps with work somebody actually needs to do.

AI can participate at each level. It can prepare the credit implementation, help construct the interruption experiment, or compare earlier investigations to find setup work worth sharing. Each contribution needs its own check. An agent that proposes a verification method should not be allowed to declare that method adequate merely because its own implementation passes.

## Follow the second investment

The [Capability composition pattern](https://grove.github.io/patterns-of-compounding-engineering/patterns/capability-composition.html) turns this into a bounded experiment. Before building the recovery check, the team writes down what it expects to reuse and why that should help. Afterward, it records what actually transferred, what had to change and how the new check was verified.

Include the inconvenient costs. Perhaps the replay assumes every operation finishes in one process. Extracting that assumption takes longer than creating a new fixture would have. Or the old cases are easy to run but no longer represent the billing policy. Reuse can preserve a mistake as efficiently as it preserves knowledge.

The [second-capability pilot](../research/second-capability.md) proposes a more careful comparison. An ordinary team can begin with a smaller observation, while acknowledging what it cannot establish. A faster second attempt might reflect a simpler task or a more experienced engineer. Showing exactly where the earlier investment helped is better evidence than comparing two ticket durations and attributing the difference to compounding.

## Leave room for the next attempt

An improvement cannot fund another improvement if its benefit never becomes usable capacity. Five scattered minutes saved across a week may be welcome without creating an afternoon for recovery work. A reduction in interruptions may free attention for the specialist while changing little for the rest of the team. Find where the benefit lands before allocating it.

Nor should every benefit be reinvested. Customers may need the released capacity now. The team may need breathing room after a difficult release. The [investment canvas](https://grove.github.io/compounding-engineering/adoption/investment-canvas.html) helps make that choice explicit without requiring a separate improvement programme.

On the next cancellation change, ask a colleague to try the recovery check. Can they explain the scenario, change a condition and recognize a result the check does not cover? If they can, the team has more than a retained script. It has evidence of a capability that another person can use and perhaps build on.
