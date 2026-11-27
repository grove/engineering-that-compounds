# Engineering capital

*What the work leaves behind*

Two famous software projects illustrate why "good engineering investment" and "compounding" are not the same thing.

SQLite's [testing architecture](https://www.sqlite.org/testing.html) pairs roughly 156 thousand lines of core C with hundreds of times as much test code, four independent harnesses, fault injection for out-of-memory and I/O errors, assembly-level mutation checks, and 100% MC/DC branch coverage in TH3. The SQLite authors are candid about what that bought them: a wave of features and speedups over recent years would have been too risky without that safety net. They are just as candid that 100% MC/DC is laborious and probably uneconomical for an ordinary application. Mostly, SQLite shows an extraordinary *recurring return*, a standing defense that pays off on every release of a library meant to live for decades.

FoundationDB's [deterministic simulation](https://apple.github.io/foundationdb/testing.html) gets closer to genuine *compounding*. By building deterministic simulation straight into their C++ coroutine runtime (`Flow`), the team could run an entire multi-node cluster (disk stalls, full drives, dropped packets, rebooting machines, adversarial network delays) inside one process, faster than real time and reproducible from a single seed. That bet did more than catch version-1 bugs. It lowered the cost of building *later* verification machinery: the same workload definitions carried directly into their live-cluster performance suite (`Circus`), and deterministic seeds made harder fault-injection and recovery tools feasible in the first place. As the team put it, they likely could not have built FoundationDB without it.

Most teams do not work on SQLite or FoundationDB, of course. The same fork shows up in ordinary product code every week.

Take a made-up billing bug: a service occasionally cuts an invoice that disagrees with its account ledger. An engineer traces the mismatch to a race between a late usage report and the monthly closing job, patches the race, fixes the bad invoices, and closes the ticket.

That single afternoon of debugging can leave the team in very different places. One engineer stops once the patch ships. Another keeps a small script that triggers the race on demand. A third wires the script into CI, or uses the investigation to settle a deeper argument: the invoicing code and the ledger disagree on what "closed billing period" means, and reconciling them collapses three tangled modules into one.

Every version ships the same fix. Six months later, when an awkward billing request arrives, those teams are standing on completely different ground.

I call whatever leaves a team on firmer ground for future work *engineering capital*. The phrase is deliberately broader than *technical debt*. Technical debt looks backward at the drag and liabilities you owe past shortcuts. Engineering capital also looks forward at the capabilities and options today's work creates, whether they live in runnable tools, written rationale, module seams, or the judgment in people's heads. You rarely notice it on the day you build it. You notice it half a year later, when a scary change takes an afternoon instead of derailing a sprint.

## Four shapes of capital, who owns them, and how they wear out

Most engineers can tell within an hour whether a codebase lets you move with confidence or feels like defusing a bomb. What gets muddied is that the assets behind that confidence have different owners, different shelf lives, and different ways of breaking.

