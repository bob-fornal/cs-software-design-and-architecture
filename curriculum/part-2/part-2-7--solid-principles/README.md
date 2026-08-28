# 7. SOLID Principles

**Part 2 — Design Principles & Patterns** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
SOLID is the five-item checklist experienced developers run in their heads while
reviewing a diff — and the fastest way to explain, in one word each, why a class is
about to become impossible to change safely.

## Learning objectives
- Can state each SOLID principle in one sentence and recognize a violation of it in
  unfamiliar code.
- Can split a multi-responsibility "God class" into single-responsibility collaborators
  connected by constructor-injected dependencies (SRP + DIP together).
- Can design a class/module boundary that is Open for extension but Closed for
  modification — adding behavior means adding a class, not editing one.
- Can identify a Liskov Substitution violation (a subtype that breaks caller
  expectations) and an Interface Segregation violation (a fat interface forcing
  clients to depend on methods they don't use).
- Can perform a structured design review of an unfamiliar file, naming which SOLID
  principle each issue violates and proposing a concrete fix.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the 4am pager | 5 min | Why "just add an `if`" is how classes die |
| Single Responsibility Principle | 10 min | One reason to change; God-class smell |
| Open/Closed Principle | 10 min | Extension without modification; the `switch` smell |
| Liskov Substitution Principle | 8 min | Subtypes must honor the base type's contract |
| Interface Segregation Principle | 7 min | Fat interfaces and unwanted method implementations |
| Dependency Inversion Principle | 10 min | Depend on abstractions; who owns the interface |
| Wrap-up: SOLID as one story | 5 min | How all five reduce to "manage the direction of dependency" |

**Hook: the 4am pager (5 min).** Tell (or elicit) a story of a class that started as
"just handle the invoice" and grew a formatting method, then an email method, then a
database call, until one change to email copy required re-testing invoice totals. Ask:
what made this fragile? Land on "too many reasons to change" — the SRP definition —
as the frame for the whole session.

**Single Responsibility Principle (10 min).** Define SRP precisely: a class should
have one reason to change, one axis of responsibility, typically tied to one actor or
stakeholder. Show the invoice class (calculates totals, formats for print, saves to
DB, emails the customer) and identify the four separate reasons it could change.
Emphasize this is about *reasons to change*, not line count — a small class can still
violate SRP.

**Open/Closed Principle (10 min).** Define: open for extension, closed for
modification. Show the `switch (paymentType) { case "credit": ...; case "paypal": ... }`
pattern and how every new payment method means editing a function that's already
shipped and tested. Refactor live into a `PaymentMethod` interface with one class per
type, selected via a registry/factory — adding PayPal-2 means adding a class, not
touching the switch.

**Liskov Substitution Principle (8 min).** Define: subtypes must be substitutable for
their base type without breaking callers' expectations. Revisit the `RubberDuck`
example from Topic 6 as an LSP violation (throwing where the base contract promised
flight), then show the classic `Square extends Rectangle` trap — overriding
`setWidth`/`setHeight` to keep them equal breaks any code that assumes setting width
alone doesn't change height.

**Interface Segregation Principle (7 min).** Define: clients shouldn't be forced to
depend on methods they don't use. Show a fat `Worker` interface (`work()`, `eat()`,
`getPaid()`) implemented by a `RobotWorker` that has to throw or no-op on `eat()`.
Split into role interfaces (`Workable`, `Feedable`, `Payable`) so `RobotWorker`
implements only what applies.

**Dependency Inversion Principle (10 min).** Define: high-level modules shouldn't
depend on low-level modules — both should depend on abstractions; abstractions
shouldn't depend on details. This is the Hollywood Principle from Topic 6 made
concrete: an `OrderService` should depend on a `PaymentGateway` interface it defines,
not on a concrete `StripeClient`, and `StripeClient` implements that interface. Connect
to constructor injection as the mechanical technique, and note DIP is what makes the
plugin system in homework 2 actually testable (fakes/mocks implement the interface).

**Wrap-up (5 min).** Reframe all five as one idea: control the *direction* dependencies
point, so change in one place doesn't ripple. SRP limits reasons to change; OCP adds
behavior without editing; LSP keeps substitution safe; ISP shrinks what a client must
know; DIP flips who depends on whom. This is the direct on-ramp to GoF patterns
(Topic 9), most of which are named techniques for satisfying OCP or DIP.

