# Running the AdCP scorecard against an AdCP agent

Human-facing guide for operators. The skill itself lives in [SKILL.md](SKILL.md) — Claude loads
that automatically; this file is the checklist for *you*: what to prepare, how to kick the
evaluation off, what to expect while it runs, and how to read the result.

## What you get

A decision report with a weighted 0–100 score across 12 criteria, a status for each of the five
hard safety gates (transaction safety, identity/trust, privacy/compliance, approval/spend
controls, measurement/reconciliation), and one final status: `REJECT`, `HOLD`, `BOUNDED PILOT`,
`LIMITED PRODUCTION`, or `PREFERRED`. Hard gates override the number — a 90/100 with one failed
gate still cannot ship: `REJECT`, or `HOLD` at best when a remediation has been accepted.

## Quick start (no agent needed): scorecard-only

If you just want a desk evaluation from documentation and supplied evidence:

> "Run the AdCP scorecard in scorecard-only mode for [your use case]."

No agent is contacted. Expect the hard gates to come back `UNVERIFIED` and the decision to be
`HOLD` — that is by design: a documentation review can never set a gate to `PASS`. The one
exception: observable evidence you supply from a prior authorised pilot round of the same
implementation merges under the scoring model's follow-up-round rules — and can then move gate
statuses and the final decision beyond `HOLD` (a merged prior `FAIL` can mean `REJECT`). Use
this mode to find out *which* pilot tests matter most for your context.

## Full run: pilot tests against a real agent

### 1. Prerequisites

Everything a pilot run needs, in one list:

1. **This skill installed**:

   ```bash
   npx skills@latest add pubx-ai/skills -s adcp-scorecard
   ```

2. **Node.js ≥ 20** with `npx` on PATH (the pilot calls run via `npx @adcp/sdk@latest`; the CLI
   is fetched and cached on first use — no global install):

   ```bash
   node --version    # must be >= 20
   ```

3. **A sandboxed or test AdCP agent** to point at. Never start with production. For a local
   seller (e.g. curation_seller) the endpoint is typically `http://localhost:3001/mcp`.
4. **A bearer token** the agent accepts, for a **test account/tenant** — not a production
   principal. Obtain it from the platform owner, or from your local seller's dev configuration.
5. **Network access** to the agent URL from the machine running Claude Code.
6. **The official AdCP buyer skills** installed (preferred source of call mechanics):

   ```bash
   npx skills add adcontextprotocol/adcp --skill call-adcp-agent --skill adcp-media-buy
   ```

   Add the task skill for whichever surface you're testing (`adcp-signals`, `adcp-creative`,
   `adcp-governance`, `adcp-brand`, `adcp-si`), or `--skill '*'` for all seven. Without them
   the skill falls back to fetching their `SKILL.md` files from GitHub, then to direct
   `npx @adcp/sdk` calls.

7. **Sanity-check connectivity** before involving the evaluator (the env prefix keeps the token
   out of process arguments — no separate export needed):

   ```bash
   ADCP_AUTH_TOKEN=<TOKEN> npx @adcp/sdk@latest http://localhost:3001/mcp get_adcp_capabilities '{}' --json
   ```

### 2. Decide the test envelope

The skill will ask for these if you don't supply them — runs go faster when you have answers
ready. Tests whose inputs are missing are marked `BLOCKED`, never improvised:

- Environment (local / sandbox / staging) and whether **mutations are allowed**
- **Maximum permitted financial exposure** (smallest cap that still exercises the flow)
- Allowed test entities (accounts, brands, campaigns) and whether synthetic data is required
- Approval requirements and who the **test owner** is
- The **emergency-stop / cancellation mechanism** and its **agreed maximum stop latency** — the
  skill verifies the mechanism works *before* any financial-mutation test, and Test 12 measures
  against the latency you declare
- Log/trace locations and where evidence should be stored — keep the evidence directory out
  of version control (gitignore it, or use a path outside the repo): raw responses land there
  unredacted

### 3. Start the evaluation

Example prompt:

> "Run the AdCP scorecard in sandbox pilot mode against `http://localhost:3001/mcp`. Mutations
> are allowed up to $50 against the test tenant, synthetic data only, I'm the test owner, and
> the emergency stop is pausing the campaign via `update_media_buy`. Store evidence in
> `./scorecard-evidence/`."

The agent URL and bearer token are session inputs like the mode and spend cap — include them in
the kickoff prompt or hand them over when the skill asks once. It passes the token to CLI calls
via a per-command environment prefix, never `--auth` argv. Use test-tenant tokens; keep
production credentials out of shared or logged chats.

### 4. What happens during the run

1. Weights for the 12 criteria are confirmed **before** scoring (defaults in
   [references/scoring-model.md](references/scoring-model.md); change them now or not at all).
   In sandbox mode the skill also runs a **sandbox isolation pre-flight** before any mutation —
   AdCP capability declaration, sandbox account reference, and `sandbox: true` response
   confirmation — plus asking you to confirm the tenant is separate and no real counterparty is
   reachable. It will not take the "sandbox" label on trust.
2. A provisional scorecard is drawn from the live AdCP docs plus the dated baseline in
   [references/adcp-baseline.md](references/adcp-baseline.md).
3. The pilot suite in [references/pilot-tests.md](references/pilot-tests.md) runs — 12 tests
   covering idempotency, authorization, revocation, privacy gates, spend controls, outage
   behaviour, reconciliation, versioning, restart recovery, and the kill switch.
4. **Expect to be asked for approval immediately before every spend-affecting operation** — a
   blanket "go ahead" given earlier does not carry. Declining marks that test `BLOCKED` and the
   run continues.
5. Scores and gate statuses update only where test evidence justifies it; a passing sandbox test
   caps a criterion at 3–4, never an automatic 5.

### 5. Read the report

The report follows the seven sections in
[references/output-contract.md](references/output-contract.md): executive decision, evaluation
context (including which docs pages were actually fetched), scorecard, hard-gate summary,
per-test results, critical findings, and the smallest safe next step.

- `HOLD` with `UNVERIFIED` gates → the named tests still need to run (or re-run unblocked).
- `BOUNDED PILOT` → gates passed in sandbox; the gap to production is listed evidence, not vibes.
- Any gate `FAIL` with no accepted remediation → `REJECT` regardless of the weighted score; with
  an accepted remediation the status is `HOLD` pending a passing re-test. Either way the number
  never overrides the gate.

Typical follow-up: fix what blocked a test, then ask for a re-run of just those tests — results
merge into the same scorecard.

## Related

- [SKILL.md](SKILL.md) — the skill itself: modes, safety rules, workflow, decision rules.
- [../../../README.md](../../../README.md) — repo overview and install instructions.
