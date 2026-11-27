# Sources

Distilled research behind `create-agents-md`. **As of September 2026 — re-verify each row
against the cited page before relying on it**, and update the row when it changes.

## How tools load instruction files

| Tool | Reads | Detail | Source |
| :--- | :---- | :----- | :----- |
| Claude Code ≥ v2.1.277 | `AGENTS.md` natively | Default setting `claude-md-or-agents-md`: **every** `AGENTS.md` and `.claude/AGENTS.md` from the working directory upward is loaded and concatenated — ancestors combine, they do not override, and a subdirectory's is added when Claude reads a file there — and only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` is in the working directory or above it; `~/.claude/CLAUDE.md`, managed `CLAUDE.md` and `.claude/rules/` do not count. Not read: `AGENTS.local.md`, `AGENTS.override.md`, or anything under a `.agents/` directory — a guide there is reached only through a link. Setting `claude-md-and-agents-md` loads both; an `AGENTS.md` that a `CLAUDE.md` imports or symlinks to is never read twice. A natively-read `AGENTS.md` is not listed in `/memory` and does not fire `InstructionsLoaded` hooks; hooks fire as usual for an `AGENTS.md` that a `CLAUDE.md` imports or symlinks to. | [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory), "AGENTS.md" |
| Claude Code < v2.1.277, sessions without feature flags (third-party providers, telemetry off), first session after an upgrade, `disableAllHooks` / `allowManagedHooksOnly`, Claude Code's built-in `agents-md` plugin disabled (unrelated to the `getsentry` skill of the same name below) | `CLAUDE.md` only | Give these sessions `AGENTS.md` via a `CLAUDE.md` that is a symlink to it or whose first line is `@AGENTS.md`. A `CLAUDE.md` that tells Claude in words to read `AGENTS.md` works only if Claude decides to open the file; a `SessionStart` hook that prints it doubles the content on versions that read it natively. Choosing between the two: Claude's Edit and Write tools refuse to write through a symlink and redirect to its target, and on Windows a symlink needs Administrator privileges or Developer Mode and checks out as plain text unless `core.symlinks` is enabled — prefer the import where any reader is on Windows. | same page, "When AGENTS.md support is unavailable", "Remove an earlier AGENTS.md workaround", "Share one file with other coding tools" |
| Claude Code, all versions | `CLAUDE.md`, `CLAUDE.local.md` | Loaded from the working directory and every directory above it, root first, working directory last; subdirectory files load when Claude reads files there; `claudeMdExcludes` skips others' files in a monorepo; block-level HTML comments are stripped before injection. | same page, "How CLAUDE.md files load" |
| Cursor | `AGENTS.md` natively | Listed as the plain-markdown alternative to `.cursor/rules/`; a `.md` file inside `.cursor/rules/` is ignored (no frontmatter). | [cursor.com/docs/context/rules](https://cursor.com/docs/context/rules) |
| GitHub Copilot | nearest `AGENTS.md` | One or more `AGENTS.md` files anywhere in the repository; the nearest in the directory tree takes precedence; separate from `.github/copilot-instructions.md`, which still loads alongside. | [docs.github.com — add repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) |
| Codex and the agents.md ecosystem | nearest `AGENTS.md` | Nested files per package; the closest one takes precedence. | [agents.md](https://agents.md/) |

## Skills worth delegating to or borrowing from

Install counts are from `npx skills find` at the date above. A copy under `~/.claude/skills/`
may be hand-placed and absent from the skills lock file; `npx skills ls -g` shows each copy's
recorded source, and a `diff` against the upstream `SKILL.md` settles whether it matches.

| Skill | Source | Installs | Take | Leave |
| :---- | :----- | :------- | :--- | :---- |
| `agents-md` | `getsentry/skills@agents-md` | 5.6K | Inspect-before-writing order; tables and one-rule-per-bullet; repo-relative paths; external-references table; `CLAUDE.md` as a compatibility symlink, never divergent copies; do not restate linter config or generic slogans | "Do not list installed skills" — this skill lists them with a not-installed clause; its 60-line target (this skill allows 100) |
| `create-agentsmd` | `github/awesome-copilot@create-agentsmd` | 12.9K | Section inventory (setup, workflow, testing, style, build/deploy, security, monorepo, PR guidelines) as a coverage checklist | Its template produces long prose roots; no progressive disclosure |
| `agent-md-refactor` | `softaworks/agent-toolkit@agent-md-refactor` | 4.1K | The five phases: contradictions → essentials → grouping → structure → prune; its deletion criteria table | "Root under 50 lines" (this skill allows 100); its suggested `.claude/` location (this skill uses `.agents/`) |
| `find-skills` | `vercel-labs/skills@find-skills` | 3.5M | Judge by install count (1K+), source reputation, GitHub stars before recommending; `npx skills find`, `npx skills add` | Nothing — installing remains the user's call |

## Worked example

Private Pubx-ai repository — skip when it is not accessible. `Pubx-ai/x10-reviewer`
(github.com/Pubx-ai/x10-reviewer — read `AGENTS.md` and `.agents/`, and confirm `CLAUDE.md →
AGENTS.md`) carries the complete shape this skill produces: a root of at most 100 lines with the
mandatory skills preamble and one-line hard rules each linked to a guide under `.agents/`. Read it
for the shape only, never for another repository's facts: its skill rows are its roster, not
yours, and where any row or sentence differs from `templates.md`, the templates win.

## Format guidance

- [agents.md](https://agents.md/) — the open format: a README for agents; nested files for
  monorepos, nearest file wins.
- [Agent Skills specification](https://agentskills.io/specification) — progressive disclosure:
  a short root, detail one link away.
