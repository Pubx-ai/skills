# Test-stack detection and known quirks

Signals for resolving how a project runs its tests, distilled from this
team's real repositories **as of July 2026** — re-verify a quirk against the
repo before relying on it. The SKILL.md precedence ladder (documented command
→ script/Make target → raw runner + lockfile) still governs; this table helps
when a rung is ambiguous.

## Detection table

| Signal | Stack | Typical command |
|---|---|---|
| `uv.lock` + `[tool.pytest.ini_options]` or `[tool.pytest]` in `pyproject.toml`, or `tests/` | Python, pytest via uv | `uv run pytest` (scoped: `uv run pytest tests/test_x.py::TestY -vv`) |
| `manage.py` + `Makefile` with docker compose | Django in Docker | `make test` (often wraps `docker compose exec -T … manage.py test`) |
| `pnpm-lock.yaml` + `vitest.config.*` | TypeScript, Vitest | `pnpm test` when the script exists (scoped/one-shot: `pnpm test -- run path/file.test.ts`); no script → `pnpm exec vitest run` |
| `pnpm-lock.yaml` + `playwright.config.*` | E2E, Playwright | `pnpm test` / `pnpm exec playwright test path` |
| `bun.lock` | TypeScript, bun:test | `bun run test` — see quirk below before using bare `bun test` |
| `poetry.lock` | Python, pytest via poetry | `poetry run pytest` |
| `package-lock.json` + `jest.config.*` | TypeScript/JS, Jest | `npm test` when the script exists (one-shot: `npm test -- --watchAll=false`); no script → `npx --no-install jest --watchAll=false` (fails rather than downloading jest on demand) |
| Requirements files + `Makefile: test` | Python, venv pytest | `make test` or `.venv/bin/pytest` |
| JSON Schema + validation command in docs | Schema-validated data repo | The documented validator invocation — exit code is the gate |
| None of the above + "no test suite" note | Intentionally testless | Documented manual validation; never scaffold tests |

## Known quirk patterns

Concrete traps observed in this team's repos — check for the *pattern*, since
new repos inherit these templates:

- **Script excludes what bare runner includes.** A `package.json` `test`
  script may enumerate directories precisely to *exclude* integration tests
  that need live services (e.g. bare `bun test` sweeping in
  `tests/integration/` that expects a service on `localhost:8001`). Always
  read what the script actually runs.
- **Mandatory flags hidden in wrappers.** Django repos here require
  `--debug-mode` on every `manage.py test` invocation for correct DB setup —
  the Makefile knows, memory doesn't.
- **`docker compose exec` vs `run --rm`.** `exec`-based Make targets need
  the stack already up (`docker compose up -d` first — which, like every
  container start, needs the user's confirmation per SKILL.md's
  precondition rule); `run --rm` variants work from cold but also start
  containers. Check `docker compose ps` before choosing.
- **Import-time configuration.** Some suites set required env vars in
  `conftest.py` at module scope; a missing variable fails at *collection*
  with a `RuntimeError`, which reads as a broken repo. Check conftest before
  concluding the suite is broken.
- **Databases with no fallback.** Integration tiers may be
  PostgreSQL-only (no SQLite substitute). Look for a documented DB-free
  path (`quick` modes, `-m "not integration"` markers) before assuming the
  full suite can run locally.
- **venv activation as a hard rule.** Some repos require
  `source ./venv/bin/activate` before any Python command, stated only in
  `.cursor/rules/*.mdc` with `alwaysApply` — a skill reading only AGENTS.md
  misses it.
- **Mock hygiene in bun.** `mock.module()` is process-global and leaks
  across test files in nondeterministic order; repos require capturing and
  restoring the real module in `afterAll`. Relevant when interpreting
  CI-only flakes.
- **Tests colocated vs mirrored vs per-app.** Root `tests/`, per-app
  `<app>/test/`, colocated `src/**/*.test.ts`, and mirrored
  `tests/**/*.test.ts` all occur — search broadly before declaring "no
  tests".
- **Docs ahead of code.** AGENTS.md sometimes documents test commands for
  code that isn't committed yet. No manifest (`package.json`,
  `pyproject.toml`) → the documented command is aspirational; report that
  rather than running it.
