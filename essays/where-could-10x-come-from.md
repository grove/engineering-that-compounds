# Where could 10× come from?

*Six ways to change the economics of engineering with AI*

Imagine a team responsible for software that schedules field service visits. A customer wants appointments to respect a technician's qualifications, travel time and the opening hours of a particular site. Another needs different rules for urgent repairs. A third asks for a small change to the way visits are confirmed.

Today, each request starts an engineering project. Somebody investigates the need, explains it to a developer, arranges a test account, checks the result with the customer and organizes the release. Some requests are valuable but too small to justify that work. They remain unanswered.

Suppose we could produce the implementation for each request almost instantly. We would still have to understand the need, decide what to promise, establish correctness and deliver the result. Perhaps we would now have enough cheap implementations to overwhelm the people doing those other jobs.

Our ambition is to become ten times as effective at delivering valuable software outcomes with AI. Where could a gain of that order come from?

There is no established answer. The field service team is hypothetical, and the possibilities that follow are designs to investigate, not predictions. But the question is worth asking at a different level from the usual discussion about coding productivity. What if we changed the kind of work the organization has to do?

## Elimination: work that no longer needs doing

Start with the request for different opening hours. The customer has to contact support because opening hours are embedded in an engineering-maintained configuration. Support creates a ticket. An engineer changes the configuration, another approves it, and the customer waits.

An agent could make the change faster. A self-service interface with appropriate validation and authority could remove the engineering request altogether. The customer still needs to express the hours; that effort and the cost of maintaining the interface belong in the comparison. The important difference is that the outcome need no longer travel through an engineering queue.

Other requests may disappear for a different reason. Perhaps a customer asks for a special report because the existing screen cannot answer a question. Making the answer directly available could remove a recurring reporting procedure. Improving how agents prepare reports would leave the reason for requesting them untouched.

A useful investigation starts with the people who need the outcome. Which engineering activities exist because of a missing product capability, an obsolete assumption or an avoidable dependency? What would someone have to do if we removed them? Preserve the purpose of necessary controls; a review required to establish safe access does not become unnecessary because it takes time.

Elimination changes the demand for engineering work. It deserves consideration before deciding how to perform that work. [Getting better at the wrong thing](./getting-better-at-the-wrong-thing.md) examines why successful automation can make an obsolete procedure harder to question.

## Autonomy: work that no longer needs our presence

Not every customer need can become self-service. A new scheduling rule may involve behavior the product has never supported.

Suppose the team has agreed on the rule, knows what evidence is needed to establish it and has a safe way to try a candidate implementation. How much of the path from that intent to a delivered change still needs somebody to be present?

There is a difference between an engineer using an agent at each step and a workflow that can proceed within its authority while the engineer works on something else. The latter needs more than a capable model. It needs a way to obtain the relevant context, run isolated experiments, verify the exact candidate, recognize exceptions and stop when the evidence is insufficient. Some of the most important machinery may be ordinary deterministic programs.

A software factory organizes that path for suitable classes of work. It might prepare several alternatives, apply reviewed expectations, integrate the chosen change and arrange its release under an explicit policy. Initially, the team can observe the whole path. With evidence and appropriate authorization, it can delegate more of the routine decisions. Changes to the policy and high-consequence exceptions remain with the appropriate people.

The engineering work has not vanished. Human attention has moved from initiating and coordinating each instance to designing the workflow, judging uncertain results and improving its capabilities. A factory that produces a queue of changes requiring lengthy review may have changed little. A factory that reliably completes eligible outcomes with occasional, informative exceptions has changed something important.

To explore this possibility, observe where someone has to intervene in several similar tasks. Ask which interruptions reflect necessary judgment and which compensate for missing knowledge or machinery. [The ability to delegate](./the-ability-to-delegate.md) and [Automating the work of engineering](./automating-the-work-of-engineering.md) develop that approach.

## Parallelism: work that no longer has to wait for other work

Consider the more difficult scheduling rule about technician qualifications. Before changing it, the team needs to understand the customer's actual practice, examine the existing constraints and investigate several possible designs.

Those questions do not all have to wait for one another. An agent could trace how qualifications are represented; another could construct cases that distinguish possible interpretations; a colleague could talk with dispatchers while a separate experiment examines the effect on travel time. The result may be a better question for the customer rather than a change to the software.

Parallelism can also change delivery itself. If independently verifiable contracts separate eligibility, route selection and appointment confirmation, suitable changes can proceed without repeatedly coordinating their internal details. Separate working copies and test environments help, but independence of meaning and authority matters as much as isolation of files.

