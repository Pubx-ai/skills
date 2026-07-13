---
name: planner
description: >
  Turn a completed requirements document into a detailed, sequential implementation
  plan that an AI coding agent can execute autonomously. Use this skill whenever the
  user asks to "create an implementation plan", "plan this feature", "break this down
  into tasks", "generate a task breakdown", "plan the implementation of…", or points
  at a requirements doc (e.g. under docs/requirements/) and asks what to build next.
  This is the natural next step after the gather-requirements skill — reach for it as
  soon as requirements are signed off. Also use it when handed a spec or detailed
  ticket where the ask is to sequence the work into executable tasks rather than to
  start coding immediately.
---

# Implementation Planner

Act as a principal software architect turning a requirements document into an
implementation plan another AI agent can execute without guessing. The consumer of
this plan is an autonomous coding agent, not a person: it can't tap a teammate on the
shoulder mid-task, so every task must be self-contained, concretely specified, and
independently verifiable. Vague tasks ("improve the cart UX") produce vague code;
the plan's job is to eliminate every decision the executor would otherwise make
silently — and possibly wrongly.

## 1. Locate and validate the requirements

Plans inherit the quality of their requirements, so start there.

- Requirements usually arrive from the **gather-requirements** skill as a file under
  `docs/requirements/<feature-slug>.md` (or `requirements.md` at the repo root). If
  the user didn't point at a document, look there before asking. Inline requirements
  in the conversation are fine too.
- Expect the structure produced by gather-requirements — DESCRIPTION, USER STORY,
  ACCEPTANCE CRITERIA, TECHNICAL CONTEXT, CONSTRAINTS, TESTING REQUIREMENTS, SCOPE,
  INTEGRATION POINTS, ASSUMPTIONS & OPEN QUESTIONS, ADDITIONAL CONTEXT — but don't
  demand it. Map whatever you're given onto those dimensions and identify what's
  genuinely missing versus merely phrased differently.
- Pay special attention to **ASSUMPTIONS & OPEN QUESTIONS**: an open question that
  changes the architecture (data model, sync strategy, auth boundary) must be
  resolved before planning around it. Ask the user; don't silently pick an answer.
- If the requirements are too thin to plan from (no acceptance criteria, unknown
  stack, unclear scope), say so and either ask targeted questions or suggest running
  gather-requirements first. Don't produce a confident plan on top of guesses.
- **Scope check:** if the requirements span multiple independent subsystems,
  propose one plan per subsystem instead of a single sprawling document. Each
  plan must produce working, testable software on its own.

**When no one is available to answer** (e.g. running non-interactively), don't
stall: make reasonable, codebase-grounded assumptions, state them explicitly in the
plan's Executive Summary, and carry any genuinely unresolvable items into the plan
as flagged decision points rather than inventing answers.

## 2. Gather project context

The codebase answers questions the requirements don't — and constrains the design.

- Read `AGENTS.md` / `CLAUDE.md` (conventions, standards), `README.md` (tech stack,
  setup), and anything under `/docs` (architecture, API specs, prior decisions).
- Skim the areas the feature will touch: real patterns, naming, utilities, existing
  types. Every existing pattern you reference in a task is a decision the executing
  agent doesn't have to make — reuse beats reinvention.
- When a task hinges on an external library's behaviour or API surface, verify it
  with the **context7 MCP** rather than guessing; use the **tavily MCP** for open
  web search when broader context is needed.

## 3. Analyze and design

Before writing tasks, work out the shape of the solution:

- **Architecture** — how the feature fits the existing system; which components are
  new vs. modified; data flow from user action to persisted state.
- **File structure** — before decomposing into tasks, map every file the feature
  creates or modifies and what each one is responsible for. One clear
  responsibility per file; prefer smaller, focused files, but follow the repo's
  existing layout rather than restructuring it. This map locks in the
  decomposition: task boundaries follow file responsibilities, and each task
  should produce self-contained changes that make sense on their own.
- **Technical approach** — key choices (state management, API design, schema
  changes) with justification grounded in the repo's existing stack.
- **Integration** — every touchpoint from the requirements' INTEGRATION POINTS,
  plus any the codebase reveals that the requirements missed.
- **Risks** — technical risks, tricky migrations, race conditions, third-party
  unknowns — each with a mitigation, not just a mention.
- **Testing** — honour the requirements' TESTING REQUIREMENTS section (coverage,
  tools, critical scenarios); don't substitute your own defaults.

