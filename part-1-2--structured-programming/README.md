# 2. Structured Programming

**Part 1 — Foundations of Code Quality** · [Back to curriculum index](../README.md)

## One-sentence pitch
Before there were classes or higher-order functions, there was a simpler discovery
that made programs provable and readable at all — that any algorithm can be built from
just three control-flow primitives, and that discipline is still what makes today's
code follow-able.

## Learning objectives
- Can name the three structured-programming primitives (sequence, selection, iteration)
  and explain why Böhm–Jacopini proved they're sufficient to express any computable
  algorithm.
- Can identify unstructured control flow (`goto`, multi-level jumps, flag-driven loops)
  in a piece of code and explain why it's hard to reason about.
- Can refactor jump-heavy or deeply nested code into single-entry/single-exit
  structured form without changing behavior.
- Can perform top-down decomposition: write a top-level algorithm as calls to
  not-yet-implemented stub procedures, then implement each procedure independently.
- Can decompose a long, flat, unstructured function into a set of well-named procedures
  using only structured constructs.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the `goto` era and why it ended | 5 min | Dijkstra's argument; what made old code unreadable |
| The three primitives | 10 min | Sequence, selection, iteration as a complete toolkit |
| Single-entry/single-exit | 10 min | Why one way in and one way out makes flow provable |
| Refactoring unstructured jumps | 10 min | Turning `goto`/flag-driven flow into structured form |
| Top-down decomposition | 10 min | Stubs first, then fill in; managing complexity by layering |
| Wrap-up / Q&A | 5 min | Structured programming as the ancestor of every later discipline |

**Hook: the `goto` era and why it ended (5 min).** Show a short snippet of `goto`-based
flow (or a modern equivalent — deeply nested `if`/`break`/`continue`/early-return
spaghetti) and ask students to trace what it does by hand. Reference Dijkstra's 1968
letter "Go To Statement Considered Harmful": the problem isn't `goto` as a keyword, it's
that unrestricted jumps make it impossible to reason locally about a program's state —
you can't know what's true at a given line without tracing every possible path that
could have arrived there.

**The three primitives (10 min).** Introduce sequence (do this, then that), selection
(`if`/`switch` — do one of these), and iteration (`while`/`for` — do this until done) as
the complete set. Mention the Böhm–Jacopini theorem: any flowchart-computable algorithm
can be rewritten using only these three, which is why every mainstream language builds
on exactly this set (possibly plus function calls) rather than raw jumps.

**Single-entry/single-exit (10 min).** A structured block has exactly one way in and,
traditionally, one way out. Show how this composability is what lets you treat a whole
block as a black box when reading the code around it — you don't need to check whether
control secretly left in the middle. Discuss the modern nuance: many teams relax
single-exit for early guard-clause returns at the *top* of a function (a readability
win), while still avoiding jumps *out of the middle* of a block — draw the line clearly
so students don't over-apply the rule.

**Refactoring unstructured jumps (10 min).** Live-refactor a flag-driven loop (a
`found = False` variable checked at multiple points, or a labeled `break` reaching out
of nested loops) into structured form — usually by extracting the inner logic into a
function that can simply `return`, replacing the jump with a normal function exit.
Show the same technique applied to a `goto`-based error-cleanup pattern, translating it
into structured exception handling or a guard-clause chain.

**Top-down decomposition (10 min).** Demonstrate writing the top level of a program
first, purely as calls to procedures that don't exist yet (stubs that return dummy
values or `pass`), so the overall shape and control flow is validated before any detail
is filled in. Then implement each stub in isolation, one at a time, re-running the
top-level flow as each piece becomes real. This is the practical technique for managing
complexity: never hold the whole problem in your head at once.

**Wrap-up (5 min).** Structured programming looks basic today because it won — every
mainstream language enforces it by default. But the underlying discipline (local
reasoning, one way in/out, decompose top-down) is the direct ancestor of small
functions and single-responsibility design later in this course.

