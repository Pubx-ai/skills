# adcp rules

Rules for Code Review Agents i.e. Bugbot (Cursor) and CodeRabbit

## What's inside

```text
rules/adcp/
├── adcp.md                                           # this file (rules docs)
└── adcp-review/
    ├── BUGBOT.md                                     # compact single-file rules for code review bots
    └── .coderabbit.yaml                              # ready-to-copy CodeRabbit config (detects BUGBOT.md)
```

## Using the review rules with code review bots

`rules/adcp/adcp-review/BUGBOT.md` is a compact, self-contained distillation of the AdCP
conformance rules, written to be dropped into a repo that implements AdCP so automated
reviewers enforce them. It has no frontmatter and fetches nothing — one file, plain
instructions.

**Cursor Bugbot** — copy it to the consuming repo root (or `.cursor/BUGBOT.md`) as
`BUGBOT.md`; Bugbot picks it up automatically.

**CodeRabbit** — CodeRabbit [auto-detects guideline files](https://docs.coderabbit.ai/knowledge-base/code-guidelines)
like `**/AGENTS.md`, `**/CLAUDE.md`, `**/.cursor/rules/*`, and `**/.rules/*`, but
`BUGBOT.md` is not in its default list. Two options in the consuming repo:

1. *Zero-config*: copy the file to a detected path, e.g. `.rules/adcp-review.md`
   (generic team rules) — or append its content to the repo's `AGENTS.md`.
2. *Keep the `BUGBOT.md` name*: copy the ready-made
   `rules/adcp/adcp-review/.coderabbit.yaml` to the consuming repo root (or merge its
   `knowledge_base` block into the existing config). It adds:

   ```yaml
   knowledge_base:
     code_guidelines:
       enabled: true
       filePatterns:
         - "**/BUGBOT.md"
         - "**/.cursor/BUGBOT.md"   # ** doesn't reliably match dot-dirs
   ```

Either way, note CodeRabbit's **directory scoping**: a guideline file applies to its own
directory and subdirectories only. Place the file at the repo root to cover everything,
or inside the AdCP service's subtree in a monorepo to scope the rules to that service.
File names are case-sensitive (`bugbot.md` won't match a `**/BUGBOT.md` pattern).
