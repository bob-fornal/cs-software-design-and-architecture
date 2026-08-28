# Session outline — Design Patterns (GoF & PoSA)

[Back to topic index](README.md) · [Back to curriculum index](../../README.md)

~55 minutes.

| Segment | Time | Content |
|---|---|---|
| Hook: you've already written these | 5 min | Patterns as names for things you've built ad hoc |
| Creational patterns | 10 min | Factory Method, Abstract Factory, Builder, Singleton |
| Structural patterns | 10 min | Decorator, Adapter, Facade, Composite |
| Behavioral patterns | 12 min | Strategy, Observer, Command, Template Method |
| PoSA: concurrency & distributed patterns | 12 min | Half-Sync/Half-Async, Leader/Followers, Active Object |
| Wrap-up: pattern as a smell too | 6 min | When a pattern adds indirection nobody needs |

## Hook: you've already written these (5 min)

Ask the class: has anyone written a class that swaps its behavior based on a
constructor argument? Congratulations, that's Strategy. Written a list of callbacks
that all get invoked on some event? That's Observer. The Gang of Four catalog isn't a
list of clever tricks to memorize — it's a vocabulary for patterns that show up
naturally once you're following composition-over-inheritance and program-to-an-
abstraction (Topic 6) consistently. Learning the names matters because "let's use
Strategy here" communicates a whole design in three words to another engineer who
knows the catalog.

## Creational patterns (10 min)

Creational patterns manage *how objects get constructed* so calling code doesn't need
to know concrete classes.

- **Factory Method** — a method (often overridden by subclasses, or parameterized by a
  type key) that returns an object implementing some interface, so the caller depends
  only on the interface. Directly enables Open/Closed (Topic 7): add a new product
  type by adding a class the factory knows about, not by editing callers.
- **Abstract Factory** — a factory that produces a *family* of related objects (e.g., a
  `UIFactory` that produces matching `Button`, `Checkbox`, and `Scrollbar` for a given
  theme), guaranteeing the family stays consistent.
- **Builder** — separates constructing a complex object step-by-step from the object's
  final representation, useful when a constructor would otherwise need many optional
  parameters.
- **Singleton** — restricts a class to one instance, globally accessible. Flag this one
  as controversial: it's really global mutable state with a design-pattern name, and it
  makes testing harder (hidden dependency, hard to substitute a fake). Mention it
  because it's common, not because it's usually the right choice.

## Structural patterns (10 min)

Structural patterns compose classes/objects into larger structures while keeping them
flexible.

- **Decorator** — wraps an object in another object implementing the same interface,
  adding behavior before/after delegating to the wrapped object. Contrast with
  inheritance: any combination of decorators can be stacked at runtime, where
  subclassing would need a new class per combination (`LoggingAndCachingService`,
  `CachingAndLoggingService`, ...).
- **Adapter** — converts one interface into another the client expects, typically to
  make an existing/third-party class fit an interface it wasn't written for.
- **Facade** — a simplified, higher-level interface over a complex subsystem, hiding
  its internals from most callers without removing access for callers that need detail.
- **Composite** — treats individual objects and groups of objects uniformly through a
  shared interface (classic example: files and folders, both are "FileSystemEntry"
  with a `size()` method).

## Behavioral patterns (12 min)

Behavioral patterns manage how objects communicate and distribute responsibility for
an algorithm or a chain of reactions.

- **Strategy** — encapsulates an interchangeable algorithm/behavior behind a common
  interface, selected and injected at runtime. This is the fix for the duck example in
  Topic 6 and for `switch`-based dispatch in homework 2 below.
- **Observer** — a subject maintains a list of dependents (observers) and notifies them
  automatically when its state changes, so the subject doesn't need to know what its
  observers do with that notification. This is the fix for tightly-coupled "call every
  interested party inline" code.
- **Command** — encapsulates a request (and its parameters) as an object, enabling
  queuing, logging, undo/redo, and decoupling the invoker from the receiver.
- **Template Method** — defines the skeleton of an algorithm in a base class, deferring
  specific steps to subclasses that override just those steps — useful, but watch for
  it becoming an LSP trap (Topic 7) if subclasses can't honor every step's contract.

## PoSA: concurrency & distributed patterns (12 min)

*Patterns of Software Architecture* (POSA2 specifically) catalogs patterns for
concurrent and networked systems — a level up from GoF's single-threaded object
design.

- **Half-Sync/Half-Async** — splits a system into a synchronous layer (simple,
  sequential application logic) and an asynchronous layer (I/O, event handling), joined
  by a queue. Lets application code stay simple while I/O stays non-blocking.
- **Leader/Followers** — a pool of threads takes turns being the "leader" that waits on
  the shared event source; when an event arrives, that thread promotes a follower to
  leader before processing the event itself, avoiding the hand-off overhead of a
  work-queue design.
- **Active Object** — decouples method invocation from method execution: a call
  becomes a request queued for execution on the object's own thread, so a caller never
  blocks on the object's internal work directly.
- **Reactor** (mention briefly if time allows) — a single thread demultiplexes and
  dispatches I/O events to registered handlers; the conceptual basis for event loops
  like Node.js's or Python's `asyncio`.

Emphasize: these patterns exist because thread-per-request doesn't scale and callback
spaghetti isn't maintainable — they're structured ways to keep concurrent code
reasoned-about, the same job GoF patterns do for single-threaded object design.

## Wrap-up: pattern as a smell too (6 min)

Close with a caution tying back to YAGNI (Topic 8): a pattern applied where the
variation it handles doesn't actually exist is *speculative generality wearing a
recognizable name* — an Observer with exactly one observer that will only ever have
one observer is unnecessary indirection. The skill isn't "use patterns," it's
"recognize the shape of the problem a pattern solves, and only reach for it when that
shape is actually present."
