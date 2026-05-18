# SF6 Knowledge Agent Kit Repo Guidance

## Core Identity

- This repo is SF6 Knowledge Agent Kit.
- It is a GitHub-reviewable source of truth for Street Fighter 6 knowledge and repo-local agent workflows.
- Public skill distribution is deferred while private Hermes-first operation is stabilized.
- Keep source-of-truth responsibilities aligned with the canonical surfaces below.

## Canonical Surfaces

- `knowledge/` is canonical.
- `data/exports/` and `data/roster/` are exact current fact authority.
- `data/aliases/` is canonical for query-normalization support, not exact current facts.
- `contracts/` is canonical for schemas and artifact contracts.
- `workflows/` are canonical maintainer procedures.
- `evals/` is canonical for answer-quality cases and rubrics.
- `skills/sf6-agent/SKILL.md` and hand-written files under `skills/sf6-agent/references/` are canonical adapter behavior only.

## Derived Surfaces

- `skills/sf6-agent/references/generated-*` is derived from `knowledge/curated/`.
- `runtime/frame-current/` is derived from `data/exports/` and `data/roster/`.
- `skills/sf6-agent/assets/frame-current/` is a deferred public adapter compatibility bridge derived from `data/exports/` and `data/roster/`.
- `runtime/normalization/` is derived from `data/aliases/`.
- `skills/sf6-agent/assets/normalization/` is a deferred public adapter compatibility bridge derived from `data/aliases/`.
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
- `skills/sf6-agent/` is the existing public adapter surface, but ADR-0002 makes it a deferred legacy distribution surface rather than the active product focus.
- See `docs/architecture/language-policy.md`.

## Japanese Maintainer Documentation

- Maintainer-facing prose may be Japanese-first when it improves repo operation.
- Required repo and skill behavior must stay in canonical entrypoints such as `AGENTS.md` and `skills/sf6-agent/SKILL.md`; do not rely on `.ja.*` companion files for required behavior.
- Do not duplicate canonical knowledge only to create separate English/Japanese versions.
- Use `.ja.*` files for human-facing localized docs only when their canonical, companion, or summary role is clear.
- See `docs/architecture/japanese-maintainer-docs-policy.md`.

## Harness And Distribution Roles

- `skills/sf6-agent/` is the existing public answer adapter surface.
- `AGENTS.md`, `workflows/*`, `tests/validation/*`, `packages/*`, and `contracts/*` are repo-local maintainer surfaces.
- Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available, but Hermes memory and profile state are not canonical.
- Hermes does not make local memory, sessions, profile state, or local skill state canonical.
- `packs/hermes-sf6/*` is repo-local orchestration support, not public answer-skill behavior.
- APM / Agent Skills public distribution is deferred. Do not create a public repo-maintainer skill package without a later architecture decision.
- See `docs/architecture/harness-and-distribution-roles.md`, `docs/architecture/decisions/0001-hermes-primary-orchestration.md`, and `docs/architecture/decisions/0002-private-hermes-first-operation.md`.

## Operating Lanes

- Repo implementation is Codex-first for issue-scoped PRs, validators, contracts, docs, packaging changes, and GitHub workflow operations.
- Hermes is the repo-local growth engine for repeated knowledge-growth and maintainer-growth workflows when a configured maintainer profile is available.
- For analysis, review, and growth tasks in scope for Hermes, Codex is the Hermes operator and boundary auditor rather than the primary analyst when a configured Hermes maintainer profile is available.
- Codex should delegate primary object-level analysis such as source analysis, claim decomposition, observation drafting, review drafting, architecture review drafting, workflow learning, validator-pattern learning, and procedural skill self-improvement to Hermes when configured.
- Codex-only analysis for Hermes-first tasks is fallback behavior and must record why Hermes delegation was not attempted or could not complete.
- Hermes memory, sessions, local skills, Curator output, Kanban workers, and checkpoints are non-canonical until promoted through reviewed repository artifacts.
- Current operation prioritizes personal/private Codex-operated Hermes-first workflows; `skills/sf6-agent/` is deferred until later scoped work decides whether to remove, relocate, or reactivate it.
- See `docs/architecture/hermes-v2.1-roadmap.md`, `docs/architecture/codex-hermes-bridge-policy.md`, and `workflows/codex-to-hermes-delegation.md`.

## Hermes Delegation Command Discipline

- Before using Hermes for in-scope analysis, review `workflows/codex-to-hermes-delegation.md`, the repo Hermes CLI capability reference, local `hermes chat --help`, and official Hermes CLI docs when command behavior or limits matter.
- Do not reuse smoke-test or probe settings such as `--max-turns 1` for real analysis.
- Give Hermes enough turn budget and wall-clock time for the task. Prefer the documented default or a larger explicit `--max-turns` for repo-wide audits, and resume the same session if the first run does not complete.
- If Hermes hits a limit, tool denial, transient provider failure, or context issue, continue with `--resume` / `--continue` or split the delegation into bounded follow-up prompts before declaring Codex fallback.
- Record Codex fallback only after a properly budgeted Hermes attempt, any reasonable resume/retry path, and the blocker have been verified.
- Treat cost saving as secondary to accurate Hermes-first analysis when the issue requires Hermes primary analysis.

## Project Status Protocol

- Before answering project status, resuming previous work, editing files, or updating progress docs, verify the current baseline.
- Identify the current date, cwd, repository root, and git root.
- Read this `AGENTS.md` and any relevant subdirectory or workflow context before applying remembered instructions.
- Run `git status --short --branch` and inspect the relevant issue, PR, roadmap, and on-disk docs for the task.
- Treat Hermes memory, session search, local skills, Curator output, Kanban state, checkpoints, and previous chat summaries as secondary hints only.
- If memory/session recall conflicts with current git, disk, issue, PR, or validator evidence, prefer the current evidence and state the contradiction.
- Label important status claims when useful as `verified_from_git`, `verified_from_disk`, `from_issue_or_pr`, `from_memory_or_session`, `inferred`, or `unknown`.
- Do not modify files, update progress docs, or claim validation if the baseline has unresolved contradictions.
- Do not report tests, validators, PR state, merge state, or issue closure as complete unless verified from current command output, GitHub state, or checked-in artifacts.

## Negative Learning Guard

- Treat missing packages, path problems, auth failures, network failures, sandbox limitations, migration artifacts, stale generated files, and tool-version mismatches as provisional failures.
- Do not write permanent Hermes skills, memory, workflow rules, or repo policy saying a tool or workflow "does not work" unless the user confirms it is a stable constraint or a later verification proves it.
- After environment, dependency, profile, auth, or toolchain changes, retry previously failed tools before preserving an avoidance rule.
- When creating or updating local skills, distinguish permanent API/spec limits, repo policy, temporary environment failures, and one-off transient errors.
- Promote only durable procedural lessons through the reviewed repo path. Do not promote raw failure logs, local Hermes state, or temporary workarounds as canonical behavior.

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
