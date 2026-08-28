# 18. Databases at Scale

**Part 5 — Data at Scale** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Every system eventually outgrows a single database instance, and the choices you make about replication, sharding, and normalization at that point determine whether scaling is a tuning exercise or a rewrite.

## Learning objectives
- Can explain when to reach for SQL vs. NoSQL for a given workload, in terms of consistency, query flexibility, and scale characteristics — not brand preference.
- Can design a leader-follower (or multi-leader) replication topology for a given read/write ratio and explain its replication-lag failure modes.
- Can design a sharding strategy for a large table: choose a shard key, identify hot-spot risk, and describe how a cross-shard query gets executed.
- Can denormalize a specific slow read path and articulate exactly what write-side complexity was traded for it.
- Can read a slow query and propose a concrete fix (index, rewrite, or schema change) using `EXPLAIN`-style reasoning.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the query that broke prod | 5 min | A read query that was fine at 10K rows and fell over at 10M. Frame the whole session as "the database is the last thing to scale — and the hardest to undo." |
| SQL vs. NoSQL, RDBMS fundamentals | 10 min | Not "SQL vs NoSQL" as a war — as a spectrum of consistency/flexibility trade-offs. Cover what an RDBMS actually guarantees (ACID, schema enforcement, joins) and where those guarantees start to cost you at scale. |
| Scaling reads: replication | 10 min | Leader-follower replication, read replicas, replication lag and stale reads. Multi-leader/multi-region briefly, and why it reintroduces conflict resolution. |
| Scaling writes: sharding & federation | 12 min | Sharding (horizontal partitioning) vs. federation (splitting by domain/service). Shard key selection, hot spots (e.g., sequential IDs or a popular tenant), and how cross-shard queries/joins get handled (scatter-gather, denormalized lookup tables, or avoiding them entirely). |
| Denormalization & SQL tuning | 10 min | Denormalization as a deliberate trade: faster reads, more complex/riskier writes (dual-write bugs, drift). SQL tuning basics: indexes, covering indexes, `EXPLAIN` plans, N+1 query patterns. |
| Wrap-up & homework framing | 3 min | Tie back to the two homework assignments — one is a denormalization trade-off, the other is a from-scratch sharding design. |

## Homework notes

### 1. Denormalize a slow read-heavy query

> Given a normalized relational schema that's slow on a specific read-heavy query, denormalize it strategically and measure/explain the trade-off (write complexity vs. read speed).

- **Goal:** Tests whether the student can identify *where* normalization is costing you (usually a join fan-out or aggregate computed at read time) and make a deliberate, bounded trade — not "denormalize everything."
- **Approach / hints:** Start with a schema that has a real join penalty — e.g., `orders` → `order_items` → `products`, with a dashboard query that sums order totals per user. Use `EXPLAIN ANALYZE` (or your DB's equivalent) to see the join/aggregate cost before changing anything. Denormalize narrowly: add a computed `order_total` column, or a `user_order_summary` table updated on write, rather than collapsing the whole schema. Measure query latency before/after with realistic data volume (seed thousands of rows, not ten). Write down what now has to stay in sync manually, and how (trigger, application code, background job).
- **Starter example:**
  ```sql
  -- Before: total computed at read time via join + aggregate
  SELECT o.id, SUM(oi.quantity * p.price) AS total
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  JOIN products p ON p.id = oi.product_id
  WHERE o.user_id = :user_id
  GROUP BY o.id;

  -- After: denormalized column maintained on write
  ALTER TABLE orders ADD COLUMN total_cents INTEGER;

  -- Application (or trigger) responsibility on every order_items write:
  UPDATE orders
  SET total_cents = (
    SELECT SUM(oi.quantity * p.price_cents)
    FROM order_items oi JOIN products p ON p.id = oi.product_id
    WHERE oi.order_id = orders.id
  )
  WHERE id = :order_id;
  ```
- **Definition of done:** A before/after schema, the actual query plans or timing numbers for both versions, and a short written explanation of what write path now has to maintain the denormalized data and what happens if that write path is skipped or fails.

### 2. Design a sharding strategy for a 500M-row table

> Design a sharding strategy for a large hypothetical table (e.g., "users" at 500M rows): pick a shard key, explain hot-spot risks, and describe how a cross-shard query would be handled.

- **Goal:** Tests whether the student understands sharding as a data-distribution problem, not just "split the table in half" — specifically, whether they can reason about access patterns and failure modes before picking a key.
- **Approach / hints:** Consider realistic candidate keys for `users` (user_id, region, signup_date, hash of email) and evaluate each against: even distribution, whether the app's most common queries can be routed to a single shard, and rebalancing cost as shards grow. Explicitly call out hot-spot scenarios — e.g., sharding by signup_date puts all new signups on one shard; sharding by region concentrates traffic where your biggest market is. Describe at least one cross-shard query (e.g., "find all users named X" or "count total active users") and how you'd execute it: scatter-gather with fan-out and merge, a secondary lookup index, or a denormalized aggregate maintained separately.
- **Definition of done:** A short design document (prose + diagram is fine, no code required) naming the chosen shard key, at least one hot-spot risk and mitigation, and a concrete walkthrough of one cross-shard query showing how results get assembled.

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
- [Use The Index, Luke](https://use-the-index-luke.com/) — a free, practical guide to SQL indexing and query performance that pairs well with the tuning segment.
