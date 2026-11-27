# Engineering capital

*What the work leaves behind*

Suppose a billing service occasionally produces an invoice that disagrees with its account ledger. The team finds a race between a late usage report and the monthly closing job. It fixes the race, repairs the affected invoices and moves on.

There are several ways the same investigation could end. The engineer might keep a script that reproduces the race. Someone might turn it into a check that runs whenever the closing procedure changes. The team might discover that the invoice and the ledger disagree about what it means for a billing period to be closed. Resolving that disagreement could simplify several parts of the service at once.

All these outcomes include a corrected invoice. They leave the team in different positions when the next billing change arrives.

I want to call the resources that improve that position *engineering capital*: the understanding, instruments and arrangements that make subsequent engineering more effective. Some of it lives in software. Some lives in people, or in the ways they work together. Its value becomes visible when somebody needs to use it.

This collection asks how deliberately we can build that capital, how easily we can lose it, and when its returns might compound.

## More than the delivered change

The distinction is familiar in practice. An experienced maintainer can make a safe change in an afternoon that would occupy a newcomer for a week. A good reproduction turns a vague report into a problem that several people can investigate. A well-chosen boundary lets a team replace an implementation without renegotiating the rest of the system.

These advantages have different lifetimes and owners. Expertise leaves with an engineer unless others have acquired it. A reproduction can outlive its author, although its dependencies may stop working. A boundary survives personnel changes, but becomes a hindrance if it preserves a distinction the business no longer makes.

Peter Naur's [Programming as Theory Building](https://doi.org/10.1016/0165-6074(85)90032-8) gives an important part of this idea a foundation. He argued that programmers develop an understanding which allows them to explain the program, connect it to the world and reason about modifications. The program text cannot carry the whole of that understanding. Treating people as interchangeable once the code has been delivered overlooks something essential to future work.

Engineering capital is a broader working vocabulary, rather than a claim that this observation is new. It includes the conditions under which people can acquire and exercise that understanding. A service with a clear execution trace and a small, reproducible workload gives an unfamiliar engineer a way in. A service with neither asks the engineer to reconstruct its behavior from scattered clues.

It also includes resources that let us avoid needing detailed knowledge in the first place. We should be able to change how an invoice is rendered without becoming experts in ledger concurrency. A dependable interface makes that possible. The organization benefits from knowing some things deeply and from arranging its software so that it need not know everything equally well.

## What counts as capital

The term becomes useless if it means everything we approve of. A document, test or abstraction qualifies only to the extent that it helps some future work, after allowing for the effort required to keep it useful.

In the billing example, several kinds of resource are involved:

- The revised closing procedure isolates a difficult rule. That is a structural advantage.
- The reproduction gives future maintainers evidence they can rerun and challenge.
- The explanation of late usage reports preserves knowledge of the business process.
- An engineer who has investigated the race is better equipped to recognize a related problem.
- A recovery exercise makes the team more capable of repairing an interrupted closing run.
- A shared review with the payments team may reveal where the same assumption appears elsewhere.

These categories overlap. The reproduction helps teach the rule; the better understanding suggests a simpler implementation; the simpler implementation makes the reproduction easier to maintain. They are useful distinctions when asking what an investigation left behind. They would make a poor accounting system if we pretended to assign each item a precise monetary value.

Nor is capital necessarily additional material. Removing a second representation of account state can make future changes easier. Deleting an obsolete test fixture can spare every newcomer a misleading explanation. Sometimes the valuable residue of work is a smaller set of things to understand.

There is also a difference between an asset belonging to an individual and a capability available to a team. A brilliant debugging technique that only one person can apply helps the organization while that person is available. Teaching a colleague to use it takes time, and the colleague's questions may expose assumptions the original author had stopped noticing. The cost of making an asset useful to somebody else belongs in our assessment of it.

## Accumulation is easier than compounding

A directory containing a thousand incident reports has accumulated information. A test harness that has saved a day of work on each of ten changes has earned a useful return. Neither observation, on its own, establishes compounding.

Compounding requires a further relationship: a return from earlier work must improve our ability to make the next investment. Consider a possible sequence in the billing service. A reliable reproduction makes it affordable to simplify the closing procedure. The simplification makes it easier to construct experiments involving partial refunds. Those experiments expose a second ambiguity in the ledger model, which the team can now resolve with less risk. Each step improves the conditions for a later step.

