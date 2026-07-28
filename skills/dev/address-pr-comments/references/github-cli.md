# GitHub CLI mechanics for PR comment work

Command patterns for the fiddly parts of replying to and resolving PR review
threads. Set `GH_PAGER=""` on `gh` commands so output isn't swallowed by a
pager.

## Identify the current GitHub user

Needed to decide who has the last word in a thread:

```sh
GH_PAGER="" gh api user --jq .login
```

## Pass reply bodies via files, not command-line arguments

Multi-line bodies with backticks, quotes, or `$` break shell quoting when
inlined. Write the body to a temp file and pass it with `--input` (REST) or
`--body-file` (`gh pr comment`):

```sh
BODY_FILE="$(mktemp)"
cat > "$BODY_FILE" <<'EOF'
Fixed in abc1234 — the delegation check now requires eligibility, not
existence.
EOF
PAYLOAD_FILE="$(mktemp)"
jq -n --rawfile body "$BODY_FILE" '{body: $body}' > "$PAYLOAD_FILE"
```

## Reply in a thread — inline review comments only

Only inline review comments (from `pulls/{n}/comments`) support threaded
replies, and `{comment_id}` must be the thread's **root** comment — GitHub
rejects replies that target a reply. If the comment being answered has
`in_reply_to_id` set (common when a reviewer follow-up is the newest message
in the thread), post to that ID instead:

```sh
GH_PAGER="" gh api --method POST \
  /repos/{owner}/{repo}/pulls/{n}/comments/{comment_id}/replies \
  --input "$PAYLOAD_FILE"
```

## Reply to non-threadable comments

Top-level PR comments (`issues/{n}/comments`) and review bodies have no
replies endpoint. Post a regular PR comment that quotes or links the original
so the connection is explicit:

```sh
GH_PAGER="" gh pr comment {n} --body-file "$BODY_FILE"
```

## Read and resolve review threads (GraphQL)

Thread resolution isn't exposed over REST — this query is also how the load
step reads `isResolved` to filter settled threads. First map comment IDs to their
containing threads (paginate — threads beyond the first 100 exist on big
PRs):

```sh
GH_PAGER="" gh api graphql --paginate \
  -f owner="{owner}" -f repo="{repo}" -F number={n} \
  -f query='
    query($owner: String!, $repo: String!, $number: Int!, $endCursor: String) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $number) {
          reviewThreads(first: 100, after: $endCursor) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              isResolved
              comments(first: 100) { nodes { databaseId url } }
            }
          }
        }
      }
    }'
```

Then resolve each approved thread:

```sh
GH_PAGER="" gh api graphql \
  -f threadId="$THREAD_ID" \
  -f query='mutation($threadId: ID!) {
    resolveReviewThread(input: { threadId: $threadId }) {
      thread { id isResolved }
    }
  }'
```

If a comment can't be replied to or resolved with the metadata available,
report the limitation and suggest a manual GitHub action instead of guessing.
