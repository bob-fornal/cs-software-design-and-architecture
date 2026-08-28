# 27. Reliability & Resiliency Patterns

**Part 7 — Cloud Design Patterns** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
In a distributed system something is always failing somewhere, so resilience isn't
about preventing failure — it's about a small catalog of patterns that contain a
failure's blast radius so one bad dependency doesn't take down everything that touches it.

## Learning objectives
- Can implement a Circuit Breaker and demonstrate it transitioning through closed →
  open → half-open states in response to a failing dependency.
- Can implement the Bulkhead pattern to isolate resource pools per dependency and
  demonstrate that a slow/failing dependency doesn't starve calls to a healthy one.
- Can implement a Compensating Transaction to undo a completed step of a multi-step
  operation when a later step fails, in the absence of a distributed transaction.
- Can explain Retry with backoff/jitter and Throttling, and articulate why naive
  unbounded retry makes outages worse (retry storms), tying back to Topic 23.
- Can describe Health Endpoint Monitoring, Leader Election, Deployment Stamps, and
  Geodes well enough to identify which one addresses a given reliability requirement.

## Session outline (~60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the cascading outage | 5 min | How one slow dependency takes down an unrelated one |
| Retry & Throttling | 8 min | Backoff, jitter, and protecting yourself from your own retries |
| Circuit Breaker | 10 min | Closed / open / half-open; failing fast on purpose |
| Bulkhead | 8 min | Isolating resource pools so one dependency can't starve another |
| Compensating Transaction | 10 min | Undoing completed steps when a later step fails, without 2PC |
| Health Endpoint Monitoring | 5 min | Making "is this instance healthy" a first-class query |
| Leader Election | 6 min | Coordinating exactly-one-actor work across replicas |
| Deployment Stamps & Geodes | 8 min | Scaling reliability out geographically/by tenant, not just per-instance |

**Hook: the cascading outage (5 min).** Trace a real shape of incident: Service A calls
Service B, which is slow today. A's threads/connections all block waiting on B. A's own
health check starts failing because it's out of capacity — not because A itself is
broken. Now A's callers see failures too, and the outage has spread to a service that
never touched B directly. Nothing here needed a *bug* — just an unbounded dependency
with no isolation. Every pattern in this session is a way of putting a boundary around
that spread.

