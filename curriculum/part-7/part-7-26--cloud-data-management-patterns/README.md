# 26. Cloud Data Management Patterns

**Part 7 — Cloud Design Patterns** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
A single normalized database can't simultaneously be fast to write, fast to read, cheap
to scale, and fully auditable — these patterns are the standard ways to split that one
impossible job across multiple purpose-built representations of the same data.

## Learning objectives
- Can explain Sharding as a horizontal-scaling strategy and pick a shard key for a
  given access pattern while identifying hot-spot risk.
- Can implement Event Sourcing for a small aggregate: store the sequence of events, not
  current state, and derive state by replay — including a snapshot optimization.
- Can build a Materialized View kept in sync with a source table and explain the
  staleness/consistency trade-off against querying the source directly.
- Can implement Cache-Aside correctly, including invalidation on write, and explain why
  it's the default caching pattern for read-heavy workloads (ties to Topic 20).
- Can distinguish Index Table and CQRS from a Materialized View: what each optimizes
  for, and when reaching for one is overkill.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: one table, five conflicting needs | 5 min | Why "just query the database" stops scaling |
| Sharding | 8 min | Horizontal partitioning, shard keys, hot spots, cross-shard queries |
| Event Sourcing | 12 min | Events as the source of truth; replay; snapshots |
| CQRS | 6 min | Separating the write model from the read model |
| Materialized View & Index Table | 8 min | Precomputed/denormalized read shapes kept in sync |
| Cache-Aside | 6 min | The default caching pattern, and invalidation on write |
| Static Content Hosting | 5 min | Taking static assets out of the application tier entirely |

**Hook: one table, five conflicting needs (5 min).** Take a single `orders` table and
list the demands on it: fast writes at checkout, fast reads for "my order history,"
full audit trail for disputes, analytics aggregation across millions of rows, and a
public read-only status page. One normalized table optimized for transactional writes
is bad at most of these. Every pattern in this session is a way of giving one of those
needs its own purpose-built data shape instead of forcing all of them through the same
table.

**Sharding (8 min).** Horizontal partitioning: split one logical table across multiple
physical databases by a shard key (user ID, tenant ID, geographic region). Walk through
picking a shard key for a "users" table at scale (this previews Topic 18's homework
directly) — a poor key (e.g., signup date) creates hot shards; a good key spreads load
evenly. Discuss the cost this imposes: a query that used to be one `JOIN` is now a
fan-out across shards with app-side merging, or is disallowed entirely.

**Event Sourcing (12 min).** Instead of storing current state and overwriting it on
each update, store the immutable sequence of events that led to that state
(`ItemAdded`, `ItemRemoved`, `CartCheckedOut`). Current state is *derived* by replaying
events from the start (or from the last snapshot). Walk a shopping cart example on the
board: three events in, ask "what's the cart total right now?" and derive it live.
Cover why this is valuable — full audit history for free, the ability to replay into a
new read model after a bug fix, temporal queries ("what did the cart look like at 2pm")
— and the cost: replaying a long event stream is slow, which motivates snapshots
(periodically persist derived state so replay only needs events since the last
snapshot).

**CQRS (6 min).** Command Query Responsibility Segregation: separate the model used to
write data from the model used to read it — they can even live in different databases.
Connect directly to Event Sourcing (a very common pairing: events are the write model,
one or more materialized views are the read models) and back to Topic 12, where CQRS
was introduced architecturally; here it's the data-management mechanics of it.

**Materialized View & Index Table (8 min).** A materialized view is a precomputed,
denormalized query result kept up to date (via triggers, events, or a scheduled job)
so expensive joins/aggregations don't run on every read. An index table is the narrower
cousin: a secondary lookup structure keyed by a field the primary store isn't
optimized to query by (e.g., "find order by customer email" when the primary key is
order ID). Emphasize the shared trade-off: both duplicate data for read speed and both
require an explicit sync strategy — the moment you denormalize, staleness becomes a
question you have to answer, not an accident.

**Cache-Aside (6 min).** Quick recap/bridge from Topic 20: application code checks the
cache first, falls back to the source on a miss and populates the cache, and — the part
students most often get wrong — explicitly invalidates or updates the cache entry on
writes to the source. Emphasize this is the default because the cache only ever holds
what's actually been read, unlike write-through, which populates on every write whether
or not it's ever read.

