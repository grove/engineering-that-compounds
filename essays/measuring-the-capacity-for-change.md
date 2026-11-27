# Measuring the capacity for change

*Finding out whether today's work helps tomorrow's engineers*

Suppose a team spends a month separating permissions from the rest of an application. It replaces scattered checks with a smaller interface, adds tests for combinations that previously went unexamined and writes down several rules the product team had never agreed on explicitly. Feature delivery slows during the work.

Three months later, the team introduces permissions scoped to individual projects. The change is straightforward. Was the earlier investment worthwhile?

The answer feels obvious to the engineers involved. Establishing it is harder. They never implemented the new requirement against the old design. Perhaps it would have been easier than they remember. Perhaps the new interface helped, but the main benefit came from resolving the disputed rules. Perhaps the work postponed something more valuable than the future effort it saved.

These difficulties do not make engineering investment impossible to assess. They do mean that claims about compounding capability require more than a convincing account of a successful refactor.

## The result appears in later work

We can observe how long a change took, what it cost and whether it behaved as intended. The capacity to make future changes is less directly visible. It concerns work that has not yet arrived, under conditions we cannot fully specify.

Counting assets is tempting because they are available now. We can count tests, decision records, reusable components and training sessions. But a large test suite may make changes harder. A decision record may preserve an obsolete assumption. A training session may leave no one better able to diagnose a failure.

The [SPACE framework](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/), developed by Nicole Forsgren and colleagues, argues that developer productivity cannot be represented by a single activity measure or dimension. The same caution applies to future capability. A shorter implementation time is useful evidence, but it needs to be considered alongside the quality of the result and the experience of the people producing it.

For the permissions work, I would look for a narrower claim than "the codebase is healthier." Perhaps the team expects that new permission rules can be introduced without editing unrelated features, and that a developer unfamiliar with the implementation can establish which access decisions are allowed. Both expectations can be challenged by subsequent tasks.

The claim should include its intended scope. Is the investment supposed to help ordinary rule changes, migrations of existing data, or entirely new authorization models? An interface that makes the first easier may make the third harder. Without a scope, almost any outcome can be described as success.

## Comparable does not mean identical

Suppose the team's average delivery time remains unchanged after the refactor. That might indicate no benefit. It might also mean that the team is now attempting harder changes.

The reverse is possible too. Average time may fall because a difficult migration has finished and the backlog now consists mostly of small adjustments. The capabilities of the team could have deteriorated while its delivery chart improved.

Useful comparisons therefore need descriptions of the work. For each relevant change, record what was requested, the obligations it had to preserve and the unfamiliar questions it raised. Distinguish a new rule behind an existing boundary from a change to the boundary itself. Note unusual dependencies, staffing changes and interruptions that explain a long delay.

This need not become a second ticketing system. A short note attached to selected changes may be enough. The purpose is to leave evidence with which the team can interpret a pattern, rather than inventing an explanation for the pattern months later.

For elapsed time, distinguish waiting from active work. A change blocked on a product decision presents a different investment opportunity from one that requires four days of tracing scattered checks. Include review and rework after the first implementation. Stopping the clock when an agent opens a pull request leaves much of the engineering cost outside the measurement.

Some comparisons will remain uncertain. It is better to report that uncertainty than to invent a complexity adjustment that produces a precise answer from subjective estimates.

## Confidence has a cost

Two implementations may take the same amount of time and leave the team with very different grounds for releasing them.

In the permissions example, one developer manually exercises a few roles in a browser. Another runs a test that checks every supported role against an independently agreed set of access rules, then investigates the failures. The second process may take longer while establishing considerably more about the result.

Speed alone would encourage the team to do less verification. Counting checks would create a different mistake: producing numerous checks that confirm the same assumption.

Before assessing a change, agree on what acceptable evidence would look like. Keep that standard reasonably stable across the comparison. Where the standard improves, record the improvement instead of treating the extra verification time as unexplained inefficiency.

