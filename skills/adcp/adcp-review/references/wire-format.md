# AdCP rules — wire format & message shapes

Apply these when the diff constructs, parses, or validates AdCP task messages.

> Curated AdCP 3.x snapshot (last curated: 2026-07-12) — when you have web access, fetch the live sources and let
> them win on any conflict:
> https://docs.adcontextprotocol.org/docs/protocol/calling-an-agent.md and
> https://docs.adcontextprotocol.org/docs/building/by-layer/L3/task-lifecycle.md

## Field names and structure

- If code constructs or parses AdCP task messages, field names, casing, and structure
  must match the AdCP schema for that task exactly — do not add, rename, or repurpose
  protocol fields, and do not drop fields the schema marks as required. AdCP schemas use
  `additionalProperties: false`; extra fields are rejected by conformant counterparties.
- Known shape traps (each of these is a bug if the diff introduces it):
  - `budget` is a **number**, not `{amount, currency}` — currency is implied by
    `pricing_option_id`.
  - `format_id` is an **object** `{agent_url, id}`, never a bare string.
  - `account` is a **discriminated union (oneOf)**: either `{account_id}` or
    `{brand: {domain}, operator, sandbox?}`. Merging fields from both variants (e.g.
    `{account_id, brand}`) fails *both* variants. Code must send exactly one variant.
  - Destination `type` is the enum `'platform'` or `'agent'` — not invented values.
- If code serialises protocol payloads, unknown/extension data must not be placed at the
  top level of the protocol message; use the protocol's extension mechanism
  (`x-`-prefixed annotations / the `context` echo field) rather than ad-hoc fields.
- If code validates inbound protocol messages, it must tolerate unknown fields from the
  counterparty (forward compatibility) rather than hard-failing, unless the spec marks
  that message as closed.

## Response envelope

- Every AdCP response is a **flat structure**: `status` and `message` are always present
  at the top level, task-specific fields sit alongside them (e.g. `products`,
  `media_buy_id`) — not nested under a `data`/`result` wrapper in the synchronous
  response.
- `status` is the single authoritative task-state field. Emitting legacy `task_status`
  or `response_status` alongside `status` is non-conformant — flag it.
- `context_id` must be preserved and echoed for conversation continuity; code that drops
  it breaks multi-turn flows.
- On MCP the typed response lives in `structuredContent`; on A2A it is at
  `task.artifacts[0].parts[0].data`. Code that parses free text instead of the typed
  payload is fragile — flag as a bug if it drives protocol decisions.

## Timestamps and intervals

- All timestamp fields must be ISO 8601 **with an explicit timezone offset**
  (`2026-04-19T10:00:00Z`). Naïve timestamps must be rejected with `INVALID_REQUEST`,
  not silently interpreted.
- Time windows (flight dates, reporting windows) are half-open intervals `[start, end)`
  — start inclusive, end exclusive. Off-by-one handling of the end boundary is a
  conformance bug.
