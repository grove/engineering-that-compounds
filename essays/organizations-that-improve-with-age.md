# Organizations that improve with age

*How a lesson becomes useful beyond the team that learned it*

Most engineering organizations aren't short on hard-won lessons. They just pay for the same lesson three times in three different departments.

Google's [postmortem culture](https://sre.google/sre-book/postmortem-culture/) tries to break that habit by treating incident writeups as part of a social loop (reviewed, argued over, and replayed in later exercises) because dropping a document into a wiki almost never changes what another team does next Tuesday.

A familiar hypothetical shows how the gap opens. An orders team runs a routine schema migration that adds a column with a check constraint, briefly grabbing an exclusive lock on a hot table. Under peak traffic, queries pile up behind the lock, worker pools saturate, and unrelated checkout endpoints stall for twelve minutes. The team rolls back, switches to expand-and-contract, and publishes a clear postmortem.

Six months later, the billing team runs nearly the same migration on its ledger table and triggers the exact same timeout cascade. Different framework, different wiki space, and nobody thought to search the orders team's incident archive.

Some rediscovery is fine; combing through another department's history often costs more than solving a small problem locally. When the same failure class burns through product after product, though, the company is piling up experience without building shared capability.

## What travels across teams

The orders team's exact SQL patch is the least portable thing they produced. It fits their table layout, their ORM, and their deploy pipeline. Pasting it into billing could easily cause a new outage.

The portable lesson is one layer down: *how the database acquires and queues locks during DDL changes, and how a brief blocked lock starves the connection pool behind it.*

Even that has edges. A low-traffic admin table can take a short lock without anyone noticing; a hot write table cannot. A team on a different database engine faces different lock rules altogether. What travels well is a testable question aimed at the right teams: *"On any table taking more than N writes per second, what lock does your migration tool grab, and what happens to live connections while it waits?"* That beats emailing the entire engineering org a four-page "lessons learned" memo.

## Sending is not transferring

Transfer needs a real receiver and real time on their sprint board. Someone (the incident lead, a staff engineer, or a rotating reliability rep) finds the handful of teams running high-write databases and hands them a small check or reproduction to run during planned work.

Several outcomes count as success: confirming their migration linter already blocks that lock mode, catching a risky release before it ships, or establishing that their traffic stays well below the danger threshold. Each answer fills in the organization's map of where the risk really lives.

Forcing every team onto the orders team's exact migration script ruins the exercise. Compliance replaces local judgment and hides real differences until the next outage. Coding agents can handle the scanning (searching repositories for risky DDL patterns and drafting candidate checks) so long as local engineers still decide whether a match represents a real hazard in their service. A lesson has crossed team lines when another group makes a better call, not when a hundred people click "mark as read."

Count the effort of finding a receiving team too. Did the agent find a team that needed the lesson, or send ten irrelevant matches for someone to dismiss? Keep the rejected matches and adaptation costs visible when deciding whether to repeat the search. [Compounding learning](./compounding-learning.md) treats this way of finding and testing lessons as an investment with its own upkeep. A useful migration check does not automatically justify the machinery used to distribute it.

## Prepare the receiving team

Suppose billing can run the check but cannot explain its output. Orders sees a successful handoff; billing sees another tool that needs a specialist whenever it turns red. Give a billing engineer time to change the example, predict the lock behavior and investigate an unfamiliar result. The missing investment may be an afternoon of joint work, a smaller example or access to the right database metrics.

Cohen and Levinthal's [work on absorptive capacity](https://doi.org/10.2307/2393553) explains why prior knowledge matters when an organization encounters something new. Recognizing its value, understanding it and putting it to use are themselves capabilities. A recipient with the relevant background can learn more from the same demonstration.

Ask what the receiving team must know and be allowed to do before it can benefit. Count the time to its first independent use, including help from the originating team. Then check a later use. An easy installation followed by permanent dependence is an unfinished transfer.

## Collective understanding without individual mastery

The earlier essays test understanding on a single service: can someone who didn't write it still reason about it? That test breaks down across a fifty-service platform, because nobody (not the chief architect and not the founders) holds a live mental model of the entire estate.

Organizations cannot solve that by asking everyone to read more docs. Trustworthy collective understanding has to be distributed: bounded local ownership where a small team knows its own slice, executable contract checks guarding the seams between teams, and named owners for cross-cutting assumptions that code cannot test on its own. Coding agents can help trace dependencies across repositories. Someone still has to check the resulting map and answer when an assumption between two services fails.

