# Implementation Plan Template

A plan is a **directory, not a file**. The executing agent reads `plan.md` plus
exactly one task file at a time — write both artifacts so that is enough:

```text
docs/plans/<feature-slug>/
├── plan.md              # overview, global constraints, checkbox task index
└── tasks/
    ├── 01-<task-slug>.md
    ├── 02-<task-slug>.md
    └── …
```

Omit sections that genuinely don't apply (e.g. Deployment for a library change,
database migrations for a UI-only feature) rather than padding them. Keep every
entry concrete — file paths, versions, function names, and measurable criteria
beat vague descriptions.

## `plan.md` — overview and task index

### Executor preamble

Start the file with this note, verbatim:

> **For the executing agent:** work the Task Index in order. For each task, open
> only that task file, complete its steps, run its tests, then tick the task's
> checkbox here before moving on. Every task implicitly includes the Global
> Constraints below.

### 1. Executive Summary

- Feature overview and the value it delivers
- Technical approach (high-level)
- Key architectural decisions and rationale
- Assumptions made (especially any carried over from the requirements doc)
- Complexity: Simple / Medium / Complex
- Tasks: N tasks

### 2. Technical Architecture

- **System Overview:** how the new components interact with existing ones
- **File Structure:** every file created or modified, one line each with its
  single responsibility — the map that task boundaries follow
- **Data Flow:** user action → processing → persistence → UI update
- **Technology Choices:** each choice with its justification
- **Integration Points:** each touched system with the integration approach

### 3. Global Constraints

Project-wide requirements every task must honour, one line each, copied
**verbatim** from the requirements doc — version floors, dependency limits,
naming and copy rules, performance budgets, platform requirements. Listing them
once here means no task has to repeat them, and every task is bound by them.

### 4. Prerequisites

One-time setup that must happen before task 1:

- **Dependencies:** exact install commands, e.g. `npm install zustand@4.5.0`
- **Environment:** variables to add and where, e.g. `.env.local`
- **Database:** migrations or seeding to run first
- **Third-Party:** external account/setup steps

### 5. Task Index

One checkbox line per task — title, file path, and dependencies. This is the
executor's progress tracker:

```markdown
- [ ] Task 1: Define cart types — `tasks/01-cart-types.md`
- [ ] Task 2: Cart Zustand store — `tasks/02-cart-store.md` (depends on: 1)
- [ ] Task 3: Cart drawer UI — `tasks/03-cart-drawer.md` (depends on: 2)
```

Order the index so each task's dependencies appear above it and the system is
testable incrementally.

### 6. Testing Strategy

- **Unit:** coverage target, framework, mocking approach, critical units — taken
  from the requirements' TESTING REQUIREMENTS, not invented
- **Integration/E2E:** critical flows and tools (when the requirements call for it)

### 7. Documentation

- **Code:** docstrings/JSDoc expectations, type documentation
- **Project:** README updates, feature docs, ADRs for major decisions

### 8. Deployment

- **Environment:** config differences across dev/staging/prod
- **Migration:** script, test approach, rollback plan
- **Feature Flags:** flag name and rollout strategy (if used)
- **Monitoring:** metrics, logging, error tracking to add

### 9. Success Metrics

- **Technical:** performance and reliability benchmarks from the requirements'
  CONSTRAINTS
- **User Acceptance:** the requirements' ACCEPTANCE CRITERIA, restated as the
  definition of done
- **Quality Gates:** tests passing, review, docs updated

## `tasks/NN-<task-slug>.md` — one file per task

Each task file must stand alone: the executor reads it with only `plan.md` in
context, never the other task files. See `example-task.md` for a fully worked
example.

````markdown
# Task N: [Action-Oriented Title]

**Objective:** [What and why in one sentence]

**Files to Create/Modify:**
- `path/to/file.ts` - [purpose]

**Dependencies:**
- Prerequisites: [None / Task X]
- Libraries: [library@version]

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact names, signatures,
  and import paths. This file is the executor's only view of those tasks.]
- Produces: [what later tasks rely on — exact function/component names,
  parameter and return types. Later tasks will import these names verbatim.]

**Implementation Steps:**

Steps follow the TDD cycle: failing test → verify it fails → implement →
verify it passes → commit. Show code where it removes ambiguity; a reference
to an existing pattern (`follow path/to/similar.ts`) is fine where the repo
already answers the question.

- [ ] *Step 1: Write the failing tests* — test file path, the scenarios to
  cover (named concretely, with boundary values), what to mock
- [ ] *Step 2: Run the tests, verify they fail* —
  Run: `[exact command]`
  Expected: FAIL with `[expected error]`
- [ ] *Step 3: Implement* — the code, or the exact signatures plus the existing
  pattern to follow; integration and edge-case handling spelled out
- [ ] *Step 4: Run the tests, verify they pass* —
  Run: `[exact command]`
  Expected: PASS
- [ ] *Step 5: Commit* — conventional-commit message, e.g.
  `git commit -m "feat(cart): add cart store"`

**Acceptance Criteria:**
- [ ] Testable condition (behaviour or metric, never an adjective)
- [ ] ...

**Code References:**
- Similar implementation: `path` (lines X–Y)
- Utility to reuse: `func()` from `path`
- Convention: [from AGENTS.md]
- Types: `Type` from `path`

**Potential Issues:**
- [Known problem] → [planned solution]
- [Edge case] → [how to handle it]
````
