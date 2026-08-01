---
name: run-tests
description: >
  Check whether the current project has a test suite, work out the correct way
  to run it, run it, and report results faithfully. Use this skill whenever
  the user asks to "run the tests", "do the tests pass", "run the test
  suite", "check the tests", "test this", "run pytest / vitest / bun test /
  playwright", or when a change needs test verification before commit or PR.
  Detects the runner from the project's own instructions (AGENTS.md,
  CLAUDE.md, .cursor/rules), Makefile/package scripts, and lockfiles rather
  than guessing from memory. Also handles projects that intentionally have no
  tests. DO NOT USE for writing new tests, designing test strategy, or
  reviewing coverage (use local-test-review for those), CI pipeline
  configuration, or debugging test logic (use systematic-debugging for that).
---

# Run Tests

Find out if this project has tests, run them the way the project intends, and
report what actually happened. The single biggest failure mode is running the
*wrong* command confidently: a bare `pytest` in a `uv` project, `bun test`
where only `bun run test` excludes integration suites, or Django tests
without the flags its Makefile encodes. The project always knows better than
memory — this skill's job is mostly to find where it wrote that down.

## 1. Read the project's own instructions first

Before touching a test runner, read what the repo says about testing:

- `AGENTS.md` / `CLAUDE.md` (root and relevant subdirectories)
- `.cursor/rules/*.mdc` — rules marked `alwaysApply` bind here too (venv
  activation requirements commonly hide there, not in AGENTS.md)
- `CONTRIBUTING.md` and `docs/` testing sections
- CI workflows (`.github/workflows/*.yml`) as a last-resort source of truth
  for how tests really run

A documented test command **wins over anything inferred** — but verify it's
real before trusting it: docs sometimes describe code that doesn't exist yet.
If `AGENTS.md` says `pnpm test` and there is no `package.json`, the docs are
aspirational; say so instead of running a command that can't work.

## 2. Confirm tests exist — or that their absence is intentional

Search for test material per stack: `tests/`, `test/`, `**/test_*.py`,
`**/*.test.ts`, `**/*.spec.ts`, `**/*_test.go`, test config in
`pyproject.toml` / `vitest.config.*` / `playwright.config.*` /
`jest.config.*`, or test targets in `Makefile` / `package.json`.

Three outcomes, each with its own report:

- **Tests exist** → continue to step 3.
- **No tests, intentionally.** Some repos state "no test suite by design"
  and define validation as something else (manual browser checks, a schema
  validator's exit code). Run the documented validation instead if one
  exists, report that this is the project's testing story, and **never
  scaffold a test suite** — some repos explicitly require an RFC before one
  may be added. When the documented validation is manual browser checking
  and the **webapp-testing** skill is installed, offer to perform it with an
  ad-hoc Playwright pass (screenshots, console errors) instead of skipping
  it.
- **No tests, no statement.** Report plainly that no test suite was found —
  that's the answer, not a defect to fix on the spot. The **local-test-review**
  skill is the right next step when the user wants a strategy and plan for
  adding them; don't start scaffolding here.

## 3. Resolve the command — precedence matters

Work down this ladder and stop at the first hit:

1. **The documented command** from step 1, verbatim — with one exception: a
   command that would never exit (watch mode) runs in its one-shot form via
   the forwarding rule in step 5, never as-is.
2. **A `Makefile` target or `package.json` script** (`make test`,
   `pnpm test`, `bun run test`). These wrappers are load-bearing: they
   encode Docker wrappers, mandatory flags, and directory selections that
   exclude integration suites. Prefer `<pm> run test` over invoking the raw
   runner the script wraps.
3. **The raw runner, coupled to the right package manager.** The lockfile
   decides: `uv.lock` → `uv run pytest`, `pnpm-lock.yaml` → `pnpm`,
   `bun.lock` → `bun`, `yarn.lock` → `yarn`, `package-lock.json` → `npm`,
   `poetry.lock` → `poetry run`. A bare `pytest` or `npx vitest` in a
   managed project is how the wrong environment gets tested.

Per-stack detection signals and known quirk patterns are in
[`references/detection.md`](references/detection.md) — consult it when the
ladder's answer is ambiguous.

## 4. Check preconditions before running

Documented test setups often assume infrastructure. Verify, don't discover
mid-run:

- **Services**: tests wrapped in `docker compose exec` require the stack to
  be *already running* — check with `docker compose ps`. If it's down, both
  remedies (starting it, or the repo's cold-start
  `docker compose run --rm …` variant) start containers and therefore go
  through the confirmation rule below first. E2E suites may need a database
  up and migrations applied before anything can run.
- **Environment variables**: missing required env vars can kill a suite at
  collection time, which looks like a broken repo rather than a config gap —
  check `conftest.py` / test setup files for what they expect.
- **Virtualenvs**: repos with an activate-the-venv rule mean it — a system
  Python will produce misleading import errors.

If a precondition needs anything heavier than an env var — starting
containers, running migrations, anything state-changing or
resource-intensive — report what's required and get the user's explicit
confirmation before doing it. Non-interactively, stop and report rather than
starting infrastructure silently.

## 5. Run

- **"Run the tests" means the suite the project defines as its test gate** —
  usually the step-3 command, unfiltered.
- **A named subset means filter, not the whole suite** — and the filter is
  forwarded **through** the project's script where one exists
  (`pnpm test -- run path/file.test.ts`, `npm test -- -k expr`) so wrapper
  flags and directory exclusions survive. Raw-runner scoping
  (`pytest path::Class -k expr`, `vitest run path`, `--filter`) is for
  projects where no script wraps the runner.
- **When the caller is iterating on failures** — a fix loop the user or a
  calling skill (e.g. execute-plan) has decided on; run-tests itself never
  initiates fixes — follow the escalation ladder the repos themselves
  document: single failing test → its file → full suite, with fail-fast
  (`-x`, `--bail`) during the loop and a full clean pass at the end.
- **Force one-shot, non-interactive execution — without abandoning the
  script.** Watch modes hang an agent forever: bare `vitest` defaults to
  watch, and `test` scripts sometimes invoke exactly that. Check what the
  script runs; when it would watch, forward the one-shot form through the
  script (`pnpm test -- run`, `npm test -- --watchAll=false`, or `CI=true`
  in the environment) so its flags and exclusions are kept. Bypass the
  script for the raw runner only when forwarding can't work — and replicate
  the script's flags and directory selections when you do.
- Capture the output; long runs go to a scratch file rather than scrolling
  away.

## 6. Report faithfully

- Counts (passed / failed / skipped / errored), duration, and the exact
  command run.
- Failures verbatim — the assertion and location, not a paraphrase. If tests
  fail, say so with the output; never soften a red suite into "mostly
  passing".
- Never "fix" a failure by deleting, skipping, `xfail`-ing, or quarantining
  a test — those repos that mention it at all forbid it, and a quarantine is
  the user's explicit decision. Never bypass hooks with `--no-verify`.
- Failures are reported first; fixing them is the caller's decision, not an
  automatic next step — this skill runs tests, it doesn't debug them.
- Don't invent quality bars: enforce a coverage threshold only when the
  project documents one; never fail a green suite against a bar of your own.

## Critical rules

| Rule | Why |
|---|---|
| Prefer the script/Make target over the raw runner | Wrappers encode flags and exclusions that bare invocations silently lose |
| Match the package manager to the lockfile | The wrong PM tests the wrong environment |
| Check the stack is up before `docker compose exec` wrappers | `exec` needs a running container; cold checkouts fail confusingly |
| A named subset → filter; never run the full suite for one test | Wasted minutes and noisy output bury the signal |
| Skipping/disabling a failing test is never the fix | It hides the failure instead of fixing it — the suite goes green while the defect stays |
| Report the suite that ran, not the one that was asked about | Filtered/partial runs must be labelled as such |
| Use one-shot mode, never watch mode | Bare `vitest`/`jest --watch` never exits; the run hangs |