This helps explain what can be lost during a reorganization. The repositories, tests and postmortems may survive while the people who knew how the services fit together are reassigned or leave. A transfer plan needs to account for those working relationships as well as ownership of the files.

## The capability trap

Even teams that know how to share lessons routinely fail to do it.

Nelson Repenning and John Sterman's work on [capability traps](https://doi.org/10.2307/3094806), drawn from manufacturing and product development, offers an explanation worth testing in software teams. When deadlines tighten, pushing harder on immediate output pays off *this week*, while fixing tooling or spreading a lesson pays off *later* and slows delivery right now. Under pressure, teams borrow from improvement to hit the release. Capability can deteriorate, leaving more rework and less time to improve.

Managers routinely misread the symptoms. Seeing missed dates and repeat outages, they assume people aren't pushing hard enough instead of noticing that the organization starved its own capacity to work cleanly. That misdiagnosis locks the trap shut: more urgency, less room to share lessons, steeper slide.

## Who pays, who benefits, and what works when management won't fix it

Writing about organizational learning often assumes everyone's interests line up. In real companies, they rarely do.

When a team turns hard-won expertise into shared checks or internal tools, the organization depends less on a few veteran specialists. That makes the company more resilient while shrinking those specialists' bargaining power. When a central platform team standardizes migrations for company-wide safety, product teams lose room to maneuver and end up queuing behind another group's roadmap. When leadership converts time saved by better engineering capital into headcount cuts rather than reinvesting part of it, engineers learn fast that improving shared capability only buys them a tighter job.

Candor carries personal risk too. Amy Edmondson's [1999 study of psychological safety](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Organizational_Learning_and_Change/Edmondson_1999_Psychological_safety.pdf) showed how tightly team learning depends on whether people expect speaking up to backfire. If pointing out that a celebrated internal platform doubled local debugging time earns you a reputation as "difficult," company memory fills up with polite fiction. Candid postmortems also point upward: a launch date that left no time for lock testing, or split ownership where nobody owned both the schema and the connection pool. Writing down only the SQL fix guarantees the same org conditions will produce the same outage again.

In an ideal company, management fixes the accounting: funding cross-team prevention out of shared reliability capacity, rewarding managers when their tools save another group an outage, and giving teams explicit authority to challenge shared standards.

What if management doesn't? In plenty of companies, quarterly targets stay rigid, directors compete for promotion, and platform teams have more political clout than their internal users. Pretending enlightened leadership is about to arrive is bad advice. When the incentives stay broken, heavy central learning programs and mandatory architecture reviews mostly turn into bureaucracy. What survives ordinary corporate politics is smaller and more self-contained:

- *Opt-in checks that pay off locally.* A ten-line migration linter that saves the adopting team from its own next Friday-night page gets adopted without an executive mandate.
- *Scheduled review or expiry on shared rules.* For internal operational guardrails (migration conventions, style rules, rollout checklists), require an explicit renewal after a year or let the rule retire so stale habits don't outlive their original sponsor. Security, safety, and regulatory controls are different: review their justification on a schedule, don't auto-remove their enforcement.
- *Platform teams that eat their own migration costs.* If a central team wants twenty product teams on a new schema pipeline, making the central team absorb the rollout work (or judging it on voluntary adoption rather than compliance) exposes real friction fast.

None of that substitutes for aligned leadership, and some orgs really will stay trapped in repeat outages until the business hurts enough to change incentives. Still, small self-serving assets have a much better survival rate than grand knowledge-management initiatives.

## Decide what the recovered capacity is for

Suppose the migration check now lets billing review an ordinary schema change without asking the orders team's specialist for help. First establish that the interruption has actually disappeared; a successful rehearsal is not a week's worth of recovered time.

Then make the next choice explicit. The team might use that capacity to ship a customer request, rehearse a difficult recovery, or help a second engineer understand the migration path. Each can be worthwhile. Reinvestment becomes a compounding hypothesis when the earlier check makes the next improvement cheaper or more effective; simply giving the team another deadline does not establish that connection.

