# Engineering that compounds

*Essays on what engineering leaves behind*

Two teams can deliver the same feature and finish with quite different prospects for the next one. One has another piece of software to maintain. The other has also learned something about its customers, found a way to reproduce a troublesome failure, or made a decision easier to reverse. Those differences rarely appear in a release note. They matter when the next awkward request arrives.

This collection follows [Software that improves with age](https://grove.github.io/software-that-improves-with-age/). It looks beyond the condition of a codebase to the knowledge, judgment and habits that make engineering possible. If AI reduces the cost of some implementation work, where should we spend the time and attention it frees? And how would we tell whether that investment had helped?

The word *compounds* makes a claim that needs testing. More documentation, tests or automation can just as easily create more upkeep. These essays ask when earlier work makes later work more effective, what gets lost along the way, and when an investment should be abandoned.

For something to try on your next ticket, start with [Engineering that compounds](./essays/engineering-that-compounds.md). It follows a small integration change through planning, review, retaining a useful lesson and handing the work to someone who was not there. The companion [Patterns of compounding engineering](https://grove.github.io/patterns-of-compounding-engineering/) supplies the field guide: concrete techniques, runnable examples and ways to check whether the effort helped.

Want to test the argument? The [second-capability pilot](./research/second-capability.md) is a proposed comparison of the cost and quality of building a new verification capability after deliberately retaining a reusable scenario or following ordinary development practice. It includes a stopping rule and a reporting template; no study results are claimed.

## Reading order

Eleven essays in four parts. Read them in order, or start with the question closest to your work. Audio editions are temporarily not included in the published site.

1. **[Engineering capital](./essays/engineering-capital.md)** — What remains useful after the immediate task is finished, and when those benefits begin to reinforce one another.
2. **[What software should remember](./essays/what-software-should-remember.md)** — Keeping the reasons for a decision available, without turning yesterday's assumptions into permanent rules.
3. **[The value of forgotten alternatives](./essays/the-value-of-forgotten-alternatives.md)** — What failed experiments can teach the next person, and how to record their limits.
4. **[Designing for decisions we haven't made yet](./essays/designing-for-decisions-we-havent-made-yet.md)** — The choices architecture keeps open, the commitments code cannot undo, and the cost of waiting.
5. **[How engineers become engineers](./essays/how-engineers-become-engineers.md)** — Developing judgment when much of the implementation can be delegated.
6. **[When software forgets the world](./essays/when-software-forgets-the-world.md)** — Finding out when a well-tested system has stopped matching the work people need to do.
7. **[Organizations that improve with age](./essays/organizations-that-improve-with-age.md)** — How a lesson learned by one team becomes useful to another.
8. **[Measuring the capacity for change](./essays/measuring-the-capacity-for-change.md)** — Looking for evidence of improvement across successive changes, including the costs that a productivity chart can hide.
9. **[Engineering that compounds](./essays/engineering-that-compounds.md)** — Follow an integration change from the first awkward question to the next engineer's attempt, and try the habit on your own work.

10. **[The ability to delegate](./essays/the-ability-to-delegate.md)** — Use recurring interruptions to discover which capabilities would make a particular kind of work easier to hand off.
11. **[Architecture for parallel work](./essays/architecture-for-parallel-work.md)** — Find out which decisions can happen independently and what it costs to put the results together.

## Website and audio

GitHub Pages address: [grove.github.io/engineering-that-compounds](https://grove.github.io/engineering-that-compounds/).

Build a text-only preview with Python 3.10 or later; no packages are needed:

```sh
python3 site/build.py --check-text
```

To check narration after regenerating it, follow the Python 3.12 instructions in the publishing guide, then run:

```sh
python3 site/build.py --check
```

The output is `_site/`. Open it through a local static server, for example `python3 -m http.server --directory _site 8000`.

The [publishing guide](./CONTRIBUTING.md) explains GitHub Pages, local checks and the optional narration workflow. GitHub Actions currently builds and publishes the text-only site; TTS generation and narration publishing are deferred. Narration uses Kokoro's `bf_emma` British English voice, as in the original collection.

## Credits and license

The static generator, initial styles and narration approach are adapted from [Software that improves with age](https://github.com/grove/software-that-improves-with-age), with a new Forest & Moss theme. The site identifies the audio as synthetic narration.

Licensed under the [Apache License 2.0](./LICENSE).
