# 28. Cloud Security Patterns

**Part 7 — Cloud Design Patterns** · [Back to curriculum index](../README.md)

## One-sentence pitch
The safest way to handle a privileged operation is usually to not let your own
application server touch it directly — these three patterns push identity checks and
risky operations out to a thin boundary or a specialized provider instead of trusting
every line of app code with full access.

## Learning objectives
- Can explain Federated Identity and why delegating authentication to a trusted
  provider (rather than each app rolling its own) reduces the attack surface.
- Can implement the Gatekeeper pattern: a thin, restricted-permission proxy that
  validates and sanitizes requests before they reach a more privileged backend.
- Can implement the Valet Key pattern: a short-lived, scoped credential/URL that lets a
  client interact directly with a resource (e.g., storage) without routing through the
  app server.
- Can articulate, for a given system, why "least privilege at the boundary" beats
  "trust the whole app tier equally."

## Session outline (~45 min)

| Segment | Time | Content |
|---|---|---|
| Hook: one compromised endpoint, full database access | 5 min | Why a monolithic trust boundary is dangerous |
| Federated Identity | 10 min | Delegating authentication to a trusted identity provider |
| Gatekeeper | 12 min | A thin, low-privilege proxy validating requests before they reach the backend |
| Valet Key | 13 min | Scoped, short-lived direct access instead of routing through the app |
| Wrap-up | 5 min | Least privilege as the common thread |

**Hook: one compromised endpoint, full database access (5 min).** Sketch a typical
monolith: one application server, running with credentials broad enough to do
everything the app ever needs to do — read/write the full database, full access to
blob storage, admin API calls. A single vulnerable endpoint (an unvalidated upload, an
injection bug) now has the blast radius of the *entire* system, not just that feature.
Every pattern in this session is a way of shrinking that blast radius by not giving
untrusted-facing code more privilege than the one operation it needs to perform.

**Federated Identity (10 min).** Instead of each application implementing its own
username/password store and authentication logic, delegate authentication to a trusted
external identity provider (an OAuth2/OIDC provider, an enterprise SSO/Active
Directory, a social login provider) and accept a signed token asserting who the user
is. Cover why this is a security win, not just a convenience: the app never touches raw
passwords, gets battle-tested MFA/breach-detection for free, and a compromise of one
app doesn't leak credentials that work everywhere else (the way password reuse across
custom-rolled auth systems does). Connect forward to Topic 32's token-based
authentication/authorization design homework — federated identity is the piece that
establishes *who* the caller is before token-based authorization decides what they can do.

**Gatekeeper (12 min).** Insert a dedicated, deliberately low-privilege service between
untrusted clients and a more privileged backend. The gatekeeper's only job is to
validate, sanitize, and authorize incoming requests — it holds just enough permission
to do that, and nothing more — then forwards legitimate requests to the backend, which
can trust that anything reaching it has already been checked. Contrast with a
traditional API layer that both validates *and* holds full backend credentials: if that
combined layer is compromised, the attacker gets both the entry point and the
privilege. Splitting them means compromising the gatekeeper alone doesn't hand over the
backend's full capability. Draw the topology: client → gatekeeper (public-facing, thin,
low-privilege) → internal network boundary → backend (privileged, not directly
reachable from outside).

**Valet Key (13 min).** Named for handing a valet a key that only starts the car, not
one that opens the trunk or the glovebox. Instead of a client uploading a file through
the app server (which then re-uploads it to storage — extra latency, extra load,
extra privilege needed on the app server), the app issues a short-lived, narrowly
scoped credential — a signed URL, a SAS token — that lets the client write (or read)
directly to storage, for a limited time, for a limited operation, without ever needing
broad storage credentials itself. Walk the flow: client asks app for permission → app
verifies the client is allowed to do this one operation → app calls the storage
provider's API to mint a scoped, time-limited token/URL → client uses it directly
against storage → app server is out of the data path entirely. Emphasize the two levers
that make it safe: **scope** (this token can only do this one operation, e.g., "PUT to
this exact object key") and **time** (it expires soon, so a leaked URL has a small
window of usefulness).

**Wrap-up (5 min).** Federated Identity answers "who is this," Gatekeeper answers
"is this specific request allowed to reach the privileged system," and Valet Key
answers "can we let them touch the resource directly without needing to trust them (or
our own app tier) with broad access." All three are instances of the same principle:
push authorization decisions to a thin, well-audited boundary and keep everything past
that boundary as unprivileged as possible.

## Homework notes

