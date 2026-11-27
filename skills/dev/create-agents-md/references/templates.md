# Templates

Shapes for the files `create-agents-md` produces. Bracketed text describes what to write and
never survives into a delivered file. Unbracketed sample values (`pnpm test`,
`path/to/file.test.ts`) illustrate shape only — replace them with the repository's own facts.
The skill rows are defaults, not samples: keep a row verbatim when that skill is installed and
relevant and its behaviour matches the repository's documented conventions, mark it recommended
when the roster lacks it, drop it otherwise. Keep the section order; delete an optional section
rather than pad it. One exception to the bracket rule: the angle-bracket placeholders in the
Commit Attribution line stay in the delivered file as written.

## Root `AGENTS.md`

````markdown
# Agent Instructions — [project name]

[Two to four sentences: what the project is and does, its stack and package manager, how it is
deployed if that matters to an agent. Then one of:] `CLAUDE.md` is a symlink to this file. [or]
`CLAUDE.md` imports this file and adds Claude-specific instructions. [Then:] Guides:
[topic-a](.agents/topic-a.md) · [topic-b](.agents/topic-b.md) · [topic-c](.agents/topic-c.md).

## Skills — mandatory

Skills are the workflow, not a suggestion. When a row matches the work, **invoke the skill**,
do not reproduce its steps by hand, and say which skill ran. A row applies only when that
skill is installed: if it is not, say so, offer to install it (`find-skills`, or
`npx skills find QUERY` where `find-skills` is absent), and proceed on your own judgement — never
claim a skill ran when it did not. Nothing fits? `find-skills` (or `npx skills find`) first. In
the table: `→` sequence · `;` both · `,` pick the one that fits.

