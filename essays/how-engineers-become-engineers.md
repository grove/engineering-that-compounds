# How engineers become engineers

*An apprenticeship with less implementation*

Consider an engineer in the first months of a new job, asked to add retries to a background worker. An agent produces a reasonable patch, including tests. The engineer follows the explanation, responds to a few review comments and gets it merged.

The task is complete. What has the engineer learned?

Perhaps quite a lot. They may have investigated what happens if the worker completes an operation and loses the connection before receiving an acknowledgment. They may now understand why retrying an operation can repeat its effect, and where the system prevents that repetition.

Or they may have learned how to recognize an explanation that sounds satisfactory. The repository looks much the same in either case.

The earlier essay [Implementation and understanding](https://grove.github.io/software-that-improves-with-age/essays/implementation-and-understanding.html) considered the understanding established engineers can lose when they delegate implementation. There is a longer question underneath it: how will someone acquire the judgment that makes delegation effective in the first place?

## What an apprenticeship used to include

Writing software gives an engineer repeated contact with the consequences of their own decisions. An apparently simple change reaches an unexpected dependency. A test that seemed sufficient misses a failure. An elegant abstraction becomes awkward under the next requirement.

The educational value lies partly in having made a prediction before finding out what happens. Someone else's explanation of the difficulty is easier to accept than our own failed attempt, but it may leave a less precise understanding of where the difficulty came from.

This was never a reliable curriculum. An engineer could spend years implementing routine features and rarely investigate a serious concurrency problem. Another could learn a great deal through a demanding project with generous colleagues. Much depended on which work happened to be available and who had time to explain it.

We should be reluctant to preserve all the inconvenience of that arrangement. A packaging problem can consume an afternoon without helping someone understand the system they are learning. Equally, removing every occasion on which a beginner must reason through an unfamiliar mechanism can leave them dependent on explanations they cannot assess.

The useful question is which parts of an assignment require the learner's attention, and which parts can be delegated without losing its educational purpose.

## Choose the judgment to practice

In their [1993 account of deliberate practice](https://doi.org/10.1037/0033-295X.100.3.363), Anders Ericsson, Ralf Krampe and Clemens Tesch-Römer distinguished activities designed to improve performance from ordinary participation in a domain. They emphasized appropriately chosen tasks and informative feedback. Their work is not evidence that a particular training scheme will produce expert software engineers; it gives us a useful distinction when designing one.

For the retry assignment, the learning goal might be to recognize the gap between an operation taking effect and its caller knowing that it took effect. That is specific enough to investigate. “Learn distributed systems” is not.

A mentor can give the engineer a small worker and a service that records completed operations. Before running anything, the engineer predicts what each side will know if the connection disappears at different points. An agent can help prepare the failure injection and collect the results. The engineer has to explain where the prediction failed.

The exercise should then change. Perhaps the operation now sends a message to another service. Perhaps the record used to detect duplicates expires. The engineer needs to work out which part of the previous argument still applies. Repeating the identical case until its answer is familiar would tell us much less.

The exercise earns its place if the engineer can reason more effectively about later work, including cases the mentor did not rehearse. A satisfying session followed by the same confusion a month later would be a reason to change how we teach it.

## Let the mentor's uncertainty be visible

An experienced engineer can make investigation look deceptively direct. They ignore several plausible explanations, inspect one counter and locate the problem. The beginner sees the command that worked without seeing why it was worth trying.

The idea of [cognitive apprenticeship, described by Allan Collins, John Seely Brown and Ann Holum](https://www.aft.org/ae/winter1991/collins_brown_holum), is useful here. Their account brings normally hidden thinking into the teaching process, with guidance gradually withdrawn as the learner takes responsibility. Applying that educational approach to an engineering team means making room for an experienced colleague's explanation while the work is still unresolved.

A mentor investigating the worker might explain why a rising retry count suggests several possibilities, what observation would separate them and which tempting investigation they are postponing. That gives the learner access to choices that a finished incident report tends to smooth away.

The mentor should also say when they do not know. If every exercise ends with the senior engineer revealing the answer they possessed all along, the beginner learns an unrealistic picture of expertise. Much engineering judgment consists of finding a way to proceed when nobody has an answer yet.

An agent's explanation can help, but it needs a different status. A fluent account of why a patch works is a claim to examine. It is not a record of the learner's reasoning, and it may not accurately describe how the result was obtained. Asking a learner to repeat it proves little.

One useful habit is to have the learner explain their current model before asking the agent for an explanation. The comparison then has something to work against.

## Assistance that changes over time

At the beginning, a learner may need a working example, a suggested hypothesis and help interpreting the result. With more experience, the same help can remove the very work they need to practice.

The retry exercise might begin with a mentor choosing the failure points. Later, the engineer chooses them and explains why. On another assignment, they decide whether retries are appropriate at all. Eventually they help someone else distinguish a safe retry from a repeated business action.

An agent can remain useful throughout that progression. It can generate test data, locate relevant code, suggest competing explanations or write the mechanical parts of an experiment. What changes is who chooses the question and who is responsible for deciding what the evidence establishes.

There is no reason to insist on a universal rule such as “beginners must code without AI for six months.” Some manual work is valuable because it exposes a mechanism clearly. Some is repetitive transcription. A learner implementing a tiny queue by hand may gain something that would be hidden by a large framework; implementing another routine HTTP client may add very little.

The choice should follow the skill being developed. If the aim is to understand ownership and lifetime, working directly with those details is reasonable. If the aim is to compare failure behavior across designs, having an agent prepare several implementations can create a better exercise than spending the available time finishing one.

## Remembering is part of reasoning

It is tempting to assume that ready access to explanations makes retained knowledge less important. We can always ask again.

In practice, deciding what to ask depends on what we already know. An engineer who has encountered an ambiguous acknowledgment may recognize the same problem hidden inside a payment callback or a job scheduler. An engineer who has only followed a particular patch may not know that there is a question to investigate.

Henry Roediger and Jeffrey Karpicke's [experiments on test-enhanced learning](https://doi.org/10.1111/j.1467-9280.2006.01693.x) found benefits to delayed retention when students retrieved material rather than only studying it again. The tasks concerned prose passages, not engineering judgment. They offer a reason to include recall in a learning routine, without claiming that recalling a protocol amounts to mastering its use.

A few days after the retry exercise, the learner can reconstruct the failure sequence without the report open. A few weeks later, they can investigate a different system with a related problem. Where their account breaks down tells the mentor what needs another pass.

These activities need not become examinations. A team can use them in ordinary design discussions: ask each person to sketch what they expect before opening the implementation, then compare. A wrong prediction is useful evidence when admitting it carries no penalty.

## Give learners something real to own

Exercises have limits. They usually come with a bounded problem, a sympathetic mentor and an expectation that a solution exists. Production work contains uncertain requirements, interruptions and consequences that continue after the patch is merged.

An apprenticeship needs a path into that responsibility. The learner might begin by owning the retry behavior of one noncritical worker, with an experienced engineer available for decisions that exceed the agreed scope. They follow it through rollout, examine its behavior and respond when an assumption proves wrong.

Ownership should grow as their judgment becomes more dependable. That is different from leaving a junior engineer alone with a difficult service and calling the resulting stress a learning opportunity. Support needs to be available at the moments when the learner cannot yet judge the risk unaided.

The work also has to include contact with users and operators. Someone can become skilled at diagnosing a retry loop while missing that the operation should never have been automatic. Engineering expertise includes recognizing when a technical difficulty is evidence of a poorly understood requirement.

Agents may make it easier to give learners bounded work with real consequences. They may also make it easier for experienced staff to do everything themselves. The latter can look efficient for a long time, right up to the point when the organization needs more experienced staff.

## Who pays for the next generation?

Mentoring consumes time. A senior engineer explaining an investigation could have finished it faster alone. A beginner making predictions and checking them will sometimes deliver less this week than a beginner accepting generated solutions.

If a team measures only immediate output, the learning will tend to disappear. The remedy requires an explicit organizational choice about which assignments are also investments in people. It cannot depend on mentors quietly adding the work to their evenings.

There are useful signs that the investment is working. The learner begins to ask questions the mentor missed. They can explain what would change their mind. They recognize when an earlier lesson does not apply. They seek help before an uncertain decision becomes a costly commitment.

None of those signs requires them to reproduce their mentor's career or write the same amount of code. They do require repeated opportunities to make judgments, encounter consequences and revise their understanding.

The retry patch may take an agent only minutes. The apprenticeship surrounding it deserves more time than that. Years later, when the engineer is responsible for a system whose failure modes nobody fully understands, the organization will be relying on what they learned while the patch was being made.
