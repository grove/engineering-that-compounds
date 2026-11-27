# How engineers become engineers

*An apprenticeship with less implementation*

For fifty years, writing code quietly did two jobs at once: it shipped software and it trained the next generation of engineers. Delegating implementation pulls those two jobs apart.

Picture a first-year engineer (an illustrative setup, though increasingly ordinary) asked to add retries to a background worker. A coding agent writes a tidy patch with unit tests. The engineer reads the agent's summary, answers two review comments, and merges the PR.

The ticket is closed. What actually changed inside the engineer's head?

Maybe plenty. Maybe they traced what happens when a worker completes an external call and drops its connection before the acknowledgment comes back, and now see why naive retries duplicate side effects. Or maybe they just got better at recognizing a confident-sounding pull request description. From the outside, the git log looks identical.

[Implementation and understanding](https://grove.github.io/software-that-improves-with-age/essays/implementation-and-understanding.html) looked at the grasp experienced engineers lose when they stop writing code. Underneath sits a harder problem: how does a beginner build the judgment needed to supervise delegated work in the first place?

## What the old apprenticeship gave us by accident

Writing code by hand forced repeated, firsthand contact with being wrong. A two-line change tripped an unexpected dependency. A green test suite let a subtle race slip straight past. A tidy abstraction cracked under the very next ticket.

The education came from making a small bet and watching reality push back. Reading someone else's explanation of why retries are tricky goes down smoothly; watching your own worker double-charge a test account leaves a mark that sticks for ten years.

None of that was a thought-out curriculum. Plenty of juniors spent years wiring up routine CRUD endpoints without ever chasing a hard concurrency bug, while a lucky peer learned fast beside a generous mentor on a messy system. Nobody misses losing an afternoon to broken packaging or hand-typing a fifth identical HTTP client.

Still, there is a floor of hands-on coding fluency you cannot skip. A beginner who has never wrestled with sockets, mutable state, or a broken stack trace lacks the basic vocabulary to predict what a system might do, or even to spot what looks odd in an agent's output. There is a big difference between removing pointless friction and removing formative struggle. Keeping some early work unassisted (writing a small worker or parser from scratch before touching an agent) builds the footing that makes higher-level judgment exercises possible at all.

## Practice the judgment, not the boilerplate

Anders Ericsson, Ralf Krampe, and Clemens Tesch-Römer's [1993 paper on deliberate practice](https://doi.org/10.1037/0033-295X.100.3.363) separated simply doing a job from designing tasks aimed at sharpening a specific skill through quick, clear feedback. Psychology won't hand you a ready-made engineering syllabus, but it gives you the right unit of design: name the exact judgment you want the newcomer to acquire.

"Learn distributed systems" is too vague. "Spot the gap between an operation taking effect and its caller finding out it took effect" is concrete enough to practice.

Give the new engineer a small worker and a service that logs completed actions. Before running a test, ask them to predict what both sides believe if the network drops at three different points in the handshake. Let an agent build the fault-injection harness and capture the traces. The learner's job is to explain where their prediction missed.

Then shift the ground. What if the worker also publishes to a second queue? What if the deduplication table expires after an hour? Now they have to work out which pieces of their reasoning still hold. Repeating the exact same drill builds muscle memory; changing one constraint tests understanding.

## Show the messy middle

Experienced engineers make debugging look deceptively straight-line. They glance at three dashboards, ignore five tempting leads, check one counter, and point at the bug. The newcomer sees the command that worked and misses all the judgment that ruled out everything else.

Allan Collins, John Seely Brown, and Ann Holum's account of [cognitive apprenticeship](https://www.aft.org/ae/winter1991/collins_brown_holum) stresses making an expert's hidden thinking audible, then gradually pulling support back as the learner takes over. On a software team, that means narrating an investigation while you are still genuinely unsure, rather than walking through a cleaned-up postmortem after the answer is known.

When the retry counter spikes, say out loud why three hypotheses fit the graph, what check separates them, and which rabbit hole you're leaving alone for now. Just as important, admit when you are stumped. If every pairing session ends with the senior unveiling an answer they knew from minute one, beginners pick up a cartoon picture of expertise. Most senior judgment is knowing how to stay oriented while still in the dark.

An agent's explanation belongs in a different bucket. Smooth prose explaining why a patch is safe is a claim to check, not evidence that either the learner or the agent understood the code. One simple habit helps right away: ask the newcomer to write down their own mental model *before* prompting the agent. Comparing the two gives them something concrete to push against.

## Withdraw the scaffolding on purpose

Early on, a mentor picks the failure points to inject and helps read the trace. A few weeks later, the learner picks where to break the system and argues for why. On a later ticket, they decide whether retries belong in the design at all. Eventually they walk the next hire through the difference between a safe retry and a duplicated business action.

AI stays in the room across that ramp, generating fixtures, mapping unfamiliar call graphs, and mocking up competing designs. What moves is who frames the question and who signs off on what the evidence proves. Blanket rules like *"no AI for six months"* miss the distinction: hand-coding a tiny queue exposes backpressure and lifetime bugs that frameworks hide, while hand-coding another REST boilerplate teaches almost nothing. Match the struggle to the skill you actually want built.

## You cannot look up what you don't know to ask

When an explanation is always one prompt away, memory starts to feel optional. It isn't.

What sits in your head determines what looks suspicious. An engineer who has internalized ambiguous acknowledgments spots the same trap hiding inside a payment webhook or a cron job. Someone who merely read and approved an agent's retry patch never notices there is a question to ask.

Henry Roediger and Jeffrey Karpicke's [experiments on retrieval practice](https://doi.org/10.1111/j.1467-9280.2006.01693.x) (run on prose retention rather than programming, so read them as a clue rather than law) showed that actively recalling material cements it much better than rereading it. The engineering version is light and informal: a few days after the retry ticket ships, ask the learner to sketch the failure sequence on a whiteboard without opening the PR; in design reviews, have everyone predict how a change behaves before opening the code. Wrong predictions cost nothing when the room treats them as data instead of a pop quiz.

## Real stakes, bounded blast radius

Exercises only carry you so far. Real production comes with fuzzy specs, impatient users, and consequences that surface three weeks after merge.

Apprenticeship needs a ramp into real ownership: start by owning retry behavior for one noncritical worker, with a senior explicitly backing them up outside the agreed boundary. Let the learner watch the rollout, field an operator's question, and repair the first assumption that breaks live. That is worlds apart from throwing a junior into a tangled legacy service alone and calling panic "growth." Keep them close to users and operators, too. You can get very sharp at debugging retry loops without ever noticing that the operation should never have been automated.

## Consuming your own future

Beneath all of this sits an ugly economic fact: a company can get measurably faster this year while liquidating its future supply of senior engineers.

Mentoring is slow. A senior paired with a coding agent can ship the retry worker before lunch; walking a junior through predictions and fault injection takes two days. If leadership only watches weekly throughput, every rational team drops the mentoring, stops hiring juniors, and lets senior staff plus agents clear the backlog.

That looks terrific on a quarterly chart. It even looks sensible for one firm, until senior engineers leave, systems get weirder, and there is nobody left who can diagnose a novel outage or catch when an agent's clean patch is quietly corrupting data. Across the industry it is a slow tragedy of the commons: everyone wants to hire experienced engineers who can audit AI, and nobody wants to pay for the apprenticeship that produces them.

Fixing that takes a management decision, not mentors burning their evenings out of goodwill. Decide which tickets double as training investments and budget for them openly. You'll know it's working when the junior starts asking questions the mentor missed, naming what evidence would change their mind, and catching risky commitments *before* merge.

An agent can produce the retry patch in three minutes. Growing the engineer who can rescue that service three years from now takes real time. If nobody pays for it now, the bill still lands later, with interest.
