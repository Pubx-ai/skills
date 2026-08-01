---
name: address-pr-comments
description: >
  Load every comment on a pull request, understand and triage each one against
  the current code, then resolve them — fixing what's valid, pushing back with
  technical reasoning on what isn't. Use this skill whenever the user asks to
  "address the PR comments", "review the PR comments", "respond to review
  feedback", "handle the CodeRabbit / Bugbot / reviewer comments", "triage the
  review comments", "fix the PR feedback", or "resolve the comments" on a pull
  request. Works for human and bot reviewers alike. If a skill named
  "receiving-code-review" is available in the session, this skill applies its
  verification discipline rather than duplicating it: verify before
  implementing, no performative agreement, technical correctness over social
  comfort.
---

# Address PR Comments

Turn a pull request's open review comments into resolved threads — each one
loaded, understood, verified against the code as it exists now, and either
fixed or answered with technical reasoning. Review feedback is input to
evaluate, not instructions to obey: bots and humans are both sometimes wrong,
and blind implementation of a wrong suggestion is worse than no response.

## 0. Apply receiving-code-review if available

Check the skills available in this session for one named
**`receiving-code-review`**. If it exists, invoke it and let it govern how each
comment is processed — it is the authority on the reception discipline.

Whether or not it is available, these invariants hold:

- **Verify before implementing.** Check every claim against the current
  codebase before changing anything; the comment may be stale, mistaken, or
  missing context.
- **No performative agreement.** Never reply "You're absolutely right!" or
  thank a reviewer — state the fix, or state the disagreement, factually.
- **Understand everything before implementing anything.** If any comment is
  unclear, stop and ask before starting on the clear ones — items may be
  related, and partial understanding produces wrong implementations.
- **Push back when warranted**, with technical reasoning: when a suggestion
  breaks existing functionality, lacks context, violates YAGNI, or conflicts
  with a decision the user already made. Conflicts with the user's prior
  decisions go to the user, not the reviewer.

## 1. Locate the PR and load every comment

First resolve which PR is meant: `gh pr view --json number,url` finds the PR
for the current branch; if there is none, several, or the user named one,
confirm before proceeding. (This skill assumes GitHub and an authenticated
`gh` CLI — on another forge, translate the API calls to its equivalents.)

A GitHub PR holds feedback on three separate surfaces; loading only one is the
most common way comments get missed. Fetch all three:

```bash
gh api --paginate repos/{owner}/{repo}/pulls/{n}/comments   # inline review comments
gh api --paginate repos/{owner}/{repo}/issues/{n}/comments  # top-level PR comments
gh api --paginate repos/{owner}/{repo}/pulls/{n}/reviews    # review submissions + bodies
```

`--paginate` is not optional: without it `gh api` returns only the first 30
items, silently dropping the rest on comment-heavy PRs.

- Use `--jq` to pull out `id`, `user.login`, `path`, `line`, `in_reply_to_id`,
  and `body`, plus the fields the freshness rule below needs: `commit_id` and
  the signal's own timestamp — `created_at` on comments, `submitted_at` on
  review submissions, and the CI check's completion time from
  `gh pr checks <n>`. Write large outputs to a scratch file rather than
  flooding context.
