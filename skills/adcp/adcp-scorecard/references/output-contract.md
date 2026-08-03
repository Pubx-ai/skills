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
- Protocol and agent versions
- Authorised scope
- Constraints
- Weight changes (with the pre-scoring justification)
- Docs provenance: whether the live AdCP docs were fetched, and which pages; disclose any
  fallback to the dated baseline

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
as a pass, and absence of findings never presented as approval.

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
