# 23. Performance Antipatterns

**Part 6 — Asynchronous & Distributed Communication** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Most production performance problems aren't exotic algorithmic complexity bugs —
they're one of a handful of named, recognizable antipatterns (chatty I/O, no caching,
retry storms) that you can learn to spot on sight and fix with a standard playbook.

## Learning objectives
- Can name and recognize each of the nine antipatterns (busy database/frontend, chatty
  I/O, extraneous fetching, improper instantiation, monolithic persistence, no
  caching, noisy neighbor, retry storm, synchronous I/O) from a code sample or symptom
  description.
- Can identify an N+1 query pattern (chatty I/O) in real code and rewrite it as a
  batched fetch.
- Can identify extraneous fetching (pulling a whole row/object for one field) and
  narrow the fetch to just what's needed.
- Can reproduce a retry storm under load and fix it with exponential backoff + jitter.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the site that's slow "for no reason" | 5 min | A page with a reasonable query plan that still times out under load — antipatterns hide in interaction, not single queries |
| I/O-shaped antipatterns | 15 min | Chatty I/O (N+1), extraneous fetching, synchronous I/O — the "too many trips, too much data, blocking too long" family |
| Resource-shaped antipatterns | 12 min | Busy database/frontend, monolithic persistence, improper instantiation — doing too much work in the wrong place, or too often |
| Caching and neighbor antipatterns | 8 min | No caching, noisy neighbor — leaving free wins on the table, and one tenant starving another |
| Retry storms | 10 min | Naive retry amplifying load on an already-struggling service; exponential backoff + jitter as the standard fix |
| Wrap-up / homework framing | 5 min | Pattern-matching these from a code review, not just a textbook |

**Hook (5 min).** Present a page/endpoint whose individual query looks fine in
isolation (`SELECT * FROM orders WHERE id = ?`) but the endpoint is slow under
realistic load. The point: performance antipatterns are almost always about
*interaction* — how many times you do something, and how much you fetch each time —
not about a single query being badly written.

**I/O-shaped antipatterns (15 min).**
- *Chatty I/O / N+1:* looping over a list and issuing one query (or one HTTP call) per
  item instead of a single batched call. Show the classic ORM N+1: fetch 50 orders,
  then lazily fetch each order's customer in a loop — 51 queries instead of 2.
- *Extraneous fetching:* pulling every column of a row (or a whole downstream
  response body) when only one field is needed — wasted bandwidth and
  deserialization cost, and it hides real cost behind a "it works" query.
- *Synchronous I/O:* blocking a thread/request on a network call that could be
  parallelized, streamed, or moved off the critical path entirely (this is the
  connective tissue back to Topic 21 — Asynchronism).

**Resource-shaped antipatterns (12 min).**
- *Busy database / busy frontend:* pushing computation that belongs in the
  application layer down into the database (or up into the client) until that tier
  becomes the bottleneck — e.g. heavy business logic in stored procedures, or a
  frontend re-rendering/re-computing on every keystroke.
- *Monolithic persistence:* using a single data store for every access pattern
  (transactional writes, full-text search, analytics) when each pattern would be
  far cheaper on a store designed for it.
- *Improper instantiation:* recreating an expensive-to-construct object (a DB
  connection, an HTTP client, a crypto context) on every request instead of reusing
  or pooling it.

**Caching and neighbor antipatterns (8 min).**
- *No caching:* recomputing or re-fetching identical results repeatedly when a cache
  with a sane invalidation strategy would eliminate most of the repeated work
  (preview of Topic 20 — Caching Strategies).
- *Noisy neighbor:* one tenant/workload consuming a shared resource (CPU, DB
  connections, disk I/O) so aggressively that other tenants on the same
  infrastructure degrade — the fix is usually quotas, throttling, or isolation.

