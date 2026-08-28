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

### 2. Programming Paradigms
Structured programming, functional programming, object-oriented programming — what
problem each paradigm solves and when to reach for it.

**Homework:**
1. Implement the same small algorithm (e.g., word-frequency counter) three ways: purely structured/procedural, purely functional (no mutation, no loops — recursion/map/filter/reduce only), and OOP (objects with state and behavior). Write a short comparison of readability and testability.
2. Take an existing imperative/OOP codebase snippet and convert its core logic to a functional-core/imperative-shell design, isolating side effects at the edges.

### 3. Object-Oriented Programming
Encapsulation, abstraction, inheritance, polymorphism, interfaces, scope/visibility,
abstract vs. concrete classes, domain models vs. anemic models, class variants,
domain language, layered architectures.

**Homework:**
1. Model a domain (e.g., a library, a parking garage, a board game) with a proper class hierarchy demonstrating encapsulation, inheritance, and polymorphism — include at least one abstract class and two interfaces.
2. Take an "anemic" domain model (data classes + separate service classes doing all the logic) and refactor it into a rich domain model where behavior lives with the data it operates on. Justify each move.
3. Design a small layered application (presentation → domain → data) for a simple use case and diagram how objects at each layer talk to each other.

---

## Part 2 — Design Principles & Patterns

### 4. Core Design Principles
Composition over inheritance, encapsulate what varies, program against abstractions,
the Hollywood Principle, Law of Demeter, Tell Don't Ask.

**Homework:**
1. Take a class hierarchy that uses deep inheritance to handle variation (e.g., `FlyingDuck extends Duck`, `RubberDuck extends Duck` with an overridden `fly()` that throws) and refactor it to use composition/strategy objects instead.
2. Refactor a piece of code that violates the Law of Demeter (chains like `a.getB().getC().doThing()`) and Tell-Don't-Ask (lots of getters used to make external decisions) into a version where objects are told what to do.

### 5. SOLID Principles
Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation,
Dependency Inversion.

**Homework:**
1. Take a "God class" (does validation, persistence, notification, and formatting) and split it to satisfy SRP and DIP, injecting dependencies rather than constructing them internally.
2. Build a small plugin-style system (e.g., pluggable payment methods or export formats) that is Open/Closed — adding a new type requires adding a class, not editing existing ones.
3. Write a short design review flagging SOLID violations in a provided ~150-line file, one violation per principle where present, each with a proposed fix.

### 6. DRY & YAGNI
Don't Repeat Yourself vs. premature abstraction; You Aren't Gonna Need It vs.
under-engineering.

**Homework:**
1. Given a codebase with 3–4 near-duplicate functions, extract the shared abstraction — but write a short justification for *where* you drew the line (over-abstracting duplicated-looking-but-conceptually-different code is a common trap).
2. Given an over-engineered mini-framework (config-driven, plugin-based) built to solve a problem that only ever has one implementation, strip it down to the simplest thing that works, and write down what you'd need to see before re-adding the abstraction.

### 7. Design Patterns (GoF & PoSA)
Creational, structural, and behavioral Gang of Four patterns; Patterns of Software
Architecture (PoSA) patterns for concurrency and distributed systems.

**Homework:**
1. Pick 3 GoF patterns from different categories (e.g., Factory Method, Decorator, Observer) and implement each in a small, realistic scenario — not the textbook example. Include a note on what problem it solved and what it would look like *without* the pattern.
2. Refactor a piece of conditional-heavy code (a big `switch`/`if-else` selecting behavior) into the Strategy pattern, and a piece of tightly-coupled notification code into Observer.
3. Research and implement one PoSA concurrency pattern (e.g., Half-Sync/Half-Async or Leader/Followers) in a toy multi-threaded or async task processor.

---

## Part 3 — Architectural Foundations

### 8. Architectural Principles
Component principles, policy vs. detail, coupling and cohesion, boundaries.

