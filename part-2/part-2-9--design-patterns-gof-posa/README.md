# 9. Design Patterns (GoF & PoSA)

**Part 2 — Design Principles & Patterns** · [Back to curriculum index](../../README.md)

## One-sentence pitch
Design patterns are a shared vocabulary for solutions that keep reappearing once you
apply the principles from Topics 6–7 consistently — learning the catalog means you
stop reinventing Strategy and Observer badly, and start recognizing them by name in
five seconds during a code review.

## Learning objectives
- Can classify a pattern as creational, structural, or behavioral (GoF) and explain
  what category of problem each group solves.
- Can implement Factory Method, Decorator, and Observer from scratch in a realistic
  (non-textbook) scenario, and explain what the code would look like without the
  pattern.
- Can refactor a large conditional dispatching behavior into Strategy, and a
  tightly-coupled "notify everyone inline" block into Observer.
- Can name at least one PoSA concurrency pattern (e.g., Half-Sync/Half-Async,
  Leader/Followers) and implement a toy version of it.
- Can argue, for a specific piece of code, whether a pattern is solving a real problem
  or adding indirection nobody needs (tying back to YAGNI from Topic 8).

This topic's material is split into two files to stay readable:

- **[outline.md](outline.md)** — the ~55-minute session outline with segment-by-segment
  content, covering GoF creational/structural/behavioral patterns and PoSA
  concurrency/distributed patterns.
- **[homework.md](homework.md)** — full notes for all three homework assignments,
  with starter code in [`examples/`](examples/).

## Further resources
- Free companion: [refactoring.guru — Design Patterns Catalog](https://refactoring.guru/design-patterns/catalog) · Vanderbilt, [POSA2 companion materials](https://www.dre.vanderbilt.edu/~schmidt/POSA/POSA2/)
