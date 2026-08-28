# 4. Object-Oriented Programming

**Part 1 — Foundations of Code Quality** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Objects that bundle data with the behavior that acts on it, hidden behind a stable
interface, let a codebase grow by adding new kinds of things instead of adding new
`if` branches everywhere an old kind of thing is checked.

## Learning objectives
- Can design a class hierarchy that uses encapsulation correctly (private state, a
  deliberate public interface) rather than exposing internals through getters/setters.
- Can distinguish a true is-a inheritance relationship from a case where inheritance is
  being misused to model variation, and can use polymorphism through an interface or
  abstract class to let calling code treat different concrete types uniformly.
- Can explain the difference between an abstract class (partial implementation, shared
  state) and an interface (a pure contract), and choose correctly between them.
- Can identify an anemic domain model (data-only classes plus separate service classes)
  and refactor it into a rich domain model where behavior lives with its data.
- Can design a simple layered architecture (presentation → domain → data) and explain
  which direction dependencies should point between layers.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Hook: two ways to add a new payment type | 5 min | Branching logic vs. a new class |
| Encapsulation and abstraction | 10 min | Hiding state; designing a deliberate interface |
| Inheritance and polymorphism | 10 min | True is-a relationships; substitutability |
| Interfaces, abstract vs. concrete classes | 10 min | Contracts vs. partial implementations; scope/visibility |
| Domain models vs. anemic models; domain language | 10 min | Where behavior should live; naming things the way the business does |
| Class variants and layered architectures | 5 min | Modeling type families; presentation/domain/data |
| Wrap-up / Q&A | 5 min | OOP features as raw material for Topics 6–9 |

**Hook: two ways to add a new payment type (5 min).** Show a `processPayment(type,
amount)` function with a `switch` on `type` that grows a new branch every time a
payment method is added. Contrast with a `PaymentMethod` interface and one new class
per payment type. The branching version means every new type touches existing code
(risk of breaking what already works); the OOP version means every new type is purely
additive. This tension — modify existing code vs. add new code — is the thread the
whole session pulls on, and it resurfaces explicitly as the Open/Closed Principle in
Topic 7.

**Encapsulation and abstraction (10 min).** Encapsulation: bundle data with the
operations that use it, and hide the data behind a deliberate public interface rather
than exposing raw fields. Warn against the "getter/setter for every field" anti-pattern
— that's encapsulation in name only, since it exposes exactly as much as public fields
would. Abstraction: expose *what* an object does, not *how* — callers of a `Stack`
shouldn't need to know whether it's backed by an array or a linked list.

**Inheritance and polymorphism (10 min).** Inheritance should model a genuine is-a
relationship where the subtype can be used anywhere the supertype is expected (this
previews Liskov Substitution in Topic 7) — revisit the Topic 6 duck example briefly as
the cautionary counter-case. Polymorphism: code written against a base type/interface
works unmodified with any conforming subtype, which is the mechanism that makes
"add a new class instead of a new branch" possible from the hook.

**Interfaces, abstract vs. concrete classes; scope/visibility (10 min).** An interface
is a pure contract — method signatures, no implementation, no state. An abstract class
can provide partial implementation and shared state, but can't be instantiated
directly; a concrete class can be instantiated and must fill in any abstract members.
Give a rule of thumb: prefer an interface when unrelated classes need to share a
capability, prefer an abstract class when related classes share actual implementation.
Cover scope/visibility (public/private/protected) as the mechanical tool that enforces
encapsulation.

**Domain models vs. anemic models; domain language (10 min).** An anemic domain model
is data classes (getters/setters, no logic) plus separate "service" classes doing all
the behavior — it looks object-oriented but behaves procedurally, and Martin Fowler's
critique is required framing here. A rich domain model puts behavior on the object that
owns the relevant data: `order.cancel()` instead of `OrderService.cancel(order)`.
Introduce domain language / ubiquitous language briefly: class and method names should
match the vocabulary domain experts actually use, not generic technical terms — this
sets up Domain-Driven Design in Topic 12.

**Class variants and layered architectures (5 min).** Class variants: modeling a family
of related types (e.g., payment methods, vehicle types) as a hierarchy or set of
implementations of a shared interface, each variant substitutable for the others.
Layered architecture preview: presentation (UI/API) → domain (business logic, the rich
objects just discussed) → data (persistence) — objects in an outer layer depend on
inner layers, never the reverse.

