# Pilot test suite

The observable tests that turn hard gates from `UNVERIFIED` into `PASS` or `FAIL`. Run them only
in the operating mode the evaluator authorised, under the safety rules in SKILL.md — those rules
precede and govern every step here.

Most tests name an **AdCP mapping**: the task or mechanism an AdCP implementation typically
exercises for that behaviour. Mappings are orientation, not spec — verify the current task names
and field semantics against the live docs (the llms.txt index plus the stable `docs/<page>`
paths — SKILL.md, Ground truth) before building the test payloads. When the official AdCP buyer
skills are available (installed, or
fetched from https://github.com/adcontextprotocol/adcp/tree/main/skills), load `call-adcp-agent`
plus the task skill for the surface under test (e.g. `adcp-media-buy`) for current payload
semantics — under the invariants in SKILL.md, which control the `idempotency_key` during tests.
The mappings below use media-buy tasks; other protocol surfaces (signals, creative, governance,
brand, SI) have parallel mappings via their task skills.

## Test execution method

For each test:

1. State the test objective and the hard gate or criterion it supports.
2. Record the preconditions and the authorised scope.
3. Capture the initial system state.
4. Execute the smallest safe test action.
5. Capture requests, responses, traces, logs, state changes, approvals, and side effects.
6. Where the test mutated state, and only once the mutation reports an actual **terminal**
   state, **read the mutated entity back and verify the change applied — accepted is not
   applied.** A terminal success whose read-back shows no change, or a revision bump with no
   observable difference, is a silent-downgrade finding, never a pass. The wait bound is not a
   terminal state: a task still pending there is never read back for a verdict — it goes to the
   `INCONCLUSIVE`/reconcile path below, where read-backs serve reconciliation. When no
   read-back surface exists (or the test itself revoked the credentials needed to read), record
   the verification as unavailable and cap the evidence confidence accordingly.
7. Compare observed behaviour with the pass condition.
8. Attempt recovery where authorised, and record the final state.
9. Assign `PASS`, `FAIL`, `BLOCKED`, or `INCONCLUSIVE`, plus an evidence-confidence level.
10. Update the related score and hard-gate status only when justified by the result.

Bound the run: async operations get ~15 minutes before the test is recorded `INCONCLUSIVE`;
retry a flaky **read-only** call at most twice — mutations follow the mutation-retry rule in
SKILL.md's safety rules (same `idempotency_key`, confirmed replay support, approval gate), never
an automatic retry. An `INCONCLUSIVE` recorded at the wait bound is re-checkable —
re-poll later and update the result; slow async completion (e.g. a task parked in
`status:'submitted'` awaiting human approval on the counterparty side) is not itself a failure.
For a mutation, `INCONCLUSIVE` is not the end of the obligation: capture the operation/task
identifier, attempt an authorised stop or cancellation, and run no further mutation tests until
it reaches a terminal or reconciled state (safety rules in SKILL.md) — re-polling later must
not be the only control, and mutation tests still blocked when the run ends are recorded
`BLOCKED`. Do not infer that a control exists simply because the happy path
succeeds.

**Canonical opening sequence** (resolves the stop-verification/first-buy circularity):
`get_adcp_capabilities` (record versions, idempotency declaration, signing block) → account
setup and read-only sandbox probe (isolation pre-flight below) → create the smallest authorised
buy as the stop-verification workflow. The non-spend constraint below binds this creation, and
in **sandbox mode the sandbox account itself is the non-spend workflow**; in live mode a media
buy has no non-spend create path (`dry_run` exists only on sync tasks, and a buy is never a
non-financial entity), so the ordering constraint applies as written — the stop is unverifiable
without spend and mutation tests are downgraded or `BLOCKED`. → Verify the emergency stop on
the buy with a **reversible** mechanism (pause), then resume it and read it back before any
replay test — a terminal stop (cancel, revocation) consumes the fixture; when only terminal
stops exist, verify the stop last or on a separate authorised fixture, and a consumed fixture
means the replay tests run on a fresh authorised buy or are `BLOCKED`. → Proceed to the replay
tests, or, when the idempotency preflight blocks them, to the next authorised test.

**Ordering constraint:** the tests below may otherwise run in any order, but verify that the
emergency-stop or cancellation mechanism works **before** the first mutation test (safety rule in
SKILL.md); Test 12 then formalises the evidence for it. That preflight verification must itself
be non-spend: use a dry-run, a sandbox-account workflow, or a non-financial entity — never a
real financial commitment. If the stop mechanism cannot be verified without spend, mutation
tests are downgraded to dry-run or marked `BLOCKED` — not run on hope.

**Idempotency preflight (before Tests 1–2):** read `get_adcp_capabilities` and validate the
full idempotency declaration, not just the boolean — when `supported` is `true`, check the
accompanying fields the current schema defines (e.g. a replay TTL) and use them to shape the
replay test's timing. A schema-invalid declaration (e.g. `supported: true` without a valid
replay TTL) means replay semantics cannot be trusted: record Tests 1–2 `BLOCKED` and the
invalid declaration itself as a conformance finding feeding the transaction-safety gate. From
the same response, record the agent's **declared AdCP versions** (`adcp.major_versions`, plus
any finer-grained version fields the response carries)
and read the **`request_signing` capability block** — judge signing enforcement from that block,
not from version inference: majors alone cannot tell you whether 3.1's mutating-call signing
mandate applies (3.0 permits bearer-only). When neither the block nor a release-precision
version is available, the signing expectation is unknown — leave the affected gate reasoning
`UNVERIFIED` rather than assuming. If `adcp.idempotency.supported` is not `true`, the
`idempotency_key` is a no-op and a
duplicate submit creates a second real mutation — do **not** send the duplicate: the gate's own
question ("are financial mutations retry-safe?") is already answered, so record the
transaction-safety gate `FAIL` citing the capability response (unless the deployment documents a
compensating dedup control — then test that instead). If the capability cannot be read, record
Tests 1–2 `BLOCKED`.

