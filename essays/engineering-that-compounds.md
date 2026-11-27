# Engineering that compounds

*What we choose to carry into the next piece of work*

The best evidence that engineering capability can compound comes from systems whose builders paid a steep upfront tax, then lived off the returns for years.

Look at two well-documented cases.

When the team behind FoundationDB built a distributed transactional database, they invested early in [deterministic simulation](https://apple.github.io/foundationdb/testing.html) wired straight into their C++ coroutine runtime (`Flow`). An entire multi-node cluster (disk latency, full drives, dropped packets, rebooting machines, and adversarial patterns like "swizzle-clogging") runs deterministically inside a single process, roughly ten times faster than wall clock and reproducible from a single seed. That bet didn't just catch bugs on version 1. It lowered the cost of building and proving every major feature that came afterward, and the exact same workload definitions carry straight into their live cluster performance suite (`Circus`). As the team puts it, they likely could not have built FoundationDB without it.

SQLite's [testing architecture](https://www.sqlite.org/testing.html) shows the same long arc from a different angle: roughly 156 thousand lines of core C backed by hundreds of times as much test code, four independent harnesses, fault injection for out-of-memory and I/O errors, assembly-level mutation checks, and 100% MC/DC branch coverage in TH3. The SQLite authors are explicit about what that bought them over time: the wave of features and speedups added in recent years would not have been possible without full coverage protecting against unintended breakage. Just as tellingly, they are blunt about its boundary: maintaining 100% MC/DC is laborious and probably not cost-effective for an ordinary application. It pays off for a ubiquitous database library that, by its nature, remembers past mistakes for decades.

Now hold those two beside the failure mode. Twilio Segment's [move from 140+ destination microservices back to a single service](https://www.twilio.com/en-us/blog/developers/best-practices/goodbye-microservices), covered in [Organizations that improve with age](./organizations-that-improve-with-age.md), started as a genuinely good investment (isolating failing partner APIs) before its carrying cost outran its return. The same thing happens on a smaller scale inside a single team. Build a local replay harness after a painful importer outage and, for a year, it compounds: diagnosis drops from days to hours, and the harness makes it safe to simplify the parser and delete old recovery paths. Three years later, that harness carries adapters for two retired services, frozen fixtures from a 2023 file format, and its own flaky CI job. New hires spend more time keeping the simulator alive than reading the importer. Capital turned into an obligation.

Compounding is real, local, and reversible. It is never a smooth exponential curve you switch on once and forget.

## What survives no matter how AI turns out

Throughout this collection, AI has played the role of accelerant: when generating code, tests, and summaries gets cheap, *produced knowledge artifacts* multiply effortlessly while *validated understanding* gets harder to hang onto. Summaries flatten provenance ([What software should remember](./what-software-should-remember.md)). Agents read abandoned branches and promote *"tried and dropped"* into *"proven impossible"* ([The value of forgotten alternatives](./the-value-of-forgotten-alternatives.md)). Juniors merge fluent patches without forming the mental models to catch the next bug ([How engineers become engineers](./how-engineers-become-engineers.md)). Automated mining turns a year of staff workarounds into formal specs ([When software forgets the world](./when-software-forgets-the-world.md)).

Still, any philosophy worth keeping should survive if its starting assumption about AI turns out to be wrong, in either direction.

Suppose AI gets dramatically better not only at writing code, but at *validating* it and reconstructing missing context from sprawling repositories. Even then, half the hard problems in these essays barely budge. No model can tell you whether an external partner's email counts as a contractual promise, settle a political conflict between depot managers and online sales, undo a public API contract customers already built around, or decide who owns the risk when an uninspected generator goes out the door. As machine verification gets cheaper, external commitments, domain contact, and organizational judgment become the whole bottleneck.

Now flip the bet: suppose AI delivers far smaller net speedups than promised once review, integration, and upkeep are put on the ledger (a possibility [Measuring the capacity for change](./measuring-the-capacity-for-change.md) takes seriously). Nothing in the argument breaks there either. Naur's theory building, Parnas's boundaries, Jackson's domain assumptions, and Repenning and Sterman's capability traps all predated modern LLMs. AI didn't invent the problem of what engineering leaves behind; it just raised the stakes on ignoring it.

## When engineering should not try to compound

A framework that tells you to build durable capital everywhere is useless. There are plenty of situations where deliberately *consuming* engineering capital is the sharper call:

- *Pre-fit products and sharp market windows.* If you don't yet know whether customers want the product, investing heavily in long-lived boundaries or replay harnesses builds equity in a company that may pivot next month.
- *Disposable bridges and one-shot migrations.* A script that moves data once before a service shuts down deserves careful verification and zero durable architecture.
- *Fast-moving substrates.* When the underlying platform, vendor API, or regulatory regime is churning faster than an investment can pay back its setup cost, lean code you can throw away beats clever infrastructure.
- *Hard external deadlines.* Missing a statutory cutoff or a seasonal launch can cost far more than the cleanup bill you'll pay in Q2, provided you admit you borrowed from the future and budget to pay it back.

The discipline isn't "always invest." It is knowing when you are building capital, when you are spending it on purpose, and when you are quietly liquidating it by accident.

## Why the pieces only work together

Step back across the earlier eight essays and notice why isolated "best practices" so often fizzle. Engineering capability behaves like a chain rather than a stockpile.

Recorded rationale ([What software should remember](./what-software-should-remember.md)) and honest negative results ([The value of forgotten alternatives](./the-value-of-forgotten-alternatives.md)) keep a team from fighting ghosts, until someone changes the world outside the code and nobody goes looking ([When software forgets the world](./when-software-forgets-the-world.md)). Clean domain insight goes nowhere if day-one commitments locked the schema shut ([Designing for decisions we haven't made yet](./designing-for-decisions-we-havent-made-yet.md)). Great harnesses and clean boundaries still stall if nobody is building the judgment to question them ([How engineers become engineers](./how-engineers-become-engineers.md)), or if organizational incentives punish the team that pays the upfront cost while rewarding everyone else ([Organizations that improve with age](./organizations-that-improve-with-age.md)).

When a team wants to invest, its instinct is usually to polish whatever is already easy: more tests where testing is pleasant, more docs where writing is cheap. The return almost always sits at the weakest link. Look at the last piece of work that dragged on three times longer than it should have and name the one missing piece: an unreproducible failure, an unsettled policy fight, a leaked external contract, or knowledge trapped in one engineer's head. Fix that link before building anything larger.

James March's [Exploration and Exploitation in Organizational Learning](https://pubsonline.informs.org/doi/abs/10.1287/orsc.2.1.71) captures why that takes deliberate protection: exploiting what already works pays off immediately and shows up on this quarter's numbers, while building capability costs time today for returns later. Shipping customer value pays the bills, so an engineering group that treats deadlines as a nuisance loses the business's trust fast. A small, explicit recurring allowance (sized to the system's expected life and reviewed openly so it never turns into a slush fund for pet frameworks) beats both heroic rewrites and secret refactoring.

## One quarter to find out

If you want to test any of this without launching a company-wide transformation, keep it to one twelve-week loop:

1. *Pick one recurring drag.* Choose work your team expects to hit several times this quarter: tricky imports, permission changes, schema rollouts, or incident reproductions.
2. *Build the smallest shareable asset, with a claim and an expiry trigger.* State what future task it should help, cap its upkeep budget, and write down what shift would make it obsolete.
3. *Hand it to someone who didn't build it.* Watch them use it on live work. Log the setup snags and wrong turns alongside the time saved, and use it to teach rather than treating it as a black box.
4. *Tally the full bill and make a call.* At week twelve, weigh saved effort and cleaner decisions against maintenance and review overhead, following [Measuring the capacity for change](./measuring-the-capacity-for-change.md). If it earned its keep, ask what single next improvement it just made cheaper. If it didn't, shrink it or delete it.

Beneath all the talk of AI, architecture, memory, and metrics sits one plain question: *what should engineering leave behind besides software?*

When the next ugly failure lands six months from now, a newcomer should be able to reproduce it in minutes, see why the old guardrails were put there, challenge the ones the world has outgrown, and leave the repository on slightly firmer ground than they found it. Nothing glamorous. Just work that makes the next hard problem a little less expensive than the last one.
