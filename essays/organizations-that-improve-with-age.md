# Organizations that improve with age

*How a lesson becomes useful beyond the team that learned it*

Most engineering organizations aren't short on hard-won lessons. They just pay for the same lesson three times in three different departments.

Take a familiar composite incident: an orders team runs a routine schema migration that adds a column with a check constraint, briefly grabbing an exclusive lock on a hot table. Under peak traffic, queries stack up behind the lock, worker pools fill, and unrelated checkout endpoints stall for twelve minutes. The team rolls back, switches to expand-and-contract, and writes a clear postmortem.

Six months later, the billing team runs almost the same migration on its ledger table and triggers the exact same timeout cascade. Different framework, different wiki space, and nobody thought to search the orders team's incident archive.

Some rediscovery is fine. Hunting through another group's history often costs more than solving a small bug locally. When the same failure class keeps burning through product after product, though, the company is piling up experience without turning it into shared capability.

## What actually travels across teams

The orders team's exact SQL patch is the least portable thing they made. It fits their table layout, their ORM, and their deploy pipeline. Pasting it into billing could easily cause a brand-new outage.

The portable lesson lives one layer down: *how the database acquires and queues locks during DDL changes, and how a short blocked lock starves the connection pool behind it.*

Even that has boundaries. A quiet admin table can take a short lock without anyone noticing; a hot write table cannot. A team on a different database engine faces different lock rules altogether. What travels cleanly is a testable question aimed at the right audience: *"On any table taking more than N writes per second, what lock does your migration tool grab, and what happens to live connections while it waits?"* That is far easier to act on than emailing the entire engineering org a four-page "lessons learned" memo.

## Sending is not transferring

Google's [postmortem culture](https://sre.google/sre-book/postmortem-culture/) treats writeups as part of a social loop (reviewed, argued over, and replayed in later exercises) because dropping a document into a wiki rarely changes what anyone does next Tuesday.

Transfer needs a real receiver and real time on their sprint board. Someone (the incident lead, a staff engineer, or a rotating reliability rep) finds the handful of teams running high-write databases and hands them a small check or reproduction to run during planned work.

Several answers count as success: proving their migration linter already blocks that lock mode, catching a risky release before it ships, or confirming their workload sits well below the danger threshold. Each answer sharpens the organization's map of where the risk actually lives.

Forcing every team onto the orders team's exact migration script ruins the exercise. Compliance replaces local judgment and hides real differences until the next outage. Coding agents can cut the legwork by scanning repos for risky DDL patterns and drafting candidate checks, provided local engineers still decide whether a match represents a real hazard. A lesson has crossed team lines when another group makes a better call, not when a hundred people click "mark as read."

## The capability trap

Even teams that know how to share lessons routinely fail to do it.

Nelson Repenning and John Sterman's work on [capability traps](https://doi.org/10.2307/3094806) (built from field studies in manufacturing and product development, though the dynamic hits software teams just as hard) explains the mechanism. When deadlines tighten, pushing harder on immediate output pays off *this week*, while fixing tooling or spreading a lesson pays off *later* and slows delivery briefly right now. Under pressure, teams borrow from improvement to hit the release. Capability dips, fires multiply, delivery slows further, and pressure to skip improvement grows even stronger.

Managers routinely misread the symptoms. Seeing missed dates and repeat outages, they assume people aren't pushing hard enough rather than noticing that the org starved its own capacity to work cleanly. That misdiagnosis locks the trap shut: more urgency, less room to share lessons, steeper slide.

## Who pays, and who benefits?

Writing about organizational learning often assumes everyone's interests line up. In real companies, they rarely do.

When a team codifies hard-won expertise into shared checks or internal tools, the organization depends less on a few veteran specialists. That makes the company more resilient while shrinking those specialists' bargaining power. When a central platform team standardizes migrations for company-wide safety, product teams lose room to maneuver and end up queuing behind another group's roadmap. And when leadership pockets the time saved by better engineering capital as headcount cuts instead of reinvesting part of it, engineers figure out fast that improving shared capability only buys them a tighter, harder job.