**Static Content Hosting (5 min).** The simplest data-management move of all: assets
that don't change per-request (images, videos, compiled JS/CSS, downloadable files)
don't belong behind the application tier at all — serve them directly from blob
storage/a CDN. Connect to Topic 16's CDN discussion and to Claim Check from Topic 25:
both are instances of "keep bulk payloads out of the path that has to stay fast and
cheap."

## Homework notes

### 1. Implement Event Sourcing for a small aggregate (e.g., a shopping cart): store events, not state, and derive current state by replaying them. Add a snapshot optimization.

**Goal:** Internalize that "current state" is a derived, cached view of history, not
the primary fact — the core mental shift Event Sourcing requires.

**Approach / hints:**
- Define an append-only event log (in-memory list or a simple table) for one aggregate
  instance, e.g. a cart: `ItemAdded`, `ItemRemoved`, `CartCheckedOut`.
- Write a pure `apply(state, event) -> state` reducer and a `replay(events) -> state`
  function that folds over the whole event list from empty state.
- Prove correctness: generate a sequence of events, replay them, and compare against
  state you compute by hand/independently.
- Add snapshotting: every N events (or on demand), persist the current derived state
  alongside the event count/id it was computed at. On load, start replay from the
  snapshot instead of from event zero, and only fold the events since then.
- Measure/demonstrate the speedup: replay time for a long event stream with vs. without
  using the snapshot.

**Starter example:**
```python
from dataclasses import dataclass, field

@dataclass
class CartState:
    items: dict[str, int] = field(default_factory=dict)
    checked_out: bool = False

def apply(state: CartState, event: dict) -> CartState:
    # TODO: handle "ItemAdded", "ItemRemoved", "CartCheckedOut"
    return state

def replay(events: list[dict], start: CartState | None = None) -> CartState:
    state = start or CartState()
    for event in events:
        state = apply(state, event)
    return state

# TODO: add save_snapshot(state, event_index) / load_snapshot() and have
# replay() resume from the latest snapshot instead of event zero.
```

**Definition of done:** An append-only event store, a working replay function proven
correct against hand-computed expected state, and a snapshot mechanism that
measurably reduces the number of events replayed on load without changing the result.

### 2. Build a materialized view that's kept in sync (via events or a scheduled job) with a normalized source table, and compare query performance against querying the source directly.

**Goal:** Feel the actual performance win a denormalized read model buys, and confront
the sync-strategy decision that comes with it.

**Approach / hints:**
- Set up a normalized schema requiring a non-trivial join/aggregation for a common
  query (e.g., `orders` + `order_items` + `products` to get "total spent per customer").
- Build the materialized view as a separate table/structure holding the precomputed
  answer, and pick a sync strategy: update it synchronously on write, update it from an
  event (if you did homework 1, this pairs naturally), or refresh it on a schedule.
- Benchmark the same logical query against the normalized source (live join) vs. the
  materialized view (direct read) at a meaningfully large data volume (thousands of
  rows minimum) and record the timing difference.
- Explicitly answer: how stale can the view get under your sync strategy, and what
  would break if a consumer needed strongly consistent reads?

**Starter example:**
```python
# Normalized query (recomputed every time)
def total_spent_live(db, customer_id):
    ...  # JOIN orders, order_items, products; SUM per customer

# Materialized view, kept in a simple table: customer_totals(customer_id, total)
def refresh_customer_total(db, customer_id):
    total = total_spent_live(db, customer_id)
    db.upsert("customer_totals", customer_id=customer_id, total=total)

def total_spent_view(db, customer_id):
    return db.get("customer_totals", customer_id=customer_id)

# TODO: call refresh_customer_total() from wherever orders are written (or from
# an event handler / cron job), then benchmark total_spent_live vs. total_spent_view.
```

**Definition of done:** A working materialized view with an explicit, documented sync
strategy, a benchmark comparing it against the live-join query at realistic data
volume, and a written note on the staleness window and what workloads that window
would and wouldn't be acceptable for.

## Further resources
- Free companion: [Azure Architecture Center — Design Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/)
- Martin Fowler, [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