**Retry storms (10 min).** A downstream service gets slow or starts erroring. Clients
retry immediately on failure. The retries add load to the already-struggling service,
which gets slower, which triggers more retries — a self-reinforcing collapse. The fix:
exponential backoff (each retry waits longer than the last) plus jitter (randomize the
wait so many clients don't retry in lockstep), and a cap on total retries or a circuit
breaker to stop retrying altogether once failure is persistent.

**Wrap-up (5 min).** These antipatterns are meant to be pattern-matched in a code
review, not identified from a formal definition — that's exactly what both homework
assignments exercise.

## Homework notes

### 1. Fix chatty I/O and extraneous fetching in a provided code sample

**Goal:** Recognize an N+1 query pattern and an over-wide fetch in real code (not just
a description of them), and know the standard fix for each.

**Approach / hints:**
- Write (or use) a sample that lists N parent records and then, in a loop, issues a
  separate query per parent to fetch a related child (classic ORM lazy-loading N+1).
- Fix chatty I/O with a batched fetch: a single `WHERE id IN (...)` query, a JOIN, or
  an ORM eager-load (`select_related`/`prefetch_related` in Django,
  `joinedload`/`selectinload` in SQLAlchemy).
- Separately, find or introduce a spot that fetches an entire row/object
  (`SELECT *` or a full API response) when only one field is used downstream. Narrow
  it to `SELECT that_field` or a partial API response/projection.
- Measure query count and/or payload size before and after each fix.

**Starter example (Python, SQLAlchemy-style before/after):**
```python
# Before — chatty I/O: 1 query for orders + N queries for customers
orders = session.query(Order).all()
for order in orders:
    print(order.customer.name)  # triggers a separate SELECT per order

# After — batched with eager loading
from sqlalchemy.orm import joinedload
orders = session.query(Order).options(joinedload(Order.customer)).all()
for order in orders:
    print(order.customer.name)  # customer already loaded, no extra query

# Extraneous fetching — before: whole row for one field
customer = session.query(Customer).get(customer_id)
email = customer.email

# After — fetch only what's needed
email = session.query(Customer.email).filter_by(id=customer_id).scalar()
```

**Definition of done:** The provided sample's query count drops from O(N) to O(1) (or
a small constant) for the chatty-I/O fix, the extraneous-fetch fix narrows the
retrieved data to just the field(s) used, and a before/after query-count or
payload-size comparison is documented.

### 2. Reproduce a retry storm and fix it with exponential backoff + jitter

**Goal:** Experience how naive retries amplify load on a struggling service, and apply
the standard mitigation rather than just describing it.

**Approach / hints:**
- Build a toy "flaky service" that fails (or is slow) above some concurrent-request
  threshold — e.g. it errors if more than 10 requests arrive within 1 second.
- Build a naive client that retries immediately (no delay) on failure, and run enough
  concurrent clients to push the service past its threshold. Record total requests
  hitting the service and the error rate — it should show cascading, sustained
  failure once the storm starts.
- Rewrite the client to use exponential backoff (delay doubles each retry, up to a
  cap) with jitter (add randomness to each delay) and a maximum retry count. Re-run
  the same load and compare requests-to-the-service and error rate.
- Document both runs side by side (a small table or chart of requests/sec and error
  rate over time is enough — no need for a full load-testing framework).

**Starter example (Python):**
```python
import random, time

def call_with_backoff(fn, max_retries=5, base_delay=0.1, max_delay=5.0):
    for attempt in range(max_retries):
        try:
            return fn()
        except ServiceError:
            if attempt == max_retries - 1:
                raise
            delay = min(max_delay, base_delay * (2 ** attempt))
            delay *= random.uniform(0.5, 1.5)  # jitter
            time.sleep(delay)

# Before: naive retry — call_with_backoff(fn, max_retries=5, base_delay=0)
# and no jitter — reproduces the storm. Compare against the version above.
```

**Definition of done:** A reproducible "before" run showing a retry storm (sustained
high error rate / request volume against the struggling service), a reproducible
"after" run using exponential backoff + jitter showing reduced load and/or faster
recovery, and both results documented together.

## Further resources
- Free companion: Azure Architecture Center, [Antipatterns](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/)
