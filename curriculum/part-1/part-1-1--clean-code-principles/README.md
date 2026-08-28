# 1. Clean Code Principles

**Part 1 — Foundations of Code Quality** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Code is read far more often than it's written, and the difference between a codebase
people are afraid to touch and one they can safely change comes down to a small,
learnable set of habits — not talent.

## Learning objectives
- Can name and apply a consistent naming/formatting standard across a file, and explain
  why consistency matters more than which specific style is chosen.
- Can refactor a long method or class into smaller, single-purpose pieces, and explain
  cyclomatic complexity well enough to spot a function that has too many paths through it.
- Can rewrite a function that takes a boolean or null parameter into a form that doesn't
  need one (split methods, explicit types, or a small enum/object).
- Can separate framework/I-O code from business logic ("push code to the edges") in a
  small program.
- Can distinguish a command (does something, returns nothing meaningful) from a query
  (returns something, changes nothing) and fix a method that does both.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the codebase nobody wants to touch | 5 min | What makes code costly to change |
| Naming, style, and consistency | 10 min | Intention-revealing names; picking *a* style and sticking to it |
| Small functions, small classes, small files | 10 min | Single Responsibility at the function level; cyclomatic complexity |
| Pure functions and command-query separation | 10 min | Predictability; splitting "do" from "ask" |
| Avoiding null/boolean params; framework at the edges | 10 min | Flag arguments; where I/O and frameworks belong |
| Tests, organizing by actor, refactoring habits | 5 min | Fast/independent tests; who a module serves; refactor as a constant small habit |
| Wrap-up / Q&A | 5 min | Clean code as a discipline, not a one-time cleanup |

**Hook: the codebase nobody wants to touch (5 min).** Ask students to recall (or
imagine) a codebase where a "simple" change took days because nobody understood the
existing code, or where every fix seemed to break something unrelated. Clean code isn't
aesthetics — it's the difference between code that can absorb changing requirements and
code that actively resists them. Frame the whole session around one question: what
makes code *cheap to change later*?

**Naming, style, and consistency (10 min).** Cover intention-revealing names (`elapsed_time_in_days`
over `d`), consistent casing/formatting across a file or repo, and indentation as a
readability signal, not decoration. The core message: which convention you pick matters
less than picking one and applying it everywhere — inconsistency forces the reader to
re-learn the rules on every file.

**Small functions, small classes, small files (10 min).** Show a 100-line function doing
five things and extract it into five well-named functions. Introduce cyclomatic
complexity informally — count the independent paths through a function (each `if`,
`for`, `while`, `case` adds one) — and connect high complexity directly to "hard to
test, hard to reason about." A function with complexity of 15 needs 15 test cases to
cover every path; a function with complexity of 2 needs 2.

**Pure functions and command-query separation (10 min).** Define a pure function
(same input, same output, no observable side effects) and show why it's easier to test
and reason about than one that reads/writes shared state. Introduce command-query
separation: a method should either *do* something (a command, returns void/nothing
meaningful) or *answer* something (a query, no side effects) — never both. Show a
`getNextId()` that both increments and returns a counter as the classic violation.

**Avoiding null/boolean params; framework at the edges (10 min).** A boolean parameter
(`createUser(name, true)`) forces the reader to go find the signature to know what
`true` means — split into two named methods or an enum instead. Null parameters/returns
push a "did this work?" check onto every caller; prefer explicit types, defaults, or
(in richer type systems) option/result types. Then generalize: this is the same instinct
behind "framework code at the edges" — keep the database, web framework, and I/O calls
in a thin outer layer, and keep business logic in plain, framework-free functions/classes
that don't know or care how they're invoked.

**Tests, organizing by actor, refactoring habits (5 min).** Fast, independent tests are
what make refactoring safe — a test suite that takes 20 minutes or depends on shared
state won't get run before every commit, which means it won't catch regressions.
"Organizing by actor" (the Single Responsibility idea restated): a module should have
one reason to change, tied to one stakeholder/actor, not several unrelated ones bundled
together. Close with refactoring as a continuous habit — the "boy scout rule" (leave the
code a little cleaner than you found it) rather than a scheduled big-bang cleanup.

