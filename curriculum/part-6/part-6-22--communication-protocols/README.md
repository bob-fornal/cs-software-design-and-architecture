# 22. Communication Protocols

**Part 6 — Asynchronous & Distributed Communication** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
Every distributed system is, underneath, two processes agreeing on bytes over a wire —
and the protocol you pick (TCP vs. UDP, REST vs. gRPC vs. GraphQL) sets a hard ceiling
on your latency, reliability, and how much client code you'll write later.

## Learning objectives
- Can place HTTP, TCP, UDP, and RPC at the correct layer relative to each other and
  explain what each one guarantees (or doesn't).
- Can explain the core trade-off between REST, gRPC, and GraphQL: resource-oriented vs.
  contract-first RPC vs. client-specified queries.
- Can implement the same simple read API as both REST and GraphQL and articulate,
  with a concrete field count, the over-fetching/under-fetching difference.
- Can build a minimal gRPC service/client pair and explain when the performance and
  strong-typing benefits of gRPC are worth losing REST's browser-native simplicity.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| Hook: what actually happens when you call an API | 5 min | Trace a REST call down through HTTP, TCP, and IP; ask where UDP would differ |
| TCP vs. UDP | 8 min | Reliable, ordered, connection-oriented vs. fire-and-forget; why each exists and who uses UDP (DNS, video, gaming) |
| HTTP as the dominant application protocol | 5 min | Request/response, statelessness, HTTP/1.1 vs. HTTP/2 multiplexing, why it won |
| RPC and REST | 10 min | RPC's "call a remote function" mental model vs. REST's resource + verb model; REST maturity (Richardson model) in brief |
| GraphQL | 10 min | Single endpoint, client-specified shape, resolvers; solving over/under-fetching, at the cost of caching simplicity |
| gRPC | 10 min | Protocol Buffers, HTTP/2 framing, strongly-typed contracts, streaming; where it wins over REST for internal service calls |
| Wrap-up: choosing a protocol | 5 min | A decision checklist: public API vs. internal, browser client vs. service-to-service, bandwidth-constrained vs. not |

**Hook (5 min).** Trace one REST call: DNS resolution, TCP handshake, TLS handshake,
HTTP request/response, connection teardown or keep-alive. Ask: which of these steps
would look different over UDP, and why doesn't anyone build a REST API on UDP?

**TCP vs. UDP (8 min).** TCP: connection-oriented, guarantees ordered/reliable
delivery via acknowledgments and retransmission, at the cost of handshake latency and
head-of-line blocking. UDP: connectionless, no delivery guarantee, no ordering — but
low overhead and low latency. Concrete examples of UDP use: DNS lookups, video/voice
streaming (a dropped frame is better than a stalled stream), online gaming. Almost
everything discussed in the rest of the session rides on top of TCP.

**HTTP as the dominant application protocol (5 min).** Request/response, textual
(HTTP/1.1) or binary framed (HTTP/2), stateless by design (state lives in tokens/
cookies, not the connection). HTTP/2's multiplexing (many logical streams over one TCP
connection) is what makes gRPC's streaming and GraphQL's single-endpoint model
practical without paying a new-connection cost per call.

**RPC and REST (10 min).** RPC: "call a function that happens to run on another
machine" — the client calls `getUser(id)` and it's transparently a network call. REST:
model the API as resources (`/users/123`) manipulated with HTTP verbs (GET, POST, PUT,
DELETE) and status codes as part of the contract. Briefly mention the Richardson
Maturity Model (plain HTTP → resources → verbs → HATEOAS) without dwelling on it. The
throughline: REST leans on HTTP semantics; RPC-style protocols (including gRPC) treat
HTTP as a transport for something closer to a function call.

**GraphQL (10 min).** One endpoint, one schema, and the client specifies exactly which
fields it wants in the query. Walk through why this fixes REST's two classic problems:
over-fetching (REST returns the whole resource even if the client wants 2 of 8 fields)
and under-fetching (a client needing data from 3 REST resources makes 3 round trips;
GraphQL resolves it in one). Trade-offs: HTTP-level caching (which relies on
predictable URLs) gets harder, and query cost/complexity needs its own safeguards
(depth limiting, cost analysis) since clients can ask for arbitrarily nested data.

