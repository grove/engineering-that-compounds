# Designing for decisions we haven't made yet

*What it costs to keep a choice open*

Consider a team building a document service. It has to decide how to attach comments to text. For the first release, a comment records the character positions at which its selection begins and ends. The implementation is small, and an agent can produce another one using a different representation in an afternoon.

Six months later, customers have written a million comments. They have also edited their documents, exported them and built integrations around the comment identifiers. The team now wants comments to survive more substantial changes to the text.

Replacing the implementation is still straightforward. Recovering what an old comment referred to may be impossible if the service never retained the relevant text or document version. The cheap part of the decision has become cheaper. The expensive part was elsewhere all along.

When we talk about the freedom to change software, we should be clear about which freedom we mean. Being able to rewrite a component tells us little about the commitments already made through it.

## Where a decision takes hold

Some decisions remain largely inside the codebase. A search routine uses one indexing strategy rather than another. Provided its behavior and resource use remain acceptable, the maintainers can replace it without asking anyone else's permission.

Other decisions establish expectations outside that boundary. A customer stores our identifiers. Another service reads our export format. An operator develops a procedure around the order in which events arrive. Once that happens, changing the software involves changing someone else's work as well.

Persistent data creates a similar obligation. A representation chosen for today's convenience can discard information needed for tomorrow's interpretation. A migration can reorganize the information we have. It cannot reliably recover distinctions we chose never to record.

The document team therefore has several decisions to make, each with a different cost of reversal. It can choose a simple matching algorithm now and replace it later. It needs more care over the meaning of a comment identifier, the evidence retained about the original selection and what the public interface promises when that selection can no longer be found.

Calling the entire feature reversible because its code is easy to regenerate would conceal the decisions that deserve the most attention.

## Boundaries around uncertainty

David Parnas's [1972 paper on decomposing systems into modules](https://doi.org/10.1145/361598.361623) proposed hiding design decisions that are difficult or likely to change. A useful boundary limits how much of a system needs to know about a particular choice. It does not remove the choice or make every possible replacement equally easy.

For the document service, a boundary around locating a comment's selection could let the team try different matching strategies without changing the surrounding application. But that boundary is only useful if its contract allows the outcomes the team may encounter. An interface that always returns an exact position has already ruled out uncertainty, even if its implementation sits in a separate package.

Suppose a paragraph appears twice after an edit. A matching algorithm may find two plausible locations. The product needs a way to represent that ambiguity. It could leave the comment attached to an older version, ask the reader to choose or show it separately from the current text. Each response has consequences for the people using the service.

A more elaborate algorithm cannot settle that product question. Nor can a generic interface repair a contract that has promised the wrong thing.

Preserving choices therefore requires some understanding of where uncertainty lies. We might be uncertain about how to find an anchor efficiently while being quite certain that the service must preserve comments when it cannot find one. That is enough knowledge to establish a useful boundary without designing every future matching strategy.

## The price of an option