## Homework notes

### 1. Split a God class to satisfy SRP and DIP

**Goal:** Practice recognizing separate responsibilities bundled into one class and
separating them into single-purpose collaborators wired together by injected
dependencies rather than internal `new` calls.

**Approach / hints:**
- Start from (or write) an `OrderProcessor` that validates input, persists to a
  database, sends a notification, and formats a receipt — all in one class, all
  concrete dependencies constructed inside its methods.
- Extract one class per responsibility: `OrderValidator`, `OrderRepository`,
  `NotificationSender`, `ReceiptFormatter`. Each gets its own single reason to change.
- Have `OrderProcessor` (or a renamed orchestrator) take these four as constructor
  parameters — typed as interfaces, not concrete classes — rather than instantiating
  them itself. That's the DIP half of the exercise.
- Prove it: write a test for the orchestrator using fake/in-memory implementations of
  all four collaborators, with no real database or network call involved.

**Starter example (TypeScript):**
```typescript
interface OrderRepository { save(order: Order): Promise<void>; }
interface NotificationSender { notify(order: Order): Promise<void>; }

class OrderProcessor {
  constructor(
    private readonly repo: OrderRepository,
    private readonly notifier: NotificationSender,
    // TODO: add validator and receiptFormatter as injected interfaces too
  ) {}

  async process(order: Order): Promise<void> {
    // TODO: validate, save, format receipt, notify — each delegated,
    // none of it implemented inline in this method.
  }
}
```

**Definition of done:** Four (or more) single-responsibility classes exist, each
independently testable; the orchestrating class receives all of them via its
constructor typed as interfaces; a unit test exercises the orchestrator with fakes and
touches no real I/O.

### 2. Build an Open/Closed plugin system

**Goal:** Design a boundary where adding a new capability never requires editing
existing, already-shipped code.

**Approach / hints:**
- Pick a domain with natural variants: payment methods, export formats
  (CSV/JSON/XML), or notification channels (email/SMS/push) all work well.
- Define one interface (e.g., `ExportFormat` with an `export(data): string` method).
- Implement 2–3 concrete variants, then add a registry/factory that maps a key
  (string or enum) to an implementation — this is the *only* place that changes shape
  as variants are added, and ideally it's driven by registration calls rather than a
  hardcoded `switch`.
- Add a brand-new variant (a fourth export format) and confirm the diff touches only
  new files plus one registration line — never the interface, never existing variant
  classes, never the code that calls the factory.

**Starter example (Python):**
```python
from abc import ABC, abstractmethod

class ExportFormat(ABC):
    @abstractmethod
    def export(self, rows: list[dict]) -> str: ...

_registry: dict[str, ExportFormat] = {}

def register(name: str, fmt: ExportFormat) -> None:
    _registry[name] = fmt

def export_as(name: str, rows: list[dict]) -> str:
    return _registry[name].export(rows)

# TODO: implement CsvFormat, JsonFormat, register both, then add a third
# format later WITHOUT touching this file's export_as/register functions.
```

**Definition of done:** At least three interchangeable implementations exist behind
one interface; a new implementation can be added and wired in without modifying any
existing class or the dispatch mechanism's logic (only additive registration).

### 3. Design review of a ~150-line file

**Goal:** Practice spotting SOLID violations in someone else's code under time
pressure — the skill a senior engineer actually uses in code review, as opposed to
writing textbook-clean code from scratch.

**Approach / hints:**
- Use a ~150-line file from an earlier assignment (yours or a classmate's), or a
  provided sample with a mix of a multi-purpose class, a type-switch, an overridden
  method that narrows a base contract, and a fat interface.
- Go principle by principle (not top-to-bottom in the file) — it's easy to see SRP
  issues and miss LSP issues if you only skim once. For each principle found violated,
  cite the specific line(s) and explain *which caller or future change* would break.
- Propose a fix for each — a sketch/diff is enough, it doesn't need to be a full
  rewrite.
- Not every principle needs to be present — if a file has no LSP violation, say so
  explicitly rather than forcing one.

**Definition of done:** A short written review (one paragraph or bullet list per
principle found) covering the five principles, each violation citing specific code and
a concrete proposed fix; principles with no violation are explicitly noted as clean.

## Further resources
- Free companion: [DeviQ — SOLID](https://deviq.com/principles/solid) · freeCodeCamp, [SOLID Principles Explained](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/)
