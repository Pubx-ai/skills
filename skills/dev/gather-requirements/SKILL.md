---
name: gather-requirements
description: >
  Turn a raw, underspecified feature request into a structured, implementation-ready
  requirements document before any planning or coding begins. Use this skill whenever
  the user describes something they want built but the details are thin — phrases like
  "I want to add X", "we need a feature that…", "gather requirements", "flesh out this
  ticket", "turn this into a spec", "write the requirements for…", or "what do you need
  to know before building this?" — and also when handed a rough Jira ticket, user story,
  or one-liner that lacks technical context, acceptance criteria, or scope. Also use it
  when the user wants an interview-style interrogation of a feature idea — "grill me about
  this feature", "stress-test these requirements", "interview me about what I want". It
  reads the project's own conventions, asks targeted clarifying questions one decision at
  a time with a recommended answer, and writes a complete requirements doc to a file so an
  implementation planner has everything it needs. Prefer this over jumping straight into
  code when the ask is vague or open to interpretation.
---

# Gather Requirements

Act as a principal engineer turning a fuzzy feature request into requirements another
agent (or person) could implement without guessing. A plan is only as good as the
requirements behind it, and ambiguity is cheapest to resolve *now* — before anyone has
written code against a wrong assumption. So the goal isn't to fill in a form; it's to
understand what's actually being asked, ground it in how *this* codebase already works,
and surface the decisions that would otherwise get made silently (and wrongly) later.

## 1. Gather project context first

Before asking the user anything, learn what the repo can already tell you — many
"requirements" are really just conventions the codebase has already settled.

- Read `AGENTS.md` / `CLAUDE.md` (conventions, standards), `README.md` (tech stack,
  setup), and anything under `/docs` (architecture, API specs, prior decisions).
- Skim the areas the feature would touch to learn the real patterns, naming, and
  utilities in use — reuse beats reinvention.
- When a requirement hinges on an external library or API, confirm its behaviour with
  the **context7 MCP** rather than guessing; use the **tavily MCP** for open web search
  when you need broader context.

This does double duty: it answers questions you'd otherwise burden the user with, and it
lets you ask *sharper* questions about the things the code genuinely can't tell you.

It also draws the line that governs the whole interview: **facts vs. decisions**. Anything
the repo (or its docs, or a library's documentation) can answer is a *fact* — look it up,
never ask. Anything that requires a judgment call — a trade-off, a scope boundary, a UX
choice — is a *decision*: always put it to the user with your recommendation, and never
resolve it silently on their behalf.

## 2. Parse what you were given

Accept the request in whatever form it arrives — free text, bullets, a Jira ticket, a
user story. Pull out the feature description, any implied user stories, technical hints,
constraints, and integration points. Cross-reference against the context from step 1, then
form a clear picture of **what's already answered vs. what's genuinely missing** — so you
only spend the user's attention on real gaps.

## 3. Walk the decision tree

Treat the open gaps as a **decision tree**, not a questionnaire. From the dimensions below,
collect the *decisions* the feature genuinely hinges on (facts were already looked up in
step 1), note which decisions depend on others, and walk them in dependency order — the
answer to "is this stored per-user or per-organisation?" reshapes every schema, auth, and
UI question that follows, so it must be settled first.

Pace the interview adaptively:

- **Design-shaping decisions go one at a time.** Ask, wait for the answer, then continue —
  the answer may prune or reshape the branches below it, and a wall of questions is
  bewildering. The test: if the answer could change what you'd ask next, the question
  goes solo.
- **Small independent details may be batched.** Naming, copy, minor defaults — things
  whose answers don't affect each other — can be grouped into one round so the interview
  stays brisk.
- **Every question carries a recommendation.** Ground it in the codebase context from
  step 1 and give a one-line why, so the user can answer most questions with "yes, do
  that". If the environment provides a structured question tool, present the recommended
  answer as the first option and mark it as recommended; otherwise state it inline.

Skip anything you can reasonably infer, but say what you inferred so the user can correct
it. Draw candidate gaps from these dimensions as relevant to the feature:

- **Technical stack** — framework/versions, key libraries, database & ORM, auth, styling,
  state management (only where not already obvious from the repo).
- **Integration & dependencies** — which components/services/APIs this touches, existing
  schemas/types to reuse, specific files or patterns to follow.
- **Functional behaviour** — key user interactions and workflows, edge cases and error
  states, validations, loading/empty states, UX expectations.
- **Non-functional** — performance targets, security (authz, input handling, secrets),
  accessibility level, browser/device support, SEO where relevant.
- **Testing** — expected coverage, test types (unit/integration/e2e), frameworks, and the
  repo's existing test patterns to mirror.
- **Scope** — MVP vs. full set, what's explicitly out of scope, what must NOT change,
  must-haves vs. nice-to-haves.
- **Business context** — the problem being solved, who the users are, any compliance
  constraints (GDPR, HIPAA, SOC2).

**When no one is available to answer** (e.g. running non-interactively), don't stall.
Make reasonable, codebase-grounded assumptions, state them explicitly, and record anything
still genuinely uncertain under an **Open Questions** section in the document rather than
inventing an answer.

## 4. Compile the requirements document

Once the critical gaps are closed, write the document using the structure in
[`references/requirements-template.md`](references/requirements-template.md). See
[`references/example-requirements.md`](references/example-requirements.md) for a filled-in
example and a contrasting under-specified one.

Save it to a file so it can feed a planner or be reviewed later. Default to
`docs/requirements/<feature-slug>.md` (create the folder if needed); if the repo has no
`docs/` convention, use `requirements.md` at the repo root. Confirm the location with the
user if there's any doubt, and tell them where you wrote it.

## 5. Validate completeness and get sign-off

Before handing off, check the document actually covers:

- Clear feature description and the business value behind it.
- User stories with testable acceptance criteria.
- The key decisions from the interview, each recorded with its answer and who decided.
- Concrete technical context (frameworks, versions, tools) and integration points.
- Non-functional requirements that apply, and testing expectations.
- Explicit scope boundaries (in / out / don't-touch).
- Any assumptions and Open Questions, so nothing ambiguous is hidden.

Then present it to the user and ask for explicit confirmation that it matches their
intent. **Sign-off is a gate, not a courtesy**: do not declare the document ready for
planning until they confirm shared understanding. If they correct something, fold the
correction into the doc — and if it overturns a decision, revisit the branches of the
decision tree that depended on it before asking for sign-off again.

When running non-interactively, skip the gate but say so explicitly in your output, and
make sure everything unconfirmed is visible under Assumptions and Open Questions.

## Communication style

Be relentless about ambiguity, but collaborative in tone — every question arrives with a
recommendation, so the interview feels like working through a design together rather than
being interrogated. Ask design-shaping decisions one at a time in dependency order; batch
only small independent details. Lead with the gaps that would most change the
implementation, and acknowledge what the user already gave you so you don't ask twice.
When several interpretations are plausible, offer the options and say which you'd pick.
When you have what you need, say so plainly ("I have enough to compile the requirements")
rather than padding with more questions.
