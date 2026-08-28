# 31. Architecture Frameworks & Methodologies

**Part 8 — The Software Architect Role** · [Back to curriculum index](../README.md)

## One-sentence pitch
Frameworks like TOGAF and notations like UML aren't the architecture itself — they're shared vocabularies that let an architect's decisions survive contact with other teams, other years, and other people who weren't in the room when the decision was made.

## Learning objectives
- Can name the purpose of TOGAF, UML, BABOK, and IAF and distinguish "enterprise architecture framework" from "modeling notation" from "business analysis framework."
- Can produce a class diagram and a sequence diagram that correctly use UML notation to document a real design.
- Can name the core practices of Scrum, Kanban, LeSS, SAFe, and XP and place each on a spectrum from lightweight/team-level to heavyweight/enterprise-scale.
- Can compare two process methodologies for a specific project context and justify a recommendation based on the project's actual constraints (regulation, team size, rate of change), not just methodology popularity.
- Can explain, at a conceptual level, what PMI, ITIL, Prince2, and RUP each govern, even without having used them directly.

## Session outline (~45–60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: why frameworks exist at all | 5 min | A team with no shared vocabulary re-derives "how do we document a decision" and "how do we run a sprint" from scratch every project. Frameworks and methodologies are accumulated answers to those recurring questions — the goal isn't dogma, it's not reinventing coordination every time. |
| Architecture frameworks: TOGAF, IAF | 8 min | TOGAF (The Open Group Architecture Framework): a process (the ADM — Architecture Development Method) for developing enterprise architecture across business, data, application, and technology layers. IAF (Integrated Architecture Framework): a similar enterprise-architecture framework with its own layered view. Note honestly: these are heavyweight, enterprise-scale tools — most students will encounter them by *name* in industry before they use them directly, and that's fine; the goal here is recognition, not mastery. |
| UML as a shared notation | 12 min | UML isn't a framework, it's a notation — a way to draw structure (class diagrams, component diagrams) and behavior (sequence diagrams, state machines, activity diagrams) so any two engineers read the same box-and-arrow the same way. Live-sketch a class diagram (classes, associations, multiplicity, inheritance) and a sequence diagram (lifelines, messages, activation bars) for a small example, e.g. "place an order." Emphasize: UML is a communication tool, not a code-generation ritual — draw only what needs to be communicated. |
| BABOK & business analysis | 5 min | BABOK (Business Analysis Body of Knowledge): a framework of business-analysis practices — requirements elicitation, stakeholder analysis, solution evaluation — that overlaps heavily with what was covered as "architect soft skills" in the prior topic, formalized into a certifiable body of knowledge. |
| Process/project methodologies | 15 min | Team-level agile: Scrum (fixed-length sprints, defined roles, ceremonies) vs. Kanban (continuous flow, WIP limits, no fixed iterations) vs. XP (engineering practices — pairing, TDD, continuous integration — layered on top of an agile process). Scaled agile: LeSS (Large-Scale Scrum — Scrum's rules stretched across multiple teams on one product) vs. SAFe (Scaled Agile Framework — a more prescriptive, role-heavy framework for large organizations). Traditional/process-heavy: PMI (project management body of knowledge — plan-driven, broadly applicable beyond software), ITIL (IT service management — incident, change, and service processes, common in ops-heavy enterprises), Prince2 (a structured, stage-gated project management method common outside the US), RUP (Rational Unified Process — an iterative, UML-heavy predecessor to modern agile methods). Compare on one axis: how much ceremony/predictability vs. how much adaptability each buys you, and for what kind of organization that trade makes sense. |
| Wrap-up & homework framing | 5-10 min | Recap: none of these are "the right answer" universally — the skill is matching the framework's assumptions (team size, regulatory context, rate of change) to the actual project. Introduce the homework: produce real UML diagrams, then argue methodology fit for a specific scenario. |

## Homework notes

### 1. UML diagrams for an earlier system
> Produce a set of UML diagrams (class diagram + sequence diagram) documenting the design of a system from an earlier module.

- **Goal:** Tests whether students can translate a design that already exists in code (or in their head) into standard notation that someone who never saw the code could still understand.
- **Approach / hints:** Pick a system from an earlier module with at least 3-4 collaborating classes and one interesting multi-step interaction. For the class diagram, show classes, key attributes/methods, and relationships (association, inheritance, composition) with correct multiplicity — resist the urge to include every private field. For the sequence diagram, pick one meaningful use case (not "everything the system does") and show the actual message order between objects, including any conditional/loop framing if relevant. Free tooling: PlantUML or Mermaid class/sequence diagram syntax both render from plain text and are good enough for this exercise.
- **Starter example:**
```
@startuml
class Order {
  -items: List<OrderItem>
  -status: OrderStatus
  +addItem(item: OrderItem)
  +submit(): void
}
class OrderItem {
  -sku: String
  -quantity: int
}
Order "1" *-- "many" OrderItem

Order -> PaymentGateway : charge(amount)
PaymentGateway --> Order : confirmation
Order -> InventoryService : reserve(items)
@enduml
```
- **Definition of done:** One class diagram and one sequence diagram, both using correct UML notation (proper relationship types and multiplicities; proper lifelines and message arrows), documenting a real design rather than a toy example invented just for the assignment.

### 2. Compare two process methodologies for a scenario
> Compare two process methodologies (e.g., Scrum vs. Kanban) for a specific project scenario (a fast-changing startup product vs. a regulated enterprise system) and justify which fits better and why.

- **Goal:** Tests whether students understand methodologies as tools with tradeoffs tied to context, not as a matter of taste or trend — the same skill an architect needs when recommending a process to a team that isn't like the last one.
- **Approach / hints:** Write out the scenario's actual constraints first (team size, how often requirements change, regulatory/audit needs, distribution of the team) before touching the methodologies — the comparison should follow from the constraints, not the other way around. For each methodology, name 2-3 concrete mechanics (e.g., Scrum's sprint commitment vs. Kanban's WIP limits) and connect each directly to a constraint in the scenario ("a regulated system needs an audit trail of what was planned vs. delivered, which favors Scrum's fixed sprint commitments over Kanban's continuous flow").
- **Definition of done:** A short comparison (roughly one page) covering two contrasting scenarios, naming specific mechanics of each methodology (not just vibes), and ending in a clear, justified recommendation per scenario.

## Further resources
- Free companion: [Scrum Guide](https://scrumguides.org/) · OMG, [UML 2.5.1 Specification](https://www.omg.org/spec/UML/2.5.1/PDF)

**A note on sourcing:** TOGAF's official documentation and BABOK both currently require a login/membership to access (TOGAF via The Open Group, BABOK via IIBA membership) — neither has genuinely free, public primary-source material at the time of writing. This topic covers both conceptually in the outline above, but students should treat the Scrum Guide and the UML specification linked above as the hands-on, freely accessible material for this session; TOGAF and BABOK are presented for recognition and vocabulary rather than as a primary-source deep dive.
