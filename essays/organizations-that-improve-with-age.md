# Organizations that improve with age

*How a lesson becomes useful beyond the team that learned it*

Most engineering organizations do not run short on hard-won lessons. They just pay for the same lesson three times in three different departments.

Consider a hypothetical outage on an orders service: a routine schema migration adds a column with a constraint check that takes a brief exclusive lock on a hot table. Under peak traffic, queries pile up behind the lock, worker pools saturate, and unrelated checkout endpoints stall for twelve minutes. The team rolls back, switches to a two-step expand-and-contract pattern, and writes a clear postmortem.

Six months later, the billing team runs a nearly identical migration on its ledger table and triggers the same cascading timeout. Their service uses a different framework, their postmortem folder sits in another wiki space, and nobody thought to search the orders team's incident archive.

Some repeated discovery is fine. Hunting through another department's history can cost more than solving a small bug locally. When the same class of failure keeps chewing through product after product, though, the organization is accumulating experience without turning it into shared capability.

## What actually travels across teams

The orders team's exact SQL patch is the least portable thing they produced. It reflects their table layout, their ORM and their deployment tooling. Copying it blindly into billing could easily cause a different outage.

The transferable lesson sits one layer lower: *how the database acquires and queues locks during DDL changes, and how a short blocked lock starves the connection pool behind it.*

Even that lesson has edges. A small admin table with low traffic can take a brief lock safely; a high-write table cannot. A team running a different database engine faces different lock rules altogether. What travels well is a testable question aimed at a specific audience: *"For any table handling more than N writes per second, what lock does your migration tool take, and what happens to live connections while it waits?"* That is far easier to act on than emailing every engineer in the company a four-page "lessons learned" document.

## Sending is not transferring

Google's [postmortem culture](https://sre.google/sre-book/postmortem-culture/) treats writeups as part of a social loop (reviewed, discussed and replayed in later exercises) precisely because dropping a document into a searchable wiki rarely changes anyone's behavior.

Transfer needs an explicit receiver and budgeted time to respond. Someone, whether the incident lead, a staff engineer or a rotating reliability representative, identifies the handful of teams running high-write databases and gives them a small reproduction or check to run during normal planned work.

A receiving team should have several valid outcomes: prove their migration linter already blocks that lock mode, run the check and catch a risky upcoming release, or confirm their workload doesn't hit the threshold. Every one of those answers fills in the organization's map of where the risk actually lives.

Forcing every team to adopt the orders team's exact migration script defeats the whole exercise. Compliance replaces local judgment and hides real differences until the next surprise. Coding agents can cut the legwork by scanning repositories for risky migration patterns and drafting candidate checks, as long as local engineers still verify whether a textual match represents a real risk. A lesson has traveled when another team makes a better decision, not when a hundred people click "mark as read."

## The capability trap

Even when engineers *know* how to spread lessons and prevent repeat outages, organizations routinely fail to do it.

Nelson Repenning and John Sterman's work on [capability traps](https://doi.org/10.2307/3094806) (based on field studies in manufacturing and product development rather than software teams, though the feedback loop is instantly recognizable) explains why. When performance dips or deadlines tighten, working harder on immediate output pays off *now*, whereas investing in better tooling and shared learning pays off *later* and briefly slows delivery down. Under pressure, teams borrow time from improvement to ship features. Capability erodes, which causes more incidents and slower delivery, which creates even more pressure to skip improvement.

Worse, leaders routinely misread the symptoms. Seeing missed deadlines and repeat fires, they assume people aren't trying hard enough rather than noticing that the organization starved its own ability to work well. That attribution error locks the trap shut: more urgency, less time to share lessons, steeper decline.

## Who pays, and who benefits?

Writing about organizational learning often assumes everyone's interests point the same way. They don't.

When a team codifies hard-won expertise into shared checks or internal platforms, the organization becomes less dependent on a few senior specialists. That is healthy for resilience, and it can simultaneously shrink those specialists' bargaining power. When a central platform team standardizes database migrations to improve company-wide safety, individual product teams lose flexibility and wait on another group's roadmap. And when leadership pockets the time saved by better engineering capital as headcount cuts instead of reinvesting it, engineers learn very quickly that improving shared capability just buys them a leaner, more stressed job.

Truth-telling has a price too. Amy Edmondson's [1999 study of psychological safety](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Organizational_Learning_and_Change/Edmondson_1999_Psychological_safety.pdf) showed how strongly learning depends on whether people expect candor to backfire. If pointing out that a celebrated platform migration made local debugging twice as slow earns you a reputation for being difficult, your organization's memory will rapidly fill up with polite fiction.

Honest postmortems also expose decisions made above the team: a launch date that left no room for lock testing, or split ownership where nobody owned both the schema and the connection pool. Recording only the SQL fix guarantees you keep reproducing the organizational conditions that caused the outage.

## Shared tools acquire landlords

After three teams trip over migration locks, someone naturally proposes a shared migration gatekeeper: a service that runs every DDL change against a staging clone, checks lock modes, and blocks unsafe deploys.

That can be a strong move. It is also the day you sign a new maintenance lease.

Who updates the gatekeeper when the database upgrades a major version? Who debugs a false positive blocking a critical Friday hotfix? Can a product team add a rule without queuing behind the platform team's quarterly planning? When the original author leaves, does anyone still know which lock modes the tool misses?

Moving expertise into shared infrastructure never makes upkeep vanish; it concentrates it and creates a new bottleneck. Often the lighter shared asset beats the platform: a small runnable check teams can copy, three concrete questions in the pull-request template, or a ten-minute live demo of how lock queues actually fail. Build the shared service only after seeing how three real teams differ, and only if the savings stay positive after you count support and coordination.

## Keep the dissent alive

Organizations are remarkably good at turning one sensible lesson into an overbroad commandment.

Suppose the lock incident hardens into a company policy: *no schema migrations without a two-week staged rollout.* Two years later, a team launching a brand-new internal table with zero traffic spends two weeks jumping through hoops built for a hot checkout table, or sidesteps the rule by stuffing structured data into a JSON blob so they never have to touch DDL at all.

Shared standards stay healthy when they carry their scope, their rationale and an explicit path for exceptions, plus a record of who disagreed and why. Uniformity buys coordination, but it also lets a single stale assumption hurt every team at once. As with [forgotten alternatives](./the-value-of-forgotten-alternatives.md), preserving the conditions behind a rule keeps today's guardrail from becoming tomorrow's cage.

## Testing whether the organization actually learns

Pick one recent incident whose mechanism plausibly reaches another team. Have the authors distill the smallest testable check and the exact conditions under which it matters. Give one neighboring team protected time during an ordinary sprint to evaluate it, and track both the friction of adapting it and whether it changed a real decision.

Then, a quarter later, hand the same check to someone who wasn't in either room. If they can tell whether it applies to their service and run it without pinging the original author, something real has crossed the team boundary. If it takes an hour of oral history to decipher, fix the transfer, or retire the lesson, before scaling it into a company program.

An organization that gets better with age is not one with the largest wiki or the strictest platform team. It is one where hard-won lessons travel lightly, stay open to challenge, and get retired once the world moves on.