Use the [focusing steps](./what-would-ten-times-look-like.md#follow-the-constraint-through-the-work) to revisit which condition now limits the work. If the next migration waits for a customer decision rather than a specialist, more migration tooling may be the wrong reinvestment. Make the allocation explicit: capacity might go toward the new constraint, customer outcomes or protective slack. Do not claim the same recovered hour as both a delivery gain and a reinvestment.

Use the existing planning conversation to name the next job, who owns it and who will maintain the shared check. If billing saves time while orders absorbs all the support, the funding decision belongs with someone responsible for both teams. There is no useful universal percentage to reserve: choose against the work in front of you, and revisit the choice if upkeep consumes the expected return.

## Shared tools acquire landlords

After three teams hit migration locks, someone inevitably proposes a central migration gatekeeper: a service that runs every DDL change against a staging clone, checks lock modes, and blocks unsafe deploys.

Sometimes that is the right call. It is also the day you sign a maintenance lease.

Twilio Segment's [account of retiring its per-destination microservices](https://www.twilio.com/en-us/blog/developers/best-practices/goodbye-microservices) shows how quickly well-meant shared architecture can invert. Early on, splitting event-forwarding destinations into separate services and repositories solved head-of-line blocking, and shared libraries made adding new destinations quick. Once the fleet grew past 140 services, updating those shared libraries meant testing and deploying dozens of repos at once. Under time pressure, engineers updated only the service in front of them. Library versions drifted apart across the fleet, operational load scaled linearly with every new destination, and three full-time engineers spent most of their time keeping services alive and answering load-spike pages. In the end, the team collapsed those 140+ services and 120 dependencies back into a single service and monorepo.

Moving expertise into shared infrastructure concentrates its upkeep and can create a coordination bottleneck. Before building a gatekeeper service, see how far a lighter asset goes: a small runnable check teams can copy, three direct questions in a PR template, or a ten-minute live demo of how lock queues stall. Look for recurring needs across real services before committing to a shared one, and count support and upgrades in the decision.

The distinction between enabling teams and platforms in [Team Topologies](https://teamtopologies.com/key-concepts-content/team-interaction-modeling-with-team-topologies) helps here. An enabling team works with another team to develop a missing capability; a platform provides a capability as a service. In this example, learning to reason about locks might need temporary help. Running a maintained migration environment might justify a platform. A check peculiar to one ledger can stay local.

Decide which arrangement the consumer needs. An enabling engagement should leave billing able to handle the next migration. A platform should let billing complete supported work without arranging a meeting with its maintainers. Adoption counts miss both tests. Watch the work people can finish and the help they still need.

## Keep the ability to change course

The shared migration system may eventually be excellent at a database the organization is leaving. Improving it further can then delay the more useful work: learning how to move safely to the replacement.

Teece, Pisano and Shuen's [dynamic capabilities framework](https://sms.onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291097-0266%28199708%2918%3A7%3C509%3A%3AAID-SMJ882%3E3.0.CO%3B2-Z) asks how firms develop and reconfigure capabilities as conditions change. For the migration team, the practical question is which parts of its investment travel: representative workloads, reviewed business invariants, rollback experience and people who know how to design a useful rehearsal. Database-specific checks may need replacing.

Preserve enough time and understanding to investigate that change. Try a bounded rehearsal when a key expert or usual tool is unavailable. Find out which decisions the team can still make and which require help. Spare capacity and overlapping expertise have a cost; name the unexpected work they are intended to support. [Learning from things that go right](./learning-from-things-that-go-right.md) examines how successful adaptations reveal what is worth preserving.

## Keep the dissent alive

Organizations are remarkably fast at turning one sensible lesson into a blanket commandment.

The lock outage turns into company policy: *no schema migrations without a two-week staged rollout.* Two years later, a team spinning up a brand-new internal table with zero traffic burns two weeks on theater built for a hot checkout table, or routes around the rule by stuffing structured data into a JSON blob so they never have to touch DDL.

Shared standards stay useful when they carry their scope, their original reason, an explicit escape hatch, and a note on who disagreed and why. Uniformity lowers coordination cost right up until one stale assumption hurts every team at once. As with [forgotten alternatives](./the-value-of-forgotten-alternatives.md), keeping the conditions attached to a rule stops today's guardrail from hardening into tomorrow's cage.

## Did the lesson cross the line?

Pick one recent incident whose failure mode plausibly reaches another group. Distill the smallest testable check along with the exact conditions where it applies, and give one neighboring team protected time during an ordinary sprint to run it.

Track two things: what friction they hit adapting it, and whether it changed a real shipping decision. Three months later, look at the neighboring team's next risky migration. If they catch the lock problem on their own, or consciously skip the check because their table doesn't meet the threshold, real capability moved across team lines. If it still takes an hour of oral history from the original incident lead to decode, fix the check or drop it.
