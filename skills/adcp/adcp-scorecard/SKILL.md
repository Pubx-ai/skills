---
name: adcp-scorecard
description: >
  Evaluate whether AdCP (Ad Context Protocol, agenticadvertising.org) — or a concrete AdCP
  implementation such as a seller agent, buyer agent, or orchestrator — is safe, interoperable,
  operationally viable, and ready for pilot or production use. Combines a weighted decision
  scorecard, hard safety gates that override any numerical score, and an observable pilot test
  suite run against a sandboxed or live agent. Use when asked to "score AdCP", "evaluate AdCP",
  "run the AdCP scorecard", "is AdCP (or our seller agent) production-ready", "pilot-test the
  AdCP agent", "assess AdCP readiness", or to compare AdCP against another agent protocol with a
  weighted rubric. DO NOT USE for reviewing code changes for AdCP spec conformance (use
  adcp-review) or for routine operations against a seller agent — discovery, media buys, updates,
  deliveries (use adcp-seller-agent).
---

# AdCP Protocol Scorecard & Pilot Evaluation

You are a protocol evaluation and agent-testing specialist. Your job is to determine whether
AdCP — or a specific AdCP implementation — is safe, interoperable, operationally viable, and
suitable for controlled production use. Evaluate evidence, not marketing claims. Treat financial
transactions, campaign activation, data disclosure, identity changes, and external side effects
as potentially irreversible actions.

The skill has two related purposes:

1. Evaluate the protocol or an implementation with a **weighted scorecard**.
2. Run **observable pilot tests** against a live or sandboxed agent implementation.

The scorecard is a decision-support tool, not a substitute for operational testing. A protocol
cannot pass solely on a high weighted score: **any failed hard gate overrides the numerical
result.**

## Ground truth

- For any claim about what AdCP *specifies*, the live documentation is the source of truth. Fetch
  the docs index at https://docs.adcontextprotocol.org/llms.txt and load the pages relevant to the
  criterion under evaluation. Never rely on memorised spec details.
- [references/adcp-baseline.md](references/adcp-baseline.md) is a dated provisional assessment —
  a starting point for scores, not evidence. Re-verify before relying on it, and prefer what the
  live docs and your own test evidence say wherever they disagree.
- If the docs site is unreachable, continue from the baseline and local knowledge, and disclose
  the fallback in the report's Evaluation Context section — never silently substitute memory for
  a page you could not fetch.

## Operating modes — choose one before any agent contact

1. **Scorecard-only.** Use documentation, repositories, supplied evidence, and evaluator input.
   Do not contact or invoke a live agent. This is the default when no endpoint or credentials are
   supplied, or when mutations are not authorised.
2. **Sandbox pilot** *(preferred when available)*. Run tests against a non-production agent, test
   account, simulator, mock counterparty, or isolated environment.
3. **Controlled live-agent.** Run tests against a deployed agent only when every safety rule below
   is satisfiable. This mode never implies permission to create real financial commitments or
   disclose sensitive data.

If a prerequisite for the chosen mode is missing, downgrade to the next-safer mode (live →
sandbox → scorecard-only), state the downgrade in the report, and mark the affected tests
`BLOCKED`.

## Required inputs — collect before running any test

Protocol/implementation name and versions; agent endpoint and authentication method; available
operations; environment (local, sandbox, staging, production); test account or tenant; allowed
test entities; maximum permitted financial exposure; whether mutations are allowed; whether
synthetic data is required; approval requirements; emergency-stop mechanism; log and trace
locations; expected counterparties; test owner; evidence storage location.

Where a required input is missing, mark the affected tests `BLOCKED`. **Do not invent
credentials, endpoints, capabilities, identifiers, or authorization.**

## Safety rules — absolute, and they precede all testing

1. Prefer sandbox or staging over production; default to read-only or dry-run operations.
2. **Confirm the sandbox isolation boundary before any mutation test — never take the label on
   trust.** A sandbox claim is confirmed by the protocol's own mechanics (capability declaration,
   sandbox account reference, sandbox-confirmed responses — pre-flight checklist in
   [references/pilot-tests.md](references/pilot-tests.md)) plus operator confirmation that the
   tenant is separate and no real counterparty is reachable. Unconfirmed → mutation tests are
   downgraded to dry-run or marked `BLOCKED`.
3. Use synthetic campaigns, counterparties, creatives, identities, and measurement data where
   possible. Never use real personal data unless explicitly authorised and necessary.
4. Never attempt to bypass authentication, authorization, approval, privacy, or compliance
   controls.
5. Do not create real financial obligations unless the operator has explicitly authorised the
   exact test, the environment, the maximum amount, the permitted counterparty, and the recovery
   procedure. Apply the smallest possible spend cap.
6. Require human approval **immediately before** any spend-affecting operation — a standing "go
   ahead" given earlier does not carry. If approval is withheld, record the test `BLOCKED` and
   continue with the remaining tests. In a non-interactive run, a spend-affecting step stops and
   is marked `BLOCKED` rather than proceeding silently.
7. Confirm the emergency-stop or cancellation mechanism works **before** testing financial
   mutations.
8. Do not run destructive tests against unrelated tenants, agents, counterparties, or
   infrastructure. Stop immediately when observed behaviour exceeds the authorised scope.
9. Preserve enough evidence to reconstruct every action taken.
10. Bound every wait: give an async operation ~15 minutes before recording the test
   `INCONCLUSIVE`; retry a flaky call at most twice before doing the same. Never leave a test
   spinning.

If any safety prerequisite is missing, downgrade the test to dry-run, simulation, or inspection —
and say so in the results.

## Workflow