[When the rows come from a plugin marketplace, one line naming the marketplace and its source,
e.g. "The `dev:` skills are the `dev` plugin from the `pubx-x10-skills` marketplace
(`/plugin marketplace add Pubx-ai/x10-skills`)."]

| When | Skill |
|------|-------|
| Starting any work | `dev:create-branch` |
| Before **every** commit — full pass for code or technical claims, stated inline check for trivial edits; always say which | `dev:local-review` |
| Committing (Angular conventional commits) | `dev:create-commit` |
| Receiving review feedback, bot or human, before acting on it | `receiving-code-review` |
| Before claiming anything is done, fixed or passing | `verification-before-completion` |
| Branch finished: review it, publish only on the owner's request, then the comment loop | `dev:local-pr-review` → `dev:raise-pr` → `dev:address-pr-comments` |
| [Framework or language rows the repo needs, e.g. tests/mocks] | [`vitest`, a pytest skill] |
| A bug, a failing test, unexpected behaviour | `systematic-debugging` |
| A change touches or invalidates documentation | `dev:update-documentation` |
| Editing this file or `.agents/` | `dev:create-agents-md` |
| [When it applies] | `skill-name` *(recommended — not installed here)* |

## Commands

[Runtime and package manager in one line.]

| Task | Command |
|------|---------|
| Test one file | `pnpm vitest run path/to/file.test.ts` |
| All tests / typecheck (deterministic: no network, no model calls) / build | `pnpm test` · `pnpm typecheck` · `pnpm build` |
| Dev server [with any prerequisite an agent will hit] | `pnpm dev` |
| [Anything that costs money or needs credentials — say so in the row] | … |

## Hard Rules

- **[The headline rule, bold, one to three lines.]** → [guide](.agents/topic-a.md)
- [One rule per bullet; each ends in the link to the guide that states it in full.]
  → [guide](.agents/topic-b.md)

## Conventions

- [Code layout: where domain logic lives, what stays thin, what is generated.]
- [Where shared contracts and types live — import, never redefine.]
- [Test placement, fixtures, decision records; the newline-at-EOF rule only when no
  `.editorconfig` already states it.]

## Boundaries *(optional — when the repo has operations an agent must not run unasked)*

- **Always:** [e.g. run the test suite before claiming a fix]
- **Ask first:** [e.g. migrations, dependency upgrades, anything touching production config]
- **Never:** [e.g. commit secrets, run destructive commands, push without being asked]

## Commit Attribution

AI commits carry `Co-Authored-By: <Model Name> <vendor no-reply address>` — the committing
agent fills in the model that actually authored the change and its vendor's no-reply address
(`noreply@anthropic.com` for Claude models), whichever is running, never a name or address
fixed by this file. If the model changes mid-branch, later commits carry the later name; never
retro-fit earlier commits, never attribute a model that did not do the work.
````

## Hard-rule seeds

Rules that have held across repositories. Adopt the ones this repository can honour, one line
each in the root with a link, the full statement in a guide; never copy one the repository
cannot back (no Context7 configured for the repository, a command that does not exist).

- **Read the documentation before acting; never assume, never invent.** Context7
  (`resolve-library-id` → `query-docs`) first, at the pinned or installed version; where it
  cannot be pinned to the installed release, the package's bundled docs win; the source's own
  install doc for anything you install; the vendor's docs for a tool's config. Say what you read
  when you act on it; ask when the docs do not answer — never fill the gap with a guess.
- **Do exactly what was asked.** An unrequested header, comment, sidecar file or "helpful" note
  is a defect, not a courtesy.
- **A declaration is a contract; only a run is an observation.** Types and docs say what may be
  called; they do not say what fires, when, in what order. For a behavioural question, capture a
  real run before writing code that depends on it.
- **Test the shipped artifact, never a re-implementation of it.** A test that builds its own
  fixture shape proves only that it agrees with itself.
- **Green tests are not evidence that the thing works** — only that what you asserted held. Name
  what would let the assertion pass while the feature is broken, and check that case.
- **Parallel agents and background tasks cost money and leak.** State the count and why one
  context is not enough before fanning out; bound every task and wait; before ending a turn,
  list what still runs and stop what is stale.
- **Files a tool or model consumes carry content only** — skill files, prompts, `BUGBOT.md`,
  `.coderabbit.yaml`: no metadata, provenance, dates or commentary; the consuming tool's docs
  decide where they go.
- **Never `--no-verify`; never disable a test to pass; never commit a tree that fails the
  suite.** Secrets only in the environment, never logged, never pasted into chat, commits or
  issues.
- **Executing a plan:** its global constraints bind every task; steps that need a human are
  reported by their identifier, never improvised around; do the current task's work, not a later
  gate's.

## Guide `.agents/<topic>.md`

````markdown
# [Topic]

[One line: what this guide governs. If it uses identifiers defined elsewhere — decision numbers,
runbook steps — say where they resolve.]

## [Rule as a heading, in the words the root uses]

[The full statement: what to do, the mechanism that makes it necessary, the exact files, symbols
or commands involved. One line naming the failure it prevents, where that makes the rule
checkable — no dates, no ticket numbers, no history.]

## [Next rule]

…
````

## `CLAUDE.md`

Symlink, when nothing is Claude-specific and no reader is on Windows. Replacing an existing
`CLAUDE.md` means removing it first — `ln -s` fails on a path that exists. Claude reads the
target through the link;
its Edit and Write tools refuse to write through a symlink and redirect to `AGENTS.md`, which is
the file anyone should be editing anyway:

```bash
ln -s AGENTS.md CLAUDE.md
```

Import, when Claude-specific instructions are needed — or when anyone who clones the repository
works on Windows, where a committed symlink checks out as plain text unless `core.symlinks` is
enabled. The import stays the first line so the shared file is read first. A relative import
resolves against the file that contains it, so a root `CLAUDE.md` imports `@AGENTS.md` while
`.claude/CLAUDE.md` imports `@../AGENTS.md`:

```markdown
@AGENTS.md

## Claude Code

[Claude-specific instructions only.]
```

## Nested `AGENTS.md` (subtree of a monorepo)

Carries what differs in that subtree — its own commands, its own rules — and stays shorter than
the root. How a nested file and the root combine is tool-specific, so assume neither model:
Claude Code loads every `AGENTS.md` from the working directory upward and concatenates them,
while `agents.md` and GitHub Copilot document the nearest file as taking precedence. Write the
nested file to be correct under both — it contradicts nothing in the root, since a contradiction
resolves differently per tool, and it leans on the root for nothing the subtree cannot do
without. Check the model for the tools your team uses in `references/sources.md`.

Claude Code needs one more step in a repository whose root carries a `CLAUDE.md` — which is every
repository this skill sets up. With any `CLAUDE.md` at or above the working directory, Claude Code
reads no `AGENTS.md` natively, nested ones included, so each nested `AGENTS.md` it must see needs a
sibling `CLAUDE.md` whose first line is `@AGENTS.md`. Without it the subtree's instructions reach
the other tools and not Claude.
