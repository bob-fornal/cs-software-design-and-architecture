# 6. Core Design Principles

**Part 2 — Design Principles & Patterns** · [Back to curriculum index](../../README.md)

## One-sentence pitch
Before you can apply SOLID or reach for a design pattern, you need the handful of
underlying instincts — favor composition, hide what changes, talk to objects instead
of interrogating them — that make those later tools make sense.

## Learning objectives
- Can identify when an inheritance hierarchy is being used to model *variation* (rather
  than a true is-a relationship) and refactor it into composition/strategy objects.
- Can name the piece of a design that is "what varies" and wrap it behind a stable
  interface so the rest of the system doesn't need to change when it does.
- Can rewrite code that programs against a concrete class to instead depend on an
  abstraction (interface/protocol/abstract base class).
- Can spot and fix a Law of Demeter violation (a "chain of dots" reaching through
  multiple objects) and a Tell-Don't-Ask violation (pulling data out to make an
  external decision instead of asking the object to act).
- Can explain the Hollywood Principle ("don't call us, we'll call you") and give an
  example of inversion of control that isn't full Dependency Injection.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the duck problem | 5 min | Why inheritance-for-variation breaks down |
| Primary principles + paradigm features recap | 10 min | Naming the toolkit; how OOP features (encapsulation, polymorphism, interfaces) are the *mechanism* these principles exploit |
| Encapsulate what varies / Program to an abstraction | 10 min | Isolating change; depending on interfaces, not concretions |
| The Hollywood Principle | 5 min | Inversion of control, framework vs. library |
| Law of Demeter | 10 min | "Only talk to your immediate friends"; the dot-chain smell |
| Tell, Don't Ask | 5 min | Moving decisions into the object that owns the data |
| Wrap-up / Q&A | 5 min | Tying all six back to "manage coupling" |

**Hook: the duck problem (5 min).** Open with the classic *Head First Design Patterns*
scenario: a `Duck` base class with a `fly()` method. Add `RubberDuck` — it can't fly, so
you override `fly()` to throw, or you return early and do nothing. Add `DecoyDuck` —
same problem. The hierarchy is now lying about what a `Duck` can do, and every new
duck variant risks breaking a `fly()` call written against the base class (this is a preview
of the Liskov Substitution Principle in Topic 7). The bug isn't bad naming — it's using
inheritance to express "this subtype behaves differently," which is a job for
composition, not `extends`.

**Primary principles + paradigm features recap (10 min).** Name the six principles this
session covers as the connective tissue between "OOP has interfaces and polymorphism"
(Topic 4) and "here is a named pattern" (Topic 9). Composition over inheritance,
encapsulate what varies, program against abstractions, the Hollywood Principle, Law of
Demeter, and Tell Don't Ask are not patterns themselves — they're the *judgment calls*
that make you reach for a pattern in the first place. Remind students that the paradigm
features they already have (interfaces, polymorphism, dynamic dispatch) are the raw
material; these principles are the discipline for using that material well.

**Encapsulate what varies / Program against abstractions (10 min).** Walk through
identifying the axis of change in the duck example (behavior, not species) and pulling
it out into a `FlyBehavior` interface with concrete implementations
(`FlyWithWings`, `FlyNoWay`). Each `Duck` now *has a* `FlyBehavior` instead of
*being a* flying or non-flying duck — composition over inheritance in practice. Connect
this directly to "program against abstractions": the `Duck` class depends on the
`FlyBehavior` interface, never on a concrete implementation, so new behaviors can be
added without touching `Duck`.

**The Hollywood Principle (5 min).** "Don't call us, we'll call you" — high-level
components define the extension points, and low-level/plugin code fills them in
without the plugin ever needing to call back into the framework directly. Contrast a
library (your code calls it) with a framework (it calls your code) as the cleanest
everyday example. This is inversion of control in its simplest form, and it sets up
Dependency Inversion in Topic 7.

**Law of Demeter (10 min).** State the rule: an object should only talk to its
"immediate friends" — itself, its parameters, objects it creates, its direct
components — not objects it reaches by chaining through another object
(`a.getB().getC().doThing()`). Show why this is fragile: it couples the caller to the
entire chain's internal structure, and any link changing shape breaks every caller.
Live-refactor a chain into a method on the first object that hides the traversal.