### 1. Implement the Gatekeeper pattern: a thin, restricted-permission proxy service that validates/sanitizes requests before they reach a more privileged backend.

**Goal:** Practice designing a genuinely reduced-privilege boundary — not just "an API
layer," but a component that provably cannot do more than validate and forward.

**Approach / hints:**
- Build a "backend" service that holds a sensitive capability (e.g., full CRUD on a
  data store, or an admin-only action) and give it no input validation of its own —
  it trusts whatever reaches it, by design, because the gatekeeper is what protects it.
- Build the gatekeeper as a separate process/service in front of it: it accepts public
  requests, validates shape/type/auth/business rules (e.g., request size limits,
  allowed fields, authenticated user's permission level), and only forwards requests
  that pass every check.
- Give the gatekeeper credentials to call the backend that are *not* the backend's own
  full privilege — e.g., the backend only accepts calls from the gatekeeper's specific
  service identity/network location, or via a narrow internal API the gatekeeper uses,
  distinct from whatever broader access the backend might have to a datastore.
- Demonstrate the point: send a malformed/malicious request directly (bypassing the
  gatekeeper, if your setup allows it) and show the backend has no defense — then show
  the same request through the gatekeeper gets rejected before it ever reaches the
  backend.

**Starter example:**
```python
# backend.py — deliberately trusts its caller; no validation here
def apply_admin_action(payload: dict) -> str:
    return f"applied: {payload}"

# gatekeeper.py — the only thing allowed to call backend directly
ALLOWED_FIELDS = {"action", "target_id"}
MAX_TARGET_LEN = 64

def handle_request(raw_request: dict, backend_call) -> str:
    # TODO: validate raw_request against ALLOWED_FIELDS / MAX_TARGET_LEN,
    # check the caller's auth/permission, reject anything that fails,
    # and only then call backend_call(raw_request).
    ...
```

**Definition of done:** Two distinct components (gatekeeper and backend) with the
gatekeeper holding narrower privilege than the backend, a documented set of
validation/sanitization rules the gatekeeper enforces, and a demonstration that a
malicious/malformed request is rejected at the gatekeeper and never reaches the backend.

### 2. Implement the Valet Key pattern: issue a short-lived, scoped access token/URL that lets a client upload directly to storage (e.g., a signed URL) without routing the file through your app server.

**Goal:** Understand how to mint and verify a narrowly scoped, time-limited credential
— the mechanism that lets a client bypass the app server for one specific operation
without that turning into a security hole.

**Approach / hints:**
- If you have access to real cloud storage (S3 pre-signed URLs, Azure Blob SAS tokens,
  GCS signed URLs), use the provider's SDK to generate one scoped to a single object
  key, a single operation (PUT), and a short expiry (e.g., 5 minutes) — this is the
  most realistic version of the homework.
- If you don't want a cloud dependency, simulate it: build a minimal local "storage
  server" and have your app mint a signed token (e.g., HMAC over `object_key +
  expiry + allowed_operation`) that the storage server verifies independently, without
  calling back to the app.
- Demonstrate the client uploading directly to storage using only the token/URL — the
  app server should be involved only in *issuing* the token, never in relaying the
  file's bytes.
- Prove the scoping/expiry actually work: show a request with an expired token is
  rejected, and a request trying to use the token for a different object key or
  operation (e.g., DELETE instead of PUT) is rejected.

**Starter example:**
```python
import hmac, hashlib, time

SECRET = b"server-side-secret"  # never given to the client

def mint_valet_key(object_key: str, operation: str, ttl_seconds: int = 300) -> dict:
    expiry = int(time.time()) + ttl_seconds
    message = f"{object_key}:{operation}:{expiry}".encode()
    signature = hmac.new(SECRET, message, hashlib.sha256).hexdigest()
    return {"object_key": object_key, "operation": operation, "expiry": expiry, "signature": signature}

def verify_valet_key(token: dict) -> bool:
    # TODO: recompute the HMAC from token's fields and compare (constant-time),
    # then check token["expiry"] > time.time() and operation matches what's
    # being attempted before allowing the storage operation to proceed.
    ...
```

**Definition of done:** A working demo where a client performs a storage operation
using only an app-issued token/URL (no file bytes pass through the app server), plus
evidence that an expired token and a token used for a different key/operation than it
was issued for are both rejected.

## Further resources
- Free companion: Azure Architecture Center, [Security design patterns](https://learn.microsoft.com/en-us/azure/well-architected/security/design-patterns)
- [OpenID Connect (OIDC) — Core specification overview](https://openid.net/specs/openid-connect-core-1_0.html)
