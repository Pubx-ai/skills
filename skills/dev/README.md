# dev skills

Development tools and coding skills — pubX's delivery pipeline, encoded as skills. Together they
cover the Agentic SDLC end to end; each skill also stands alone.

Install: `npx skills@latest add pubx-ai/skills` and pick `/dev` (see the repo [README](../../README.md)).
Skills are invoked as `/dev:<skill>`.

## Skills

| Stage | Skill | What it does |
| :---- | :---- | :----------- |
| Plan | `gather-requirements` | Interviews you one decision at a time; turns a fuzzy ask into an implementation-ready requirements doc |
| Plan | `create-plan` | Turns signed-off requirements into a task-by-task plan an agent can execute without guessing |
| Plan | `execute-plan` | Executes that plan task by task — review gate on every commit, checkpoint after every task |
| Build | `create-branch` | Correctly named feature branch (`feat/PUB-1234-slug`), cut from a fresh base, JIRA-aware |
| Build | `create-commit` | Conventional Commits with branch-safety and staging discipline |
| Build | `local-review` | Senior-engineer review of uncommitted changes, before they hit a commit |
| Build | `run-tests` | Detects how *this* project runs its tests (AGENTS.md, lockfiles, Makefiles) and runs them properly |
| Ship | `local-pr-review` | Whole-branch review with a score and merge recommendation, before the PR exists |
| Ship | `local-bot-review` | Runs the CodeRabbit CLI locally so bot findings land before you push |
| Ship | `raise-pr` | Verifies the branch is raisable, gates on review, opens a structured PR — on your say-so |
| Ship | `address-pr-comments` | Loads, triages, and resolves PR comments — fixes what's real, pushes back with reasoning |
| Assess | `local-test-review` | Reviews a repo's testing state against a strategy; delivers a risk-ranked gap plan |

## Recommended companion skills / credits

Several skills delegate to — or borrow technique from — external skills *when they're installed*;
everything works without them, but they deepen the experience. Install any of them with the
[skills CLI](https://skills.sh/) (`npx skills add <owner>/<repo> --skill <name>`):

| Skill | Source | Used by |
| :---- | :----- | :------ |
| [`executing-plans`](https://skills.sh/obra/superpowers/executing-plans) | `obra/superpowers` | execute-plan (delegated loop) |
| [`subagent-driven-development`](https://skills.sh/obra/superpowers/subagent-driven-development) | `obra/superpowers` | execute-plan (preferred delegate with subagents) |
| [`receiving-code-review`](https://skills.sh/obra/superpowers/receiving-code-review) | `obra/superpowers` | address-pr-comments, execute-plan, local-bot-review |
| [`verification-before-completion`](https://skills.sh/obra/superpowers/verification-before-completion) | `obra/superpowers` | execute-plan |
| [`writing-plans`](https://skills.sh/obra/superpowers/writing-plans) | `obra/superpowers` | create-plan |
| [`systematic-debugging`](https://skills.sh/obra/superpowers/systematic-debugging) | `obra/superpowers` | run-tests (debugging hand-off) |
| [`grill-me`](https://skills.sh/mattpocock/skills/grill-me) / [`grilling`](https://skills.sh/mattpocock/skills/grilling) | `mattpocock/skills` | gather-requirements (premise stress-testing) |
| [`writing-great-skills`](https://skills.sh/mattpocock/skills/writing-great-skills) | `mattpocock/skills` | skill authoring |
| [`skill-creator`](https://skills.sh/anthropics/skills/skill-creator) | `anthropics/skills` | skill authoring |
| [`webapp-testing`](https://skills.sh/anthropics/skills/webapp-testing) | `anthropics/skills` | run-tests, local-test-review (browser validation) |
| [`testing-strategy`](https://skills.sh/anthropics/knowledge-work-plugins/testing-strategy) | `anthropics/knowledge-work-plugins` | local-test-review (delegated strategy design) |
| [`code-review`](https://skills.sh/coderabbitai/skills/code-review) | `coderabbitai/skills` | local-bot-review (delegated CodeRabbit review) |
| [`python-testing-patterns`](https://skills.sh/wshobson/agents/python-testing-patterns) | `wshobson/agents` | local-test-review (Python implementation how-to) |
| [`interview-me`](https://skills.sh/addyosmani/agent-skills/interview-me) | `addyosmani/agent-skills` | gather-requirements (intent-level interviewing) |

## Prerequisites

`gh` (authenticated), the Claude Code CLI, and the CodeRabbit CLI (`coderabbit`, for
local-bot-review).
