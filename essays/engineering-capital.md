# Engineering capital

*What the work leaves behind*

Two software projects illustrate why a useful engineering investment and a compounding effect are different claims.

SQLite's [testing architecture](https://www.sqlite.org/testing.html) includes independent harnesses, fault injection and coverage checks. Its authors describe how those tests support changes that would otherwise be too risky. That is evidence of a recurring benefit from a substantial verification investment. It does not, by itself, establish that successive verification capabilities became cheaper to develop.

FoundationDB's [testing documentation](https://apple.github.io/foundationdb/testing.html) describes a deterministic simulation integrated with its `Flow` runtime. The team can reproduce failures across a simulated cluster, and workload specifications also run in its live performance-testing environment, `Circus`. That shared infrastructure is a plausible place to investigate compounding: did it make later verification capabilities easier to develop? The documentation shows reuse and explains why the team values the simulator. It does not provide a comparative measure of that later development cost.

Most teams do not work on SQLite or FoundationDB, of course. The same fork shows up in ordinary product code every week.

Take a made-up billing bug: a service occasionally cuts an invoice that disagrees with its account ledger. An engineer traces the mismatch to a race between a late usage report and the monthly closing job, patches the race, fixes the bad invoices, and closes the ticket.

That single afternoon of debugging can leave the team in very different places. One engineer stops once the patch ships. Another keeps a small script that triggers the race on demand. A third wires the script into CI, or uses the investigation to settle a deeper argument: the invoicing code and the ledger disagree on what "closed billing period" means, and reconciling them collapses three tangled modules into one.

Every version ships the same fix. Six months later, when an awkward billing request arrives, those teams are standing on completely different ground.

I call the resources a team develops or maintains for future engineering work *engineering capital*. They include runnable tools, recorded reasoning, module boundaries and the judgment in people's heads. The phrase gives us a way to discuss investments as well as the liabilities usually described as technical debt. An investment may be useful, premature or mistaken; its value becomes clearer when later work needs it and somebody has to pay for its upkeep.

## Capital supports a capability

Capital is what the team can draw on. A capability is something it can reliably accomplish under stated conditions. The reproduction script is capital. Being able to investigate a closing-period failure without its original author is a capability.

That ability needs more than the script. Someone must understand its result, have access to the right environment and be able to resolve a disputed expectation. A team can possess all the right files and still be unable to act. Describe an investment in terms of the work it should make possible, then ask someone to try it.

