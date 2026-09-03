# skills

**Skills from pubXers, straight from our `.claude` directories. Live long and prompt!** 🖖

Created by [pubXers](https://pubx.ai/our-team/) — a shared collection of agent skills and code-review rules that anyone can install into their coding agent of choice.

## Quickstart (30-second setup)

1. Run the [skills.sh](https://skills.sh) installer:

   ```bash
   npx skills@latest add pubx-ai/skills
   ```

2. Pick the skills you want and which coding agents to install them on.
   **Make sure you select `/adcp`, `/adtech`, or `/dev`.**

## What's inside

### [`skills/`](skills/)

Agent skills, installable via [skills.sh](https://skills.sh). Each skill lives in its own `<folder>/<skill-name>/SKILL.md`:

| Folder                      | What it covers                                                                                   |
| :-------------------------- | :----------------------------------------------------------------------------------------------- |
| [`adcp/`](skills/adcp/)     | AdCP (Ad Context Protocol) skills — spec-conformance code review, readiness scorecard, and more. |
| [`adtech/`](skills/adtech/) | AdTech practitioner Q&A — programmatic, header bidding, GAM, OpenRTB, agentic advertising.       |
| [`dev/`](skills/dev/)       | Development workflow skills — requirements gathering, implementation planning, and more.         |

Browse a folder to see the current set of skills — they evolve often.

### [`rules/`](rules/)

Rules for code review agents (Cursor Bugbot and CodeRabbit). See [rules/adcp/adcp.md](rules/adcp/adcp.md) for setup instructions.

---

Questions or ideas? Open an issue or PR — contributions from fellow pubXers are always welcome.
