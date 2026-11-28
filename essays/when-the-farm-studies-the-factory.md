# When the farm studies the factory

*An investigation should be allowed to change what gets built*

A software factory needs work whose purpose is sufficiently clear to carry through to a result. A software farm starts with a question whose answer may change that work. Putting them together creates an interesting possibility: the organization can investigate the machinery through which it delivers software while continuing to use it.

It also creates an obvious failure mode. The factory produces changes faster, the farm produces suggestions faster, and the same few engineers must inspect both. The organization acquires a larger queue and calls it learning.

To make the relationship useful, follow one question all the way through to a decision, a change and its later consequences. We will use a hypothetical reporting team. Its factory handles routine changes to scheduled customer exports. Agents can prepare and check the implementation, but an experienced engineer still has to explain which records belong in almost every export. The team wants to know why.

## Give the investigation a decision to inform

"Find ways to improve our factory" is a poor starting assignment. Almost any inconvenience could justify a plausible recommendation. There is no natural limit to the findings and no clear reason to choose one over another.

The reporting team has a more useful question: can it reduce the repeated work of establishing what an export means? The answer could justify a shared account of the business rules, a change to the product, a better verification method, or leaving review with the specialist. The investigation is worthwhile if it helps choose among those options.

The product lead and an engineer responsible for the reporting system agree on the scope. They will examine several recent changes, include one that went smoothly, and talk to the people who requested and reviewed them. They set aside time for the investigation and for checking its conclusions. An agent can help recover source material and compare cases within that scope.

These are responsibilities within an existing team. The farm need not be a new department or a standing population of agents. At this stage it is a deliberate way to organize uncertain work, with someone responsible for deciding whether its answer is useful.

Its output should make a decision possible. A list of suspicious code, a dozen rewritten documents or a proposed platform may be intermediate material. The team still needs an explanation of the difficulty, evidence that distinguishes it from other explanations, and a bounded next step.

## Study the work people actually do

The delivery history shows repeated requests for additional examples. An agent groups these as missing test coverage. It recommends expanding the test suite.

That is a reasonable lead. Watching the specialist review an export reveals something else. She spends much of her time tracing the word "active" through different reports. One report includes accounts active at the end of a month. Another includes accounts with any activity during that month. A third includes only accounts whose setup has been confirmed. Their fixtures contain similar-looking records and different expectations.

Additional tests could preserve all three definitions without explaining when each applies. A shared helper named `active_accounts` could make the situation worse by choosing one definition silently.

The farm follows the ambiguity to the people using the exports. One customer reconciles its month-end account list. Another needs to see every account used during a period. A third asks for a weekly report only because the product's existing screen omits the confirmation status.

Now the investigation has changed the options. Two exports have distinct purposes that need to remain explicit. The third may be avoidable. The apparent problem with testing was partly a problem with meaning and partly a missing product capability.

This is where a farm needs contact with the world outside the repository. Delivery logs describe work that entered the factory. They do not explain all the needs that caused it, or the needs that never became tickets. [When software forgets the world](./when-software-forgets-the-world.md) examines the cost of treating internally consistent evidence as a complete account of what people need.

## Let a finding remove work

Suppose the investigation shows that exposing the missing account status in the product would let the third customer do its work without the weekly export. The product owner can choose that change and cancel the proposed export automation. The factory then has a smaller, different assignment.

The farm should receive credit for establishing that choice even though it produced no new recurring workflow. If its success is judged by the number of proposals accepted into delivery, it will learn to create work. If the factory's success is judged only by changes completed, it will prefer the original backlog. Both measures would penalize a useful result.

Cancellation still needs a responsible decision. A customer may rely on an export in ways the investigation missed, or need it to satisfy an existing agreement. The farm brings evidence to the person who can change the commitment. It does not remove the report on the strength of a model's suggestion.

The remaining exports might justify keeping their definitions, reviewed examples and history together. That investment should be small enough to try on an actual change. The team does not need to redesign every report before discovering whether a more explicit account of "active" helps a different engineer establish the right result.

