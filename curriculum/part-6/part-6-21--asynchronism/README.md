# 21. Asynchronism

**Part 6 — Asynchronous & Distributed Communication** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
The moment a request handler does something slow, you have to choose between making
the user wait and making the work happen somewhere else — asynchronism is the
discipline of doing the "somewhere else" part without losing or duplicating work.

## Learning objectives
- Can distinguish event-driven background jobs (triggered by something happening) from
  schedule-driven ones (triggered by a clock) and pick the right one for a given task.
- Can explain the difference between a message queue (general pub/sub, potentially
  many consumer types) and a task queue (work items destined for a specific kind of
  worker) and when each is the better fit.
- Can build a producer/consumer pipeline that offloads slow work out of a request path.
- Can define idempotency precisely and make an operation safe to process twice.
- Can explain back pressure, demonstrate a producer overwhelming a consumer, and apply
  at least one mitigation (bounded queue + reject, or rate limiting).

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the slow request | 5 min | A request handler that resizes an image or sends an email inline; show the latency cost and the failure mode when the downstream service is slow |
| Event-driven vs. schedule-driven jobs | 8 min | "Something happened" vs. "it's time" — webhooks/events vs. cron; when to combine them (scheduled retry sweep for failed events) |
| Message queues vs. task queues | 10 min | Pub/sub topics with multiple subscriber types vs. a work queue with one consumer pool; brokers (Redis, RabbitMQ, SQS, Kafka) as points on this spectrum |
| Producer/consumer mechanics | 8 min | Enqueue from the request handler, acknowledge-on-completion, visibility timeout / redelivery, dead-letter queues |
| Back pressure | 8 min | What happens when producers outpace consumers; bounded queues, rejection, rate limiting, and why unbounded queues just delay the outage |
| Idempotent operations | 8 min | At-least-once delivery is the default; idempotency keys, natural idempotency (SET vs. INCREMENT), and dedup stores |
| Wrap-up / homework framing | 3 min | Tie the three homework projects back to the three pillars: offload, idempotency, back pressure |

**Hook: the slow request (5 min).** Start with a request handler that calls an image
resizer or an email API synchronously inside an HTTP POST. Ask what happens to p99
latency, and what happens to the whole request if the downstream call hangs. The fix
isn't "make it faster" — it's "don't make the caller wait for it."

**Event-driven vs. schedule-driven jobs (8 min).** Event-driven: a job fires because
something happened (a file was uploaded, an order was placed) — usually via a queue
message or webhook. Schedule-driven: a job fires because a clock said so (nightly
report, hourly cleanup, a cron-triggered retry sweep). Many real systems need both: an
event-driven job does the work, and a schedule-driven job cleans up anything the
event-driven path missed (failed messages, stuck jobs).

**Message queues vs. task queues (10 min).** A message queue is a general-purpose
transport for messages between components — potentially many kinds of producers and
consumers, often pub/sub (Kafka topics, RabbitMQ exchanges). A task queue is narrower:
discrete units of work destined for a pool of interchangeable workers (Celery, Sidekiq,
SQS-backed workers). Draw the spectrum: Kafka (durable log, many subscriber types) →
RabbitMQ (flexible routing) → Redis list / SQS (simple task queue) → in-memory queue
(single process, no durability). Emphasize the trade-off: durability and fan-out
flexibility versus operational simplicity.

**Producer/consumer mechanics (8 min).** The request handler enqueues a message and
returns immediately. A separate worker process dequeues, does the slow work, and
acknowledges. Cover visibility timeout (message becomes invisible while being
processed, reappears if the worker crashes before ack) and dead-letter queues (a
message that fails repeatedly gets moved aside instead of looping forever).

**Back pressure (8 min).** If producers can enqueue faster than consumers can drain,
the queue grows without bound — memory pressure, latency spikes, and eventually an
outage that's worse than if you'd rejected work up front. Two mitigations: a bounded
queue that rejects (or applies back pressure to the producer, e.g. HTTP 429) once full,
and rate limiting the producer directly. Contrast with unbounded queues, which just
postpone the failure and make it bigger.

**Idempotent operations (8 min).** Most real queues offer at-least-once delivery, not
exactly-once — a consumer crash after processing but before acknowledging causes
redelivery. An idempotent consumer produces the same end state whether it processes a
message once or five times. Techniques: idempotency keys (store "already processed
message ID X" and short-circuit), natural idempotency (`SET balance = 100` is
idempotent; `balance += 10` is not), and dedup stores with a TTL.

**Wrap-up (3 min).** Each homework maps to one pillar: offloading work (1), making that
work safe to repeat (2), and keeping a slow consumer from being drowned (3).