## Sandbox isolation pre-flight (sandbox mode only)

Before the first mutation test, confirm the isolation boundary instead of trusting the
environment's label. AdCP makes sandbox **account-level and verifiable** (mechanics as of the
media-buy sandbox page in the live docs, August 2026 — locate it fresh via the docs index
plus the stable `docs/<page>` paths (SKILL.md, Ground truth), following the media-buy page's
own links to the sandbox page rather than inventing an unlisted URL, and re-verify before
relying on them):

1. **Capability**: `get_adcp_capabilities` declares `account.sandbox: true`. Not declared or
   `false` → the seller does not support protocol sandbox; do not treat the deployment as
   sandbox on someone's word.
2. **Account reference**: every request must carry sandbox semantics on the account itself —
   implicit account model (`require_operator_auth: false`): natural key with `sandbox: true`
   (declared via `sync_accounts`); explicit model (`require_operator_auth: true`): a sandbox
   `account_id` discovered via `list_accounts` filtered with `sandbox: true`, or supplied
   through the seller's documented out-of-band test-account setup. Either way, record the
   account's provenance (who supplied it, how it was verified as a test account).
3. **Response confirmation**: run one read-only call (e.g. `get_products`, preferring a
   synchronous discovery mode such as `buying_mode: "wholesale"` where the seller supports it —
   brief-driven modes may go async) on the sandbox account and check the success response
   includes `sandbox: true`. During tests, a mutation response *without* that confirmation means
   isolation cannot be confirmed: stop mutations and record it as a finding (the spec says
   sellers SHOULD include it).
4. **No header reliance**: never treat the deprecated `X-Dry-Run` / `X-Test-Session-ID` /
   `X-Mock-Time` headers as isolation — the spec forbids buyers relying on them; only the
   account-level sandbox reference guarantees sandbox semantics.
5. **Operator confirmation**: the tenant is separate from production and no real counterparty
   is reachable from it. Checks 1–4 are self-attested by the agent under test; this one is the
   independent leg and is required — record who confirmed it.

If any check fails or cannot be run: mutation tests are downgraded to `dry_run: true` where the
task supports it (sync tasks), otherwise marked `BLOCKED`; and a "sandbox" that produces a real
side effect is a critical finding — stop testing immediately (safety rules in SKILL.md).

## Common suite

### Test 1 — Duplicate financial mutation

- **Objective:** verify retry safety and idempotency.
- **Procedure:** submit a permitted financial mutation; simulate a timeout or lost response;
  resubmit the identical request with the **same** idempotency identifier.
- **Pass:** exactly one order/booking/media buy exists; the repeated request returns a
  deterministic result; the idempotency decision is auditable.
- **Hard gate:** transaction safety and failure semantics.
- **AdCP mapping:** `create_media_buy` with a repeated `idempotency_key`. The test procedure owns
  the key — never "recover" mid-test by switching to a fresh key.

### Test 2 — Conflicting idempotency reuse

- **Objective:** verify an idempotency identifier cannot be reused for a different transaction.
- **Procedure:** reuse an existing idempotency identifier with materially different payload data.
- **Pass:** a typed conflict or equivalent deterministic rejection; no additional mutation; an
  explicit recovery path.
- **Hard gate:** transaction safety and failure semantics.
- **AdCP mapping:** `create_media_buy` / `update_media_buy` with a reused `idempotency_key` and a
  changed payload.

### Test 3 — Unauthorized pricing or privilege claim

- **Objective:** determine whether the agent independently verifies price-affecting or
  authorization claims.
- **Procedure:** with an *authorised test identity*, claim a higher pricing tier, role, or
  spending authority than the identity possesses. Do not forge third-party credentials or bypass
  access controls.
- **Pass:** the claim is independently verified; invalid claims are rejected or downgraded before
  protected inventory, pricing, or actions are exposed.
