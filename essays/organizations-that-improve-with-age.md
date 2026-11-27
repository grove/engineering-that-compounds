# Organizations that improve with age

*How a lesson becomes useful beyond the team that learned it*

Suppose a team discovers why its export service occasionally publishes the same file twice. A worker uploads the file, loses its connection before acknowledging the job, and receives the job again. The queue is behaving as designed. The worker has treated an uncertain outcome as a failed operation.

The team repairs the problem and writes a good account of the investigation. Six months later, engineers working on invoicing encounter the same sequence. Their service looks quite different, and nobody thinks to search the export team's incident reports.

The organization has paid for the lesson twice. That alone does not prove negligence. Some repeated investigation is cheaper than finding and understanding somebody else's work. But if the same failure keeps appearing in different products, a collection of capable teams is leaving something on the table.

An organization acquires experience whenever its people solve problems. Whether that experience improves its future work depends on what happens after the local problem has been resolved.

## What can travel

The export team's patch is probably the least transferable part of its investigation. It depends on a particular object store, job representation and naming convention. Copying it into the invoicing service could create a new defect.

The useful lesson lies one level below that patch: the external side effect and the queue acknowledgement are separate operations. Losing contact between them leaves the worker unable to tell whether the effect happened. Any retry policy has to account for that uncertainty.

Even this statement needs boundaries. The notification team may accept an occasional duplicate message. The invoicing team may require a stable operation identifier and a reconciliation process. Another system might make the side effect and acknowledgement atomic within one database. Similar-looking code does not imply identical obligations.

A transferable finding therefore needs enough information for another team to decide whether it applies. What promise was being broken? Which sequence broke it? What conditions were necessary? How could someone reproduce or rule out the problem elsewhere? A link to the original evidence lets the receiving team investigate without trusting a compressed moral of the story.

This changes the purpose of an incident report. It still explains what happened locally, but it can also offer a testable question to a specific audience. The export team could ask the owners of other queued jobs whether a successful external operation can be repeated after an ambiguous acknowledgement. That is a much more useful interruption than sending every engineer a lengthy report marked "lessons learned."

## Somebody has to receive the lesson

Google's account of its [postmortem practice](https://sre.google/sre-book/postmortem-culture/) describes review, broader sharing and exercises that reuse previous incidents. The document is part of a social process: people inspect it, discuss it and use it in later work. Putting a report in a searchable repository is only one step.

For the export finding, someone needs to identify plausible recipients and allow them time to respond. That job might belong to the engineer who led the investigation, a reliability group or a rotating representative from the affected teams. The title matters less than the assigned responsibility and available time.

The receiving team should have several legitimate responses. It might demonstrate that its transaction boundary prevents the problem, run the reproduction and find a defect, or explain why duplicates are acceptable in its product. It may also find that the proposed test cannot establish anything useful in its environment. All of these responses improve the organization's account of where the finding applies.

Requiring every recipient to install the original team's fix would defeat this process. It would replace local reasoning with compliance, and it would conceal differences that may matter on the next investigation.

Agents could reduce some of the mechanical cost. They can search for similar acknowledgement paths, trace a job through different repositories and prepare a candidate reproduction. Those candidates still need local review. A textual resemblance is a reason to inspect a service; it is weak evidence that the service shares the defect.

The transfer is complete when a receiving team can make a better decision. A hundred report views do not establish that. A short response explaining why a service is unaffected may.

## The price of telling the truth

Useful organizational memory depends on what people are willing to put into it.

An engineer may know that a recovery procedure works only because one colleague remembers an undocumented step. Another may suspect that a celebrated platform migration has made a common task harder. If mentioning these facts creates trouble for the speaker, a beautifully maintained knowledge system will contain a selective account of reality.

In her [1999 study of 51 work teams](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Organizational_Learning_and_Change/Edmondson_1999_Psychological_safety.pdf), Amy Edmondson found an association between psychological safety and learning behavior. The study concerned teams in a manufacturing company; it does not establish how an AI-assisted software organization should be designed. It does give us reason to treat the interpersonal cost of asking questions and reporting errors as part of the learning problem.