**Retry & Throttling (8 min).** Retry: a transient failure (a dropped connection, a
momentary timeout) often succeeds on a second attempt, so blind failure is wasteful.
But naive immediate retry-in-a-loop is how a struggling service gets finished off — this
is the retry storm from Topic 23's homework. Fix: exponential backoff (wait longer
between each attempt) plus jitter (randomize the wait so a thundering herd of clients
doesn't retry in lockstep). Throttling is the mirror image: a service protecting
*itself* by rejecting or delaying requests once it's near capacity, rather than
degrading for everyone. Frame them as offense (retry, from the caller) and defense
(throttle, from the callee).

**Circuit Breaker (10 min).** Wrap a call to a flaky dependency in a breaker with three
states: **closed** (calls pass through normally, failures are counted), **open** (after
too many failures, calls fail immediately without even attempting the dependency — this
is failing *fast* on purpose, protecting both the caller's resources and the struggling
dependency), and **half-open** (after a cooldown, let a small number of trial calls
through to test recovery — success closes the breaker again, failure reopens it).
Live-code or diagram the state machine on the board. Emphasize the key insight: a
circuit breaker's job during an outage is to stop calling the dependency, not to keep
trying harder.

**Bulkhead (8 min).** Named for ship compartments that keep one hull breach from
sinking the whole vessel. Give each downstream dependency its own resource pool (thread
pool, connection pool, semaphore) instead of one shared pool for everything. If
Dependency B is slow and exhausts *its* pool, calls to healthy Dependency C still have
capacity because they were never competing for the same pool. Connect back to the hook:
Bulkhead is the direct fix for "A's threads all blocked on B took down A's calls to C."

**Compensating Transaction (10 min).** Distributed operations spanning multiple
services can't use a single ACID transaction. When step 2 of a multi-step operation
fails after step 1 already committed, the fix is an explicit compensating action that
semantically undoes step 1 — not a rollback, a deliberate inverse operation (e.g.,
"release the reservation" as the compensation for "reserve inventory," since the
reservation may already be visible to other parts of the system). Walk the classic
example: reserve inventory → charge card fails → release inventory reservation.
Emphasize that compensations must be designed per-operation and are often not perfect
inverses (a "cancel shipment" compensation for an already-picked order looks different
from simply un-reserving stock).

**Health Endpoint Monitoring (5 min).** Expose a `/health` (or `/ready` vs. `/live`)
endpoint that reports whether an instance can actually do its job — not just "the
process is running," but "can it reach its database, is it out of capacity." Connect to
Topic 24's monitoring instrumentation and to load balancers (Topic 16) that use health
checks to pull unhealthy instances out of rotation automatically.

**Leader Election (6 min).** Some work must be done by exactly one instance at a time
(a scheduled job, a singleton coordinator) even though the service runs many replicas
for availability. Leader election lets replicas agree on which one is "it" right now,
and re-elect automatically if the leader dies. Keep it conceptual — name the mechanism
(a coordination service like a consensus-backed lock, e.g., via ZooKeeper/etcd/a
database row lock) without requiring implementation.

**Deployment Stamps & Geodes (8 min).** Both patterns scale reliability *out* rather
than *up*. Deployment Stamps: deploy independent, fully isolated copies ("stamps") of
the whole application stack per customer/tenant/region, so one stamp's failure or noisy
neighbor doesn't affect any other stamp. Geodes: distribute the same deployable unit
across multiple geographic regions, each capable of serving any request, so a region
outage or high-latency user is routed elsewhere. Contrast both with simple horizontal
scaling (more identical instances behind one load balancer, still one blast radius):
these patterns are about isolating blast radius by tenant or geography, not just adding
capacity.

## Homework notes

### 1. Implement a Circuit Breaker wrapping a call to a flaky/slow downstream dependency; demonstrate it transitioning through closed → open → half-open states.

**Goal:** Build the actual state machine, not just call a library — understand exactly
what triggers each transition and what "failing fast" means in code.

**Approach / hints:**
- Build a fake downstream dependency you can control: force it to fail N times in a
  row, then recover, so you can drive the breaker through every transition on demand.
- Track failure count (or failure rate over a rolling window) in the **closed** state;
  trip to **open** once a threshold is crossed.
- In **open**, reject calls immediately (raise/return an error without invoking the
  dependency) until a cooldown timer expires, then move to **half-open**.
- In **half-open**, allow exactly one (or a small fixed number of) trial call(s) through
  — success transitions back to **closed** (reset failure count), failure transitions
  back to **open** (reset cooldown timer).
- Log or print every state transition with a timestamp so the closed → open →
  half-open → closed sequence is visible in the output of a demo run.

**Starter example:**
```python
import time
from enum import Enum

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=3, cooldown_seconds=5):
        self.state = State.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.opened_at = None

    def call(self, fn, *args):
        # TODO: if OPEN and cooldown elapsed -> HALF_OPEN
        # TODO: if OPEN and cooldown not elapsed -> raise immediately, don't call fn
        # TODO: try fn(*args); on success reset/close; on failure increment/trip
        ...
```

**Definition of done:** A runnable demo where a controllable dependency's failures
drive the breaker from closed to open, a cooldown elapses into half-open, and a
subsequent success or failure resolves back to closed or open — with each transition
visibly logged.

### 2. Implement the Bulkhead pattern isolating resource pools (e.g., separate thread/connection pools per downstream dependency) and demonstrate that one slow dependency doesn't starve calls to a healthy one.

**Goal:** Prove resource isolation actually works by measuring it, not just asserting it
conceptually.

**Approach / hints:**
- Build two fake downstream dependencies: Dependency B (artificially slow/hanging) and
  Dependency C (fast, healthy).
- Baseline (no isolation): one shared thread pool / connection pool of limited size
  serving calls to both B and C. Flood it with calls to B and show calls to C start
  timing out or queuing behind B's calls.
- Fixed version: give B and C separate pools (e.g., separate `ThreadPoolExecutor`
  instances, or separate semaphores bounding concurrent calls to each). Repeat the same
  flood of B calls and show C's calls are unaffected — similar latency/success rate as
  when B isn't under load at all.
- Report concrete numbers: C's p95 latency (or success rate) with and without bulkhead
  isolation, under identical load against B.

**Starter example:**
```python
from concurrent.futures import ThreadPoolExecutor
import time

# Shared pool (no isolation) — TODO: show this fails under load
shared_pool = ThreadPoolExecutor(max_workers=4)

# Isolated pools — TODO: show this survives the same load
pool_b = ThreadPoolExecutor(max_workers=2)
pool_c = ThreadPoolExecutor(max_workers=2)

def call_dependency_b():
    time.sleep(5)  # simulates a hung/slow dependency
    return "B ok"

def call_dependency_c():
    time.sleep(0.05)
    return "C ok"

# TODO: submit a flood of call_dependency_b() and a steady stream of
# call_dependency_c() through the shared pool, then through the isolated pools,
# and compare C's observed latency in each scenario.
```

**Definition of done:** A before/after demo with measured latency or success-rate data
for calls to the healthy dependency, showing it degrades under the shared-pool baseline
but stays healthy once isolated in its own bulkhead.

### 3. Implement a Compensating Transaction for a multi-step operation that can partially fail (e.g., "reserve inventory" + "charge card" — charge fails, so inventory reservation must be undone).

**Goal:** Practice designing an explicit undo step for a distributed operation, and
confront that compensations are domain-specific logic, not an automatic rollback.

**Approach / hints:**
- Model at least two services/steps with independent state: an inventory service
  (`reserve(item, qty)` / `release(reservation_id)`) and a payment service
  (`charge(amount)` that you can force to fail).
- Implement the happy path first: reserve succeeds, charge succeeds, operation complete.
- Implement the failure path: reserve succeeds, charge fails — the orchestrating code
  must call the inventory service's compensating action (`release`) so the reservation
  doesn't leak.
- Prove it: after a forced charge failure, assert/inspect that the inventory reservation
  no longer exists (or is marked released) — not just that an error was logged.
- Stretch: make the compensation itself fallible (release fails too) and decide how you
  handle that — retry the compensation, or record it for manual follow-up. This is the
  edge every "just add a rollback" mental model misses.

**Starter example:**
```python
class InventoryService:
    def reserve(self, item: str, qty: int) -> str:
        ...  # returns a reservation_id
    def release(self, reservation_id: str) -> None:
        ...  # compensating action

class PaymentService:
    def charge(self, amount: float) -> str:
        ...  # raises on failure

def place_order(inventory: InventoryService, payment: PaymentService, item, qty, amount):
    reservation_id = inventory.reserve(item, qty)
    try:
        payment.charge(amount)
    except Exception:
        # TODO: compensate — undo the reservation, then re-raise or return a
        # clear failure result to the caller.
        raise
    return reservation_id
```

**Definition of done:** A working demo showing the happy path completing normally and
the failure path leaving no orphaned reservation — verified by inspecting inventory
state after a forced payment failure, plus a short written note on what happens if the
compensating action itself fails.

## Further resources
- Free companion: Azure Architecture Center, [Reliability design patterns](https://learn.microsoft.com/en-us/azure/well-architected/reliability/design-patterns)
- Martin Fowler, [CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html)
