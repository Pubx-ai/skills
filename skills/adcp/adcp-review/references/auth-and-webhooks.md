# AdCP rules — authentication, signing, webhooks & account isolation

Apply these when the diff touches auth, request/webhook signing or verification,
outbound fetches of counterparty-supplied URLs, or account scoping.

> Curated AdCP 3.x snapshot (last curated: 2026-07-12) — when you have web access, fetch the live sources and let
> them win on any conflict:
> https://docs.adcontextprotocol.org/docs/building/by-layer/L1/security.md and
> https://docs.adcontextprotocol.org/docs/building/by-layer/L3/webhooks.md

## Inbound requests

- Handlers that accept inbound AdCP requests must verify the caller's
  identity/signature per the protocol's auth requirements **before acting**. A handler
  that processes a task without verification is a blocking bug.
- Hardcoded credentials in protocol client code are a blocking bug. Credentials must
  come from secure storage / environment, never version control.

## Account isolation (seller side)

- Every object (media buy, creative, session, idempotency cache entry) is bound to the
  account that created it, and every subsequent access must verify the authenticated
  agent may act on that account — the two-step pattern:
  1. Auth precheck: the request's `account` must be in the authenticated agent's
     authorized set.
  2. Resource query: filter by the request's specific `account_id`, not the whole
     authorized set (filtering by the whole set lets account A read account B's buys).
- Failures must fail closed with a **generic** "not found" — an error body that
  distinguishes "unauthorized" from "not found" is an existence leak.
- A seller must not silently substitute a credential-implied default account when the
  schema requires an explicit `account`.

## Webhooks

- AdCP 3.0 webhooks are signed with RFC 9421 (key published via `brand.json`
  `agents[].jwks_uri`); receivers must verify. The HMAC-SHA256 scheme is a deprecated
  legacy fallback (removed in 4.0) — new code should not default to it.
- If the diff implements the legacy HMAC scheme, the load-bearing rules are:
  - HMAC computed over `{unix_timestamp}.{raw_http_body_bytes}` — the **raw bytes on
    the wire**, captured before any JSON parse. Verifying against a re-serialized parsed
    payload is a bug (key order / unicode / number formatting drift).
  - Timestamp comes from the `X-ADCP-Timestamp` header, not a body field.
  - Constant-time comparison (`timingSafeEqual`), replay window ±300 s, secret ≥ 32
    bytes.
  - Verification order: missing headers → non-numeric timestamp → window → HMAC.

## Outbound fetches of counterparty URLs (SSRF)

Any URL a counterparty supplies for this code to fetch (webhook URLs, governance agent
URLs, `authoritative_location`, …) is an SSRF vector. Before fetching, code must:

1. Reject non-HTTPS in production.
2. Resolve the hostname and reject reserved ranges (RFC 1918, loopback, link-local —
   including `169.254.169.254` cloud metadata — CGNAT, IPv6 equivalents and
   IPv4-mapped `::ffff:0:0/96`).
3. Pin the connection to the validated IP (DNS-only validation is rebindable).
4. Refuse redirects (narrow, spec-defined exceptions for brand.json / adagents.json).
5. Cap response size and timeouts; don't echo detailed fetch errors back to the URL
   supplier (topology probe side-channel).

Missing IP-range validation or connection pinning on a counterparty-URL fetch is a
security bug, not a nit.
