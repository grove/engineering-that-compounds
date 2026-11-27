# What would ten times look like?

*A distant ambition for teams working with AI*

Imagine a team adding a credit for customers who cancel partway through a subscription. An agent prepares the change and a set of tests. During review, an engineer asks what should happen when cancellation arrives after the next invoice has already been issued. The tests give an answer. Nobody can say who agreed to it.

The patch waits while someone from the team finds the person who understands the billing policy. Producing another patch would be easy. Finishing this one requires a decision.

Our distant aim is to become ten times as effective as a team, with AI helping us do the work. We want to solve worthwhile problems that would overwhelm the team today, within sustainable working hours and with at least the same care for the people using the software. The number gives us a reason to examine the whole job. Whether we can reach it remains an open question.

For the team in this hypothetical example, the ambition raises an awkward question. If an agent could prepare ten times as many changes tomorrow, how many could they finish? Where would the others wait?

## Decide what we want more of

Before looking for a multiplier, name a useful result. The billing team wants customers to receive the right credit without a support agent spending an afternoon reconstructing their account. That result includes discovering the rule, implementing it, establishing that it works, releasing it and dealing with what happens afterward.

Ten times as many patches would tell us little about this. A change that eliminates a recurring billing mistake may be more useful than several new features. So might discovering, before implementation, that a proposed feature would make the problem worse.

The distant ambition therefore needs a more modest, concrete question nearby: what worthwhile work is currently too slow, too costly or too uncertain for this team to finish? Perhaps there are small customer problems that never justify the investigation. Perhaps a migration has been postponed because nobody can establish what it would break. Those are places to look.

AI might help investigate an unfamiliar path, prepare competing implementations or build a missing diagnostic tool. Whether that help makes the result cheaper depends on the work needed to direct it, check it and keep the resulting software useful. That is something to find out on an actual change.

## Follow the constraint through the work

Return to the cancellation. The team agrees on the policy with the people responsible for billing. For this example, they decide to leave the issued invoice unchanged and create a separate credit for the unused part of the new period. Repeated notifications of the same cancellation must not create additional credits. They work through accounts on either side of the renewal date, and someone checks the expected amounts against the policy before those expectations become tests.

An agent can help find cases the team has overlooked and turn the reviewed examples into a runnable check. It can also expose a disagreement. If the policy is still unsettled, generating more tests will only give the disagreement more places to hide.

On the next change, an engineer can find the rule and run the cases. Perhaps the expensive part is now recreating the right account state. A small scenario builder could remove that setup work. The team tries it on another cancellation case and asks a colleague who was absent from the original discussion to use it. Where does that colleague still need help?

Suppose the new check reveals that calculating the credit and issuing it are tangled together. Checking a calculation requires a payment-provider sandbox and a shared database. Two investigations interfere with each other. Extracting the calculation behind a clear interface might let each run with its own inputs. The retained cases give the team a starting point for checking the separation, while integration checks still have to establish that the right credit is issued once.

There is no prescribed order here. Another team might already have excellent tests and spend most of its week waiting for access to an environment. Or two changes might depend on the same policy decision and belong together. [Architecture for parallel work](./architecture-for-parallel-work.md) examines that distinction. Starting more agents will not make a shared decision independent.

Nor does every interruption need removing. An engineer encountering the billing system for the first time needs to understand why a repeated event is possible and predict what the handler will do. That investigation develops judgment the team will need during a failure. The [ability to delegate](./the-ability-to-delegate.md) includes knowing which work benefits from supervision.

After several improvements, the team may be able to prepare and verify billing changes readily, yet still be unsure which changes customers need. The next useful investment could be a conversation with support or a way to examine disputed invoices. The constraint has moved beyond the code. The tenfold ambition should give us permission to follow it there.

## Make one improvement help build another

The cancellation cases can help on several later changes. That is a return on keeping them. Compounding makes a further claim: earlier work can make a new capability cheaper or more effective to build.

Consider a later effort to recover safely from an interrupted credit operation. The team already has an account state, an agreed expected credit and a way to replay the cancellation. It can use those to build a check that stops processing between named steps and then resumes. It still needs to implement the interruption mechanism and establish what the storage and payment interfaces guarantee. The original test cannot answer those questions.

Now there is a specific connection to investigate. How much of the recovery check came from the earlier work? How much new work remained? Did adapting the old scenario help, or did its assumptions make the investigation harder? [Engineering capital](./engineering-capital.md) gives this connection a name; [Measuring the capacity for change](./measuring-the-capacity-for-change.md) asks how we could test it.

This is also a reason to spend some recovered time on the next obstacle. If every saving is immediately filled with more feature requests, the team may never get round to the verification work that would make a larger change possible. The appropriate investment may be small: one diagnostic command or the removal of an unnecessary handoff. A distant ambition does not require a large improvement programme.

## Count what the improvement costs

Suppose the billing team makes the scenario builder increasingly general. It acquires configuration for plans nobody sells, elaborate fixtures for a retired payment provider and a second language for describing account state. The original cases become hard to read. Maintaining the tool now takes longer than setting up the few cases the team actually needs.

The right response could be to shrink it. Keeping a handful of explicit examples might preserve most of the benefit. The tenfold ambition gives us no reason to keep an investment that makes useful work harder.

For the next few comparable changes, record enough to see where the effort went. Include investigation, agent supervision, review, failed attempts, release work and repairs. Keep elapsed waiting separate from engineering effort, and record compute costs alongside them. Notice whether support or another team has inherited work that disappeared from the developers' accounts. Check the resulting behavior as well as the time taken.

An improvement in a small activity remains a small part of the team's total work. Tenfold gains in two different tasks cannot simply be multiplied together. Nor should easier tasks be compared with harder ones and presented as progress. A narrow result can still be useful: another engineer could complete the same kind of investigation with less help, and the evidence held up when something went wrong.

There is no single number that will settle all of this. We can be ambitious about where we want to go while being precise about the improvement we have actually observed.

## Choose the next attempt

The [tenfold exercise in the field guide](https://grove.github.io/patterns-of-compounding-engineering/guide.html#use-the-tenfold-ambition-to-choose-the-next-investment) starts with a recent change and follows the effort from the original need to a useful result. It asks where more implementation capacity would have helped, what actually held the work up, and which small investment might change that.

For our billing team, the first attempt is straightforward. Settle the cancellation rule, retain a few reviewed cases, and let another engineer try them on the next relevant change. See whether the repeated investigation goes away and what becomes difficult instead. That will tell them more about where to invest next than a plan to automate the entire billing backlog.