The gain here is partly elapsed time and partly the ability to explore alternatives we would previously have discarded without investigating. It comes at a cost: comparing results, resolving disagreements and integrating changes. More concurrent work can make delivery slower if it all waits for the same person or changes the same underlying assumption.

Look at several changes that waited for one another. Which dependencies were inherent in the problem? Which were introduced by the architecture, environment, division of responsibility or a shared decision? Try making one consequential dependency unnecessary rather than increasing the number of concurrent agents. [Architecture for parallel work](./architecture-for-parallel-work.md) explores how to distinguish independent work from work that merely appears independent.

## Simplification: a system that needs less engineering

Over time, the field service product may have acquired a collection of customer-specific scheduling branches. Each new rule interacts with several existing ones. The team needs considerable knowledge to change any of them safely.

Perhaps qualification, availability and travel constraints could be expressed in a simpler model with an explicit account of conflicts and priorities. A new customer requirement might then become a change to a rule rather than another conditional path through the program. Independent expectations for that model could serve a range of later changes.

Simplification is related to elimination, but the question is different. Elimination removes an activity that need no longer happen. Simplification changes the underlying structure so necessary activities require less understanding, coordination or repair. A smaller number of interacting concepts can change what both engineers and agents are able to do.

There is an interesting counterpossibility. If AI makes small, well-understood pieces of software economical to create and maintain, some teams may no longer need a large shared framework to avoid writing code more than once. A narrow independent solution might be simpler than adding another abstraction to a generalized platform. On the other hand, generating a separate implementation for every customer could reproduce defects and create an unmanageable maintenance burden.

Compare both designs over their useful lives. How much knowledge must someone acquire to change them? Which behavior can be verified independently? What happens when a shared rule changes or a model is replaced? Count migration, operation and recovery, not only the initial implementation. The purpose of simplification is a more comprehensible and adaptable system, not merely fewer lines of code.

## Learning: cheaper access to understanding and better judgment

What if the scheduling team could investigate the actual dispatching practices of several customers, compare them with its current model and discover which apparently different requirements express the same underlying need?

Today that might compete with a quarter's delivery commitments. AI could make parts of the investigation cheaper: finding relevant support cases, tracing behavior, proposing competing explanations, preparing experiments and helping engineers explore an unfamiliar domain. Actual customers and operational evidence would still have to resolve what the software should do.

A software farm organizes continuing investigation rather than waiting for every question to become a ticket. Its questions may concern the software, customer needs, architectural possibilities or the way the factory itself operates. A useful result could be an explanation, a counterexample or evidence that a proposed improvement is unnecessary. The farm need not produce a patch.

There is also a human opportunity. Instead of spending most of an investigation assembling context or producing an implementation, an engineer may spend more of it comparing explanations, predicting outcomes and understanding why an experiment succeeds or fails. A colleague who was not present can try a related case and challenge the team's account. That is a way to test whether understanding has travelled.

None of this follows from generating more documentation. An agent can give a fluent explanation of a system without establishing that it is true; a person can accept the explanation without learning to reason about the system. The question is whether people become able to make better decisions, investigate harder problems and recognize the limits of delegation.