**Wrap-up (5 min).** Clean code rules are heuristics for a single goal: make change
cheap. Every rule this session covered exists to reduce the cost of the *next* change,
which is why it opens the curriculum — everything else assumes you can safely modify
code.

## Homework notes

### 1. Refactor a messy ~200-line script using clean-code rules only

**Goal:** Practice behavior-preserving refactoring — applying naming, decomposition, and
complexity-reduction rules to real (if small) code without changing what it does, and
being able to articulate *which* rule fixed *which* smell.

**Approach / hints:**
- Get (or supply) a working script full of typical smells: cryptic names, one giant
  function, deep nesting, boolean flags, mixed I/O and logic.
- Before touching anything, run/test it and capture its current behavior (sample
  inputs/outputs) so you can verify nothing changed afterward.
- Refactor in small steps, re-running after each change: rename first (cheapest, safest),
  then extract functions, then address complexity and boolean/null params last.
- Keep a running log as you go — one line per change, naming the smell and the rule
  applied — rather than trying to reconstruct it afterward from the diff.

**Definition of done:** A diff showing the messy script transformed with no behavior
change (same outputs for the same inputs), plus a short written note listing each
significant change and which clean-code rule motivated it.

### 2. Build a module under a hard rule: ≤15-line functions, no booleans, no "what" comments

**Goal:** Force internalization of decomposition and command-query habits by making the
easy way out (a long function, a boolean flag, a comment explaining confusing code)
unavailable.

**Approach / hints:**
- Pick a self-contained problem — a CSV parser or a receipt/total calculator work well
  because they naturally decompose into parse → validate → compute → format stages.
- Whenever a function wants to exceed 15 lines, that's the signal to extract a helper —
  treat the limit as a smell detector, not a bureaucratic constraint.
- Whenever you're tempted to add a boolean parameter, ask what the two behaviors really
  are and give them two names (two functions, or a small enum) instead.
- If you feel the urge to write a comment explaining *what* a line does, that's usually
  a sign the code itself needs a better name — save comments for *why* a non-obvious
  choice was made (e.g., "rounding down here to match the vendor's invoice format").

**Starter example (Python):**
```python
def parse_row(raw_line: str) -> dict:
    fields = raw_line.strip().split(",")
    return {"sku": fields[0], "qty": int(fields[1]), "price": float(fields[2])}

def line_total(item: dict) -> float:
    return item["qty"] * item["price"]

def parse_csv(text: str) -> list[dict]:
    lines = text.strip().splitlines()[1:]  # skip header
    return [parse_row(line) for line in lines]

# TODO: add validate_row(item) -> bool (no booleans passed IN, this returns one out)
# TODO: add format_receipt(items: list[dict]) -> str, each function still <= 15 lines
```

**Definition of done:** Every function is 15 lines or fewer, no function takes a boolean
parameter, and the only comments present explain a non-obvious *why* — none explain
*what* the following line does.

### 3. Pair-review: produce a clean-code report card

**Goal:** Practice reading and critiquing someone else's code against a fixed rubric —
the skill of *recognizing* a violation is different from (and necessary before) the
skill of fixing one.

**Approach / hints:**
- Exchange homework 1 or 2 with a classmate (or use a provided sample if pairing isn't
  available).
- Score against each rule from this session individually (naming, function size,
  complexity, boolean/null params, framework-at-the-edges, CQS) rather than giving one
  overall grade — a report card, not a verdict.
- For every deduction, cite a specific line or function name — "line 42, `getStatus()`
  mutates `self.status` internally, violating CQS" — not a vague "could be cleaner."
- Where possible, suggest the specific fix, not just the violation, so the report card
  is useful for revision.

**Definition of done:** A short written report scoring the reviewed submission against
each rule covered this session, with at least one specific line/function reference per
rule that was violated (or a note that the rule was satisfied).

## Further resources
- Free companion: MIT [6.005 Software Construction](https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/) · [blog.cleancoder.com](https://blog.cleancoder.com/)
