# 3. Functional Programming

**Part 1 — Foundations of Code Quality** · [Back to curriculum index](../README.md)

## One-sentence pitch
A function that always returns the same output for the same input, and touches nothing
outside itself, is a function you can test, reason about, and run in parallel without
fear — and that single idea (purity) is the engine behind most of what makes functional
code easier to trust.

## Learning objectives
- Can write a pure function and identify why a given function is *not* pure (hidden
  input via shared state, hidden output via a side effect).
- Can use `map`, `filter`, and `reduce` to replace an equivalent hand-written loop, and
  explain when a loop is still the clearer choice.
- Can compose small functions together (via `compose`/`pipe`) into a pipeline and
  explain how this differs from writing one large function.
- Can explain referential transparency and use it to justify safely reordering or
  memoizing a call.
- Can rewrite a function that mutates shared state and produces side effects mid-logic
  into a pure function plus an isolated side-effecting shell.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the bug that only happens sometimes | 5 min | Shared mutable state and why it's hard to debug |
| Pure functions and referential transparency | 10 min | Definition, examples, non-examples |
| Immutability | 10 min | Why "no mutation" simplifies reasoning; copy-on-write patterns |
| First-class/higher-order functions and composition | 10 min | Functions as values; building pipelines |
| map/filter/reduce | 10 min | Replacing loops with declarative transforms |
| Recursion over iteration; avoiding shared mutable state | 5 min | When recursion reads better; pushing state to the edges |
| Wrap-up / Q&A | 5 min | Functional core / imperative shell as the practical takeaway |

**Hook: the bug that only happens sometimes (5 min).** Present a bug caused by shared
mutable state — two functions both reading and writing a shared list or global counter,
producing different results depending on call order. Ask: what would it take to make
this bug *impossible*, not just harder to trigger? The answer functional programming
gives is: don't share mutable state in the first place.

**Pure functions and referential transparency (10 min).** Define a pure function:
given the same inputs, always returns the same output, and has no observable side
effects (no I/O, no mutation of anything outside its own scope). Referential
transparency is the consequence: a call to a pure function can be replaced by its
result value anywhere it appears, without changing the program's behavior — which is
what makes memoization, reordering, and parallel execution safe. Contrast with an
impure function reading a global or writing to a file mid-computation.

**Immutability (10 min).** Once data can't change after creation, a huge class of bugs
(a caller mutating an object another part of the code still holds a reference to)
becomes structurally impossible. Show updating a record by producing a new copy with
one field changed, rather than mutating in place, and discuss the trade-off (allocation
cost vs. safety) briefly and honestly rather than presenting immutability as free.

**First-class/higher-order functions and composition (10 min).** Functions as values:
they can be passed as arguments, returned from other functions, and stored in
variables/data structures. A higher-order function takes and/or returns functions.
Build a tiny `compose(f, g)` (or `pipe`) and show assembling `validate`, `transform`,
and `format` into a single pipeline function, each stage independently testable and
swappable.

**map/filter/reduce (10 min).** Reframe common loops as declarative transforms:
`map` (transform each element), `filter` (keep some elements), `reduce` (fold into one
value). Live-convert an imperative loop that builds a filtered, transformed list with a
running accumulator into a `map`/`filter`/`reduce` chain. Be honest that not every loop
becomes clearer this way — a loop with multiple side effects or complex early exits may
stay a loop, and that's a legitimate judgment call, not a failure.

**Recursion over iteration; avoiding shared mutable state (5 min).** Show a small
example (e.g., summing a list, tree traversal) where recursion expresses the structure
of the problem more directly than a loop with manual index/accumulator bookkeeping.
Recap the throughline of the whole session: every technique covered — purity,
immutability, composition, declarative transforms, recursion — is in service of one
goal, avoiding shared mutable state.

**Wrap-up (5 min).** Introduce the "functional core, imperative shell" idea as the
practical takeaway most developers actually use: keep decision-making logic pure and
push I/O/mutation to a thin outer layer. This previews Topic 5 (Programming Paradigms),
where students will build exactly this kind of hybrid deliberately.

## Homework notes

### 1. Process orders into a summary report with pure functions and map/filter/reduce only

**Goal:** Practice building a real (if small) data pipeline without loops or mutation —
forcing the map/filter/reduce/compose muscle rather than falling back on imperative
habits.

**Approach / hints:**
- Model orders as immutable records (a frozen dataclass, a `readonly`-typed object, or
  plain tuples/dicts you never mutate in place).
