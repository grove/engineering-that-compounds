# Engineering that compounds

*What we choose to carry into the next piece of work*

It is easy to slap the word *compounding* onto any engineering habit that ages well. Held to the stricter standard from [Engineering capital](./engineering-capital.md), where earlier work lowers the cost or raises the yield of *later* investments, often by converting one form of capital into another, real compounding is rarer, more local, and harder to sustain than most engineering slogans admit.

The real cases we looked at earlier make that plain. SQLite's massive testing suite buys an extraordinary recurring dividend, yet its authors warn it would rarely pay for itself in an ordinary app. FoundationDB's deterministic simulation gets closer to genuine compounding because one early runtime bet made whole classes of later testing tools feasible. And Twilio Segment's 140+ destination microservices show the reversal: an architecture that solved real isolation problems early on eventually cost three full-time engineers just to keep upright until the team collapsed it back into a single service.

The same rise and reversal happens at small scale inside an ordinary product team. Build a local replay harness after a bad importer outage and, for a year, it compounds: diagnosis drops from days to hours, and the harness makes it safe to simplify the parser and delete old recovery paths. Three years later, that harness carries adapters for two retired services, frozen fixtures from a 2023 file format, and its own flaky CI job. New hires spend more time keeping the simulator alive than reading the importer. Capital has turned into an obligation.

Even the famous examples are retrospective. They show what to watch for, not a guarantee that deliberate engineering investment always compounds. Real compounding is local, uneven, and reversible; it is never an exponential curve you switch on once and forget.

## What survives no matter how AI turns out

Across these essays, AI has acted as an accelerant on one central tension: when generating code, tests, and summaries gets cheap, *produced knowledge artifacts* multiply while *validated understanding* gets harder to hold onto. Summaries flatten provenance ([What software should remember](./what-software-should-remember.md)). Agents read abandoned branches and promote *"tried and dropped"* into *"proven impossible"* ([The value of forgotten alternatives](./the-value-of-forgotten-alternatives.md)). Juniors merge clean patches without forming the mental models needed to catch the next bug ([How engineers become engineers](./how-engineers-become-engineers.md)). Automated mining turns a year of staff workarounds into formal specs ([When software forgets the world](./when-software-forgets-the-world.md)).

At the same time, coding agents now consume engineering capital directly. Clean module boundaries, deterministic reproducers, executable contract checks, and small pruned constraint indexes make every future agent run sharper; bloated wikis and tangled abstractions make agents confidently wrong faster.

Still, any engineering philosophy worth keeping has to survive if its starting bet about AI turns out to be wrong, in either direction.

What if AI gets dramatically better not only at writing code, but at *validating* it, running experiments, and reconstructing missing context across huge repositories? That would shift far more work onto machines, and it shows why the line that holds isn't "AI writes, humans check." As [What software should remember](./what-software-should-remember.md) laid out, the split runs between four roles: *producing a claim*, *establishing evidence*, *judging sufficiency*, and *accepting accountability*. Even if machines take over most of the first two and assist heavily with the third, half the hard problems in this collection barely budge. No model can tell you whether a partner's email counts as a contractual promise, settle a political conflict between depot managers and online sales, undo a public API contract customers already built around, or decide who eats the cost when an uninspected generator goes out the door. As machine verification gets cheaper, external commitments, domain contact, and human accountability become the main bottleneck.

Now flip the bet: what if AI delivers much smaller net speedups than promised once review, integration, and upkeep are counted (a possibility [Measuring the capacity for change](./measuring-the-capacity-for-change.md) takes seriously)? Nothing in the argument breaks there either. Naur's theory building, Parnas's boundaries, Jackson's domain assumptions, and Repenning and Sterman's capability traps all predated modern LLMs. AI did not invent the problem of what engineering leaves behind; it just made ignoring it faster.

## When engineering should not try to compound

A framework that tells you to build long-lived capital everywhere is useless. Plenty of situations call for deliberately *spending* engineering capital instead:

