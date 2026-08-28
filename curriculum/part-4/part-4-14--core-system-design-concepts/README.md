# 14. Core System Design Concepts

**Part 4 — System Design Fundamentals** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Every system design decision you'll ever defend in an interview or an architecture
review comes down to a handful of trade-offs — performance vs. scalability, latency
vs. throughput, availability vs. consistency — and this session gives you the
vocabulary and the CAP theorem framework to reason about them precisely instead of
by gut feel.

## Learning objectives
- Explain the difference between performance and scalability, and give an example
  where a system is fast but doesn't scale (or scales but isn't fast).
- Distinguish latency from throughput and describe a concrete change that trades one
  for the other (e.g., batching).
- Explain availability vs. consistency as a real engineering trade-off, not just a
  vocabulary pair.
- State the CAP theorem correctly (what it guarantees, and specifically *under a
  network partition*) and avoid the common "pick any 2 of 3" misstatement.
- Classify a real system as CP or AP and justify the choice with a concrete failure
  scenario.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Performance vs. scalability | 10 min | Definitions, worked example |
| Latency vs. throughput | 10 min | Definitions, the batching trade-off |
| Availability vs. consistency | 10 min | What each means for a client request |
| CAP theorem (CP vs. AP) | 15 min | Correct statement, examples, common misconceptions |
| Wrap-up / homework framing | 5 min | Connect to the two homework prompts |

**Performance vs. scalability (10 min).** Performance is how fast a system responds
under a *given* load; scalability is whether performance holds up as load grows.
A system can be fast at 10 requests/sec and fall over at 10,000 — it was
performant but not scalable. Conversely, a system built for massive horizontal
scale-out can have worse single-request latency than a tightly optimized monolith
at low load, because it pays coordination overhead (network hops, distributed
locks) that a single-machine system doesn't. Worked example: a single-node SQLite
app with no network hops vs. a sharded, replicated Postgres cluster — the former
wins on raw latency at low load, the latter wins as concurrent users grow into the
millions.

**Latency vs. throughput (10 min).** Latency = time for one operation to complete.
Throughput = operations completed per unit time. They are not the same axis and
optimizing one can hurt the other. Batching is the classic trade: grouping 100
writes into one batch write raises throughput (fewer round trips, better
amortization) but raises the latency of any *individual* write in the batch
(it waits for the batch to fill or flush). Queuing theory intuition: as a system
approaches its throughput ceiling, latency doesn't creep up linearly — it spikes,
because requests start queuing behind a saturated resource.

**Availability vs. consistency (10 min).** Availability: every request to a
non-failing node gets *a* response, without guaranteeing it's the most recent
write. Consistency: every read gets the most recent write (or an error) — but
that requires coordination that can block a response. Frame with a concrete
example: two replicas of a shopping cart in different regions get partitioned
from each other; do you (a) let both keep accepting writes and reconcile later
(available, inconsistent) or (b) refuse writes on one side until the partition
heals (consistent, unavailable there)?

**CAP theorem (15 min).** State it precisely: in the presence of a network
**P**artition, a distributed system must choose between **C**onsistency and
**A**vailability — you cannot have both *during the partition*. Outside of a
partition, you can (and should) have both. Common misconception to correct:
"pick 2 of 3" is wrong — partition tolerance isn't optional for any system that
runs on more than one node over an unreliable network, so realistically the
choice is CP vs. AP, made *only when* a partition is actually happening. Give
2-3 real examples: a distributed banking ledger (CP — better to reject a
transaction than double-spend), a DNS system (AP — stale records are fine,
total unavailability isn't), a shopping cart (usually AP with reconciliation).

## Homework notes

### 1. CP vs. AP design memo
> Write a short design memo for a hypothetical system (e.g., a URL shortener)
> explicitly stating whether it favors CP or AP under partition, and why,
> referencing CAP theorem trade-offs.

**Goal:** tests whether the student can translate the abstract CAP framework into
a concrete, defensible architectural decision — not recite the theorem, but apply
it.

**Approach / hints:** Pick a system with at least two distinct operations that
might want different answers (e.g., URL shortener: *creating* a short code needs
to avoid collisions, *redirecting* an existing short URL is read-heavy and
tolerates staleness). State explicitly what "a partition" means concretely for
this system (e.g., the write-region and a read-region losing connectivity).
Argue the trade-off in terms of user-visible consequences, not jargon: what does
the user see if you choose CP? What do they see if you choose AP?

**Definition of done:** a memo (roughly half a page to a page) that names the
system, states a CP or AP choice per operation type if they differ, explains the
concrete partition scenario considered, and describes the user-visible behavior
under that choice. No code required.

### 2. Classify three scenarios
> Given three system scenarios (e.g., banking ledger, social media feed, chat
> delivery receipts), classify each as prioritizing consistency or availability
> and justify the choice.

**Goal:** tests pattern recognition — can the student generalize the CP/AP
framework across different domains without a worked example to copy.

**Approach / hints:** For each scenario, ask two questions: "what's the cost of
showing a stale/wrong read?" and "what's the cost of refusing to respond at
all?" Whichever cost is worse tells you which side of CAP to favor. A banking
ledger: a stale balance shown briefly is usually tolerable, but a double-spend
from an inconsistent write is not — favor consistency on writes. A social feed:
showing a slightly stale feed is fine, refusing to load the app is not — favor
availability. Chat delivery receipts: a lost or duplicate "delivered" tick is
mildly annoying, not catastrophic — favor availability, reconcile later.

**Definition of done:** each of the three scenarios has a one-word classification
(C-leaning or A-leaning) plus 2-3 sentences of justification referencing a
specific concrete consequence of the trade-off, not a restatement of CAP theory.

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
- Eric Brewer, [CAP Twelve Years Later: How the "Rules" Have Changed](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed/) (InfoQ) — CAP's original author revisiting and clarifying common misreadings
- Coda Hale, [You Can't Sacrifice Partition Tolerance](https://codahale.com/you-cant-sacrifice-partition-tolerance/) — a sharp, short explanation of why "pick 2 of 3" is the wrong mental model
