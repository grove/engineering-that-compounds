# The value of forgotten alternatives

*Learning from the code we decided not to keep*

"We tried that before" is one of the most expensive sentences in software design. Backed by evidence, it saves a week. Said from fuzzy memory, it kills a solid idea because somebody tried a rough cousin of it under different traffic two years ago and only remembers that it went badly.

Human memory blurs the edges of past experiments fast. In [Belief & Evidence in Empirical Software Engineering](https://www.microsoft.com/en-us/research/publication/belief-evidence-in-empirical-software-engineering/), Prem Devanbu, Thomas Zimmermann, and Christian Bird found Microsoft engineers holding strong convictions that frequently clashed with measurements from their own projects. One study at one company is not an indictment of engineering intuition, of course, but it shows how easily remembered verdicts drift away from the conditions that produced them.

## What rejected code actually knows

Production code only records the design that won. It says nothing about the branches that lost, which is why mature systems often look oddly complicated to newcomers, especially when a simpler version looks like an afternoon's work.

Take a hypothetical design review where someone proposes caching product availability to pull load off an inventory service. A senior engineer remembers an abandoned prototype from two years ago. The branch is long gone; all that survives is an old slide showing a latency spike and a vague memory that "the cache blew up during a sale."

Now the team has an ugly choice: drop the idea, rebuild the prototype from scratch, or gamble that a fresh version will avoid whatever broke the old one. They already paid for an investigation and threw away the part that would let anyone reuse it.

Suppose that earlier prototype cached availability with a flat five-minute TTL. During a flash sale, hot SKUs all expired together and slammed the database with a synchronized wall of refreshes. Browsing got faster on slow Tuesdays and fell over during the one hour the business cared about. (Final stock reservation still went to the authoritative database; the cache only served browsing reads.)

That finding is worth keeping. Compressing it into *"caching inventory doesn't work"* strips out the expiry policy, the skewed traffic, and the actual failure mode, turning one flawed prototype into a permanent taboo. Hand an engineer the real finding and they know right away what to test next: jittered expiry, single-flight coalescing, or background refresh. Without it, they spend half a week arguing with folklore.

Wasted time isn't even the worst cost. When abandoned designs harden into oral history, they create *path dependence*: whole regions of the design space stop getting proposed at all. Each decision steers the next round of work, reinforcing the original choice until nobody remembers what ruled out the alternatives. Honest records of negative results save rework, and they also keep a team capable of challenging its own past.

## Four ways an experiment can fail

Teams lump four very different outcomes under "failed," even though they call for opposite responses:

- *Disproven.* A prototype turns up a clean counterexample to a required invariant, such as two concurrent callers both reserving the last unit. One solid failure rules out that mechanism; a thousand passing runs don't rescue it.
- *Uncompetitive under tested conditions.* A latency test misses its target on a specific workload and hardware profile. That locates a bottleneck; it doesn't condemn the whole family of designs.
- *Inconclusive.* The test environment flaked out, the numbers were noisy, or the sprint ended before anyone finished the prototype. Calling this "rejected" invents certainty out of an unfinished test.
- *Rejected for non-technical reasons.* The prototype worked fine, and the company walked away anyway because operating it demanded skills the team lacked, migration risk was too high, or priorities shifted.

That four-way split matters even more once coding agents start reading repository history. `"Attempted and abandoned"` is a historical fact. An agent that summarizes it as `"shown not to work"` fabricates a proof that never existed, and will then reinforce an organization's old prejudices on every future proposal with complete confidence.

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

The value here comes from keeping three things separate: the question from the verdict, the observed numbers from the untested hypothesis, and the conditions under which the conclusion stops applying.

## Preserve enough to challenge, not a museum

Writing a half-page note takes five minutes. Keeping an experiment runnable for three years can cost more than the production code it was meant to inform, as runtimes drift and datasets vanish.

Match the artifact to the claim. A concurrency counterexample often shrinks to a thirty-line test you can keep indefinitely. A performance finding needs the workload generator and hardware notes. A strategic walk-away only needs a short paragraph naming the constraint that mattered.

The [ACM's artifact review policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current) separates an artifact merely being *available* from someone else being able to *run it* and *reproduce the result*. That distinction is worth borrowing without the academic paperwork. A dead link to an archived branch only proves someone wrote code once. When a finding will steer architectural choices for years, ask a colleague who wasn't involved to follow the notes before you archive them; wherever they trip is where an assumption went unwritten. For small detours, a brief note is plenty.

## Cheap prototyping raises the bar on curation

With coding agents, a team can prototype five cache variants in the afternoon it once took to build one. You get more negative evidence, and a lot more noise.

An agent asked to optimize the inventory service can benchmark three eviction policies and return a polished report in ten minutes. That report is still only a claim until someone verifies whether the test workload actually resembles a flash sale. A sharp comparison against the wrong traffic shape is still wasted effort, just with nicer charts.

The bigger hazard runs the other way: agents scanning old experiment logs and treating every abandoned path as settled law. Good experiment notes invite the next investigator (human or agent) to spot which premise changed and run a sharper test. That also sets a practical review line: don't review every discarded scratch branch, *do* review conclusions about to enter shared guidance, because future engineers and agents will inherit them without redoing the work.

## Making a clean "no" count as work

Not all repetition is waste. Deliberately re-running an old cache test teaches a newcomer how the service behaves under load, checks whether an old finding still holds under new traffic, and occasionally catches a bogus explanation behind a good decision. Blind repetition rebuilds a dead end nobody knew existed; informed repetition starts where the last person stopped.

None of this survives if an organization only rewards merged features. When negative answers look like wasted sprints, engineers nurse shaky designs into production rather than closing an experiment honestly. Stating a bounded question and a stopping rule before writing code makes walking away a normal result, and gives the next team actual evidence to argue with instead of a hallway rumor.