- Break the task into named pure stages — filter to relevant orders, map to the fields
  you need, reduce to totals/groupings — rather than one function doing everything.
- If you need a running total per category, `reduce` into a dictionary, building a new
  dictionary each step rather than mutating one in place.
- No `for`/`while` loops and no reassigning a variable after its initial binding — if
  you reach for either, there's a `map`/`filter`/`reduce` (or a small helper function)
  that does the same job.

**Starter example (Python):**
```python
from dataclasses import dataclass
from functools import reduce

@dataclass(frozen=True)
class Order:
    customer: str
    amount: float
    category: str

def total_by_category(orders: list[Order]) -> dict[str, float]:
    return reduce(
        lambda acc, o: {**acc, o.category: acc.get(o.category, 0) + o.amount},
        orders,
        {},
    )

# TODO: add a pure `large_orders(orders, threshold)` using filter,
# and a pure `summary_lines(totals)` using map — no loops, no mutation.
```

**Definition of done:** The program produces the summary report using only pure
functions, immutable data, and `map`/`filter`/`reduce` (or equivalent comprehensions
used declaratively) — no `for`/`while` loops and no in-place mutation anywhere in the
pipeline.

### 2. Refactor an impure, side-effecting function into a pure function plus an edge shell

**Goal:** Practice the single most transferable functional-programming skill: pulling
side effects and shared-state mutation *out* of decision-making logic, leaving a pure
core that's trivial to test.

**Approach / hints:**
- Start from (or write) a function that reads/writes a shared variable, logs or prints
  mid-computation, and returns a result — all tangled together.
- Identify which parts are actually *decisions* (pure logic) vs. which parts are
  *effects* (I/O, mutation, logging) — list them separately before writing any code.
- Rewrite the decision-making part as a pure function that takes all its inputs as
  parameters and returns a result (and/or a description of what effect *should* happen)
  with no side effects of its own.
- Move the actual I/O/mutation into a thin caller that invokes the pure function and
  then performs the effect based on its return value.

**Starter example (TypeScript):**
```typescript
// Before: impure — mutates `inventory`, logs mid-logic, returns a result
function reserveItem(inventory: Record<string, number>, sku: string, qty: number): boolean {
  if (inventory[sku] < qty) {
    console.log(`insufficient stock for ${sku}`);
    return false;
  }
  inventory[sku] -= qty; // mutation!
  console.log(`reserved ${qty} of ${sku}`);
  return true;
}

// After — TODO: write a pure `canReserve`/`applyReservation` pair that takes
// inventory as input and returns a new inventory + outcome, with logging
// and the actual state update left to the caller.
```

**Definition of done:** The core decision-making logic is a pure function (no
mutation, no I/O, deterministic output for a given input) with its own tests that need
no mocking; a separate thin function/shell performs the actual side effect based on the
pure function's result.

### 3. Build `compose`/`pipe` utilities and assemble a validate → transform → format pipeline

**Goal:** Practice function composition as a design tool — building a pipeline out of
small, independently testable functions rather than one monolithic function.

**Approach / hints:**
- Write `compose(...fns)` (right-to-left, math convention) or `pipe(...fns)`
  (left-to-right, reads like a sentence) — pick one and be consistent.
- Write `validate`, `transform`, and `format` as three separate, independently testable
  single-argument functions with matching input/output types so they can chain.
- Assemble the pipeline once with `pipe(validate, transform, format)` and confirm each
  stage can still be unit-tested in isolation, not just as part of the whole chain.
- Consider what happens when `validate` needs to short-circuit (e.g., return an error) —
  this is a natural place to discuss `Result`/`Either`-style types if your language
  supports them well, without requiring a full implementation.

**Starter example (TypeScript):**
```typescript
type Fn<A, B> = (a: A) => B;

function pipe<A, B, C>(f: Fn<A, B>, g: Fn<B, C>): Fn<A, C> {
  return (a: A) => g(f(a));
}

const validate = (input: string): string => input.trim();
const transform = (input: string): number => Number(input);
// TODO: add `format` (number -> string) and chain all three with pipe(),
// then extend pipe() to accept more than two functions via reduce.
```

**Definition of done:** A working `compose`/`pipe` utility exists and is used to
assemble at least a three-stage pipeline out of small named functions, each of which
has its own passing unit test independent of the pipeline.

## Further resources
- Free companion: MIT, [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) (SICP, full free text)