The sequence can stop at any point. The saved effort might go entirely into unrelated feature work. The harness might turn out to be too narrow to support the next investigation. A new external requirement might overwhelm the benefit of the simplification. Calling the process compounding is a hypothesis about these relationships, not a promise of exponential productivity.

There is a precedent for taking the relationships seriously. In [Toward High-Performance Organizations](https://dougengelbart.org/content/view/116/), Douglas Engelbart distinguished ordinary work, work that improves how it is done, and work that improves the improvement process itself. His argument directs attention to the means by which an organization gets better, including the tools and practices it uses to learn. It does not establish that any particular engineering investment will pay off. It gives us somewhere useful to look.

For a software team, evidence would look fairly ordinary. An investigation that used to require the service's author becomes accessible to another maintainer. A failure experiment supports a simplification that makes later experiments cheaper. A lesson from one subsystem helps a team find a related defect in another. These are claims we can examine in the history of actual changes.

## What cheaper implementation changes

Many investments in engineering capital contain a substantial amount of mechanical work. Building a representative workload requires scripts, fixtures and adapters. Investigating a design alternative may require an implementation that will never ship. Making an old failure reproducible can mean replacing production dependencies with controllable substitutes.

Where AI reduces the cost of that work, investigations that previously lost out to immediate delivery may become practical. It might become reasonable to preserve three useful experiments from an incident instead of the one somebody could find time to clean up.

The saving is conditional. A generated workload that nobody checks may reproduce the team's assumptions rather than the customer's problem. A large explanation can take longer to verify than a small experiment takes to perform. The relevant cost includes deciding what to investigate, establishing that the result means what we think it means, and maintaining whatever we keep.

There is a second change. Historically, implementation often paid for learning without a separate decision. An engineer became familiar with billing because the organization needed a billing feature. If an agent supplies the implementation, that learning may no longer happen to the people responsible for the service. A team can save effort on a feature while reducing its ability to handle an unfamiliar failure later.

That is a reason to make the learning deliberate. It is not a reason to preserve every laborious step. Asking an engineer to predict how the closing job behaves when usage arrives late, then testing the prediction, may teach more than asking them to write another routine endpoint. The essay [How engineers become engineers](./how-engineers-become-engineers.md) examines this problem in more detail.

## Investments that should be refused

It is easy to make almost any technical preference sound like an investment in the future. A team builds a general experiment framework because it dislikes its collection of scripts. The framework acquires a configuration language. Supporting it becomes somebody's job. The original scripts ran a few times a year.

The fact that something might be reusable is a weak justification for building it. There should be a plausible future task, a current obstacle and some reason to believe the proposed work will remove enough of that obstacle to justify its continuing cost.

Sometimes the honest answer is that we do not know. A small experiment can help. Before building a framework, give an existing reproduction to an engineer who did not write it. See what prevents them from using it. The useful investment may be a dependency lockfile and three sentences of explanation.

The expected lifetime matters too. A service scheduled for retirement in two months offers fewer opportunities to recover a major refactoring cost. A library used by several teams over many years may justify considerable care. Neither conclusion follows simply from whether the existing code is elegant.

Capital also depreciates. A once-representative workload becomes misleading as customers change. A trusted runbook stops matching the deployment process. An expert's intuition remains calibrated to a workload the system no longer serves. Keeping these resources useful requires contact with current evidence, and occasionally the willingness to retire them.

## A modest place to begin

For the next substantial investigation, keep track of what somebody else could use afterwards. Choose one result worth preserving. It might be a reproduction, a clearer boundary, or an explanation of a business constraint that is otherwise easy to miss.

Name the next kind of work it should help with. Later, when that work happens, ask whether it did. Include the time spent repairing the instrument, finding the explanation and teaching someone to use it. If the benefit disappears under those costs, make the resource smaller or stop maintaining it.

This leaves plenty of room for judgment. We will sometimes keep knowledge whose eventual use we cannot predict, just as we will sometimes discard a seemingly useful experiment. The point is to make our reasoning open to correction.

The billing team still owes its customers correct invoices. Meeting that obligation comes first. But when the incident is over, there is a further question: does the next engineer inherit only a patch, or a better chance of understanding and changing the service? The answer determines much of what a year of engineering is worth.
