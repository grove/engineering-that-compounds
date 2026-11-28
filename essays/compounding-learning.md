# Compounding learning

*How AI can help teams learn from recurring problems*

Consider a hypothetical billing team. Several recent pull requests contain the same review question: what happens if this payment event arrives twice? Each author adds a test. Each change ships. On the next ticket, someone asks again.

An agent could collect those comments and write a lesson about duplicate delivery. It could also add a reminder to every pull request. Neither tells the team why the question keeps coming up. Perhaps the engineers do not understand the risk. Perhaps they understand it perfectly and cannot easily construct the test. Perhaps the service has no agreed rule for what counts as the same payment.

Those explanations call for different investments. Getting that choice right is part of engineering work, and AI can help with the investigation as well as the implementation.

The earlier essays describe what teams retain: judgment, executable checks, useful rationale and boundaries that let people work independently. Learning is how experience changes those things. It can compound when an earlier investigation makes a later capability cheaper or more effective to develop. The way we investigate can itself be one of those capabilities. AI gives us more ways to try this; later work has to tell us whether they helped.

## Find the question behind the repeated work

Start with the difficulty somebody can point to. The billing team chooses a small set of recent payment changes, including ones that passed review without the reminder. It asks an agent to find the relevant comments, link each one to the code and test it concerned, and identify differences between the cases.

That is a useful assignment because the output can be checked. A reviewer can open a source, reject a misleading match and notice a case the agent missed. A free-ranging request to discover everything the organization should learn is much harder to assess and creates a queue of suggestions for somebody else to read.

Even this narrow search needs care. Two comments can mention retries while referring to different problems. One may concern repeated delivery of the same event. Another may concern two distinct events for one business operation. The same test does not necessarily answer both. Ask the agent to preserve those distinctions and the evidence that challenges its grouping. A cluster of similar sentences is a lead to investigate.

Then talk to the people who did the work. Review history records what somebody chose to write down. It may omit the half-hour spent getting a fixture to run or the product discussion that settled the expected result. AI can help find the conversation worth having; the repository does not contain every reason a change was difficult.

