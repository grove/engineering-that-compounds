# Engineering that compounds

*Essays on how teams become more capable*

Two teams can deliver the same feature and finish with quite different prospects for the next one. One has another piece of software to maintain. The other has also learned something about its customers, found a way to reproduce a troublesome failure, or made a decision easier to reverse. Those differences matter when the next awkward request arrives.

This collection follows [Software that improves with age](https://grove.github.io/software-that-improves-with-age/). It asks how an organization becomes better at understanding problems, solving them and developing the capabilities the next problem will need. AI can help investigate, teach, compare and verify as well as implement. Whether that help improves the whole job depends on the knowledge, judgment and working arrangements around it.

Our distant aim is to become ten times as effective with AI, within sustainable hours and with the same care for the people using the software. [What would ten times look like?](./essays/what-would-ten-times-look-like.md) makes the ambition practical: find what limits worthwhile work and choose one investment. [Where could 10× come from?](./essays/where-could-10x-come-from.md) explores six mechanisms for transforming the work. [What becomes possible?](./essays/what-becomes-possible.md) asks which valuable work might come within reach. These essays do not promise a measured multiplier.

The word *compounds* makes a claim that needs testing. A useful test can pay off repeatedly. A further claim is that it makes a new verification capability easier to develop. The [foundations](https://grove.github.io/compounding-engineering/foundations.html) explain that distinction and the theory behind it. The essays also examine where investment fails: when knowledge goes stale, improvements reinforce the wrong goal, or automation erodes the understanding needed to respond to a surprise.

For something to try on your next ticket, start with [Engineering that compounds](./essays/engineering-that-compounds.md). The companion [field guide](https://grove.github.io/patterns-of-compounding-engineering/) supplies patterns and runnable examples. For a team investment, use the [adoption guide](https://grove.github.io/compounding-engineering/adoption/) and its [investment canvas](https://grove.github.io/compounding-engineering/adoption/investment-canvas.html).

Want to test the argument? The [second-capability pilot](./research/second-capability.md) is a proposed comparison of the cost and quality of building a new verification capability after deliberately retaining a reusable scenario or following ordinary development practice. It includes a stopping rule and a reporting template; no study results are claimed.

## Reading order

Twenty essays in six parts. Read in order, or choose the question closest to your work. Each essay can stand on its own; the foundations and field guide offer shorter routes into practice. Audio editions are temporarily not included in the published site.

1. **[What would ten times look like?](./essays/what-would-ten-times-look-like.md)** — A distant ambition for teams working with AI, and how it helps us choose what to improve next.
2. **[Where could 10× come from?](./essays/where-could-10x-come-from.md)** — Six mechanisms that could change the economics of engineering, and how they might reinforce one another.
3. **[What becomes possible?](./essays/what-becomes-possible.md)** — Revisit valuable work that used to be too difficult, expensive or uncertain.
4. **[Engineering capital](./essays/engineering-capital.md)** — Distinguish the resources a team retains from what it becomes able to do.
5. **[Improving our ability to improve](./essays/improving-our-ability-to-improve.md)** — Combine existing capabilities and investigate whether they help develop the next one.
6. **[What software should remember](./essays/what-software-should-remember.md)** — Keeping the reasons for a decision available, without turning yesterday's assumptions into permanent rules.
7. **[The value of forgotten alternatives](./essays/the-value-of-forgotten-alternatives.md)** — What failed experiments can teach the next person, and how to record their limits.
8. **[Designing for decisions we haven't made yet](./essays/designing-for-decisions-we-havent-made-yet.md)** — The choices architecture keeps open, the commitments code cannot undo, and the cost of waiting.
9. **[How engineers become engineers](./essays/how-engineers-become-engineers.md)** — Developing judgment when much of the implementation can be delegated.
10. **[When software forgets the world](./essays/when-software-forgets-the-world.md)** — Finding out when a well-tested system has stopped matching the work people need to do.
11. **[Getting better at the wrong thing](./essays/getting-better-at-the-wrong-thing.md)** — Question the task, explore alternatives and retire assumptions that no longer hold.
12. **[Compounding learning](./essays/compounding-learning.md)** — Use AI to investigate recurring difficulties, test what they mean and find out whether the way you learn improves.
13. **[The economics of feedback](./essays/the-economics-of-feedback.md)** — Make important questions cheaper to answer without losing the evidence that makes answers useful.
14. **[Learning from things that go right](./essays/learning-from-things-that-go-right.md)** — Investigate successful adjustments and preserve the conditions that let people respond to surprises.
15. **[Organizations that improve with age](./essays/organizations-that-improve-with-age.md)** — How a lesson learned by one team becomes useful to another.
16. **[Measuring the capacity for change](./essays/measuring-the-capacity-for-change.md)** — Looking for evidence of improvement across successive changes, including the costs that a productivity chart can hide.
17. **[Engineering that compounds](./essays/engineering-that-compounds.md)** — Follow an integration change from the first awkward question to the next engineer's attempt, and try the habit on your own work.
18. **[The ability to delegate](./essays/the-ability-to-delegate.md)** — Use recurring interruptions to discover which capabilities would make a particular kind of work easier to hand off.
19. **[Architecture for parallel work](./essays/architecture-for-parallel-work.md)** — Find out which decisions can happen independently and what it costs to put the results together.
20. **[Automating the work of engineering](./essays/automating-the-work-of-engineering.md)** — What it takes for routine work to happen without somebody starting and supervising it each time.

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
