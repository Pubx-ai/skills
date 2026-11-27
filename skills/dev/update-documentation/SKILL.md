---
name: update-documentation
description: >
  Audit existing project documentation against the code as it is now and update what has
  drifted — either the whole documentation set, or scoped to one branch's changes as a step of
  raising a PR. Use this skill whenever the user asks to "update the docs", "bring the
  documentation up to date", "sync the docs with the code", "check if the docs are stale",
  "refresh the architecture doc", "the docs are thin — flesh them out", or asks whether a change
  needs documentation updates — and as the documentation step of the raise-pr flow, where it
  runs branch-scoped before the PR review.
  DO NOT USE when the project has no documentation yet — creating docs from scratch is
  create-documentation's job. DO NOT USE for agent-instruction files such as AGENTS.md or
  CLAUDE.md (operating instructions for agents, a different genre from orientation docs), for
  changelogs or release notes, or for generated API reference — typedoc, sphinx, openapi
  generators belong to the project's own tooling.
---

# Update Documentation

Act as a technical documentation specialist keeping documentation truthful. Stale documentation
is worse than none: a reader who finds nothing goes to the code, but a reader who finds a
confident wrong answer acts on it.

**Guiding principle: documentation says what the code *cannot* say.** Point to code; don't
restate it. Every sentence that paraphrases something a reader could learn from the file it
links to is a sentence that will rot the moment that file changes.

## 1. Establish the scope

Two modes, decided by how this skill was invoked:

- **Branch-scoped** — invoked as part of raising a PR (the raise-pr skill runs this step before
  its review gate) or asked about a specific change. Whatever names the base — the caller, the
  user, or, standalone with none named, the default branch (`gh repo view --json
  defaultBranchRef -q .defaultBranchRef.name`, or the remote HEAD) — `git fetch origin <base>`
  first and diff with `git diff origin/<base>...HEAD`: a local base branch is only as fresh as
  its last update, and the triple-dot form scopes the diff to this branch's own changes. The
  audit covers the documentation files the diff itself touches, plus documentation claims
  elsewhere that the diff could invalidate —
  renamed or moved paths, changed behaviour, new or removed components, altered setup or
  workflow.
- **Full audit** — asked generally ("update the docs", "are the docs stale?"). The audit covers
  every documentation claim against the current codebase.

Say which mode is running before auditing, so a wrong guess is cheap to correct.

## 2. Find the documentation

Locate what exists: `docs/`, the root `README.md`, and any other orientation docs the repo
carries. Read `AGENTS.md` / `CLAUDE.md` for facts only — they are agent operating instructions,
not project docs, and stay out of scope. Then:

- **Documentation exists** → proceed to the audit.
- **None exists** → there is nothing to update. Standalone, say so and point the user at
  **create-documentation**. Inside the raise-pr flow, report "no documentation to update" and
  return — scaffolding docs is never a side effect of raising a PR.
- **Documentation lives elsewhere** (the repo says so — e.g. a team wiki) → audit what is
  reachable; for what isn't, report which claims the change likely staled so the user can fix
  the external home. Never scaffold a parallel `docs/` folder.

## 3. Audit

One pass, not a loop: collect all findings first, then fix. For each in-scope doc file, check
its claims against reality:

- Referenced files, modules, and symbols still exist at the stated locations.
- Described behaviour, workflows, and commands still match the code and CI (verify that scripts
  and targets exist and read their definitions — don't execute state-changing commands to find
  out).
- Diagrams still reflect the top-level flow.
- Recorded decisions and constraints still hold.

While reading, also flag violations of the principles below (volatile facts, restated code,
multi-diagram files, documents that no longer earn their keep) — drift in *kind*, not just in
fact. And check the reverse direction: does
the code contain something the docs now need — a new component, a new external dependency, a
changed contract — that their existing sections should cover? In branch-scoped mode, audit the
full content of documentation files the diff itself changes (an edited doc can introduce a
stale claim as easily as edited code can stale one), and limit the reverse coverage check to
the code, configuration, and workflow changes the diff introduces; in a full audit (including
"the docs are thin" asks), both directions cover the whole codebase.

## 4. Documentation principles

These five principles govern every update; the report in §6 enforces them.

1. **Progressive disclosure.** Lead with the essential, then link to detail. A reader should be
   able to stop at any point and still have something useful.
2. **Reference, don't restate.** Favour file paths and module references over reproducing
   implementation details. "Authentication lives in `src/auth/` — see `JwtStrategy`" is
   correct; a step-by-step prose replay of the token validation flow is wrong.
3. **Stable over volatile.** Document what changes infrequently: purpose, structure, contracts,
   key decisions. Leave out what the code expresses directly — exact function signatures,
   configuration defaults, dependency versions, test counts. Volatile facts get a source
   reference instead of a value.
4. **One diagram maximum per document.** A diagram only where spatial relationships genuinely
   aid understanding — ASCII or Mermaid, top-level flow only, no implementation detail.
5. **Don't document for documentation's sake.** Documentation is a cost a human chose to pay,
   per repo: code answers *what*, docs exist for *why* and orientation, and a document that no
   longer earns its maintenance is deleted (or never written), not kept polished.

## 5. Apply the updates

Make the smallest change that restores truth, in the file's existing voice and structure. The
target shape for each standard file is defined in create-documentation's
[templates](../create-documentation/references/templates.md) — use them to judge what a section
should contain, not as a licence to reformat. If that file is unavailable, judge by the
principles in §4 instead.

- **Stale fact** → correct it, or better, replace the volatile value with a source reference so
  it cannot go stale the same way again.
- **Dead reference** → repoint it to where the thing lives now; if the thing is gone, remove the
  claim.
- **Missing coverage** (the reverse check) → add the minimal entry to the existing section —
  completing a section the docs already carry keeps its claim true, so it is updating. A whole
  missing file is creation, not updating — note it in the report as a create-documentation
  follow-up rather than scaffolding it mid-update, and remember creation is the user's decision,
  never this skill's.
- **Not worth maintaining** (a document that fails principle 5 — restating code, orientation
  value gone, nobody reading it) → propose deleting it and wait for the user's yes. On yes,
  delete it and reconcile everything that links to it; on no, or when no one is available to
  answer, leave it in place, fix only its facts, and record the proposal in the report.
  Deleting is the honest fix for such a document — polishing it spends maintenance on something
  that shouldn't exist — but it destroys work, so it is always the user's call.
- **Structural problems** (the file's organisation fights the principles) → propose the
  restructure and wait for the user's yes; on yes, restructure per the templates; on no, or
  when no one is available to answer, fix the facts in place and record the proposal in the
  report. Never rewrite wholesale on your own judgement — a full rewrite discards accumulated
  judgement and makes review impossible.

## 6. Report

Report faithfully, in both modes:

- Which files changed and why — one line per meaningful correction.
- What was flagged but not fixed: declined or pending restructure and deletion proposals,
  unreachable external docs, missing standard files left for create-documentation.
- **"No updates needed" is a valid outcome, but only after the audit actually ran** — never
  report clean because the docs looked recent or the diff looked small.

Committing follows the invocation: inside the raise-pr flow, the caller commits these changes
via create-commit before its review gate; standalone, present the changes and leave committing
to the user unless they already asked for it.
