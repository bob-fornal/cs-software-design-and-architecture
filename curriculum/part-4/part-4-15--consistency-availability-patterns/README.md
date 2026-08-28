# 15. Consistency & Availability Patterns

**Part 4 — System Design Fundamentals** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
CAP theorem tells you which side of the trade-off to pick; this session gives you
the concrete mechanisms — consistency models, failover strategies, replication
topologies, and the availability math behind "the nines" — that actually implement
that choice in a real system.

## Learning objectives
- Differentiate weak, eventual, and strong consistency with a concrete example of
  what a client could observe under each.
- Compare active-active vs. active-passive failover and state a scenario favoring
  each.
- Compare master-slave vs. master-master replication, including the conflict risk
  multi-master writes introduce.
- Calculate system availability for components in series and in parallel from
  per-component uptime percentages.
- Design a replication topology for a read-heavy service and describe the
  client/UI handling required to cope with staleness.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Consistency models | 12 min | Weak, eventual, strong — with examples |
| Failover strategies | 8 min | Active-active vs. active-passive |
| Replication topologies | 12 min | Master-slave vs. master-master |
| Availability math | 15 min | Nines, series vs. parallel, redundancy |
| Wrap-up | 8 min | Tie replication + availability into one design |

**Consistency models (12 min).** *Weak consistency*: after a write, reads may or
may not see it, with no guarantee of when they will (e.g., some UDP-based video
streams — a dropped frame is just gone). *Eventual consistency*: after a write,
if no new writes happen, all replicas *will* eventually converge to the same
value, but there's a window where reads can return stale data (classic example:
DNS propagation, or old-style S3 read-after-write on overwrites). *Strong
consistency*: a read is guaranteed to return the most recent write, achieved via
synchronous replication or a consensus protocol (Raft/Paxos) — at the cost of
latency and, per CAP, availability during a partition. Anchor with a single
running example (e.g., a "like count") shown under each model.

**Failover strategies (8 min).** *Active-passive*: one primary serves all
traffic, a standby replica sits idle (or serves nothing) and is promoted on
failure. Simple to reason about, but wastes standby capacity and has a
detection-plus-promotion gap (real downtime, however brief). *Active-active*:
multiple nodes serve traffic simultaneously; no failover pause when one dies,
but now you need to keep them in sync and resolve conflicting concurrent writes
— it trades an operational simplicity problem for a data consistency problem.

**Replication topologies (12 min).** *Master-slave (single-leader)*: one node
accepts writes, propagates to read replicas; simple mental model, no write
conflicts, but replicas lag behind the master (replication lag) and all writes
bottleneck through one node. *Master-master (multi-leader)*: multiple nodes
accept writes and replicate to each other; scales write throughput and survives
a single node loss without a promotion step, but concurrent writes to the same
record on different masters can conflict — needs a resolution strategy
(last-write-wins, vector clocks, CRDTs, or application-level merge logic).

**Availability math (15 min).** Uptime percentages translate to real downtime:
99% ≈ 3.65 days/year, 99.9% ("three nines") ≈ 8.76 hours/year, 99.99% ("four
nines") ≈ 52.6 minutes/year, 99.999% ≈ 5.26 minutes/year. *Series* (a request
must pass through component A **and** B): combined availability = A × B — a
chain is only as reliable as the product of its links, and adding a component
in series always lowers availability. *Parallel* (either replica can serve the
request): combined availability = 1 − (1−A) × (1−B) — redundancy in parallel
raises availability, since both must fail simultaneously to cause an outage.
This is the mechanism behind "add a second instance to hit four nines."

## Homework notes

### 1. Series vs. parallel availability calculation
> Calculate theoretical availability for a system with components in series vs.
> parallel (given per-component uptime %) and propose a redundancy change to hit
> "four nines."

**Goal:** tests quantitative fluency with the series/parallel availability
formulas and the ability to identify the weakest link in a chain.

**Approach / hints:** Pick a realistic request path with 3-4 components in
series (e.g., load balancer 99.99%, app server 99.95%, database 99.9%). Multiply
them to get the combined series availability — it'll be visibly worse than any
single component. Identify the weakest link (usually the database here), then
recompute treating *that one component* as two in parallel using the parallel
formula. Show the before/after numbers and state whether four nines (99.99%,
≈52.6 min/year downtime) is actually reached — if not, say what else would need
to change.

**Starter example:**
```python
def series_availability(*uptimes):
    result = 1.0
    for u in uptimes:
        result *= u
    return result

def parallel_availability(*uptimes):
    failure = 1.0
    for u in uptimes:
        failure *= (1 - u)
    return 1 - failure

components = [0.9999, 0.9995, 0.999]  # LB, app server, database
print(series_availability(*components))
```

**Definition of done:** submission shows the computed series availability for
the original design, identifies the bottleneck component, shows the recomputed
availability after adding parallel redundancy to that component, and states in
one sentence whether the four-nines target is met.

### 2. Master-slave replication design for a read-heavy service
> Design a replication strategy (diagram) for a read-heavy service using
> master-slave replication; describe what breaks under eventual consistency and
> how the UI/client should handle stale reads.

**Goal:** tests the ability to connect a replication topology to its real
user-facing consequences, not just draw boxes and arrows.

**Approach / hints:** Diagram one master (accepts writes) feeding N read
replicas behind a load balancer that serves read traffic; writes go straight to
the master. Call out replication lag explicitly. Then work through the classic
failure mode: a user submits a write (e.g., posts a comment) which hits the
master, gets redirected to a page that reads from a lagging replica, and
doesn't see their own comment — the "read-your-own-writes" problem. Propose at
least one concrete mitigation: route a user's own reads to the master for a
short window after their write, pass a version/timestamp token the client
checks against replica freshness, or have the UI optimistically render the
write locally before confirming server state.

**Definition of done:** a diagram showing the master, replicas, load balancer,
and direction of replication; a short write-up naming at least one concrete
broken scenario caused by eventual consistency and at least one concrete
mitigation for it.

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
- Kyle Kingsbury (Jepsen), [Consistency Models](https://jepsen.io/consistency) — a rigorous, visual map of the consistency-model hierarchy referenced in this session
- Amazon, [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) — the paper behind multi-master replication and eventual consistency in practice
