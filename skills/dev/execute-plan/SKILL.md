---
name: execute-plan
description: >
  Execute a written implementation plan task by task, with a critical review of
  the plan before starting and a checkpoint after every task. Use this skill
  whenever the user asks to "execute the plan", "implement the plan", "run the
  plan", "work through the plan", "start on task 1", "continue the plan", or
  points at a plan directory or file (e.g. under docs/plans/) and asks to build
  it. This is the natural next step after the create-plan skill — reach for it
  as soon as a plan exists and the ask is to start coding. If a skill named
  "executing-plans" is available in the session, this skill delegates the
  loop to it rather than duplicating it, while keeping its own review-gate
  and checkpoint invariants.
---

# Execute Plan

Turn a written implementation plan into working, tested code — one task at a
time, with review gates instead of a blind sprint to the end. The plan was
written so an agent could execute it without guessing; honour that by following
it exactly and stopping when it fails you, rather than improvising around gaps.

## 0. Delegate if a plan-execution skill is available

Check the skills available in this session and delegate the execution loop
to the best match, in this order of preference:

1. **`executing-plans`** (Superpowers, sometimes installed as a personal
   skill) — same-session execution loop with review checkpoints.

Subagent availability is necessary but not sufficient for dispatching tasks
to subagents — **judge the fit against the plan's shape**, because the wrong
loop can cost more than it buys:

