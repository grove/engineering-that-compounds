# The value of forgotten alternatives

*Learning from the code we decided not to keep*

“We tried that before” is an awkward thing to hear during a design discussion. It might save everyone a week. It might also mean that somebody tried a different thing, under different conditions, and remembers only the disappointment.

Suppose a team considers caching product availability to reduce load on an inventory service. An engineer recalls a prototype that was abandoned two years earlier. The branch is gone. There is a presentation with a graph, but no record of the workload. The engineer remembers that the cache behaved badly during a sale.

Should the team abandon the idea? Rebuild the prototype? Trust that a new implementation will avoid the old problem?

The previous investigation has left a warning, but little usable knowledge. The team paid to learn something and kept too little to find out what it was.

## What a rejected design can tell us

An implementation that never reaches production can still answer a consequential question. A prototype may reveal that a proposed interface cannot express a necessary operation. A workload may expose a performance cost that makes a design unattractive. Trying to automate a process may uncover a decision that somebody had been making informally for years.

Successful software tends to preserve evidence of the path chosen. It is harder to recover the alternatives that helped us choose it. Their absence can make the current design look arbitrary, especially to someone who can see how easily an apparently simpler version could be written.

In the inventory example, imagine that the original prototype cached each product's availability for a fixed interval. When popular entries expired together, refreshes arrived at the inventory service in a burst. The cache reduced ordinary browsing load but worsened response times during the particular sale workload the team tested. The final reservation still went through the authoritative inventory service; the experiment concerned browsing and load, not permission to sell nonexistent stock.

That finding is useful. “Caching inventory does not work” loses most of its usefulness. It hides the cache policy, the workload and the property that disappointed the team. It also turns a result about one design into a prohibition on a broad family of designs.

A future engineer might investigate staggered expiry, background refresh or a different representation of availability. The old experiment should help them choose a worthwhile question. It should not force them to defend themselves against an unexplained institutional preference.

## Different ways for an experiment to end

Several outcomes get called failure, although they should lead to different decisions.

A prototype can produce a clear counterexample to a proposed guarantee. If a design allows two callers to reserve the last item, one reproducible execution is enough to show that the guarantee does not hold for that design. Repeated successful runs do not cancel the counterexample.

A performance experiment is usually less decisive. An implementation may miss a latency target under a particular workload on particular hardware. That result tells us where to investigate and whether the design is promising enough to continue. It does not establish that every implementation of the idea must miss the target.

An experiment can also be inconclusive. The measurement may be too noisy. The environment may fail before the behavior of interest appears. The prototype may take longer to complete than the team can afford. Recording these as rejected approaches makes future readers too confident about what was learned.

Sometimes an experiment succeeds technically and the organization still chooses another direction. The design might require an operational skill the team does not have, impose an unacceptable migration, or solve a problem that has ceased to matter. Those are reasonable grounds for a decision. They ought to remain visible as such.

The distinction matters particularly when an agent summarizes a collection of investigations. “Attempted and abandoned” is a fact about the work's history. Converting it into “shown not to work” adds a conclusion the evidence may not support.

## Keep the scope attached to the result

For the inventory cache, a useful record would identify the question before explaining the outcome. Was the goal to reduce database work, improve browsing latency, or keep the service available during a sale? A design can help with one and hurt another.

The record should describe enough of the experiment to interpret the result: the versions tested, the request distribution, the expiry policy, the resources available and the way measurements were taken. Keep the baseline. Without it, a graph can tell us that a service was slow while telling us nothing about the proposed change.

It should then separate what was observed from the explanation. The service received a burst of refresh requests after entries expired. The team believes synchronized expiry caused the slowdown. A further experiment which changes only the expiry behavior would provide stronger evidence for that explanation. These are different claims, and each may be useful later.

