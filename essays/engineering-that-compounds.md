# Engineering that compounds

*What we choose to carry into the next piece of work*

It is easy to slap the word *compounding* onto any engineering investment that ages well. Held to the stricter definition from [Engineering capital](./engineering-capital.md), where earlier investments improve the economics of *subsequent* investments rather than just paying a steady recurring dividend, real compounding is rarer, more local, and harder to prove.

Look closely at two famous long-horizon engineering bets, and notice the difference between them.

SQLite's [testing architecture](https://www.sqlite.org/testing.html) is roughly 156 thousand lines of core C backed by hundreds of times as much test code, four independent harnesses, fault injection for out-of-memory and I/O errors, assembly-level mutation checks, and 100% MC/DC branch coverage in TH3. The SQLite authors are explicit about what that bought them: a wave of features and speedups added over recent years would not have been possible without full coverage protecting against unintended breakage. Even so, most of what SQLite demonstrates is an extraordinary *recurring return*: a standing safety net that keeps paying on every release. Just as tellingly, its authors warn that maintaining 100% MC/DC is laborious and probably not cost-effective for an ordinary application. It pays off for a ubiquitous database library that must live with past mistakes for decades.

FoundationDB's [deterministic simulation](https://apple.github.io/foundationdb/testing.html) gets closer to true *second-order compounding*. By wiring deterministic simulation straight into their C++ coroutine runtime (`Flow`), the team could run an entire multi-node cluster (disk latency, full drives, dropped packets, rebooting machines, adversarial "swizzle-clogging") inside a single process, roughly ten times faster than wall clock and reproducible from one seed. That early bet did not only catch version-1 bugs. It lowered the cost of building *later* verification and reliability investments: the exact same workload definitions carried directly into their live cluster performance suite (`Circus`), and deterministic seeds made inventing harder fault-injection and recovery machinery feasible at all. As the team puts it, they likely could not have built FoundationDB without it.

Now hold both cases beside the reversal. Twilio Segment's [move from 140+ destination microservices back to a single service](https://www.twilio.com/en-us/blog/developers/best-practices/goodbye-microservices), covered in [Organizations that improve with age](./organizations-that-improve-with-age.md), began as a sensible investment (isolating failing partner APIs) before its carrying cost overtook its return. The same inversion happens inside a single team. Build a local replay harness after an ugly importer outage and, for a year, it compounds: diagnosis drops from days to hours, and the harness makes it safe to simplify the parser and delete old recovery paths. Three years later, that harness carries adapters for two retired services, frozen fixtures from a 2023 file format, and its own flaky CI job. New hires spend more time keeping the simulator alive than reading the importer. Capital turned into an obligation.

Even those real examples are retrospective. They show what to look for, not a general proof that deliberate engineering investment always compounds. Real compounding is local, uneven, and reversible; it is never a neat exponential curve you switch on once and forget.

## What survives no matter how AI turns out

Across these essays, AI has acted as an accelerant on one central tension: when generating code, tests, and summaries gets cheap, *produced knowledge artifacts* multiply while *validated understanding* gets harder to hang onto. Summaries flatten provenance ([What software should remember](./what-software-should-remember.md)). Agents read abandoned branches and promote *"tried and dropped"* into *"proven impossible"* ([The value of forgotten alternatives](./the-value-of-forgotten-alternatives.md)). Juniors merge clean patches without forming the mental models needed to catch the next bug ([How engineers become engineers](./how-engineers-become-engineers.md)). Automated mining turns a year of staff workarounds into formal specs ([When software forgets the world](./when-software-forgets-the-world.md)).

Still, any engineering philosophy worth keeping has to survive if its starting bet about AI turns out to be wrong, in either direction.

Suppose AI improves dramatically not only at generating code, but at *validating* it, running experiments, and reconstructing missing context across huge repositories. That would move much more of the work onto machines, and it shows why the durable boundary isn't "AI writes, humans check." The durable line runs between four distinct roles:

- *Producing a claim* (a patch, a summary, a proposed architecture)
- *Establishing evidence* (tests, traces, reproductions, workload measurements)
- *Judging sufficiency* (deciding whether the evidence covers the real risk)
- *Accepting accountability* (owning the consequences when the bet goes wrong)

Even if machines take over most of the first two roles and assist heavily with the third, half the hard problems in this collection barely budge. No model can tell you whether a partner's email counts as a contractual promise, settle a political conflict between depot managers and online sales, undo a public API contract customers already built around, or decide who eats the cost when an uninspected generator goes out the door. As machine verification gets cheaper, external commitments, domain contact, and human accountability become the main bottleneck.