A farm that creates more findings than the organization can evaluate merely moves the constraint. Give it consequential questions, a budget for investigation and review, and standards for evidence. Ask what decision a finding could change. See [Continuous cultivation of software](https://grove.github.io/software-that-improves-with-age/essays/continuous-cultivation-of-software.html) and [Compounding learning](./compounding-learning.md).

## Compounding: making the next transformation easier

Imagine the team has investigated the qualification rules and retained well-understood examples that distinguish necessary constraints from historical practices. Those examples help it simplify the scheduling model. The simpler model and the independent checks may make it feasible to delegate a class of changes.

Later, the team investigates a new opportunity: assigning jobs to combinations of technicians rather than individuals. It can use the domain understanding, environments and verification machinery developed for the earlier work to investigate that question. Some will transfer; some will need to change.

The interesting possibility is that the first transformation has made a second capability easier to develop. That is a stronger claim than saying the earlier checks run repeatedly or the earlier factory continues to save effort.

Learning can support simplification. Simplification can support autonomy and parallelism. A factory can make it cheaper to implement the improvements a farm discovers; a farm can investigate why the factory still needs intervention. A better product boundary can eliminate work and release attention for learning about a previously impractical opportunity.

The connections can also work against us. A factory may embed an obsolete rule and make it harder to change. Greater parallelism may increase coordination costs. A broadly shared tool can become a constraint on every team that uses it. We should look for the connections that actually help rather than assume that successful investments always reinforce one another.

[Improving our ability to improve](./improving-our-ability-to-improve.md) distinguishes complementary capabilities from compounding across successive investments. The latter is something to investigate: what did the earlier work contribute, what did adapting it cost, and what could the organization now do that it could not do before?

## Put the ambition to work as a design constraint

Suppose a typical customer-specific change in our hypothetical scheduling product takes sixty hours of human attention, including discovery, implementation, verification, coordination and follow-up. Twenty of those hours are implementation. Even if AI removes all twenty, forty hours remain. We have improved the human effort per comparable outcome by a factor of one and a half, not ten.

Now imagine a different arrangement for a defined class of customer needs. Some requests become self-service; others can proceed through a factory. A farm investigates the exceptions and opportunities to simplify the underlying model. Independent environments and clear decisions allow suitable work to happen concurrently.

What would have to be true for an eligible change to require six hours of human attention, including its share of the investment? One possible target budget is two hours for clarifying intent and decisions, one for preparing the work, one for examining evidence, and two for exceptions, support, maintenance and amortized development of the machinery. These are design budgets, not observations. They may prove unrealistic.

The arithmetic forces a useful conversation. If every candidate needs four hours of specialist review, the proposed budget will not hold. If the design depends on people at the customer doing more work, count their effort and experience too. Include compute and tool costs, assess required quality and account for the demand that is not served.

Coverage matters just as much. If the six-hour path serves eighty percent of equally demanding changes while the remaining twenty percent still consume sixty hours each, the average is 16.8 hours. That is less than a fourfold improvement in human effort per comparable change, even before considering other costs. The tenfold target for one path is not tenfold effectiveness for the portfolio.

That does not make the experiment a failure. A new route might become viable for a large, consequential class of work, and the capabilities it develops might open other routes. Alternatively, those capabilities may prove too expensive to extend. This is why we need to follow the work beyond the first successful demonstration.

Do not use the same unit of output when the outcome itself has changed. If a self-service capability removes most custom changes, counting those changes as lost productivity would be absurd. Assess the useful customer outcomes, including needs previously left unserved. [What becomes possible?](./what-becomes-possible.md) examines how to recognize an expansion of what an organization can accomplish.

## Imagine a different engineering organization

In one possible future, a team's work is organized around the outcomes it is responsible for rather than the tickets its engineers can individually complete.

The people understand the business and the software, set priorities and decide what is worth exploring. A farm continuously investigates selected questions about existing behavior, emerging needs, recurring exceptions and the engineering system itself. A factory delivers the work whose intent, evidence requirements and boundaries are sufficiently clear. Neither needs to be a separate department or a particular agent platform.

The team spends attention on consequential decisions, novel problems and on changing the machinery that handles familiar ones. When a workflow repeatedly requires intervention, that becomes a question about its design. When a proposed solution creates more work than it removes, the team can abandon it. Learning from delivery and operation changes both the team's understanding and the way it works.

This is one possible arrangement, not a prescription. In some settings, a person must remain closely involved in much of the work; in others, the most valuable transformation may be a product that no longer needs to be customized. The important thing is that the operating model is open to design. We do not have to preserve the organization of work that made sense when implementation was expensive.

There may be other mechanisms beyond these six, and they will matter differently in different organizations. Stronger models, better interfaces, new product possibilities and changes in the surrounding business can invalidate a route we thought promising. A team needs the ability to change direction as well as the ability to execute it.

## Find your first route

Choose a useful outcome you cannot currently deliver at the scale you would like. Follow a few actual examples to understand where the work and waiting occur. Then sketch two substantially different ways to organize it if human attention were the scarce resource and machine execution were cheaper.

For each design, name what could disappear, what could run within delegated authority, what could happen independently and what would need to become simpler. Ask which uncertainty the team most needs to resolve, and which existing understanding or capability could help. Check whether the proposed change relieves the actual constraint on delivering value.

Choose one experiment that could change your mind. It might be a conversation with a customer, a comparison of independent designs, a trial of an isolated delivery workflow or a way of observing whether an apparently necessary handoff is doing useful work. The [transformation experiments guide](https://grove.github.io/compounding-engineering/adoption/experiments.html) offers ways to frame the investment and follow its consequences.

When it finishes, ask two questions. Did it improve the outcome at a worthwhile total cost? And has it changed what we can profitably investigate or attempt next? Give those questions separate answers, including failures and uncertainty.

We may discover that tenfold effectiveness is not achievable in a particular setting, or that the useful transformation has little to do with the work we first intended to automate. That would be worth learning. We do not need to know the entire route today, but we do need to make choices that help us discover it.
