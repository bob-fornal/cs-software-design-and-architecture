# 20. Caching Strategies

**Part 5 — Data at Scale** · [Back to curriculum index](../../README.md)

## One-sentence pitch
Caching is the cheapest performance win in system design, but every caching strategy is really a decision about who's allowed to see stale data and for how long — get that decision wrong and you've traded latency for silent correctness bugs.

## Learning objectives
- Can implement a cache-aside layer in front of a slow data-access function, including correct invalidation on writes.
- Can distinguish cache-aside, read-through/refresh-ahead, write-through, and write-behind, and choose the right one for a given latency/consistency requirement.
- Can name the caching layers a request passes through (client, CDN, web server, application, database) and what each is good at caching.
- Can explain the failure modes of write-behind caching (e.g., a crash before the write is flushed) and describe a mitigation.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the fix that was one line and 100x | 5 min | A slow endpoint made fast by wrapping it in a cache — then broken by stale data on the next deploy. Frames caching as "easy to add, easy to get subtly wrong." |
| Caching layers across the stack | 10 min | Trace a single request through every layer that might cache it: browser/client cache, CDN (static assets, sometimes API responses), web server cache, application-level cache (in-process or shared like Redis/Memcached), and database query/buffer cache. Each layer trades off scope (how many requests it can serve from cache) against staleness risk. |
| Cache-aside | 10 min | The default pattern: app checks cache, falls back to the data source on miss, populates the cache, and explicitly invalidates or updates the cache entry on writes. Discuss the "thundering herd" risk on a cold cache and cache stampede mitigations (locking, jitter). |
| Read-through & refresh-ahead | 8 min | Read-through: the cache itself owns the fetch-on-miss logic, so the app only ever talks to the cache. Refresh-ahead: proactively refresh hot keys before they expire, trading extra background load for fewer cold misses. |
| Write-through vs. write-behind | 12 min | Write-through: write to cache and backing store synchronously — simple, strongly consistent, slower writes. Write-behind (write-back): write to cache immediately, flush to the backing store asynchronously — fast writes, but data loss risk if the process crashes before the flush. Walk through the crash-before-flush failure mode explicitly. |
| Wrap-up & homework framing | 5 min | Tie back to the two homework assignments: one is "add a cache," the other is "compare two write strategies under failure." |

## Homework notes

### 1. Add a cache-aside layer with invalidation

> Add a cache-aside layer in front of a slow data-access function in a toy app; include cache invalidation on writes and measure the before/after latency.

- **Goal:** Tests whether the student can implement the single most common caching pattern correctly — specifically, whether invalidation actually fires on every write path that could make the cached value stale.
- **Approach / hints:** Start with a deliberately slow read function (e.g., `time.sleep(0.2)` standing in for a slow query or external call) and a corresponding write function that mutates the same underlying data. Wrap the read path with a cache-aside check: on a hit, skip the slow path entirely; on a miss, call through and populate the cache. On every write, invalidate (or update) the corresponding cache entry — don't just leave it to expire on TTL alone. Measure wall-clock latency for a sequence of reads before adding the cache, then after, including one read immediately after a write to prove the invalidation actually took effect (i.e., you don't serve stale data).
- **Starter example:**
  ```python
  import time

  cache = {}

  def slow_get_user(user_id, db):
      time.sleep(0.2)  # stand-in for a slow query
      return db[user_id]

  def get_user_cached(user_id, db):
      if user_id in cache:
          return cache[user_id]
      value = slow_get_user(user_id, db)
      cache[user_id] = value
      return value

  def update_user(user_id, db, new_data):
      db[user_id] = new_data
      cache.pop(user_id, None)  # invalidate — don't just wait for TTL
  ```
- **Definition of done:** A cache-aside wrapper with working invalidation on write, a before/after latency comparison (numbers, not just "it felt faster"), and one test showing a read right after a write returns the updated value rather than a stale cached one.

### 2. Compare write-through and write-behind under failure

> Implement write-through vs. write-behind caching for the same write path and discuss the durability/consistency trade-off and failure modes (e.g., crash before flush) of each.

- **Goal:** Tests whether the student understands that write-behind's speed comes from a real durability trade-off, not a free lunch — and can reason concretely about what's lost when the async flush never happens.
- **Approach / hints:** Implement the same write operation two ways against the same toy "backing store" (a dict or file standing in for a database). Write-through: write to cache and backing store in the same call, return only after both succeed. Write-behind: write to cache, queue the backing-store write (a background thread, or just a list of pending writes flushed later), and return immediately. Then simulate a crash: for write-behind, kill the process (or just skip the flush step) before the queued write is applied, and show that the backing store is now missing data the cache had already reported as "written." Write up what a real system does to reduce this risk (write-ahead log, periodic/forced flush, accepting the risk for non-critical data).
- **Starter example:**
  ```python
  backing_store = {}
  cache = {}
  pending_writes = []  # write-behind queue

  def write_through(key, value):
      backing_store[key] = value  # durable immediately
      cache[key] = value

  def write_behind(key, value):
      cache[key] = value          # fast: caller sees success now
      pending_writes.append((key, value))  # flushed later, e.g. by a background loop

  def flush_pending():
      while pending_writes:
          key, value = pending_writes.pop(0)
          backing_store[key] = value

  # Simulate a crash: call write_behind(...) then never call flush_pending()
  # -> cache has the value, backing_store does not.
  ```
- **Definition of done:** Both write paths implemented against a shared backing store, a demonstrated crash scenario for write-behind where the backing store ends up missing data the cache already accepted, and a short written comparison of the durability/latency trade-off between the two.

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
- [MDN — HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching) — free, canonical reference for client and CDN-layer caching behavior (cache-control, validation, freshness).