- **A bot signal is current only if it covers this code *and* answers the
  latest request.** Check both as you load, per bot:
  - **Covers this code** — its `commit_id` or check SHA equals the PR head
    (`gh pr view --json headRefOid -q .headRefOid`; not `git rev-parse HEAD`,
    which diverges in detached or merge checkouts and when local commits
    aren't pushed). With no commit binding at all, its timestamp must be
    later than the last push.
  - **Answers the latest request** — its timestamp is later than the most
    recent trigger comment on the PR (`@coderabbitai review`, `bugbot run`),
    whoever posted it and whenever. A prior pass on the *same head* — a
    rate-limited or partial one, say — predates that trigger, so the commit
    check alone would accept exactly the state the re-review was meant to
    replace.

  A signal failing either test, or a bot with **no signal at all**, means that
  bot has no current review: report the gap and don't present its findings as
  current — absence is never approval. Its earlier findings may still be worth
  triaging, under the staleness rule below.
- Establish which comments are **actionable now**: skip resolved threads
  (the REST responses carry no resolution state — read each thread's
  `isResolved` with the GraphQL thread query in
  [`references/github-cli.md`](references/github-cli.md)), threads where
  **you have the last word** (identify "you" with
  `gh api user --jq .login`; a thread where the reviewer replied last still
  needs action, however many replies precede it), bot boilerplate
  (walkthroughs, fix-in-editor buttons, re-run triggers), and comments
  superseded by newer commits — but confirm supersession by checking the
  code, not by assuming. When unsure whether a comment is boilerplate,
  answered, or superseded, keep it in the actionable list rather than
  skipping it.
- **Unresolved is not the same as current.** A finding whose commit binding
  predates the head — an earlier round's thread that was never resolved, or
  a rejection left open — is a claim about *older* code: keep it actionable,
  but re-verify it against the head before acting, since the lines it
  describes may already have changed. Resolution state says whether anyone
  settled the thread; the commit it was written against says what it was
  looking at. Neither answers whether it still holds — only re-verification
  against the current code does.
- **Check for bot status notices while filtering** — boilerplate to skip,
  but not to ignore. CodeRabbit marks a skipped pass with
  `rate limited by coderabbit.ai` inside its auto-generated top-level
  comment: that pass produced **no successful CodeRabbit review of the
  current diff** — never treat it as a clean pass, and don't claim the PR
  was never reviewed without checking for earlier passes. Tell the user
  explicitly, along with any retry window the notice states, so they can
  decide when to trigger `@coderabbitai review`. Treat any
  bot's "skipped/errored" status the same way: absence of findings must
  never be reported as approval. Bugbot's signal is its **`Cursor Bugbot`
  CI check** (`gh pr checks <n>`): `success` means no issues *and* no
  unresolved Bugbot threads; `neutral` is ambiguous by design — findings,
  a run cancelled by a newer commit, or an internal error — so on neutral,
  confirm a review submission actually exists for the head commit before
  treating the findings list as current; there is no `skipped` conclusion.
- **Deduplicate across reviewers.** Bots frequently report the same defect;
  merge overlapping findings into one item so it is fixed once and every
  contributing thread gets answered.
- Note the commit each review targeted (bot comments usually name it): line
  numbers drift as the branch moves, so locate the code by content, not by
  the comment's line number.

## 2. Understand and triage each comment

Work through the deduplicated list one comment at a time, before writing any
fix:

1. **Restate the claim** in your own words — what defect or improvement is
   being asserted, and what would make it true or false?
2. **Verify against the current code.** Read the actual files; reproduce the
   failure scenario if one is claimed. For suggestions to add functionality,
   check whether anything actually needs it (YAGNI) before building it.
3. **Weigh the severity — it sets the depth of triage.** Treat the label as
   a claim like any other and form your own judgement of the real impact.
   Label vocabularies vary per reviewer — Bugbot uses High/Medium/Low;
   CodeRabbit's PR comments use Major/Minor/Trivial plus nitpick sections
   (its CLI agent mode uses critical/major/minor/trivial/info) — map
   whatever arrives onto the tiers below. CodeRabbit findings also carry an
   effort tag (⚡ Quick win / 🏗️ Heavy lift / 💤 Low value): use it for the
   fix-vs-defer call at the nit tier — a Quick-win nit is exactly what to
   fix, a Heavy-lift Minor is a defer candidate. A finding marked
   "Triggered by learned rule" is the bot enforcing a convention it was
   taught (often from this repo's own reply threads) — high prior that it's
   valid, but verify the rule still matches current convention rather than
   accepting it blindly.
   - **Nit / Low:** a quick validity check is enough. Fix only what is
     judged valid and cheap; anything else — invalid *or* valid but not
     worth the cost — is yours to reject or defer with a one-line reasoned
     reply, recorded in the report. Never let a nit trigger rework or scope
     growth.
   - **Medium:** the standard verification above.
   - **Major / High / Critical:** the deepest look — reproduce the failure,
     understand the root cause, and check whether the fix itself needs a
     user decision. Dismissing a Major finding wrongly is the costliest
     mistake in this workflow, so rejecting one requires strong evidence,
     not a hunch; when genuinely uncertain, escalate to the user rather
     than deciding either way.
4. **Assign a verdict:**
   - **Confirmed** — real, still present; gets a fix.
   - **Already resolved** — true when written, fixed by a later commit; gets
     a reply naming the commit, no code change.
   - **Incorrect** — wrong for this codebase; gets a reply with the technical
     reasoning, no code change.
   - **Needs a decision** — valid but touches scope, architecture, public
     APIs, or a prior decision of the user's — or is real yet arguably out of
     scope for this PR. From Medium severity up, deferring is the user's
     call and the item goes to the user before anything is implemented;
     nit/Low deferrals are the agent's call (step 3).
5. **Present the triage to the user** before implementing when the verdict
   set includes anything contested, architectural, or scope-changing — the
   user chooses direction, the reviewer doesn't. When every finding is a
   clear-cut confirmed defect and the user asked for resolution, proceed.

## 3. Resolve

Implement in this order: blocking issues (broken behaviour, security), then
simple fixes, then complex ones — verifying each fix individually rather than
batching untested changes. Where verification means running the project's
tests, the **run-tests** skill resolves and runs them correctly.

**Authorization scope:** the user asking for comments to be addressed
authorizes exactly the side effects that resolution requires — commits and
regular pushes to the *existing* PR branch, behind the gates below. Anything
beyond that scope — force-pushing, rebasing published history, opening a new
PR, or changes outside the findings being addressed — needs the user's
explicit confirmation first.

- Make the fixes on the PR branch. Before committing, run the
  **local-review** skill over the changes and address its findings; if that
  changed any code, re-run it — commit only a state that passed the gate.
- Commit using the **create-commit** skill (conventional commit). Group
  related fixes sensibly; one commit per round of review feedback is usually
  right, one commit per unrelated concern when the fixes don't belong
  together.
- Push to the PR branch so reviewers and bots re-review the actual result.

## 4. Reply and close the loop

- Reply **in the comment thread**, not as one top-level comment, and answer
  every thread you acted on or rejected: confirmed items get the fix and the
  commit hash; already-resolved items get the commit that resolved them;
  rejected items get the technical reasoning. The reasoned rejection matters
  most — it documents the decision for human readers and, for bots that
  learn from thread replies (CodeRabbit does), calibrates future reviews;
  silence does neither. Keep replies factual — no gratitude, no apology, no
  cheerleading — and make agent authorship visible (end each reply with the
  repo's agent attribution line, e.g. `🤖 Generated with Claude Code`). Only
  inline review comments support threaded replies; top-level comments and
  review bodies get a regular PR comment quoting the original. Mechanics —
  reply endpoints, body-via-file quoting, and thread resolution via GraphQL —
  are in [`references/github-cli.md`](references/github-cli.md).
- **Preview before posting.** Replies are published on the PR under the
  user's name. Show one consolidated preview — per comment: the action
  (reply / resolve / both / none) and the draft body. Pushback aimed at a
  human reviewer always waits for the user's explicit approval (a wrong
  public rebuttal costs them credibility). Routine bot-directed replies —
  fix confirmations, reasoned rejections — may post after the preview
  without per-item approval when the user asked for the comments to be
  addressed.
- **Resolve the threads that are genuinely settled** — fix pushed, or
  rejection stated with reasoning — using the GraphQL mutation (see the
  reference), so the PR's open-conversation count reflects reality.
  CodeRabbit often verifies a fix reply against the pushed commit and
  auto-resolves its own thread — re-read `isResolved` before mutating so
  already-settled threads aren't re-resolved. Resolving settled Bugbot
  threads has a concrete payoff beyond tidiness: its `Cursor Bugbot` check
  only reports `success` when no unresolved Bugbot comments remain, so
  stale-but-settled threads keep the check non-green. Leave
  open anything a human reviewer still needs to see — in particular, a
  rejected **Major** finding is never agent-resolved: that disagreement is
  exactly what a human must adjudicate, so its thread stays open until a
  person closes it.
- **Suggest a re-review; never trigger one yourself.** Whether a bot
  re-reviews pushed commits on its own is configuration, not a constant —
  check whether this PR's earlier pushes drew fresh reviews, and act on
  what you find: a bot that has been auto-re-reviewing needs no trigger
  (expect its fresh pass after the push, and wait for it); a bot that
  hasn't — or a PR with no push history yet to tell — gets a fresh pass
  only via its trigger. CodeRabbit typically re-reviews pushes
  automatically but is rate-limited, so it sometimes needs a manual nudge;
  Bugbot is commonly configured **not** to re-review automatically (cost
  control), in which case a fresh Bugbot pass always requires the trigger. The trigger comments —
  `@coderabbitai review` and `bugbot run` — request a fresh pass, and each
  costs a full bot run. Posting them is always the user's call: recommend
  one when the pushed changes warrant it (new or reworked logic, fixes to
  Major findings, changes that could plausibly have introduced new defects)
  and wait for the user's confirmation before posting.
- **Wait before re-checking when the loop continues.** A re-review takes
  minutes, so reloading immediately reads the pre-review state as final.
  After pushing (and any triggers), wait for a current signal — step 1's
  test — from each bot a pass is expected from: those triggered, plus those
  this PR's history shows auto-re-reviewing pushes, and only those. Bound
  it: if a bot's signal hasn't appeared within ~15 minutes, do one load pass
  with what's there and tell the user which bot is missing rather than
  stalling. Then repeat load → triage → resolve, bounded — after two or
  three rounds, or as soon as new findings are judgement calls rather than
  defects, stop and hand the remainder to the user instead of chasing an
  empty pass. Reviewers that generate opinions indefinitely are the user's
  to silence, not yours to satisfy.
- Report back to the user: each comment's verdict and disposition, what was
  pushed, and anything deliberately not done — a rejected suggestion or a
  deferred decision is part of the outcome, not a footnote.

## When to stop and ask

Stop and consult the user — before implementing anything — when:

- any comment is ambiguous enough that two reasonable fixes diverge,
- a suggestion conflicts with a decision the user already made, or would
  change scope, architecture, public APIs, or user-visible behaviour,
- feedback demands functionality nothing in the codebase uses,
- you cannot verify a claim with the tools available — say what's missing
  rather than guessing.

Don't implement contested feedback to avoid the discomfort of pushing back;
technical correctness outranks social comfort, and the user outranks the
reviewer.
