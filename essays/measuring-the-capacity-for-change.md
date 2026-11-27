# Measuring the capacity for change

*Finding out whether today's work helps tomorrow's engineers*

In [METR's randomized study of early-2025 AI coding tools](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), experienced open-source developers felt substantially faster while objectively taking longer. That study is no permanent verdict on AI tools (models and workflows move fast), but it lands a blunt methodological point: feeling faster is a terrible measuring instrument.

The same problem haunts every engineering investment. You can measure the cost down to the hour; the payoff shows up months later inside work that has no counterfactual.

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

Splitting active work from waiting stops a legal bottleneck from masquerading as an architecture problem. Including review and rework stops people from halting the clock the second an agent opens a pull request, which is where a large share of AI-assisted time goes. And when the data stays noisy, report the noise plainly instead of inventing a "complexity score" that launders guesswork into two decimal places.

## Speed without confidence is deferred pain

Two engineers ship a permission change in one afternoon. The first clicks through three roles in staging and merges. The second runs a matrix suite against independently agreed rules and catches two accidental grants. Measuring elapsed time alone hands the trophy to the engineer taking an invisible gamble.

Agree upfront on what counts as adequate verification and keep that bar visible, especially when you raise it, so tougher checks don't look like mysterious slowdowns. Remember what production *fails* to prove, too: a calm month after launch may just mean nobody hit the rare role combination that breaks. Pair defect counts with hands-on checks: ask an unfamiliar engineer or on-call responder to explain an unexpected denial or add a small rule, and watch where they hesitate. Where they get stuck tells you far more than a five-point survey.

## Count the full bill

The permissions refactor didn't stop costing money at the end of the month. The policy engine needs upkeep. Product still has to review rule updates. Flaky matrix tests burn attention. If only one person really understands the new module, that bus factor is a carrying cost too.

AI tools bring their own off-ledger bills: reviewing plausible-looking diffs, fixing generated fixtures that miss the point, inference spend, and deciding when to throw away an agent's branch and start over.

Note opportunity cost too, even roughly: write down which feature slid for that month and why the trade looked sensible at the time. Sometimes an investment is worth doing before it pays back in hours, such as cutting single-person dependency before a key maintainer rotates off. Label it deliberate risk reduction instead of pretending it's a proven speed gain.

## A twelve-week field check, and how to test compounding

On a working team, run a grounded twelve-week check on one high-frequency class of change (skip subsystems touched twice a year; you won't get a signal). Write down the investment, its upkeep cap, and the specific later work it is meant to help. Log a handful of baseline changes, awkward ones included, and record ordinary tickets as they arrive instead of cherry-picking flattering ones. At week twelve, read the individual notes before computing averages; one painful migration usually explains more than a mean. Accept upfront that twelve weeks in production has weak causal control (people learn while the product shifts) and use it to decide whether to keep, shrink, or scrap the investment.

Testing the *compounding* claim rigorously in a research setting takes more than a before-and-after benchmark. Start with a four-group design across equivalent starting repositories, equal total engineering budgets (setup and maintenance included), and a *sequence* of withheld requirements changes:

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

Testing second-order compounding directly needs a second experiment aimed at the economics of *subsequent investments*. Give equivalent teams the same starting system. One group builds a reusable reproduction harness; the other spends the same budget on other work. Later, introduce an unforeseen requirement for a *new* verification capability (for example, a fault-injection check or a contract test for a new integration). Measure the cost and quality of building that second capability, including upkeep and reuse, and watch whether it lowers the cost of a third. That tests the compounding claim directly, rather than inferring it from feature velocity.

## What would prove this framework wrong?

A philosophy that argues for falsifiable claims owes the reader its own failure conditions. It also helps to separate what a negative result would refute: one specific practice, the AI-specific thesis, or the broader idea of compounding engineering capital.

- *Falsifying a specific practice:* Maintaining recorded rationale or abandoned-experiment notes consistently consumes more engineering hours in a given domain than re-deriving answers from code and logs on demand. That refutes the practice in that domain, not the whole framework.
- *Falsifying the AI-specific claims:* Juniors trained primarily with AI assistance and no unassisted coding floor diagnose novel production failures just as reliably as engineers trained through structured apprenticeship, or coding agents get no measurable lift from cleaner boundaries and executable checks compared to raw source code.
- *Falsifying the general thesis:* Teams that skip deliberate capability investment and rely on fast rewrites consistently match or beat investing teams across four or more unpredictable requirement rounds, even after counting production defects, onboarding time, and the cost of adding later verification tools.

If those outcomes hold in your domain, don't defend "engineering capital" out of loyalty to the phrase. Stop paying for investments that aren't clearing their cost.

## Make a "no" answer safe to report

Every measurement system breaks down the moment people need it to defend their reputation or hit a bonus target they can game by editing what gets logged.

Treat the twelve-week review as a steering call, not a report card. Maybe the permissions boundary paid off for routine role tweaks and turned into drag during a tenant migration. Maybe it sped up onboarding without earning back its original month. Those are useful findings, because they tell you what *not* to repeat next quarter. If a team can't safely declare an investment a bust, the numbers stop being useful for deciding what to do next.