Now flip the bet: suppose AI delivers much smaller net speedups than promised once review, integration, and upkeep are put on the ledger (a possibility [Measuring the capacity for change](./measuring-the-capacity-for-change.md) takes seriously). Nothing in the argument breaks there either. Naur's theory building, Parnas's boundaries, Jackson's domain assumptions, and Repenning and Sterman's capability traps all predated modern LLMs. AI did not invent the problem of what engineering leaves behind; it just made ignoring it faster.

## When engineering should not try to compound

A framework that tells you to build durable capital everywhere is useless. Plenty of situations call for deliberately *spending* engineering capital instead:

- *Pre-fit products and sharp market windows.* If you don't yet know whether customers want the product, investing heavily in long-lived boundaries or replay harnesses builds equity in a company that may pivot next month.
- *Disposable bridges and one-shot migrations.* A script that moves data once before a service shuts down deserves careful verification and zero durable architecture.
- *Fast-moving substrates.* When the underlying platform, vendor API, or regulatory regime churns faster than an investment can earn back its setup cost, lean code you can throw away beats clever infrastructure.
- *Hard external deadlines.* Missing a statutory cutoff or a seasonal launch can cost far more than the cleanup bill you'll pay in Q2, provided you admit you borrowed from the future and budget to pay it back.

Good engineering is not "always invest." It is knowing when you are building capital, when you are spending it on purpose, and when you are liquidating it by accident.

## Why the pieces only work together

Step back across the earlier eight essays and notice why isolated "best practices" fizzle. Engineering capability behaves like a chain rather than a stockpile.

Recorded rationale ([What software should remember](./what-software-should-remember.md)) and honest negative results ([The value of forgotten alternatives](./the-value-of-forgotten-alternatives.md)) keep a team from fighting ghosts, until the world outside the code shifts and nobody goes looking ([When software forgets the world](./when-software-forgets-the-world.md)). Sharp domain insight goes nowhere if day-one commitments locked the schema shut ([Designing for decisions we haven't made yet](./designing-for-decisions-we-havent-made-yet.md)). Great harnesses and clean boundaries still stall if nobody is building the judgment to question them ([How engineers become engineers](./how-engineers-become-engineers.md)), or if organizational incentives punish the team that pays the upfront cost while rewarding everyone else ([Organizations that improve with age](./organizations-that-improve-with-age.md)).

When a team decides to invest, its first instinct is usually to polish whatever is already pleasant: more tests where testing is easy, more docs where writing is cheap. The return almost always lies at the weakest link. Look at the last piece of work that dragged on three times longer than it should have and name the one missing piece: an unreproducible failure, an unsettled policy fight, a leaked external contract, or knowledge trapped in one engineer's head. Fix that link before building anything larger.

James March's [Exploration and Exploitation in Organizational Learning](https://pubsonline.informs.org/doi/abs/10.1287/orsc.2.1.71) captures why that takes deliberate protection: exploiting what already works pays off immediately and shows up on this quarter's numbers, while building capability costs time today for uncertain returns later. Shipping customer value pays the bills, so an engineering group that treats deadlines as a nuisance loses the business's trust fast. A small, explicit recurring allowance (sized to the system's expected life and reviewed openly so it never turns into a slush fund for pet frameworks) beats both heroic rewrites and secret refactoring.

## One quarter to find out

These essays lay out an argument and a set of bets, not a settled law. If you want to test whether any of it holds on your own team without launching a company-wide transformation, keep it to one twelve-week loop:

1. *Pick one recurring drag.* Choose work your team expects to hit several times this quarter: tricky imports, permission changes, schema rollouts, or incident reproductions.
2. *Build the smallest shareable asset, with a claim and an expiry trigger.* State what future task it should help, cap its upkeep budget, and write down what shift would make it obsolete.
3. *Hand it to someone who didn't build it.* Watch them use it on live work. Log the setup snags and wrong turns alongside the time saved, and use it to teach rather than treating it as a black box.
4. *Tally the full bill and make a call.* At week twelve, weigh saved effort and cleaner decisions against maintenance and review overhead, following [Measuring the capacity for change](./measuring-the-capacity-for-change.md). If it paid off, ask what single next improvement it just made cheaper. If it didn't, shrink it or delete it.

Most writing about AI and software asks how to produce more code faster. The more useful question is simpler: *what does shipping this feature leave us capable of doing next?*

When the next ugly failure lands six months from now, a newcomer should be able to reproduce it in minutes, see why the old guardrails exist, challenge the ones the world has outgrown, and leave the repository on slightly firmer ground than they found it. If an investment doesn't move you closer to that, drop it and try a smaller bet.
