# How engineers become engineers

*An apprenticeship with less implementation*

For fifty years, writing code did two jobs at once: it shipped software, and it trained the next generation of engineers. Delegating implementation splits those two jobs apart.

Picture a first-year engineer asked to add retries to a background worker. A coding agent writes a clean patch with unit tests. The engineer reads the agent's summary, answers two review comments, and merges the PR.

The ticket is closed. What actually changed inside the engineer's head?

Maybe plenty. Maybe they traced what happens when a worker completes an external call and drops its connection before the acknowledgment comes back, and now understand why naive retries duplicate side effects. Or maybe they just got better at recognizing a confident pull-request description. From the outside, the git log looks identical.

[Implementation and understanding](https://grove.github.io/software-that-improves-with-age/essays/implementation-and-understanding.html) looked at the grasp experienced engineers lose when they stop writing code. There is a harder question behind it: how does a beginner build the judgment needed to supervise delegated work in the first place?

## What the old apprenticeship gave us by accident

Writing code by hand forced repeated, firsthand contact with being wrong. A two-line edit tripped an unexpected dependency. A green test suite let a race condition slip straight past. An abstraction cracked under the very next ticket.

The education came from making a small bet and watching reality push back. Reading someone else's explanation of why retries are tricky goes down smoothly; watching your own worker double-charge a test account leaves a mark that sticks for ten years.

None of that was a well-designed curriculum. Plenty of juniors spent years wiring up routine CRUD endpoints without ever chasing a hard concurrency bug, while a lucky peer learned fast beside a generous mentor on a messy system. Nobody misses losing an afternoon to broken packaging or hand-typing a fifth identical HTTP client.

My working bet is that there is still a floor of hands-on coding fluency beginners shouldn't skip: wrestling with sockets, mutable state, or a broken stack trace builds the feel for what a system will do, and for what looks off in an agent's diff. That bet is a hypothesis, not settled law. Nobody yet knows exactly where the floor sits, and teams will have to find it empirically by watching where AI-first juniors stumble during unfamiliar outages or subtle state bugs. Removing pointless friction is welcome; removing formative struggle by accident is the risk. Keeping some early work unassisted, like building a small worker or parser from scratch before bringing in an agent, is a sensible hedge while we find out which struggles really matter.

## What an AI-native apprenticeship can do better

It is easy to talk about AI in onboarding as pure loss. That misses half the picture. The old apprenticeship was slow, uneven, and depended heavily on luck: which failures happened to hit production while a junior was on the team, and whether a senior had time to explain them.

Used deliberately, AI opens up forms of practice that the old model rarely offered:

- *Compressed exposure to rare failure modes.* A newcomer does not have to wait two years for a partial network partition, a poisoned queue message, or a clock-skew bug to hit production. An agent can spin up a local fault-injection harness in minutes and let the learner break a small worker ten different ways in an afternoon.
- *Fast, low-stakes feedback loops.* Instead of waiting half a day for a senior to point out a flawed mental model, a learner can write down their prediction, ask an agent to generate a minimal reproducer that tests it, and see right away where reality diverged.
- *Breadth across unfamiliar codebases.* Mapping call graphs, tracing how data crosses service boundaries, or comparing two competing designs side by side used to take a junior a week before they even understood the question. Getting that map quickly leaves more time for the hard part: deciding what the evidence proves.

Notice how this connects back to [Engineering capital](./engineering-capital.md): an executable asset like a fault-injection harness does not only catch bugs in CI. Handed to a beginner alongside a prediction exercise, it converts directly into human judgment. None of that happens by default, though. Left to itself, AI makes passive approval the path of least resistance: accept the diff, skim the summary, move to the next ticket. An AI-native apprenticeship can beat the old accidental one, *if* a team turns cheap generation into structured practice instead of skipping practice altogether.

## Practice the judgment, not the boilerplate

Anders Ericsson, Ralf Krampe, and Clemens Tesch-Römer's [1993 paper on deliberate practice](https://doi.org/10.1037/0033-295X.100.3.363) separated doing a job from designing exercises aimed at a specific skill with fast, clear feedback. Psychology will not hand you a ready-made engineering syllabus, but it gives you the right unit of design: name the exact judgment you want the newcomer to build.

"Learn distributed systems" is too vague. "Spot the gap between an operation taking effect and its caller learning that it took effect" is concrete enough to practice.

Give the new engineer a small worker and a service that logs completed actions. Before running a test, ask them to predict what both sides believe if the network drops at three points in the handshake. Let an agent build the fault-injection harness and capture the traces. The learner's job is to explain where their prediction missed.

Then move the goalposts. What if the worker also publishes to a second queue? What if the deduplication table expires after an hour? Now they have to work out which parts of their reasoning still hold. Repeating the same drill builds routine; changing one constraint tests understanding.

## Show the messy middle

Experienced engineers make debugging look deceptively straight-line. They glance at three dashboards, ignore five tempting leads, check one counter, and point at the bug. The newcomer sees the command that worked and misses all the judgment that ruled out everything else.

Allan Collins, John Seely Brown, and Ann Holum's account of [cognitive apprenticeship](https://www.aft.org/ae/winter1991/collins_brown_holum) emphasizes making an expert's hidden thinking audible, then gradually pulling support back as the learner takes over. On a software team, that means narrating an investigation while you are still unsure, rather than walking through a cleaned-up postmortem after the answer is known.

When the retry counter spikes, say out loud why three hypotheses fit the graph, what check separates them, and which rabbit hole you're leaving alone for now. Even more important, admit when you are stumped. If every pairing session ends with the senior unveiling an answer they knew from minute one, beginners pick up a cartoon picture of expertise. Most senior judgment is knowing how to stay oriented while still in the dark.

An agent's explanation belongs in a different category. Fluent prose explaining why a patch is safe is a claim to test, not proof that either the learner or the agent understood the code. One simple habit helps right away: ask the newcomer to write down their own mental model *before* prompting the agent. Comparing the two gives them something concrete to push against.

## Withdraw the scaffolding on purpose

Early on, a mentor picks the failure points to inject and helps read the trace. A few weeks later, the learner picks where to break the system and argues for why. On a later ticket, they decide whether retries belong in the design at all. Eventually they walk the next hire through the difference between a safe retry and a duplicated business action.

AI stays in the room across that ramp, generating fixtures, mapping unfamiliar call graphs, and mocking up competing designs. What shifts is who frames the question, who decides what evidence is strong enough, and who signs off on the risk. Blanket rules like *"no AI for six months"* miss the point: hand-coding a tiny queue exposes backpressure and lifetime bugs that frameworks hide, while hand-coding another REST client teaches almost nothing. Match the struggle to the skill you want built.

## You cannot look up what you don't know to ask

When an explanation is always one prompt away, memory starts to feel optional. It isn't.

What you carry in your head determines what looks suspicious. An engineer who has internalized ambiguous acknowledgments spots the same trap hiding inside a payment webhook or a cron job. Someone who only read and approved an agent's retry patch never notices there is a question to ask.

Henry Roediger and Jeffrey Karpicke's [experiments on retrieval practice](https://doi.org/10.1111/j.1467-9280.2006.01693.x) (run on prose retention rather than programming, so treat them as a clue rather than law) showed that actively recalling material cements it much better than rereading it. The engineering version is light and informal: a few days after the retry ticket ships, ask the learner to sketch the failure sequence on a whiteboard without opening the PR; in design reviews, have everyone predict how a change behaves before opening the code. Wrong predictions cost nothing when the room treats them as data instead of a pop quiz.

## Real stakes, bounded blast radius

Exercises only take you so far. Real production brings fuzzy specs, impatient users, and consequences that surface three weeks after merge.

Apprenticeship needs a ramp into real ownership: start by owning retry behavior for one noncritical worker, with a senior explicitly backing them up outside the agreed boundary. Let the learner watch the rollout, field an operator's question, and repair the first assumption that breaks live. That is worlds apart from dropping a junior into a tangled legacy service alone and calling panic "growth." Keep them close to users and operators, too. You can get very good at debugging retry loops without ever noticing that the operation should never have been automated.

## Consuming your own future

Behind all of this sits a hard economic fact: a company can get measurably faster this year while liquidating its future supply of senior engineers.

Mentoring is slow. A senior paired with a coding agent can ship the retry worker before lunch; walking a junior through predictions and fault injection takes two days. If leadership only watches weekly throughput, every rational team drops mentoring, stops hiring juniors, and lets senior staff plus agents clear the backlog.

That looks great on a quarterly chart. It even looks sensible for one firm, until senior engineers leave, systems get stranger, and nobody is left who can diagnose a novel outage or catch when an agent's clean patch is corrupting data. Across the industry it becomes a slow tragedy of the commons: everyone wants to hire experienced engineers who can audit AI, and nobody wants to pay for the apprenticeship that produces them.

Fixing that takes a management decision, not mentors burning their evenings out of goodwill. Decide which tickets double as training investments and budget for them openly. You'll know it's working when the junior starts asking questions the mentor missed, naming what evidence would change their mind, and catching risky commitments *before* merge, rather than approving diffs faster.
