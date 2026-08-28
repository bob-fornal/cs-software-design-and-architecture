# 12. Architectural Patterns — Homework Notes

[Back to topic index](README.md) · [Back to curriculum index](../../README.md)

### 1. MVC, then CQRS, same feature
> Build a small feature using MVC, then re-architect the same feature using CQRS (separate command/query models). Document what changed and why you would/wouldn't do this for a real feature this size.

- **Goal:** Tests whether students understand CQRS as a *trade-off*, not a strictly-better upgrade — the exercise should make the added complexity tangible, not just theoretical.
- **Approach / hints:** Pick a small, well-scoped feature — "apply a discount to an order" (matches the topic 13 homework, so reuse is fine) or similar. Build it once as classic MVC: one `Order` model with the discount logic, a controller, a view. Then rebuild as CQRS: a command (`ApplyDiscountCommand`) handled by a command handler that enforces the rule and writes state, and a separate query/read model shaped for display. Decide and document how the read side stays in sync with the write side (direct call, or an event). The write-up should explicitly answer: for a feature this small, was CQRS worth it? What would need to be true (traffic pattern, team size, read/write ratio) for the answer to flip?
- **Starter example:** See [`examples/mvc_order.py`](examples/mvc_order.py) and [`examples/cqrs_order.py`](examples/cqrs_order.py) for skeletons of each version.
- **Definition of done:** Two working (or near-working) versions of the same feature — one MVC, one CQRS — plus a short written comparison that names at least one concrete cost CQRS introduced (extra sync step, eventual consistency, more files) and a judgment call on whether it's worth it here.

### 2. DDD tactical design for a bounded context
> Take a single well-defined bounded context (e.g., "order fulfillment") and apply DDD tactically: identify entities, value objects, aggregates, and a repository interface — no implementation required, just the design.

- **Goal:** Tests whether students can distinguish entities from value objects (identity vs. attribute-equality) and correctly draw an aggregate boundary — the most commonly misapplied part of tactical DDD.
- **Approach / hints:** Pick a bounded context with enough shape to be interesting but not sprawling — "order fulfillment," "hotel booking," or "library lending" all work. List the nouns in the domain, then for each ask: does it have an identity that persists even if all its attributes change (entity), or is it fully defined by its current attributes and safely replaceable (value object)? Group entities/value objects into aggregates, each with exactly one root that's the only thing external code is allowed to reference directly — enforce this rule explicitly in the write-up. Finish with a repository interface (method signatures only) for each aggregate root, e.g. `find_by_id`, `save` — no implementation.
- **Definition of done:** A design document (diagram or structured list is fine) naming each entity, value object, and aggregate with its root clearly marked, plus at least one repository interface with method signatures — no code implementation required.

### 3. Monolith to microservices decomposition
> Sketch a decomposition of a monolithic app (provided or one from a prior assignment) into 3–4 microservices, including how they'd communicate (sync vs. async) and what data each would own.

- **Goal:** Tests whether students can find seams along business capability (not just technical layers) and reason about the sync/async trade-off for each cross-service interaction — the two hardest judgment calls in real decomposition work.
- **Approach / hints:** Start from a monolith you already have (e.g., the layered app from topic 4's homework, or a provided one). List its major responsibilities and group them by business capability, not by technical layer — "everything about orders" is a service candidate, "everything about the database" is not. For each proposed service, name what data it exclusively owns (no shared tables) and how other services get that data (an API call, or a published event). For each inter-service interaction, justify sync (needs an immediate answer, e.g. "is this in stock?") vs. async (fire-and-forget or eventually-consistent, e.g. "order was placed, notify shipping"). A diagram with services as boxes and arrows labeled sync/async is the deliverable core.
- **Definition of done:** A diagram showing 3-4 services, each with the data it owns, and every inter-service arrow labeled as synchronous or asynchronous with a one-line justification.

## Further resources
- Free companion: *[Software Engineering: A Modern Approach](https://softengbook.org/chapter7), Ch. 7* · Eric Evans, [DDD Reference](https://www.domainlanguage.com/ddd/reference/)
