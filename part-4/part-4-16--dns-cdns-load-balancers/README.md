# 16. DNS, CDNs & Load Balancers

**Part 4 — System Design Fundamentals** · [Back to curriculum index](../../README.md)

## One-sentence pitch
Before a single byte of your application logic runs, a request has already
traveled through DNS resolution, possibly a CDN edge cache, and a load balancer —
and understanding that path is what separates "it works on my machine" from
designing a system that serves millions of users reliably.

## Learning objectives
- Trace a full request path from a browser typing a URL to a response, naming
  every network hop.
- Differentiate push vs. pull CDN population strategies and state when each is
  used.
- Explain the difference between a load balancer and a reverse proxy, and where
  the two overlap in real products.
- Compare at least three load balancing algorithms and state a workload each
  suits.
- Explain Layer 4 vs. Layer 7 load balancing and give a use case only Layer 7
  can handle.

## Session outline (~55 min)

| Segment | Time | Content |
|---|---|---|
| DNS resolution | 10 min | Resolution chain, caching, TTLs |
| CDNs | 10 min | Push vs. pull, cache hit/miss |
| Load balancers vs. reverse proxies | 10 min | What each does, where they overlap |
| LB algorithms + L4 vs. L7 | 15 min | Algorithm comparison, layer trade-offs |
| Wrap-up | 10 min | Assemble the full request path end to end |

**DNS resolution (10 min).** Walk the chain a browser follows to turn a hostname
into an IP: browser cache → OS resolver cache → recursive resolver (usually the
ISP's or a public one like 8.8.8.8) → root nameserver → TLD nameserver (`.com`)
→ authoritative nameserver for the domain, which returns the IP. Each hop can be
cached, controlled by a TTL on the DNS record — a low TTL means faster failover
if you change the IP, but more resolution traffic; a high TTL means less load on
nameservers but slower propagation of changes.

**CDNs (10 min).** A CDN caches content at edge locations physically closer to
users to cut latency and offload the origin. *Push CDN*: you proactively upload
content to the CDN ahead of time — good for a known, relatively static set of
large assets (e.g., a game's launch assets) where you control exactly when
content updates. *Pull CDN*: the CDN fetches from your origin on the first
request for a given URL and caches it, serving subsequent requests from cache
until TTL expiry — simpler to operate (no upload step) and scales naturally to
a large, unpredictable content catalog, at the cost of a cache-miss penalty on
first request.

**Load balancers vs. reverse proxies (10 min).** A *reverse proxy* sits in front
of one or more backend servers and can do things like TLS termination, response
caching, compression, and request routing by path — even in front of a single
server. A *load balancer* specifically distributes traffic across a *pool* of
servers for capacity and availability. The two concepts overlap heavily in real
products — nginx and HAProxy are commonly deployed as both simultaneously — but
conceptually, "reverse proxy" answers "what sits between the client and my
servers," and "load balancer" answers "how is the load spread across them."

**LB algorithms + L4 vs. L7 (15 min).** Algorithms: *round robin* (cycle through
servers evenly — simple, assumes uniform request cost), *weighted round robin*
(bias toward more capable servers), *least connections* (send to whichever
server currently has the fewest open connections — better when request cost
varies widely), *IP hash / consistent hashing* (route the same client
consistently to the same server — needed for session affinity or cache
locality). *Layer 4* load balancing operates on the transport layer (IP/port),
routing TCP/UDP packets without inspecting content — fast and protocol-agnostic.
*Layer 7* operates on the application layer, so it can read HTTP headers, paths,
and cookies to make routing decisions (e.g., route `/api/*` to one service pool
and `/static/*` to another) — more overhead, but necessary for content-based
routing and is where TLS termination and path-based microservice routing
happen.

## Homework notes

### 1. Diagram the full request path
> Diagram the full request path from a browser typing a URL to a response,
> labeling where DNS resolution, CDN caching, and load balancing occur.

**Goal:** tests whether the student can integrate DNS, CDN, and load balancing
into one coherent mental model instead of three memorized facts in isolation.

**Approach / hints:** Start from the browser's own DNS cache, walk the full
recursive resolution chain, then the TCP/TLS handshake to whatever IP was
resolved (which may be a CDN edge node's IP, not your origin's). Show a branch
for a CDN cache hit (response served from the edge, origin never touched) and a
cache miss (edge fetches from origin, caches it, then responds). After the CDN,
show the load balancer distributing to one of several app server instances.
Label every arrow with what's cached where and for how long.

**Definition of done:** a diagram (any tool, including hand-drawn and
photographed) with every hop labeled, and explicit callouts for where DNS
caching, CDN caching, and the load-balancing algorithm choice each occur in
the path.

### 2. Configure a local reverse proxy/load balancer
> Configure a local reverse proxy/load balancer (e.g., Nginx or a simple custom
> one) in front of 2–3 instances of a toy app, and demonstrate round-robin vs.
> least-connections behavior.

**Goal:** tests hands-on config skill and whether the student can connect LB
algorithm theory to actually-observed traffic distribution.

**Approach / hints:** Stand up 2-3 instances of a trivial HTTP server on
different ports, each returning its own instance ID in the response so you can
tell them apart. Point nginx's `upstream` block at all of them (round robin is
the default — no directive needed) and hit it repeatedly with a `curl` loop,
logging which instance answered each time. Then add `least_conn;` to the
upstream block and repeat, ideally after making one instance artificially slow
(e.g., an endpoint with a sleep) so you can see least-connections favor the
faster instances.

**Starter example:**
```nginx
upstream backend {
    # round robin is nginx's default with no extra directive
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}

server {
    listen 8080;
    location / {
        proxy_pass http://backend;
    }
}
```
Add `least_conn;` as the first line inside `upstream backend { ... }` to switch
algorithms.

**Definition of done:** submission includes the nginx config for both
algorithms, captured output/logs showing the distribution pattern under each
(round robin cycling evenly, least-connections favoring less-busy instances
under a simulated slow endpoint), and 2-3 sentences explaining the observed
difference.

## Further resources
- Free companion: [system-design-primer](https://github.com/donnemartin/system-design-primer)
- NGINX, [HTTP Load Balancing Admin Guide](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/) — official docs covering the algorithms used in homework 2
- Cloudflare Learning Center, [What Is a CDN?](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) — accessible explainer on push/pull caching and edge networks
