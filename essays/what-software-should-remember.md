# What software should remember

*Keeping reasons available, and open to revision*

Consider an export job with a twenty-minute delay. The code explains how the delay works. Its tests make sure the job waits. A comment says the delay is necessary because a partner sometimes revises files after uploading them.

Suppose the partner now provides an explicit signal that an upload is complete. Can the delay go?

The answer depends on things the code does not tell us. Did the partner guarantee that signal, or did somebody merely observe it? Were revisions the only reason for waiting? Does another process rely on the gap? Was twenty minutes measured, negotiated or chosen because it seemed generous?

A capable agent can trace the implementation and find its callers. It cannot reconstruct evidence that was never recorded. It may produce a persuasive explanation of the delay while getting its original purpose wrong.

This is the problem I want engineering memory to address. A future maintainer needs enough of the past to judge what can change now.

## Reasons that survive the decision

Michael Nygard's [proposal for architecture decision records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) offers a practical starting point. A short record preserves the context, decision, status and consequences. When a decision changes, its predecessor remains available but is marked as superseded. A reader can distinguish an old choice from the one currently in force.

That distinction is easily lost in ordinary documentation. A page describing the export job might have been correct when written. Five edits later, it may combine the original explanation with current implementation details and an untested suggestion. Nothing looks obviously false, but the reader cannot tell which statements still have evidence behind them.

The useful record for the delay would be short. It would explain the failure being avoided, identify the partner behavior on which the decision depended, and link to whatever established that behavior. It would say whether other remedies were considered. It would also say what would justify revisiting the decision: a reliable completion signal, a changed export protocol, or evidence that the wait no longer prevents the problem.

Reconsideration conditions matter because they connect memory to future work. Without them, a decision record can become a polite instruction to leave things alone. With them, a maintainer has a reason to investigate a changed circumstance.

We cannot anticipate every circumstance that might make a decision obsolete. Even an incomplete account of its dependencies is useful. “This assumes uploads can change after they first become visible” tells us more than “required for reliability.”

## An observation is not a promise

Imagine finding three statements in the export documentation. The partner says a completed upload will never be revised. A month's logs contain no revisions after completion. The current implementation ignores any revisions it receives.

These statements concern the same behavior, but they support different conclusions. The first describes an external promise whose precise scope we should check. The second describes an observation within a limited period. The third describes our own choice. Combining them into “completed uploads never change” discards distinctions a future engineer may need.

An agent asked to summarize the documentation could make exactly that compression. So could a busy human. A smooth explanation is often easier to read than a pile of qualified claims, which makes the loss difficult to notice.

The [W3C's work on provenance](https://www.w3.org/TR/prov-overview/) provides a useful vocabulary here. It concerns the entities, activities and people involved in producing information, so that readers can assess where a claim came from. A small engineering project need not adopt the full machinery. It can retain the underlying discipline: link a conclusion to the evidence and the process that produced it.

For an experiment, that may mean a commit, a workload and the environment in which it ran. For a business rule, it may mean the person responsible for the process and the document that describes it. For an inference, it means saying that it is an inference and identifying what remains uncertain.

None of this makes a claim true. It makes the claim inspectable. A confident statement without an origin is harder to challenge than an imperfect observation whose limits are visible.

## Put knowledge where a question arises

A well-written explanation has little value if nobody encounters it. Keeping every decision in a central repository makes storage orderly, but does not ensure that an engineer working on the export job will know which record matters.

The connection should work in both directions. The delay can point to its decision record. The record can identify the code and checks through which the decision is enforced. A test of the partner protocol can link to the assumption it examines. When the test fails, the maintainer can discover why the behavior mattered before deciding how to repair it.

This is more useful than copying the entire explanation into every file. Copies drift independently. A small number of well-placed references can preserve the path to the reasoning while leaving one place to update it.

Some knowledge belongs in executable form. If repeated processing of the same completed upload must produce the same result, a test can exercise that requirement across repeated deliveries and worker restarts. The test is easier to trust when its expected result comes from the contract we intend to provide, rather than from the implementation it tests.

Other knowledge resists that treatment. A test cannot decide whether the partner's promise is commercially credible. Nor can it tell us whether delaying every export is an acceptable inconvenience to customers. Turning a judgment into a constant does not remove the judgment. It makes the reason for choosing the constant worth keeping.

The [value of an abandoned experiment](./the-value-of-forgotten-alternatives.md) follows the same rule. Preserve the path from a question to the evidence that changed our answer. Keeping all the experimental code is optional; keeping a useful way to inspect the conclusion may be essential.

## Memory needs maintenance

It would be convenient if we could attach an expiry date to every claim and have an agent renew it automatically. Some checks are suitable for that. A command can confirm that a linked file still exists, a reproduction still runs, or a stated schema still matches the deployed version.

The harder claims do not become current merely because somebody has recently read them. A record can have a fresh review date and an obsolete premise. An agent that compares the record with the code may certify both even though the real change happened in the partner's operating procedure.

Review is most useful when something relevant changes. The export protocol gains a completion signal. A different team starts consuming the same files. A customer needs results within five minutes. Each event gives us a concrete reason to reopen the delay decision and check its dependencies.

There will still be disagreements. One record may say revisions are impossible; an incident may contain an example of one. A maintenance process should surface that conflict. Quietly rewriting the old explanation to match the latest account makes the repository easier to read while destroying the clue that something needs investigation.

For consequential knowledge, keep the earlier claim, mark its status and point to the evidence that challenged it. The current explanation can remain concise. Its history should be available to anyone who needs to understand the change.

This is also a limit on automated memory updates. An agent can propose that a claim is contradicted or likely obsolete. Deciding whether an external guarantee still applies may require someone with authority over the relationship, and sometimes a conversation outside the engineering team.

## The cost of remembering everything

Recording every prompt, tentative explanation and failed command would preserve plenty of history. It would also bury the few things a future maintainer needs under the details of how somebody happened to work.

Most intermediate material deserves a short life. The useful residue of an investigation is usually much smaller: the question, the evidence that mattered, the conclusion and its limits. If a particular failed command revealed an important environmental dependency, keep that fact. There is rarely a need to keep every unsuccessful invocation around it.

Some evidence is expensive or inappropriate to retain in its original form. Production traces may contain customer information. An investigation may depend on a large dataset that cannot be kept indefinitely. A small synthetic reproduction can preserve the relevant behavior, provided its author checks that the reduction has not removed the feature responsible for the result.

We also need to distinguish historical preservation from current guidance. An obsolete decision can remain in an archive without appearing in every answer about how to change the export job. Search and retrieval should show its status. Agents consuming repository knowledge need that context as much as people do.

Forgetting can be a useful act of maintenance. A duplicated explanation can be deleted. An unsupported rule can be replaced with an explicit question. A record that no longer affects any current decision may need only a brief historical note. These choices reduce the chance that old material will be mistaken for a present obligation.

## A test of the memory

A practical review requires no elaborate knowledge platform. Give the export job to an engineer who did not build it and ask whether the twenty-minute delay can be removed. Watch what they need to discover.

If they can identify the original problem, find the relevant promise and run a check that bears on it, the project has preserved something useful. If they can only explain the current code, the important gap remains. If they accept the delay because three documents repeat the same unsupported claim, the memory is actively misleading them.

The engineer does not have to agree with the original decision. They should be able to understand why it was reasonable, identify what has changed, and make a new decision without reconstructing the entire investigation.

That is what I would like an old system to remember. Enough to help its next maintainer ask a better question, and enough uncertainty to let them change the answer.
