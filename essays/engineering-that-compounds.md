# Engineering that compounds

*What we choose to carry into the next piece of work*

Return to the fictional export service in [What software should remember](./what-software-should-remember.md). It waits twenty minutes after a partner uploads a file before forwarding the contents. The partner now offers a completion webhook. Customers want their data sooner. Removing the timer looks like a pleasant little ticket.

An agent deletes the delay, updates the tests and produces a tidy diff. Before it can ship, someone asks why the timer existed. The old uploader exposed a placeholder before finishing the file. A test that exports immediately can pass while faithfully demonstrating the bug.

The team sorts this out and ships the change. Now comes a smaller decision, easy to skip: what should remain available when somebody changes this integration again?

They could save the whole conversation, add a stern warning to the agent instructions, or build a framework for simulating every partner. They could also keep one useful test and fix the link that would have led them to the answer sooner. Choosing among those options is where this collection becomes ordinary engineering work.

## Put learning on the route to done

[Every's Compound Engineering guide](https://every.to/guides/compound-engineering) gives learning a regular place in AI-assisted development: plan, work, review, compound. Its final step captures a reusable lesson, makes it findable and asks whether the system would catch the problem next time. That is a useful operating habit; the guide is a practitioner's account, not evidence that every retained lesson pays for itself.

For our export team, the habit has two ends. Before starting, recover what earlier work already established. Before closing, decide whether this task has left something worth passing on. The next use connects them.

That last part matters. A beautifully written note is still an untested investment until someone needs it. An ordinary change that teaches us nothing reusable can finish without a new artifact. The point of the pause is to make a choice while the reason for it is still fresh.

## Find the old reason before writing the new plan

The first useful instruction to the agent is to investigate the delay: find its rationale, the behavior it protects and the uncertainties that changing it would expose. Ask for the sources as well as the explanation. A plausible account of why someone chose twenty minutes is no help if the choice came from a different constraint entirely.

In this example, the integrations owner confirms that the new contract identifies a completed file version that will no longer change. The team also checks the open question in the old record: no downstream consumer requires the twenty-minute gap. Those are facts established for this fictional change, not assumptions the agent can fill in from the webhook's name.

Now the plan can be specific. Export the completed version once. Never export the placeholder. Repeated notifications must not produce repeated exports. Check what happens if a notification is lost or the worker restarts. The implementation still needs design work, but the team has something firmer to review than “replace polling with webhooks.”

If the contract remains unclear, the plan keeps that question open and names who must answer it. A blocked decision is useful information. Turning it into a confident paragraph only moves the blockage into production.

This also gives the team a modest improvement to its next integration plan: when file visibility and file completion are separate events, establish the completion contract before changing the scheduler. One well-placed question may earn its keep sooner than a new planning template.

## Leave something useful when the tests go green

Suppose the awkward part of the investigation was recreating the upload sequence. The team builds a small synthetic replay: a file appears with incomplete contents, the contents are replaced, a completion signal arrives, then that signal arrives again. The expected result comes from the agreed behavior: nothing is exported before completion, and the completed contents are exported once.

The agent can write the fixture and test. Review still has to establish that they represent the problem. In an isolated checkout, temporarily restore the eager “export when visible” behavior and make sure the replay catches the incomplete export. Then run it against the fix. A green check is more informative when you have seen the same check reject the mistake you care about.

That replay covers a particular sequence. Lost notifications and restarts need their own verification; the existence of a convincing fixture does not settle them. Nor does a second agent agreeing with the first establish the partner's contract. The distinction between a claim and its evidence remains useful even when agents do much of the work on both.

What should the team keep? If the replay fits into an existing integration test, put it there. There is no prize for giving a small test its own command-line tool. If recreating the sequence requires several hidden setup steps, a documented local command may be worth keeping too. The [field guide](https://grove.github.io/patterns-of-compounding-engineering/) offers patterns for both choices.

The current decision record should link to the test and the contract it relies on. The old timer record should say that it has been superseded. Where an engineer or agent enters this part of the repository, a short pointer should lead to the current record. Keep the reasoning in one place so future edits have one place to correct it.

The useful residue of the task is quite small: a verified example, a current explanation and a route to them. The debugging transcript can go.

## Give someone else the next turn

Try the handoff before declaring the repository better informed. Ask a teammate who missed the investigation, or an agent in a fresh session, to propose recovery for a missed completion notification. Give them the task and the repository access they would normally have. Leave out the helpful sentence telling them which note contains the answer.

Watch what happens. Do they find the completion contract? Do they notice that the timer record is superseded? Do they identify what recovery needs to establish before forwarding a file? Finding the right page, using it correctly and producing a sound change are three different achievements.

In our example, the first rehearsal goes badly. The service README still recommends waiting twenty minutes. The agent proposes restoring the timer when a notification is missed, without finding the new contract. The team had updated the decision record and left a copied explanation behind.

They replace that paragraph with a link to the current record and try another fresh session. This time the proposal reaches the missing question: how can recovery establish that a file version is complete when the notification never arrived? The integrations owner has something specific to resolve before anyone writes the fallback. The repaired link has helped expose a gap; it has not filled the gap for them.

A fresh agent session is a useful rehearsal, not a substitute for an unfamiliar engineer's judgment. One successful run also says little about reliability across tasks. The stronger evidence arrives during later work: someone uses the replay, catches a mistaken assumption and can show what it helped them decide.

## A return is a beginning

The next integration change may become easier because the replay already exists. That is a recurring return. [Engineering capital](./engineering-capital.md) reserves *compounding* for a further connection: earlier work makes a later investment cheaper or more effective.

Here, the replay might make it practical to build a recovery drill for interrupted exports. The drill could then let the team simplify an old recovery path it was afraid to touch. We have a plausible chain of improvements, with something observable at each step. We do not yet have proof that the chain will continue.

It can run out of usefulness. The partner retires the uploader, but its fixtures remain. Someone adds support for three other protocols. A small replay grows its own configuration language. Soon the team is repairing the test machinery whenever it changes the exporter.

Name a person or team responsible for the retained tool, and name the event that should reopen the decision to keep it. For this replay, a changed completion contract or the retirement of the integration is a better trigger than a ceremonial yearly review. Count the setup problems and repairs alongside the successful uses. When an ordinary test would now do the job, shrink the tool.

Skipping an investment can be the right decision at the start, too. A one-off migration still needs careful verification; it may need no reusable framework. A service being retired next month is a poor home for a new testing platform. An urgent restoration can finish before its reusable lesson is ready, with a small follow-up only if somebody expects to use it. “Nothing worth retaining” is an acceptable result of the pause.

## What if the next change needed no ticket?

The team has made an integration change easier to understand and verify. Now look at the work that still needs a person. Suppose every missed completion notification opens a support ticket. Somebody finds the affected file, establishes whether it is complete, and decides whether to retry. If that procedure becomes well understood, the team can try running the recovery check when the notification is overdue. It still needs a sound way to distinguish a completed file from a partially written one; where that evidence is missing, the case belongs with an engineer.

Our distant aim is to become [ten times as effective with AI](./what-would-ten-times-look-like.md). Take a recurring outcome and ask what would need to be true for it to require a tenth of the effort. That will often point outside the code change itself. Could the failure be prevented? Could the evidence be gathered automatically? Would a simpler contract remove the manual recovery procedure altogether? If most of the effort lies in agreeing with a partner about what complete means, another agent writing retry code will not help much.

Try to establish the current cost before making the investment, and include the people who do the work after the code ships. Work on the part that accounts for the most avoidable effort. As it improves, look for the next constraint. The [automation essay](./automating-the-work-of-engineering.md) follows that idea through dependency maintenance, including a hypothetical tenfold reduction in effort for a narrowly defined class of work.

## What a repository cannot carry for us

The export example works because several kinds of effort support one another. The old rationale preserves a question. Someone with domain knowledge answers it. A test makes part of the answer executable. A colleague learns enough to challenge it later.

Recording the answer does not remove the need for that colleague. [How engineers become engineers](./how-engineers-become-engineers.md) argues for building judgment deliberately: make a prediction, inspect the evidence and explain a surprise. A replay can support that practice. Used as a green light nobody understands, it cannot.

Nor can a repository settle who pays for shared work. If one team maintains the replay while three others benefit, the arrangement needs to be visible, as [Organizations that improve with age](./organizations-that-improve-with-age.md) discusses. Otherwise the team carrying the cost has a reasonable incentive to stop.

These questions remain whether AI makes implementation a little cheaper or dramatically cheaper. More capable agents may do more investigation and verification. We will still need to decide which commitments to make, what evidence is enough and who owns the consequences. Keeping those responsibilities explicit is more useful than prescribing a permanent boundary between human and machine work.

## Try it on the next awkward ticket

There is no need to launch a new engineering programme. Choose a kind of work you expect to encounter again soon. Before starting, look for the previous decision or experiment. While working, preserve the evidence that resolves the difficult part. At review, ask what would save the next person from repeating the investigation, and whether keeping it costs less than rediscovering it.

Then put the smallest useful answer where that person will meet it. If it adds upkeep, give that upkeep an owner and a limit. On the next use, ask where it helped, where it misled and what still needed explaining. Those answers belong in the next revision of the tool or note, not in a separate report nobody needs.

For a team trial, follow one recurring class of change over a quarter. Record ordinary uses, including the awkward ones, and count review, setup and repairs. [Measuring the capacity for change](./measuring-the-capacity-for-change.md) explains how to make that judgment without mistaking a pleasing story for a measured improvement. A useful trial can end with a decision to delete something.

The export team has shipped a faster integration. The next engineer can now find out why it works, make it fail on purpose and test a different approach. That is enough to try on one ticket. The next ticket will tell them what to improve.