The [Friction to hypothesis](https://grove.github.io/patterns-of-compounding-engineering/patterns/friction-to-hypothesis.html) pattern turns this into a small investigation: name the difficulty, keep competing explanations open and choose a check that could distinguish them.

## Test the explanation before saving the lesson

Suppose the billing engineers can explain duplicate delivery clearly. Watching someone add the test reveals a different problem: constructing a paid invoice requires unrelated account, pricing and subscription setup. They postpone the test until review because the fixture is awkward to adapt.

Now there is a specific hypothesis: a small way to construct the relevant state would make duplicate-delivery checks easier to add before review. An agent can propose the helper and a few cases. Before accepting them, the team agrees on the expected behavior independently of the generated implementation. Delivering the same event ID twice should apply its effect once; delivering two distinct, valid payments should apply both. A check that rejects every second payment is wrong even if it catches the original bug.

Write down what would distinguish the explanations. If setup is the obstacle, an engineer who understands the rule should complete the check more easily with the helper. If the rule itself is unclear, easier setup will leave the disagreement intact. This follows the discipline of [Plan-Do-Study-Act](https://deming.org/explore/pdsa/): make a prediction, compare it with observations and revise the explanation. A passing test alone cannot settle why the original work was difficult.

Try the helper on a bounded change with an engineer who did not build it. Watch what they need to discover, what they misunderstand and where they ask for help. Include the time spent inspecting generated tests and correcting false alarms. The first attempt may show that the helper merely moves a complicated setup into an undocumented function.

If people disagree about whether two events represent the same payment, stop the tooling experiment long enough to settle that rule. Generating more tests would freeze the disagreement into code. If the fixture turns out to be easy already, investigate another explanation or leave the workflow alone. Ruling out an unnecessary improvement can save more work than implementing it.

Whether AI saves time in this hypothetical depends on the work the model removes and the work needed to check it.

## Question the rule behind the work

The billing team may uncover a different problem: every payment change needs a senior engineer's approval, even when the agreed checks pass. Preparing better approval notes could shorten the wait. First ask what the approval protects.

Perhaps it was introduced when ledger writes could bypass validation. If that path has since been removed, the rule may need a narrower scope. If reviewers still catch ambiguous refund policies, the approval serves a purpose that more automated tests will not remove. Bring that evidence to the person responsible for the rule and agree on a bounded change or keep it.

Argyris's [double-loop learning](https://store.hbr.org/product/double-loop-learning-in-organizations/77502) includes questioning the policies and objectives that govern a correction. The useful habit is to ask what would justify changing the requirement as well as how to meet it. [Getting better at the wrong thing](./getting-better-at-the-wrong-thing.md) follows that question further.

Look at the changes that went smoothly too. Perhaps another engineer noticed the ambiguity early and called a product specialist before writing code. Find out what they noticed and how they knew whom to ask. The lack of a review delay does not tell you that no effort was required. A [successful work investigation](https://grove.github.io/patterns-of-compounding-engineering/patterns/successful-work-investigation.html) helps recover that otherwise invisible work.

## Keep what the next person needs

If the helper proves useful, keep it where the payment tests already live. Put the example beside it, with the assumption that event IDs remain stable across redelivery. Link the short explanation to the investigation that established the rule. Name who will revisit it if the provider changes that contract.

When the contract changes, revisit the lesson and its consumers together. Mark the old assumption as superseded, update the check and find the guidance that still recommends it. An agent retrieving an obsolete rule can undo the benefit of having made it easy to find. Consequential rules need an owner and a reason to review them; a date alone should never silently disable a safety control.

The rejected explanations may deserve a sentence too. Knowing that engineers understood the rule but struggled to construct the state could prevent the next retrospective from prescribing another training session. Keep enough evidence to check that conclusion and resume an unfinished question; discard intermediate summaries once they add nothing.

The next ordinary payment change gives the team its first useful evidence of return. Can another engineer find the helper, use it correctly and finish the check with less effort at the same standard? [Verified retrieval](https://grove.github.io/patterns-of-compounding-engineering/patterns/verified-retrieval.html) addresses that handoff. A file in the repository establishes that something was stored. Watching later work establishes whether it helped.

Compounding requires another connection. Suppose a later change needs to check what happens when a worker restarts between receiving and recording a payment. If the existing scenario makes that recovery check cheaper or more effective to build, there is a candidate compounding effect. Record what was reused and what had to change. The sequential duplicate-delivery test does not establish crash recovery or coordination between workers; those need their own contracts and checks. The [evolving billing lab](https://grove.github.io/patterns-of-compounding-engineering/examples/evolving-billing/) illustrates that distinction with synthetic, runnable stages.

## Let the knowledge travel where it fits

The helper might also support a practice exercise. Ask a newcomer to predict the ledger after a repeated event, then change one condition and ask for another prediction. An agent can prepare variations; an experienced engineer checks that they exercise the intended distinction. Later, use a different failure to find out whether the newcomer can choose and defend a useful check. Recognizing the answer to an exercise they have already seen tells us less. [How engineers become engineers](./how-engineers-become-engineers.md) develops this approach to judgment.

A neighboring refunds team may need the lesson too, but its event contract could be different. Give it the question and the evidence, then let its engineers decide whether the check applies. An agent can locate likely consumers and help adapt an example within the teams' access boundaries. [Organizations that improve with age](./organizations-that-improve-with-age.md) explains the ownership and funding this transfer needs.

The fixture may serve billing well and have no useful life elsewhere. The new learning may instead justify deleting a misleading check or keeping a decision with an engineer. Choose the next use because someone needs it, and give that person time to try it.

## Find out whether the investigation got better

The fixture and the method used to discover it are separate investments. The team could build a useful fixture after an expensive, distracting search through irrelevant review comments. In that case the tool may deserve to stay while the search should change.

At the next retrospective, look at the actual decisions. Which agent suggestion led to a useful question? Which needed so much correction that reading the original reviews would have been quicker? Did it miss a recurring problem the team already knew about? Include rejected suggestions, investigation time, model costs and interruptions to other people. Counting generated lessons rewards a busy agent regardless of whether anybody learns.

Perhaps the team finds that reviewing every merged change produces mostly noise. It could restrict the search to a recurring review delay, or run it only when an incident raises a specific question. A plain script may be enough to collect the relevant changes. Use AI where comparing explanations or unfamiliar evidence helps, and ordinary programs where the task is already well defined.

If the selected sources and comparison procedure help investigate a later, different difficulty, record that connection too. Did the earlier work reduce the cost of developing a better diagnostic or experiment? Could the next investigator use it without the original author? The investigation method has become one of the capabilities being tested.

The [measurement essay](./measuring-the-capacity-for-change.md#check-the-learning-method-too) suggests what to observe. Its [proposed research extension](../research/second-capability.md#a-separate-comparison-of-ai-assisted-investigation) separates the value of an AI-assisted investigation from the value of the capability it recommends. The proposed comparison has not been run.

## Keep the disagreement visible

The person responsible for a service still has to decide whether a proposed lesson holds. A generated explanation can omit an inconvenient counterexample or turn a tentative convention into a rule. Keep the source and the conditions of use attached to the conclusion, and make it easy for the next engineer to challenge both.

The same applies to learning about people. A repeated review comment is evidence about a change and its workflow. Using it to rank engineers gives people a reason to hide the very difficulties the team needs to understand. Agree on the scope of the investigation, use material the team is authorized to inspect, and evaluate the work rather than producing individual performance scores.

An agent can draft a better check or investigation procedure on a branch. Changes to acceptance rules, permissions or automatic enforcement still need the responsible reviewer. A failed attempt is no reason for the agent to lower its own standard of success. The [automation essay](./automating-the-work-of-engineering.md#let-the-exceptions-improve-the-job) makes this boundary concrete.

On the billing team's next payment change, the useful question is simple: does somebody still need to ask for the missing check? If so, open that case and find out why. It may reveal a flaw in the helper, a new business rule or a mistaken explanation of the original problem. That is the next piece of work.
