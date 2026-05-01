# SF6 Knowledge Agent Kit Repo Guidance

## Core Identity

- This repo is SF6 Knowledge Agent Kit.
- It is a GitHub-reviewable source of truth and distribution kit for AI agents answering Street Fighter 6 questions.
- Keep source-of-truth responsibilities aligned with the canonical surfaces below.

## Canonical Surfaces

- `knowledge/` is canonical.
- `data/exports/` and `data/roster/` are exact current fact authority.
- `contracts/` is canonical for schemas and artifact contracts.
- `workflows/` are canonical maintainer procedures.
- `evals/` is canonical for answer-quality cases and rubrics.
- `skills/sf6-agent/SKILL.md` and hand-written files under `skills/sf6-agent/references/` are canonical adapter behavior only.

## Derived Surfaces

- `skills/sf6-agent/references/generated-*` is derived from `knowledge/curated/`.
- `skills/sf6-agent/assets/frame-current/` is derived from `data/exports/` and `data/roster/`.
- Release bundles and generated agent-specific front doors are derived distribution outputs.
- Generated surfaces must identify their generator and source paths.
- Do not make generated surfaces canonical.

## Current Fact Rules

- Do not put exact current values in `knowledge/curated/` or generated knowledge references.
- Exact move-specific current facts must stay grounded in `data/exports/` and generated frame-current assets.
- `data/raw/...`, `data/normalized/...`, and `*_manual_review.*` are not final evidence for normal public answers.
- Runtime frame-current assets must exclude CSV sidecars and manual-review outputs.

## Evidence Metadata And Answer Modes

- Use generic evidence metadata such as `source_kind`, `source_role`, `evidence_basis`, `verification_state`, `confidence`, `volatility`, `patch_sensitivity`, `review_status`, `source_refs`, and `review_after`.
- Use answer modes and evidence-boundary behavior to evaluate answer quality.
- Keep answer behavior grounded in contracts, evals, and source boundaries.

## Workflow Rules

- Maintainer procedures belong under `workflows/`.
- Ingestion and publishing implementation belongs under `ingest/frame_data/`.
- Public adapter packaging belongs under `packages/skill-packaging/`.
- Knowledge-generation tooling belongs under `packages/knowledge-generation/`.
- Hermes is optional maintainer harness, not canonical memory.
- Do not store full copyrighted articles, videos, or transcripts by default.

## GitHub Management

- Use GitHub CLI (`gh`) as the default tool for reproducible issue, pull request, CI status, label, milestone, and merge operations.
- Canonical workflow: `workflows/github-management.md`.
- Use the GitHub web UI when it is safer, clearer, or required by GitHub settings.
- Do not include secrets, tokens, credentials, or private local state in commands, logs, issue comments, PR bodies, or smoke reports.