**Wrap-up (5 min).** Everything in this session — encapsulation, polymorphism,
interfaces — is raw material, not a finished discipline. Topics 6 through 9 (design
principles, SOLID, patterns) are all about *how* to use these features well; today was
about knowing what the features are and how to use them correctly at all.

## Homework notes

### 1. Model a domain with a proper class hierarchy

**Goal:** Practice designing encapsulation, inheritance, and polymorphism together in a
single coherent model, including choosing correctly between an abstract class and an
interface.

**Approach / hints:**
- Pick a domain with natural variation — a library (books, media, members with
  different borrowing rules), a parking garage (vehicle types, spot types), or a board
  game (piece types, player types).
- Identify the true is-a relationships first (candidates for an abstract base class with
  shared implementation) separately from the pure capabilities (candidates for
  interfaces — e.g., `Payable`, `Reservable`).
- Require at least one abstract class (partial implementation shared by subclasses) and
  two interfaces (pure contracts implemented by otherwise-unrelated classes).
- Keep all mutable state private; every external interaction should go through
  deliberately designed public methods, not raw field access.

**Starter example (Python):**
```python
from abc import ABC, abstractmethod

class LibraryItem(ABC):
    def __init__(self, title: str):
        self._title = title
        self._checked_out = False

    @abstractmethod
    def loan_period_days(self) -> int: ...

    def check_out(self) -> None:
        if self._checked_out:
            raise ValueError(f"{self._title} is already checked out")
        self._checked_out = True

class Book(LibraryItem):
    def loan_period_days(self) -> int:
        return 21

# TODO: add a second LibraryItem subclass (e.g., DVD, with a shorter loan
# period), plus two interfaces (e.g., Reservable, Renewable) implemented
# by only the item types where they make sense.
```

**Definition of done:** A class hierarchy with at least one abstract class and two
interfaces, all mutable state private, polymorphic code (a function that operates on the
abstract type/interface, not concrete classes) that works unmodified across all
implementing types.

### 2. Refactor an anemic domain model into a rich one

**Goal:** Practice recognizing an anemic model and relocating behavior to the object
that owns the relevant data, with a justification for each move (not every method
necessarily belongs on the object — this should be a judgment call, not mechanical).

**Approach / hints:**
- Start from (or write) data classes with public fields/getters-setters and a separate
  `*Service` class containing all logic that operates on them.
- For each method on the service class, ask "which object's data does this method need
  in order to do its job?" — that's usually where the method belongs.
- Move methods over one at a time, tightening visibility on the data class's fields as
  you go (they should end up private, accessed only through the new behavior methods).
- Some logic legitimately coordinates *multiple* objects (e.g., transferring money
  between two accounts) — it's fine for that to stay in a small coordinating
  function/service; write down why you left it there rather than force-fitting it onto
  one object.

**Definition of done:** Each data class now exposes intention-revealing behavior
methods (not just getters/setters) and owns the logic that only needs its own data; a
short written note justifies each relocated method and explains any logic that
legitimately remained outside a single object.

### 3. Design a layered application and diagram the object interactions

**Goal:** Practice separating concerns across presentation, domain, and data layers,
and reasoning explicitly about the direction dependencies should point.

**Approach / hints:**
- Pick a simple use case (e.g., "a user submits a review" or "a user checks out a
  cart") small enough to fully design in one sitting.
- Define the domain layer first — the rich objects and their behavior — before
  worrying about how a UI or database will connect to them.
- Add a data layer (repository-style interface) that the domain layer depends on as an
  abstraction, and a presentation layer that depends on the domain layer.
- Diagram the layers with arrows showing dependency direction; every arrow should point
  inward (presentation → domain, data → domain interfaces), never outward from domain
  to presentation or to a concrete data implementation.

**Definition of done:** A diagram of the three layers with labeled objects and
dependency-direction arrows, plus a short write-up explaining what would break (and
what wouldn't) if the database implementation were swapped out.

## Further resources
- Free companion: MIT [6.005 Software Construction](https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/) · Martin Fowler, [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html)