- **Hard gate:** identity, authorization, and counterparty trust.
- **AdCP mapping:** account/brand context on discovery and buy tasks; any signed-claim or
  governance mechanism the implementation exposes.

### Test 4 — Revocation during an active workflow

- **Objective:** verify authorization can be withdrawn.
- **Procedure:** begin a permitted workflow; revoke or disable the test agent or credential
  through an authorised administrative mechanism; attempt a further mutation.
- **Pass:** further mutations fail closed; revocation appears in the audit trail; previously
  committed state remains reconcilable.
- **Hard gate:** identity, authorization, and counterparty trust.
- **AdCP mapping:** revoke the bearer token / API key between two calls of a discover → buy →
  update sequence.

### Test 5 — Missing privacy or diligence approval

- **Objective:** verify privacy and compliance enforcement.
- **Procedure:** remove or omit a required approval, consent, diligence result, or
  regulated-category clearance.
- **Pass:** the affected discovery or mutation stops per documented policy; no silent downgrade
  or bypass; the failure is explainable and auditable.
- **Hard gate:** privacy and compliance integration.
- **AdCP mapping:** regulated-category briefs or whatever consent/policy surface the deployment
  documents; check the live docs for what is normative versus deployment-specific.

### Test 6 — Budget or approval threshold exceeded

- **Objective:** verify pre-commitment spending controls.
- **Precondition:** a spend threshold *below* the evaluator's authorised cap must exist —
  a seller-side limit, a deployment approval layer, or a configurable account ceiling. Without
  one, the test cannot be constructed inside the authorization; record `BLOCKED` naming this
  missing precondition rather than a generic reason.
- **Procedure:** construct a permitted test transaction that exceeds its configured budget or
  approval threshold.
- **Pass:** no financial commitment before valid approval; approver and approval scope are
  auditable; the approval cannot be reused outside its authorised scope.
- **Hard gate:** human approval and spend controls.

### Test 7 — Approval or governance service outage

- **Objective:** verify failure behaviour when a required control service is unavailable.
- **Procedure:** in an isolated environment, make the approval or governance dependency
  unavailable; attempt a mutation requiring it.
- **Pass:** the agent fails closed; no orphaned or partially authorised transaction; the workflow
  remains recoverable.
- **Hard gate:** human approval and spend controls.

### Test 8 — Partial delivery or missing measurement

- **Objective:** verify incomplete delivery data can be reconciled.
- **Procedure:** return or simulate partial delivery; omit one committed metric or required
  reporting field.
- **Pass:** missing data is explicit; the report stays tied to the original transaction; the
  discrepancy reconciles without silently treating missing data as zero or complete.
- **Hard gate:** delivery, measurement, and reconciliation.
- **AdCP mapping:** `get_media_buy_delivery` against a buy with known-incomplete delivery.

### Test 9 — Late measurement correction

- **Objective:** verify update and finality semantics.
- **Procedure:** submit an initial delivery or measurement report; submit an authorised late
  correction.
- **Pass:** the correction follows deterministic supersession/versioning rules; the current
  authoritative result is identifiable; history remains audit-ready.
- **Hard gate:** delivery, measurement, and reconciliation.

### Test 10 — Protocol version mismatch

- **Objective:** verify explicit version negotiation and failure behaviour.
- **Procedure:** use an unsupported or incompatible protocol version.
- **Pass:** typed rejection, or a compatible version explicitly negotiated; no silent semantic
  downgrade.
- **Criterion:** specification and conformance maturity (not a hard gate).
- **AdCP mapping:** `get_adcp_capabilities` (supported major versions) plus a request pinned to an
  unsupported version.

### Test 11 — Restart during an in-flight transaction

- **Objective:** verify state recovery.
- **Procedure:** in a sandbox or controlled environment, restart the agent during an active
  transaction.
- **Pass:** the workflow recovers without duplicate spend; approval state is not lost or
  improperly reused; counterparty state remains consistent or deterministically reconcilable.
- **Hard gates:** transaction safety; human approval; reconciliation.

### Test 12 — Emergency stop

- **Objective:** verify the operational kill switch.
- **Procedure:** begin an authorised test campaign or workflow; activate the documented
  emergency-stop mechanism; attempt a new mutation.
- **Pass:** new mutations stop within the agreed control interval; existing state remains
  inspectable and reconcilable; the stop action and initiator are auditable.
- **Hard gate:** human approval and spend controls.
- **AdCP mapping:** the deployment's documented stop mechanism — e.g. `update_media_buy` with
  `paused: true` or `canceled`, or credential revocation at the operator.

## Optional protocol-specific extensions

Add tests where the implementation claims capabilities beyond the common suite — for example:
governance-token validation, cryptographic request signing, proposal expiry, inventory
reservation, price-tier verification, deal-ID generation, creative approval, counterparty
registry validation, measurement finality, streaming updates, cancellation semantics, multi-agent
delegation, capability discovery.

Clearly label these as protocol-specific tests rather than common comparison criteria.