**Tell, Don't Ask (5 min).** The companion habit to Demeter: instead of pulling data
out of an object with getters to make a decision *externally*, ask the object to make
the decision and act, using the data it already owns. Show a `if (account.getBalance()
< amount) { ... }` caller turning into `account.withdraw(amount)` with the balance
check and the mutation both living inside `Account`.

**Wrap-up (5 min).** All six threads pull one direction: minimize how much one part of
a system needs to know about another part's internals. That's the throughline into
SOLID and GoF patterns next.

## Homework notes

### 1. Refactor a Duck-style inheritance hierarchy into composition

**Goal:** Recognize inheritance used to model *behavioral variation* rather than a
true type hierarchy, and know the standard fix — extract the varying behavior into an
interface/strategy object the class holds a reference to.

**Approach / hints:**
- Start from (or write) a `Duck` base class with subclasses like `FlyingDuck` and
  `RubberDuck`, where `RubberDuck.fly()` either throws or silently does nothing.
- Identify the axis of variation (flying behavior — and consider quacking behavior too,
  for a second axis) and extract it into its own interface with 2+ implementations.
- Give `Duck` a field of that interface type, set at construction (or via a setter for
  runtime behavior changes), and delegate to it instead of overriding.
- Verify: adding a new duck type that flies normally but quacks silently should require
  zero changes to existing duck classes — only a new `Duck` instantiation with a
  different behavior combination.

**Starter example:**
```python
from abc import ABC, abstractmethod

class FlyBehavior(ABC):
    @abstractmethod
    def fly(self) -> str: ...

class FlyWithWings(FlyBehavior):
    def fly(self) -> str:
        return "I'm flying!"

class FlyNoWay(FlyBehavior):
    def fly(self) -> str:
        return "I can't fly."

class Duck:
    def __init__(self, fly_behavior: FlyBehavior):
        self._fly_behavior = fly_behavior

    def perform_fly(self) -> str:
        return self._fly_behavior.fly()

# TODO: add QuackBehavior the same way, then build RubberDuck / MallardDuck
# as Duck instances configured with the right behavior objects — no subclassing.
```

**Definition of done:** No subclass overrides a behavior method to throw or no-op; the
varying behavior lives in its own interface with at least two implementations; a new
behavior combination can be added by composing existing pieces without editing the
`Duck` class.

### 2. Fix a Law of Demeter / Tell-Don't-Ask violation

**Goal:** Recognize when calling code is reaching through an object graph to gather
data instead of delegating the decision to the object that owns the data.

**Approach / hints:**
- Find (or write) code with a chain like `order.getCustomer().getAccount().charge(amt)`
  or a block that calls several getters (`getStatus()`, `getBalance()`, `getItems()`)
  purely to decide what to do next from outside the object.
- For the Demeter fix: add a method on the first object (`order.chargeCustomer(amt)`)
  that internally does the traversal — callers no longer need to know the chain exists.
- For the Tell-Don't-Ask fix: move the conditional logic that used the getters *inside*
  the object being queried, and expose a single intention-revealing method instead
  (e.g., `cart.checkout()` instead of checking `cart.getItems().isEmpty()` externally).
- Write a short before/after comparing what each caller needed to know about internal
  structure.

**Starter example (TypeScript):**
```typescript
// Before — violates both LoD and Tell-Don't-Ask
if (order.getCustomer().getAccount().getBalance() < order.getTotal()) {
  throw new Error("insufficient funds");
}
order.getCustomer().getAccount().charge(order.getTotal());

// After — TODO: implement chargeFor() on Order (delegates to Customer/Account
// internally) so the caller only ever talks to `order`.
order.chargeFor(order.getTotal());
```

**Definition of done:** No calling code chains through more than one level of object
to reach data or behavior; decisions that depend on an object's internal state are made
by a method on that object, not by external code that first extracted the state.

## Further resources
- Free companion: [DeviQ — Principles](https://deviq.com/principles/)
