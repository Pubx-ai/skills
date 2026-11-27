# File templates

Templates for each file the documentation skills produce. Two rules apply to every template:

- Sections marked *(only if …)* are deleted when the condition doesn't hold — an empty heading
  helps no one.
- Bracketed text describes what to write and never survives into the delivered file. Unbracketed
  sample values (paths like `src/routes/`, names like Stripe, the example diagram, endpoint rows,
  error payloads) are illustrations of shape only — replace them with the project's own facts,
  and never let one leak into a delivered file verbatim.

## `docs/README.md`

````markdown
# [Project Name]

> One or two sentences: what this is and who it's for.

## What it does

[3–5 sentences describing the core problem solved and how. Avoid enumerating features; describe
the system's job.]

## Quick start *(only if the root README has no quick start; otherwise link to it instead)*

```bash
# Minimum steps to run locally. Point at the project's env-var example file (.env.example or
# equivalent) when one exists; otherwise name the required variables and where they're read.
```

Detailed setup → [CONTRIBUTING.md](./CONTRIBUTING.md)

## Key concepts *(only if there are domain terms or non-obvious abstractions)*

[3–6 bullet points maximum, each one sentence. Link to source locations.]

## Where to find things

| Concern | Location |
|---|---|
| [e.g. API routes] | [e.g. `src/routes/`] |
| [e.g. Data models] | [e.g. `src/models/`] |
| [e.g. Business logic] | [e.g. `src/services/`] |

[Keep this table to the most important 5–8 entry points. Omit obvious scaffolding.]
````

## `docs/ARCHITECTURE.md`

````markdown
# Architecture

## Overview

[2–4 sentences describing the architectural style and the main reason for it. Name the pattern
if there is one — e.g. "layered MVC", "hexagonal", "event-driven pipeline".]

## System diagram *(only if spatial relationships genuinely aid understanding)*

[One high-level diagram showing major components and their relationships — ASCII or Mermaid, no
implementation detail. The shape below is an illustration:]

```
[Browser] ──→ [API Gateway] ──→ [App Server] ──→ [Database]
                                       └──→ [Queue] ──→ [Worker]
```

## Components

[For each major component — not every module, only components with distinct responsibilities:]

**[Component name]**
- Purpose: one sentence
- Location: [e.g. `src/path/`]
- Key interfaces/contracts: [brief description or link]
- Notable constraints or decisions: [only if non-obvious]

## External dependencies *(only if the system integrates with external services)*

| Service | Purpose | Integration point |
|---|---|---|
| [e.g. Stripe] | [e.g. Payments] | [e.g. `src/billing/stripe-client.ts`] |

## Key decisions *(only if there are decisions a newcomer would otherwise be confused by)*

[2–5 architectural decisions that are not obvious from the code. Format: decision → rationale
→ consequence.]

- **[Decision]**: [Why it was made. What tradeoff it introduces.]
````

## `docs/CONTRIBUTING.md`

````markdown
# Contributing

## Setup

```bash
# Prerequisites: [e.g. Node 20+, Docker]
# Steps to get a working local environment
```

[Point at the project's env-var example file (.env.example or equivalent) when one exists — do
not duplicate its contents here. Otherwise, name the required variables and link to where
they're read.]

## Development workflow

[Describe the branch strategy and PR process in 3–5 sentences. Only include what isn't obvious
from CI config or PR templates.]

## Running tests

```bash
# Commands only — no explanation of what tests exist
```

Test structure → [test directory]

## Conventions *(only if there are conventions not enforced by tooling)*

[If a linter or formatter handles it, don't document it. Focus on naming patterns, module
boundaries, or domain-specific rules a linter cannot catch.]

## Getting help *(only if there is a real place to ask)*

[Where to ask questions — Slack channel, discussion board, etc.]
````

## `docs/API.md` — *(only if the project exposes an API)*

The template below assumes HTTP/REST. Adapt the sections to the API's actual style: for GraphQL
or gRPC, replace Endpoints with the schema or service entry points and where they're defined;
for event/message APIs, document topics and payload contracts instead.

````markdown
# API

## Base URL and versioning

[Base URL pattern and versioning strategy — one sentence each.]

## Authentication

[Authentication mechanism and where credentials are obtained. Link to relevant source, e.g. the
auth module.]

## Endpoints

[Document only endpoints that are non-obvious, complex, or frequently misunderstood. For
straightforward CRUD, a table is sufficient — the rows below are illustrations:]

| Method | Path | Description |
|---|---|---|
| [e.g. `GET`] | [e.g. `/users`] | [e.g. List users (paginated)] |

[For complex endpoints, add a brief note on behaviour, side-effects, or required context — not a
full schema restatement.]

## Error format

[One example of the project's standard error envelope — the shape below is an illustration. Do
not list every error code.]

```json
{ "error": { "code": "VALIDATION_ERROR", "message": "..." } }
```

## Rate limiting *(only if a policy exists)*

[Policy in one sentence.]
````

## Root `README.md` — Documentation section

Add to the root `README.md` (or include in the minimal one create-documentation writes when none
exists). List only files that actually exist — including pre-existing doc files whose names
differ from the standard set. If the README already has a Documentation section or scattered doc
links, reconcile in place rather than appending a second section.

```markdown
## Documentation

- [Overview](./docs/README.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Contributing](./docs/CONTRIBUTING.md)
- [API](./docs/API.md) [drop this line when API.md was not produced]
```
