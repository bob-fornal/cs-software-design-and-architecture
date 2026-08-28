# 25. Cloud Messaging Patterns

**Part 7 — Cloud Design Patterns** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Distributed systems fall apart under load and partial failure unless the pieces talk
to each other asynchronously and indirectly — these ten patterns are the standard
vocabulary for how messages flow between services that can't call each other directly
and can't assume the other side is even listening right now.

## Learning objectives
- Can implement Queue-Based Load Leveling to decouple a producer's request rate from a
  consumer's processing rate, and explain why this improves resilience under bursty load.
- Can distinguish Competing Consumers (parallel workers pulling from one queue) from
  Publisher/Subscriber (broadcast to many independent subscribers) and pick the right
  one for a given fan-out requirement.
- Can design a Pipes and Filters pipeline where each stage is independently testable,
  replaceable, and has no knowledge of the stages around it.
- Can explain when to reach for Claim Check (large payload, small reference) and Async
  Request-Reply (synchronous-looking API over an asynchronous backend) instead of
  passing full payloads through a message bus.
- Can describe Priority Queue, Sequential Convoy, Choreography, and Scheduling Agent
  Supervisor well enough to recognize which one solves a given ordering, sequencing, or
  coordination problem in an architecture review.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the bursty API | 5 min | Why calling a downstream service directly breaks under load spikes |
| Queue-Based Load Leveling | 8 min | Decoupling producer and consumer rates with a buffer |
| Competing Consumers | 7 min | Horizontal scale-out of workers pulling from one queue |
| Publisher/Subscriber | 7 min | Broadcast/fan-out vs. point-to-point delivery |
| Priority Queue | 4 min | Ordering delivery by importance, not arrival time |
| Pipes and Filters | 8 min | Composable, swappable processing stages |
| Claim Check | 4 min | Keeping large payloads out of the message bus |
| Choreography | 5 min | Decentralized coordination vs. a central orchestrator |
| Async Request-Reply | 4 min | Giving a sync-looking API an async backend |
| Scheduling Agent Supervisor & Sequential Convoy | 3 min | Coordinating multi-step workflows and strict ordering |

**Hook: the bursty API (5 min).** Picture a checkout service that calls an inventory
service synchronously on every request. Traffic spikes 10x during a flash sale; the
inventory service falls over, and now checkout fails too — one overloaded dependency
takes down everything upstream of it. The fix isn't "add more inventory servers," it's
"stop calling it directly." That reframing is the through-line for the whole session:
almost every pattern here exists to remove a synchronous, tightly-coupled call.

**Queue-Based Load Leveling (8 min).** Put a queue between producer and consumer. The
producer writes messages as fast as it wants; the consumer drains them at whatever rate
it can sustain. The queue absorbs the burst, so the consumer never sees a spike, only a
sustained backlog it works down over time. Draw the throughput graph: direct calls show
a spike that causes errors/timeouts; queued calls show a flat consumer rate with a
temporary queue depth increase. Note the trade-off: added latency and a new failure
mode (unbounded queue growth) that later ties into Topic 27's Throttling.

