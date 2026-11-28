# Engineering by exception

*What changes when routine work can finish without us?*

Consider a team that maintains access policies for a company's internal applications. A support group needs a new tool. A service needs to read another service's data. An incident creates a temporary need for wider access. Each request becomes a policy change that an engineer prepares, checks and releases.

This is a hypothetical team. Coding agents can prepare the changes quickly, but an engineer still visits every request. She checks who authorized it, explains the application's particular rules and decides whether the evidence is sufficient. Her day fills with short interruptions from work that appears to be happening by itself.

An alternative would let familiar, authorized changes finish without her participation. Unfamiliar consequences and unresolved decisions would return to the right person. The team would also investigate why ordinary access decisions require engineering work at all.

[Automating the work of engineering](./automating-the-work-of-engineering.md) follows the machinery needed for one recurring job. Here we will follow the surrounding stream: what enters, what comes back to people and what could disappear.

## Find out what the engineer contributes

Watch several requests through to completion. On one, the engineer repairs a test environment using an obsolete group membership. On another, she notices that permission to view a case also permits downloading its attachments. On a third, she asks whether an outside support partner should retain access after an assignment ends.

These interventions need different answers. The environment needs a repair. The attachment behavior needs an explicit account of what the permission includes. The partner's continuing access needs a decision from someone responsible for the relationship and the information involved.

Record what was missing and how the engineer established the answer. Include work that went smoothly. She may have quietly chosen the correct application owner or noticed that a familiar role name means something different in this service. That contribution needs to be understood before anyone assumes it has become unnecessary.

Across requests, common causes may emerge. Perhaps every application translates the same approved business role into a different set of local permissions. An agent could learn those translations. The team could also ask whether the product architecture still needs them. [The ability to delegate](./the-ability-to-delegate.md) investigates individual interruptions; a stream of them can reveal a structural problem.

## Give familiar work a complete route

Begin with an existing group receiving an existing permission whose meaning is already established. The responsible owner has authorized that assignment. The request identifies its scope and, where appropriate, its expiry. There is no new business decision for the engineer to make.

A complete route would verify that authorization, prepare the policy change, evaluate it and apply it within the agreed scope. Checks need examples of access that should succeed and access that should remain denied. Ordinary programs can perform stable comparisons and enforce the rules. An agent might investigate an unfamiliar failure or help construct a missing diagnostic.

The route has to reach the useful outcome. Automatically opening a pull request leaves much of the work intact if someone must inspect every one. Find out what that inspection contributes. The team may be able to establish the same evidence without repeated review for this class of change. Where it cannot, keep the review and the unresolved question visible.

OpenAI's [account of harness engineering](https://openai.com/index/harness-engineering/) describes human QA becoming a constraint as agent-produced changes increased. The team made application behavior and observability accessible to agents and enforced architectural rules. That account concerns one new product, not access management or a general productivity multiplier. It illustrates the value of investigating what people repeatedly supply around generated code.

A request that requires a new role or changes what an existing permission allows has left our familiar class. The workflow needs to recognize that departure. Approval for a known permission does not authorize an agent to redefine it.

## Return an actual decision

Suppose the support partner asks to download attachments so it can diagnose a case offline. The request looks like a small extension to an existing role. It also changes where the information can go and how long it may remain available.

A useful interruption states that difference. It identifies the affected information, the current restriction, the proposed behavior and the decision required. The responsible owner can permit the change, choose another way to support the work or decline it. A message saying "Please review this policy" leaves the engineer to reconstruct the question.

Some exceptions can be resolved with better evidence. Perhaps attachment download was already included in the approved role but the application's check failed to reflect it. Others expose a real choice that should remain with a person. Repeated requests do not, by themselves, settle that choice.

Treat an unresolved decision as a legitimate result. If the workflow is judged only by changes completed, a plausible patch looks better than a necessary question. The same applies to the people operating it: declining an inappropriate change should not count as failure to deliver.

## Remove the recurring engineering request

