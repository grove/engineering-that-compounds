# When software forgets the world

*Keeping domain knowledge in contact with its subject*

Suppose a company hires out equipment. Its booking system treats an item as available when the previous hire ends. That rule worked when customers returned equipment to a staffed desk and employees inspected it before closing the hire.

The company later introduces unattended returns. A customer can leave an item at a depot on Sunday evening, and the system closes the hire automatically. Inspection now happens on Monday. Staff keep a separate list of items they do not want to promise to another customer yet.

Nothing in the booking system is malfunctioning. Its tests confirm that equipment becomes available when a hire closes. The availability service is fast and reliable. Its documentation accurately describes the rule.

The staff's list is doing work the software no longer represents.

A system can become better engineered internally while its account of the world grows less useful. If we want engineering knowledge to improve with experience, we have to keep renewing the observations on which that knowledge rests.

## The assumptions beneath a correct program

Michael Jackson's [The World and the Machine](https://doi.org/10.1145/225014.225041) places the purpose of a software system in the world where it is used. Examining the machine alone cannot establish whether it serves that purpose. It is a useful reminder because the machine is usually the part engineers can inspect most easily.

In the hire company, “the previous hire has ended” and “the equipment can be promised to someone else” were once connected by a procedure. An employee inspected the item before closing the transaction. The code depended on that procedure even though the procedure was never part of the program.

