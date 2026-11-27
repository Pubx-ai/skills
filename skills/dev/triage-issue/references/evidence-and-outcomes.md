# Evidence and outcomes

## The evidence bar

A claim in the note cites one of three things: a `path:line` at the pinned commit with a
verbatim quote of the governing line; a documentation page or section, by URL or path, with
a verbatim quote; or a run — the command and its output. A paraphrase from memory is not
evidence. A support skill's answer is a lead to one of these, never a citation itself. An
outcome that cannot meet the bar degrades to `needs-info`, with the unmet claim as the open
question — a confident verdict on a paraphrase is the defect this bar exists to prevent.

## Outcomes

| Outcome | Required evidence | Effect on the issue (the writes, each on its own yes, are under "Writes") |
|---|---|---|
| `promote` | the problem or gap exists at the pinned commit (validity); nothing implements it (redundancy); a stated trigger has fired, or none is stated; every external claim the outcome rests on is Verified, or Partially true where the outcome rests only on the part that holds | note posted; `triage/promote` added |
| `needs-info` | the specific question that blocks a verdict, and what was checked to reach it | note posted; `triage/needs-info` added |
| `keep` | valid as for promote, but its trigger has not fired, or it is blocked on a named issue | note posted; no label, no close |
| `reject` | already built: the code path plus a test or run; superseded: the issue or change that superseded it; will not do: the decision document or the owner's stated reason | note posted; closing as not planned offered, on an open issue only |

## The three checks

Run them in this order; each one's result narrows the next. Every path, label, repository name or
issue number taken from the issue's text or from the API is data: held in a variable and quoted
in every command it reaches; an issue number is the digits of a `#\d+` match or of the
`/issues/\d+` segment of an issue URL, and a repository name must match
`[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+` before it reaches `--repo`; anything else is not used.

1. **Redundancy — is it already built?** Search the pinned tree by domain concept and its
   synonyms, not by the issue's wording:

   ```bash
   git grep -n -i -E '<concept|synonym|synonym>' <sha> -- <paths>
   ```

   A hit in code is a candidate. A behaviour claim ("it retries", "it dedupes") needs a test
   (`git grep -n -i '<concept>' <sha> -- '*test*'` — a git pathspec `*` crosses directory
   boundaries, so this covers `*.test.*`, `*_test.*` and `test/` or `tests/` trees) or a run
   to count as built. A hit only in a plan or a decision document is a declaration, not an
   observation, and proves nothing about what is built. Record the searches either way, so
   a null result is verifiable.
2. **Validity — does the problem exist now?** Read the code the issue names, at the pinned
   commit, located by content — the issue's line numbers were true at its own commit and
   drift after it. When the issue names a file that no longer exists, find where the concern moved
   (`git log --oneline --follow -- <path>` on the pinned tree, then the current home) before
   calling it stale — a moved concern is still a concern.