**Homework:**
1. Take a monolithic module and identify its "policy" (business rules) vs. "detail" (I/O, frameworks, UI). Redraw it as a diagram with a boundary line and explain what should never cross it.
2. Audit a real or provided codebase for coupling and cohesion: identify the two most tightly coupled modules and propose a boundary/interface that would decouple them.

### 9. Architectural Styles
Layered, client-server, peer-to-peer, event-driven, publish-subscribe, component-based,
monolithic, distributed.

**Homework:**
1. Design (diagram + short write-up) the same simple system — e.g., a chat app — under two different architectural styles: layered client-server vs. event-driven pub-sub. Compare trade-offs in latency, coupling, and failure handling.
2. Build a minimal working pub-sub message dispatcher (in-process is fine) and a minimal layered equivalent of the same feature; compare code structure.

### 10. Architectural Patterns
MVC, Domain-Driven Design, Microservices, Microkernel, Blackboard, Serverless,
Event Sourcing, SOA, CQRS.

**Homework:**
1. Build a small feature using MVC, then re-architect the same feature using CQRS (separate command/query models). Document what changed and why you would/wouldn't do this for a real feature this size.
2. Take a single well-defined bounded context (e.g., "order fulfillment") and apply DDD tactically: identify entities, value objects, aggregates, and a repository interface — no implementation required, just the design.
3. Sketch a decomposition of a monolithic app (provided or one from a prior assignment) into 3–4 microservices, including how they'd communicate (sync vs. async) and what data each would own.

### 11. Enterprise Application Patterns
DTOs, identity maps, use cases, repositories, mappers, transaction script, commands/
queries, value objects, domain models, entities, ORMs.

**Homework:**
1. Implement a Repository + DTO pattern in front of a simple data store (in-memory or SQLite): domain objects never leak past the repository boundary, and API responses use DTOs, not entities.
2. Compare Transaction Script vs. Domain Model for the same use case (e.g., "apply a discount to an order"): implement both, then write a short comparison of when each is the better choice.

---

## Part 4 — System Design Fundamentals

### 12. Core System Design Concepts
Performance vs. scalability, latency vs. throughput, availability vs. consistency,
CAP theorem (CP vs. AP).

**Homework:**
1. Write a short design memo for a hypothetical system (e.g., a URL shortener) explicitly stating whether it favors CP or AP under partition, and why, referencing CAP theorem trade-offs.
2. Given three system scenarios (e.g., banking ledger, social media feed, chat delivery receipts), classify each as prioritizing consistency or availability and justify the choice.

### 13. Consistency & Availability Patterns
Weak/eventual/strong consistency; failover (active-active, active-passive);
replication (master-slave, master-master); availability in numbers (99.9%, 99.99%)
and in parallel vs. sequence.

**Homework:**
1. Calculate theoretical availability for a system with components in series vs. parallel (given per-component uptime %) and propose a redundancy change to hit "four nines."
2. Design a replication strategy (diagram) for a read-heavy service using master-slave replication; describe what breaks under eventual consistency and how the UI/client should handle stale reads.

### 14. DNS, CDNs & Load Balancers
Domain Name System resolution; push vs. pull CDNs; load balancers vs. reverse
proxies; load balancing algorithms; Layer 4 vs. Layer 7.

**Homework:**
1. Diagram the full request path from a browser typing a URL to a response, labeling where DNS resolution, CDN caching, and load balancing occur.
2. Configure a local reverse proxy/load balancer (e.g., Nginx or a simple custom one) in front of 2–3 instances of a toy app, and demonstrate round-robin vs. least-connections behavior.

### 15. Scaling Applications
Horizontal scaling, stateless application layers, microservices at scale, service
discovery.

**Homework:**
1. Take a stateful toy web app (sessions stored in memory) and refactor it to be horizontally scalable (externalize session state), then simulate running 2+ instances behind a load balancer.
2. Implement a minimal service discovery mechanism (even a shared registry file/service) for 2–3 toy services that need to find each other's addresses at runtime.

---

## Part 5 — Data at Scale

