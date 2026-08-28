# 5. Programming Paradigms

**Part 1 — Foundations of Code Quality** · [Back to curriculum index](../../README.md)

## One-sentence pitch
Structured, functional, and object-oriented programming aren't competing religions —
they're tools shaped for different kinds of problems, and the strongest real-world code
usually mixes them deliberately instead of picking one and forcing every problem
through it.

## Learning objectives
- Can implement the same small algorithm in structured/procedural, functional, and OOP
  style, and articulate concrete trade-offs (readability, testability, extensibility)
  between the three, not just "they're different."
- Can identify which paradigm best fits a given problem shape (e.g., a fixed
  step-by-step process vs. a family of interchangeable behaviors vs. a data
  transformation pipeline).
- Can design and build a "functional core, imperative shell": pure functions for
  decision-making logic, with I/O and mutation isolated at the boundary.
- Can explain, with a concrete example, what a functional-core/imperative-shell design
  makes easier (testing the core) and what it can make harder (tracing the full
  request path across the boundary).

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: three solutions, one problem | 5 min | Same feature request, radically different code shapes |
| Recap: what each paradigm optimizes for | 10 min | Structured (control flow), functional (data transformation, testability), OOP (extensibility, modeling variation) |
| Matching problem shape to paradigm | 10 min | Reading a requirement and predicting which paradigm fits |
| Mixing paradigms deliberately | 10 min | Functional core / imperative shell as the dominant real-world pattern |
| Live comparison exercise | 10 min | Word-frequency counter walked through in all three styles |
| Wrap-up / Q&A | 5 min | Paradigm fluency as a design skill, not a language choice |

**Hook: three solutions, one problem (5 min).** Show three short solutions to the same
small problem (e.g., computing a discount given a cart) — one procedural with a
sequence of steps and a few `if`s, one functional as a pipeline of pure transforms, one
OOP with a `DiscountStrategy` interface and concrete strategies. Ask which one the
class would pick, and why — there's no single right answer, which is the point.

**Recap: what each paradigm optimizes for (10 min).** Synthesize Topics 2–4 rather than
re-teach them: structured programming optimizes for *locally reasoning about control
flow* — best when a problem is genuinely a fixed sequence of steps. Functional
programming optimizes for *testability and predictability of data transformations* —
best when the problem is "take this data, produce that data," with minimal need for
extension over time. OOP optimizes for *extensibility under variation* — best when a
problem has a family of related behaviors that will grow (new payment types, new
shapes, new file formats).

**Matching problem shape to paradigm (10 min).** Work through several requirement
statements as a group and predict which paradigm fits most naturally, and why: "process
this file top to bottom, one clear sequence of stages" (structured/procedural);
"transform this list of records into a report, no persistent state" (functional);
"support new export formats being added over time without touching existing code" (OOP,
via an interface/strategy). Stress that these are defaults, not laws — a functional
codebase can still model variation with higher-order functions instead of interfaces,
and this is fine.

**Mixing paradigms deliberately (10 min).** Most production code isn't pure anything —
it's commonly a "functional core, imperative shell": the decision-making logic is
written as pure functions (easy to unit test, no mocking needed), while I/O, database
calls, and mutation live in a thin outer layer that calls into the core. Show a small
diagram: `shell (impure, calls out to DB/network) → core (pure functions, all the
actual business rules) → shell (impure, persists the result)`. This is often *also*
where OOP shows up — the shell may be organized as classes/objects even while the core
stays purely functional.

**Live comparison exercise (10 min).** Walk through a word-frequency counter in the
three styles side by side (procedural: read line, split, loop, increment counts in a
dict; functional: split → map to words → reduce into a frequency map, no loops;
OOP: a `WordCounter` class with an internal `Counter` collaborator and a `count(text)`
method). Ask the class, live, which version would be easiest to extend with "ignore a
configurable stop-word list" — this is meant to surface that the answer isn't obvious
and depends on how the extension is shaped, not just the paradigm.

**Wrap-up (5 min).** The goal of this topic isn't to declare a winner — it's paradigm
fluency: recognizing what shape a problem has and reaching for the paradigm (or mix of
paradigms) that fits, rather than defaulting to whatever the last project happened to
use. This closes Part 1; Part 2 assumes this fluency and starts stacking design
principles and patterns on top of it.

## Homework notes

### 1. Implement the same algorithm three ways and compare

**Goal:** Get hands-on evidence (not just an assertion) for how paradigm choice affects
readability, testability, and ease of extension — by changing the requirement after the
fact and seeing which version absorbs the change most gracefully.

**Approach / hints:**
- Pick a small, well-defined algorithm — a word-frequency counter works well and
  connects directly to the in-session exercise — and implement it three times: purely
  structured/procedural (loops, no classes, no map/filter/reduce), purely functional (no
  loops, no mutation, composed from `map`/`filter`/`reduce`), and OOP (a class or small
  hierarchy with clear responsibilities).
- Reuse code from Topics 2–4 if you built something similar there rather than starting
  from zero.
- After all three work, apply the *same* new requirement to each (e.g., "ignore a
  configurable list of stop words" or "also report the top 3 words") and note how much
  each version had to change.
- Write the comparison as a short table or a few paragraphs: readability, testability
  (how hard is it to unit test in isolation), and how easily each absorbed the new
  requirement — with specifics, not just impressions.

**Starter example (Python — functional version only, as a shape reference):**
```python
from collections import Counter
from functools import reduce

def word_frequency(text: str) -> dict[str, int]:
    words = text.lower().split()
    return dict(reduce(lambda acc, w: acc + Counter([w]), words, Counter()))

# TODO: write the procedural version (explicit loop + dict) and the OOP
# version (a WordCounter class) solving the identical problem, then apply
# the same new requirement to all three and compare.
```

**Definition of done:** Three working implementations of the same algorithm (one per
paradigm), evidence that all three were tested against the same new requirement after
the fact, and a written comparison covering readability, testability, and ease of
extension with specific observations for each version.

### 2. Convert an OOP or structured snippet to a functional-core/imperative-shell design

**Goal:** Practice the paradigm-mixing skill directly — isolating the actual
decision-making logic as pure functions and pushing I/O/mutation to the boundary — and
be able to say concretely what got easier and what got harder.

**Approach / hints:**
- Start from an existing OOP or structured snippet (yours from an earlier topic, or a
  provided one) where business logic and I/O/mutation are interleaved — e.g., a class
  method that reads from a database, makes a decision, and writes back, all in one
  method.
- Identify the actual decision points first (the "if this, then that" business rules)
  separately from the effects (reads, writes, logging).
- Extract the decision points into pure functions that take plain data in and return
  plain data (or a description of what should happen) out — no I/O, no mutation, no
  hidden dependencies.
- Rewrite the original method as a thin shell: read data in, call the pure core, apply
  the result as an effect. Write unit tests for the pure core with no mocking required,
  and note whether the shell became harder to read end-to-end as a trade-off.

**Definition of done:** A pure functional core with its own tests requiring no mocks or
stubs, a thin impure shell that performs all I/O and calls the core, and a short written
note on what got easier to test and what (if anything) got harder to follow by
splitting the logic this way.

## Further resources
- Free companion: Stanford [CS107: Programming Paradigms](https://see.stanford.edu/Course/CS107) (Stanford Engineering Everywhere)
