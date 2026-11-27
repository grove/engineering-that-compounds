# When software forgets the world

*Keeping domain knowledge in contact with its subject*

Picture an equipment-hire depot (a made-up setting, though anyone who has built operations software has seen its twin). Next to the booking terminal sits a laminated clipboard. On it is a handwritten list of machines currently parked in the yard that staff must not promise to a customer yet.

Nothing in the booking software is broken. Its tests check that equipment flips back to *available* the second a hire closes. The service is fast, clean, and well tested. It just still assumes the world from three years ago, when customers returned gear to a staffed counter and someone looked it over before closing the hire.

Once the company introduced unattended Sunday drop-offs, the software started closing hires automatically while inspection slid to Monday morning. Nobody filed a bug. Depot staff simply grabbed a clipboard, and the clipboard took over the piece of reality the software stopped knowing about.

Code can get cleaner and better tested every quarter while losing touch with the work it exists to support. Domain knowledge isn't something you harvest once in a discovery workshop and freeze into a schema; it decays every time the world around the system shifts.

## The unstated premise under green tests

Michael Jackson made this point cleanly in [The World and the Machine](https://doi.org/10.1145/225014.225041): a program's purpose lives out in the domain, never solely inside the machine. Together with Pamela Zave in [Four Dark Corners of Requirements Engineering](https://doi.org/10.1145/237432.237434), he showed that a specification only satisfies its requirement when its assumptions about the environment hold. Break the environmental assumption, and a bug-free implementation quietly fails.

Here, the hidden assumption was simple: *closing a hire means someone verified the machine is ready for the next customer.* Unattended drop-offs snapped that link without touching a line of code.

The right fix might be a new state in the booking system. Or it might be changing Monday's yard routine, adding a reservation buffer, or allowing tentative bookings. Reading pull requests won't tell you which one fits; standing in the depot on Monday morning will.

## Read the workarounds before replacing them

A clipboard or shadow spreadsheet should make any engineer curious. Not every manual step deserves to be automated away, but every workaround marks a seam where the software stopped fitting the job.

Before touching the schema, figure out what the list actually does. Who writes on it? What puts a machine on it, and what takes it off? What breaks tomorrow if you throw it away?

Watching staff work through Monday's returns quickly shows that "inspection" isn't a boolean. A pressure washer takes a two-minute visual look. A generator might wait on a missing cable or the one technician certified to test it. Staff will happily take a provisional booking on one and refuse it on the other. Replacing the clipboard with a single `inspected` checkbox before spotting that split can make everyone's week worse, trading flexible human judgment for tidy, useless precision.

## Software bends the world it models

Domain drift doesn't just happen *to* software from outside. Software reshapes the behavior of the people around it.

Once depot staff realize the booking app will cheerfully promise an uninspected generator to an online customer, they start taking tricky hires by phone and keying them in after the fact. Now the database only sees the clean cases. A dashboard reporting that 98% of bookings follow the intended flow is mathematically accurate and completely blind to the mess it caused.

Customers adapt too. Tighten online availability rules and regular contractors start over-booking "just in case" and canceling late, warping the utilization curve the pricing engine was tuned on. Whenever software enforces categories or incentives, people route around its sharp edges. Those detours become part of the real domain, even when telemetry never sees them.

## Fieldwork with a boundary

One morning at a depot beats guessing from headquarters, though a single visit has blind spots of its own. Veterans explain how work is *supposed* to happen; newer hires improvise differently. A quiet Tuesday hides the pile-up of a Monday after a holiday weekend. And watching people changes what they do.

Cross-check stories against real records: follow ten hires from booking to return, pull three disputed bookings, and ask staff why the database disagrees with what happened in the yard. When two depots handle the same step differently, pay attention. You've usually found either a real local constraint or a company policy nobody settled.

Keep the question tight enough to finish. "Understand depot operations" turns into a month-long safari. "Find out what staff check before releasing gear returned after hours" takes two days. Once the question is clear, fast prototyping earns its keep: have an agent mock up two small workflows (say, tentative reservations awaiting confirmation versus a holding buffer) and walk depot staff through real awkward bookings from last week, then trial the winner at one depot before rolling it out everywhere.

## Facts, policies, and competing interests

Half the tangles in mature software come from blurring what *happens*, what the business *wants*, and who *wins* when two groups disagree.

"Overnight returns are inspected before opening" is a claim about reality; you can check it by looking. "Customers may reserve an uninspected machine" is a policy call. Finding out that staff occasionally allow it doesn't make it the rule. It surfaces a real conflict.

The outside world isn't always one coherent truth waiting for better fieldwork. Depot managers want fewer angry contractors standing at the counter at 7 a.m. Online sales wants higher booking conversion and fewer unavailable listings. Finance wants higher fleet utilization and lower damage write-offs. Those three groups are pulling the same state machine in different directions. Domain modeling frequently exposes political disagreements that software can't solve on its own. At best, it forces them into the open so someone with authority actually decides who eats the cost when a promised machine turns out to be broken.

Coding agents make the old failure mode sharper. Point an agent at a year of override logs or legacy unit tests to infer requirements, and yesterday's makeshift coping mechanism quietly hardens into formal specification. Attach provenance and ownership to consequential rules, as [What software should remember](./what-software-should-remember.md) suggests: separate what was observed from what was decided, name who owns the policy, and leave unresolved disagreements visible instead of hiding them under vague status names.

## Go back out to the yard

Nobody can re-audit every domain assumption every quarter. Tie checks to events that actually shift the ground: launching unattended returns, opening a depot with different staffing, adding regulated equipment. Watch operational friction (rising manual overrides, frequent last-minute swaps, widening gaps between recorded returns and real handovers) as triggers to go look, not excuses to wire up ten permanent dashboards.

And resist modeling every local quirk once you spot a missing distinction. A good model leaves plenty out. Separating *returned* from *ready* prevents broken promises to customers; encoding the exact order a veteran technician prefers for a checklist mostly adds data entry nobody wanted. Sometimes the best engineering result after a depot visit is keeping the core model small and agreeing on a plain manual escape hatch for odd cases.

Whatever you ship, walk back into the depot a month later. Did the clipboard disappear because the software actually fit the work, or did staff just move the list into a private chat group? Can a new hire explain the states without hedging? Good tests keep the machine honest. Going back to the yard is how you find out if it still belongs to the world it runs in.