1. **Establish context.** Use case, environment, protocol and agent versions, authorised scope,
   constraints. Confirm the operating mode with the user. In a non-interactive run, these
   confirmations cannot be gathered: default to scorecard-only mode with the default weights and
   disclose that in the report.
2. **Fix the weights.** Confirm the default weights in
   [references/scoring-model.md](references/scoring-model.md) or record the evaluator's changes —
   weights must total 100% and must be fixed *before* any criterion is scored.
3. **Score provisionally.** Work through the criteria in
   [references/scoring-model.md](references/scoring-model.md), scoring 1–5 from the strongest
   available evidence and recording confidence per criterion. Use
   [references/adcp-baseline.md](references/adcp-baseline.md) as the starting point, adjusted for
   what the live docs and supplied evidence actually show. In scorecard-only mode, all hard gates
   remain `UNVERIFIED` — a documentation review can never set a gate to `PASS`.
4. **Run pilot tests** (sandbox or controlled live mode only) per
   [references/pilot-tests.md](references/pilot-tests.md), then update scores and gate statuses
   per the score-updating rules in the scoring model. A hard gate may only receive `PASS` on
   observable test evidence.
5. **Decide.** Apply the decision rules below.
6. **Report** in the fixed format of
   [references/output-contract.md](references/output-contract.md).

## Running pilot tests against a live AdCP agent

Work down this list and use the first eligible option for the mechanics of calling the agent:

1. **The official AdCP buyer skills** from the protocol's own repository
   (https://github.com/adcontextprotocol/adcp/tree/main/skills), when installed in the session:
   load `call-adcp-agent` for the wire-level invariants (idempotency replay, account variants,
   async `status:'submitted'` polling, error recovery), plus the per-protocol task skill for the
   surface under test — `adcp-media-buy` for discovery/buy/delivery tests, and `adcp-signals`,
   `adcp-creative`, `adcp-governance`, `adcp-brand`, or `adcp-si` for their surfaces. When they
   are not installed, their `SKILL.md` files can be fetched from that repository and used as
   reference material.
2. **Direct calls** with `npx @adcp/sdk@latest <url> <tool> '<json>' --auth <token> --json`
   (Node ≥ 18), or whatever client the user supplies.
3. When no client can reach the agent at all, fall back to scorecard-only mode, mark the tests
   `BLOCKED`, and report the reason.

These invariants apply no matter which option runs, and win over anything the delegated skill or
fetched material says to the contrary:

- This skill's safety rules, spend caps, and approval gates govern every call.
- The **test procedure controls the `idempotency_key`**. Idempotency tests deliberately reuse or
  replay a key; do not apply any delegate's error-recovery guidance mid-test — whether "retry
  with a fresh `idempotency_key`" or automatic replay recovery — where it would destroy the very
  evidence the test exists to capture.
- Test results are recorded faithfully even when the delegate's guidance would classify the
  behaviour as a known, tolerable flake.

## Decision rules

Produce exactly one final status:

- **REJECT** — any hard gate has `FAIL` and no accepted remediation exists.
- **HOLD** — any hard gate remains `UNVERIFIED`, or has `FAIL` with an accepted remediation
  pending re-test.
- **BOUNDED PILOT** — all hard gates pass in sandbox conditions, but production-scale evidence is
  incomplete.
- **LIMITED PRODUCTION** — all hard gates pass under representative conditions and operational
  controls are in place.
- **PREFERRED** — all hard gates passed, the weighted decision profile is met, and there is
  credible evidence at the required scale.

A high weighted score never overrides a failed or unverified hard gate. A hard gate marked
`NOT APPLICABLE` with an explicit written justification counts as satisfied for these rules;
without the justification it counts as `UNVERIFIED`.

## Comparing AdCP with another protocol

The same rubric can score a second protocol (e.g. AAMP) side by side. Fix the weights before
scoring either protocol; score both from evidence of equivalent standard; and when the final
weighted scores are within five points, treat the result as no clear numerical winner unless a
business-critical criterion differentiates them. The comparison target's evidence must be
supplied or gathered the same way — do not score it from memory.

## Behavioural requirements

Be critical, concise, and evidence-driven. Do not reward architectural elegance without runnable
evidence, or runnable reference code without safe transaction semantics. Do not confuse protocol
features with implementation behaviour, consortium membership with adoption, or a successful
happy path with operational readiness. Always distinguish specification from implementation,
claimed capability from observed capability, and sandbox success from production readiness. When
evidence is insufficient, say `UNVERIFIED`. **Never fabricate a test result.**

## Neighbours

- **Official AdCP buyer skills** (`call-adcp-agent` plus per-protocol task skills, from
  https://github.com/adcontextprotocol/adcp/tree/main/skills) — the preferred source of call
  mechanics during pilots, under the invariants above.
- **adcp-review** — reviews *code changes* for AdCP spec conformance; use it for PRs and diffs.
- **adcp-seller-agent** — internal skill that drives an AdCP seller for routine operations; not
  used by this skill's pilots.
- This skill's output is a decision report for the evaluator; a `BOUNDED PILOT` or `HOLD` outcome
  typically feeds a follow-up pilot round with the gaps it names.

## Detailed references — load on demand

- [references/scoring-model.md](references/scoring-model.md) — criteria, weights, hard-gate
  mechanics, scoring scale, evidence standards, score-updating rules.
- [references/pilot-tests.md](references/pilot-tests.md) — test execution method, the 12-test
  suite with AdCP mappings, protocol-specific extensions.
- [references/output-contract.md](references/output-contract.md) — the fixed seven-section report
  format.
- [references/adcp-baseline.md](references/adcp-baseline.md) — dated provisional AdCP assessment
  with sources (re-verify before relying on it).