**gRPC (10 min).** Protocol Buffers define a strongly-typed, versioned service
contract (`.proto` file) that's compiled into client/server code in any supported
language. Runs over HTTP/2, supporting request/response plus client-streaming,
server-streaming, and bidirectional streaming. Binary serialization is smaller and
faster to (de)serialize than JSON. The catch: it's not natively browser-friendly
(needs grpc-web or a proxy) and it's harder to poke at with `curl` — so it shines for
internal service-to-service calls where both ends are under your control, less so for
a public-facing API consumed by arbitrary clients.

**Wrap-up (5 min).** A decision checklist: Is the client a browser or an unknown third
party? → lean REST/GraphQL. Is it another internal service you control on both ends,
where latency and type safety matter? → lean gRPC. Does the client need to shape its
own response to avoid over-fetching across many client types (mobile vs. web)? →
lean GraphQL.

## Homework notes

### 1. Implement the same API as REST and GraphQL; compare over/under-fetching

**Goal:** Feel the over-fetching/under-fetching difference directly, with a concrete
field count, rather than taking it on faith.

**Approach / hints:**
- Pick a small resource with at least 8 fields (e.g. a `User` with id, name, email,
  bio, avatarUrl, createdAt, role, lastLoginAt) and a "list posts" collection.
- Implement REST endpoints (`GET /users/:id`, `GET /posts`) that return the full
  resource shape.
- Implement the same data via a GraphQL schema and resolvers (e.g. with
  `graphql-core` in Python or `graphql-yoga`/`apollo-server` in Node).
- Write a client scenario that only needs 2 of the 8 fields. Measure/report response
  payload size (bytes) for REST vs. GraphQL for that scenario, and do the reverse for
  a scenario needing data from two related resources (posts + their authors) to show
  REST's extra round trip versus GraphQL's single query.

**Starter example (Python, minimal GraphQL resolver with `graphql-core`):**
```python
from graphql import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString, GraphQLID

UserType = GraphQLObjectType("User", lambda: {
    "id": GraphQLField(GraphQLID),
    "name": GraphQLField(GraphQLString),
    "email": GraphQLField(GraphQLString),
    # TODO: add the remaining 5+ fields to match your REST resource
})

def resolve_user(root, info, id):
    return get_user_from_db(id)  # TODO: implement

QueryType = GraphQLObjectType("Query", lambda: {
    "user": GraphQLField(UserType, args={"id": GraphQLID}, resolve=resolve_user),
})

schema = GraphQLSchema(query=QueryType)
# Client can now request: { user(id: "1") { name email } } — 2 of 8 fields.
```

**Definition of done:** Working REST and GraphQL implementations of the same
underlying data, a documented byte-size or field-count comparison for an
under-fetching client (2 of 8 fields) and an over-fetching-avoided/multi-resource
client, and 3-5 sentences summarizing which approach won which scenario and why.

### 2. Build a minimal gRPC service/client and compare to REST

**Goal:** Get hands-on with Protocol Buffers and generated client/server code, and
form an opinion — backed by direct experience — on gRPC vs. REST for internal calls.

**Approach / hints:**
- Define a small `.proto` service (e.g. `GetUser(GetUserRequest) returns (UserReply)`).
- Generate server and client code (`grpcio-tools` for Python, `protoc` + the Node/Go
  gRPC plugins, etc.) and implement the server handler plus a client that calls it.
- Time a batch of N calls (e.g. 1,000 sequential `GetUser` calls) against gRPC and
  against an equivalent REST/JSON endpoint on the same machine, and note payload size
  differences for the same logical data.
- Write a short comparison (10-15 sentences) covering: type safety at compile time,
  payload size, ease of debugging with generic tools (`curl` vs. `grpcurl`), browser
  compatibility, and where each fits (public API vs. internal service mesh).

**Starter example (`.proto` definition):**
```protobuf
syntax = "proto3";

service UserService {
  rpc GetUser (GetUserRequest) returns (UserReply);
}

message GetUserRequest {
  string id = 1;
}

message UserReply {
  string id = 1;
  string name = 2;
  string email = 3;
  // TODO: add remaining fields, then run protoc/grpcio-tools to generate stubs
}
```

**Definition of done:** A working gRPC server and client exercising at least one RPC
call end-to-end, a timing/payload-size comparison against an equivalent REST call, and
a written comparison covering the trade-offs above.

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
