# 32. Security for Architects

**Part 8 — The Software Architect Role** · [Back to curriculum index](../../../README.md)

## One-sentence pitch
An architect doesn't need to be a penetration tester, but every structural decision — how passwords are stored, how services trust each other, which OWASP-class mistakes the design makes impossible by construction — either closes a class of vulnerability for good or leaves it open for every developer who touches the system afterward.

## Learning objectives
- Can explain why a fast general-purpose hash (MD5/SHA-family alone) is unsafe for passwords, and why a slow, salted algorithm (bcrypt/argon2) is the correct choice.
- Can name and briefly describe at least 6 of the OWASP Top 10 categories, and identify an example of each in real or sample code.
- Can design an authentication/authorization strategy for a multi-service system using a token-based approach, and explain how trust is established once and propagated.
- Can describe the basic role of PKI (public/private key pairs, certificates, certificate authorities) in establishing trust between two parties that have never communicated before.

## Session outline (~45–60 min)

| Segment | Time | Content |
|---|---|---|
| Hook: the breach that started with one bad decision | 5 min | Reference a well-known pattern (not necessarily a specific named breach): plaintext or unsalted-hash password storage, exposed at scale, cracked in bulk. Land on: this wasn't a clever attack, it was an architectural decision made once, years before the breach. |
| Hashing algorithms & password storage | 10 min | Distinguish encryption (reversible) from hashing (one-way) from encoding (not security at all — Base64 is not protection). Explain why fast hashes (MD5, SHA-256 alone) are wrong for passwords: they're *designed* to be fast, which is exactly what makes brute-forcing/rainbow tables cheap. Introduce salting (defeats precomputed rainbow tables) and slow, purpose-built algorithms (bcrypt, scrypt, argon2) that make brute-forcing computationally expensive per guess. |
| PKI fundamentals | 8 min | Asymmetric key pairs (public/private), what a certificate actually asserts (this public key belongs to this identity), and the role of a certificate authority in making that assertion trustworthy to a stranger. Tie to TLS: this is what makes "the server I'm talking to is really who it claims to be" verifiable without a prior relationship. |
| OWASP Top 10 | 12 min | Walk through several categories with a concrete example each: injection (unsanitized input reaching a query/command), broken access control (missing authorization check on an endpoint), cryptographic failures (weak/no encryption of sensitive data at rest or in transit), and a couple more time permits (security misconfiguration, vulnerable/outdated components, identification & authentication failures). For each, frame it as a *design* failure an architect can prevent structurally (e.g., mandating parameterized queries, centralizing authorization checks) rather than a bug to catch in review. |
| Authentication & authorization strategies | 10 min | Authentication (who are you) vs. authorization (what are you allowed to do) as distinct concerns. Token-based approaches (OAuth2/JWT): identity established once at a central auth service, a signed token carried by the client, each downstream service verifying the token's signature and claims without calling back to the auth service every time. Discuss token expiry, refresh, and revocation as the hard parts architects must plan for explicitly. |
| Wrap-up & homework framing | 5-10 min | Recap: security is cheapest when it's a structural decision (how auth flows, how passwords are stored) rather than a per-endpoint patch. Introduce the homework: implement correct password storage, find and fix real OWASP-class bugs, and design a token-based auth strategy. |

## Homework notes

### 1. Proper password storage vs. naive hashing
> Implement proper password storage (salted hashing with a modern algorithm like bcrypt/argon2) and demonstrate why a naive MD5/SHA1-without-salt approach is broken (e.g., via a rainbow table lookup demo).

- **Goal:** Tests hands-on understanding of *why* the recommended approach is recommended, not just that it is — seeing an unsalted hash cracked in seconds makes the lesson permanent in a way a slide never does.
- **Approach / hints:** Build two tiny functions: one hashing a password with unsalted MD5/SHA1, one with bcrypt or argon2 (most languages have a well-maintained library — don't hand-roll the algorithm). For the "broken" demo, either use a small precomputed table of common-password hashes you generate yourself, or an existing small rainbow-table/wordlist tool, to show the unsalted hash reversed in a lookup; then show the salted/bcrypt hash resists the same lookup because the salt makes precomputation useless. Keep the demo self-contained and offline — don't hit a real breach-data service.
- **Starter example:**
```python
import bcrypt
import hashlib

# Broken: unsalted, fast hash -> vulnerable to precomputed lookup tables.
def naive_hash(password: str) -> str:
    return hashlib.sha1(password.encode()).hexdigest()

# Correct: bcrypt generates and stores its own salt, and is deliberately slow.
def store_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)
```
- **Definition of done:** Working code for both approaches, plus a short write-up showing the naive hash cracked via a lookup table/wordlist and explaining why the bcrypt/argon2 version resists the same attack (salt + deliberate slowness).

### 2. Find and fix three OWASP Top 10 vulnerabilities
> Pick 3 OWASP Top 10 vulnerabilities, demonstrate each in a small deliberately-vulnerable app, then fix all three and write up the fix.

- **Goal:** Tests whether students can recognize these vulnerability classes in real code (not just definitions) and apply the standard structural fix for each.
- **Approach / hints:** Build (or use an existing minimal) small app — a handful of routes is enough. Good starter picks: SQL injection (string-concatenated query → parameterized query fix), broken access control (an endpoint missing an authorization check → add the check, ideally centralized/middleware-based rather than per-route), and security misconfiguration (verbose error messages/stack traces exposed to users → generic error responses with details only in server-side logs). For each, show the exploit working, apply the fix, then show the exploit failing.
- **Definition of done:** A small app with three vulnerabilities each demonstrated (proof the exploit works), fixed, and re-verified (proof the exploit no longer works), with a short written explanation per vulnerability of the underlying design mistake — not just the line-level patch.

### 3. Design a token-based auth strategy for a multi-service system
> Design an authentication/authorization strategy (diagram) for a multi-service system using a token-based approach (e.g., OAuth2/JWT), showing how identity is established once and trusted across services.

- **Goal:** Tests architectural (not just implementation-level) understanding of distributed identity — the design skill of deciding *where* trust is established and *how* it propagates, which is exactly the kind of decision an architect, not just a developer, is responsible for.
- **Approach / hints:** Diagram at least 3 services plus a central auth/identity service. Show the login flow (credentials → auth service → signed token issued), then show at least two downstream services independently validating that same token (verifying its signature/claims) without calling back to the auth service synchronously. Address explicitly: what's in the token (claims — user id, roles/scopes, expiry), how a service knows the token is genuinely from the auth service (shared secret or the auth service's public key), and what happens when a token needs to be revoked before it expires.
- **Definition of done:** A diagram (sequence or component diagram) plus a short written walkthrough covering token issuance, propagation, per-service validation, and how expiry/revocation is handled — a reader should be able to trace exactly where trust originates and how far it reaches.

## Further resources
- Free companion: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