## Homework notes

### 1. Build a producer/consumer task queue for a slow operation

**Goal:** Prove you can move slow work out of the request/response path using a real
(or in-memory) queue, and understand the producer/consumer/broker roles.

**Approach / hints:**
- Pick a slow operation: resizing an image, "sending" an email (can be a stub that
  sleeps and logs), or generating a PDF.
- Producer: an HTTP handler that validates the request, pushes a job payload onto a
  queue (Redis list, RabbitMQ queue, or even a `queue.Queue` / async in-memory queue
  for a single-process demo), and returns a `202 Accepted` with a job ID immediately.
- Consumer: a separate worker loop (separate process or thread) that pulls jobs,
  performs the slow operation, and writes a result/status somewhere the client can poll.
- Measure and report request latency before and after moving the work off the request
  path.

**Starter example (Python, Redis-backed):**
```python
import json, uuid, redis

r = redis.Redis()
QUEUE_KEY = "jobs:image_resize"

def enqueue_job(image_url: str) -> str:
    job_id = str(uuid.uuid4())
    payload = {"job_id": job_id, "image_url": image_url, "status": "queued"}
    r.hset(f"job:{job_id}", mapping=payload)
    r.rpush(QUEUE_KEY, job_id)
    return job_id  # handler returns this immediately, 202 Accepted

def worker_loop():
    while True:
        _, job_id = r.blpop(QUEUE_KEY)  # blocks until work arrives
        job_id = job_id.decode()
        r.hset(f"job:{job_id}", "status", "processing")
        # TODO: do the actual slow resize here
        r.hset(f"job:{job_id}", "status", "done")
```

**Definition of done:** A request handler that returns quickly regardless of the
operation's true duration, a separate consumer that performs the work, a way to check
job status/result, and a short before/after latency comparison.

### 2. Make a consumer idempotent and prove it with a duplicate delivery

**Goal:** Understand that at-least-once delivery means duplicates *will* happen, and
know the standard techniques for making reprocessing a duplicate message harmless.

**Approach / hints:**
- Take the consumer from homework 1 (or a new one) and pick an operation that would be
  unsafe to run twice if done naively — e.g. "credit a user's account by $10" or
  "increment a counter."
- Add an idempotency key: before processing, check a "processed message IDs" store
  (a set, a database table with a unique constraint, a Redis `SETNX`). If the ID is
  already present, skip the side effect and return the previous result.
- Write a test that constructs the same message twice (same idempotency key), delivers
  both to the consumer, and asserts the side effect happened exactly once.

**Starter example (Python):**
```python
processed_ids: set[str] = set()  # swap for a durable store in a real system

def handle_message(message: dict) -> None:
    msg_id = message["idempotency_key"]
    if msg_id in processed_ids:
        return  # already applied — safe no-op
    apply_side_effect(message)  # e.g. credit_account(message["user_id"], message["amount"])
    processed_ids.add(msg_id)

# Test: deliver the same message twice, assert apply_side_effect ran once.
```

**Definition of done:** A consumer that produces the same end state whether a given
message is delivered once or twice, plus a test that explicitly delivers a duplicate
and asserts no double side effect occurred.

### 3. Simulate back pressure and mitigate it

**Goal:** Experience what happens when a producer outpaces a consumer, and apply a
concrete mitigation rather than just describing the concept.

**Approach / hints:**
- Build a fast producer (loop enqueuing as fast as possible) and a deliberately slow
  consumer (sleep per item) against an unbounded queue. Record queue depth and memory
  or latency over time — it should grow without bound.
- Implement one mitigation: (a) a bounded queue that rejects/returns an error once full
  (`queue.Queue(maxsize=N)` raising `Full`, or an HTTP 429 from the producer-facing
  endpoint), or (b) rate-limit the producer to roughly the consumer's drain rate
  (token bucket or simple sleep-based throttle).
- Re-run the same load and document queue depth / rejection rate / latency before and
  after the mitigation, side by side.

**Starter example (Python, bounded queue):**
```python
import queue, threading, time

q = queue.Queue(maxsize=100)  # bounded — the mitigation

def producer():
    for i in range(10_000):
        try:
            q.put_nowait(i)
        except queue.Full:
            record_rejection(i)  # TODO: count/log rejected items

def consumer():
    while True:
        item = q.get()
        time.sleep(0.05)  # deliberately slow
        q.task_done()
```

**Definition of done:** A documented "before" run showing unbounded queue growth (or
its consequence) under a fast producer/slow consumer, a documented "after" run with the
mitigation applied showing bounded growth or controlled rejection, and a short
explanation of the trade-off the mitigation introduces (dropped work vs. throttled
producer).

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
