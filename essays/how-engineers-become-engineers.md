# How engineers become engineers

*An apprenticeship with less implementation*

For half a century, writing code did two jobs at once: it shipped software and it trained the next generation of engineers. Delegating implementation pries those two jobs apart.

In a hypothetical first-year assignment, a new engineer is asked to add retries to a background worker. A coding agent writes a clean patch with tests. The engineer reads the agent's summary, addresses two review comments and merges the pull request.

The ticket is done. What actually happened inside the engineer's head?

Maybe a great deal. Maybe they traced what happens when a worker completes an external call and drops its connection before the acknowledgment arrives, and now see why naive retries duplicate side effects. Or maybe they just got better at recognizing a confident-sounding explanation. From the outside, the git history looks identical.

[Implementation and understanding](https://grove.github.io/software-that-improves-with-age/essays/implementation-and-understanding.html) looked at the grasp experienced engineers lose when they stop writing code. Beneath that sits a harder problem: how does anyone build the judgment needed to supervise delegated work in the first place?

## What the old apprenticeship accidentally gave us

Writing code by hand forced repeated, intimate contact with being wrong. A two-line change tripped an unexpected dependency. A test suite stayed green while a subtle race slipped through. A tidy abstraction cracked under the very next requirement.

The education came from making a bet, however small, and watching reality correct it. Reading somebody else's summary of why retries are tricky is effortless; watching your own worker double-charge a test account leaves a much deeper mark.

None of this was a well-designed curriculum. Plenty of engineers spent years wiring up routine CRUD endpoints without ever chasing a hard concurrency bug, while a lucky colleague learned fast beside a generous mentor on a thorny system. Nobody should be nostalgic for losing an afternoon to broken packaging or writing the same boilerplate client for the fifth time.

Still, stripping away every moment where a beginner has to reason through an unfamiliar mechanism leaves them dependent on explanations they cannot evaluate. The question is not whether juniors should be banned from using AI. It is which parts of a task build judgment and which parts are just typing.

## Practice the judgment, not the boilerplate

Anders Ericsson, Ralf Krampe and Clemens Tesch-Römer's [1993 work on deliberate practice](https://doi.org/10.1037/0033-295X.100.3.363) drew a clear line between simply doing a job and structuring tasks specifically to improve a skill through fast, informative feedback. That psychology research won't hand you a ready-made engineering syllabus, but it points at the right design unit: name the specific judgment you want the learner to build.

"Learn distributed systems" is too broad. "Spot the gap between an operation taking effect and its caller learning that it took effect" is concrete enough to practice.

Give the new engineer a small worker and a service that logs completed actions. Before running a single test, ask them to predict what both sides believe if the network drops at three different points in the handshake. Let an agent build the fault-injection harness and gather the traces. The learner's job is to explain where their prediction missed.

Then shift the scenario. What if the worker also publishes an event to a second queue? What if the deduplication table expires after an hour? Now they have to figure out which part of their earlier reasoning still holds. Drilling the same exercise twice builds familiarity; moving the ground tests whether they actually understood it.

## Show the messy middle

Experienced engineers make debugging look deceptively linear. They glance at three dashboards, ignore five plausible leads, check one counter and point at the bug. The newcomer sees the command that worked and misses the judgment that ruled everything else out.

Allan Collins, John Seely Brown and Ann Holum's account of [cognitive apprenticeship](https://www.aft.org/ae/winter1991/collins_brown_holum) emphasizes making an expert's hidden thinking audible and gradually pulling back support as the learner takes over. On an engineering team, that means narrating an investigation while you are still genuinely unsure, not just walking through a polished postmortem afterward.

When the retry count spikes, say out loud why three explanations fit the graph, what measurement separates them, and which tempting rabbit hole you are ignoring for now. Just as important, admit when you are stumped. If every pairing session ends with the senior engineer unveiling an answer they knew from minute one, beginners absorb a distorted view of expertise. Most senior judgment is knowing how to make progress while still in the dark.

An agent's explanation belongs in a different category. Fluent prose explaining why a patch is safe is a claim to test, not proof that the learner (or the agent) understood the system. One habit that pays off immediately: ask the learner to write down their own mental model *before* prompting the agent. Comparing the two gives them something concrete to push against.

## Withdraw the scaffolding on purpose

Early on, a mentor picks the failure points to inject and helps read the output. A few weeks later, the learner chooses where to break the system and defends the choice. On a later task, they decide whether retries belong in the design at all. Eventually they walk the next hire through the difference between a safe retry and a repeated business action.

AI stays in the room throughout that progression, generating test fixtures, mapping unfamiliar call graphs and mocking up competing designs. What shifts is who frames the question and who signs off on what the evidence proves.

A blanket rule like "no AI for the first six months" misses the point. Hand-coding a tiny queue can expose lifetime and backpressure bugs that a framework hides; hand-coding another standard HTTP client teaches almost nothing. Match the friction to the skill. If the goal is comparing how three retry policies fail under load, having an agent build all three variants lets the learner spend their time on the analysis that actually matters.

## You cannot look up what you don't know to ask

When an explanation is always one prompt away, memory starts to feel optional. It isn't.

What you already carry in your head determines what looks suspicious. An engineer who has internalized ambiguous acknowledgments spots the same trap hiding inside a payment webhook or a cron scheduler. Someone who merely read and approved an agent's retry patch never notices there is a question to ask.

Henry Roediger and Jeffrey Karpicke's [experiments on retrieval practice](https://doi.org/10.1111/j.1467-9280.2006.01693.x) (done on prose retention rather than engineering, so treat them as a clue rather than a recipe) showed that actively recalling material cements it far better than rereading it. The engineering equivalent is light and informal: a few days after the retry work, ask the learner to sketch the failure sequence on a whiteboard without opening the PR; in design reviews, have everyone predict how a change will behave before opening the code. Wrong predictions cost nothing when the room treats them as data instead of a quiz.

## Real stakes, bounded blast radius

Exercises only take you so far. Real production work comes with fuzzy requirements, impatient stakeholders and consequences that show up three weeks after merge.

Apprenticeship needs a ramp into real ownership: start by owning retry behavior for one noncritical worker, with a senior engineer explicitly on call for anything outside the agreed boundary. Let the learner watch the rollout, answer an operator's question, and repair the first assumption that breaks in production. That is worlds apart from tossing a junior into a tangled legacy service alone and calling panic "growth."

Keep them close to users and operators, too. You can become very good at debugging retry loops without ever noticing that the operation should never have been automated in the first place.

## Consuming your own future

Here is the uncomfortable economics underneath all of this: an organization can become measurably more productive this year while liquidating its future supply of expertise.

Mentoring is slow. A senior engineer pairing with an AI agent can ship the retry worker before lunch; mentoring a newcomer through predictions and fault injection takes two days. If leadership measures only weekly throughput, every rational team cuts the mentoring, stops hiring juniors, and lets senior staff plus agents carry the backlog.

That looks brilliant on a quarterly chart. It even looks rational for one company, right up until senior engineers turn over, systems grow weirder, and the firm discovers there is nobody left who can diagnose a novel outage or tell when an agent's confident patch is subtly corrupting data. At the industry level it is a slow-motion tragedy of the commons: everyone wants to hire experienced engineers who can audit AI, and nobody wants to pay for the apprenticeship that creates them.

Fixing that takes an explicit management choice, not heroics from mentors squeezing teaching into their evenings. Decide which tickets double as training investments and budget for them openly. You will know the investment is working when the learner starts asking questions the mentor missed, naming what evidence would change their mind, and flagging risky commitments *before* merging.

The retry patch might take an agent three minutes. Building the engineer who can rescue that system three years from now takes deliberate time. If nobody pays for it today, the bill still comes due later, with interest.
