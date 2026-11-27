# Organizations that improve with age

*How a lesson becomes useful beyond the team that learned it*

Most engineering organizations aren't short on hard-won lessons. They just pay for the same lesson three times in three different departments.

Google's [postmortem culture](https://sre.google/sre-book/postmortem-culture/) tries to break that habit by treating incident writeups as part of a social loop (reviewed, argued over, and replayed in later exercises) because dropping a document into a wiki almost never changes what another team does next Tuesday.

Suppose an orders team runs a routine schema migration that adds a column with a check constraint, briefly grabbing an exclusive lock on a hot table. Under peak traffic, queries pile up behind the lock, worker pools saturate, and unrelated checkout endpoints stall for twelve minutes. The team rolls back, switches to expand-and-contract, and publishes a clear postmortem.

Six months later, the billing team runs nearly the same migration on its ledger table and triggers the exact same timeout cascade. Different framework, different wiki space, and nobody thought to search the orders team's incident archive.

Some rediscovery is fine; combing through another department's history often costs more than solving a small problem locally. When the same failure class burns through product after product, though, the company is piling up experience without building shared capability.

## What actually travels across teams

The orders team's exact SQL patch is the least portable thing they produced. It fits their table layout, their ORM, and their deploy pipeline. Pasting it into billing could easily cause a new outage.

The portable lesson is one layer down: *how the database acquires and queues locks during DDL changes, and how a brief blocked lock starves the connection pool behind it.*

Even that has edges. A low-traffic admin table can take a short lock without anyone noticing; a hot write table cannot. A team on a different database engine faces different lock rules altogether. What travels well is a testable question aimed at the right teams: *"On any table taking more than N writes per second, what lock does your migration tool grab, and what happens to live connections while it waits?"* That is far more actionable than emailing the entire engineering org a four-page "lessons learned" memo.

## Sending is not transferring

Transfer needs a real receiver and real time on their sprint board. Someone (the incident lead, a staff engineer, or a rotating reliability rep) finds the handful of teams running high-write databases and hands them a small check or reproduction to run during planned work.

Several outcomes count as success: confirming their migration linter already blocks that lock mode, catching a risky release before it ships, or establishing that their traffic stays well below the danger threshold. Each answer sharpens the organization's map of where the risk actually lives.

Forcing every team onto the orders team's exact migration script ruins the exercise. Compliance replaces local judgment and hides real differences until the next outage. Coding agents can handle the scanning (searching repositories for risky DDL patterns and drafting candidate checks) so long as local engineers still decide whether a match represents a real hazard in their service. A lesson has crossed team lines when another group makes a better call, not when a hundred people click "mark as read."

## Collective understanding without individual mastery

Earlier essays leaned heavily on handing a service or a check to one engineer who didn't build it. That test works at the scale of a single service. It breaks down across a fifty-service platform, because nobody, not the chief architect and not the founders, holds a live mental model of the entire estate.

Organizations cannot solve that by asking everyone to read more docs. Trustworthy collective understanding has to be distributed: bounded local ownership where a small team truly knows its own slice, executable contract checks guarding the seams between teams, and named owners for cross-cutting assumptions that code cannot test on its own. Coding agents change the mix by mapping cross-repo dependencies faster than humans ever could, yet someone still has to hold authority over each seam and answer when an assumption between two services fails.

## The capability trap

Even teams that know how to share lessons routinely fail to do it.

Nelson Repenning and John Sterman's work on [capability traps](https://doi.org/10.2307/3094806) (drawn from field studies in manufacturing and product development, though the dynamic hits software teams just as hard) explains why. When deadlines tighten, pushing harder on immediate output pays off *this week*, while fixing tooling or spreading a lesson pays off *later* and slows delivery right now. Under pressure, teams borrow from improvement to hit the release. Capability dips, fires multiply, delivery slows further, and pressure to skip improvement grows stronger.

Managers routinely misread the symptoms. Seeing missed dates and repeat outages, they assume people aren't pushing hard enough instead of noticing that the organization starved its own capacity to work cleanly. That misdiagnosis locks the trap shut: more urgency, less room to share lessons, steeper slide.

## Who pays, who benefits, and what works when management won't fix it

Writing about organizational learning often assumes everyone's interests line up. In real companies, they rarely do.

When a team turns hard-won expertise into shared checks or internal tools, the organization depends less on a few veteran specialists. That makes the company more resilient while shrinking those specialists' bargaining power. When a central platform team standardizes migrations for company-wide safety, product teams lose room to maneuver and end up queuing behind another group's roadmap. When leadership converts time saved by better engineering capital into headcount cuts rather than reinvesting part of it, engineers learn fast that improving shared capability only buys them a tighter job.