Pamela Zave and Jackson develop the distinction between requirements, specifications and descriptions of the environment in [Four Dark Corners of Requirements Engineering](https://doi.org/10.1145/237432.237434). A system's behavior supports the desired outcome only in conjunction with assumptions about its environment. If those assumptions fail, a correct implementation can cease to meet the requirement.

We can express the hire system's assumption quite plainly: closing a hire means that someone has established the item's readiness for its next use. Once unattended returns remove that step, the implication no longer holds.

The remedy might be a new state in the application. It might also be a change to the return procedure, an adjustment to when the company accepts reservations or a better way of handling uncertain availability. Choosing among them requires knowing how the depots operate. A code review will not provide that knowledge.

## Workarounds are evidence

The separate list should attract an engineer's attention, but not because every spreadsheet or handwritten note is a defect to automate away.

It may represent a sensible division of work. Staff might use it for unusual judgments that do not justify a permanent feature. It might be a temporary response to a local problem. It might also reveal that the central system's categories no longer fit the work.

The first useful question is what the list allows people to do. Who adds an item? What information do they use? What would happen if the list disappeared tomorrow?

Watching a member of staff handle a returned item may reveal that “inspection” covers several different activities. Some items need a quick check. Others wait for a missing accessory or for an employee with particular experience. The company may allow a provisional reservation for some items while refusing it for others.

Replacing the list with a single “inspected” checkbox before understanding those distinctions could make matters worse. Staff would still need judgment, but the new system might imply a certainty they do not have.

There is also knowledge in the cases people avoid entering. If staff know the booking system will make an unsuitable promise, they may arrange a hire by phone and record it afterwards. Usage data then excludes the very cases the engineers most need to examine. A dashboard showing that almost all recorded bookings follow the intended process could be perfectly accurate and deeply misleading.

These possibilities are reasons to investigate a workaround. They are not reasons to assume its users are right about every aspect of the solution.

## What observation can establish

A visit to one depot will improve the team's understanding, but it will not produce a complete account of the business.

An experienced employee may describe how the work is supposed to happen. A new employee may follow a different procedure. A quiet Tuesday may reveal little about a Monday morning after a busy weekend. The engineer's presence can also change what people do or what they choose to explain.

The team needs to compare accounts with examples. It can follow several hires from reservation through return, examine a few disputed bookings and ask staff to explain discrepancies between the records and what happened. Where two depots disagree, that disagreement is itself useful. It may reveal a legitimate local difference or a policy nobody has settled.

The scope should stay modest enough that someone can act on the findings. “Understand all equipment operations” is an invitation to an endless study. “Find out what evidence staff use before offering equipment returned outside staffed hours” gives the investigation a boundary.

Once that question is clearer, implementation becomes useful again. An agent can help build two small prototypes: one where reservations wait for confirmation and another where staff allocate a pool of equipment with an allowance for uncertain returns. Staff can try them against real examples, including the awkward ones.

A prototype can expose confusion in a proposed workflow. It cannot establish that the new workflow will work across the company simply because the interface is easy to use. That requires a bounded trial in the actual operation, with a way to recover when the proposal proves incomplete.

## Distinguish facts from decisions

Some assumptions describe what happens. Others describe what the organization wants to permit. They need different treatment.

“Items returned overnight are inspected before the depot opens” is an empirical claim. It can be checked, and it may be true at one depot and false at another.

“Customers may reserve an item before it has been inspected” is a policy choice. Observing that employees sometimes do it does not establish that the organization should permit it. It tells us there is a practice worth examining, including who benefits and who bears the consequences when the item is unavailable.

This distinction matters when agents help maintain requirements. An agent analyzing historical records may infer a rule from repeated behavior. If that behavior was a workaround, an exception or a mistake, turning it into a specification can give it an authority it never had.

The same problem occurs when engineers treat an old test as proof of intended policy. The test may faithfully encode a compromise made when the service had one depot and a different operating model.

For consequential rules, the record should say what was observed, what was decided and who has the standing to reconsider the decision. This adds a practical requirement to [What software should remember](./what-software-should-remember.md): preserving a claim without preserving its status can make future reasoning worse.

Disagreement should remain visible until it is resolved. A sentence that makes two conflicting procedures sound compatible will help nobody when the next ambiguous hire arrives.

## Renew the knowledge where change occurs

We cannot continuously revisit every fact on which a system depends. Most would tell us nothing new, and the investigation itself would disrupt the people doing the work.

The company can instead identify events likely to invalidate its important assumptions. Unattended returns are one. Opening a depot with different staffing is another. A new class of equipment may require a different inspection procedure. Each change gives the team a reason to examine the relevant parts of the model.

Operational evidence can provide additional prompts. A growing gap between recorded returns and readiness, repeated manual overrides or customers being offered substitutions may indicate a mismatch. These signals tell us where to look; they do not explain the cause on their own.

Nor should every signal become another permanent dashboard. If a short investigation resolves an uncertainty, a temporary report may be enough. The continuing cost of maintaining a measure belongs in the decision to keep it.

When a claim matters enough to retain, attach it to an observation and a condition for review. A note that the current availability rule was checked against three depots during a staffed return process is more useful than a timeless assertion that “returned equipment is available.” It also makes the limits of the evidence hard to miss.

Changes to the business should be able to trigger changes to engineering knowledge even when no one has requested a software feature yet. Otherwise, the organization will hear about the mismatch only after staff have absorbed it into their own work.

## A useful model leaves things out

There is a temptation, after discovering an omitted distinction, to represent everything explicitly. The hire system acquires a state for each local procedure, every employee exception and all the ways an item can wait for attention.

That can be as unhelpful as the original simplification. The world contains more detail than a useful application should preserve. Some distinctions do not affect the decisions the software supports. Others change so frequently that a rigid representation would impose work without improving the outcome.

The team should ask what a new distinction enables. Separating “returned” from “ready” may prevent promises the company cannot meet. Recording the exact sequence in which an employee checks a straightforward item may contribute very little. A field for a meaningful unresolved condition may serve better than an elaborate state machine for every possible cause.

The decision also has to account for who maintains the information. If employees must perform extra data entry, the benefit should reach their work or the customers they serve. A more complete database is not sufficient justification by itself.

And sometimes the original model should survive. After investigation, the company may decide that its rare exceptions are best handled by people, while the booking system continues to cover the common case. The improvement is then a clearer boundary and an agreed procedure for exceptions, rather than another feature.

## Return to the depot

The team might ultimately introduce a separate readiness decision and a small queue for items awaiting it. It might revise how provisional bookings work. Whichever change it chooses, someone should return to the depot after it has been in use for a while.

Has the separate list disappeared because it is unnecessary, or because staff moved it somewhere else? Can employees explain the new states consistently? Have customers gained a more dependable service? Those questions concern the purpose of the work and deserve a place beside the deployment checks.

Over time, the system can accumulate better knowledge of the operation it supports. That knowledge will include distinctions worth preserving and previous distinctions that have outlived their usefulness. Its quality depends on the team's willingness to revise both.

The booking service will still need tests, clear boundaries and reliable deployments. It will also need engineers who spend some of their time watching how the equipment is actually returned.
