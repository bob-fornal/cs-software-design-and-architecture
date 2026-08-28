# Software Design & Architecture Curriculum

Synthesized from three roadmap.sh guides:
[Software Design & Architecture](https://roadmap.sh/software-design-architecture) ·
[System Design](https://roadmap.sh/system-design) ·
[Software Architect](https://roadmap.sh/software-architect)

Structured as sequential modules, one topic at a time. Each topic lists its key
subtopics and 1–3 homework projects meant to be assigned after that topic is taught.
Projects generally build in difficulty within a topic (project 1 = apply the concept
directly, later projects = combine it with prior modules).

---

## The Backbone Curriculum

The 33 topics below are the index for the whole curriculum — the order they're meant
to be taught in, with a genuinely free companion resource next to each where one
exists. Every link was checked to confirm it's actually live, actually free (no
paywall or signup wall), and actually on-topic — not guessed. Several topics share a
resource where one source legitimately covers more than one subject (the
[system-design-primer](https://github.com/donnemartin/system-design-primer) repo for
most of Parts 4–6, the Azure Architecture Center's pattern catalog for most of Part 7)
rather than forcing a distinct citation onto every row.

| # | Topic | Free companion / source |
|---|---|---|
| 1 | [Clean Code Principles](#1-clean-code-principles) | MIT [6.005 Software Construction](https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/) · [blog.cleancoder.com](https://blog.cleancoder.com/) |
| 2 | [Structured Programming](#2-structured-programming) | Harvard [CS50x](https://cs50.harvard.edu/x/) |
| 3 | [Functional Programming](#3-functional-programming) | MIT, [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) (SICP, full free text) |
| 4 | [Object-Oriented Programming](#4-object-oriented-programming) | MIT [6.005 Software Construction](https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/) · Martin Fowler, [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html) |
| 5 | [Programming Paradigms](#5-programming-paradigms) | Stanford [CS107: Programming Paradigms](https://see.stanford.edu/Course/CS107) (Stanford Engineering Everywhere) |
| 6 | [Core Design Principles](#6-core-design-principles) | [DeviQ — Principles](https://deviq.com/principles/) |
| 7 | [SOLID Principles](#7-solid-principles) | [DeviQ — SOLID](https://deviq.com/principles/solid) · freeCodeCamp, [SOLID Principles Explained](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/) |
| 8 | [DRY & YAGNI](#8-dry--yagni) | [DeviQ — DRY](https://deviq.com/principles/dont-repeat-yourself) / [YAGNI](https://deviq.com/principles/yagni/) · Martin Fowler, [Yagni](https://martinfowler.com/bliki/Yagni.html) |
| 9 | [Design Patterns (GoF & PoSA)](#9-design-patterns-gof--posa) | [refactoring.guru — Design Patterns Catalog](https://refactoring.guru/design-patterns/catalog) · Vanderbilt, [POSA2 companion materials](https://www.dre.vanderbilt.edu/~schmidt/POSA/POSA2/) |
| 10 | [Architectural Principles](#10-architectural-principles) | Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) |
| 11 | [Architectural Styles](#11-architectural-styles) | *[Software Engineering: A Modern Approach](https://softengbook.org/chapter7), Ch. 7 — free open textbook (page blocks automated fetches; spot-check before relying on it)* |
| 12 | [Architectural Patterns](#12-architectural-patterns) | *[Software Engineering: A Modern Approach](https://softengbook.org/chapter7), Ch. 7 · Eric Evans, [DDD Reference](https://www.domainlanguage.com/ddd/reference/) — covers MVC, Microservices, Layered, and DDD; doesn't name-check Microkernel/Blackboard/SOA/CQRS directly* |
| 13 | [Enterprise Application Patterns](#13-enterprise-application-patterns) | Martin Fowler, [P of EAA Catalog](https://martinfowler.com/eaaCatalog/) |
| 14 | [Core System Design Concepts](#14-core-system-design-concepts) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 15 | [Consistency & Availability Patterns](#15-consistency--availability-patterns) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 16 | [DNS, CDNs & Load Balancers](#16-dns-cdns--load-balancers) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 17 | [Scaling Applications](#17-scaling-applications) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 18 | [Databases at Scale](#18-databases-at-scale) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 19 | [NoSQL Database Types](#19-nosql-database-types) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 20 | [Caching Strategies](#20-caching-strategies) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 21 | [Asynchronism](#21-asynchronism) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 22 | [Communication Protocols](#22-communication-protocols) | [system-design-primer](https://github.com/donnemartin/system-design-primer) |
| 23 | [Performance Antipatterns](#23-performance-antipatterns) | Azure Architecture Center, [Antipatterns](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/) |
| 24 | [Monitoring & Observability](#24-monitoring--observability) | Google, [SRE Book — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) |
| 25 | [Cloud Messaging Patterns](#25-cloud-messaging-patterns) | [Azure Architecture Center — Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/) |
| 26 | [Cloud Data Management Patterns](#26-cloud-data-management-patterns) | [Azure Architecture Center — Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/) |
| 27 | [Reliability & Resiliency Patterns](#27-reliability--resiliency-patterns) | Azure Architecture Center, [Reliability design patterns](https://learn.microsoft.com/en-us/azure/well-architected/reliability/design-patterns) |
| 28 | [Cloud Security Patterns](#28-cloud-security-patterns) | Azure Architecture Center, [Security design patterns](https://learn.microsoft.com/en-us/azure/well-architected/security/design-patterns) |
| 29 | [Understanding Software Architecture](#29-understanding-software-architecture) | MIT [ESD.34 System Architecture](https://ocw.mit.edu/courses/esd-34-system-architecture-january-iap-2007/) |
| 30 | [Architect Responsibilities & Soft Skills](#30-architect-responsibilities--soft-skills) | MIT [21W.780 Communicating in Technical Organizations](https://ocw.mit.edu/courses/21w-780-communicating-in-technical-organizations-fall-2001/) |
| 31 | [Architecture Frameworks & Methodologies](#31-architecture-frameworks--methodologies) | [Scrum Guide](https://scrumguides.org/) · OMG, [UML 2.5.1 Specification](https://www.omg.org/spec/UML/2.5.1/PDF) |
| 32 | [Security for Architects](#32-security-for-architects) | [OWASP Top 10](https://owasp.org/www-project-top-ten/) |
| 33 | [Operations & DevOps Knowledge](#33-operations--devops-knowledge) | freeCodeCamp, [DevOps articles & tutorials](https://www.freecodecamp.org/news/tag/devops/) |

*No free, no-signup companion could be verified for two frameworks named in topic 31
— TOGAF's official docs now sit behind a mandatory OAuth login, and BABOK requires
IIBA membership — so neither is cited above; teach them from other material. Rows 29
and 30 are the closest free full courses found, not exact topic matches: MIT's system
architecture and technical-communication courses cover the underlying skills but
don't walk through "levels of architecture" or "requirements elicitation" by name.*

---

## Part 1 — Foundations of Code Quality

### 1. Clean Code Principles
Consistency, naming, indentation/style, small methods/classes/files, pure functions,
minimizing cyclomatic complexity, avoiding null/boolean params, keeping framework code
at the edges, fast/independent tests, organizing code by actor, command-query
separation, refactoring habits.

**Homework:**
1. Take a working but messy ~200-line script (provide one, or use a prior assignment) and refactor it using only clean-code rules — no behavior changes. Submit a before/after diff with a written note on which rule fixed which smell.
2. Write a small module (e.g., a CSV parser or receipt calculator) with a hard rule: every function ≤ 15 lines, no boolean parameters, no comments explaining *what* code does (only *why*, where unavoidable).
3. Pair-review exercise: exchange code with a classmate and produce a "clean code report card" scoring their submission against the rules above with specific line references.

### 2. Structured Programming
Sequence, selection, and iteration as the only control-flow primitives; single-entry/
single-exit; avoiding unstructured jumps (`goto`); top-down decomposition into
procedures/functions.

**Homework:**
1. Take a piece of code with tangled, jump-heavy control flow (a `goto`-based example, or a deeply nested mess of early returns and flags) and refactor it into pure structured constructs — sequence, selection, iteration only — with single-entry/single-exit.
2. Solve a problem (e.g., a menu-driven program or a simple state machine) using top-down decomposition: write the top-level algorithm first as calls to not-yet-implemented procedures (stubs), then fill in each procedure in isolation.
3. Take one long, flat, unstructured function (all logic inline, no sub-procedures) and decompose it into a set of well-named procedures using only structured constructs, without changing its behavior.

### 3. Functional Programming
Pure functions, immutability, first-class and higher-order functions, function
composition, map/filter/reduce, recursion over iteration, referential transparency,
avoiding shared mutable state.

**Homework:**
1. Implement a small data-processing task (e.g., turning a list of orders into a summary report) using only pure functions, immutable data structures, and map/filter/reduce — no loops, no mutation.
2. Take an imperative function that mutates shared state and produces side effects mid-logic, and refactor it into a pure function, pushing the side effects out to the edge of the program.
3. Build small `compose`/`pipe` utilities and use them to assemble a pipeline (e.g., validate → transform → format) out of small, independently testable functions.

### 4. Object-Oriented Programming
Encapsulation, abstraction, inheritance, polymorphism, interfaces, scope/visibility,
abstract vs. concrete classes, domain models vs. anemic models, class variants,
domain language, layered architectures.

**Homework:**
1. Model a domain (e.g., a library, a parking garage, a board game) with a proper class hierarchy demonstrating encapsulation, inheritance, and polymorphism — include at least one abstract class and two interfaces.
2. Take an "anemic" domain model (data classes + separate service classes doing all the logic) and refactor it into a rich domain model where behavior lives with the data it operates on. Justify each move.
3. Design a small layered application (presentation → domain → data) for a simple use case and diagram how objects at each layer talk to each other.

### 5. Programming Paradigms
Now that structured, functional, and object-oriented programming have each been
practiced in isolation: comparing them directly, recognizing which problem shape
each paradigm fits best, and mixing paradigms deliberately within one codebase
(e.g., a functional core with an object-oriented or structured shell).

**Homework:**
1. Implement the same small algorithm (e.g., a word-frequency counter) three ways — purely structured/procedural, purely functional, and OOP — reusing what you built in topics 2–4 where possible. Write a short comparison of readability, testability, and how easily each version accommodates a new requirement.
2. Take an existing OOP or structured codebase snippet and convert its core logic to a functional-core/imperative-shell design: pure functions for the decision-making logic, with I/O and mutation isolated at the boundary. Explain what got easier to test and what got harder to read.

---

## Part 2 — Design Principles & Patterns

### 6. Core Design Principles
Composition over inheritance, encapsulate what varies, program against abstractions,
the Hollywood Principle, Law of Demeter, Tell Don't Ask.

**Homework:**
1. Take a class hierarchy that uses deep inheritance to handle variation (e.g., `FlyingDuck extends Duck`, `RubberDuck extends Duck` with an overridden `fly()` that throws) and refactor it to use composition/strategy objects instead.
2. Refactor a piece of code that violates the Law of Demeter (chains like `a.getB().getC().doThing()`) and Tell-Don't-Ask (lots of getters used to make external decisions) into a version where objects are told what to do.

### 7. SOLID Principles
Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation,
Dependency Inversion.

**Homework:**
1. Take a "God class" (does validation, persistence, notification, and formatting) and split it to satisfy SRP and DIP, injecting dependencies rather than constructing them internally.
2. Build a small plugin-style system (e.g., pluggable payment methods or export formats) that is Open/Closed — adding a new type requires adding a class, not editing existing ones.
3. Write a short design review flagging SOLID violations in a provided ~150-line file, one violation per principle where present, each with a proposed fix.

### 8. DRY & YAGNI
Don't Repeat Yourself vs. premature abstraction; You Aren't Gonna Need It vs.
under-engineering.

**Homework:**
1. Given a codebase with 3–4 near-duplicate functions, extract the shared abstraction — but write a short justification for *where* you drew the line (over-abstracting duplicated-looking-but-conceptually-different code is a common trap).
2. Given an over-engineered mini-framework (config-driven, plugin-based) built to solve a problem that only ever has one implementation, strip it down to the simplest thing that works, and write down what you'd need to see before re-adding the abstraction.

### 9. Design Patterns (GoF & PoSA)
Creational, structural, and behavioral Gang of Four patterns; Patterns of Software
Architecture (PoSA) patterns for concurrency and distributed systems.

**Homework:**
1. Pick 3 GoF patterns from different categories (e.g., Factory Method, Decorator, Observer) and implement each in a small, realistic scenario — not the textbook example. Include a note on what problem it solved and what it would look like *without* the pattern.
2. Refactor a piece of conditional-heavy code (a big `switch`/`if-else` selecting behavior) into the Strategy pattern, and a piece of tightly-coupled notification code into Observer.
3. Research and implement one PoSA concurrency pattern (e.g., Half-Sync/Half-Async or Leader/Followers) in a toy multi-threaded or async task processor.

---

## Part 3 — Architectural Foundations

### 10. Architectural Principles
Component principles, policy vs. detail, coupling and cohesion, boundaries.

**Homework:**
1. Take a monolithic module and identify its "policy" (business rules) vs. "detail" (I/O, frameworks, UI). Redraw it as a diagram with a boundary line and explain what should never cross it.
2. Audit a real or provided codebase for coupling and cohesion: identify the two most tightly coupled modules and propose a boundary/interface that would decouple them.

### 11. Architectural Styles
Layered, client-server, peer-to-peer, event-driven, publish-subscribe, component-based,
monolithic, distributed.

**Homework:**
1. Design (diagram + short write-up) the same simple system — e.g., a chat app — under two different architectural styles: layered client-server vs. event-driven pub-sub. Compare trade-offs in latency, coupling, and failure handling.
2. Build a minimal working pub-sub message dispatcher (in-process is fine) and a minimal layered equivalent of the same feature; compare code structure.

### 12. Architectural Patterns
MVC, Domain-Driven Design, Microservices, Microkernel, Blackboard, Serverless,
Event Sourcing, SOA, CQRS.

**Homework:**
1. Build a small feature using MVC, then re-architect the same feature using CQRS (separate command/query models). Document what changed and why you would/wouldn't do this for a real feature this size.
2. Take a single well-defined bounded context (e.g., "order fulfillment") and apply DDD tactically: identify entities, value objects, aggregates, and a repository interface — no implementation required, just the design.
3. Sketch a decomposition of a monolithic app (provided or one from a prior assignment) into 3–4 microservices, including how they'd communicate (sync vs. async) and what data each would own.

### 13. Enterprise Application Patterns
DTOs, identity maps, use cases, repositories, mappers, transaction script, commands/
queries, value objects, domain models, entities, ORMs.

**Homework:**
1. Implement a Repository + DTO pattern in front of a simple data store (in-memory or SQLite): domain objects never leak past the repository boundary, and API responses use DTOs, not entities.
2. Compare Transaction Script vs. Domain Model for the same use case (e.g., "apply a discount to an order"): implement both, then write a short comparison of when each is the better choice.

---

## Part 4 — System Design Fundamentals

### 14. Core System Design Concepts
Performance vs. scalability, latency vs. throughput, availability vs. consistency,
CAP theorem (CP vs. AP).

**Homework:**
1. Write a short design memo for a hypothetical system (e.g., a URL shortener) explicitly stating whether it favors CP or AP under partition, and why, referencing CAP theorem trade-offs.
2. Given three system scenarios (e.g., banking ledger, social media feed, chat delivery receipts), classify each as prioritizing consistency or availability and justify the choice.

### 15. Consistency & Availability Patterns
Weak/eventual/strong consistency; failover (active-active, active-passive);
replication (master-slave, master-master); availability in numbers (99.9%, 99.99%)
and in parallel vs. sequence.

**Homework:**
1. Calculate theoretical availability for a system with components in series vs. parallel (given per-component uptime %) and propose a redundancy change to hit "four nines."
2. Design a replication strategy (diagram) for a read-heavy service using master-slave replication; describe what breaks under eventual consistency and how the UI/client should handle stale reads.

### 16. DNS, CDNs & Load Balancers
Domain Name System resolution; push vs. pull CDNs; load balancers vs. reverse
proxies; load balancing algorithms; Layer 4 vs. Layer 7.

**Homework:**
1. Diagram the full request path from a browser typing a URL to a response, labeling where DNS resolution, CDN caching, and load balancing occur.
2. Configure a local reverse proxy/load balancer (e.g., Nginx or a simple custom one) in front of 2–3 instances of a toy app, and demonstrate round-robin vs. least-connections behavior.

### 17. Scaling Applications
Horizontal scaling, stateless application layers, microservices at scale, service
discovery.

**Homework:**
1. Take a stateful toy web app (sessions stored in memory) and refactor it to be horizontally scalable (externalize session state), then simulate running 2+ instances behind a load balancer.
2. Implement a minimal service discovery mechanism (even a shared registry file/service) for 2–3 toy services that need to find each other's addresses at runtime.

---

## Part 5 — Data at Scale

### 18. Databases at Scale
SQL vs. NoSQL, replication, sharding, federation, denormalization, SQL tuning, RDBMS.

**Homework:**
1. Given a normalized relational schema that's slow on a specific read-heavy query, denormalize it strategically and measure/explain the trade-off (write complexity vs. read speed).
2. Design a sharding strategy for a large hypothetical table (e.g., "users" at 500M rows): pick a shard key, explain hot-spot risks, and describe how a cross-shard query would be handled.

### 19. NoSQL Database Types
Key-value stores, document stores, wide-column stores, graph databases — access
patterns and when each fits.

**Homework:**
1. Model the same domain (e.g., a social network's "friends" and posts) in a document store and a graph database; implement one representative query in each and compare.
2. Given four scenarios (session cache, product catalog, sensor time-series, social graph), match each to the best-fit NoSQL type with a one-paragraph justification, then build a minimal working example for one of them.

### 20. Caching Strategies
Cache-aside, read-through/refresh-ahead, write-through, write-behind; client, CDN,
web server, application, and database caching layers.

**Homework:**
1. Add a cache-aside layer in front of a slow data-access function in a toy app; include cache invalidation on writes and measure the before/after latency.
2. Implement write-through vs. write-behind caching for the same write path and discuss the durability/consistency trade-off and failure modes (e.g., crash before flush) of each.

---

## Part 6 — Asynchronous & Distributed Communication

### 21. Asynchronism
Background jobs (event-driven vs. schedule-driven), message queues, task queues,
back pressure, idempotent operations.

**Homework:**
1. Build a producer/consumer task queue (e.g., using Redis, RabbitMQ, or an in-memory queue) for a slow operation (image resize, email send) offloaded from a request handler.
2. Make one of your queue consumers idempotent (safe to process the same message twice) and write a test that proves it by delivering a duplicate message.
3. Simulate back pressure: have a fast producer overwhelm a slow consumer and implement one mitigation (bounded queue + reject, or rate limiting) with before/after behavior documented.

### 22. Communication Protocols
HTTP, TCP, UDP, RPC, REST, gRPC, GraphQL.

**Homework:**
1. Implement the same simple API (e.g., "get user by id", "list posts") as both a REST endpoint and a GraphQL resolver; compare over/under-fetching for a client that only needs 2 of 8 fields.
2. Build a minimal gRPC service and client for a small use case, and write a short comparison of gRPC vs. REST for internal service-to-service calls.

### 23. Performance Antipatterns
Busy database/frontend, chatty I/O, extraneous fetching, improper instantiation,
monolithic persistence, no caching, noisy neighbor, retry storm, synchronous I/O.

**Homework:**
1. Given a provided code sample exhibiting "chatty I/O" (N+1 query pattern) and "extraneous fetching" (fetching whole rows/objects when only one field is needed), identify both and fix them.
2. Write a small load-test/demo that reproduces a "retry storm" (naive retry-on-failure with no backoff overwhelming a struggling service) and fix it with exponential backoff + jitter.

### 24. Monitoring & Observability
Health, availability, performance, security, and usage monitoring; instrumentation;
visualization & alerts.

**Homework:**
1. Instrument a toy service with basic metrics (request count, error rate, p95 latency) and a `/health` endpoint, then wire up a simple dashboard (even a local Grafana/Prometheus stack or a rolled-your-own chart).
2. Define and implement 3 alert conditions (e.g., error rate > 5%, p95 latency > 500ms, health check failing) for your instrumented service, and simulate each condition to prove the alert fires.

---

## Part 7 — Cloud Design Patterns

### 25. Cloud Messaging Patterns
Queue-based load leveling, competing consumers, publisher/subscriber, priority queue,
pipes and filters, claim check, choreography, async request-reply, scheduling agent
supervisor, sequential convoy.

**Homework:**
1. Implement Queue-Based Load Leveling in front of a bursty workload and show it smooths throughput to the downstream service compared to calling it directly.
2. Build a Pipes and Filters pipeline (e.g., an ETL-style text processor: read → clean → transform → write) where each stage is independently swappable/testable.

### 26. Cloud Data Management Patterns
Sharding, materialized view, index table, event sourcing, CQRS, cache-aside,
static content hosting.

**Homework:**
1. Implement Event Sourcing for a small aggregate (e.g., a shopping cart): store events, not state, and derive current state by replaying them. Add a snapshot optimization.
2. Build a materialized view that's kept in sync (via events or a scheduled job) with a normalized source table, and compare query performance against querying the source directly.

### 27. Reliability & Resiliency Patterns
Circuit breaker, bulkhead, retry, throttling, health endpoint monitoring, leader
election, compensating transaction, deployment stamps, geodes.

**Homework:**
1. Implement a Circuit Breaker wrapping a call to a flaky/slow downstream dependency; demonstrate it transitioning through closed → open → half-open states.
2. Implement the Bulkhead pattern isolating resource pools (e.g., separate thread/connection pools per downstream dependency) and demonstrate that one slow dependency doesn't starve calls to a healthy one.
3. Implement a Compensating Transaction for a multi-step operation that can partially fail (e.g., "reserve inventory" + "charge card" — charge fails, so inventory reservation must be undone).

### 28. Cloud Security Patterns
Federated identity, gatekeeper, valet key.

**Homework:**
1. Implement the Gatekeeper pattern: a thin, restricted-permission proxy service that validates/sanitizes requests before they reach a more privileged backend.
2. Implement the Valet Key pattern: issue a short-lived, scoped access token/URL that lets a client upload directly to storage (e.g., a signed URL) without routing the file through your app server.

---

## Part 8 — The Software Architect Role

### 29. Understanding Software Architecture
What software architecture is, what a software architect does, levels of
architecture (application, solution, enterprise).

**Homework:**
1. Write a one-page Architecture Decision Record (ADR) for a real or hypothetical technical decision (e.g., "choose message broker" or "choose primary datastore"), including context, options considered, decision, and consequences.
2. Take a system you've built in a prior module and describe it at all three levels: application (its internal design), solution (how it fits with adjacent systems), and enterprise (how it fits organizational strategy/standards).

### 30. Architect Responsibilities & Soft Skills
Requirements elicitation, documentation, enforcing standards, collaboration,
consulting/coaching developers, decision making, simplifying things, estimating,
balancing trade-offs, communication.

**Homework:**
1. Run a mock requirements-elicitation session (with a classmate or written scenario) for an ambiguous feature request, and produce a requirements document distinguishing functional vs. non-functional requirements and open questions.
2. Given two competing technical proposals for the same problem (provided or written by classmates), write a decision memo that fairly evaluates trade-offs and makes a recommendation with clear reasoning — practicing decision-making and communication together.

### 31. Architecture Frameworks & Methodologies
TOGAF, UML, BABOK, IAF; project/process methodologies (Agile — Scrum, Kanban,
LeSS, SAFe, XP; PMI, ITIL, Prince2, RUP).

**Homework:**
1. Produce a set of UML diagrams (class diagram + sequence diagram) documenting the design of a system from an earlier module.
2. Compare two process methodologies (e.g., Scrum vs. Kanban) for a specific project scenario (a fast-changing startup product vs. a regulated enterprise system) and justify which fits better and why.

### 32. Security for Architects
Hashing algorithms, PKI, OWASP Top 10, authentication/authorization strategies.

**Homework:**
1. Implement proper password storage (salted hashing with a modern algorithm like bcrypt/argon2) and demonstrate why a naive MD5/SHA1-without-salt approach is broken (e.g., via a rainbow table lookup demo).
2. Pick 3 OWASP Top 10 vulnerabilities, demonstrate each in a small deliberately-vulnerable app, then fix all three and write up the fix.
3. Design an authentication/authorization strategy (diagram) for a multi-service system using a token-based approach (e.g., OAuth2/JWT), showing how identity is established once and trusted across services.

### 33. Operations & DevOps Knowledge
Infrastructure as Code, cloud providers, serverless concepts, containers, CI/CD,
service mesh, Linux/Unix fundamentals.

**Homework:**
1. Containerize an application from a prior module (Dockerfile) and write an Infrastructure-as-Code definition (Terraform, Pulumi, or even a documented CLI script) that provisions what it needs to run.
2. Set up a CI/CD pipeline (GitHub Actions or similar) that builds, tests, and deploys that containerized app automatically on push to main.
3. Deploy the same piece of business logic as both a long-running containerized service and a serverless function; compare cold start, cost model, and operational complexity.

---

## Suggested Capstone

Combine 4–5 modules into one system built over multiple weeks: a small but real
service (e.g., a URL shortener, an event ticketing system, or a job board) designed
with explicit architectural style and patterns (Part 3), built with clean code and
SOLID (Parts 1–2), made horizontally scalable with caching and a message queue
(Parts 4–6), instrumented and made resilient with at least two cloud/reliability
patterns (Part 7), and documented with an ADR and UML diagrams as a software
architect would (Part 8).