Candor carries personal risk too. Amy Edmondson's [1999 study of psychological safety](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Organizational_Learning_and_Change/Edmondson_1999_Psychological_safety.pdf) showed how tightly team learning depends on whether people expect speaking up to backfire. If pointing out that a celebrated internal platform doubled local debugging time earns you a reputation as "difficult," company memory fills up with polite fiction. Honest postmortems also point upward: a launch date that left no time for lock testing, or split ownership where nobody owned both the schema and the connection pool. Writing down only the SQL fix guarantees the same org conditions will produce the same outage again.

In an ideal company, management fixes the accounting: funding cross-team prevention out of shared reliability capacity, rewarding managers when their tools save another group an outage, and giving teams explicit authority to challenge shared standards.

What if management doesn't? In plenty of companies, quarterly targets stay rigid, directors compete for promotion, and platform teams have more political clout than their internal users. Pretending enlightened leadership is about to arrive is bad advice. When the incentives stay broken, heavy central learning programs and mandatory architecture reviews mostly rot into bureaucracy. What survives ordinary corporate politics is much smaller and more self-contained:

- *Opt-in checks that pay off locally.* A ten-line migration linter that saves the adopting team from its own next Friday-night page gets adopted without an executive mandate.
- *Default expiration dates on shared rules.* Require any cross-team guardrail to be explicitly renewed after a year, or it retires automatically. That keeps stale policies from outliving the political sponsor who created them.
- *Platform teams that eat their own migration costs.* If a central team wants twenty product teams on a new schema pipeline, making the central team absorb the rollout work (or judging it on voluntary adoption rather than compliance) exposes real friction fast.

None of that substitutes for aligned leadership, and some orgs really will stay trapped in repeat outages until the business hurts enough to change incentives. Still, small self-serving assets have a much better survival rate than grand knowledge-management initiatives.

## Shared tools acquire landlords

After three teams hit migration locks, someone inevitably proposes a central migration gatekeeper: a service that runs every DDL change against a staging clone, checks lock modes, and blocks unsafe deploys.

Sometimes that is the right call. It is also the day you sign a maintenance lease.

Twilio Segment's [account of retiring its per-destination microservices](https://www.twilio.com/en-us/blog/developers/best-practices/goodbye-microservices) shows how quickly well-meant shared architecture can invert. Early on, splitting event-forwarding destinations into separate services and repositories solved head-of-line blocking, and shared libraries made adding new destinations quick. Once the fleet grew past 140 services, updating those shared libraries meant testing and deploying dozens of repos at once. Under time pressure, engineers updated only the service in front of them. Library versions drifted apart across the fleet, operational load scaled linearly with every new destination, and three full-time engineers spent most of their time keeping services alive and answering load-spike pages. In the end, the team collapsed those 140+ services and 120 dependencies back into a single service and monorepo.

Moving expertise into shared infrastructure never makes upkeep disappear; it concentrates it and creates a coordination bottleneck. Before building a gatekeeper service, see how far a lighter asset goes: a small runnable check teams can copy, three sharp questions in a PR template, or a ten-minute live demo of how lock queues stall. Build the shared service only after watching three real teams diverge, and only if the payoff still clears the bar once support and upgrades are on the bill.

## Keep the dissent alive

Organizations are remarkably fast at turning one sensible lesson into a blanket commandment.

The lock outage turns into company policy: *no schema migrations without a two-week staged rollout.* Two years later, a team spinning up a brand-new internal table with zero traffic burns two weeks on theater built for a hot checkout table, or routes around the rule by stuffing structured data into a JSON blob so they never have to touch DDL.

Shared standards stay useful when they carry their scope, their original reason, an explicit escape hatch, and a note on who disagreed and why. Uniformity lowers coordination cost right up until one stale assumption hurts every team at once. As with [forgotten alternatives](./the-value-of-forgotten-alternatives.md), keeping the conditions attached to a rule stops today's guardrail from hardening into tomorrow's cage.

## Testing whether anything crossed the boundary

Take one recent incident whose failure mode plausibly reaches another group. Distill the smallest testable check and the exact conditions where it matters, then give one neighboring team protected time during an ordinary sprint to try it, tracking both the friction of adapting it and whether it changed a real decision.

A quarter later, hand the same check to an engineer who wasn't in either room. If they can tell whether it applies to their service and run it without messaging the original author, real capability crossed the team line. If it takes an hour of oral history to decode, either fix the check or drop it.