Candor carries personal risk too. Amy Edmondson's [1999 study of psychological safety](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Organizational_Learning_and_Change/Edmondson_1999_Psychological_safety.pdf) showed how tightly team learning depends on whether people expect speaking up to backfire. If pointing out that a celebrated internal platform made local debugging twice as slow earns you a reputation as "not a team player," the company's memory quickly fills up with polite fiction.

Honest postmortems also point upward: a launch date that left no time for lock testing, or split ownership where nobody owned both the schema and the connection pool. Writing down only the SQL fix guarantees the same org conditions will reproduce the outage.

Process rituals won't fix misaligned incentives. Management has to change the accounting. If the orders team spends a week packaging a migration check that saves four other teams from outages, leadership needs to fund that work out of shared reliability capacity (or credit cross-team prevention in how managers and senior engineers are evaluated) rather than letting it look like a missed feature commitment on the orders team's roadmap. Someone also needs explicit authority to challenge a shared standard without being sidelined. Without those structural shifts, asking engineers to "share learnings" is asking them to donate their own schedule to another department's metrics.

## Shared tools acquire landlords

After three teams hit migration locks, someone inevitably pitches a central migration gatekeeper: a service that runs every DDL change against a staging clone, checks lock modes, and blocks unsafe deploys.

Sometimes that's the right call. It is also the day you sign a maintenance lease.

Twilio Segment's [account of retiring its per-destination microservices](https://www.twilio.com/en-us/blog/developers/best-practices/goodbye-microservices) shows how quickly well-meant architecture and shared tooling can invert. Early on, splitting event-forwarding destinations into separate services and repositories solved head-of-line blocking, and shared libraries made adding new destinations quick. Once the fleet grew past 140 services, updating those shared libraries meant testing and deploying dozens of repos at once. Under time pressure, engineers updated only the service in front of them. Library versions drifted apart across the fleet, operational load scaled linearly with every new destination, and three full-time engineers spent most of their time just keeping services alive and answering load-spike pages. In the end, the team collapsed those 140+ services and 120 dependencies back into a single service and monorepo.

Moving expertise into shared infrastructure never makes upkeep vanish; it concentrates it and creates a coordination bottleneck. Before building a gatekeeper service, see how far a lighter asset goes: a small runnable check teams can copy, three sharp questions in the PR template, or a ten-minute live demo of how lock queues fail. Build the shared service only after watching three real teams differ, and only if the payoff survives once support and upgrades are on the bill.

## Keep the dissent alive

Organizations are remarkably quick to harden one sensible lesson into a blanket commandment.

The lock outage turns into company policy: *no schema migrations without a two-week staged rollout.* Two years later, a team spinning up a brand-new internal table with zero traffic burns two weeks on theater built for a hot checkout table, or quietly dodges the rule by stuffing structured data into a JSON blob so they never have to touch DDL.

Shared standards stay useful when they carry their scope, their original reason, an explicit escape hatch, and a note on who disagreed and why. Uniformity lowers coordination cost, right up until one stale assumption hurts every team at once. As with [forgotten alternatives](./the-value-of-forgotten-alternatives.md), keeping the conditions attached to a rule is what stops today's guardrail from turning into tomorrow's cage.

## Testing whether anything crossed the boundary

Take one recent incident whose failure mode plausibly reaches another group. Distill the smallest testable check and the exact conditions where it matters, then give one neighboring team protected time during an ordinary sprint to try it, tracking both the friction of adapting it and whether it changed a real decision.

A quarter later, hand the same check to someone who wasn't in either room. If they can tell whether it applies to their service and run it without messaging the original author, real capability crossed the team boundary. If it takes an hour of oral history to decode, fix the transfer or drop the lesson before turning it into a company-wide mandate.
