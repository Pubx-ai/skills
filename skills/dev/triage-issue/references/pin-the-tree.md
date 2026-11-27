# Pin the tree

Every `path:line` in a triage note refers to one commit of the issue's own repository. This
file is the procedure that produces that commit and the read-only tree it is read from. A
triage that reads a working copy another process may move, or a clone of some other
repository, produces confidently wrong citations.

## Which repository

The tree to pin is the repository the issue belongs to — `<owner>/<repo>` from the reference,
never whatever the current directory happens to be (a bare issue number was already resolved
to `<owner>/<repo>` at the skill's Inputs step, which is where a missing checkout is handled).

Compare the checkout with the issue's repository by name, case-insensitively, and never by
parsing the remote URL, whose forms differ:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner   # run inside the checkout
```

When the names differ, or there is no checkout, work in a clone of the issue's repository
at the scratch location. If that directory already exists and names the same repository
(`gh repo view --json nameWithOwner` inside it), reuse it and fetch; if it exists and names
another, stop and report the collision; otherwise clone:

```bash
gh repo clone <owner>/<repo> <scratch>/triage-<owner>-<repo> -- --filter=blob:none
```

`<scratch>` is the session's scratch directory when the environment names one, otherwise
the system temporary directory. A clone made this way is removed when the session's last
triage of that repository ends, or reported to the user with its path — the same rule as
the worktree below. Never point `git worktree add` at the clone itself.

## Which commit

Resolve the default branch, and treat the answer as data: git accepts `;`, `$`, backticks,
`&`, `|` and parentheses in a ref name, so the value is held in a variable and always
quoted, never pasted into a command line.

```bash
branch="$(gh repo view <owner>/<repo> --json defaultBranchRef -q .defaultBranchRef.name)"
```

If that lookup is refused, ask the user which branch to pin, or non-interactive stop and
report it. Then fetch the branch and take the sha from what the fetch brought:

```bash
git fetch origin "refs/heads/$branch"
sha="$(git rev-parse FETCH_HEAD)"
```

`FETCH_HEAD`, not `origin/<branch>`: a checkout with a narrower fetch refspec, such as a
single-branch clone, never updates the tracking ref. Check the sha is forty hex characters
before it reaches any further command.

## The worktree

```bash
git worktree add --detach "<scratch>/triage-<repo>-${sha:0:7}" "$sha"   # from the checkout or clone
```

Verify `git rev-parse HEAD` in the worktree equals `$sha` before the first read, and do
every read of the repository there. If a worktree for this same sha already exists, verify
its HEAD the same way and reuse it — consecutive triages in one session share the pin.
Remove the worktree (`git worktree remove <dir>`) when the note is delivered or the triage
stops for any reason, unless another triage in the session still needs it; otherwise tell
the user it exists and where.

## What the worktree does not contain

A blob-less worktree holds source, not dependencies: there is no `node_modules` or
equivalent in it. A package's bundled documentation is read from an existing install whose
lockfile matches the pinned tree's lockfile (compare the two files); when no such install
exists, the bundled docs are unavailable and the source order moves on to the tool's own
documentation. Never run an install, a build or any of the repository's scripts inside the
worktree or the clone: a triage reads the target, it does not execute it.

History commands on a blob-less clone (`git log --follow`, `git log -S`) fetch the blobs
they need on demand and can be slow on broad paths; scope them to the specific files the
check needs.
