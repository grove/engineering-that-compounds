# Automating the work of engineering

*How much of this work needs an engineer to be there when it happens?*

Suppose a team looks after thirty small services. Every week there are dependency updates. Someone checks which versions have changed, reads release notes, updates a lockfile, runs the relevant tests and asks a colleague to look at the result. Most of the updates are uneventful. A few are quite important.

With an agent, the engineer can get through the list more quickly. She still has to remember to start, explain what may be updated, decide which checks to run and return to each result. On a busy week, the list waits.

What would it take for her to hear about the important updates and leave the others to a program?

## Give the work somewhere to happen

Start with a narrow case. Our hypothetical team has a service whose patch updates can usually be made without changing application code. It already has a command that prepares a clean test environment and a suite that checks the behavior it depends on. Before asking an agent to manage anything, the team runs that command on the last few updates and finds out where it still relies on someone knowing what to do.

One problem is easy to fix. The test command expects a local database that somebody must have started earlier. Give it an isolated database and a cleanup step. Another is less mechanical: the service relies on a particular library's interpretation of a timestamp, but nothing in its tests says so. Agree on the expected behavior and keep examples of the awkward dates.

Now a scheduled job can look for an eligible update, prepare a branch and run the checks. The job records which versions it considered, why it chose one, and which evidence it obtained. At first, an engineer reviews every result. The job needs no credentials to deploy software or modify the rules under which it runs.

After reviewing enough representative attempts, the team might allow some changes to merge under a narrow policy. The candidate must be based on the current target branch. Independent checks must pass on the exact candidate, the changed files and dependencies must be within scope, and the normal release checks still apply. A failure to obtain evidence leaves the change unmerged. Changes to the policy, verification code or permissions require separate authorization. Someone owns the job, can suspend it and knows how to recover from a bad release.

A patch version is no guarantee of compatibility or safety. Perhaps the team finds that a library's versioning conventions are unreliable. It can take that library out of the policy rather than make the job increasingly clever at guessing.

Notice where AI is useful here. An agent could investigate an unfamiliar test failure or propose an additional check. Comparing versions, scheduling runs and enforcing permissions are generally better jobs for ordinary programs. A useful automation may contain no model calls at all.

## Look for the work around the work

The important change is not the time it takes to edit a lockfile. Suppose a week brings twenty routine updates and two that fail for unfamiliar reasons. Instead of starting and coordinating twenty-two procedures, an engineer could spend her time on the two that reveal a compatibility question.

This is worth looking for elsewhere. A recurring request to investigate a failed import might lead to a diagnostic command that runs when an import fails. A check that people run before every merge probably belongs in CI. A report that nobody uses might be cheaper to stop producing. Do not automate a handoff whose only purpose is to compensate for a bad interface.

AI can make small, awkward tools economical to build where they previously were not. That depends on whether someone can establish that they do the right thing and keep them useful. Code that was cheap to generate can be expensive to own. Start with the work that occurs often enough to justify the experiment, and see how much of the surrounding effort the tool actually removes.

## What would a tenth of the effort look like?

The [tenfold ambition](./what-would-ten-times-look-like.md) becomes a concrete design question when we apply it to one class of work. If a hundred comparable outcomes require a thousand hours of engineering time today, what would have to change for them to require a hundred? Saving half the time spent writing code will not be enough if implementation accounts for only a fifth of the total effort. Even removing implementation effort entirely leaves eight hundred hours.

In the dependency example, imagine that over a quarter one hundred eligible updates consume a hundred hours in discovery, preparation, review and follow-up. A possible budget for the same work is four hours for exceptions and rework, two for routine oversight, two for maintenance and two for a share of the initial investment. That is ten hours. These are target numbers, not results. They give the team something to investigate: can most updates actually meet the acceptance standard without review, and can the job be built and maintained within that budget? Include unsuccessful attempts and any work displaced onto other people in the time budget; count compute costs separately. Count the updates that should have happened but did not, too.

If the job achieves that target and updates were only five percent of the team's work, the team has recovered 4.5 percent of its original time. A large improvement in a small activity is still worth having, but it says little about the team's overall capacity. Look again at where its time goes. It may be waiting for product decisions, chasing down failures or coordinating changes across services. Work on the constraint that actually matters, rather than finding more jobs for the dependency agent.

## Let the exceptions improve the job

The timestamp test helps on the next update. That is a recurring return. Something more interesting happens when the team starts planning a runtime upgrade. It can use the same isolated environment, dependency inventory, timestamp cases and candidate checks to build a different workflow. What would that workflow have cost without the first investment?

The team can also learn from the job's own history. Three updates stopped because a failure message did not identify the offending dependency. An engineer investigates and improves the diagnostic command. The next time a test fails, the job can collect the relevant evidence without someone opening a terminal. That command may be useful outside dependency maintenance.

An agent could prepare such improvements from recorded failures, on a separate branch. It must not be able to silence the check it failed, widen its own permissions or redefine an acceptable result. Review improvements to the machinery against cases that include failures and cases where the job must stop. Some exceptions belong with an engineer permanently: a change in the meaning of a business rule is a decision, not a defect in the workflow.

Repeated failures are worth investigating before codifying a remedy. A missing dependency name might come from a weak diagnostic, a broken environment or an update the job should never have attempted. Ask for the evidence that separates those explanations. [Compounding learning](./compounding-learning.md) follows that investigation through to later use, including the cost of suggestions that send the team in the wrong direction.

This is one practical way to pursue the argument in [Engineering capital](./engineering-capital.md). Give the time recovered by automation somewhere useful to go. Use part of it to investigate the next expensive problem, and find out whether the tools already in place make the new investment easier. [Measuring the capacity for change](./measuring-the-capacity-for-change.md) describes how to distinguish that claim from ordinary reuse.

Pick one procedure you have done several times recently. Before building anything, write down what it takes to finish, including the work you do after the apparently successful result. Ask what a program would need to know to start it on its own, what evidence would let it finish, and which decision would bring it back to you. Try that on one safe class of work. The next time the job comes round, see whether it really needs you.
