# AdCP rules — task lifecycle, async handling & idempotency

Apply these when the diff initiates AdCP tasks, handles task status, retries calls, or
implements long-running operations.

> Curated AdCP 3.x snapshot (last curated: 2026-07-12) — when you have web access, fetch the live sources and let
> them win on any conflict:
> https://docs.adcontextprotocol.org/docs/building/by-layer/L3/task-lifecycle.md and
> https://docs.adcontextprotocol.org/docs/protocol/calling-an-agent.md

## Status values

- Only protocol-defined status values may be used: `submitted`, `working`,
  `input-required`, `completed`, `canceled`, `failed`, `rejected`, `auth-required`,
  `unknown`. Inventing statuses (or reusing `pending_approval`, which is an *Account*
  status, for task state) is a conformance bug.
- Terminal states are genuinely terminal — no transitions out of
  `completed`/`failed`/`canceled`/`rejected`.
- `submitted` and `working` mean different things and require different handling:
  - `working` — server is actively processing; the result arrives on the open
    connection. **Do not poll** for `working`.
  - `submitted` — blocked on an external dependency (human approval, publisher review).
    Configure a webhook (preferred) or poll `tasks/get` / `get_task_status` with the
    returned `task_id`, passing `include_result: true` to receive the terminal payload.
- A task that cannot complete synchronously must return `submitted`/`working` and be
  resolvable later — do not block the connection indefinitely, poll-spin, or fake a
  synchronous completion.
- Human-in-the-loop approval is modelled as `input-required` (buyer must respond) or
  `submitted` (seller waiting on an internal human) — not as a bespoke mechanism.
- Transport state ≠ AdCP state: an MCP/A2A task can complete after delivering a payload
  that still says `status: 'submitted'`. Code that treats transport completion as AdCP
  completion (e.g. reads A2A `Task.state: 'completed'` and assumes the media buy exists)
  has a real bug — the work is still queued.

## Idempotency

Every mutating tool (`create_media_buy`, `update_media_buy`, `sync_*`, `activate_signal`,
`log_event`, etc.) requires an `idempotency_key` (UUID). The key semantics matter because
they are the only thing standing between a network retry and a duplicate spend:

- **Same key on retry → replay.** Transport-level retries (timeout, 5xx, dropped
  connection) must reuse the same key; the server replays the same response and, for
  async flows, the same `task_id`.
- **Fresh key → new operation.** Generating a new UUID *because the previous attempt
  failed* is the classic way to create duplicate media buys. Flag any retry path that
  mints a fresh key for the same logical operation as a bug.
- Same key + different body → server returns `IDEMPOTENCY_CONFLICT`; client code must
  not paper over this.
- `IDEMPOTENCY_IN_FLIGHT` → wait (`error.details.retry_after`) and retry with the
  **same** key; a fresh key here turns a safe retry into a double-execution race.

## Reconciliation

- Long-lived buyers/orchestrators should recover lost state via `list_tasks`
  (filter on `submitted`/`working`/`input-required`) rather than assuming local state is
  complete. Code that silently drops in-flight tasks on restart loses money-moving
  operations — worth a finding if the diff introduces such state handling.