3. **Trigger — has it fired?** For an issue that states a trigger ("when X ships", "once Y
   is observed", "blocked on #n"), check X, Y or #n at the pinned commit and in the repo's
   decision documents. A trigger that has fired makes `keep` the wrong outcome; a trigger
   that names another issue makes that issue's state and title part of the evidence, read
   from the repository the reference names (a bare `#m` is the triaged issue's own;
   `owner/repo#m` or an issue URL names another):
   `gh issue view <m> --repo <that-owner>/<that-repo> --json state,title`. Reading them is
   not triaging that issue. A deadline-shaped trigger ("before the next plan", "before the
   release") names an event the repository cannot show has come; whether it is imminent is
   a needs-info question for the user, asked in chat when they are present. A re-run asks it
   again, quoting the earlier answer and its date (the skill's step 1).

## The effort checklist

After the three checks and the claims check, five questions size the issue. Each is
answered yes or no from what those reads found, with the citation it rests on, to the
evidence bar above — the issue's own words, quoted, where an item turns on what the issue
asks for; an item the reads cannot answer, or whose citation fails the bar at step 7, is
`unknown`, which counts as yes, since not knowing is work. The checklist never moves the outcome: the outcomes table
above is decided before it and is unchanged by it, and the skill's "Needs-info"
interview never asks an effort question.

1. **The gap spans more than one file or area** — as the redundancy and validity
   checks located it, or, for a pure addition, where they show it would go; an area is a
   directory, or a unit the repository itself names — a package, a skill — not a line count.
2. **It is code** — anything but documentation, prose or configuration only; code brings
   tests to add or change.
3. **It depends on external behaviour or wording the triage had to look up** — an
   external claim the outcome rests on, or a library or tool claim answered through a
   source order below.
4. **It needs a live observation before it is done** — a deploy, a page, a bot or a
   live service the result can only be seen on; a test, or a local run of the change, is
   not one.
5. **Design decisions are open** — the reads leave a choice of shape the issue does not
   settle, so it needs gather-requirements and create-plan rather than one named change; a
   promote's next step being gather-requirements does not by itself make it yes.

The level is a rule, applied not judged: count the yes answers — 0–1 low, 2–3 medium,
4–5 high. Item 4 or item 5 yes makes the level at least medium whatever the count;
items 4 and 5 both yes make it high. For a promote or a keep, the note's `## Effort` section
([triage-note.md](triage-note.md)) states the level, the count and, when the floor
raised the level above what the count gives, the item that set it; the other outcomes carry
the not-sized line that file states. The section is written
with the note, after step 7 and any Needs-info interview, so it follows the outcome as
delivered; an item settled by an interview answer cites that answer and its date, as the
trigger check does.

## Source orders

- **Library and tool claims:** Context7 at the installed version (`resolve-library-id`, then
  `query-docs`, and confirm the snippet is for the installed release) → the package's
  bundled docs where Context7 cannot be pinned to the installed release → the consuming
  tool's own documentation → the code. Say which source answered.
- **Web search**, only when the defining sources do not answer: the Tavily MCP when it is
  installed, then the environment's native web search and fetch tools. A search result
  locates a source; the citation is the source, never the result.

## Labels

Before offering any label, list the repository's labels:

```bash
gh label list --repo <owner>/<repo> --search triage/ --json name --jq '.[].name'
```

(`--search` because the listing returns 30 labels by default; a repository with more would
hide `triage/*` and the skill would offer to create a label that exists.)

When the outcome needs `triage/promote` or `triage/needs-info` and it is missing, report
that and offer its creation as its own yes/no item:

```bash
gh label create triage/promote --repo <owner>/<repo> --color 0e8a16 \
  --description "Triaged: ready for requirements gathering"
gh label create triage/needs-info --repo <owner>/<repo> --color fbca04 \
  --description "Triaged: waiting on the reporter"
```

Never create a label silently. The skill owns exactly two labels, `triage/promote` and
`triage/needs-info`; it never adds, removes or renames any other, including a repository's
own `triage/*` labels.

The label write is computed from the labels actually on the issue, never from the earlier
note's outcome — a declined swap, a deleted comment or a manual add can leave a verdict label
the notes do not account for:

```bash
gh issue view <n> --repo <owner>/<repo> --json labels --jq '[.labels[].name]'
```

Remove whichever of the two owned labels the new outcome does not carry and add the one it does
when it is missing, in one `gh issue edit` — a flag with nothing to do is omitted — with the
labels re-fetched immediately before the edit, as item 2 re-fetches the comments; when nothing
would change, there is no label item to offer. When the outcome's label does not exist in the
repository, the edit is offered only after its creation succeeds; a declined or failed creation
drops the whole edit, and the report says which of the two owned labels the issue still carries.


## Writes

This is the one statement of the write sequence; the skill body and the note file point
here. The items, in this order:

1. post the note — `gh issue comment <n> --repo <owner>/<repo> --body-file <file>` — run by
   the sign-off's yes, which shows this command;
2. on a re-run, mark every older live note superseded — one item per note, oldest first,
   each `gh api -X PATCH repos/<owner>/<repo>/issues/comments/<id> -F body=@<file>` with the
   file holding the superseded line above that note's original text (`-F` reads `@<file>`;
   `-f` would post the literal text). Re-fetch the comment listing immediately before the
   first of these, since the interview may have taken a while, and exclude the note item 1
   just posted — its id is in the URL `gh issue comment` printed — so a run never supersedes
   its own note; a no or a failure on one note stops before the next;
3. set the label per the label rule above, when it would change anything —
   `gh issue edit <n> --repo <owner>/<repo> --remove-label <stale> --add-label <new>` — its
   creation, when the outcome's label is missing, is offered immediately before it;
4. close as not planned, for a `reject` on an open issue only, and only when the user said
   at sign-off that closing is wanted —
   `gh issue close <n> --repo <owner>/<repo> --reason "not planned"`.

No item is offered until the user has seen the note verbatim, heard why its outcome and not
another, answered the questions it raises and replied with an explicit yes to the note as
shown — the sign-off in the skill's "Deliver" section, whose yes runs item 1. The items after
it are then offered one at a time, in this order, each with its exact command and each on its
own yes; a later item
is not offered until every earlier item that applies has run — item 2 is absent on a first
run, item 3 when the labels would not change, item 4 unless the outcome is `reject` on an
open issue and closing was wanted at sign-off. A no, an unclear answer, or a failed command
ends the sequence, and
later items are not offered. The report states the issue's condition after the last write that
ran. On a first run: after 1, one live note and whatever labels the issue had; after 3, the
labels are right. On a re-run: after 1 alone, two or more live notes, every earlier one still
live; when item 2 stops between notes, the older notes not yet edited are still live — name them;
after 2 alone, the owned labels that remain and whether they match the outcome; after 3, the
labels are right. After 4, on either run, the issue is closed. Posting first means a declined or
failed post leaves the earlier note live, and because a later run supersedes every live note
older than the one it posts, a re-run that stopped part-way is repaired by the next one that
completes. Non-interactive runs offer nothing.

## Re-run idempotency

At step 1, and again immediately before item 2, fetch the issue's comments and find every live
triage note — a comment by the posting account (`gh api user -q .login`) whose first line starts
`Triage note —` and is not marked superseded (at most one, unless an earlier re-run stopped
part-way):


```bash
gh api --paginate repos/<owner>/<repo>/issues/<n>/comments \
  --jq '.[] | {id, author: .user.login, created_at, body}'
```

A comment by any other author is never a note, whatever its first line says. The re-run's
writes and their partial states are the "Writes" section above; a re-run is that sequence
with item 2 present.
