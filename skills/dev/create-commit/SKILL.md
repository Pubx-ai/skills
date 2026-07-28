---
name: create-commit
description: >
  Compose and create a git commit whose message follows the Angular Conventional
  Commits standard, so semantic-release can version and changelog it automatically.
  Use this skill whenever the user wants to commit staged changes, "make a commit",
  "commit this", "write a commit message", "commit with conventional/angular format",
  or asks what type/scope a change should be. Also use it when a ticket ID (e.g.
  PUB-4204) should be pulled from the branch name into the commit footer. The skill
  reviews the staged diff first and only commits after the change has been reviewed.
---

# Create Commit

Turn a set of staged changes into a single, well-formed Conventional Commit. The
message format isn't cosmetic: [semantic-release](https://github.com/semantic-release/semantic-release)
parses the commit `type` and `BREAKING CHANGE` marker to decide the next version
number and to build the changelog. A wrong type means a wrong release, so the type
must honestly describe the change.

## Workflow

1. **Check the branch first.** Run `git rev-parse --abbrev-ref HEAD` and resolve
   what's protected: the repo's default branch
   (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name`), plus
   `main`, `master`, `develop`, and `release/*` branches. Committing straight to
   any of them is off-limits — create or switch to a feature branch first, using
   the **create-branch** skill when it's available.
2. **See what's staged.** Run `git diff --staged --stat` (then `git diff --staged`
   for detail). If nothing is staged, stop and ask the user what to stage rather
   than guessing — never `git add -A` on their behalf. When staging on the user's
   behalf, stage explicit paths and watch for unrelated untracked files sitting
   in the worktree: they belong to other work and must not ride along in this
   commit.
3. **Pick the type from the diff, not the intent.** A change that adds a feature
   is `feat`; a change that only fixes behavior is `fix`; a docs-only change is
   `docs`, etc. When a commit genuinely does two things, that's usually a sign it
   should be two commits — mention that to the user.
4. **Add a scope if it clarifies.** Scope is the area of the codebase touched
   (`api`, `auth`, `deps`, a module name). Omit it when it wouldn't add signal.
5. **Extract the ticket ID from the branch.** Pull an ID like `PUB-4204` out of a
   branch name such as `feat/PUB-4204-site-creation`.
   If one exists, reference it in the footer (`Closes PUB-4204`). If the branch has
   none, skip the footer — don't invent one.
6. **Compose the message** (see format below).
7. **Commit after review.** Since the diff has been reviewed in step 2 (and, when
   the **local-review** skill is available, given a proper review pass first),
   create the commit with `git commit`. Never bypass hooks with `--no-verify` —
   a failing hook is feedback, not an obstacle. Report the resulting message back
   to the user.

## After the commit

More work on the same feature loops back here, one reviewed commit at a time.
When the branch is complete, the **raise-pr** skill pushes it and opens the pull
request; **local-pr-review** before raising catches what per-commit review
missed.

## Message format

```
<type>(<optional scope>): <subject>

<optional body>

<optional footer>
```

Build it with one `-m` per block:

```bash
git commit -m "<type>(<scope>): <subject>" [-m "<body>"] [-m "<footer>"]
```

Subject line rules and the reasoning behind them:

- **Imperative mood** ("add", not "added"/"adds") — it reads as "this commit will
  <subject>", matching how git itself phrases things.
- **Lowercase** type and subject (proper nouns/acronyms excepted), **no trailing
  period** — this is what the Angular preset's parser and changelog generator expect.
- **≤ 72 characters**, ideally ~50. Longer detail belongs in the body.
- Put the *why* and any context in the body; keep the subject to the *what*.

## Types and their release impact

Only `feat` and `fix` (and breaking changes) produce a release. The rest still
appear in the changelog but don't bump the version.

| Type | Meaning | Release |
|---|---|---|
| `feat` | A new feature | minor (`0.x.0`) |
| `fix` | A bug fix | patch (`0.0.x`) |
| `docs` | Documentation only | none |
| `style` | Formatting, no logic change | none |
| `refactor` | Neither fixes a bug nor adds a feature | none |
| `perf` | Performance improvement | none |
| `test` | Add or correct tests | none |
| `build` | Build system or dependencies | none |
| `ci` | CI config and scripts | none |
| `chore` | Anything not touching src/test | none |
| `revert` | Reverts a previous commit | none |

## Breaking changes

A breaking change forces a **major** release. Signal it either way:

- Add `!` after the type/scope: `feat(api)!: switch response to array shape`, or
- Add a `BREAKING CHANGE:` paragraph in the footer describing the break and the
  migration.

Prefer the footer when consumers need migration instructions.

## Examples

Simple feature:

```bash
git commit -m "feat: add user authentication module"
```

Fix with scope:

```bash
git commit -m "fix(api): resolve null pointer in user endpoint"
```

Body explaining the why, plus a ticket footer:

```bash
git commit -m "refactor(fetchers): restructure with shared base class" \
  -m "Move report_date handling into GenericFetcher and add GenericReportFetcher as an intermediate abstract class to cut duplication." \
  -m "Closes PUB-4204"
```

Breaking change via footer:

```bash
git commit -m "feat(api): change response format to array-based structure" \
  -m "BREAKING CHANGE: responses now return an array instead of an object; update all API consumers accordingly."
```

Revert:

```bash
git commit -m "revert: feat(api): change response format" \
  -m "This reverts commit abc123def456."
```
