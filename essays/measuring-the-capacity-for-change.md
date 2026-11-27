# Measuring the capacity for change

*Finding out whether today's work helps tomorrow's engineers*

You can measure the cost of an engineering investment down to the hour. The payoff shows up months later, inside work that has no counterfactual.

Take an illustrative case: a product team spends a month pulling authorization logic out of feature handlers and into a single policy boundary, adds tests for role combinations nobody had checked, and pins down half a dozen product rules that had lived in verbal folklore. Feature output drops to near zero for four weeks.

Three months later, the team ships project-scoped permissions in three days. Everyone involved *feels* the refactor paid for itself. Proving it is another matter. They never built project-scoped permissions on the old code. Maybe the old code wouldn't have fought back as hard as everyone remembers. Maybe the real speedup came from finally settling the disputed product rules, not the new code boundary. Maybe the month they spent delayed a launch worth ten times what they saved.

That doesn't make capability unmeasurable. It just means a tidy success story isn't evidence.

## Measure the work that follows, not the pile of artifacts

Counting artifacts is tempting because you can put it on a chart this Friday: ADRs written, test count, shared modules, workshop hours. Every one of those numbers can climb while the team gets slower. A brittle test suite turns small edits into a chore; a stale ADR locks in a dead premise.

Nicole Forsgren and colleagues made the broader case in the [SPACE framework](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/): no single activity metric captures engineering performance. Capacity for change works the same way. Shorter cycle time means little unless you read it alongside release confidence and whether someone other than the original author can safely touch the code.

Before starting an investment, skip vague goals like *"make permissions cleaner"* and write down a falsifiable claim with explicit edges: *"new role rules can be added without editing feature handlers, and an engineer who didn't build the module can verify what a role permits within an hour."* That claim deliberately says nothing about migrating legacy tenants or switching to attribute-based access control. Without stated edges, any outcome can be narrated as a win after the fact.

## Averages hide shifts in difficulty

Suppose average ticket time stays flat after the refactor. Did the month get wasted? Maybe. Or maybe the team is now taking on nastier permission work it used to dodge. The reverse happens just as easily: cycle time drops because a brutal migration wrapped up and the backlog drifted back to minor tweaks. Capability can decay while the velocity chart trends smoothly upward.

Timestamps need thin context glued to them. Not a second Jira, just six lines on sampled changes so nobody has to reconstruct what happened from memory three months later:

```text
Change: Project-scoped read-only role (#1842)
Type: New rule inside existing policy boundary
Active time / Wait time: 1.5 days active / 2 days waiting on legal wording
Who: Maintainer new to permissions module
Verification: Ran role-matrix suite + added 4 cross-project denial cases
Rework / surprises: 1 PR round (missed export endpoint bypassing policy boundary)
```

Splitting active work from waiting stops a legal bottleneck from masquerading as an architecture problem. Including review and rework stops people from halting the clock the second an agent opens a pull request, which is where a huge share of AI-assisted work actually gets spent. And when the data stays noisy, report the noise plainly instead of inventing a "complexity score" that launders guesswork into two decimal places.

## Speed without confidence is deferred pain

Two engineers ship a permission change in one afternoon. The first clicks through three roles in staging and merges. The second runs a matrix suite against independently agreed rules and catches two accidental grants. Measuring elapsed time alone hands the trophy to the engineer taking an invisible gamble.

Agree upfront on what counts as adequate verification and keep that bar visible (especially when you raise it, so tougher checks don't look like mysterious slowdowns). Remember what production *fails* to prove, too: a quiet month after launch may just mean nobody hit the rare role combination that breaks. Pair defect counts with hands-on checks: ask an unfamiliar engineer or on-call responder to explain an unexpected denial or add a small rule, and watch where they hesitate. Their sticking points tell you far more than a five-point survey.

## Put the full bill on the ledger

The permissions refactor didn't stop costing money at the end of the month. The policy engine needs upkeep. Product still has to review rule updates. Flaky matrix tests chew up attention. If only one person really understands the new module, that bus factor is a carrying cost too.

AI tools bring their own off-ledger bills: reviewing plausible-looking diffs, fixing generated fixtures that miss the point, inference spend, and deciding when to throw away an agent's branch and start fresh. [METR's randomized study of early-2025 AI tools](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) with experienced open-source developers is no permanent verdict on AI coding (models and workflows shift fast), yet it is a sharp methodological warning: seasoned engineers genuinely felt faster while objectively taking longer. Feeling productive is a terrible instrument.

Note opportunity cost too, even roughly: write down which feature slid for that month and why the trade looked sensible at the time. Sometimes an investment is worth doing before it pays back in hours, like cutting single-person dependency before a key maintainer rotates off. Just label it deliberate risk reduction instead of pretending it's a proven speed gain.

## A twelve-week field check, and how to actually test compounding

On a working team, run a grounded twelve-week check on one high-frequency class of change (don't bother on subsystems touched twice a year; you'll get no signal). Write down the investment, its upkeep cap, and the specific later work it is meant to help. Log a handful of baseline changes, awkward ones included, and record ordinary tickets as they arrive instead of cherry-picking flattering ones. At week twelve, read the individual notes before computing averages; one ugly migration usually explains more than a mean. Accept upfront that twelve weeks in production has weak causal control (people learn while the product shifts) and use it to decide whether to keep, shrink, or scrap the investment.

Testing the *compounding* claim rigorously in a research setting requires more care than a simple before-and-after benchmark. First, you need a four-group design across equivalent starting repositories, equal total engineering budgets (including setup and maintenance), and a *sequence* of withheld requirements changes:

- *Group A:* No AI assistance, no explicit capability investment
- *Group B:* AI assistance, no explicit capability investment
- *Group C:* No AI assistance, explicit capability investment
- *Group D:* AI assistance, explicit capability investment

Keep later requirements hidden while participants work on earlier rounds so nobody can study to the test, score behavior independently, and preserve failed attempts across the run.

Even that 2×2 split has a subtle trap worth spelling out. Comparing totals across the four groups separates four different questions that get blurred together:

- *Direct AI productivity* (`B` vs `A`): does AI speed up ordinary work?
- *Capability return* (`C` vs `A`): does deliberate investment pay back its own cost over a sequence of changes?
- *AI × capability interaction* (`(D - B)` vs `(C - A)`): do AI tools amplify (or get amplified by) better structure and executable checks?
- *Compounding itself:* does the *trajectory* across rounds improve, meaning earlier investments make *later investments* cheaper or raise the payoff of Round 3 and Round 4 relative to Round 1 and Round 2, rather than delivering a single one-time step change?

A positive interaction between AI and capability investment is interesting, yet by itself it does not prove compounding. Compounding lives in the slope across successive rounds. Even a clean multi-round benchmark won't capture real turnover or shifting company strategy, but it would finally test whether the claim holds up outside anecdotes.

## Make a "no" answer safe to report

Every measurement system rots the moment people need it to defend their reputation or hit a bonus target they can game by editing what gets logged.

Treat the twelve-week review as a steering call, not a report card. Maybe the permissions boundary paid off nicely for routine role tweaks and turned into drag during a tenant migration. Maybe it sped up onboarding without earning back its original month. Those are useful results, because they tell you what *not* to repeat next quarter.

If engineering capital is going to be a real practice rather than a reassuring phrase, teams have to be able to declare an investment a bust. Any scorecard that reads every outcome as progress cannot help you decide where to spend next month.