## 4. Present the architectural approach

Before generating the full plan, present a short summary for confirmation: the
technical approach, major decisions with trade-offs, identified risks with
mitigations, and the phase sequence. This is the cheapest moment for the user to
redirect you — a wrong architectural call discovered after 15 detailed tasks wastes
everyone's time.

Wait for confirmation when someone is available to give it. Non-interactively,
proceed with the best-grounded approach and record the decisions and their
rationale in the plan so they can be reviewed later.

## 5. Generate the plan

Write the plan following the structure in
[`references/plan-template.md`](references/plan-template.md), with every task
meeting the principles below. See
[`references/example-task.md`](references/example-task.md) for a fully worked task
at the level of specificity to aim for.

The plan is a **directory, not a single file** — progressive disclosure for the
executing agent, which loads the index plus exactly one task file per session
instead of the whole plan:

```text
docs/plans/<feature-slug>/
├── plan.md              # overview, global constraints, checkbox task index
└── tasks/
    ├── 01-<task-slug>.md
    ├── 02-<task-slug>.md
    └── …
```

The executor works the index in order: read `plan.md`, open the first unchecked
task file, complete it, tick its checkbox in the index, move on. Create the
folders if needed (this mirrors where gather-requirements puts its output); if
the repo has a different plans convention, follow it. Tell the user where you
wrote it.

## Planning principles

**Atomicity.** A task is the smallest unit that carries its own test cycle and
is worth a fresh reviewer's gate — roughly one focused session for an agent.
Fold setup, configuration, scaffolding, and documentation steps into the task
whose deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbour. Each task ends with an
independently testable deliverable and leaves the system in a working state.

**Sequencing.** Foundations first — types, schemas, utilities — then features, then
integration and polish. Respect dependencies explicitly (each task names its
prerequisites) and order tasks so the system is testable incrementally rather than
only at the end.

**Specificity.** Exact file paths, concrete function and component names,
signatures where they matter, expected inputs/outputs, and acceptance criteria
phrased as testable conditions (metrics and behaviours, never adjectives like
"fast" or "clean").

**Context preservation.** Point each task at the existing code it should imitate:
similar implementations with file paths, utilities and hooks to reuse, conventions
from `AGENTS.md`. The executing agent starts each task fresh — the references you
embed are its memory.

**Self-containment.** The executor loads `plan.md` and one task file — nothing
else. Each task file must therefore be readable with zero other task files in
context. Its **Interfaces** block (Consumes: the exact signatures it uses from
earlier tasks; Produces: the exact names and types later tasks rely on) is the
only way a task learns its neighbours' contracts — spell them out. Never write
"similar to Task N": repeat the content, because the executor may never open
Task N.

**No placeholders.** These are plan failures — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" without naming the actual scenarios
- "Similar to Task N" (repeat the content instead)
- Steps that describe *what* to do without showing *how* — a step that changes
  code shows the code or the exact signature plus the pattern to follow
- References to types, functions, or methods not defined in any task

## Before finalizing

Re-read the requirements with fresh eyes and verify the plan against this bar —
it's what separates an executable plan from a wish list:

- **Spec coverage.** Walk each requirement and point at the task that implements
  it — a requirement with no task means adding the task. The plan covers
  everything in SCOPE (MVP features), and nothing marked Out of Scope has crept
  in.
- **Placeholder scan.** Search every task file for the banned patterns above and
  replace each with the actual content.
- **Consistency.** Types, function signatures, and property names used in later
  tasks match what earlier tasks define — `clearLayers()` in task 3 but
  `clearFullLayers()` in task 7 is a bug. Dependencies are mapped, the index
  order respects them, and every index entry points at a task file that exists
  (and vice versa).
- **Self-containment.** Each task file makes sense opened on its own: measurable
  acceptance criteria, explicit testing requirements, no ambiguous requirements
  ("ensure quality", "handle errors appropriately"), and an Interfaces block
  covering everything it shares with its neighbours.
- Code references point at real files in this repo (verify they exist).
- Sections of the template that genuinely don't apply (e.g. deployment for a
  library, migrations for a UI-only change) are omitted rather than padded.

Fix issues inline and move on — no re-review loop.

## Communication style

Be professional and direct when presenting the approach; state assumptions plainly
so they can be corrected. Be open to feedback and alternatives at the approach
stage — but once the approach is confirmed, generate the complete plan in one pass
without further back-and-forth.