- *Pre-fit products and sharp market windows.* If you don't yet know whether customers want the product, investing heavily in long-lived boundaries or replay harnesses builds equity in a company that may pivot next month.
- *Disposable bridges and one-shot migrations.* A script that moves data once before a service shuts down deserves careful verification and zero lasting architecture.
- *Fast-moving substrates.* When the underlying platform, vendor API, or regulatory regime churns faster than an investment can earn back its setup cost, lean code you can throw away beats clever infrastructure.
- *Hard external deadlines.* Missing a statutory cutoff or a seasonal launch can cost far more than the cleanup bill you'll pay in Q2, provided you admit you borrowed from the future and budget to pay it back.

Good engineering is not "always invest." It is knowing when you are building capital, when you are spending it on purpose, and when you are liquidating it by accident.

## Why the pieces only work together

Step back across the earlier eight essays and notice why isolated "best practices" fizzle. Engineering capability behaves like a chain rather than a stockpile.

Recorded rationale ([What software should remember](./what-software-should-remember.md)) and clear negative results ([The value of forgotten alternatives](./the-value-of-forgotten-alternatives.md)) keep a team from fighting ghosts, until the world outside the code shifts and nobody goes looking ([When software forgets the world](./when-software-forgets-the-world.md)). Sharp domain insight goes nowhere if day-one commitments locked the schema shut ([Designing for decisions we haven't made yet](./designing-for-decisions-we-havent-made-yet.md)). Great harnesses and clean boundaries still stall if nobody is building the judgment to question them ([How engineers become engineers](./how-engineers-become-engineers.md)), or if organizational incentives punish the team that pays the upfront cost while handing the dividend to someone else ([Organizations that improve with age](./organizations-that-improve-with-age.md)).

Who pays the upkeep and who collects the return matters as much as whether a return exists. An investment that makes the company safer while slowing down the team that maintains it, or eroding the influence of the specialists who shared what they knew, will stall unless leadership accounts for the trade.

When a team does decide to invest, its first instinct is usually to polish whatever is already pleasant: more tests where testing is easy, more docs where writing is cheap. The return almost always lies at the weakest link. Look at the last piece of work that dragged on three times longer than it should have and name the one missing piece: an unreproducible failure, an unsettled policy fight, a leaked external contract, or knowledge trapped in one engineer's head. Fix that link before building anything larger.

James March's [Exploration and Exploitation in Organizational Learning](https://pubsonline.informs.org/doi/abs/10.1287/orsc.2.1.71) captures why that takes deliberate protection: exploiting what already works pays off immediately and shows up on this quarter's numbers, while building capability costs time today for uncertain returns later. Shipping customer value pays the bills, so an engineering group that treats deadlines as a nuisance loses the business's trust fast. A small, explicit recurring allowance (sized to the system's expected life and reviewed openly so it never turns into a slush fund for pet frameworks) beats both heroic rewrites and secret refactoring.

## One quarter to find out

These essays lay out an argument and a set of bets, not a settled law. If you want to test whether any of it holds on your own team without launching a company-wide transformation, keep it to one twelve-week loop:

1. *Pick one recurring drag.* Choose work your team expects to hit several times this quarter: tricky imports, permission changes, schema rollouts, or incident reproductions.
2. *Build the smallest shareable asset, with a claim and an expiry trigger.* State what future task it should help, cap its upkeep budget, and write down what shift would make it obsolete.
3. *Put it in someone else's hands.* Watch a teammate who didn't build it use it on live work. Log the setup snags and wrong turns alongside the time saved, and use it to teach rather than treating it as a black box.
4. *Tally the full bill and make a call.* At week twelve, weigh saved effort and cleaner decisions against maintenance and review overhead, following [Measuring the capacity for change](./measuring-the-capacity-for-change.md). If it paid off, ask what single next improvement it just made cheaper. If it didn't, shrink it or delete it.

Most writing about AI and software asks how to produce more code faster. The more useful question is simpler: *what does shipping this feature leave us capable of doing next?*

When a strange failure lands six months from now, a newcomer should be able to reproduce it in minutes, see why the old guardrails exist, challenge the ones the world has outgrown, and leave the repository on slightly firmer ground than they found it. If an investment doesn't move you closer to that, drop it and try a smaller bet.
