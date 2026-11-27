# The ability to delegate

*What has to be true before someone else can take the next step?*

Imagine that the billing team has two tickets. One changes the wording of a receipt. The other changes what happens when a payment notification is delivered twice. The same agent is available for both. It has access to the same repository, can read the tests and knows the language well.

The first ticket can go to the agent with little ceremony. The second leaves an experienced engineer hovering over the terminal. She has to explain how the payment provider retries events, ask for a particular reproduction, notice that the proposed fix keeps its deduplication state in memory, and interrupt before the agent concludes that a green test means the change is ready to deploy.

It is tempting to attribute that difference to the agent's ability. Give it a better model, a more elaborate prompt, another specialist reviewer. But much of the trouble is sitting in the team's own repository. The delivery contract is hard to find. The test demonstrates sequential retries, not what two workers do. The deployment procedure cannot distinguish a harmless retry from a second charge.

Those would be problems for a new colleague, too.

## Look at the interruptions

[Every's Compound Engineering guide](https://every.to/guides/compound-engineering) describes a progression toward more delegated development, supported by better planning, review and tools. There is a useful experiment hiding in that progression. Instead of trying to make the agent do more, find out why the engineer keeps having to intervene.

For a recurring class of work, keep a small record of the interruptions that changed the outcome. What did the engineer know? What was missing from the environment? Would the next engineer encounter the same problem?

In the billing example, the first interruption is about the expected behavior. The second is about constructing the right state. The third concerns the strength of the evidence. They need different repairs.

- Make the current delivery contract discoverable from the handler.
- Retain the duplicate-delivery scenario and a safe way to run it.
- Establish a check for concurrent delivery using the actual transaction and storage guarantees the proposed design relies on.

The third repair may turn out to be expensive. That is useful to know before delegating the next concurrency change. A synthetic replay is not a substitute for it.

The field guide's [Earned delegation](https://grove.github.io/patterns-of-compounding-engineering/) pattern turns these interruptions into a small investigation. Start with one task and one recurring intervention. Improve the environment where it is cheaper than repeated supervision, then try a similar task again.

## A boundary, not a job title

Suppose the team has established the sequential delivery contract, a replay with a reviewed expectation and a way to run it on isolated synthetic data. It can now ask an agent to prepare a small handler change, run the checks and open a pull request. Nobody has to watch each command.

That agreement says what the agent can do, and what it cannot. It can modify the handler in a branch. It can run the local tests. It cannot issue real payments, change the production database, decide that a financial obligation no longer applies, or deploy a change merely because the replay is green.

If the task turns out to require a new transaction boundary, the agent brings the question back. The team might expand the agreement once the necessary evidence and recovery plan exist.

Notice how much more useful that is than declaring a repository ready for autonomous development. Readiness belongs to a particular kind of change. The same repository can support unattended work on an isolated documentation preview and require close supervision of a migration with irreversible effects.

A safe boundary also needs to be enforced. A prompt saying not to touch production is a poor replacement for credentials that cannot touch production. Give the work an isolated environment with the access it actually needs. Where a destructive operation is possible, establish who can authorize it and how recovery will work.

## Improve the method, too

Some interruptions happen even when the information is already available. An experienced engineer knows to inspect the transaction and trace the external side effect before proposing a retry fix. A new engineer sees a loop and starts looking for a missing conditional.

After a couple of similar investigations, it may be worth keeping a short method: the starting question, places to look, evidence to collect, and when to stop. The instructions should point to the tools and current rules rather than repeat them. A person can follow the procedure; an agent can load it as a skill. Both should return a recommendation someone else can inspect.

Try the method on a different failure, including one where the first suspicion is wrong. If it turns every payment problem into an investigation of duplicate delivery, it is not much of a method yet. A more capable skill knows when it does not apply.

This is another place engineering capital can accumulate. A reliable reproducer makes a verification procedure easier to teach. That procedure reveals which remaining checks are worth building. The next investigation can spend its time on a new question instead of recovering the old one.

## Do not delegate away the apprenticeship

There is another way for our engineer to stop interrupting: stop reading the proposed changes. The cost disappears from her calendar and may reappear during an incident.

A useful delegation experiment therefore observes more than the number of questions asked. Did the review catch the same mistakes? Was the work easier to understand? Did someone have to redo the investigation in private? Did the change introduce a new risk? Count that effort along with the time spent building and maintaining the checks.

There are also occasions when an interruption is worth having. A junior engineer investigating their first retry failure should be able to predict what the handler will do, run the replay and explain why the result surprised them. [How engineers become engineers](./how-engineers-become-engineers.md) explains why this experience matters. A useful command can make the lesson cheaper without doing the thinking for them.

Keep such opportunities deliberate. The team may delegate repetitive fixture setup while retaining the investigation of a new business rule as a learning task. The correct amount of supervision depends on what the team is trying to accomplish, including what it wants its people to learn.

## Try it next week

Pick a task you have supervised more than once. Record the moments where you had to step in and why. Pick one intervention to make less necessary; perhaps the missing thing is a worked example, a safer environment or simply a link to a current decision. Give the next attempt the same scope and check the outcome against independent evidence.

If the task becomes easier to hand off, keep the improvement. If the check took longer to maintain than the interruptions it replaced, simplify it. Do not widen the permission boundary just to demonstrate progress.

The interesting possibility is that a team can become better at delegating even if the model never changes. It can also lose that ability when knowledge goes stale, checks become unreliable or an architectural decision invalidates the assumptions. Delegation is a property of the work and the environment, earned over time and subject to revision.

The next essay, [Architecture for parallel work](./architecture-for-parallel-work.md), takes the same question a step further: what happens when several people or agents are ready to work at once?