Carliss Baldwin and Kim Clark describe this economic aspect in [The Option Value of Modularity in Design](https://scholarsarchive.byu.edu/facpub/8944/). Their analysis treats opportunities to replace parts of a modular design as real options. The value depends on factors including the potential for improvement, the cost of experiments and the cost of establishing the architecture that makes independent changes possible.

This is a helpful way to think about architecture, provided we remember that options cost something to maintain.

The document team could retain each original text selection, some surrounding context and a reference to its document version. That may preserve ways of interpreting comments later. It also consumes storage and complicates deletion and retention behavior. Keeping every historical document forever would preserve still more choices, at a much greater cost.

The relevant question is whether the retained information supports a plausible future need whose cost would otherwise be substantial. We cannot answer that by counting how many hypothetical designs an architecture could accommodate.

There are also cases where cheap implementation reduces the value of building an abstraction in advance. If a small internal component has no persistent state and no outside consumers, replacing it when the need arises may cost less than maintaining a flexible framework from the outset. AI could strengthen that argument by reducing the effort of the eventual replacement.

The same change in economics can therefore favor more investment at a public boundary and less investment inside it. We should expect to spend our effort unevenly.

## Buying information before making a promise

Sometimes the best way to preserve a choice is to learn enough to stop keeping it open.

Before publishing the comment interface, the team can collect examples of edits its users actually make. It can compare position tracking with matching based on retained text. It can inspect the cases in which each approach loses the selection or attaches a comment to the wrong passage.

An agent can help construct these experiments and run them across a collection of documents. The team still has to judge whether the examples represent real editing practices and whether the behavior is acceptable. A test corpus full of small spelling corrections will make a weak anchoring scheme look unusually dependable.

The experiment should help the team make a particular decision. If the uncertainty concerns how often ambiguous matches arise, measuring throughput alone is an attractive distraction. If users care chiefly about retaining the discussion, the team may discover that preserving the old passage is more valuable than sophisticated automatic relocation.

There is a stopping point. More experiments will usually reveal more edge cases, but a product cannot wait until its designers have eliminated every uncertainty. A useful investigation ends when the remaining uncertainty no longer justifies delaying the commitment, or when the team has established how it will handle the unresolved cases.

It helps to record what new evidence would change the decision. The note discussed in [What software should remember](./what-software-should-remember.md) can say that the simple matching strategy is adequate for the observed editing patterns, and that widespread document restructuring would warrant another look. The decision then has a reason and a boundary.

## Reversibility has to be exercised

A plan to reverse a change deserves the same scrutiny as the change itself.

Suppose the document service introduces a new representation for comments. It deploys the new code successfully and begins writing new records. A problem appears the next morning. The old application starts when redeployed, but cannot interpret those records. The team had preserved its old executable without preserving its ability to return to the old behavior.

Sandeep Pokkunuri's account of [rollback safety at Amazon](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/) addresses this problem directly. Safe deployment requires attention to compatibility between readers and writers across versions, including during transitions. Testing each version in isolation does not establish that moving between them is safe.

For our document service, a rehearsal could create comments using the new representation, make edits and then run the previous application against the resulting state. If the old application cannot cope, the team needs a different transition plan. It might introduce support for reading the format before allowing any component to write it, or keep a compatible representation during a bounded migration period.

The rehearsal gives a claimed option an observable meaning. We can return to a specified earlier state under specified conditions. It may also reveal the point beyond which returning is no longer practical.

That point should be deliberate. Once a migration has completed and the new representation has proved satisfactory, keeping both indefinitely can become a source of errors. Maintaining an escape route for a week and supporting two storage models for five years are quite different investments.

## The cost of refusing to choose

An organization can become so attached to flexibility that every decision remains provisional.

The document service might retain three anchor formats, two public interfaces and several modes of relocation, each introduced to avoid committing too soon. Every engineer and agent then has to understand their interactions. Customers discover that a feature behaves differently depending on when a document was created. Tests grow around combinations nobody intentionally designed.

Those costs are present even if none of the alternatives is ever used again. An option that once had value can become an obligation.

Keeping a choice open should therefore come with a reason to revisit it. Perhaps the team is waiting for a particular customer workflow to be tested, or for a migration rehearsal to establish an acceptable recovery path. Once that evidence arrives, it should either make the commitment or identify a new, concrete reason for waiting.

Sometimes an early commitment is exactly what makes progress possible. A stable public contract lets other teams build without negotiating every detail. A shared data representation makes comparisons and tooling easier. Preserving our freedom at the expense of everyone else's predictability is not automatically good engineering.

The practical aim is to place commitments where they buy coordination and leave room for change where useful information is still likely to arrive.

## What remains possible

The document service will eventually make choices its maintainers regret. No architecture can prevent that. It can, however, make the consequences of those choices easier to understand before they spread.

When reviewing a consequential design, I would ask what it writes into lasting data, what other people will come to depend on and what evidence would persuade us to replace it. I would then ask whether we have actually tried the replacement or reversal we claim will be easy.

These questions often lead to modest changes: retaining a piece of information, narrowing a promise, rehearsing a migration or deleting an unnecessary extension point. They rarely produce an architecture that anticipates everything.

Years later, the value becomes visible when a new requirement arrives. The team has enough evidence to reinterpret its old data, enough freedom to replace an uncertain algorithm and a sufficiently stable contract that customers can continue their work. Someone made those later decisions possible by being careful about a few earlier ones.
