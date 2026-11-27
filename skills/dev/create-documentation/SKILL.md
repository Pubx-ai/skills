---
name: create-documentation
description: >
  Create concise, high-signal project documentation where none exists — a docs/ folder with
  README, ARCHITECTURE, CONTRIBUTING, and (only when the project exposes an API) API docs —
  written for progressive disclosure so engineers and AI agents can orient in a codebase without
  reading it whole. Use this skill whenever the user asks to "document this project", "write
  project docs", "create a docs folder", "set up documentation", "write an architecture overview
  or ARCHITECTURE.md", "add onboarding or contributor docs", or says the project has no
  documentation and needs some. DO NOT USE for bringing existing documentation up to date — that
  is update-documentation's job. DO NOT USE for agent-instruction files such as AGENTS.md or
  CLAUDE.md (operating instructions for agents, a different genre from orientation docs), for
  requirements documents (use gather-requirements), for implementation plans (use create-plan),
  or for generated API reference, which belongs to the project's own tooling.
---

# Create Documentation

Act as a technical documentation specialist producing concise, high-signal documentation that
helps engineers and AI coding agents quickly understand a codebase — its purpose, structure, and
boundaries — without duplicating what the source code already expresses.

**Guiding principle: documentation says what the code *cannot* say.** Point to code; don't
restate it. Every sentence that paraphrases something a reader could learn from the file it
links to is a sentence that will rot the moment that file changes.

**User-initiated only.** Run this skill when the user explicitly asked for documentation to be
created, or confirmed a suggestion to create it. Other skills point here as a follow-up — that's
a suggestion for the *user* to answer, never a licence to chain into creating docs autonomously.
Whether a repo carries documentation at all is a cost/benefit decision that belongs to a human,
not a workflow side effect.

## 1. Orient before writing anything

Examine the project first — most documentation inputs are facts the repo already holds:

- Directory tree (top 2–3 levels).
- The dependency manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or
  equivalent) — tech stack, entry points, scripts.
- CI/CD configuration — how changes actually reach production.
- Any existing docs: root `README.md`, `docs/`, wikis linked from the repo, `AGENTS.md` /
  `CLAUDE.md` (read them for facts; do not edit them — they are a different genre).

## 2. Take stock — this skill creates, it does not rewrite

What you found in step 1 decides whether this skill applies at all:

- **Documentation already exists** (a `docs/` folder, or equivalent files elsewhere) → changing
  existing files is **update-documentation**'s job; say so and use it. This skill may still
  *add* files genuinely missing from the set (e.g. `docs/` has a README but no
  `ARCHITECTURE.md`): run §3–§6 scoped to just the missing file(s), match the existing files'
  style and location, and reconcile the root README's Documentation section to include them.
- **Documentation is intentionally absent or lives elsewhere** (the repo says so — e.g.
  "documentation lives in the team wiki") → respect that. If the documented home is reachable,
  offer to improve it there instead. If the user accepts, run §3–§6 with that home as the
  target — same content, the home's own structure and format; when the home cannot be edited
  from this session, draft the material locally and hand it to the user to publish. If the user
  declines, the home is unreachable, or no one is available to answer, report the situation and
  stop. Never scaffold a parallel `docs/` folder that will compete with the documented home.
- **No documentation and no statement about it** → proceed: this is the case the rest of this
  skill serves.

## 3. Ask only what the code cannot answer

Before producing anything, close the gaps step 1 left open. They split the way requirements do —
facts versus judgement:

- Anything the repo, its CI, or its dependencies can answer is a **fact**: look it up, never
  ask.
- What remains is worth one round of targeted questions, drawn from: purpose and audience; key
  entry points; architecture style and its rationale; external service dependencies; domain
  terms and business rules invisible in the code; how changes get from a branch to production.
  Ask only the ones still open, each with your best inference stated so the user can simply
  confirm or correct.

**When no one is available to answer** (running non-interactively), don't stall: write the docs
from codebase-grounded inference, mark anything genuinely uncertain inline as an explicit open
question (e.g. a blockquote "TODO: confirm — …"), and list those spots in your final report
rather than inventing an answer.

## 4. Documentation principles

These five principles govern every file; the quality check in §6 enforces them.

1. **Progressive disclosure.** Lead with the essential, then link to detail. A reader should be
   able to stop at any point and still have something useful.
2. **Reference, don't restate.** Favour file paths and module references over reproducing
   implementation details. "Authentication lives in `src/auth/` — see `JwtStrategy`" is
   correct; a step-by-step prose replay of the token validation flow is wrong.
3. **Stable over volatile.** Document what changes infrequently: purpose, structure, contracts,
   key decisions. Leave out what the code expresses directly — exact function signatures,
   configuration defaults, dependency versions, test counts. Volatile facts get a source
   reference instead of a value.
4. **One diagram maximum per document.** A diagram only where spatial relationships genuinely
   aid understanding — ASCII or Mermaid, top-level flow only, no implementation detail.
5. **Don't document for documentation's sake.** Documentation is a cost a human chose to pay,
   per repo: code answers *what*, docs exist for *why* and orientation, and a document that no
   longer earns its maintenance is deleted (or never written), not kept polished.

## 5. Produce the documentation

With inputs settled (§3), produce exactly what §2 scoped you to — the full set below in create
mode; only the missing file(s) when gap-filling an existing set; the external home's files when
the user accepted that offer. Never write over a documentation file that already exists —
changing existing files is update-documentation's job, whatever mode this run is in. The one
exception is the root `README.md`'s Documentation section below, which this skill adds or
reconciles in place. The full create-mode set:

```text
./docs/
├── README.md          # What this system is and why it exists
├── ARCHITECTURE.md    # How the system is structured and why
├── CONTRIBUTING.md    # How to work on this project
└── API.md             # Only if the project exposes an API
```

Follow the per-file templates in [references/templates.md](references/templates.md) — read that
file before writing any of them. `API.md` exists only when the project actually exposes an API;
for a library, CLI, or internal tool, omit it rather than force-fit one.

Then give the **root `README.md`** a "Documentation" section linking to every documentation
file that exists — pre-existing files, non-standard names included, plus what this run produced
(the block shape is in the templates file). If the root
README already has such a section or scattered doc links, reconcile in place — never append a
duplicate. Do not duplicate
setup instructions between the root README and `docs/`: the root README stays the quick-start
entry point, `docs/README.md` provides the deeper orientation. If the project has no root
README, create a minimal one — title, one-paragraph description, quick start, and the
Documentation section — nothing more.

## 6. Quality check — before delivering

Verify every produced file:

- [ ] Nothing restates information already clear from the source code.
- [ ] Every section earns its place — delete anything that doesn't help orientation. An empty
      template section is deleted, not padded.
- [ ] File and module references are accurate — spot-check that each referenced path exists.
- [ ] At most one diagram per document, top-level flow only.
- [ ] Volatile information (exact versions, config values, schema fields) is absent or replaced
      with a source reference.
- [ ] No sample values from the templates survived into the delivered files.
- [ ] A new engineer or AI agent could orient from these docs without reading the whole
      codebase.

Fix what fails, then report: which files were created, what was deliberately omitted and why
(e.g. no `API.md` — project exposes no API), and any open questions awaiting the user. Present
the result for review — committing, like any state change to the repo, is the user's call unless
they already asked for it.