There is good reason to be careful about conclusions that harden into professional instinct. In [Belief & Evidence in Empirical Software Engineering](https://www.microsoft.com/en-us/research/publication/belief-evidence-in-empirical-software-engineering/), Prem Devanbu, Thomas Zimmermann and Christian Bird studied developers' beliefs at Microsoft alongside project evidence. They found strongly held beliefs that did not necessarily agree with evidence from the developers' own projects. This was a particular study, not a verdict on engineering experience. It does show why a remembered conclusion deserves an inspectable basis.

Scope also includes the conditions under which a result deserves another look. A change in traffic distribution, the expiry mechanism or the underlying inventory service could make the old experiment less relevant. Listing these conditions gives a future maintainer a starting point for reconsideration.

## Preserve enough to challenge it

Keeping a report is cheap. Keeping an experiment runnable for years may not be. Old runtimes disappear, datasets become unavailable and a reproduction can acquire more maintenance needs than the production code it was supposed to illuminate.

The right amount of preservation depends on the claim. A concurrency error may reduce to a small sequence of operations and a test. A performance claim may require the original workload generator and environment description. A business decision may require a record of the constraint that ruled out an otherwise workable design.

An archive is not the same thing as a validated result. The [ACM's artifact review policy](https://www.acm.org/publications/policies/artifact-review-and-badging-current) explicitly separates making artifacts available, evaluating them, and validating results. Internal investigations do not need academic badges, but the distinction is useful. A link to an old branch tells us that material exists. It does not tell us that someone else can run it or obtain the reported result.

For a result that will guide many future decisions, ask a colleague who did not conduct the investigation to follow the instructions. The attempt may expose an omitted configuration, a hidden dependency or a conclusion broader than the measurements. That is useful review work even when the colleague agrees with the result.

For a minor investigation, a short account may be enough. Preservation should be proportionate to the cost of being wrong and the likelihood that the question will return. We do not need a permanent laboratory for every idea we decline to pursue.

## When experiments become cheap

AI may let a team investigate more alternatives in the time it previously spent building one prototype. That changes the volume of material available to preserve. It does not remove the effort of deciding which findings deserve to influence later work.

An agent asked to optimize the inventory service could construct several cache variants, run them against the same workload and summarize the results. The team should still inspect the workload and decide whether it represents the pressure the service actually faces. A precise comparison among irrelevant designs remains irrelevant.

It would also be easy for several agents to rediscover the same difficulty independently. A short, searchable record linked from the inventory interface could tell each investigator which expiry behavior was previously tested and what happened. The next assignment can then start from a sharper question.

There is a cost to giving old findings too much authority. If an agent treats every rejected approach as forbidden, the organization may become unusually efficient at protecting its mistakes. A useful record should invite a successor to identify a changed assumption or a better experiment. The agent's report can say why the new attempt differs from the old one, rather than quietly ignoring it or accepting it as law.

This gives us a practical review boundary. We need not examine every discarded line of experimental code. We should examine claims that are being promoted into shared guidance, because later people and agents may rely on them without repeating the work.

## Some repetition is worthwhile

Avoiding repeated work is only one possible benefit of engineering memory. Repeating an experiment can teach a new maintainer how the system behaves. It can check whether a previous result still holds. It can reveal that an explanation was mistaken even though its practical recommendation happened to be sound.

The aim should therefore be to make repetition informed. A newcomer who reruns the cache workload should know which behavior to look for and why it matters. They might predict the refresh burst, change the expiry policy and discover whether the explanation survives. That is a more useful exercise than rebuilding the prototype without knowing anybody has tried it before.

The organization also has to make it acceptable to keep a disappointing result. An investigation should be judged partly by the uncertainty it resolved. If only merged code counts as progress, an engineer has a reason to salvage a weak design rather than close the experiment. Producing a clear answer that an approach is unsuitable can be the more valuable outcome.

That does not excuse aimless experimentation. A bounded question and an agreed stopping point make it possible to distinguish useful negative evidence from work that never acquired a purpose. They also let a team stop without inventing a stronger conclusion to justify the time already spent.

Return to the next discussion about the inventory cache. “We tried that before” could be followed by a link to a small reproduction, an explanation of the workload and a note about what remains unresolved. The team might decide to leave the cache alone. It might decide that a different expiry policy is now worth trying.

Either decision would make better use of the earlier work than another argument about who remembers it correctly.