- **Subagent dispatch pays off when** tasks are substantial, independent
  (touching different files — the plan's File Structure map tells you), and
  numerous enough that fresh reviewer eyes per task and a lean main context
  outweigh each subagent re-reading schemas, fixtures, and prior code from
  scratch.
- **Prefer a same-session loop** (`executing-plans`, or section 3) when most
  tasks touch the same files (they serialize anyway, so dispatch buys no
  parallelism), when the plan is doc/config-heavy with small tasks (the
  per-dispatch rebuild dwarfs the work), or when the user has signaled that
  speed matters more than maximum review ceremony.
- **State the choice and its reason** before starting; an explicit user
  preference for speed or rigor wins over this heuristic. Mid-plan, if
  dispatch overhead is visibly dominating (long rebuilds yielding only
  trivial findings), say so and propose switching loops rather than
  silently continuing at the chosen pace.

When the criteria favour dispatch, that is a **proposal to the user**, never
a silent switch — the consent gate in the invariants below governs. Either
answer continues execution:

- **User agrees** → run the section 3 loop, dispatching tasks to subagents;
  every invariant below still binds each dispatched task.
- **User declines, or dispatch was never worth proposing** → invoke
  `executing-plans` when present and follow its execution loop instead of
  the one in section 3; without it, use section 3 directly.

Delegation covers the loop, not the guarantees. These invariants apply no
matter which loop runs, and win over anything the delegated skill says to the
contrary:

- execution defaults strongly to **same-session** — dispatch tasks to
  subagents only when the user explicitly requests it or agrees to a
  proposal: if the plan's shape makes dispatch look clearly beneficial
  (large, independent, numerous tasks), propose it with the trade-off and
  wait. Never dispatch silently — including when the delegated skill's own
  text recommends a subagent-driven variant,
- run the **local-review** skill and address its findings before **every**
  commit,
- run the **local-pr-review** skill and address its findings before the
  branch is first published as a ready-for-review PR — or before a draft PR
  is marked ready; pushes to an existing user-approved draft ride on the
  per-commit local-review gate instead of a full branch review each time,
- never push the branch or open a PR without the user's explicit request or
  confirmation — suggest **raise-pr** and wait,
- report a checkpoint to the user after every task (format in step 3.6).

If `executing-plans` is not available — or the user prefers the built-in
loop — follow the process below.

## 1. Locate the plan

- Plans usually arrive from the **create-plan** skill as a directory under
  `docs/plans/<feature-slug>/` containing `plan.md` (overview, global
  constraints, checkbox task index) and `tasks/NN-<task-slug>.md` files. If the
  user didn't point at a plan, look there before asking.
- A single-file plan, or one in another location, is fine too — map it onto the
  same shape: an ordered list of tasks, each with steps, verification, and
  acceptance criteria.
- For **execution**, read `plan.md` (or the whole single file) plus the
  **first unchecked task only**. Task files are self-contained by design;
  keeping them all in context invites cross-task improvisation. The one
  exception is the pre-flight review (section 2), which scans every task file
  once before execution starts.

## 2. Review critically before touching code

The cheapest moment to catch a bad plan is before task 1. This review is a
quick scan across `plan.md` **and every task file** (search for the patterns
below rather than deep-reading each task) — the only point where the whole
plan is read, since cross-task defects are invisible one task at a time.

- **Gaps:** placeholders ("TBD", "add appropriate error handling", "similar to
  Task N"), steps that say *what* without *how*, references to types or
  functions no task defines.
- **Staleness:** code references that no longer exist, dependencies whose
  versions moved, files the repo has since restructured.
- **Open decisions:** anything the plan flags as unresolved that changes the
  architecture.
- **Workspace safety:** implementation happens on a named feature branch
  created for this plan. Starting anywhere else — `main`/`master`, release or
  production branches, protected branches, detached HEAD — requires explicit
  user consent; absent that, create or switch to a feature branch first,
  using the **create-branch** skill when it's available.

If you find concerns, raise them with the user before starting; don't silently
patch the plan. If the user updates the plan, re-review. If there are no
concerns, create todos from the task index and proceed.

**When no one is available to answer** (e.g. running non-interactively), don't
stall on minor gaps: resolve low-risk implementation details with reasonable,
codebase-grounded choices and record each one in the checkpoint report. Stop
outright for ambiguities touching architecture, security, data integrity,
public APIs, destructive operations, or user-visible behaviour.

## 3. Execute tasks with checkpoints

First, complete `plan.md`'s **Prerequisites** section — dependency installs,
environment variables, migrations, third-party setup. It is one-time setup the
plan requires before task 1; doing it now beats discovering it reactively when
a verification fails. Run low-impact setup (dependency installs, local env
vars) directly, but confirm with the user before any prerequisite that touches
shared or external state — database migrations, third-party account changes,
anything destructive or irreversible. Non-interactively, stop at such a
prerequisite rather than running it silently.

Then, for each task in index order:

1. Mark it in progress. Open its task file — that file plus `plan.md`'s Global
   Constraints is the full spec.
2. Follow the steps exactly — including the test-first cycle (write the
   failing test, verify it fails, implement, verify it passes) **where the
   task's steps call for one**. Tasks with no applicable automated test
   (documentation, configuration, setup) run their task-specific
   verification commands instead of inventing a test. Don't skip
   verifications, and don't substitute your own approach where the plan
   specifies one. One exception: task files usually end with their own
   *commit* step — don't execute it as written. When you reach it, stage the
   task's changes and continue with steps 4–6 below, which replace that step
   with the review-gated commit.
3. Run the task's verification commands and confirm the acceptance criteria —
   each one, not a vibe check. Where the task's verification means running
   the test suite, the **run-tests** skill resolves and runs it the way the
   project intends. If the **verification-before-completion** skill
   is available, apply it: a task is only done when you hold the command
   output proving it, never on the strength of the code looking right.
4. Tick the task's checkbox in the file that holds the task index —
   `plan.md` for directory plans, the plan file itself for single-file
   plans — and mark the todo completed — the
   plan-state change belongs in the same reviewed commit as the task's work,
   so a session that dies at the checkpoint never leaves a completed task
   looking unchecked (and ripe for re-execution).
5. Run the **local-review** skill over the uncommitted changes (task work plus
   the `plan.md` update) and address its findings — every commit gets this
   gate, not just the last one. If the **receiving-code-review** skill is
   available, use it to process the findings: verify each one technically
   rather than implementing it blindly or agreeing performatively. If
   addressing findings changed any code, re-run local-review on the new diff —
   the state that gets committed must be the state that passed the gate. Then
   commit using the **create-commit** skill (conventional commit, as the task
   specifies).
6. **Checkpoint:** report to the user before starting the next task —
   - what was built (one or two sentences),
   - verification evidence (commands run, pass/fail output),
   - any deviation from the plan and why,
   - what the next task is.

   In an interactive session, pause at the checkpoint for a go-ahead if the
   user asked to review as you go; otherwise continue. Non-interactively, the
   checkpoint is a written record, not a pause.

## 4. When to stop and ask

Stop executing immediately — ask rather than guess — when:

- a verification fails repeatedly (after 3 attempts, stop and reassess),
- a step is ambiguous enough that two reasonable implementations diverge,
- a dependency or prerequisite from the plan is missing,
- a local-review pass requests changes that require a decision the plan
  doesn't answer (scope, architecture, product behaviour),
- completing a task would require contradicting an earlier task's interfaces
  or the Global Constraints.

Don't force through blockers, and never mark a task's checkbox without its
verifications passing.

## 5. Finish

After the last task: run the full test suite one final time, summarize what was
built against the plan's Success Metrics / acceptance criteria, and list any
deviations or follow-ups. Before the branch is first published as a
ready-for-review PR — or before an existing draft is marked ready; an
intentionally early draft may be
raised before this gate (with the user's consent), its pushes riding on the
per-commit local-review gate — run the
**local-pr-review** skill over the branch's full diff against **the same
base the eventual PR will target** — the repo base by default; under the
chained-branches option, the previous phase's branch — passed to it
explicitly
and address its findings — the PR gate, just as local-review is the per-commit
gate. If addressing findings adds commits, re-run local-pr-review until the
final diff passes. Pushing the branch and raising the PR are then the
user's call — suggest the **raise-pr** skill and wait for their go-ahead;
never publish a branch or open a PR the user hasn't explicitly asked for or
confirmed.

**The PR gate never blocks task progress.** The whole plan executes as
review-gated commits on the single plan branch; the PR comes once, at the
end — execution never waits on a PR merge. When a plan feels too big for
one reviewable PR, that's usually a scoping smell to report (create-plan
mandates one plan per subsystem). If the user wants incremental review
anyway, offer the two shapes with their costs and let them choose:

- **Grow an open draft PR** — raise early (with consent), keep committing to
  the same branch. Reviewers see progress continuously; no sync machinery;
  the review targets a moving diff.
- **Chained branches per phase** — each phase branches off the previous
  one; execution never blocks on merges. The first phase branches off — and
  its PR targets — the repo base as normal; **each later phase's PR targets
  the previous phase's branch**, not the repo base — tell raise-pr the base
  explicitly, or every stacked PR shows a cumulative overlapping diff.
  Costs the user accepts by choosing it: review feedback on an early PR
  forces a rebase cascade through every later branch, the stack must merge
  in order, and squash merges break it outright — never squash a stacked
  PR.
