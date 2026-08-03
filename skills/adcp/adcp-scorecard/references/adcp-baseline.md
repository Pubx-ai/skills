# AdCP provisional baseline

**As of 3 August 2026 — re-verify before relying on this.** These scores are advisory inferences
from public artifacts, distilled from a comparative protocol analysis (snapshot of 1 August
2026); the runnable-implementation row was re-scored on 3 August 2026 against the runnable-code
tiers in scoring-model.md. They are a *starting point* for step 3 of the workflow, not evidence.
Replace them with the evaluator's own pilot evidence, and prefer the live docs
(https://docs.adcontextprotocol.org/llms.txt) wherever they disagree with a rationale below.

Assumed decision profile: balanced enterprise buyer/agency with an existing ad-tech stack,
evaluating a bounded near-term pilot with strong transaction-safety requirements. A different
profile likely changes the weights — fix that before scoring (see scoring-model.md).

Under the default weights, this baseline yields a weighted score of **71.6/100** with **all five
hard gates `UNVERIFIED`** — decision status `HOLD` until the gates are tested. The weighted
total is not an approval to transact real spend.

## Provisional scores

| Criterion | Weight | Score | Confidence | Provisional rationale |
|-----------|-------:|------:|------------|-----------------------|
| Existing-stack compatibility | 14% | 2.5 | High | AdCP introduces new lifecycle objects and boundary adapters rather than reusing existing IAB rails (OpenDirect/OpenRTB) directly. |
| Campaign lifecycle coverage | 9% | 4.5 | Medium | AdCP specifies a broad campaign lifecycle: planning, proposals, buying, creative, delivery, measurement. |
| Discovery and pricing flexibility | 7% | 4.5 | Medium | Supports seller-curated, brief-specific proposals without exposing full rate cards. |
| Transaction safety and failure semantics | 10% | 4.5 | Medium | Idempotency, typed errors, and request signing are placed in the protocol itself. Hard gate — `UNVERIFIED` until tested. |
| Identity, authorization and counterparty trust | 10% | 4 | Medium | Uses signed claims and governance context. Hard gate — `UNVERIFIED` until tested. |
| Privacy and compliance integration | 8% | 2.5 | Medium | Governance seams exist, but no general normative consent signal outside specific profiles. Hard gate — `UNVERIFIED` until tested. |
| Human approval and spend controls | 8% | 4 | Medium | Machine governance per commit when configured. Hard gate — `UNVERIFIED` until tested. |
| Delivery, measurement and reconciliation | 8% | 4 | Medium | Defines on-protocol delivery reporting and finality semantics. Hard gate — `UNVERIFIED` until tested. |
| Specification and conformance maturity | 7% | 3.5 | High | Spec-first, but with release-discipline issues and experimental surfaces. |
| Runnable implementation and deployability | 8% | 3.5 | Medium | Sits at the SDK/reference tier of the runnable-code ladder (scoring-model.md): maintained SDKs (e.g. `@adcp/sdk`), a TypeScript reference implementation, and custom agents built on them. Independent production deployments with conformance evidence remain thin, and platform connectors are fewer than incumbent-rail approaches. |
| Counterparty availability and adoption | 6% | 2 | Low | Demand-side ecosystem immature; membership and registry counts are weak proxies for real spend. |
| Composability and exit cost | 5% | 3.5 | Low | Could compose with other layers behind adapters, but no public bridge or interoperability proof. |

## Caveats

- Scores and confidence labels above are the source analysis's own ratings. Under the scoring
  model's evidence standards, a doc-inferred row reads as `LOW` confidence and any score ≥ 4 is
  a hypothesis: confirm it with qualifying evidence or reduce it before reporting a final
  scorecard — the headline total here is not reproducible as a *final* score without that
  evidence.
- All hard gates begin `UNVERIFIED`; a documentation review can never set a gate to `PASS`.
- Adoption evidence: public registry and member counts do not prove transaction volume,
  reliability, or counterparty readiness.
- Low-confidence rows (adoption, composability) are exactly the criteria pilot tests and
  reference checks should target first.

## Sources

- Comparative analysis (repository-level comparison, tradeoffs, evidence gaps):
  https://nofluffadvisory.com/writing/adcp-vs-aamp/
- AdCP introduction (scope, campaign lifecycle): https://docs.adcontextprotocol.org/docs/intro
- AdCP trust and security (governance, signatures, authorization, stated limitations):
  https://docs.adcontextprotocol.org/docs/trust
- AdCP known limitations (explicit gaps, deferred capabilities):
  https://docs.adcontextprotocol.org/docs/reference/known-limitations
- AdCP media buy (lifecycle, reporting surface): https://docs.adcontextprotocol.org/docs/media-buy
- `@adcp/sdk` on npm — maintained SDK evidence for the runnable-implementation row (as of
  August 2026): https://www.npmjs.com/package/@adcp/sdk
- Official reference implementation and buyer skills (as of August 2026):
  https://github.com/adcontextprotocol/adcp
