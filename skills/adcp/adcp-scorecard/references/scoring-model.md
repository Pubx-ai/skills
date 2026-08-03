# Scoring model

The weighted rubric, hard-gate mechanics, evidence standards, and score-updating rules for the
adcp-scorecard skill. Weights may be changed to reflect the evaluator's operating context, but any
changes must be made **before any criterion is scored**, and must still total 100%.

## Criteria

| Category     | Criterion                                       | Weight | Hard gate | Decision question |
|--------------|-------------------------------------------------|-------:|-----------|-------------------|
| Integration  | Existing-stack compatibility                    |    14% | No  | Can it reuse our DSP, ad server, OpenDirect/OpenRTB, identity and reporting integrations? |
| Scope        | Campaign lifecycle coverage                     |     9% | No  | Does it cover planning, proposals, buying, creative, delivery and measurement for our channels? |
| Commercial   | Discovery and pricing flexibility               |     7% | No  | Can sellers curate proposals without exposing full rate cards, and can buyers negotiate within clear bounds? |
| Safety       | Transaction safety and failure semantics        |    10% | **Yes** | Are financial mutations idempotent, authenticated, retry-safe and explicit under timeout or conflict? |
| Trust        | Identity, authorization and counterparty trust  |    10% | **Yes** | Can every party independently verify identity, authority, revocation and price-affecting claims? |
| Compliance   | Privacy and compliance integration              |     8% | **Yes** | Does the design integrate with our actual privacy diligence, consent and regulated-category controls? |
| Control      | Human approval and spend controls               |     8% | **Yes** | Can we enforce approvals, budget ceilings, policy checks and an emergency stop before money moves? |
| Measurement  | Delivery, measurement and reconciliation        |     8% | **Yes** | Can we reconcile spend, delivery, missing metrics, late updates and finality across counterparties? |
| Standards    | Specification and conformance maturity          |     7% | No  | Are contracts versioned, documented, testable and supported by independent conformance evidence? |
| Delivery     | Runnable implementation and deployability       |     8% | No  | Can our team deploy, operate, observe and recover the implementation without excessive custom engineering? |
| Ecosystem    | Counterparty availability and adoption          |     6% | No  | Will the counterparties and channels we need support it at meaningful production volume? |
| Architecture | Composability and exit cost                     |     5% | No  | Can we isolate the protocol behind adapters, combine layers, and switch without rewriting our domain model? |

Weights total 100%.

## Scoring scale (per criterion, 1–5)

| Score | Meaning | Evidence standard | Typical decision | Risk |
|-------|---------|-------------------|------------------|------|
| 1 | Not viable | Critical capability absent, unsafe, or contradicted by evidence | Reject | Unbounded |
| 2 | Major gaps | Demo/spec claim exists; material controls or integrations missing | Do not pilot with real spend | High |
| 3 | Pilotable | Core path works with compensating controls, bounded scope, human approval | Bounded pilot | Medium-high |
| 4 | Production-capable | Required controls tested; known gaps operationally manageable | Limited production | Medium |
| 5 | Proven at required scale | Independent implementations and production evidence at the required volume | Preferred | Low |

Do not award 4 or 5 based only on documentation, marketing statements, membership announcements,
or reference implementations. This bar governs the scores you **report as final**: a provisional
baseline may carry higher hypothesis scores, but each one must be confirmed by qualifying
evidence — or reduced — before the final scorecard. Half-point scores (e.g. 3.5) are allowed;
the evidence standard of the lower whole band applies.

## Runnable-code evidence tiers

For **Runnable implementation and deployability**, "has code" is not a binary — score the
strongest tier the evidence actually supports:

| Tier | Evidence looks like | Supports score |
|------|---------------------|----------------|
| Examples only | Snippets, demos, unmaintained samples, pseudocode in docs | ≤ 2 |
| SDKs & reference implementations | Maintained SDKs, a runnable reference agent, tooling a team can build real agents on | 3–4 |
| Production implementations with conformance evidence | Independent production deployments plus conformance or interop results | 4–5 |

Within a tier, the deployability half of the decision question (operate, observe, recover
without excessive custom engineering) decides where in the band the score lands. The middle
tier's 4 is earned, not granted: consistent with the scale above, the mere existence of SDKs or
a reference implementation supports at most 3 — a 4 additionally requires the deployability
controls to have been tested. Custom agents built on an SDK are evidence for the middle tier;
they only reach the top tier with production deployment *and* conformance evidence behind them.

## Weighted score formula

For each criterion: `weighted contribution = weight × score ÷ 5 × 100` (weight as a fraction).
The final weighted score is the sum of all contributions, reported on a 0–100 scale.

## Hard-gate mechanics

Hard gates: transaction safety and failure semantics; identity, authorization and counterparty
trust; privacy and compliance integration; human approval and spend controls; delivery,
measurement and reconciliation.

Each hard gate carries exactly one status: `PASS`, `FAIL`, `UNVERIFIED`, or `NOT APPLICABLE`.

1. Any `FAIL` means the implementation must not be approved for production use: with an accepted
   remediation the decision status is `HOLD` pending re-test, otherwise `REJECT`.
2. Any `UNVERIFIED` means the decision status is `HOLD`.
3. A high weighted score cannot override a failed or unverified hard gate.
4. `NOT APPLICABLE` requires an explicit written justification. With that justification recorded,
   the gate counts as satisfied for decision purposes; without it, treat the gate as `UNVERIFIED`.
5. A hard gate may only receive `PASS` when supported by observable test evidence.

## Evidence standards

For every score and gate status, identify the strongest available evidence. Acceptable evidence:
captured request/response payloads, agent execution traces, audit logs, state-transition records,
signed identity or authorization evidence, reconciliation records, test reports, source code,
versioned protocol specifications, independent interoperability results, production references
with meaningful volume.

Classify confidence per criterion:

- `HIGH` — directly observed or independently verified.
- `MEDIUM` — supported by implementation evidence but not proven at representative scale.
- `LOW` — inferred from documentation, public claims, or incomplete artifacts.

Never represent low-confidence evidence as proven behaviour. Low-confidence criteria should
trigger pilot tests.

## Rubric discipline

| Rule | Purpose | How to apply |
|------|---------|--------------|
| Hard gates override totals | Prevent unsafe numerical wins | Any `FAIL` means reject or remediate before spend |
| Weight business outcomes | Reflect the evaluator's context | Weights total 100% and change only before scoring |
| Score evidence, not claims | Reduce standards-body optimism | Require repo, wire trace, test result, or production reference; a press release alone scores ≤ 2 |
| Use confidence explicitly | Expose weak evidence | Low-confidence criteria trigger pilot tests |
| Keep adapters internal | Preserve exit options | Map protocol objects to your own domain model; don't let them leak across the codebase |

## Score-updating rules (after pilot tests)

- Increase a score only when new evidence materially improves confidence.
- Decrease a score when observed behaviour contradicts documentation or expected semantics.
- Do not automatically assign 5 after one passing test. A passing sandbox test generally supports
  a maximum of 3 or 4, depending on realism and completeness; a 5 requires credible evidence at
  the evaluator's required scale.
- A failed hard-gate test sets the relevant gate to `FAIL`.
- A blocked or inconclusive test normally leaves the gate `UNVERIFIED`.
- Do not infer that a control exists simply because the happy path succeeds.
