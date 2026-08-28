# 17. Scaling Applications

**Part 4 — System Design Fundamentals** · [Back to curriculum index](../../README.md)

## One-sentence pitch
Horizontal scaling only works if any server can handle any request — which means
hunting down every piece of hidden state in your app and making services able to
find each other dynamically, instead of assuming a fixed cast of machines.

## Learning objectives
- Explain why statelessness is a precondition for horizontally scaling an
  application tier.
- Externalize session state out of in-process memory into a shared store.
- Describe what changes — and what new failure modes appear — when decomposing a
  monolith into microservices at scale.
- Implement or describe a minimal service discovery mechanism and explain why
  hardcoded addresses break down as a system grows.

## Session outline (~50 min)

| Segment | Time | Content |
|---|---|---|
| Horizontal vs. vertical scaling | 8 min | Recap and cost/reliability trade-offs |
| Statelessness & externalizing state | 12 min | Where state hides, how to move it out |
| Microservices at scale | 12 min | Independent scaling, new failure modes |
| Service discovery | 13 min | Client-side vs. server-side discovery |
| Wrap-up | 5 min | Connect to homework |

**Horizontal vs. vertical scaling (8 min).** Vertical scaling means a bigger
machine (more CPU/RAM on the same box) — simple, but has a ceiling and is a
single point of failure. Horizontal scaling means more machines behind a load
balancer — no hard ceiling, and losing one instance doesn't take the whole
service down, but it only works if any instance can serve any request. That
requirement is the entire reason statelessness matters.

**Statelessness & externalizing state (12 min).** The most common hidden state:
session data stored in a process-local dict, in-memory cache, or the local
filesystem. If instance A stores a logged-in user's session in its own memory,
a load-balanced request that lands on instance B has no idea who that user is.
Fix: move session data to a shared store every instance can read — Redis or a
database table keyed by session ID — or eliminate server-side session state
entirely by using a signed, self-contained token (JWT) the client holds. Same
principle applies to anything else living only in one process: local file
uploads, in-memory rate-limit counters, in-memory job queues.

**Microservices at scale (12 min).** Splitting a monolith into services lets you
scale the hot path independently (e.g., scale the image-processing service to
20 instances while the billing service stays at 2) instead of scaling the whole
monolith uniformly. The cost: what used to be an in-process function call is now
a network call, with all of network's failure modes — timeouts, partial
failures, versioning mismatches between services deployed independently. This
is where the trade-offs from earlier topics (CAP, consistency, retries) stop
being theoretical and start being Tuesday.

**Service discovery (13 min).** Once you have multiple instances of multiple
services, each potentially changing address as they're redeployed or
autoscaled, hardcoded IPs break immediately. *Client-side discovery*: a service
queries a registry directly and picks an instance itself (client-side load
balancing). *Server-side discovery*: a service calls a fixed, well-known address
(a load balancer or proxy) which itself queries the registry and forwards the
request — this is what Kubernetes Services and cloud load balancers do.
Registration can be self-registration (the instance tells the registry it
exists on startup and heartbeats) or third-party registration (a separate
process/sidecar watches instances and registers them). Either way, the registry
needs a way to drop entries for instances that stopped heartbeating.

## Homework notes

### 1. Externalize session state and run 2+ instances behind a load balancer
> Take a stateful toy web app (sessions stored in memory) and refactor it to be
> horizontally scalable (externalize session state), then simulate running 2+
> instances behind a load balancer.

**Goal:** tests the core mechanical skill of horizontal scaling: finding hidden
per-process state and moving it somewhere shared.

**Approach / hints:** Start from (or write) a toy app storing sessions in a
plain in-memory dict. Find every read and write of that dict and replace it
with calls to a shared store (Redis is the standard choice; a shared database
table works too). Run two instances of the app on different ports pointed at
the same store, and put a simple load balancer in front (nginx round robin
from topic 16 works fine). Prove statelessness by logging in via one instance
and confirming the *other* instance can read the session back.

**Starter example:** see
[`examples/example1_externalized_sessions.py`](examples/example1_externalized_sessions.py)
for a Flask + Redis skeleton with the login/session-lookup routes stubbed out.

**Definition of done:** submission includes the before (in-memory) and after
(externalized) code, the load balancer config used, and a demonstration (logs,
terminal output, or screenshots) proving a session created on one instance is
readable from another.

### 2. Minimal service discovery mechanism
> Implement a minimal service discovery mechanism (even a shared registry
> file/service) for 2–3 toy services that need to find each other's addresses at
> runtime.

**Goal:** tests understanding of *why* dynamic address resolution matters, via
the smallest implementation that actually demonstrates it — not a production
service mesh.

**Approach / hints:** The simplest working version is a shared registry — even
a single small HTTP service (or a shared JSON file, if you want to skip the
HTTP layer) that other services register with on startup and heartbeat
periodically. A service that needs to call another looks up its current
address from the registry instead of using a hardcoded one. To make it a real
discovery mechanism rather than static config in disguise, add a staleness
check: if a service hasn't heartbeated recently, the registry should stop
returning it as available.

**Starter example:** see
[`examples/example2_service_registry.py`](examples/example2_service_registry.py)
for a minimal Flask-based registry with `/register` and `/lookup/<name>`
endpoints and a heartbeat-window staleness check.

**Definition of done:** 2-3 toy services register themselves and successfully
look each other up by name at runtime (no hardcoded addresses in the calling
code); killing one service causes it to drop out of the registry within the
heartbeat window, demonstrated in logged output.

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
- [The Twelve-Factor App — Processes](https://12factor.net/processes) — the canonical short statement of why app processes must be stateless
- Kubernetes docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/) — a production example of server-side service discovery
