# 12. Architectural Patterns

**Part 3 — Architectural Foundations** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
MVC, DDD, microservices, event sourcing, CQRS — these are the reusable, named shapes that architectural styles collapse into once real business complexity shows up, and knowing the catalog means recognizing the right shape instead of reinventing it badly.

## Learning objectives
- Can explain the core idea of MVC, Domain-Driven Design, Microservices, Microkernel, Blackboard, Serverless, Event Sourcing, SOA, and CQRS in one or two sentences each, with a real-world example of where each is used.
- Can identify tactical DDD building blocks (entities, value objects, aggregates, repositories) in a given domain and apply them correctly.
- Can implement the same feature under both MVC and CQRS and explain the structural and operational differences.
- Can decompose a monolithic application into microservices, deciding what data each owns and whether communication should be synchronous or asynchronous.

This topic is split into two files to keep each one focused:

- **[outline.md](outline.md)** — the full ~50-minute session outline covering all ten subtopics.
- **[homework.md](homework.md)** — detailed notes (goal, approach, starter code, definition of done) for all three homework assignments.

Starter code referenced from the homework notes lives in **[examples/](examples/)**.

## Further resources
- Free companion: *[Software Engineering: A Modern Approach](https://softengbook.org/chapter7), Ch. 7* · Eric Evans, [DDD Reference](https://www.domainlanguage.com/ddd/reference/)
- Note: these two sources cover MVC, Microservices, Layered architecture, and DDD well, but neither name-checks Microkernel, Blackboard, SOA, or CQRS directly — the outline below leans on its own explanations for those four subtopics.
