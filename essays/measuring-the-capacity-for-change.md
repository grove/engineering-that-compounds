# Measuring the capacity for change

*Finding out whether today's work helps tomorrow's engineers*

In [METR's randomized study of early-2025 AI coding tools](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), experienced open-source developers felt substantially faster while objectively taking longer. That study is no permanent verdict on AI tools (models and workflows move fast), but it lands a blunt methodological point: feeling faster is a terrible measuring instrument.

The same problem haunts every engineering investment. You can measure the cost down to the hour; the payoff shows up months later inside work that has no counterfactual.

Suppose a product team spends a month pulling authorization logic out of feature handlers into a single policy boundary, adds tests for role combinations nobody had checked, and pins down half a dozen product rules that had lived in verbal folklore. Feature output drops to near zero for four weeks.

Three months later, the team ships project-scoped permissions in three days. Everyone involved *feels* the refactor paid for itself. Proving it is harder. They never built project-scoped permissions on the old code. Maybe the old code wouldn't have fought back as hard as everyone remembers. Maybe the real speedup came from finally settling the disputed product rules, not the new code boundary. Maybe the month they spent delayed a launch worth ten times what they saved.

None of that makes capability unmeasurable. It just means a flattering story after the fact is not evidence.

## Measure the work that follows, not the pile of artifacts

Counting artifacts is tempting because you can put it on a chart this Friday: ADRs written, test count, shared modules, workshop hours. Every one of those numbers can climb while the team gets slower. A brittle test suite turns small edits into a chore; a stale ADR locks in a dead premise.

Nicole Forsgren and colleagues made the broader case in the [SPACE framework](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/): no single activity metric captures engineering performance. Capacity for change works the same way. Shorter cycle time means little unless you read it alongside release confidence and whether someone other than the original author can safely touch the code.

Before starting an investment, skip vague goals like *"make permissions cleaner"* and write down a falsifiable claim with clear edges: *"new role rules can be added without editing feature handlers, and an engineer who didn't build the module can verify what a role permits within an hour."* That claim deliberately says nothing about migrating legacy tenants or switching to attribute-based access control. Without stated edges, any outcome can be narrated as a win after the fact.

## Averages hide shifts in difficulty

Suppose average ticket time stays flat after the refactor. Did the month get wasted? Maybe. Or maybe the team is now taking on nastier permission work it used to dodge. The reverse happens just as easily: cycle time drops because a brutal migration wrapped up and the backlog drifted back to minor tweaks. Capability can decay while the velocity chart trends smoothly upward.

Timestamps need thin context attached to them. Not a second Jira, just six lines on sampled changes so nobody has to reconstruct what happened from memory three months later:

```text
Change: Project-scoped read-only role (#1842)
Type: New rule inside existing policy boundary
Active time / Wait time: 1.5 days active / 2 days waiting on legal wording
Who: Maintainer new to permissions module
Verification: Ran role-matrix suite + added 4 cross-project denial cases
Rework / surprises: 1 PR round (missed export endpoint bypassing policy boundary)
```

Splitting active work from waiting stops a legal bottleneck from masquerading as an architecture problem. Including review and rework stops people from halting the clock the second an agent opens a pull request, which is where a large share of AI-assisted time actually goes. And when the data stays noisy, report the noise plainly instead of inventing a "complexity score" that launders guesswork into two decimal places.

## Speed without confidence is deferred pain

Two engineers ship a permission change in one afternoon. The first clicks through three roles in staging and merges. The second runs a matrix suite against independently agreed rules and catches two accidental grants. Measuring elapsed time alone hands the trophy to the engineer taking an invisible gamble.

Agree upfront on what counts as adequate verification and keep that bar visible, especially when you raise it, so tougher checks don't look like mysterious slowdowns. Remember what production *fails* to prove, too: a calm month after launch may just mean nobody hit the rare role combination that breaks. Pair defect counts with hands-on checks: ask an unfamiliar engineer or on-call responder to explain an unexpected denial or add a small rule, and watch where they hesitate. Where they get stuck tells you far more than a five-point survey.

## Put the full bill on the ledger

The permissions refactor didn't stop costing money at the end of the month. The policy engine needs upkeep. Product still has to review rule updates. Flaky matrix tests burn attention. If only one person really understands the new module, that bus factor is a carrying cost too.

AI tools bring their own off-ledger bills: reviewing plausible-looking diffs, fixing generated fixtures that miss the point, inference spend, and deciding when to throw away an agent's branch and start over.

Note opportunity cost too, even roughly: write down which feature slid for that month and why the trade looked sensible at the time. Sometimes an investment is worth doing before it pays back in hours, such as cutting single-person dependency before a key maintainer rotates off. Label it deliberate risk reduction instead of pretending it's a proven speed gain.

## A twelve-week field check, and how to actually test compounding

On a working team, run a grounded twelve-week check on one high-frequency class of change (skip subsystems touched twice a year; you won't get a signal). Write down the investment, its upkeep cap, and the specific later work it is meant to help. Log a handful of baseline changes, awkward ones included, and record ordinary tickets as they arrive instead of cherry-picking flattering ones. At week twelve, read the individual notes before computing averages; one ugly migration usually explains more than a mean. Accept upfront that twelve weeks in production has weak causal control (people learn while the product shifts) and use it to decide whether to keep, shrink, or scrap the investment.

Testing the *compounding* claim rigorously in a research setting takes more than a before-and-after benchmark. You need a four-group design across equivalent starting repositories, equal total engineering budgets (setup and maintenance included), and a *sequence* of withheld requirements changes:

- *Group A:* No AI assistance, no explicit capability investment
- *Group B:* AI assistance, no explicit capability investment
- *Group C:* No AI assistance, explicit capability investment
- *Group D:* AI assistance, explicit capability investment

Keep later requirements hidden while participants work on earlier rounds so nobody can study to the test, score behavior independently, and preserve failed attempts across the run.

Comparing outcomes across the four groups separates four distinct questions that usually get tangled together:

- *Direct AI productivity* (`B` vs `A`): does AI speed up ordinary work?
- *Capability return* (`C` vs `A`): does deliberate investment pay back its own cost over a sequence of changes?
- *AI × capability interaction* (`(D - B)` vs `(C - A)`): do AI tools amplify (or get amplified by) better structure and executable checks?
- *Compounding itself:* does an earlier investment improve the economics of *subsequent investments*, not merely subsequent feature delivery?

That fourth distinction is easy to blur. Because all four groups work through the same sequence of rounds, comparing `C` against `A` already controls for ordinary codebase familiarity. Even so, a widening gap in Round 3 or Round 4 still does not prove compounding by itself: a single early module boundary might just happen to yield a larger recurring return on later requirements. To isolate true second-order compounding, you have to observe whether Investment 1 makes *building and validating Investment 2* cheaper or more effective, or makes two assets reinforce each other beyond the sum of their separate returns.

## What would prove this framework wrong?

A philosophy that argues for falsifiable claims owes the reader its own failure conditions. The thesis behind this collection would be seriously weakened, or outright falsified in a given domain, if controlled runs or honest field logs kept turning up results like these:

- Teams that skip deliberate capital investment and rely on cheap AI-assisted rewrites consistently match or beat investing teams across four or more unpredictable requirement rounds, even after counting production defects and onboarding time.
- Maintaining recorded rationale and abandoned-experiment notes reliably consumes more engineering hours than re-deriving answers from code and logs on demand.
- Juniors trained primarily with AI assistance and no unassisted coding floor diagnose novel production failures just as reliably as engineers trained through structured apprenticeship.

If those outcomes hold in your domain, the right response is not to defend "engineering capital" out of loyalty to the phrase. Stop paying for investments that aren't clearing their cost.

## Make a "no" answer safe to report

Every measurement system rots the moment people need it to defend their reputation or hit a bonus target they can game by editing what gets logged.

Treat the twelve-week review as a steering call, not a report card. Maybe the permissions boundary paid off for routine role tweaks and turned into drag during a tenant migration. Maybe it sped up onboarding without earning back its original month. Those are useful findings, because they tell you what *not* to repeat next quarter. If a team can't safely declare an investment a bust, the numbers stop being useful for deciding what to do next.
