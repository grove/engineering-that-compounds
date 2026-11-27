# Engineering that compounds

*What we choose to carry into the next piece of work*

Consider a team maintaining a service that imports large files from customers. Every few weeks, an unusual file gets stuck. An engineer downloads a sanitized copy, reconstructs the relevant settings, runs the importer locally and eventually finds the cause. The patch is usually small. Getting into a position to write it takes much longer.

After one particularly awkward investigation, the team keeps the reproduction environment. A second engineer makes it possible to replay an import without contacting external services. Later, somebody adds a check that accounts for every accepted and rejected record, so a run that finishes without crashing can still be examined for missing data.

These changes have an immediate benefit: the next incident is easier to investigate. There is also a possibility of a further return. The replay environment could make an unfamiliar design affordable to test. The record checks could give the team enough confidence to simplify the importer. An engineer learning the system could use the same tools to challenge an explanation instead of accepting it on trust.

That further return is the proposition running through this collection. Engineering can leave us with means of doing better work, and some of those means can improve how we acquire the next ones. Whether this happens often enough to justify the expense is a question we should investigate.

## A return has to reach the next decision

The distinction between accumulating assets and compounding their benefits is easy to lose.

A replay environment that saves an afternoon on every incident is useful even if its benefit never grows. It has produced a recurring return. Calling that return compounding adds little unless we can describe what happens to the saved effort or newly available capability.

Suppose the team uses the replay environment to compare two ways of handling malformed records. The comparison reveals that several recovery branches exist to preserve a behavior customers no longer need. With product agreement and suitable checks, those branches can be removed. The simpler importer is easier to model, which makes it cheaper to build an experiment for a different class of failure. A later investigation now starts with both better tools and less unnecessary machinery.

That is a plausible mechanism for compounding: one investment improves the conditions under which another useful investment is made. It is more specific than a rising count of tests or an expanding documentation directory.

The mechanism can fail at each step. The saved afternoon may go entirely to another urgent feature. Product experts may be unavailable. The replay tool may simulate the wrong behavior. The proposed simplification may move complexity into customer support. There is no automatic conversion from an efficient investigation into greater engineering capability.

We should be able to point to the decision made possible by an earlier investment, and then to evidence that the decision helped. Without that connection, compounding is a hopeful description of activity.

## Reinvestment competes with real needs

James March's [Exploration and Exploitation in Organizational Learning](https://pubsonline.informs.org/doi/abs/10.1287/orsc.2.1.71) examines how organizations divide effort between developing new possibilities and making use of what they already know. His models show why adaptive processes can favor near-term effectiveness while undermining longer-term adaptation. They do not supply a budget percentage for engineering teams, but they identify the tension behind it.

For the import service, shipping the next requested format is a legitimate use of time saved by the replay environment. Customers may need it now. An investment programme that treats every immediate request as a distraction will soon lose the support of the people it is supposed to serve.

The team needs an explicit decision about how much effort to spend improving its future work. A small recurring allowance can make experiments possible without requiring every one to win an argument against the entire product backlog. The allowance should still be reviewed. Otherwise, a sensible protection against short-term pressure becomes an entitlement to build machinery nobody needs.

The right scale depends on the expected life of the system, the frequency of relevant changes and the consequences of mistakes. A service with years of likely operation and recurring import failures offers a different case from a script that will be discarded after one migration. The script may deserve careful verification while needing almost no durable support infrastructure.

There is also a timing problem. An organization close to running out of money may be unable to wait for a sound investment to repay itself. Calling the expenditure engineering capital does not make that constraint disappear. The language is useful only if it helps make the tradeoff clearer.

## Some assets work better together

The record checker is valuable because the team has agreed what a completed import means. The replay environment is valuable because engineers can interpret its output. A short explanation of an old workaround is valuable because someone has a safe way to test whether its justification still holds.

These relationships matter more than a comprehensive inventory of capital. A team can possess excellent tools and still lack authority to act on their findings. It can understand its domain deeply while lacking any inexpensive way to test a change. Investing in what is already strong may deliver less than repairing the missing connection.