**Competing Consumers (7 min).** Once there's a queue, scaling the consumer side is just
running more worker instances that all pull from the same queue — each message is
processed by exactly one worker. Contrast with naively broadcasting the same message to
every worker (wrong — that's Pub/Sub's job, not this pattern's). Discuss idempotency
and visibility timeouts / message acknowledgment: a worker crashing mid-processing must
not silently drop the message, and duplicate delivery must be handled (ties back to
Topic 21's idempotent operations homework).

**Publisher/Subscriber (7 min).** Contrast with Competing Consumers directly: Pub/Sub
delivers each message to *every* subscribed consumer group, not just one worker.
Use a concrete example — an "order placed" event that both the shipping service and the
analytics service need to react to independently. Show the topology difference: one
queue with many competing workers vs. one topic with many independent subscriptions,
each behaving like its own queue.

**Priority Queue (4 min).** Not all messages are equal — a paid customer's request or a
security alert may need to jump the line. Implementation options: multiple queues (one
per priority level, drain higher ones first) vs. a single queue with a priority field
the broker sorts on. Warn about starvation of low-priority messages and the need for
aging/fairness safeguards.

**Pipes and Filters (8 min).** Decompose a multi-step process (e.g., ingest → validate
→ transform → enrich → store) into independent filters connected by pipes, each filter
knowing only its input and output shape, not what's upstream or downstream. This is the
messaging-architecture version of the Unix pipeline and of the `compose`/pipeline work
from Topic 3. Emphasize testability: each filter can be unit-tested in isolation by
feeding it fixture input, and stages can be reordered, parallelized, or swapped (e.g.,
replace a JSON parser filter with a CSV parser filter) without touching the others.

**Claim Check (4 min).** Large payloads (a video file, a big document) shouldn't ride
through a message queue — brokers are optimized for small, frequent messages. Store the
payload in blob storage, put only a reference ("claim check") on the queue, and let
consumers fetch the full payload when they need it. This is also a security/cost lever:
smaller messages move faster and cost less to store/replicate in the broker.

**Choreography (5 min).** Contrast with a central orchestrator (which Topic 12's
Microservices discussion and Scheduling Agent Supervisor both touch on): in
choreography, each service reacts to events and emits its own events, with no single
component directing the workflow. Trade-off: no single point of failure or bottleneck,
but harder to see/debug the overall workflow since the logic is smeared across services.

**Async Request-Reply (4 min).** A client wants a synchronous-feeling "submit and get a
result" experience, but the actual work is long-running and asynchronous. Standard
shape: client POSTs, gets back a 202 Accepted with a status URL or correlation ID, then
polls (or gets pushed via websocket/webhook) for the result. This is the pattern behind
most "generate a report" or "process this upload" APIs.

**Scheduling Agent Supervisor & Sequential Convoy (3 min).** Scheduling Agent Supervisor
coordinates a set of distributed steps (possibly across services) as one logical
workflow, tracking progress and handling failure/retry centrally — the orchestrated
counterpart to Choreography. Sequential Convoy guarantees a sequence of related messages
(e.g., events for the same order) is processed in order, typically via a partition/
session key that pins related messages to one consumer. Flag that ordering guarantees
and horizontal scale (Competing Consumers) are in tension — convoy patterns trade some
parallelism for ordering.

## Homework notes

### 1. Implement Queue-Based Load Leveling in front of a bursty workload and show it smooths throughput to the downstream service compared to calling it directly.

**Goal:** Prove — with a measurable before/after — that inserting a queue changes the
*shape* of load a downstream service experiences, not just where the work happens.

**Approach / hints:**
- Build a "downstream service" with a hard concurrency limit (e.g., can only handle 5
  requests/sec before it starts erroring or its latency explodes) — simulate with a
  semaphore and an artificial delay.
- Version A: a producer that calls it directly at a bursty rate (e.g., 50 requests in
  1 second). Record error rate / latency distribution.
- Version B: the same producer pushes to an in-memory or Redis/RabbitMQ queue; a fixed
  pool of workers drains it at a sustainable rate.
- Plot or tabulate queue depth over time and downstream error rate for both versions.
- Stretch: add a max queue size and decide what happens when it's full (reject vs.
  block) — this previews Throttling in Topic 27.

**Starter example:**
```python
import queue, threading, time

work_queue: queue.Queue = queue.Queue(maxsize=1000)

def downstream_call(item):
    # TODO: simulate a rate-limited/slow downstream dependency
    time.sleep(0.1)

def worker():
    while True:
        item = work_queue.get()
        if item is None:
            return
        downstream_call(item)
        work_queue.task_done()

# TODO: start N worker threads, then hammer work_queue.put() in a tight burst
# and compare downstream_call's observed rate to the producer's burst rate.
```

**Definition of done:** Two runnable versions (direct-call and queued) with recorded
metrics (error rate, latency, or downstream request rate over time) showing the queued
version keeps the downstream service within its sustainable rate while the direct-call
version doesn't.

### 2. Build a Pipes and Filters pipeline (e.g., an ETL-style text processor: read → clean → transform → write) where each stage is independently swappable/testable.

**Goal:** Practice designing components that communicate only through a well-defined
input/output contract, with zero knowledge of neighboring stages — the messaging-system
analog of function composition from Topic 3.

**Approach / hints:**
- Define a common filter interface (e.g., `process(input: Iterable[T]) -> Iterable[T]`,
  or a stream-of-records shape) that every stage implements identically.
- Build at least four stages: a reader (source), a cleaner (e.g., strip blank lines/
  normalize whitespace), a transformer (e.g., uppercase, or parse CSV into records),
  and a writer (sink).
- Wire them together with a pipeline runner that just chains `process` calls — the
  runner shouldn't know what any individual filter does.
- Prove swappability: write a second transformer (e.g., a filter instead of a map) and
  swap it in via configuration/composition, not by editing the pipeline runner.
- Unit-test each filter alone with fixture input/output, with no dependency on the rest
  of the pipeline.

**Starter example:**
```typescript
type Filter<T> = (input: Iterable<T>) => Iterable<T>;

function* clean(lines: Iterable<string>): Iterable<string> {
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length > 0) yield trimmed;
  }
}

function pipeline<T>(...filters: Filter<T>[]): Filter<T> {
  return (input) => filters.reduce((acc, f) => f(acc), input);
}

// TODO: implement `transform` and `write` filters, then compose:
// const run = pipeline(clean, transform, write);
```

**Definition of done:** At least four independently unit-tested stages, a pipeline
runner with no stage-specific logic, and a demonstration of swapping one stage without
modifying any other stage or the runner.

## Further resources
- Free companion: [Azure Architecture Center — Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/)
- [Enterprise Integration Patterns — Pipes and Filters](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PipesAndFilters.html)
