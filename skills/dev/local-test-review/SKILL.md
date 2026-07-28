---
name: local-test-review
description: >
  Review a project's testing state against a proper test strategy: inventory
  what tests exist, baseline what passes, identify the gaps that matter, and
  produce a prioritized test plan — running the suite via the run-tests skill
  when one exists. Use this skill whenever the user asks "how should we test
  this", "review our test coverage", "what tests do we need", "is our testing
  adequate", "test strategy for X", "assess the tests", or wants a test plan
  for a feature or repo. If a skill named "testing-strategy" is available in
  the session, this skill delegates the strategy design to it. DO NOT USE
  when the user just wants the tests executed — that's run-tests — or wants a
  specific test written (that's implementation work).
---

# Local Test Review

Answer "is this project tested the way it should be?" with evidence, not
vibes: what exists, what passes, what's missing that matters, and a plan
sized to the risk. This is the thinking layer over **run-tests** (the
execution layer) — it never runs a suite by hand, and run-tests never designs
strategy.

## 0. Delegate strategy design if testing-strategy is available

Check the skills available in this session for one named
**`testing-strategy`**. If it exists, plan to delegate the strategy design to
it — but invoke it only when you reach section 3, with the inventory (1) and
baseline (2) in hand: strategy designed blind of the project's facts is the
failure mode this ordering exists to prevent. If it's not available, use the
inline fallback in section 3.

Either way, these house rules — the defaults this plugin enforces, distilled
from the team's repos — apply on top of whatever the strategy says:

- **Determinism boundary**: unit suites must run with no network, no model
  calls, no live services — that work belongs in separated integration/eval
  tiers, gated behind markers or dedicated commands.
- **Escalation ladder**: plans should support fast → scoped → full
  execution, not only an all-or-nothing suite.
- **No invented thresholds**: hold the project to a coverage bar only when
  it documents one — flag meaningful gaps, don't measure green suites
  against imaginary percentages.
- **Tests are never disabled to get to green**, and a repo that declares
  "no tests by design" keeps that status unless the user decides otherwise —
  when that status is declared, do not invent testing gaps or recommend a
  new suite unless the user explicitly opts in.

## 1. Inventory the current testing state

Establish the facts the same way run-tests does (its detection steps and
[`references/detection.md`](../run-tests/references/detection.md) apply):

- Read the project's own instructions — `AGENTS.md` / `CLAUDE.md`,
  `.cursor/rules/*.mdc`, `CONTRIBUTING.md`, CI workflows — for the intended
  testing story.
- Map what actually exists: which tiers (unit / integration / E2E / evals),
  which frameworks, where the tests live, roughly how much there is per
  tier, and which tiers need infrastructure (databases, Docker, env vars).
- Note the discrepancies both ways: documented-but-missing (aspirational
  docs) and present-but-undocumented.
- **Short-circuit for intentional testlessness.** If the project declares
  "no tests by design", the review ends here: report the policy and the
  documented alternative validation, and skip sections 2–4 entirely — no
  pyramid, no gap ranking, no add-tests plan — unless the user explicitly
  opts in to reconsidering the policy (some repos require an RFC first).

## 2. Baseline with run-tests

If a runnable suite exists, invoke the **run-tests** skill to establish what
passes *today* — a red baseline changes every recommendation that follows
(fix before extend). Skip the baseline only when the suite needs
infrastructure the user hasn't agreed to start; report that it was skipped
and why.

## 3. Design the target strategy

Via the delegated skill when available; otherwise:

- **Pyramid shape**: many fast unit tests, some integration, few E2E — high
  confidence at the top, fast feedback at the bottom.
- **By component type**: API endpoints → unit tests for business logic,
  integration for the HTTP layer, contract tests for consumers; data
  pipelines → input validation, transformation correctness, idempotency;
  frontend → component, interaction, visual regression, accessibility;
  infrastructure → smoke, load.
- **Cover**: business-critical paths, error handling, edge cases, security
  boundaries, data integrity. **Skip**: trivial getters/setters, framework
  code, one-off scripts.

Ground the strategy in *this* project: its component types, its risk
profile, its existing conventions — not a generic ideal.

## 4. Gap analysis and plan

Compare inventory (1) + baseline (2) against strategy (3):

- Rank gaps by risk: untested business-critical path > untested error
  handling > missing tier > style issues. A handful of high-risk gaps
  beats an exhaustive inventory of trivial ones.
- For each gap worth closing: what to test, the tier it belongs in, and one
  or two concrete example cases — specific enough that an implementer
  doesn't have to re-derive the analysis.
- Call out over-testing too: slow, flaky, or redundant tests that cost more
  than they catch.

## 5. Report and hand off

Deliver: current state, baseline result (or why skipped), ranked gaps, the
recommended plan, and any repo-quirk warnings for whoever implements. Writing
the tests is separate work — hand the plan to the user, or into the
gather-requirements → create-plan → execute-plan flow for anything
substantial. Don't start implementing tests inside this skill. For the
implementer, note the relevant how-to skills when installed:
**python-testing-patterns** for pytest fixtures/mocking/parametrization,
**webapp-testing** for ad-hoc Playwright verification of web UIs.
