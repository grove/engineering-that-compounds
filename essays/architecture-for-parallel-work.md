# Architecture for parallel work

*How much work can we do at once before it becomes more work?*

Picture three developers, human or otherwise, making changes to a billing service. One is adding a discount. One is updating the invoice export. One is replacing a payment library. Each has a branch and a passing test suite. The first two merge. The third spends the afternoon undoing its own assumptions about invoice totals.

All three tasks looked independent on the board. In the code, the export and payment adapter had quietly come to depend on the same calculation. Each branch tested a world that no longer existed by the time it merged.

[Every's Compound Engineering guide](https://every.to/guides/compound-engineering) makes extensive use of concurrent research and review, and of isolated working copies during implementation. More work can be attempted at once. Whether it can be finished at once depends on the software and the decisions people are making about it.

## Start by splitting questions

Before asking three agents to write three patches, try giving them three questions.

In our fictional billing service, an engineer is considering a change to the pricing model. One investigation traces the finance team's requirements for historical invoices. Another runs the current calculator against a shared set of awkward scenarios. A third sketches a simpler alternative and identifies what would need to be different. Each returns evidence and uncertainties. None has permission to redefine the invoice contract.

The three investigations can proceed without merging a line of code. A person still has to reconcile the answers. Perhaps the scenarios contradict the finance team's description. That contradiction is the most valuable thing the parallel work produced.

The [Competing prototypes](https://grove.github.io/patterns-of-compounding-engineering/patterns/competing-prototypes.html) pattern makes this useful for a design decision: separate experiments, the same question and reviewed expectations, and one explicit choice. Independent attempts are especially helpful if they start with different approaches and preserve failures rather than negotiating a shared explanation too early. Agents that share a model, prompt or mistaken assumption can still agree on the wrong answer.

## A worktree does not give you a contract

Git worktrees are excellent for keeping local files apart. They do not keep two engineers from independently changing the meaning of a field.

Imagine the discount developer decides that an invoice line includes tax. Meanwhile, the export developer assumes it excludes tax. Neither edits the other's code. There may not even be a merge conflict. The integrated software is wrong.

A useful boundary has more than a directory around it. It has a responsibility people recognize, an interface with clear meaning, and a way to verify what can cross it. A calculator that accepts a well-defined invoice state and returns amounts with an explanation gives the export developer something to work against. Reviewed examples that cross the boundary can reveal disagreements before the whole system is assembled.

Stable contracts should not mean permanent contracts. If the right fix is to change the meaning of the invoice line, that change needs to be a shared decision and a coordinated migration. Freezing a bad interface to make agent throughput look better is a costly victory.

The earlier collection, [Software that improves with age](https://grove.github.io/software-that-improves-with-age/), develops the value of module boundaries and independent verification. Parallel work gives us one more reason to care about those qualities. It also gives us a way to discover where they are missing.

## Independence has an operational side

Separate files are not enough if both branches run against the same test database. The first developer clears the tables while the second is checking a migration. Both receive surprising output and spend an hour investigating bugs that belong to neither implementation.

A local verification procedure needs its own state, predictable inputs and cleanup. Where a shared external service is unavoidable, the work needs separate accounts or a coordinated access policy. Credentials must constrain what the work can do. A separate worktree is not a security boundary.

And every candidate needs to meet again on a common base. Run the relevant checks after integrating, including cross-boundary behavior that the isolated tests cannot observe. A feature can satisfy its local contract while the whole system violates a business invariant. The person responsible for the change needs evidence of the latter, too.

## Follow the waiting

Consider a team that can launch ten independent investigations in a minute but can review only two carefully in an afternoon. Adding an eleventh investigator is unlikely to help. It creates another result waiting for attention.

Parallel work has costs: comparing answers, resolving disagreements, maintaining isolated environments and integrating changes. Those costs may be small or may be the most expensive part of the task. Count elapsed time to an accepted result, reviewer attention, failed integrations and rework. The number of agents launched is not a measure of useful work.

Try a modest experiment on the next design question. Let two people or agents investigate independently, with the same evidence standard and a timebox. Merge their findings into a single decision, including what remains unknown. Compare that effort with the last similar investigation, without pretending the tasks were identical.

If separate investigations are useful, try two bounded implementation changes with explicit interfaces, isolated environments and an integration check. When they collide, inspect the reason. It may be a missing example of the contract, shared setup or a genuinely coupled decision. The first two may be worth fixing; the third might simply be work that belongs together.

## Keep what makes the next change independent

The payoff from an experiment like this might be a simpler way to start a local service or one test that establishes what an invoice line means. It might be a decision to keep two tasks together until a shared migration is complete.

Over time, improvements to verification, boundaries and the development environment can reinforce each other. A reliable local setup makes it cheap to explore a boundary. The new boundary makes it practical to write a focused integration check. That check enables a later change to proceed independently. This is a plausible path to compounding, not a guarantee that parallel development will pay off.

The [ability to delegate](./the-ability-to-delegate.md) belongs to a particular class of work. So does the ability to run it concurrently. A mature engineering organization knows which decisions it can separate, which must be made together, and how to tell the difference before the merge queue fills up.

The next essay, [Automating the work of engineering](./automating-the-work-of-engineering.md), asks which of those independent tasks need someone to start them in the first place.