For engineering managers, this has ordinary consequences. When a team discloses that an accepted design is unsafe under a particular workload, the response affects what gets disclosed next time. If every investigation turns into an argument about who approved the original change, engineers have an incentive to describe findings as isolated accidents.

An honest report may also expose a decision above the team's authority. Perhaps the service was given a delivery deadline that excluded recovery work. Perhaps ownership was split in a way that left no team responsible for the full operation. An organization that records only technical remedies will keep reproducing the conditions that made those remedies necessary.

This does not mean abandoning accountability. Someone must own the follow-up, make the tradeoff explicit and check that the remedy works. It means examining how reasonable local decisions produced an unacceptable overall result, including the decisions made by management.

## Shared tools acquire landlords

After several teams investigate ambiguous acknowledgements, a shared testing tool may become worthwhile. It could interrupt workers after an external effect and check what happens when the job returns. Teams would supply their own definition of an acceptable outcome.

This is a promising use of accumulated experience. It is also the beginning of a maintenance obligation.

Who updates the tool when a queue client changes? Who explains a confusing failure? Can a team extend it without waiting for another department's planning cycle? If the original author leaves, does anyone still understand which failures the simulator can and cannot represent?

There is no free transfer of expertise into infrastructure. A common tool can reduce duplicated work while concentrating a new dependency in one place. Its owners need to see how other teams use it, and those teams need a way to challenge its assumptions.

Sometimes the right shared asset is smaller: a recorded demonstration, a minimal test case, a few questions added to a design review. Building a framework before the differences between services are understood can consume more effort than the repeated investigations it was meant to replace.

The useful question is whether sharing makes the next team's work easier after adaptation and support have been counted. That is the same discipline needed when deciding [what software should remember](./what-software-should-remember.md): retention earns its place through later use.

## Keep the disagreement

Organizations can become very efficient at spreading a bad lesson.

Suppose the export incident is reduced to a company rule that all background jobs must use one particular queue library. The library includes a helpful deduplication mechanism, but its protection expires after a configurable period. Years later, a team uses it for jobs that may remain suspended beyond that period. The organization remembers the approved solution and has forgotten the conditions that justified it.

A healthy shared practice preserves the reason for the rule, the scope of its evidence and the circumstances under which an exception makes sense. People need to be able to say that a standard no longer fits without first winning an argument about the competence of everyone who adopted it.

Local variation has a cost. It can make operations harder and force repeated tool development. Uniformity also has a cost: a mistaken assumption can reach every service at once. The balance depends on what is being standardized. Common identifiers, interoperable evidence and clear ownership may support independent judgment better than a mandatory implementation.

An organization should also remember who disagreed and why, where that disagreement remains relevant. A rejected alternative can be a useful starting point when conditions change. [Negative knowledge](./the-value-of-forgotten-alternatives.md) needs enough context to prevent an old decision from becoming a permanent prohibition.

## A modest test of institutional learning

Choose one recent finding that plausibly affects another team. Ask its authors to prepare the smallest useful explanation and a way to check the claim. Ask a receiving team to assess it during ordinary planned work, with time explicitly set aside. Keep a record of the adaptation effort, any decision it changed and whatever remained unclear.

The first attempt may reveal that the explanation relies on conversations absent from the report. It may show that the reproduction assumes a deployment arrangement nobody else uses. Those are findings about the transfer process, and they are worth correcting before building a larger programme around it.

Later, let someone who did not participate in either investigation try to use the result. If they can identify the relevant condition and run a meaningful check without calling the original author, some capability has survived its immediate circumstances.

It will still need maintenance. Services change, people leave and old remedies become inappropriate. An organization that improves with age must be able to retire its lessons as carefully as it spreads them.

When another team meets an ambiguous acknowledgement, it should have somewhere useful to start. The earlier investigation can give it an experiment to run and enough context to judge whether the result applies.
