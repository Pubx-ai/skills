# AdCP rules — errors & recovery

Apply these when the diff constructs protocol errors, handles error responses, or
implements retry/recovery logic.

> Curated AdCP 3.x snapshot (last curated: 2026-07-12) — when you have web access, fetch the live sources and let
> them win on any conflict:
> https://docs.adcontextprotocol.org/docs/protocol/calling-an-agent.md and
> https://docs.adcontextprotocol.org/docs/building/by-layer/L3/error-handling.md

## Producing errors (agent side)

- Protocol-level errors must use the protocol's error structure and codes — an
  `adcp_error` envelope with `code`, `recovery`, and (for validation failures)
  `issues[]` carrying RFC 6901 JSON Pointers to the offending fields.
- Do not leak transport-level errors (raw HTTP bodies, stack traces, upstream vendor
  errors) as protocol responses, and do not signal failure through a success-shaped
  payload. A `completed` response whose body describes a failure is a conformance bug.
- Validation failures should be `correctable` with actionable `issues[]`; internal
  faults are `transient`; conditions needing human action (account suspended, payment
  required) are `terminal`.

## Consuming errors (caller side)

- `recovery` drives behaviour and code must branch on it:
  - `correctable` — fix the fields named by `issues[].pointer` and resend. Blind retry
    of a correctable error is a bug.
  - `transient` — retry **with the same `idempotency_key`**.
  - `terminal` — do not retry; surface to a human.
- For `oneOf` validation failures, the fix is to pick ONE variant from
  `issues[].variants` and send only its required fields — code that "merges" variant
  fields to satisfy the error will fail both variants.
- Error handling that swallows the `errors[]` array on a mutating call and proceeds as
  if the operation succeeded is a money-losing bug, not a style issue.
