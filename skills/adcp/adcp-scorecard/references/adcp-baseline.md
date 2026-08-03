# AdCP provisional baseline

**As of 3 August 2026, evaluated against live docs build 3.1.2 — re-verify before relying on
this.** These scores are advisory inferences from public artifacts: distilled from a comparative
protocol analysis (snapshot of 1 August 2026), then re-scored on 3 August 2026 against the live
docs (`reference/known-limitations`, docs build 3.1.2) and the runnable-code tiers in
scoring-model.md. They are a *starting point* for step 3 of the workflow, not evidence. Replace
them with the evaluator's own pilot evidence, and prefer the live docs at
docs.adcontextprotocol.org wherever they disagree with a rationale below.

**Protocol version assumption:** the scores assume an implementation current with the 3.1-era
docs. Safety expectations are version-dependent — request signing on mutating calls is normative
from 3.1, while 3.0 permits bearer-only auth — so re-check the transaction-safety and identity
rows against the target agent's declared version before reusing them.

Assumed decision profile: balanced enterprise buyer/agency with an existing ad-tech stack,
evaluating a bounded near-term pilot with strong transaction-safety requirements. A different
profile likely changes the weights — fix that before scoring (see scoring-model.md).

Under the default weights, this baseline yields a weighted score of **68.0/100** with **all five
hard gates `UNVERIFIED`** — decision status `HOLD` until the gates are tested. The weighted
total is not an approval to transact real spend.

## Provisional scores

| Criterion | Weight | Score | Confidence | Provisional rationale |
|-----------|-------:|------:|------------|-----------------------|
| Existing-stack compatibility | 14% | 2.5 | High | AdCP introduces new lifecycle objects and boundary adapters rather than reusing existing IAB rails (OpenDirect/OpenRTB) directly. |
| Campaign lifecycle coverage | 9% | 4.5 | Medium | AdCP specifies a broad campaign lifecycle: planning, proposals, buying, creative, delivery, measurement. |
| Discovery and pricing flexibility | 7% | 4.5 | Medium | Supports seller-curated, brief-specific proposals without exposing full rate cards. |
| Transaction safety and failure semantics | 10% | 4 | Medium | Idempotency, typed errors, and request signing are placed in the protocol itself — but signing on mutating calls is normative only from 3.1; 3.0 permits bearer-only auth, and `adcp.idempotency.supported: false` is a legal capability state. Hard gate — `UNVERIFIED` until tested. |
| Identity, authorization and counterparty trust | 10% | 3.5 | Medium | Uses signed claims and governance context, but the registry provides no key-transparency anchoring yet (no enrollment ceremony, no append-only rotation record), so key history is rooted in the counterparty. Hard gate — `UNVERIFIED` until tested. |
| Privacy and compliance integration | 8% | 2.5 | High | Explicitly documented limitations: no jurisdictional consent signal on the wire, no consent-scope propagation, structural privacy only in TMP, no residency/retention mechanism. Hard gate — `UNVERIFIED` until tested. |
| Human approval and spend controls | 8% | 3.5 | Medium | Machine governance per commit when configured, but no protocol-mandated HITL on sync tasks, and schema-level regulated-category enforcement covers only fair_housing / fair_lending / fair_employment. Hard gate — `UNVERIFIED` until tested. |
| Delivery, measurement and reconciliation | 8% | 3.5 | Medium | Defines on-protocol delivery reporting and finality semantics, but there is no protocol-level delivery-dispute flow — buyer/seller disagreement reconciles out-of-band. Hard gate — `UNVERIFIED` until tested. |
| Specification and conformance maturity | 7% | 3.5 | High | Conformance is defined by a storyboard suite with a registry compliance API, but AdCP Verified is self-attested in 3.0 (formal program from 3.1), reference test vectors are partial, and experimental surfaces remain. |
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
