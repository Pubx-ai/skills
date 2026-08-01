---
name: local-pr-review
description: >
  Act as a senior engineer and review the committed changes on the current git
  branch against the base branch (develop or main) — a local, pre-push PR review.
  Use this skill whenever the user wants feedback on a branch as a whole before
  opening or merging a pull request — phrases like "review my branch", "PR review
  before I push", "review my changes against develop/main", "is this branch ready
  to merge?", "review the whole feature branch", or asking about the correctness,
  security, performance, tests, or style of the commits that diverge from the base
  branch. Unlike local-review (which looks at uncommitted work), this reviews the
  branch's committed diff. Produces feedback anchored to file paths and line
  numbers plus a 0–10 score and an APPROVE / REQUEST_CHANGES style recommendation.
---

# Local PR Review

Review the **committed changes on the current branch against the base branch**, as a
senior engineer would in a pull request — but locally, before the PR is opened or
merged. The value of doing this now is that it's the last cheap moment to catch
problems: the work is finished enough to judge as a whole, but you can still amend
history and fix issues without a round-trip through review. So the goal isn't a
generic checklist; it's to judge the branch against how *this* codebase actually
works and catch what would bite a reviewer — or production — later.

## 0. Dispatch to a subagent by default

Whenever subagents are available, run this review in one and act on its returned
findings. This is the last gate before the work goes in front of other people, it
fires once per branch rather than in a loop, and both of its benefits land here:

- **Independence.** A fresh context reads the branch cold, without the authoring
  session's assumptions — and that is most of what a review gate buys, since the
  session that wrote the code "knows what it meant", which is exactly what a
  reviewer must not assume.
- **Context economy.** A whole-branch review reads many files; the subagent burns
  its own context and returns only the findings, keeping the main session lean.

The dispatch is read-only and single-shot — it may run read-only inspection
commands (diffs, file reads) but changes no files. **The subagent gets this
skill, not a vague ask**: include these instructions (or point at this file), the
resolved base, and the exact diff scope in the dispatch prompt, and require the
report to meet the output contract below — findings anchored to file paths and
line numbers, a 0–10 score, and a recommendation. A bare "review my branch"
dispatch produces a generic review and silently degrades the gate.

Stay same-session when subagents aren't available or the branch diff is trivial.
When findings trigger fixes and this review re-runs until the final diff passes,
the repeat runs may be same-session after a dispatched first pass — honour the
user's speed-vs-rigour preference there.

**Blocked by policy is not the same as unavailable.** Some sessions permit
subagents but instruct that they only be used when the user asks. That is a
decision to surface, not a reason to quietly downgrade the gate: say the review
would be stronger run with fresh eyes, ask whether to dispatch one, and wait for
the answer. If they agree, dispatch exactly as this section describes; if they
decline, review same-session — a weakened gate the user chose is fine; one they
never heard about is not.

## 1. Determine the base branch

The base is the branch this work will merge back into. When the caller passes one
explicitly (the **raise-pr** skill does), use it verbatim. Otherwise resolve it the same
way the sibling skills do — from the remote's truth, never from local branch names:

- The repo's default branch is authoritative:
  `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`. Where recent PRs
  merge tells you when the convention differs (`gh pr list --limit 20 --json baseRefName`
  — e.g. a `develop` flow). A local `develop` branch merely *existing* is not evidence of
  a develop convention.
- **Refresh before comparing**: `git fetch origin <base>` — the local tracking ref is
  only as fresh as the last fetch, and a stale base reviews a different diff than the PR
  will present. Compare against `origin/<base>`.
- If it's still ambiguous, ask the user which branch to review against rather than
  assuming.

## 2. Gather the branch diff

Review only what *this branch* introduced, not unrelated commits that landed on the
base since you branched off.

- **Use the merge-base (three-dot) diff:** `git --no-pager diff origin/<base>...HEAD` shows
  the changes the branch adds relative to where it diverged from the base — this is exactly
  what a PR shows. Always diff against the freshly fetched `origin/<base>` from step 1, never
  the bare local name. (Two-dot `origin/<base>..HEAD` can include base-side changes and
  mislead you.)
- **Overview first:** `git --no-pager diff origin/<base>...HEAD --stat` for the shape of the
  change, then the full diff for detail.
- **See the commits too:** `git --no-pager log --oneline origin/<base>..HEAD` reveals how the
  work is structured and whether the commit history itself is sensible.
- **In Cursor**, the `@diff <base>...` context is a convenience view — use it if present,
  but prefer the git commands above when the base branch is in doubt.
- **Unset the pager first.** Git's pager can hang a non-interactive shell and, worse,
  make git interpret pager tokens as filenames. Either run `unset PAGER` once or use
  `git --no-pager …` on each call.
- **If the branch is even with the base (no diff), stop.** Report that there's nothing to
  review and confirm the branch and base with the user.

## 3. Understand the change in context

A diff on its own is easy to misjudge. Before forming opinions, read enough of the
surrounding code to know what "good" looks like here:

- `AGENTS.md`, `README.md`, and anything under `/docs` for project rules and intent.
- The changed files in full (not just the diff hunks) and their close neighbours, to see
  the patterns, naming, and error-handling style already in use.
- Library behaviour when a change hinges on an external API — pull current docs via the
  **context7 MCP** rather than guessing at signatures or defaults.

## 4. What to look for

Evaluate the branch across these lenses, roughly in priority order — a correctness or
security defect matters far more than a style nit:

- **Correctness & edge cases** — does it do what it intends, including empty/null,
  boundary, and error paths?
- **Security** — untrusted input, injection, secrets, authz gaps, unsafe defaults.
- **Error handling** — failures surfaced and handled, not swallowed or left to crash.
- **Performance** — needless work, N+1s, or hot-path allocations that will matter at scale.
- **Tests** — is the new behaviour covered, and does it follow the repo's testing conventions?
- **Consistency** — does it match the architecture, patterns, and style already present?
- **Readability & maintainability** — will the next person understand it without archaeology?

Because this is a whole-branch review, also step back and judge it at the PR level: does
the change hang together as one coherent unit of work, is it appropriately scoped (not two
unrelated features in one branch), and is the commit history clean enough to merge?

## 5. Give actionable feedback

For every issue, make it easy to act on:

- Anchor it to the **file path and line number(s)** from the diff.
- Explain **why** it's a problem and what the impact is — not just that it's "wrong".
- Give a **concrete fix or example**, not a vague direction.
- Point to an **existing pattern in the codebase** the change should follow, when one exists.

Separate **blocking issues** (must fix before merge) from **nits** (optional polish) so the
user knows what actually gates the PR. If the branch is clean, say so plainly rather than
inventing problems.

## 6. Score and recommendation

Close with a single score out of 10 and the matching recommendation:

| Score | Recommendation |
|---|---|
| 9–10 | **APPROVE** |
| 7–8 | **APPROVE WITH MINOR SUGGESTIONS** |
| 5–6 | **REQUEST_CHANGES** |
| 3–4 | **MAJOR_CHANGES_NEEDED** |
| 1–2 | **REJECT** |

Then state clearly whether this branch should be merged into the base branch, tying the
verdict to the specific findings above (correctness, security, tests, and alignment with
project standards) rather than a general impression.

On an APPROVE-level verdict, the natural next step is the **raise-pr** skill to push the
branch and open the pull request; once reviews land there, **address-pr-comments** owns
the triage loop.
