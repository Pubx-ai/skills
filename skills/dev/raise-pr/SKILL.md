---
name: raise-pr
description: >
  Push the current feature branch and raise a GitHub pull request with a
  conventional-commit style title and a structured body, after verifying the
  branch actually has committed work to raise. Use this skill whenever the
  user asks to "raise a PR", "open a pull request", "create a PR", "push and
  PR", "get this reviewed", or wants the current branch turned into a pull
  request. This is the last step of the delivery flow — after create-branch
  and one or more create-commit commits — and hands off to address-pr-comments
  once reviews arrive.
---

# Raise PR

Turn a finished feature branch into a pull request reviewers can act on. The
PR is the branch's public face: the title feeds changelogs and merge commits,
the body is what a reviewer (human or bot) reads before the diff, and a PR
raised from the wrong branch state wastes everyone's pass.

**User-initiated only.** Run this skill when the user explicitly asked for a
PR or confirmed a suggestion to raise one. Other skills point here as the
natural next step — that's a suggestion for the *user* to answer, never a
license to chain into raising autonomously. Publishing a branch is the
user's decision, not a workflow side effect.

## 1. Verify there is something to raise

Run the checks; each failure has a specific remedy, not a workaround:

- **On a feature branch, not the base.** `git rev-parse --abbrev-ref HEAD`
  must not equal the base resolved in the next check — nor `main`,
  `master`, `develop`, or a `release/*` branch. If it does, the branch step
  was skipped; use **create-branch** first and move the work over.
- **Commits ahead of the base.** Determine the base
  (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name`, or
  `develop` where that's the repo's convention — check where recent PRs
  merge with `gh pr list --limit 20 --json baseRefName`), refresh it with
  `git fetch origin <base>` (the local tracking ref is only as fresh as the
  last fetch), then check `git log --oneline origin/<base>..HEAD`. No
  commits → nothing to raise; uncommitted work goes through
  **create-commit** first.
- **Clean working tree.** Uncommitted or untracked changes at PR time are
  either forgotten work (commit them) or unrelated clutter (leave behind,
  but tell the user they exist). Never let them decide silently.
- **An existing PR for this branch?** `gh pr view` — if one exists, this is a
  push-and-update, not a new PR.

## 2. Review before raising

Run the **local-pr-review** skill over the branch's full diff and address its
findings before pushing — the PR gate. Tell it explicitly to review against
the `<base>` resolved in step 1 rather than letting it derive its own: the
review must cover the same diff the PR will present, or the gate is checking
a different door. If addressing findings
adds commits, re-run it until the final diff passes. Skip only if the user
explicitly wants a draft PR for early feedback; mark it as a draft
(`--draft`) in that case.

## 3. Push and raise

1. Push with tracking: `git push -u origin <branch>`.
2. **Title** — conventional-commit style, matching the branch's dominant
   change: `feat(dev): add execute-plan skill`. A single-commit branch reuses
   that commit's subject; a multi-commit branch gets a subject describing the
   aggregate, not a list.
3. **Body** — structured and skimmable, written into `gh pr create` via a
   heredoc (inline `--body` strings mangle quoting):

   ```bash
   gh pr create --base <base> --title "<type>(<scope>): <subject>" --body "$(cat <<'EOF'
   ## Summary
   - What changed and why, a bullet per meaningful change — written from the
     diff, not from memory.

   ## Notes
   - Anything a reviewer needs that the diff doesn't say: decisions taken,
     alternatives rejected, follow-ups deliberately deferred.

   Closes <TICKET-ID>   # only when the branch carries one — omit otherwise

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

   Reference the ticket (`Closes <TICKET-ID>`, per house style) only when the
   branch name carries one — for JIRA IDs the keyword is a reading
   convention, not GitHub auto-close. Keep the agent attribution footer —
   agent-raised PRs stay identifiable.
4. Report the PR URL back to the user.

## 4. Hand off

Review bots (CodeRabbit, Bugbot) post their findings on the new PR within
minutes. When they do — or when human reviews land — the
**address-pr-comments** skill owns the load → triage → resolve loop.
