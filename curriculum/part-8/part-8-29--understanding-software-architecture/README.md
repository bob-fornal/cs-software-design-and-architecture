# 29. Understanding Software Architecture

**Part 8 — The Software Architect Role** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Everything you've learned so far — clean code, SOLID, architectural styles, distributed-systems tradeoffs — is raw material; "architecture" is the discipline of deciding which of those tools matter for *this* system, at *this* level, and living with the consequences.

## Learning objectives
- Can give a working definition of software architecture that distinguishes it from "just design" (scope, cost of change, and stakeholder impact are the differentiators).
- Can list the concrete activities a software architect actually does day to day, beyond drawing diagrams.
- Can classify a given decision as application-, solution-, or enterprise-level architecture and explain why the level matters for who's involved and how reversible the decision is.
- Can describe a real system at all three levels (application, solution, enterprise) with different content and different audiences at each level.

## Session outline (~45–60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: architecture vs. design | 5 min | Ask: "what's the difference between a design decision and an architecture decision?" Land on: architecture decisions are expensive to reverse and affect people beyond the team that made them (other teams, ops, the business). A variable name is design; "which database" or "sync vs. async between services" is architecture. |
| What software architecture is | 10 min | Define architecture as the set of structural decisions that are hard to change later: component boundaries, communication patterns, technology choices, quality attribute tradeoffs (performance vs. cost, consistency vs. availability). Emphasize it's as much about the *rationale* as the diagram — the diagram is a snapshot, the rationale is what survives. |
| What a software architect does | 10 min | Walk through the real job: translating business/quality requirements into structural decisions, documenting and communicating those decisions, reviewing designs against standards, unblocking teams, and owning technical risk. Contrast the myth (architect draws boxes and leaves) with reality (architect is embedded, iterating, and accountable). |
| Levels of architecture | 15 min | Application level: the internal structure of one system/service (its layers, modules, patterns — everything from Parts 1-3 of this course). Solution level: how that system fits with the systems around it — integration points, data contracts, shared infrastructure. Enterprise level: how the solution fits organizational strategy — standards, reuse across business units, build-vs-buy, portfolio-level tradeoffs. Use one running example (e.g., an internal payments service) and show what changes about the conversation at each level: at application level you're debating layering; at solution level you're debating which team owns the API contract; at enterprise level you're debating whether this should even be a new service or reuse an existing platform capability. |
| Wrap-up & homework framing | 10-15 min | Recap: same system, three lenses, three different audiences (your team, adjacent teams, leadership/governance). Introduce the homework: write an ADR (practicing application-level decision documentation) and describe a past system at all three levels. |

## Homework notes

### 1. Architecture Decision Record (ADR)
> Write a one-page Architecture Decision Record (ADR) for a real or hypothetical technical decision (e.g., "choose message broker" or "choose primary datastore"), including context, options considered, decision, and consequences.

- **Goal:** Tests whether students can externalize architectural reasoning — not just make a good call, but document it so someone six months from now (including future-them) understands *why*, not just *what*.
- **Approach / hints:** Pick a decision with real tension (at least two genuinely viable options, not a strawman). Context should state the forces at play (scale, team skill, budget, existing stack) without yet revealing the answer. Options should each get a fair one-or-two-sentence treatment of pros/cons. Consequences should include the downsides of the chosen option, not just the upsides — a good ADR admits what you're giving up.
- **Starter example:**
```markdown
# ADR-001: Choice of Message Broker

## Status
Accepted

## Context
We need async communication between the order service and 3 downstream
consumers. Expected volume: ~200 msg/sec peak. Team has no prior Kafka
experience; two engineers know RabbitMQ well.

## Options Considered
1. RabbitMQ — mature, team expertise, simpler ops, weaker for replay/streaming.
2. Kafka — better for high throughput and replay, steeper ops learning curve.
3. Cloud provider queue (e.g., SQS) — least ops overhead, vendor lock-in, no
   native pub/sub fan-out without extra topics/fanout config.

## Decision
RabbitMQ, given current volume, existing team expertise, and no near-term
need for event replay.

## Consequences
- Faster to ship; lower operational risk.
- Revisit if throughput exceeds ~2k msg/sec or replay/audit becomes a
  requirement — would likely mean migrating to Kafka.
```
- **Definition of done:** A one-page ADR (context, options considered with genuine tradeoffs, a decision, and consequences including at least one honest downside) for a decision with real stakes.

### 2. Describe a system at three levels
> Take a system you've built in a prior module and describe it at all three levels: application (its internal design), solution (how it fits with adjacent systems), and enterprise (how it fits organizational strategy/standards).

- **Goal:** Tests whether students can zoom out from "how I built it" to "how it fits" — the transition every engineer has to make to start thinking architecturally.
- **Approach / hints:** For application level, reuse language from earlier modules (layers, patterns used, module boundaries). For solution level, even a school/personal project has *some* adjacent context — what would it integrate with in a real deployment (auth provider, payment gateway, notification system)? Name the contracts. For enterprise level, if there's no real organization, invent a plausible one and describe how this system would need to conform to its standards (a shared logging format, a required auth provider, a data classification policy) — the point is practicing the *kind* of reasoning, not having a real enterprise on hand.
- **Definition of done:** Three short write-ups (a paragraph or diagram each) for the same system, each with content and an audience appropriate to its level — a reviewer should be able to tell which level they're reading without a label.

## Further resources
- Free companion: MIT [ESD.34 System Architecture](https://ocw.mit.edu/courses/esd-34-system-architecture-january-iap-2007/)