The team could accumulate instructions for translating each business role into every application's permissions. That might reduce interruptions while preserving a growing collection of special cases.

A more substantial investment would let applications ask a shared authorization service about permissions whose meanings are explicitly defined. Application-specific behavior would still need engineering, but an ordinary change to who holds an established role would no longer require separate policy patches across services.

That proposal needs investigation. Two applications may use the same word for different responsibilities. Combining their rules carelessly could grant access nobody intended. The team should first establish which decisions are shared, keep necessary differences explicit and try the boundary on a useful subset of applications.

If it works, an owner could authorize the routine role assignment through an existing administrative workflow. The owner still makes a decision; engineers no longer translate it into several implementations. Count the owner's effort and any support needed. A form that makes the owner decipher application internals has merely moved the problem.

Temporary incident access offers another opportunity. If the authorized expiry is part of the assignment and the system enforces it, a recurring cleanup request can disappear. Extensions would require a new decision. The team would need to check what happens when an application caches an old permission or loses contact with the authority; changing a record is insufficient evidence that access ended.

The result could be fewer engineering requests and a smaller class of meaningful exceptions. The factory would handle changes that still need implementation, while ordinary assignments follow the product's established behavior. This is a different investment from making an agent better at editing policy files.

## Look beyond the quiet queue

A policy workflow can appear successful because its mistakes do not interrupt anyone. Granting too much access may produce no complaint. Denying necessary access may send the complaint to support rather than the engineering team.

Observe results outside the workflow's own declaration of success. Exercise independently agreed allowed and denied cases, examine effective permissions after changes, and follow problems reported by users. A successful operation that stores a policy does not establish that every application applies it correctly. Keep changes to the acceptance rules separate from attempts to satisfy them.

Coverage matters too. A low intervention rate says little if the route excludes most requests. Keep the excluded work in the account, including the difficult cases that remain with specialists. Removing a permission later also cannot undo information already disclosed, so recovery should not be treated as a substitute for establishing the boundary before release.

Follow effort wherever it goes. The engineer may receive fewer questions while application owners spend longer understanding requests. Maintaining the shared authority may consume some of the capacity released. The [measurement essay](./measuring-the-capacity-for-change.md) explains how to include these costs alongside useful outcomes and elapsed time.

As ordinary work disappears, the remaining exceptions will become an unusual sample. An engineer may spend her day on difficult cases and feel that nothing has improved. Account for the routine outcomes completed elsewhere, and give her enough uninterrupted time to investigate the harder questions. A collection of five-minute interruptions is a poor working arrangement for decisions that require sustained thought.

## Keep people able to understand the exceptions

The new arrangement also removes ordinary cases through which engineers used to learn the system. A newcomer might meet only a confusing permission inheritance problem without having acquired the model that makes it tractable.

Reading routine approval summaries does not establish understanding. In a [small randomized study of developers learning an unfamiliar Python library](https://www.anthropic.com/research/AI-assistance-coding-skills), Anthropic found lower immediate comprehension scores with AI assistance, without a statistically significant improvement in completion time. That does not establish long-term effects on engineering expertise. It gives us a reason to check learning separately from completion.

Use the policy examples for deliberate practice. Ask an engineer to predict what a person can do after joining two overlapping groups. Then end one assignment while an application still has a cached decision. Let the engineer choose a check and explain what its result establishes. Include a case where the technical behavior is clear but the requested authority has never been granted.

Real exceptions can become supported ownership. An engineer learning the system might investigate the support partner's request, discuss its purpose with the owner and propose a narrower capability. Allocate time for that work. The [apprenticeship essay](./how-engineers-become-engineers.md) explores how responsibility can grow alongside delegation.

Later, the team might use its explicit permissions and examples to assess a replacement authorization service. That would be a new capability to investigate, with new questions about failure and consistency. Record what the earlier work contributes and what still has to be learned.

Start with the last few requests that interrupted an engineer. Follow one back to its cause. On the next request, find out whether the revised arrangement can complete the familiar work, expose the unfamiliar decision and leave the responsible person with enough evidence to make it.
