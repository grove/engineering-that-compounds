# Measuring the capacity for change

*Finding out whether today's work helps tomorrow's engineers*

You can measure the cost of an engineering investment to the hour. Its payoff arrives months later, inside work that has no counterfactual.

Say a hypothetical product team spends a month untangling permissions from the rest of an application. They replace scattered authorization checks with a single policy boundary, add tests for role combinations nobody had checked before, and pin down half a dozen rules product had never formally agreed on. Feature delivery slows to a crawl while they do it.

Three months later, the team ships project-scoped permissions in three days. Everyone involved *feels* the refactor paid for itself. Proving it is harder. They never built project-scoped permissions on the old codebase. Maybe the old code wouldn't have fought back as hard as they remember. Maybe the real speedup came from finally settling the disputed product rules, not the new code boundary. Maybe the month they spent postponed a launch worth ten times what they saved.

None of that makes engineering investment unmeasurable. It just means a tidy success story is not evidence.

## Measure the work that follows, not the pile of artifacts

Counting artifacts is seductive because you can graph them today: number of ADRs, test count, shared modules, workshop hours. Every one of those numbers can climb while the team gets slower. A bloated test suite can turn every edit into a chore; an unmaintained ADR can lock in a dead assumption.

Nicole Forsgren and colleagues made the broader point in the [SPACE framework](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/): no single activity metric captures engineering performance. Future capability is no different. Faster cycle time means little unless you read it beside the confidence behind each release and whether engineers other than the original author can work in the system.

Instead of claiming *"the permissions module is healthier,"* write down a falsifiable expectation before starting, with a scope attached. For example: *"new role rules can be added without editing feature handlers, and an engineer who didn't build the module can verify which actions a role permits within an hour."* Notice what that scope leaves out: it makes no promise about migrating legacy tenants or switching to attribute-based access control. Without a stated scope, almost any outcome can be spun as a win.

## Averages hide the shift in difficulty

If average delivery time stays flat after the refactor, did it fail? Maybe. Or maybe the team is now taking on knottier permission changes they used to dodge. The mirror image happens too: cycle time drops simply because a gnarly migration finished and the backlog drifted back to minor tweaks. Capability can erode while the velocity chart looks better every sprint.

Raw timestamps need thin context attached to them. Not a second Jira, just a six-line note on sampled changes so nobody has to reconstruct history from memory three months later:

```text
Change: Project-scoped read-only role (#1842)
Type: New rule inside existing policy boundary
Active time / Wait time: 1.5 days active / 2 days waiting on legal wording
Who: Maintainer new to permissions module
Verification: Ran role-matrix suite + added 4 cross-project denial cases
Rework / surprises: 1 PR round (missed export endpoint bypassing policy boundary)
```

Separating active work from waiting keeps a product bottleneck from looking like an architecture failure. Counting review and rework prevents stopping the clock the second an agent opens a pull request, which is where half the real cost of AI-assisted work sits. And where comparisons stay noisy, report the uncertainty plainly instead of inventing a "complexity score" that launders guesswork into two decimal places.

## Speed without confidence is just deferred pain

Two developers ship a permission change in the same afternoon. One clicks through three roles in staging and merges. The other runs a matrix check against independently agreed access rules and chases down two unexpected grants. Measuring elapsed time alone rewards the first developer for taking an invisible gamble.

Before evaluating an investment, agree on what counts as sufficient verification and hold that bar steady (or note explicitly when you raise it, so stronger checks don't show up as unexplained slowdown). Watch what production *doesn't* prove, too: a quiet month after launch may just mean nobody triggered the rare role combination that breaks. Pair defect counts with hands-on checks: ask an unfamiliar engineer or on-call responder to explain an unexpected denial or add a small rule, and watch where they hesitate. Their sticking points tell you far more than a five-point satisfaction survey.

## Put the full cost on the ledger

The permissions refactor didn't stop costing money when the month ended. The policy boundary needs upkeep. Product still has to review rule updates. Flaky matrix tests burn attention. If only one person really grasps the new engine, that bus factor is a carrying cost too.

AI tools add their own off-ledger expenses: reviewing plausible-looking patches, fixing generated fixtures that miss the point, inference bills, and figuring out when to scrap an agent's approach and start over. [METR's randomized study of early-2025 AI tools](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) with experienced open-source developers offers a sobering methodological warning. It is no blanket verdict on AI tools in every era, since models and workflows move quickly, yet it shows that experienced engineers can genuinely feel faster while objectively taking longer. Subjective confidence is a lousy yardstick.

Record opportunity cost too, even imperfectly: write down what feature got pushed back for that month and why the trade looked right at the time. Sometimes an investment is still worth making before it breaks even, such as cutting single-person dependency before a key maintainer rotates off. Just call it a deliberate risk reduction rather than a proven productivity gain.

## A twelve-week field check, and a better benchmark

Locally, a team can run a grounded twelve-week trial on one high-frequency class of change (skip subsystems you touch twice a year; you won't get enough data). Write down the investment, its maintenance cap, and the specific later work it should help. Collect a handful of baseline changes, including awkward ones, and log ordinary changes as they arrive rather than cherry-picking flattering examples. At week twelve, read individual change notes before computing averages; one painful migration usually explains more than a mean. Accept up front that twelve weeks of local observation has weak causal control (people are learning while the product shifts) and use it to decide whether to continue, shrink, or scrap the investment.

To test the compounding claim more rigorously in a research setting, a three-way split is not enough. Comparing ordinary work, AI-assisted work, and AI-assisted work with capability investment leaves you unable to tell whether the gain came from the capability investment itself or from its interaction with AI. You want a four-group design across equivalent starting repositories, equal total engineering budgets (including setup and upkeep), and a sequence of requirements changes:

- *Group A:* No AI assistance, no explicit capability investment
- *Group B:* AI assistance, no explicit capability investment
- *Group C:* No AI assistance, explicit capability investment
- *Group D:* AI assistance, explicit capability investment

Keep later requirements withheld from everyone designing the earlier improvements so participants cannot study to the test, score resulting behavior independently, and preserve failed attempts across the whole sequence. Even a clean 2×2 benchmark won't capture real staff turnover or shifting business strategy, but it would finally separate AI speed from deliberate capability building and show whether the two actually amplify each other.

## Make a "no" answer safe to report

Every measurement scheme rots the moment people need it to defend their reputation, or get bonused on a metric they can game by changing what gets logged.

Treat the twelve-week review as a steering decision, not a performance verdict. Maybe the permissions boundary paid off handsomely for ordinary role tweaks and turned into friction during a tenant migration. Maybe it improved onboarding clarity without paying back its initial month. Those are genuinely valuable findings because they tell you what *not* to repeat next quarter.

If engineering capital is going to be a real discipline instead of a comforting metaphor, it has to be able to declare an investment a bust. Any framework that interprets every outcome as progress cannot help you decide how to spend next month.
