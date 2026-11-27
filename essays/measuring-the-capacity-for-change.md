# Measuring the capacity for change

*Finding out whether today's work helps tomorrow's engineers*

In [METR's randomized study of early-2025 AI coding tools](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), experienced open-source developers felt substantially faster while objectively taking longer. That study is no permanent verdict on AI tools (models and workflows move fast), but it lands a blunt methodological point: feeling faster is a terrible measuring instrument.

The same problem haunts every engineering investment. You can measure the cost down to the hour; the payoff shows up months later inside work for which you rarely have a credible comparison.

Take a common hypothetical: a product team spends a month pulling authorization logic out of feature handlers into a single policy boundary, adds tests for role combinations nobody had checked, and settles half a dozen product rules that had lived in verbal folklore. Feature output drops to near zero for four weeks.

Three months later, the team ships project-scoped permissions in three days. Everyone involved *feels* the refactor paid for itself. Proving it is harder. They never built project-scoped permissions on the old code. Maybe the old code wouldn't have fought back as hard as everyone remembers. Maybe the real speedup came from settling the disputed product rules, not the new code boundary. Maybe the month they spent delayed a launch worth ten times what they saved.

None of that makes capability unmeasurable. It just means a flattering story after the fact is not evidence.

## Measure the work that follows, not the pile of artifacts

Counting artifacts is tempting because you can put it on a chart this Friday: ADRs written, test count, shared modules, workshop hours. Every one of those numbers can climb while the team gets slower. A brittle test suite turns small edits into a chore; a stale ADR locks in a dead premise.

Nicole Forsgren and colleagues made the broader case in the [SPACE framework](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/): no single activity metric captures engineering performance. Capacity for change works the same way. Shorter cycle time means little unless you read it alongside release confidence and whether someone other than the original author can safely touch the code.

Before starting an investment, skip vague goals like *"make permissions cleaner"* and write down a falsifiable claim with clear edges: *"new role rules can be added without editing feature handlers, and an engineer who didn't build the module can verify what a role permits within an hour."* That claim deliberately says nothing about migrating legacy tenants or switching to attribute-based access control. Without stated edges, any outcome can be narrated as a win after the fact.

## Averages hide shifts in difficulty

What if average ticket time stays flat after the refactor? Did the month get wasted? Maybe. Or maybe the team is now taking on nastier permission work it used to dodge. The reverse happens easily too: cycle time drops because a brutal migration wrapped up and the backlog drifted back to minor tweaks. Capability can decay while the velocity chart trends smoothly upward.

Timestamps need thin context attached to them. Not a second Jira, just six lines on sampled changes so nobody has to reconstruct what happened from memory three months later:

```text
Change: Project-scoped read-only role (#1842)
Type: New rule inside existing policy boundary
Active time / Wait time: 1.5 days active / 2 days waiting on legal wording
Who: Maintainer new to permissions module
Verification: Ran role-matrix suite + added 4 cross-project denial cases
Rework / surprises: 1 PR round (missed export endpoint bypassing policy boundary)
```

Splitting active work from waiting stops a legal bottleneck from masquerading as an architecture problem. Including review and rework stops people from halting the clock the second an agent opens a pull request. And when the data stays noisy, report the noise plainly instead of inventing a "complexity score" that launders guesswork into two decimal places.

## Speed without confidence is deferred pain

Two engineers ship a permission change in one afternoon. The first clicks through three roles in staging and merges. The second runs a matrix suite against independently agreed rules and catches two accidental grants. Measuring elapsed time alone hands the trophy to the engineer taking an invisible gamble.

Agree upfront on what counts as adequate verification and keep that bar visible, especially when you raise it, so tougher checks don't look like mysterious slowdowns. Remember what production *fails* to prove, too: a calm month after launch may just mean nobody hit the rare role combination that breaks. Pair defect counts with hands-on checks: ask an unfamiliar engineer or on-call responder to explain an unexpected denial or add a small rule, and watch where they hesitate. Where they get stuck tells you far more than a five-point survey.

## Count the full bill

The permissions refactor didn't stop costing money at the end of the month. The policy engine needs upkeep. Product still has to review rule updates. Flaky matrix tests burn attention. If only one person really understands the new module, that bus factor is a carrying cost too.

AI tools bring their own off-ledger bills: reviewing plausible-looking diffs, fixing generated fixtures that miss the point, inference spend, and deciding when to throw away an agent's branch and start over.

Note opportunity cost too, even roughly: write down which feature slid for that month and why the trade looked sensible at the time. Sometimes an investment is worth doing before it pays back in hours, such as cutting single-person dependency before a key maintainer rotates off. Label it deliberate risk reduction instead of pretending it's a proven speed gain.

## When the work runs without you

An automated procedure changes what needs sampling. Use all eligible events as the denominator, not just the ones for which the job reports success. Keep counts of unattended completions, escalations, failed or missed attempts and changes later found to be wrong. Inspect a sample of the unattended outcomes against the original acceptance criteria. A quiet job might be excellent, or it might have stopped looking for work.

For a defined class of comparable outcomes, record total human time from discovery to acceptance and follow-up, including setup, exception handling, oversight, recovery and the allocated cost of building and maintaining the machinery. Record elapsed time and non-human costs separately; a thousand expensive retries may save attention without making the arrangement worthwhile. Compare against the same scope and quality bar before automation. Report the share of the team's original work the class accounted for before extrapolating from it.

If an existing automation supplies the fixtures, environment or verification for a second workflow, record what was reused and what had to be adapted. A reduction in supervision is valuable; evidence that the second capability costs less to build is a different claim. See [Automating the work of engineering](./automating-the-work-of-engineering.md) for the distinction in a dependency-maintenance example.

## A twelve-week field check

On a working team, run a grounded twelve-week check on one high-frequency class of change (skip subsystems touched twice a year; you won't get a signal). Write down the investment, its upkeep cap, and the specific later work it is meant to help. Log a handful of baseline changes, awkward ones included, and record ordinary tickets as they arrive instead of cherry-picking flattering ones. At week twelve, read the individual notes before computing averages; one painful migration usually explains more than a mean. Accept upfront that twelve weeks in production has weak causal control (people learn while the product shifts) and use it to decide whether to keep, shrink, or scrap the investment.

Record a second connection if it occurs: which earlier capability helped build a later one, what was reused, and what adaptation cost. A replay that catches another bug has earned a return. A replay that reduces the work of building a recovery drill is a candidate for compounding. Reuse alone does not establish the saving; distinguish what you observed from what you estimate would have happened without it.

## Three questions for a comparative study

The field check helps a team decide what to keep. A comparison can investigate why an improvement helped. Keep three claims separate:

- **Return:** does an investment improve later engineering outcomes enough to justify its full cost?
- **Compounding:** does an earlier capability make a subsequent capability cheaper to build or more effective?
- **AI interaction:** does using AI change the benefit of those investments?

A tool can earn recurring returns without helping build another tool. AI can improve ordinary delivery without amplifying either effect. Report those outcomes separately.

To investigate returns and AI interaction together, use a four-group design across equivalent starting repositories, equal total engineering budgets (setup and maintenance included), and a *sequence* of withheld requirements changes:

- *Group A:* No AI assistance, no explicit capability investment
- *Group B:* AI assistance, no explicit capability investment
- *Group C:* No AI assistance, explicit capability investment
- *Group D:* AI assistance, explicit capability investment

Keep later requirements hidden while participants work on earlier rounds so nobody can study to the test, score behavior independently, and preserve failed attempts across the run. Even with that control, one subtle confound remains: good engineers naturally leave behind small helpers and cleaner code while shipping features. Forbidding that creates an artificial baseline; permitting it blurs the line between treatment and control. Any serious study has to record what the control groups built incidentally rather than pretending they built nothing.

Comparing outcomes across the four groups separates three questions that usually get tangled together:

- *Direct AI productivity* (`B` vs `A`): does AI speed up ordinary work?
- *Capability return* (`C` vs `A`): does deliberate investment pay back its own cost over a sequence of changes?
- *AI × capability interaction* (`(D - B)` vs `(C - A)`): do AI tools amplify (or get amplified by) better structure and executable checks?

Even a widening gap in Round 3 or Round 4 still does not prove *compounding* by itself: an early module boundary might simply pay a larger recurring return on later requirements, and deliberate investment changes what engineers learn along the way.

To investigate compounding itself, focus on the economics of *subsequent investments*. Give comparable participants the same starting system and initial task. One group deliberately retains a reusable reproduction capability; the other uses its ordinary development practice under the same budget. Later, introduce a new verification problem and measure the effort and quality of building the capability that answers it. Count the original investment and its upkeep too: a cheaper second step need not repay an expensive first one.

The [second-capability pilot](../research/second-capability.md) turns this into a proposed protocol with independent acceptance checks, repeated assignments and a maintenance round. It has not been run. It is a smaller starting point than the four-group study, and does not test the AI interaction claim. The [evolving billing lab](https://grove.github.io/patterns-of-compounding-engineering/examples/evolving-billing/) illustrates the mechanism; its published rounds cannot also serve as unseen research tasks.

## What would make us change our minds?

A philosophy that asks for evidence needs outcomes that would change its recommendations. State them for the investment, task family and period under study:

- *Against a specific practice:* Maintaining recorded rationale consistently costs more than recovering the relevant answers from code and logs, with no compensating improvement in correctness or handoff. Stop recommending that practice for this work.
- *Against the proposed compounding mechanism:* The retained harness repeatedly adds adaptation work without improving the quality or cost of building the next verification capability. It may still catch regressions, but that is a different benefit.
- *Against the AI interaction claim:* With adequate precision to rule out the improvement being claimed, capability investments provide the same or smaller benefit with AI as without it. A small, noisy study with no detectable difference leaves this question open.
- *Against the investment strategy:* Ordinary development consistently matches or beats deliberate investment across the chosen sequence after counting quality, onboarding and upkeep. Reconsider which investments to make in that setting.

These findings can reject a strategy in a particular setting. They cannot establish that engineering capabilities never reinforce one another. Equally, one successful harness cannot establish that they usually do. Publish the conditions and the exceptions so another team can judge whether your result applies to its work.

## Make a "no" answer safe to report

Every measurement system breaks down the moment people need it to defend their reputation or hit a bonus target they can game by editing what gets logged.

Treat the twelve-week review as a steering call, not a report card. Maybe the permissions boundary paid off for routine role tweaks and turned into drag during a tenant migration. Maybe it sped up onboarding without earning back its original month. Those are useful findings, because they tell you what *not* to repeat next quarter. If a team can't safely declare an investment a bust, the numbers stop being useful for deciding what to do next.
