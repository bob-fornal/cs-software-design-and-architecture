# 19. NoSQL Database Types

**Part 5 — Data at Scale** · [Back to curriculum index](../../README.md)

## One-sentence pitch
"NoSQL" isn't one thing — key-value, document, wide-column, and graph stores each optimize for a different access pattern, and picking the wrong one buys you all of the flexibility cost and none of the performance win.

## Learning objectives
- Can classify a NoSQL database into key-value, document, wide-column, or graph and describe its underlying data model in one sentence.
- Can map a given access pattern (session cache, catalog, time-series, social graph) to the best-fit NoSQL type with a concrete justification.
- Can model the same small domain in both a document store and a graph store and write an equivalent query in each.
- Can articulate what a NoSQL database gives up relative to an RDBMS (joins, multi-record transactions, ad hoc query flexibility) in exchange for its scaling properties.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: "just use NoSQL" is not a strategy | 5 min | A quick story of a team that moved to a document store for scale and then reimplemented joins in application code. Frames the session: NoSQL types are specialized tools, not a blanket upgrade from SQL. |
| Key-value & document stores | 12 min | Key-value: opaque blob behind a key, O(1) lookup, no query language (Redis, DynamoDB as key-value). Document stores: schema-flexible JSON/BSON documents, secondary indexes, querying into nested structure (MongoDB). Discuss when flexible schema is a feature vs. a liability. |
| Wide-column stores | 8 min | Column-family model (Cassandra, HBase, Bigtable): rows keyed by a partition key + clustering columns, optimized for high write throughput and time-ordered data. Contrast with a relational table — no joins, denormalization is the default design stance. |
| Graph databases | 10 min | Nodes, edges, and properties; index-free adjacency makes multi-hop traversal (friends-of-friends) cheap where it's expensive in a relational join chain. Cover when a graph model actually earns its complexity vs. when a document/relational model with a few extra columns is good enough. |
| Matching workload to database type | 10 min | Walk through the four homework scenarios live (session cache, product catalog, sensor time-series, social graph) and reason through each as a group before assigning homework. |
| Wrap-up | 5 min | Recap: the access pattern drives the data model choice, not the other way around. |

## Homework notes

### 1. Model a social domain in a document store and a graph database

> Model the same domain (e.g., a social network's "friends" and posts) in a document store and a graph database; implement one representative query in each and compare.

- **Goal:** Tests whether the student can see the same domain through two different data models and feel where each one makes a query natural vs. awkward — specifically, multi-hop relationship queries.
- **Approach / hints:** Keep the domain small: users, a `friends` relationship, and posts authored by users. In the document store, decide (and justify) whether friends are embedded arrays of IDs or a separate collection, and whether posts are embedded in the user document or separate. In the graph model, represent users as nodes and `FRIENDS_WITH`/`AUTHORED` as edges. Pick one query that's genuinely harder in one model than the other — "posts by friends-of-friends" is a good choice, since it's a 2-hop traversal that's cheap in a graph and requires either multiple round-trips or app-side joins in a document store. You don't need a live database cluster — SQLite/a Python dict for the document side and a small adjacency-list structure (or an actual graph DB like Neo4j's free tier / embedded option) for the graph side are both fine.
- **Starter example:**
  ```python
  # Document-store shape (e.g., MongoDB-style)
  users = {
      "u1": {"name": "Ada", "friend_ids": ["u2", "u3"]},
      "u2": {"name": "Bob", "friend_ids": ["u1", "u4"]},
  }
  posts = [{"id": "p1", "author_id": "u2", "text": "..."}]

  # Friends-of-friends query: app-side traversal, one round trip per hop
  def friends_of_friends(uid):
      direct = users[uid]["friend_ids"]
      fof = set()
      for f in direct:
          fof.update(users[f]["friend_ids"])
      return fof - {uid} - set(direct)
  ```
  ```cypher
  // Equivalent graph query (Cypher) — one query, no app-side loop
  MATCH (me:User {id: $uid})-[:FRIENDS_WITH]->()-[:FRIENDS_WITH]->(fof)
  WHERE NOT (me)-[:FRIENDS_WITH]->(fof) AND fof.id <> $uid
  RETURN DISTINCT fof
  ```
- **Definition of done:** Working (even if minimal/in-memory) implementations of both models with the same seed data, one query implemented in each, and a short written comparison of what each approach required (round trips, code complexity, or query readability).

### 2. Match scenarios to NoSQL types and build one example

> Given four scenarios (session cache, product catalog, sensor time-series, social graph), match each to the best-fit NoSQL type with a one-paragraph justification, then build a minimal working example for one of them.

- **Goal:** Tests the ability to reason from access pattern to data model choice on demand, without defaulting to whatever database the student happens to know best.
- **Approach / hints:** For each scenario, name the dominant access pattern first (point lookup by key? flexible/nested queries? high-volume timestamped writes? multi-hop relationship traversal?), then pick the type that fits: session cache → key-value (TTL, pure key lookup); product catalog → document (varying attributes per product category, queried by multiple fields); sensor time-series → wide-column (append-heavy, partitioned by device + time range); social graph → graph (relationship traversal). Then build the minimal example for whichever one you have real tooling for — a Redis (or plain dict-with-TTL) session cache is the easiest to stand up without infrastructure.
- **Starter example:**
  ```python
  import time

  class SessionCache:
      """Minimal key-value store with TTL, standing in for Redis."""
      def __init__(self):
          self._store = {}  # key -> (value, expires_at)

      def set(self, key, value, ttl_seconds=1800):
          self._store[key] = (value, time.time() + ttl_seconds)

      def get(self, key):
          entry = self._store.get(key)
          if not entry:
              return None
          value, expires_at = entry
          if time.time() > expires_at:
              del self._store[key]
              return None
          return value
  ```
- **Definition of done:** Four scenario-to-type mappings, each with a one-paragraph justification tied to the access pattern (not just "it's popular"), plus one working minimal example with a couple of sanity-check calls (write, read, and — where relevant — expiry/miss behavior).

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
- [Redis documentation — Data types](https://redis.io/docs/latest/develop/data-types/) — free, canonical reference for key-value data modeling.
- [MongoDB Manual — Data Modeling](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/) — free, canonical reference for document store design trade-offs (embedding vs. referencing).