Capabilities can also be inputs to later capabilities. Investigating a closing-period failure might teach the team how to build a recovery rehearsal. The [foundations](https://grove.github.io/compounding-engineering/foundations.html) put this connection at the centre of the framework: create value while developing, combining and renewing the abilities future work will need.

## Four shapes of capital, who owns them, and how they wear out

The assets behind that ability have different owners, different useful lives and different ways of breaking.

Start with *human judgment*. Peter Naur gave the classic account in [Programming as Theory Building](https://doi.org/10.1016/0165-6074(85)90032-8): building software forms a live theory in the programmers' minds, a feel for how the code maps to the world and what a proposed change will disturb. Source code never holds the whole theory, which is why rotating out maintainers after launch hollows out a system over time. Judgment is the most adaptable asset a team has, and the least owned by the company: it belongs to the engineer, walks out the door when they leave, and fades when they stop touching the system.

*Executable assets* (reproduction scripts, fault-injection harnesses, fast tests, linters) stay with the organization after their authors move on. A newcomer can run them on day one. Their failure mode is drift. Dependencies upgrade, data shapes shift, and a harness that once saved days starts burning hours just to stay green.

*Recorded rationale* (decision records, experiment notes, documented invariants) also outlives turnover and tells the next maintainer *why* the code looks strange. It breaks through staleness and misreading: the world moves on while the note stands still, or a later reader mistakes an old guess for a permanent rule.

*Structural and organizational boundaries* (clean module seams, stable contracts, clear team ownership) matter because real systems outgrow any single person's head. Nobody holds Naur's full theory for a fifty-service platform; good boundaries let you change invoice formatting without becoming an expert in ledger concurrency. Their failure mode is rigidity and cost-shifting: a seam drawn around yesterday's product split turns into ceremony once the business shifts, and a boundary that makes life easy for one group often dumps coordination work onto its neighbors.

These four shapes can also be damaged abruptly. A reorganization or platform migration may leave every repository and wiki page untouched while separating the people whose shared understanding made them usable. Treating the forms as interchangeable, as if a wiki page could replace judgment or a test suite could repair a broken team boundary, misses what got lost.

## Investments can still lose money

If "engineering capital" just meant "anything good," the term would explain nothing. Defining it strictly as work whose payoff beats its upkeep creates a different trap: you could no longer talk plainly about bad bets or tools that used to pay off and stopped.

Keep four things separate: the *asset* you build, its *expected return*, its *realized net return* once upkeep is counted, and its *depreciation*.

Back to the billing race. Out of one incident, a team might keep a reproduction script, a short note on how late usage reports arrive, a cleaner closing-period boundary, a recovery drill for half-finished runs, or a contract check shared with the payments team. Each is a wager. Some earn back their cost many times over. Others sit untouched until a framework upgrade breaks them, ending in the red. Calling a bad bet a failed capital investment, rather than pretending it never counted, keeps the books straight.

Sometimes the best investment is subtraction. Deleting a duplicate copy of account state makes every later edit safer. Ripping out a flaky fixture saves the next hire an afternoon of chasing ghosts. Leaving less machinery behind often helps future work more than anything you add.

## Accumulation, returns, and how compounding happens

A Confluence space with a thousand postmortems is accumulation. A replay harness that shaves a day off every release earns a recurring return. Neither, on its own, is compounding.

Compounding needs a link across investments: an earlier capability makes a subsequent capability cheaper or more effective to develop. Keep that distinct from *complementarity*, where having one capability increases the value of investing in another. A scenario builder may make independent invariants more useful, and vice versa. That combination could help build a recovery check, but we have to observe the later development to establish the connection. Composition can enable compounding; it does not establish it by itself.

Follow the billing example through a conversion chain. Debugging the race sharpens an engineer's judgment. Turning that judgment into a deterministic reproduction script converts private intuition into an executable asset. Because the script catches concurrency mistakes in seconds, the team can safely carve out a cleaner closing-period boundary, turning an executable asset into a structural one. That cleaner boundary makes it cheap to prototype partial refunds, which exposes a second ambiguity in the ledger model. Six months later, running a new hire through that same script converts executable capital back into human judgment.

Learning is the work behind those conversions. An agent might connect several difficult reviews, propose competing explanations and help build a check that separates them. The resulting investment still belongs to one of the forms above. [Compounding learning](./compounding-learning.md) asks whether AI can improve that investigation, and whether the method itself helps us develop a later capability. A convincing explanation is only the start of that test.

Douglas Engelbart made a related distinction in [Toward High-Performance Organizations](https://dougengelbart.org/content/view/116/), separating ordinary work from improving how work is done, and both from improving the improvement process itself. [Improving our ability to improve](./improving-our-ability-to-improve.md) follows that third kind of work. The chain can break: urgent feature work absorbs the capacity before the next investment happens; the script is too narrow for the new question; upkeep exceeds the benefit; or the business retires the subsystem. Who pays may also differ from who benefits, a tension [Organizations that improve with age](./organizations-that-improve-with-age.md) takes up directly.

An investment whose upkeep exceeds its benefit has a negative return. Negative compounding needs a reinforcing loop: skip verification to hit a deadline and the next change becomes harder to trust, which raises the pressure to skip the next check too. Ship faster while understanding drains out of the team, and incidents take longer to diagnose, eating the time you would have spent fixing the mess. On a quarterly velocity chart, a team liquidating its engineering capital can look fast right up until an unfamiliar failure lands.

## Cheap artifacts, scarce understanding, and agents as consumers

Building engineering capital used to require a lot of dull plumbing: wiring up fixtures, stubbing production dependencies, scripting replay runs, mocking throwaway designs. That grunt work is why sensible investments routinely lost to the sprint backlog.

When AI tools lower the cost of writing code and scaffolding, investigations that used to be too expensive become practical. After an incident, a team can build a clean reproducer and compare two competing fixes before committing.

The trap is harder to spot because it looks like productivity. Cheap generation makes it effortless to multiply *produced knowledge artifacts* (sprawling test suites that lock in existing bugs, polished summaries that sand off every caveat, generated benchmarks that mirror the team's blind spots) while *validated understanding* thins out. A repository can grow heavier with docs, tests, and abstractions every week while the people operating it understand less of what it does.

There is a flip side, too: coding agents are now *consumers* of engineering capital alongside humans. That changes which assets pay off. A fast deterministic test harness, a strict contract check, or a short, current list of architectural constraints amplifies every future agent run as well as every human edit. A sprawling wiki full of half-obsolete lore does the opposite. It poisons context windows and gives agents plausible reasons to make the wrong change.

Writing code by hand used to bundle learning with delivery: you figured out how billing worked because you had to change it line by line. Hand the implementation to an agent and the feature can ship without any mental model forming. The answer is not to type boilerplate by hand; it is to build understanding on purpose, for example by predicting how the closing job behaves on late usage before running an experiment to check. [How engineers become engineers](./how-engineers-become-engineers.md) looks at how to make that habit stick.

## Spending capital on purpose

Almost any pet refactoring can be sold as an investment in the future. A team gets annoyed with four reproduction scripts, invents a generic experimentation framework with its own config language, and signs up for a permanent maintenance bill to serve scripts that run four times a year. Before building a framework, watch a colleague who didn't write one of those scripts try to run it. Half the time the right investment is a lockfile and three lines in a README.

The [tenfold ambition](./what-would-ten-times-look-like.md) uses the Theory of Constraints to choose investments by what limits worthwhile outcomes. In billing, if changes wait for a shared definition of a closed period, a faster way to prepare patches may only lengthen the queue. First settle the rule and make better use of existing capacity. Invest in a retained check or boundary when it helps remove that constraint, protects a necessary guarantee or prepares for a credible future limit.

A capability may produce a real recurring return or make another capability cheaper to build without changing what the team can deliver. Those are different claims. Ask where the released capacity can actually be used, who will maintain the investment, and whether a smaller intervention elsewhere would matter more. Revisit the choice as the constraint moves.

Just as important: an engineering group exists to create value with its capital, not to hoard it.

Often the right call is to *spend* capital rather than build it: ship a rough integration to catch a real market window, leave a one-off migration script plain once its output is verified, or skip generalizing a service slated for retirement next quarter. A defensible investment names a recurring obstacle, a realistic lifetime, and a concrete reason to expect the payoff to beat the upkeep. When those aren't there, skipping the investment is good engineering.

The billing team still owes its customers accurate invoices; everything else serves that. What separates a team that gets stronger from one that just stays busy is whether it pays attention to what a finished ticket leaves behind, and whether six months later it counts the upkeep straight and scraps the bets that didn't pay.
