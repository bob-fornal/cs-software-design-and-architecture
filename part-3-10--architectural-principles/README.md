# 10. Architectural Principles

**Part 3 — Architectural Foundations** · [Back to curriculum index](../README.md)

## One-sentence pitch
Long before you pick a framework or draw a microservices diagram, architecture is decided by where you put the line between what your software *does* (policy) and what it *runs on* (detail) — get that line wrong and every later decision inherits the mess.

## Learning objectives
- Can classify any piece of code in a real module as "policy" (business rule) or "detail" (I/O, framework, UI, database) and explain why the classification matters.
- Can state and apply the component cohesion principles (REP, CCP, CRP) to decide what belongs in the same component.
- Can state and apply the component coupling principles (ADP, SDP, SAP) to diagnose why a codebase is hard to change.
- Can identify a concrete instance of afferent/efferent coupling in a dependency graph and propose a boundary that reduces it.
- Can draw an architecture boundary (with a dependency-inversion interface) that keeps policy from depending on detail.

## Session outline (~45–60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the cost of no boundaries | 5 min | Show a real "big ball of mud" symptom: a change to a UI framework forces edits in business logic. Ask: why did that happen? |
| Policy vs. detail | 10 min | Define policy (rules that would exist even if you rewrote the UI/DB/framework) vs. detail (the specific mechanism delivering data in/out). Walk through a concrete example: an "apply late fee" rule (policy) vs. the SQL query and REST controller that surround it (detail). |
| Component cohesion principles | 10 min | REP (Reuse/Release Equivalence Principle), CCP (Common Closure Principle — classes that change together, live together), CRP (Common Reuse Principle — don't force consumers to depend on things they don't use). Use a small package-structure example to show a violation of each. |
| Component coupling principles | 10 min | ADP (Acyclic Dependencies Principle — no cycles), SDP (Stable Dependencies Principle — depend in the direction of stability), SAP (Stable Abstractions Principle — stable components should be abstract). Draw a dependency graph with a cycle and show how to break it (dependency inversion / extracting an interface). |
| Boundaries in practice | 10 min | What a boundary actually is: a place where you can change one side without recompiling/redeploying the other. Show the "plugin architecture" pattern — policy defines an interface, detail implements it, and the arrow of source-code dependency points *inward*, toward policy. Emphasize: data crossing a boundary should be simple structures, not framework-coupled objects. |
| Wrap-up & homework framing | 5–10 min | Recap: coupling and cohesion aren't abstract — they predict how painful your next feature will be. Introduce the homework: draw the boundary, then go find a real coupling problem. |

## Homework notes

### 1. Policy vs. detail diagram
> Take a monolithic module and identify its "policy" (business rules) vs. "detail" (I/O, frameworks, UI). Redraw it as a diagram with a boundary line and explain what should never cross it.

- **Goal:** Tests whether students can actually separate "what the software decides" from "how it's delivered" — the core skill behind Clean Architecture, Hexagonal Architecture, and most other boundary-drawing frameworks they'll meet later.
- **Approach / hints:** Pick a module with an obvious framework dependency (a controller that also computes a discount, a script that both parses a file and decides what's valid). List every responsibility as a bullet, tag each "policy" or "detail," then group. The diagram doesn't need to be fancy — boxes and one boundary line are enough. The write-up should explicitly say what crosses the boundary (plain data) and what must never cross it (framework types, ORM entities, HTTP request objects).
- **Definition of done:** A diagram with a clearly drawn boundary line, every original responsibility placed on one side or the other, and 2-3 sentences explaining what data is allowed to cross and why nothing on the detail side should be referenced by name from the policy side.

### 2. Coupling and cohesion audit
> Audit a real or provided codebase for coupling and cohesion: identify the two most tightly coupled modules and propose a boundary/interface that would decouple them.

- **Goal:** Tests whether students can read a dependency graph (not just single files) and recognize afferent/efferent coupling as a *design smell*, then propose a concrete fix — an interface plus dependency inversion — rather than just describing the problem.
- **Approach / hints:** Start by listing imports/dependencies between modules (a simple grep for import statements works, or use a dependency-graph tool if the language has one). Look for two modules that both change whenever the other changes, or where a "stable" module depends on something volatile (violates SDP). Propose the fix as: extract an interface owned by the more stable side, have the volatile side implement it, invert the dependency arrow.
- **Starter example:**
```python
# Before: OrderProcessor directly depends on the concrete EmailSender detail.
class EmailSender:
    def send(self, to, subject, body): ...

class OrderProcessor:
    def __init__(self):
        self.mailer = EmailSender()  # concrete dependency -> tight coupling

    def complete_order(self, order):
        # ... business rules ...
        self.mailer.send(order.customer_email, "Order complete", "...")

# After: invert the dependency through an interface owned by policy.
class Notifier(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...

class OrderProcessor:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier  # depends on abstraction, not detail
```
- **Definition of done:** A short written audit naming the two most coupled modules with evidence (import lists or a graph), plus a proposed interface/boundary with either a diagram or a code sketch showing the inverted dependency.

## Further resources
- Free companion: Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