Start with *human judgment*. Peter Naur gave the classic account in [Programming as Theory Building](https://doi.org/10.1016/0165-6074(85)90032-8): building software forms a live theory in the programmers' minds, a feel for how the code maps to the world and what a proposed change will disturb. Source code never holds the whole theory, which is why rotating out maintainers after launch hollows out a system over time. Judgment is the most adaptable asset a team has, and the least owned by the company: it belongs to the engineer, walks out the door when they leave, and fades when they stop touching the system.

*Executable assets* (reproduction scripts, fault-injection harnesses, fast tests, linters) stay with the organization after their authors move on. A newcomer can run them on day one. Their failure mode is drift. Dependencies upgrade, data shapes shift, and a harness that once saved days starts burning hours just to stay green.

*Recorded rationale* (decision records, experiment notes, documented invariants) also outlives turnover and tells the next maintainer *why* the code looks strange. It breaks through staleness and misreading: the world moves on while the note stands still, or a later reader mistakes an old guess for a permanent rule.

*Structural and organizational boundaries* (clean module seams, stable contracts, clear team ownership) matter because real systems outgrow any single person's head. Nobody holds Naur's full theory for a fifty-service platform; good boundaries let you change invoice formatting without becoming an expert in ledger concurrency. Their failure mode is rigidity and cost-shifting: a seam drawn around yesterday's product split turns into ceremony once the business shifts, and a boundary that makes life easy for one group often dumps coordination work onto its neighbors.

These four shapes do not just fail through slow neglect. They can also be destroyed overnight. A reorganization, a round of layoffs, or an abrupt platform migration often leaves every repository and wiki page untouched while wiping out the tacit understanding and team seams that made them usable. Treating all four as interchangeable, as if a wiki page could replace judgment or a test suite could repair a broken team boundary, misses what got lost.

## Investments can still lose money

If "engineering capital" just meant "anything good," the term would explain nothing. Defining it strictly as work whose payoff beats its upkeep creates a different trap: you could no longer talk plainly about bad bets or tools that used to pay off and stopped.

Keep four things separate: the *asset* you build, its *expected return*, its *realized net return* once upkeep is counted, and its *depreciation*.

Back to the billing race. Out of one incident, a team might keep a reproduction script, a short note on how late usage reports arrive, a cleaner closing-period boundary, a recovery drill for half-finished runs, or a contract check shared with the payments team. Each is a wager. Some earn back their cost many times over. Others sit untouched until a framework upgrade breaks them, ending in the red. Calling a bad bet a failed capital investment, rather than pretending it never counted, keeps the books straight.

Sometimes the best investment is subtraction. Deleting a duplicate copy of account state makes every later edit safer. Ripping out a flaky fixture saves the next hire an afternoon of chasing ghosts. Leaving less machinery behind often helps future work more than anything you add.

## Accumulation, returns, and how compounding happens

A Confluence space with a thousand postmortems is accumulation. A replay harness that shaves a day off every release earns a recurring return. Neither, on its own, is compounding.

Compounding needs a second-order link: an earlier investment has to make the *next* investment cheaper or more effective, or two assets have to pay off more together than either could alone. Often that happens when one shape of capital converts into another.

Follow the billing example through a conversion chain. Debugging the race sharpens an engineer's judgment. Turning that judgment into a deterministic reproduction script converts private intuition into an executable asset. Because the script catches concurrency mistakes in seconds, the team can safely carve out a cleaner closing-period boundary, turning an executable asset into a structural one. That cleaner boundary makes it cheap to prototype partial refunds, which exposes a second ambiguity in the ledger model. Six months later, running a new hire through that same script converts executable capital back into human judgment.

Douglas Engelbart made a related cut in [Toward High-Performance Organizations](https://dougengelbart.org/content/view/116/), separating ordinary work from improving how work is done, and both from improving the improvement process itself. That tells you what to look for, not that the loop runs by itself. In practice, the chain snaps easily. Time saved on the first harness gets eaten by urgent feature work before the second step ever happens. The script turns out to be too narrow for the next question. Upkeep grows faster than reuse, or the business retires the subsystem before the return arrives. And who pays for an investment is rarely who collects the payoff, a tension [Organizations that improve with age](./organizations-that-improve-with-age.md) takes up directly.

An investment whose upkeep exceeds its benefit has a negative return. Negative compounding needs a reinforcing loop: skip verification to hit a deadline and the next change becomes harder to trust, which raises the pressure to skip the next check too. Ship faster while understanding drains out of the team, and incidents take longer to diagnose, eating the time you would have spent fixing the mess. On a quarterly velocity chart, a team liquidating its engineering capital can look fast right up until an unfamiliar failure lands.

## Cheap artifacts, scarce understanding, and agents as consumers

Building engineering capital used to require a lot of dull plumbing: wiring up fixtures, stubbing production dependencies, scripting replay runs, mocking throwaway designs. That grunt work is why sensible investments routinely lost to the sprint backlog.

When AI tools lower the cost of writing code and scaffolding, investigations that used to be too expensive become practical. After an incident, a team can build a clean reproducer and compare two competing fixes before committing.

The trap is harder to spot because it looks like productivity. Cheap generation makes it effortless to multiply *produced knowledge artifacts* (sprawling test suites that lock in existing bugs, polished summaries that sand off every caveat, generated benchmarks that mirror the team's blind spots) while *validated understanding* thins out. A repository can grow heavier with docs, tests, and abstractions every week while the people operating it understand less of what it does.

There is a flip side, too: coding agents are now *consumers* of engineering capital alongside humans. That changes which assets pay off. A fast deterministic test harness, a strict contract check, or a short, current list of architectural constraints amplifies every future agent run as well as every human edit. A sprawling wiki full of half-obsolete lore does the opposite. It poisons context windows and gives agents plausible reasons to make the wrong change.

Writing code by hand used to bundle learning with delivery: you figured out how billing worked because you had to change it line by line. Hand the implementation to an agent and the feature can ship without any mental model forming. The answer is not to type boilerplate by hand; it is to build understanding on purpose, for example by predicting how the closing job behaves on late usage before running an experiment to check. [How engineers become engineers](./how-engineers-become-engineers.md) looks at how to make that habit stick.

## Spending capital on purpose

Almost any pet refactoring can be sold as an investment in the future. A team gets annoyed with four reproduction scripts, invents a generic experimentation framework with its own config language, and signs up for a permanent maintenance bill to serve scripts that run four times a year. Before building a framework, watch a colleague who didn't write one of those scripts try to run it. Half the time the right investment is a lockfile and three lines in a README.

The [tenfold ambition](./what-would-ten-times-look-like.md) asks us to choose investments by what holds the team back. In billing, a shared definition of a closed period may remove more repeated investigation than a faster way to prepare patches. Recent changes should tell us where to look.

Just as important: an engineering group exists to create value with its capital, not to hoard it.

Often the right call is to *spend* capital rather than build it: ship a rough integration to catch a real market window, leave a one-off migration script plain once its output is verified, or skip generalizing a service slated for retirement next quarter. A defensible investment names a recurring obstacle, a realistic lifetime, and a concrete reason to expect the payoff to beat the upkeep. When those aren't there, skipping the investment is good engineering.

The billing team still owes its customers accurate invoices; everything else serves that. What separates a team that gets stronger from one that just stays busy is whether it pays attention to what a finished ticket leaves behind, and whether six months later it counts the upkeep straight and scraps the bets that didn't pay.
