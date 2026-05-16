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

## Language Policy

- Japanese is the primary operating language for SF6 user questions, source summaries, review notes, and curated prose when appropriate.
- Metadata keys, artifact IDs, schema enum values, filenames, generated markers, and validator contracts remain English-compatible.
- Do not duplicate canonical knowledge only to create separate English/Japanese versions.
- Keep `skills/sf6-agent/` as the single public adapter unless a later architecture decision changes it.
- See `docs/architecture/language-policy.md`.

## Japanese Maintainer Documentation

- Maintainer-facing prose may be Japanese-first when it improves repo operation.
- Required repo and skill behavior must stay in canonical entrypoints such as `AGENTS.md` and `skills/sf6-agent/SKILL.md`; do not rely on `.ja.*` companion files for required behavior.
- Do not duplicate canonical knowledge only to create separate English/Japanese versions.
- Use `.ja.*` files for human-facing localized docs only when their canonical, companion, or summary role is clear.
- See `docs/architecture/japanese-maintainer-docs-policy.md`.

## Harness And Distribution Roles

- `skills/sf6-agent/` is the public answer adapter.
- `AGENTS.md`, `workflows/*`, `tests/validation/*`, `packages/*`, and `contracts/*` are repo-local maintainer surfaces.
- Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available, but Hermes memory and profile state are not canonical.
- Hermes does not replace `skills/sf6-agent/` as the public answer adapter.
- `packs/hermes-sf6/*` is repo-local orchestration support, not public answer-skill behavior.
- APM / Agent Skills may support public `sf6-agent` distribution or repo-local setup manifests, but do not create a public repo-maintainer skill package without a later architecture decision.
- See `docs/architecture/harness-and-distribution-roles.md` and `docs/architecture/decisions/0001-hermes-primary-orchestration.md`.

## Operating Lanes

- Repo implementation is Codex-first for issue-scoped PRs, validators, contracts, docs, packaging changes, and GitHub workflow operations.
- Hermes is the repo-local growth engine for repeated knowledge-growth and maintainer-growth workflows when a configured maintainer profile is available.
- For analysis, review, and growth tasks in scope for Hermes, Codex is the Hermes operator and boundary auditor rather than the primary analyst when a configured Hermes maintainer profile is available.
- Codex should delegate primary object-level analysis such as source analysis, claim decomposition, observation drafting, review drafting, architecture review drafting, workflow learning, validator-pattern learning, and procedural skill self-improvement to Hermes when configured.
- Codex-only analysis for Hermes-first tasks is fallback behavior and must record why Hermes delegation was not attempted or could not complete.
- Hermes memory, sessions, local skills, Curator output, Kanban workers, and checkpoints are non-canonical until promoted through reviewed repository artifacts.
- End users do not need Hermes; `skills/sf6-agent/` remains the public answer adapter.
- See `docs/architecture/hermes-v2.1-roadmap.md`, `docs/architecture/codex-hermes-bridge-policy.md`, and `workflows/codex-to-hermes-delegation.md`.

## Workflow Rules

- Maintainer procedures belong under `workflows/`.
- Ingestion and publishing implementation belongs under `ingest/frame_data/`.
- Public adapter packaging belongs under `packages/skill-packaging/`.
- Knowledge-generation tooling belongs under `packages/knowledge-generation/`.
- Hermes is primary when configured, but not canonical memory.
- Do not store full copyrighted articles, videos, or transcripts by default.

## GitHub Management

- Use GitHub CLI (`gh`) as the default tool for reproducible issue, pull request, CI status, label, milestone, and merge operations.
- Canonical workflow: `workflows/github-management.md`.
- Use the GitHub web UI when it is safer, clearer, or required by GitHub settings.
- Do not include secrets, tokens, credentials, or private local state in commands, logs, issue comments, PR bodies, or smoke reports.