In the import example, generating more test files might be easy. The scarce resource could be a product expert who can decide whether rejecting a malformed row is acceptable. Until that decision is made, additional tests may simply preserve conflicting guesses more thoroughly.

AI assistance could make some supporting work cheaper: constructing a replay fixture, tracing an unfamiliar path or drafting an experiment. That would change which investigations are affordable. It would not determine what counts as a correct import, and it would not remove the cost of checking an agent's proposed answer.

The practical starting point is to look at where a recent piece of engineering became unnecessarily difficult. Ask what would have changed that experience, and whether the same improvement would help work that is likely to recur. A small instrument attached to a real decision has a better chance of being used than a general platform built in anticipation of every future need.

## Experience can become executable

There are established examples of projects preserving substantial engineering knowledge in their verification machinery. SQLite's account of [how it is tested](https://www.sqlite.org/testing.html) describes independently maintained harnesses, fault testing and checks for malformed inputs, among other techniques. It is a concrete example of experience preserved in working tools, although its costs and benefits cannot be assumed to carry over to a smaller project.

The import team can apply the underlying idea at a smaller scale. A difficult customer file becomes a maintained regression case with an explanation of the relevant property. The team may also preserve the experiment that exposed a mistaken theory, so future investigators know which explanation was ruled out and under what conditions.

Some knowledge should remain outside executable checks. A test can establish that a file produces a particular result; it cannot by itself explain why a customer needs that result. People also acquire judgment through deciding what to investigate and interpreting unexpected outcomes. Automating the mechanical steps while leaving new engineers only the task of accepting a verdict would consume part of the capability the team hopes to build.

This is why [developing engineers](./how-engineers-become-engineers.md) belongs in the same discussion as improving tools. The replay environment can be an instrument for learning if engineers use it to make predictions and inspect discrepancies. Its educational value depends on how work is organized around it.

## The machinery can turn against us

After several years, the replay environment may have become a second implementation of the importer. It may contain elaborate adapters for services that were retired long ago. Its fixtures may encode customer practices that have changed. New engineers may spend more time satisfying the tool than understanding the production system.

The team has accumulated an obligation. Continuing to call it an asset does not improve it.

Every retained instrument needs a plausible user and a reason to trust its current output. If a simpler check now answers the same question, replace it. If the relevant behavior has disappeared, retire the check with enough history to explain the decision. Preserving everything makes earlier investments compete with later work for attention.

There are limits even when the machinery remains useful. The easiest recurring problems may already have been removed. Further improvement may require expensive work for a small benefit. A new business direction can make years of domain expertise less relevant. An organization can become so practiced at its current approach that it struggles to recognize a better one.

Compounding should therefore describe an observed relationship over a period and within a domain. It should not imply indefinite exponential growth. The service can become easier to change in useful ways while the organization faces entirely new difficulties elsewhere.

## Choose one next investment

For a team interested in trying this, I would start with an investigation it already expects to do again. Preserve one useful result in a form another engineer can use. State the later decision it should help, set a limit on maintenance effort and arrange a review after that decision arrives.

In the import service, that might mean keeping the replay environment for the next format change. Ask someone who did not build it to use it. Record the setup work and confusion as well as the time it saves. If it helps, decide what small improvement would make the next investigation more informative. If it does not, repair or discard it before expanding the scheme.

The evaluation will be imperfect. As [Measuring the capacity for change](./measuring-the-capacity-for-change.md) argues, the alternative history is unavailable and later tasks differ. We can still ask whether an investment was used, what decision it changed and what it cost to keep useful.

The original collection asked whether a software system could benefit from its age. This one extends that question to the people and arrangements through which the system is understood and changed. Both depend on decisions made during ordinary work: what to investigate, what to retain, who gets to learn from it and when to let it go.

When the next troublesome file arrives, the new engineer should be able to do something the team could not do before. Perhaps she can reproduce the failure in minutes, establish that no records were lost, or test a repair without asking the original author to reconstruct the system from memory. That is a return worth recognizing. Whether it helps her leave an even better starting point for the next engineer is the claim we still have to earn.