### 16. Databases at Scale
SQL vs. NoSQL, replication, sharding, federation, denormalization, SQL tuning, RDBMS.

**Homework:**
1. Given a normalized relational schema that's slow on a specific read-heavy query, denormalize it strategically and measure/explain the trade-off (write complexity vs. read speed).
2. Design a sharding strategy for a large hypothetical table (e.g., "users" at 500M rows): pick a shard key, explain hot-spot risks, and describe how a cross-shard query would be handled.

### 17. NoSQL Database Types
Key-value stores, document stores, wide-column stores, graph databases — access
patterns and when each fits.

**Homework:**
1. Model the same domain (e.g., a social network's "friends" and posts) in a document store and a graph database; implement one representative query in each and compare.
2. Given four scenarios (session cache, product catalog, sensor time-series, social graph), match each to the best-fit NoSQL type with a one-paragraph justification, then build a minimal working example for one of them.

### 18. Caching Strategies
Cache-aside, read-through/refresh-ahead, write-through, write-behind; client, CDN,
web server, application, and database caching layers.

**Homework:**
1. Add a cache-aside layer in front of a slow data-access function in a toy app; include cache invalidation on writes and measure the before/after latency.
2. Implement write-through vs. write-behind caching for the same write path and discuss the durability/consistency trade-off and failure modes (e.g., crash before flush) of each.

---

## Part 6 — Asynchronous & Distributed Communication

### 19. Asynchronism
Background jobs (event-driven vs. schedule-driven), message queues, task queues,
back pressure, idempotent operations.

**Homework:**
1. Build a producer/consumer task queue (e.g., using Redis, RabbitMQ, or an in-memory queue) for a slow operation (image resize, email send) offloaded from a request handler.
2. Make one of your queue consumers idempotent (safe to process the same message twice) and write a test that proves it by delivering a duplicate message.
3. Simulate back pressure: have a fast producer overwhelm a slow consumer and implement one mitigation (bounded queue + reject, or rate limiting) with before/after behavior documented.

### 20. Communication Protocols
HTTP, TCP, UDP, RPC, REST, gRPC, GraphQL.

**Homework:**
1. Implement the same simple API (e.g., "get user by id", "list posts") as both a REST endpoint and a GraphQL resolver; compare over/under-fetching for a client that only needs 2 of 8 fields.
2. Build a minimal gRPC service and client for a small use case, and write a short comparison of gRPC vs. REST for internal service-to-service calls.

### 21. Performance Antipatterns
Busy database/frontend, chatty I/O, extraneous fetching, improper instantiation,
monolithic persistence, no caching, noisy neighbor, retry storm, synchronous I/O.

**Homework:**
1. Given a provided code sample exhibiting "chatty I/O" (N+1 query pattern) and "extraneous fetching" (fetching whole rows/objects when only one field is needed), identify both and fix them.
2. Write a small load-test/demo that reproduces a "retry storm" (naive retry-on-failure with no backoff overwhelming a struggling service) and fix it with exponential backoff + jitter.

### 22. Monitoring & Observability
Health, availability, performance, security, and usage monitoring; instrumentation;
visualization & alerts.

**Homework:**
1. Instrument a toy service with basic metrics (request count, error rate, p95 latency) and a `/health` endpoint, then wire up a simple dashboard (even a local Grafana/Prometheus stack or a rolled-your-own chart).
2. Define and implement 3 alert conditions (e.g., error rate > 5%, p95 latency > 500ms, health check failing) for your instrumented service, and simulate each condition to prove the alert fires.

---

## Part 7 — Cloud Design Patterns

### 23. Cloud Messaging Patterns
Queue-based load leveling, competing consumers, publisher/subscriber, priority queue,
pipes and filters, claim check, choreography, async request-reply, scheduling agent
supervisor, sequential convoy.

**Homework:**
1. Implement Queue-Based Load Leveling in front of a bursty workload and show it smooths throughput to the downstream service compared to calling it directly.
2. Build a Pipes and Filters pipeline (e.g., an ETL-style text processor: read → clean → transform → write) where each stage is independently swappable/testable.

### 24. Cloud Data Management Patterns
Sharding, materialized view, index table, event sourcing, CQRS, cache-aside,
static content hosting.

**Homework:**
1. Implement Event Sourcing for a small aggregate (e.g., a shopping cart): store events, not state, and derive current state by replaying them. Add a snapshot optimization.
2. Build a materialized view that's kept in sync (via events or a scheduled job) with a normalized source table, and compare query performance against querying the source directly.

### 25. Reliability & Resiliency Patterns
Circuit breaker, bulkhead, retry, throttling, health endpoint monitoring, leader
election, compensating transaction, deployment stamps, geodes.

**Homework:**
1. Implement a Circuit Breaker wrapping a call to a flaky/slow downstream dependency; demonstrate it transitioning through closed → open → half-open states.
2. Implement the Bulkhead pattern isolating resource pools (e.g., separate thread/connection pools per downstream dependency) and demonstrate that one slow dependency doesn't starve calls to a healthy one.
3. Implement a Compensating Transaction for a multi-step operation that can partially fail (e.g., "reserve inventory" + "charge card" — charge fails, so inventory reservation must be undone).

### 26. Cloud Security Patterns
Federated identity, gatekeeper, valet key.

**Homework:**
1. Implement the Gatekeeper pattern: a thin, restricted-permission proxy service that validates/sanitizes requests before they reach a more privileged backend.
2. Implement the Valet Key pattern: issue a short-lived, scoped access token/URL that lets a client upload directly to storage (e.g., a signed URL) without routing the file through your app server.

---

## Part 8 — The Software Architect Role

### 27. Understanding Software Architecture
What software architecture is, what a software architect does, levels of
architecture (application, solution, enterprise).

**Homework:**
1. Write a one-page Architecture Decision Record (ADR) for a real or hypothetical technical decision (e.g., "choose message broker" or "choose primary datastore"), including context, options considered, decision, and consequences.
2. Take a system you've built in a prior module and describe it at all three levels: application (its internal design), solution (how it fits with adjacent systems), and enterprise (how it fits organizational strategy/standards).

### 28. Architect Responsibilities & Soft Skills
Requirements elicitation, documentation, enforcing standards, collaboration,
consulting/coaching developers, decision making, simplifying things, estimating,
balancing trade-offs, communication.

**Homework:**
1. Run a mock requirements-elicitation session (with a classmate or written scenario) for an ambiguous feature request, and produce a requirements document distinguishing functional vs. non-functional requirements and open questions.
2. Given two competing technical proposals for the same problem (provided or written by classmates), write a decision memo that fairly evaluates trade-offs and makes a recommendation with clear reasoning — practicing decision-making and communication together.

### 29. Architecture Frameworks & Methodologies
TOGAF, UML, BABOK, IAF; project/process methodologies (Agile — Scrum, Kanban,
LeSS, SAFe, XP; PMI, ITIL, Prince2, RUP).

**Homework:**
1. Produce a set of UML diagrams (class diagram + sequence diagram) documenting the design of a system from an earlier module.
2. Compare two process methodologies (e.g., Scrum vs. Kanban) for a specific project scenario (a fast-changing startup product vs. a regulated enterprise system) and justify which fits better and why.

### 30. Security for Architects
Hashing algorithms, PKI, OWASP Top 10, authentication/authorization strategies.

**Homework:**
1. Implement proper password storage (salted hashing with a modern algorithm like bcrypt/argon2) and demonstrate why a naive MD5/SHA1-without-salt approach is broken (e.g., via a rainbow table lookup demo).
2. Pick 3 OWASP Top 10 vulnerabilities, demonstrate each in a small deliberately-vulnerable app, then fix all three and write up the fix.
3. Design an authentication/authorization strategy (diagram) for a multi-service system using a token-based approach (e.g., OAuth2/JWT), showing how identity is established once and trusted across services.

### 31. Operations & DevOps Knowledge
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
