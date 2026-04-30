# SF6 Knowledge Agent Kit

SF6 Knowledge Agent Kit is a GitHub-reviewable source of truth and distribution kit for AI agents that answer Street Fighter 6 questions with clear evidence boundaries.

The repo separates stable curated knowledge, exact current facts, agent workflows, evals, and generated distribution payloads. The public runtime adapter is `skills/sf6-agent/`.

## Source Boundaries

- `knowledge/` is canonical for curated SF6 knowledge.
- `data/exports/` and `data/roster/` are the exact current-fact authority.
- `contracts/` is canonical for artifact schemas and structured contracts.
- `workflows/` is canonical for maintainer procedures.
- `evals/` is canonical for answer-quality cases and rubrics.
- `skills/sf6-agent/SKILL.md` and hand-written policy references are canonical adapter behavior.
- `skills/sf6-agent/references/generated-*` is derived from `knowledge/curated/`.
- `skills/sf6-agent/assets/frame-current/` is derived from `data/exports/` and `data/roster/`.
- Release bundles and generated agent front doors are distribution outputs, not canonical source.

## Generation Lines

Curated knowledge becomes bundled references through a one-way generated surface:

```text
knowledge/curated/
-> packages/knowledge-generation/
-> skills/sf6-agent/references/generated-*.md
```

Exact current facts become bundled runtime assets through a separate current-fact package:

```text
data/exports/ + data/roster/
-> packages/skill-packaging/build-frame-current-runtime-assets.ps1
-> skills/sf6-agent/assets/frame-current/
```

Generated knowledge references must not contain exact current frame values. Exact move-specific values belong only in `data/exports/` and derived frame-current runtime assets.

## Public Adapter

Use `skills/sf6-agent/` as the single public adapter. It can answer from:

- hand-written answer, uncertainty, and current-fact policies
- generated curated knowledge references
- generated frame-current runtime assets

The adapter communicates answer modes and evidence boundaries without requiring legacy bracket labels.

## Installation

Public distribution is built as:

```text
.dist/sf6-agent-bundle.zip
```

Human-readable install docs live under `docs/distribution/agents/`.

## Contributing

Before moving knowledge or current facts, read [v2-architecture.md](./docs/architecture/v2-architecture.md).

Do not store full copyrighted articles, videos, or transcripts by default. Store source references, short necessary excerpts, summaries, extracted claims, frame ranges or timestamps, review notes, and generic evidence metadata.