Production outcomes also matter, but a quiet period is limited evidence. Some permission errors remain unnoticed until an unusual combination of roles appears. A useful assessment combines observed defects with targeted challenges to the guarantees the team cares about. It should preserve the distinction between detecting no failures and establishing that a particular failure has become less likely.

The people using the new arrangement can supply evidence that logs miss. Does a newcomer understand why a rule exists? Can the on-call engineer explain an unexpected denial? Ask them to perform a representative task and discuss where they got stuck. Their account complements timing data; it should not be reduced to a satisfaction score and used as a substitute for the task.

## Count what the investment consumes

The permissions refactor has costs beyond its initial month. The shared interface needs maintenance. Product experts must review changes to the rules. Tests take time to run and sometimes fail for irrelevant reasons. If only one engineer understands the new machinery, that dependence belongs in the assessment too.

AI assistance introduces further costs that can disappear from a narrow measure of implementation time: reviewing plausible suggestions, repairing generated experiments, paying for inference and deciding when to abandon an unproductive approach. Those costs should be counted alongside any savings.

There is a useful warning in [METR's study of early-2025 AI tools](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/). Experienced open-source developers believed the tools had saved them time, while the randomized experiment found longer completion times in that setting. The result concerns particular developers, tasks and tools; it is no verdict on every later use of AI. Its relevance here is methodological: a strong impression of improvement can survive contrary measurements.

Opportunity cost is harder to measure than an invoice. We cannot know exactly what would have happened if the permissions month had been spent on another feature. We can at least record which work was delayed and why the investment seemed preferable at the time. An assessment that quietly excludes that tradeoff is predisposed to approve the investment.

There may be good reasons to continue even before the costs have been recovered. Reducing dependence on one specialist can matter during a likely staff transition. But that is a specific judgment under uncertainty, not a saving already realized.

## A practical study

A team could start with one class of recurring change over twelve weeks. Permissions might be suitable if relevant requests arrive often enough. A rarely touched subsystem would require a longer period, and might be a poor candidate for a first study.

Before starting, write down the proposed investment, its budget and the later work it is expected to help. Choose a few observations: effort spent understanding the request, effort spent establishing confidence, material rework, and the ability of someone other than the original author to complete a related task. Record the existing examples available for comparison, including awkward ones.

During the period, keep the full cost of the investment visible. Sample ordinary changes rather than selecting only those that showcase the new design. At the review, examine individual cases before calculating averages. A single expensive migration or unresolved defect may explain more than the mean.

This is a local evaluation, with weak causal control. The team is learning the domain while changing the software. Requirements and staffing may move. Report those limitations and use the result to decide whether to continue, alter or stop the investment. Twelve weeks cannot establish that returns will compound for years.

A research benchmark could provide a stronger comparison. Start several groups from equivalent repositories, allocate equal total engineering budgets and expose them to successive requirements changes. Compare ordinary development, AI-assisted development and AI-assisted development with an explicit capability investment. Include preparation and maintenance within the budget. Randomize assignments where practical and repeat across projects.

Some later tasks should be withheld from participants and from the people designing the improvements. Otherwise, the benchmark rewards preparation for a known exam. Evaluate resulting behavior independently, retain failed attempts and follow costs across the whole sequence. Even then, a benchmark would test its own selection of tasks; real organizational turnover and shifting product goals would remain difficult to reproduce.

## Leave room for an unwelcome answer

Measurement becomes less useful when the people supplying the evidence must defend the investment to protect their reputation. It becomes actively misleading if individuals are rewarded for reducing a number they can influence by changing what gets recorded.

Use the findings to question a practice and choose the next investment. Let engineers describe costs that the collection process missed. Retire measures that consume more attention than their decisions justify.

The permissions work might prove worthwhile for ordinary rule changes and poor for the next architectural shift. It might need simplifying. It might have improved understanding without recovering its implementation cost. Those are useful answers because they change what the team should do next.

If engineering capability is going to become an explicit object of investment, it must also be possible to conclude that a particular investment failed. A theory that explains every outcome as progress will not help us spend the next month well.
