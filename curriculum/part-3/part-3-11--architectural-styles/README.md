# 11. Architectural Styles

**Part 3 — Architectural Foundations** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
The architectural style you choose — layered, event-driven, peer-to-peer, or something else — silently decides how your system fails, scales, and gets debugged at 3am, long before a single line of business logic is written.

## Learning objectives
- Can describe the defining structure of layered, client-server, peer-to-peer, event-driven/pub-sub, component-based, monolithic, and distributed styles, and name one system that fits each.
- Can explain the coupling and failure-mode trade-offs between a request/response style and an event-driven style for the same feature.
- Can pick an appropriate style for a given scenario and justify the choice using latency, coupling, and failure-handling criteria (not just "it's popular").
- Can implement a minimal working example of both a layered request/response flow and a pub-sub dispatcher, and articulate the structural differences in the code itself.

## Session outline (~45–60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: same feature, different shape | 5 min | Pose the chat-app scenario used in the homework: "a message needs to reach other users." Ask how many different ways this could be built. Park the answers, revisit at the end. |
| Layered & client-server | 8 min | Layered: presentation → business logic → data access, each layer only talks to the one below. Client-server: centralized server, clients request/respond. Note these are often combined (a layered server behind a client-server boundary). Trade-off: simple mental model, but the server is a bottleneck and a single point of failure. |
| Peer-to-peer | 6 min | No central server; nodes act as both client and server. Trade-off: no single point of failure, better for resilience/scale, but much harder to reason about consistency and discovery (see BitTorrent, blockchain networks as examples). |
| Event-driven & publish-subscribe | 10 min | Producers emit events without knowing who consumes them; consumers subscribe to topics/channels. Decouples producer from consumer in time and in knowledge of each other. Trade-off: excellent for scaling and loose coupling, but harder to trace a request end-to-end ("where did this event go?") and requires thinking about eventual consistency and idempotency. |
| Component-based, monolithic, distributed | 8 min | Component-based: system built from independently replaceable units with well-defined interfaces (cuts across the others — a monolith can still be component-based internally). Monolithic: one deployable unit — simple to deploy and reason about, but scaling and team-ownership get harder as it grows. Distributed: multiple independently deployable units communicating over a network — scales and isolates failure, but introduces network partiality, latency, and operational complexity. |
| Compare & contrast: latency, coupling, failure handling | 8 min | Build a comparison table live: for layered client-server vs. event-driven pub-sub, ask the class to fill in latency (sync wait vs. fire-and-forget), coupling (caller knows callee vs. anonymous), and failure handling (caller sees the error immediately vs. a dead-letter queue / retry policy needed). |
| Wrap-up & homework framing | 5–8 min | Revisit the chat-app hook. Introduce the homework: design it twice, then build a minimal version of both to feel the code-structure difference. |

## Homework notes

### 1. Chat app under two styles
> Design (diagram + short write-up) the same simple system — e.g., a chat app — under two different architectural styles: layered client-server vs. event-driven pub-sub. Compare trade-offs in latency, coupling, and failure handling.

- **Goal:** Tests whether students understand that architectural style is a *design decision with consequences*, not just a diagram-drawing exercise — they need to reason about what breaks and how under each style.
- **Approach / hints:** Keep the feature scope small — "user A sends a message, user B receives it" is enough. For layered client-server, draw the request path: client → API layer → business logic → data layer → response. For event-driven pub-sub, draw: publisher emits `MessageSent` event → broker/topic → subscriber(s) deliver to recipient. In the write-up, explicitly answer: what happens if the recipient is offline? What happens if the server crashes mid-request? Which style makes it easier to add a third consumer (e.g., a notification service) later?
- **Definition of done:** Two diagrams (one per style) covering the same feature, plus a short (half-page) written comparison hitting all three named criteria — latency, coupling, failure handling — with a concrete answer for each, not just generalities.

### 2. Minimal pub-sub vs. layered implementation
> Build a minimal working pub-sub message dispatcher (in-process is fine) and a minimal layered equivalent of the same feature; compare code structure.

- **Goal:** Tests whether the structural difference between the styles shows up concretely in code — direct calls with layer boundaries vs. decoupled publish/subscribe — not just in diagrams.
- **Approach / hints:** Pick one small feature (e.g., "notify when an order ships"). Implement it once as a layered call chain (controller calls service, service calls repository), and once as a pub-sub dispatcher (an in-memory event bus with `publish(event)` and `subscribe(event_type, handler)`). Keep both under ~50 lines. In the comparison, point out where new functionality would be added in each version (a new layer method call vs. a new subscriber) and what that implies for coupling.
- **Starter example:**
```typescript
// Minimal in-process pub-sub dispatcher
type Handler<T> = (event: T) => void;

class EventBus {
  private handlers = new Map<string, Handler<any>[]>();

  subscribe<T>(eventType: string, handler: Handler<T>): void {
    const list = this.handlers.get(eventType) ?? [];
    list.push(handler);
    this.handlers.set(eventType, list);
  }

  publish<T>(eventType: string, event: T): void {
    for (const handler of this.handlers.get(eventType) ?? []) {
      handler(event);
    }
  }
}

// Layered equivalent: OrderController -> OrderService -> NotificationService
// (direct calls, no bus, each layer knows the next)
```
- **Definition of done:** Two small runnable code samples (or one file each) implementing the same feature, plus a short written note (a paragraph or two) comparing how a new consumer/behavior would be added to each.

## Further resources
- Free companion: *[Software Engineering: A Modern Approach](https://softengbook.org/chapter7), Ch. 7 — free open textbook. Note: the page blocks automated fetches, so it's worth a manual spot-check before relying on it for class.*
