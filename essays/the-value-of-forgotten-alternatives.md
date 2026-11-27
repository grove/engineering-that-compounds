# The value of forgotten alternatives

*Learning from the code we decided not to keep*

"We tried that before" is one of the most expensive sentences in software design. Backed by evidence, it saves a week. Said from fuzzy memory, it kills a solid idea because somebody tried a rough cousin of it under different traffic two years ago and only remembers that it ended badly.

Picture a design review (an illustrative case, though every long-lived team has its own version) where someone proposes caching product availability to take load off an inventory service. A senior engineer remembers an abandoned prototype from two years back. The branch was pruned long ago; all that remains is a slide showing a latency spike and a vague recollection that "the cache blew up during a sale."

Now the team is stuck. Drop the idea? Rebuild the prototype from scratch? Bet that a new version will dodge whatever broke the old one? They already paid for an investigation and threw away the part that would let them reuse it.

## What rejected code actually knows

Production code only records the design that won. It stays silent about the branches that lost, which is why mature systems often look weirdly overcomplicated to newcomers, especially when a simpler alternative looks easy to code up over an afternoon.

Suppose that old inventory prototype cached availability with a flat five-minute TTL. During a flash sale, popular items all expired together and hit the database with a synchronized wall of refreshes. Browsing got faster on quiet Tuesdays and fell over at the exact hour the business cared about. (Final stock reservation still went to the authoritative database; the cache was purely for browsing load, not overselling.)

That finding is genuinely useful. Compressing it into *"caching inventory doesn't work"* strips away the expiry policy, the skewed traffic, and the actual failure mode, turning one flawed prototype into a blanket taboo. An engineer handed the real finding knows immediately what to try next: jittered expiry, single-flight coalescing, or background refresh. Without it, they burn half a week arguing against oral history.

There is a quieter cost beyond wasted time: *path dependence*. When abandoned designs harden into folklore, they shrink what a team even thinks to propose next. Each decision steers the next set of experiments, which reinforces the original choice, until nobody remembers why whole regions of the design space became off-limits. Honest records of negative results save rework, and they also keep an organization able to challenge its own history.

## Four ways an experiment can fail

Teams file four very different outcomes under "failed," even though they warrant opposite responses:

- *Disproven.* A prototype turns up a clean counterexample to a required invariant, like two concurrent callers both reserving the last unit. One solid failure rules out that mechanism; a thousand green runs don't rescue it.
- *Uncompetitive under tested conditions.* A latency test misses its target on a specific workload and hardware profile. That locates a bottleneck; it doesn't condemn the entire family of designs.
- *Inconclusive.* The test environment flaked out, the numbers were too noisy, or the sprint ended before anyone finished the prototype. Calling this "rejected" manufactures certainty out of an unfinished test.
- *Rejected for non-technical reasons.* The prototype worked fine, and the company walked away anyway because operating it demanded skills the team didn't have, the migration risk wasn't worth it, or priorities shifted.

That four-way split gets twice as important once coding agents start reading your repo history. `"Attempted and abandoned"` is a historical fact. An agent that summarizes it as `"shown not to work"` invents a proof that never existed, and can enforce an organization's old prejudices across every future proposal with complete confidence.

## Keep the boundaries attached to the result

Half a page is enough to keep the scope glued to the verdict:

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

What earns its keep here is separating the question from the verdict, the observed numbers from the untested hypothesis, and the conditions under which the conclusion stops applying.

Human memory blurs those boundaries almost immediately. In [Belief & Evidence in Empirical Software Engineering](https://www.microsoft.com/en-us/research/publication/belief-evidence-in-empirical-software-engineering/), Prem Devanbu, Thomas Zimmermann, and Christian Bird found Microsoft engineers holding strong convictions that frequently disagreed with measurements from their own projects. One study at one company isn't a blanket indictment of engineering intuition, but it is a sobering reminder that remembered verdicts deserve a paper trail you can actually inspect.

## Preserve enough to challenge, not a museum

Writing a half-page note takes five minutes. Keeping an experiment runnable for three years can cost more than the production code it was meant to inform, as runtimes drift and datasets disappear.

Match the artifact to the claim. A concurrency counterexample often shrinks to a thirty-line test you can keep indefinitely. A performance finding needs the workload generator and hardware notes. A strategic walk-away only needs a short paragraph naming the constraint that mattered.

The [ACM's artifact review policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current) separates an artifact merely being *available* from someone else being able to *run it* and *reproduce the result*. That distinction is worth stealing without the academic paperwork. A dead link to an archived branch only proves someone wrote code once. When a finding is going to steer architecture choices for years, ask a colleague who wasn't involved to follow the notes before you archive them; wherever they trip is where your assumptions went unwritten. For small detours, a brief note is plenty.

## Cheap prototyping raises the bar on curation

With coding agents, a team can prototype five cache variants in the afternoon it once took to build one. You get more negative evidence, and a lot more noise.

An agent asked to optimize the inventory service can benchmark three eviction policies and hand back a spotless report in ten minutes. Someone still has to check whether the test workload actually looks like a flash sale. A sharp comparison against the wrong traffic shape is still wasted effort, only now it comes with charts.

The bigger risk runs the other way: agents scanning past experiment logs and treating every abandoned path as settled law. Good experiment notes should invite the next investigator (human or agent) to spot which premise changed and run a sharper test. That also draws a practical review line: don't review every discarded scratch branch, *do* review the conclusions about to enter shared guidance, because future engineers and agents will inherit them without redoing the work.

## Making a clean "no" count as work

Not all repetition is waste. Re-running an old cache test teaches a newcomer how the service behaves under load, verifies whether the old finding still holds, and occasionally catches a bogus explanation sitting behind a good decision. Blind repetition rebuilds a dead end nobody knew existed; informed repetition starts where the last person stopped.

None of this survives if an organization only rewards merged features. When negative answers look like wasted sprints, engineers quietly nurse shaky designs into production rather than closing an experiment honestly. Naming a bounded question and a stopping rule before writing code makes walking away legitimate, so the next time someone says *"we tried that before,"* they drop a link instead of a sigh.
