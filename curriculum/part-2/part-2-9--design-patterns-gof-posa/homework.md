# Homework notes — Design Patterns (GoF & PoSA)

[Back to topic index](README.md) · [Back to curriculum index](../../../README.md)

## 1. Implement 3 GoF patterns from different categories, in realistic scenarios

**Goal:** Practice recognizing which pattern fits a *real* problem shape (not the
textbook example everyone has memorized), and articulate what the code would look
like — and what would go wrong — without the pattern.

**Approach / hints:**
- Pick one pattern each from creational, structural, and behavioral (e.g., Factory
  Method, Decorator, Observer — or substitute any other three from different
  categories covered in [outline.md](outline.md)).
- Ground each in a scenario that isn't "shapes" or "animals" — e.g., Decorator for
  stacking middleware/request-processing behavior (logging, auth, rate-limiting) around
  a base HTTP handler; Factory Method for creating the right parser given a file
  extension; Observer for a stock-price ticker updating multiple independent displays.
- For each, write a short "without this pattern" note: what would the code look like
  if you'd solved it with an `if`/`switch` or a hardcoded call list instead, and what
  specifically breaks or gets harder as requirements grow (this is the same "what
  problem did it solve" habit as the design review in Topic 7's homework).
- Keep each implementation small — 30–60 lines is plenty to demonstrate the pattern
  clearly; the point is applying the pattern to something plausible, not building a
  production system.

**Starter shape (illustrative, not prescriptive):**
```typescript
// Decorator example shape — stacking request-handling behavior
interface Handler { handle(req: Request): Response; }

class BaseHandler implements Handler {
  handle(req: Request): Response { /* core logic */ return coreResponse(req); }
}

class LoggingHandler implements Handler {
  constructor(private inner: Handler) {}
  handle(req: Request): Response {
    console.log(`-> ${req.path}`);
    const res = this.inner.handle(req);
    console.log(`<- ${res.status}`);
    return res;
  }
}
// TODO: add AuthHandler, RateLimitHandler the same way, then compose:
// new LoggingHandler(new AuthHandler(new BaseHandler()))
```

**Definition of done:** Three working implementations, each from a different GoF
category, each in a distinct realistic scenario (not the same textbook example
restated); each accompanied by a short written note on the problem it solved and what
the code would look like without it.

## 2. Refactor conditional dispatch into Strategy, and coupled notification into Observer

**Goal:** Practice the two most common real-world entry points into GoF patterns:
replacing a growing `switch`/`if-else` with Strategy, and replacing a hardcoded list
of "everyone who needs to know" with Observer.

**Approach / hints:**
- Starter "before" code for both parts is in
  [`examples/homework2_before.py`](examples/homework2_before.py) — translate it to
  your language of choice if you'd rather not use Python.
- **Strategy refactor:** define an interface with one method (e.g.,
  `cost(weight_kg, distance_km)`), implement one class per existing branch, and replace
  the dispatch function with a registry keyed by the same strings the `switch` used.
  Confirm: adding "international" shipping requires only a new class and one
  registration line.
- **Observer refactor:** turn the class making inline calls into a subject that
  maintains a list of observers and calls a single `notify()`-style method on each;
  turn each previously-hardcoded client into an observer implementation. Confirm:
  adding a fifth interested party requires only registering a new observer, with zero
  changes to the method that used to call everyone directly.
- Write a short before/after note for each: what had to change to add a new
  case/observer, before vs. after.

**Definition of done:** Both refactors compile/run and produce the same external
behavior as the originals; adding one new shipping method and one new order observer
each requires adding a class/registration only, with no edits to existing dispatch or
notification logic.

## 3. Implement a PoSA concurrency pattern in a toy task processor

**Goal:** Move beyond single-threaded object design into concurrency-oriented pattern
thinking — recognize that "how do I structure concurrent work" is its own catalog of
named, reusable solutions, not something to improvise from scratch each time.

**Approach / hints:**
- A starter skeleton for a Half-Sync/Half-Async task processor is in
  [`examples/posa_starter.py`](examples/posa_starter.py) (Python `threading` +
  `queue`); an `asyncio`-based version, or a Leader/Followers or Active Object
  implementation instead, is equally acceptable — pick whichever your background makes
  most natural.
- The required structural elements, whichever pattern you pick: a boundary between an
  "accept work" side that never blocks and a "do work" side that processes
  sequentially; and a clear hand-off mechanism between them (a queue, a promoted
  leader thread, or a per-object request queue for Active Object).
- Demonstrate it under load: submit tasks faster than they can be processed and show
  the hand-off mechanism doing its job (queue backing up, a leader being promoted,
  etc.) rather than the producer blocking or work being dropped silently.
- Write a short note on why this pattern (vs. naive thread-per-request or a single
  blocking loop) helps at the concurrency level this toy example demonstrates.

**Definition of done:** A working toy processor implementing one named PoSA
concurrency pattern, demonstrated under a bursty/overloaded workload, with a short
written explanation of the hand-off mechanism and why it helps versus the naive
alternative.