The [transformation experiments guide](https://grove.github.io/compounding-engineering/adoption/experiments.html) offers a way to frame that trial. The significant step is choosing evidence that could make the team abandon its preferred explanation. If the specialist still has to reconstruct the customer need each time, the retained definitions have not resolved the difficulty.

## Keep judgment close to the consequences

An investigation can propose several kinds of change, and they need different decisions. The reporting engineer can repair a fixture. The product owner decides whether a customer-facing meaning should change. The person responsible for the delivery workflow decides whether new evidence is sufficient to remove a recurring review.

Keeping those responsibilities explicit prevents the farm from becoming a source of unowned advice. The person receiving a proposal needs to understand both the evidence and the cost of acting on it. They should be able to reject it, ask a sharper question or choose a different experiment.

There is a particular problem when the proposal changes how the factory judges its own output. An agent might notice that a check often blocks a change and suggest relaxing it. The check may be obsolete; it may also be catching exactly the mistake it exists to catch. Examine known failures and valid counterexamples before changing the standard. The program attempting the change should not also grant itself permission to accept less evidence.

[StrongDM's account of its software factory](https://factory.strongdm.ai/) describes behavioral scenarios, including scenarios kept outside the implementation's codebase, and replicas of external services used for evaluation. That first-party account suggests a useful distinction between producing a candidate and evaluating it. It does not establish that a separate scenario set is correct or complete. Someone must still examine whether the scenarios represent the intended behavior.

For the reporting team, this means preserving the customer question alongside the expected rows. A future engineer should be able to challenge an obsolete definition without having to reverse-engineer why a test once expected it.

## Find time for questions with uncertain returns

The factory has work waiting today. The farm offers a possibility of improving tomorrow's work. These demands compete for the same experienced people, even if agent execution is inexpensive.

James March's [Exploration and Exploitation in Organizational Learning](https://doi.org/10.1287/orsc.2.1.71) examines this tension. His models explain how the more immediate returns from exploiting established knowledge can crowd out exploration. Applying that argument to farms and factories is our proposal; the paper does not prescribe an allocation for software teams.

A fixed percentage of engineering time would not settle the reporting team's problem. It needs to account for the scarce person who can interpret the evidence. Several parallel investigations that all require her review may delay delivery while resolving little. A single well-chosen question, with time reserved for that review, could be more useful.

Start with a bounded commitment. The team might give this investigation two working sessions with the specialist and decide what to do next once it has examined the competing explanations. That limit is a design choice for the example, not a recommended universal budget. If the investigation uncovers a consequential question it cannot answer, someone can choose to fund a further attempt.

Some capacity must remain available for questions outside the current delivery constraint. Otherwise the farm becomes a troubleshooting service for the factory's existing design. It will never investigate whether the product needs those exports at all. The team needs both a reason to improve today's work and room to question tomorrow's work.

## Follow the next capability

The reporting team now has a clearer account of several business definitions and examples another engineer can use. On the next export change, those examples may reduce repeated interpretation. That is a useful return from the original investment.

Suppose the team later considers replacing the reporting store. The old examples could help it construct a comparison between old and new implementations. This is a different capability: checking whether a replacement preserves the required behavior across relevant cases.

The earlier material provides only part of what is needed. The migration may introduce new timing behavior, historical data problems or differences under concurrent updates. The team must establish those expectations and checks separately. It should record exactly what transferred, what adapting it cost and what had to be discovered afresh.

There is a second possible connection. The farm developed a method for investigating repeated review work: recover cases, observe the hidden decisions, follow uncertain meanings to their users, and compare alternative explanations. Could that method help a different engineer investigate delays in permission changes? The subject matter and evidence would differ. If the method merely tells the new investigator to produce more documentation, it has preserved a conclusion rather than a way to investigate.

These are separate claims. The examples might help build a migration check while the investigative method proves too specific to reporting. Or the method might travel while the examples become obsolete. [Improving our ability to improve](./improving-our-ability-to-improve.md) distinguishes doing the work, improving how it is done, and improving the development of improvements. The [second-capability pilot](../research/second-capability.md) proposes a more careful comparison of that final claim.

Do not infer compounding from the fact that the second task finished sooner. It may simply have been easier. Show what the earlier investment enabled, include its maintenance and adaptation costs, and ask a colleague to try the new capability without its author's help.

## Keep the investigation open to correction

When the next export change reaches the factory, watch where the work goes. The specialist may spend less time explaining definitions while another engineer spends more time finding the right example. The new product screen may remove the report request but generate support questions. Those consequences belong to the same investigation.

The farm can then revisit its explanation with something better than a progress report. Did the decision change? Did the intended work disappear? Can the team perform the remaining work with less effort at the required standard? Is the new capability useful beyond its first demonstration?

There is no need to turn every answer into another programme. Keep the evidence beside the definitions and examples it explains. Give an unresolved question a place to resume, and remove guidance that no longer applies. The [open questions](../research/open-questions.md) suggest several investigations that could challenge the wider argument.

On the team's next customer request, someone who was not part of the investigation should be able to establish which meaning of "active" applies, find the evidence, and notice when none of the existing meanings fits. If they still need to reconstruct the whole story, that is where the farm has more work to do.
