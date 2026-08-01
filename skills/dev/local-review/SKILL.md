---
name: local-review
description: >
  Act as a senior engineer and review all uncommitted changes in the local git
  branch — both staged and unstaged, including new untracked files — before they
  get committed. Use this skill whenever the user wants pre-commit feedback on
  work in progress — phrases like "review my changes", "review my diff", "code
  review before I commit", "look over what I changed", "is this ready to commit?",
  "check my local changes", or asking for feedback on the correctness, security,
  performance, tests, or style of uncommitted work. Pairs with the create-commit
  skill: review first, commit after. Produces feedback anchored to file paths and
  line numbers plus a 0–10 score and an APPROVE / REQUEST_CHANGES style
  recommendation.
---

# Local Review

Review **all uncommitted changes in the local git branch** — staged, unstaged, and
new untracked files — as a senior engineer would, before they become a commit. The
value of a pre-commit review is that problems are cheapest to fix *now* — while
nothing is in history yet and the author still has full context. So the goal isn't
to run a generic checklist; it's to judge these changes against how *this* codebase
actually works and catch the things that would bite later.

## 0. Run it with fresh eyes when you can

If subagents are available, prefer dispatching this review to one and acting on its
returned findings: a fresh context reads the diff cold, without the authoring
session's assumptions — and that independence is most of what a review gate buys,
since the session that wrote the code "knows what it meant", which is exactly what
a reviewer must not assume. The dispatch is read-only and single-shot — it may run
read-only inspection commands (diffs, file reads) but changes no files. Two
conditions make it worth having:

- **The subagent gets this skill, not a vague ask.** Include these instructions
  (or point at this file) and the exact diff scope in the dispatch prompt, and
  require the report to meet the output contract below — findings anchored to
  file paths and line numbers, a 0–10 score, and a recommendation. A bare
  "review my changes" dispatch produces a generic review and silently degrades
  the gate.
- **Repeated runs change the economics.** When this review gates every commit in
  a longer workflow, the dispatch cost repeats each time — honour the user's
  speed-vs-rigour preference there, keeping the small commits same-session.

Stay same-session when subagents aren't available or the change is trivial (a
few lines), where dispatch overhead outweighs the fresh eyes.

## 1. Gather all local changes

Work from the real changes, not an assumption about what changed. You want the full
picture of uncommitted work, regardless of whether it's been `git add`-ed yet.

- **See everything at a glance first:** `git --no-pager status --short` lists staged,
  unstaged, and untracked files together so you know the full scope.
- **Tracked changes (staged + unstaged):** `git --no-pager diff HEAD` shows every
  modification to already-tracked files relative to the last commit. (If you need to
  distinguish them, `git --no-pager diff --staged` is the staged set and
  `git --no-pager diff` is the unstaged set.)
- **New untracked files:** these don't appear in any diff — identify them from
  `git status` and read them in full with the file tools, since the whole file is new.
- **In Cursor**, the `@diff` context is a convenience view, but confirm it covers the
  changes you intend to review (it may only show the staged set); prefer the git
  commands above when in doubt.
- **Unset the pager first.** Git's pager can hang a non-interactive shell and, worse,
  make git interpret pager tokens as filenames. Either run `unset PAGER` once or use
  `git --no-pager …` on each call.
- **If there are no changes at all, stop.** Report that the working tree is clean and
  ask what to review — don't fall back to reviewing already-committed history, since
  the user asked about what they're *about to commit*.

## 2. Understand the change in context

A diff on its own is easy to misjudge. Before forming opinions, read enough of the
surrounding code to know what "good" looks like here:

- `AGENTS.md`, `README.md`, and anything under `/docs` for project rules and intent.
- The files being changed in full (not just the diff hunks) and their close neighbours,
  to see the patterns, naming, and error-handling style already in use.
- Library behaviour when a change hinges on an external API — pull current docs via
  the **context7 MCP** rather than guessing at signatures or defaults.

## 3. What to look for

Evaluate each changed file across these lenses, roughly in priority order — a
correctness or security defect matters far more than a style nit:

- **Correctness & edge cases** — does it do what it intends, including empty/null,
  boundary, and error paths?
- **Security** — untrusted input, injection, secrets, authz gaps, unsafe defaults.
- **Error handling** — failures surfaced and handled, not swallowed or left to crash.
- **Performance** — needless work, N+1s, or hot-path allocations that will matter at scale.
- **Tests** — is the new behaviour covered, and does it follow the repo's testing conventions?
- **Consistency** — does it match the architecture, patterns, and style already present?
- **Readability & maintainability** — will the next person understand it without archaeology?

## 4. Give actionable feedback

For every issue, make it easy to act on:

- Anchor it to the **file path and line number(s)** from the diff.
- Explain **why** it's a problem and what the impact is — not just that it's "wrong".
- Give a **concrete fix or example**, not a vague direction.
- Point to an **existing pattern in the codebase** the change should follow, when one exists.

Separate **blocking issues** (must fix before commit) from **nits** (optional polish) so
the user knows what actually gates the commit. If the change is clean, say so plainly
rather than inventing problems.

## 5. Score and recommendation

Close with a single score out of 10 and the matching recommendation:

| Score | Recommendation |
|---|---|
| 9–10 | **APPROVE** |
| 7–8 | **APPROVE WITH MINOR SUGGESTIONS** |
| 5–6 | **REQUEST_CHANGES** |
| 3–4 | **MAJOR_CHANGES_NEEDED** |
| 1–2 | **REJECT** |

Then state clearly whether these changes should be committed, tying the verdict to the
specific findings above (correctness, security, tests, and alignment with project
standards) rather than a general impression. When the verdict is APPROVE, it's natural to
stage anything still unstaged and hand off to the **create-commit** skill next.
