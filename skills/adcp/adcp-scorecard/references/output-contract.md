# Output contract

Every evaluation report returns these seven sections, in this order. The format is fixed so that
follow-up pilot rounds and cross-protocol comparisons can consume earlier reports directly.

## 1. Executive decision

- Recommended status (`REJECT` / `HOLD` / `BOUNDED PILOT` / `LIMITED PRODUCTION` / `PREFERRED`)
- Leading option, when comparing protocols
- Weighted score (0–100)
- Hard-gate status summary
- One-paragraph rationale

## 2. Evaluation context

- Use case
- Environment and operating mode (including any mode downgrades and why)
- Protocol and agent versions, plus the resolved versions of the tools used — the `@adcp/sdk`
  version `@latest` resolved to, and the source (repo + commit or install date) of any official
  buyer skills used
- Authorised scope
- Constraints
- Weight changes (with the pre-scoring justification)
- The declared decision bars from workflow step 2 — the weighted-score bar, required scale,
  what counts as representative conditions, and the operational controls expected in place —
  that the final status was judged against
- The controlled evidence-store location (from the required inputs) holding the raw, unredacted
  evidence — required before any evidence capture
- The prior evaluation rounds this report builds on (evidence lineage), so consumers can verify
  append-only evidence and status supersession
- Docs provenance: whether the live AdCP docs were fetched, which pages, and the docs build
  version the stable paths resolved to; disclose any fallback to the dated baseline

## 3. Scorecard

For every criterion: weight, score, weighted contribution, confidence, evidence, key risk,
required next action.

## 4. Hard-gate summary

For every hard gate: status, tests performed, evidence, failure or uncertainty, remediation
required.

## 5. Pilot test results

For every test: test ID and name, objective, preconditions, actions performed, expected result,
observed result, side effects, recovery result, status (`PASS` / `FAIL` / `BLOCKED` /
`INCONCLUSIVE`), evidence confidence, evidence reference.

Report faithfully: failures verbatim, partial runs labelled partial, `BLOCKED` never presented
as a pass, and absence of findings never presented as approval. Verbatim has one carve-out:
**redact bearer tokens, credentials, personal data, and confidential payload values** from
reproduced failures — keep exact error codes, field names, and state transitions, and keep the
unredacted raw evidence only in the controlled evidence store named in section 2.

## 6. Critical findings

Explicitly identify: behaviour that contradicted documentation; unsafe default behaviour; silent
fallback or downgrade; ambiguous transaction state; missing audit evidence; unverified claims;
operational dependencies; lock-in or exit risks.

## 7. Decision and next step

- Whether the agent may proceed beyond the current environment
- Which exact risks block progression
- Which tests must be repeated
- What evidence would change the decision
- The smallest safe next stage
