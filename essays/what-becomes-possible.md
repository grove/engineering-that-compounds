# What becomes possible?

*Recognizing progress when the work itself changes*

Suppose a company wants to leave a billing provider. The fees are painful, but an earlier investigation found that nobody could confidently reproduce the provider's treatment of old plans, partial refunds and late adjustments. A replacement would be easy to demonstrate and hard to trust. The proposal was shelved.

Since then, the team has investigated disputed invoices, retained reviewed examples and separated several calculations from the provider's API. It has a way to replay account histories and people who can explain the disagreements. The migration may now deserve another look.

Nothing in this hypothetical story requires the team to deliver more features per week. Its progress may be that a worthwhile project has become possible within a budget and risk limit the company can accept.

## Name the boundary

A team's *capability frontier* is the boundary of what it can accomplish under stated conditions. The phrase is useful only if those conditions are clear. With this team, this budget, this time and these quality requirements, which jobs can it reasonably undertake?

There is no single scale of difficulty. A team may become better at migrating large datasets while becoming less able to diagnose unfamiliar outages. A new provider may make an integration cheaper while increasing dependence on a service the team cannot operate without. The frontier is a way to ask better questions, not a number to put on a league table.

Compare like conditions. A project becoming feasible after doubling the team is a different claim from earlier investments making it feasible with the same resources. Lowering the reliability requirement also changes the question. Both may be legitimate business choices; neither should be reported as an unexplained improvement in engineering effectiveness.

For the billing migration, recover the old decision. Which uncertainty stopped it? Was the budget credible? Did customers actually need the capabilities the replacement promised? If the original proposal was a poor idea, better tooling has not made it a good one.

## Becoming able to develop new abilities

David Teece, Gary Pisano and Amy Shuen's [Dynamic Capabilities and Strategic Management](https://doi.org/10.1002/(SICI)1097-0266(199708)18:7%3C509::AID-SMJ882%3E3.0.CO;2-Z) examines how firms build and reconfigure capabilities as conditions change. Their argument connects processes, existing assets and the paths a firm has followed. It offers a strategic context for this collection's narrower questions about engineering investment.

Being able to deploy the current service safely is valuable. Being able to work out how to verify and operate an unfamiliar service is a further ability. The latter depends on people who can investigate, evidence they can trust, experiments they can afford and decisions they have authority to make.

The distinction should affect leadership questions. Alongside asking whether AI reduced implementation effort, ask which previously impractical work the organization can now investigate responsibly. Could it replace an expensive dependency, serve a customer need that required too much manual work, or test a product idea before committing to a full launch?

These are candidate opportunities, not benefits to book in advance. The migration team has reduced some uncertainty. It still needs to investigate cutover, recovery, support costs and the behavior of historical accounts. An expanding capability should make that investigation more credible, not make its conclusion inevitable.

## Use what the organization has learned about its world

In this hypothetical migration, the cases are useful only if the team checks them against actual rules and customer situations. A collection of generated accounts could exercise more code while missing the reasons customers dispute charges. [When software forgets the world](./when-software-forgets-the-world.md) examines that gap.

Retained domain knowledge can serve several jobs. Engineering can use a disputed-credit case to verify behavior. Product and design can use the same situation to investigate whether a clearer explanation would prevent confusion. Support can identify which information is missing from the account view. Each group will need different detail, and the case must retain its source and limits as it travels.

The relationship can work in both directions. Better understanding of customer work helps the team design a more revealing experiment. Better experimental tools make another customer question affordable to investigate. That is a possible compounding mechanism worth following across real decisions. Counting scenarios or interviews would miss it.

## Stronger models are not the whole capability

An organization may perform better because it has access to a stronger AI model. That is a useful benefit, but it differs from developing its own ability to evaluate and apply models.

For the migration team, reviewed account histories and independent expectations make it possible to compare several models or tools on relevant work. Engineers who can investigate disagreements can recognize when a fluent migration plan omits a necessary step. Clear authority and reversible execution make it possible to act on a good proposal. These investments may remain useful as providers change, although they still need maintenance.

AI can help beyond implementation: finding related support cases, comparing alternative migration plans, translating a billing rule into candidate examples or preparing questions for a domain expert. The resulting evidence must still be checked. Access to the same model does not imply that two organizations have the same data, understanding, permissions or ability to use the answer.

Beware of developing all those abilities around one fragile dependency. A shared agent platform may reduce local effort while making every team's recovery depend on the same service. A safe rehearsal with the usual automation unavailable can reveal whether the organization still understands the job. Preservation belongs beside exploitation and exploration when choosing the next investment.

## Reopen one worthwhile proposal

Find a project previously rejected as too difficult, costly or uncertain. Read the old reason before suggesting new tools. Then ask what has changed, which existing capabilities bear on that reason and what evidence would justify another step. The [investment canvas](https://grove.github.io/compounding-engineering/adoption/investment-canvas.html) can hold that decision in a form the people doing the work can review.

For the billing team, the first step might be replaying one well-understood account history through a candidate replacement. Record the discrepancies and ask the people responsible for billing to resolve their meaning. A successful comparison would justify a larger investigation, not a claim that the whole portfolio can now be migrated.

Perhaps the new evidence still makes leaving the provider a bad investment. The team can stop with a better answer. Or perhaps it reveals a smaller replacement that removes the expensive dependency without recreating everything it offered. That is the kind of progress a count of completed features would fail to notice.
