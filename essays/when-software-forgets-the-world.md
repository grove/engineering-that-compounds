# When software forgets the world

*Keeping domain knowledge in contact with its subject*

Beside the booking terminal at a depot in a hypothetical equipment-hire company sits a laminated clipboard. On it is a handwritten list of machines currently parked in the yard that staff must not promise to a customer yet.

Nothing in the booking software is broken. Its tests verify that equipment flips back to *available* the moment a hire closes. The service is fast, reliable and well documented. It simply still assumes the world that existed when customers returned gear to a staffed desk and an employee checked it over before closing the hire.

Once the company added unattended Sunday drop-offs, the system began closing hires automatically while inspection moved to Monday morning. Nobody filed a bug report. The depot staff just reached for a clipboard, and the clipboard started doing the work the software stopped representing.

A system can grow cleaner, faster and better tested inside while its grip on the outside world slips. Domain knowledge is not something you extract once during discovery and lock into a schema; it decays whenever the work around the software moves on.

## The unstated premise under green tests

Michael Jackson made this point in [The World and the Machine](https://doi.org/10.1145/225014.225041): a program's purpose lives out in the domain, never solely inside the machine. Together with Pamela Zave in [Four Dark Corners of Requirements Engineering](https://doi.org/10.1145/237432.237434), he showed how a specification achieves its requirement only alongside assumptions about the environment. Break the environmental assumption, and a flawless implementation stops doing its job.

Here, the hidden assumption was simple: *closing a hire means someone has verified the machine is ready for the next customer.* Unattended returns severed that link without touching a single line of code.

The fix might be a new state in the booking system. Or it might be a change to the depot's Monday routine, a buffer before reservations open, or a way of marking availability as tentative. Reading pull requests will not tell you which one fits; watching the depot on Monday morning will.

## Read the workarounds before replacing them

A clipboard or a shadow spreadsheet should always make an engineer curious. Not every manual step is a defect waiting to be automated away, but every workaround marks a seam where the software stopped matching the work.

Before touching the schema, find out what the list actually does. Who writes on it? What triggers an entry? What breaks tomorrow if it disappears?

Watching staff handle Monday's returns quickly reveals that "inspection" is not one boolean. A pressure washer needs a two-minute visual check. A generator might wait for a missing cable or the one technician certified to test it. Staff may happily take a provisional booking for one and refuse it for the other. Turning the clipboard into a single `inspected` checkbox before noticing those distinctions can make everyone's day worse, replacing flexible human judgment with false precision.

## Software also bends the world it models

Domain drift is not only something that happens *to* software from the outside. Software actively changes the behavior of the people around it.

Once depot staff realize the booking system will cheerfully promise an uninspected generator to an online customer, they start handling tricky hires by phone and typing them into the system after the fact. The database now records only the tidy cases. A dashboard showing that 98% of bookings follow the intended workflow is completely accurate, and completely blind to the friction it created.

Customers adapt too. Introduce strict online availability rules and repeat contractors learn to over-book "just in case" and cancel late, shifting the utilization pattern the pricing engine was tuned for. Whenever a system enforces categories or incentives, people route around its sharp edges. Those detours are part of the domain now, even if they never appear in telemetry.

## Fieldwork with a boundary

Spending a morning at one depot beats guessing from headquarters, though one visit has its own blind spots. Senior staff describe how work is *supposed* to run; new hires improvise differently. A slow Tuesday hides the chaos of a Monday after a holiday weekend. And watching people changes what they do.

Compare stories against real artifacts: trace ten hires from booking to return, pull up three disputed bookings, and ask staff why the record disagrees with what happened. When two depots run the same step differently, pay attention. You may have found a real local constraint or an unresolved company policy.

Keep the question narrow enough to act on. "Understand all depot operations" turns into an endless safari. "Find out what evidence staff check before releasing gear returned after hours" finishes in two days. Once that question is clear, fast prototyping shines again: have an agent spin up two small workflows (say, tentative reservations awaiting confirmation versus a buffer pool) and walk depot staff through real awkward bookings from last week. Follow that with a bounded trial at one depot before rolling anything out company-wide.

## Facts are not policies

Half the mess in mature systems comes from mixing up what *happens* with what the business *wants*.

"Overnight returns are inspected before opening" is a claim about reality. It may be true at one depot and false at another, and you can check it by looking. "Customers may reserve an uninspected item" is a policy choice. Discovering that staff sometimes allow it does not make it the right rule; it tells you there is a tradeoff to settle openly, including who eats the cost when the machine turns out to be damaged.

This trap gets worse when coding agents mine historical records or codebases to infer requirements. If an agent reads a year of workaround data and turns repeated exceptions into formal specs, yesterday's makeshift fix silently acquires the force of law. Old unit tests do the same thing, faithfully preserving a compromise made when the company had one depot and no self-service drop-off.

Attach status and ownership to consequential rules, just as [What software should remember](./what-software-should-remember.md) recommends: note what was observed, what was decided, and who has the authority to overturn it. Keep unresolved disagreements visible instead of papering over them with vague wording.

## Renew the model when the business moves

Nobody can re-audit every domain assumption every quarter. Tie review to events that actually disturb the ground: launching unattended returns, opening a depot with different staffing, adding a regulated class of machinery. Watch operational friction too, like rising manual overrides, frequent last-minute equipment swaps, or growing gaps between recorded returns and actual handovers. Treat those as triggers to go look, not excuses to build ten permanent dashboards.

And resist the urge, once you spot a missing distinction, to model every local quirk in a sprawling state machine. A good model leaves plenty out. Separating *returned* from *ready* prevents broken promises to customers; tracking the exact checklist order an experienced technician uses rarely pays for the data entry it imposes. Sometimes the best engineering outcome after a depot visit is leaving the core booking model small and agreeing on a simple manual path for rare exceptions.

Whatever you ship, go back to the depot a month later. Did the clipboard vanish because the software solved the problem, or did staff just move it into a private chat group? Can a new hire explain the new states without hedging? Good tests and small modules keep the machine honest; walking back out onto the yard is what keeps it connected to the work it exists to serve.
