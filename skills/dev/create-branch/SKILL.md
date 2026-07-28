---
name: create-branch
description: >
  Create a correctly named git feature branch off an up-to-date base, carrying
  the JIRA ticket ID when one is in context. Use this skill whenever the user
  wants to "create a branch", "make a new branch", "branch off main", "start
  work on PUB-1234", "checkout a feature branch", or when work is about to
  begin (or a commit is about to land) while still on main/master. This is the
  first step of the delivery flow — branch, then commit with create-commit,
  then raise the PR with raise-pr.
---

# Create Branch

Start every piece of work on its own correctly named branch, cut from an
up-to-date base. The branch name isn't cosmetic: the create-commit skill pulls
the JIRA ticket out of it for commit footers, PRs inherit it, and a consistent
`<type>/<TICKET>-<slug>` shape makes branches self-describing in a busy repo.

## 1. Find the JIRA ticket

The branch should carry the ticket ID (`PUB-4204` style — any `PROJ-123`
pattern) whenever the work has one. Look for it in this order:

1. The user's request or earlier conversation.
2. Documents driving the work: a requirements doc under `docs/requirements/`,
   a plan under `docs/plans/`, a pasted ticket or spec.
3. If none is found, ask the user for one — a one-line question is cheaper
   than renaming a branch later. Branching without a ticket is fine when the
   user confirms there isn't one; never invent an ID.

## 2. Name the branch

```text
<type>/<TICKET-ID>-<short-slug>     # feat/PUB-4204-site-creation
<type>/<short-slug>                 # fix/dropdown-focus-trap  (no ticket)
```

- `<type>` uses the same taxonomy as create-commit (`feat`, `fix`, `chore`,
  `docs`, `refactor`, …) and describes the work about to happen.
- `<short-slug>` is kebab-case, 2–5 words, describing the change — not the
  ticket title verbatim.
- All lowercase — except the ticket ID, which keeps its canonical uppercase
  form (`PUB-4204`, never `pub-4204`; create-commit's footer extraction and
  JIRA both expect it). No spaces, underscores, or trailing dashes.

## 3. Cut it from an up-to-date base

1. Identify the base branch — the repo's default (`gh repo view --json
   defaultBranchRef -q .defaultBranchRef.name`), unless the repo's convention
   is to branch from `develop`; where recent PRs merge tells you
   (`gh pr list --limit 20 --json baseRefName`).
2. Check the name is free **before creating anything**:
   `git branch --list <name>` and `git ls-remote --heads origin <name>`. If
   it already exists, ask whether to switch to it instead — never reuse a
   name for different work.
3. Check the working tree (`git status`). Uncommitted changes that belong to
   the new work simply ride along to the new branch. Changes that belong to
   *other* work should be surfaced to the user before switching — don't let
   them silently migrate.
4. Create from the fetched remote base, not the local copy:
   `git fetch origin <base> && git checkout -b <name> origin/<base>`. A
   `git pull` on the local base would merge any stray local commits sitting
   there, and the new branch — and eventually its PR — would inherit them;
   branching from `origin/<base>` sidesteps that entirely. If currently on
   another feature branch, confirm with the user whether to stack on it
   instead of branching from the base.

Report the created branch and its base. The natural next steps are the work
itself, then **create-commit** for each reviewed change, and **raise-pr** when
the branch is ready.