## Homework notes

### 1. Refactor jump-heavy/tangled control flow into pure structured constructs

**Goal:** Recognize why unstructured jumps make code hard to trace, and practice
converting them into sequence/selection/iteration only, with single-entry/single-exit.

**Approach / hints:**
- Start from (or write) code with tangled flow: a `goto`-based example if your language
  supports it, or a realistic equivalent — nested loops with multiple flag variables and
  early `break`/`continue` scattered across several levels.
- Trace all the ways control can currently leave each block before changing anything;
  write them down so you can verify the refactor preserves every path's behavior.
- Replace flags with early returns from extracted functions, and replace jumps-into-the-
  middle with restructured conditionals that reach the same outcome through normal flow.
- Re-test after each small change rather than rewriting the whole thing at once.

**Starter example (Python):**
```python
# Before: flag-driven, jump-heavy
def find_first_valid(items):
    found = False
    result = None
    i = 0
    while i < len(items) and not found:
        if items[i] is not None:
            if items[i] > 0:
                result = items[i]
                found = True
        i += 1
    return result

# TODO: refactor to single-entry/single-exit structured form —
# hint: a for-loop with a single early return needs no flag at all.
```

**Definition of done:** The refactored code uses only sequence, selection, and
iteration (no `goto`, no multi-level jumps, no flag variables standing in for control
flow), has a single entry and single exit per block, and produces identical output to
the original for the same inputs.

### 2. Solve a problem via top-down decomposition with stubs

**Goal:** Practice designing the shape of a solution before its details — writing the
top-level algorithm as calls to procedures that don't exist yet, then filling each one
in independently.

**Approach / hints:**
- Pick a problem with natural stages, such as a menu-driven program (display menu → read
  choice → dispatch to an action → repeat) or a simple state machine (traffic light,
  vending machine).
- Write the top-level function first, calling procedures like `show_menu()`,
  `read_choice()`, `handle_choice(choice)` before any of them are implemented — have
  each stub return a hardcoded value or do nothing, and confirm the top-level flow runs.
- Implement each stub one at a time, re-running the top level after each so you always
  have a working (if incomplete) program.
- Resist the urge to implement everything before testing the outer flow — the whole
  point of the exercise is validating structure before detail.

**Starter example (Python):**
```python
def show_menu() -> None:
    print("1) Add  2) List  3) Quit")

def read_choice() -> str:
    return input("> ")  # TODO: validate input

def handle_choice(choice: str, items: list) -> bool:
    # TODO: implement each branch; return False to signal "quit"
    return choice != "3"

def main() -> None:
    items = []
    running = True
    while running:
        show_menu()
        choice = read_choice()
        running = handle_choice(choice, items)
```

**Definition of done:** The top-level control flow was written and validated (even with
stub procedures) before any procedure's internals were implemented, every procedure was
then implemented independently, and the finished program uses only structured
constructs.

### 3. Decompose one long, flat, unstructured function into named procedures

**Goal:** Practice extracting sub-procedures from an inline block of logic without
changing behavior — the structured-programming precursor to "small functions" in
Topic 1.

**Approach / hints:**
- Take (or write) a single long function that does everything inline — no helper
  procedures — covering several logical stages (e.g., read input, validate, compute,
  print results, all in one block).
- Identify natural boundaries between stages first (comment them, if it helps), then
  extract each stage into its own well-named procedure taking explicit parameters.
- Keep every extracted procedure using only sequence, selection, and iteration — this
  exercise is about decomposition, not about introducing other paradigms yet.
- Verify behavior is unchanged by comparing output on the same inputs before and after.

**Definition of done:** The original single function is replaced by a set of clearly
named procedures, each handling one stage of the original logic, called from a short
top-level function; output for identical inputs is unchanged.

## Further resources
- Free companion: Harvard [CS50x](https://cs50.harvard.edu/x/)
