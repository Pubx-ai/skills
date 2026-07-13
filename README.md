# skills
Skills from pubXers. Straight from our .claude directories. Live long and prompt!

Created by [pubXers](https://pubx.ai/our-team/).

## Quickstart (30-second setup)

1. Run the skills.sh installer:

```bash
npx skills@latest add pubx-ai/skills
```

2. Pick the skills you want, and which coding agents you want to install them on. **Make sure you select `/adcp` or `/dev`**.

## What's inside

- [`skills/`](skills/) — agent skills, installable via [skills.sh](https://skills.sh):
  - `adcp/adcp-review` — review code changes for conformance with the AdCP (Ad Context Protocol) technical spec.
  - `dev/gather-requirements` — turn a fuzzy feature request into an implementation-ready requirements document.
  - `dev/planner` — turn a requirements document into a sequential implementation plan an AI coding agent can execute.
- [`rules/`](rules/) — rules for code review agents (Cursor Bugbot and CodeRabbit). See [rules/adcp/adcp.md](rules/adcp/adcp.md) for setup instructions.
