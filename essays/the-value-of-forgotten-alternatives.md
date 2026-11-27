# The value of forgotten alternatives

*Learning from the code we decided not to keep*

“We tried that before” is one of the most expensive sentences in software design. Said with evidence, it saves a team a week. Said from hazy recollection, it kills a good idea because somebody tried a different version of it under different conditions and remembers only that it went badly.

Imagine a design review in which a team proposes caching product availability to take load off an inventory service. Someone recalls an abandoned prototype from two years earlier. The branch is long gone; all that survives is a slide with a latency spike and a vague memory that "the cache blew up during a sale."

Now the team is stuck. Drop the idea? Rebuild the prototype from scratch? Assume a new implementation will somehow dodge whatever broke the old one? They already paid for an investigation and kept too little of it to know what they bought.

## What rejected code actually knows

Production code records the path that won. It says almost nothing about the branches that lost, which is why mature designs often look arbitrary to anyone arriving later, especially when a simpler alternative looks so easy to write.

In that hypothetical inventory service, suppose the old prototype cached availability for a fixed five-minute TTL. During a flash sale, popular items expired together and slammed the inventory database with a synchronized wave of refreshes. Browsing got faster on quiet days and worse at the exact moment it mattered. (Final stock reservation still hit the authoritative service; the cache was only about browsing load, not overselling.)

That specific finding has real teeth. Compressing it into *"caching inventory doesn't work"* throws away the expiry policy, the traffic shape and the actual failure mode, turning one bad prototype into a blanket taboo. A future engineer armed with the real finding knows immediately what to test next: jittered expiry, background refresh, or a different availability model. Without it, they spend half their energy arguing against folklore.

## Four ways an experiment can fail

Teams lump very different outcomes under "failed," even though they call for opposite reactions.

- *Disproven.* A prototype produces a clear counterexample to a required invariant, such as two concurrent callers both reserving the last item. One clean failure settles the question for that design; a thousand green runs do not erase it.
- *Uncompetitive under tested conditions.* A latency benchmark misses its target on a specific workload and hardware profile. That tells you where the bottleneck sits, not that the whole family of designs is hopeless.
- *Inconclusive.* The environment flaked out, the measurements were too noisy, or time ran out before the prototype was finished. Filing this as "rejected" manufactures false confidence out of an unfinished test.
- *Rejected for non-technical reasons.* The prototype worked fine, and the organization still walked away because operating it demanded skills the team lacked, the migration risk wasn't worth it, or the business priority moved on.

The difference matters twice as much once coding agents start reading your repository's history. `"Attempted and abandoned"` is a historical fact. An agent that summarizes it as `"shown not to work"` invents a proof that never existed, and can become remarkably effective at enforcing an organization's old prejudices across every future proposal.

## Keep the boundaries attached to the result

Even a half-page record keeps the scope attached to the conclusion:

```text
Experiment: Fixed-TTL availability cache (branch archived, commit 8a4f2c)
Outcome: Abandoned (missed sale-load latency target)

Question: Can a 5-minute availability cache cut inventory DB load during
promotional bursts without hurting p95 browse latency?

Setup:
- Baseline: Direct DB reads under replayed 2023-11 sale trace (4x normal RPS,
  top 50 SKUs = 62% of traffic). p95 = 180 ms, DB CPU = 84%.
- Variant: In-memory cache, uniform 300s TTL, synchronous miss fill.

Observed:
- Steady-state DB CPU dropped to 31%.
- At each 300s boundary, cache misses spiked to 9x baseline; p95 hit 1,400 ms.

Hypothesis (untested): Synchronized expiry caused the stampede; jittered TTL
or single-flight refresh would likely eliminate it.

Revisit if: We test jittered expiry / request coalescing, or SKU skew drops.
```

Notice what this separates: the question from the verdict, the baseline from the variant, and the observation from the untested explanation.

That separation is worth the extra five minutes because memory drifts fast. In [Belief & Evidence in Empirical Software Engineering](https://www.microsoft.com/en-us/research/publication/belief-evidence-in-empirical-software-engineering/), Prem Devanbu, Thomas Zimmermann and Christian Bird found Microsoft engineers holding firm convictions that often disagreed with measurements from their own projects. One company's data is no universal indictment of intuition, but it is a clear reminder that remembered conclusions deserve a paper trail you can check.

## Preserve enough to challenge, not a museum

Writing down a summary costs minutes. Keeping an experiment runnable for years can cost more than the production code it was meant to illuminate, as runtimes rot and datasets vanish.

Match the artifact to the claim. A concurrency counterexample might reduce to a thirty-line test you can keep forever. A performance result needs the workload generator and environment notes. A strategic walk-away only needs a paragraph explaining the constraint that mattered.

The [ACM's artifact review policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current) draws a distinction worth borrowing without the academic bureaucracy: an artifact merely *being available* is not the same as someone else being able to *run it* and *reproduce the result*. A dead link to an archived branch proves only that someone wrote code once. For a finding likely to shape years of architecture decisions, have a colleague who wasn't involved try to follow the instructions before you archive it. Their stumbling blocks will reveal the missing config flags and overstated conclusions right away.

For smaller detours, a brief note is plenty. Preservation has to stay cheaper than the mistake it prevents.

## When prototyping gets cheap, curation gets harder

Coding agents let a team test five cache variants in the afternoon it once took to build one. That produces far more negative evidence, and far more noise.

An agent asked to optimize the inventory service can benchmark three eviction policies and write a neat report in ten minutes. Someone still has to ask whether the workload resembles real sale traffic. A precise comparison across the wrong workload is still wasted effort.

The deeper risk runs in the opposite direction: agents reading past experiment logs and treating every abandoned path as off-limits. If a rejected prototype becomes a rule, cheap tooling turns an organization into a machine for preserving its blind spots. A good experiment record invites the next investigator (human or agent) to point out which assumption has changed and run a better test.

That also gives teams a clear review boundary. Do not review every discarded line of scratch code. Review the claims that are about to become shared guidance, because future engineers and agents will inherit them without re-running the work.

## Making negative results legitimate

Not all repetition is waste. Re-running an old cache experiment teaches a newcomer how the service behaves under pressure, checks whether the original claim still holds, and occasionally exposes a flawed explanation behind a sound decision. The difference is between *blind* repetition (rebuilding a dead end because nobody knew it existed) and *informed* repetition, starting where the last person stopped.

None of this sticks unless an organization treats a clean negative answer as real work. If only merged features count, engineers have every incentive to nurse a shaky design into production rather than close the experiment honestly. Setting a bounded question and a stopping point upfront makes it safe to walk away without inflating the conclusion to justify the time spent.

Then, the next time someone says *"we tried that before"* about the inventory cache, they can drop a link instead of a sigh. The team might still pass on caching, or it might test jittered expiry that afternoon. Either way, it builds on the work already paid for instead of arguing over who remembers a two-year-old slide deck better.
