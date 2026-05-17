# Harness And Distribution Roles

SF6 Knowledge Agent Kit separates public answer distribution from repo-local maintenance.

The public package previously aimed to help agents answer Street Fighter 6
questions. Repo-local maintainer surfaces help maintainers grow and validate
this repository after cloning it.

ADR-0002 changes the active priority: private Hermes-first operation is the
current focus, and public skill distribution is deferred while knowledge
collection, review, validation, and promotion workflows are stabilized.

## Public Answer Adapter

`skills/sf6-agent/` is the existing public answer adapter surface.

It is not the active product surface during the private Hermes-first operation
phase. There are no known external public-skill users, so this surface is not
protected as an external compatibility contract. Later scoped work may remove
or relocate it after mapping its remaining canonical and derived
responsibilities.

While it remains in the repository, public distribution surfaces are limited
to:

- `skills/sf6-agent/SKILL.md`
- hand-written adapter policies under `skills/sf6-agent/references/`
- generated reference payloads under `skills/sf6-agent/references/generated-*`
- frame-current runtime assets under `skills/sf6-agent/assets/frame-current/`
- release bundles derived from those adapter surfaces

Do not create a separate `sf6-agent-ja` adapter at this stage.
Do not add new public adapter features unless a later architecture decision
reactivates public distribution work.

## Repo-local Maintainer Surfaces

The following are repo-local maintainer surfaces:

- `AGENTS.md`
- `workflows/*`
- `tests/validation/*`
- `packages/*`
- `contracts/*`
- `docs/architecture/*`
- `packs/hermes-sf6/*`

Maintainers use these after cloning the repository. They are not public answer skills and do not need to be externally distributed as a public repo-maintainer skill package.

“Repo-local” describes distribution and access boundaries; it does not mean non-canonical. Some repo-local surfaces, such as `contracts/` and `workflows/`, are canonical within the repository.

## Hermes Repo-Local Orchestration

Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available.

Hermes coordinates knowledge ingest, review, image observation, video observation, validation, smoke workflows, and repo-local answer orchestration. It is not a public answer adapter and is not required for public distribution.

Hermes is primary when configured, but it is not a hard dependency for using or maintaining the repository. Maintainers may use Codex, other agents, or manual workflows as fallback executors when Hermes is unavailable.

Hermes memory, sessions, profile state, browser state, cron state, and local managed skills are not canonical SF6 knowledge.

Hermes built-in memory and `session_search` may be used only as local
non-canonical context under `docs/architecture/hermes-memory-policy.md`.
External Memory Providers are not enabled by default for v2.6 private
`sf6ingest` operation.

Final outputs must be repo artifacts, such as:

- `knowledge/sources/*`
- `knowledge/evidence/claims/*`
- `knowledge/evidence/video-observations/*`
- `knowledge/review/*`
- `knowledge/curated/*` after review and promotion
- `docs/testing/smoke-runs/*`

## Hermes Wrappers

`packs/hermes-sf6/*` is repo-local Hermes orchestration support.

Hermes wrappers, if added later, should be thin wrappers around canonical workflows such as:

- `workflows/ingest-article.md`
- `workflows/ingest-video.md`
- `workflows/review-claims.md`
- `workflows/media-scratch-cache-policy.md`
- `workflows/hermes-ingest-profile-setup.md`

Wrappers must not become independent source-of-truth procedures. If a wrapper discovers a better procedure, update the canonical workflow first or in the same PR.

The accepted v2.1 orchestration decision is [decisions/0001-hermes-primary-orchestration.md](./decisions/0001-hermes-primary-orchestration.md).
The active private-operation priority is [decisions/0002-private-hermes-first-operation.md](./decisions/0002-private-hermes-first-operation.md).

## Codex And Repo Development

Codex, humans, or other agents may be used for repo development, PR work, validators, packaging, and GitHub operations.

`workflows/github-management.md` is repo-local maintainer workflow guidance. It is not public answer skill behavior.

Repository development work belongs in repo-local surfaces such as `AGENTS.md`, `workflows/*`, `tests/validation/*`, `packages/*`, and `contracts/*`.

## APM And Agent Skills

APM or Agent Skills public distribution is deferred by ADR-0002.

APM may also support repo-local maintainer setup manifests after cloning this repository.

External Agent Skill dependencies for private `sf6ingest` operation are
managed by `docs/architecture/agent-skill-dependency-policy.md` and
`tools/agent-skills/apm.yml`. They are maintainer executor / operator
instruction dependencies only; they do not provide SF6 official values,
formulas, rounding rules, current facts, or public answer authority.

Do not create a public repo-maintainer skill package at this stage. Repo
maintainer workflows require a clone of this repository and should remain
repo-local unless a later architecture decision says otherwise.

## Language Policy

This boundary follows the Japanese-first operating policy in `docs/architecture/language-policy.md`.

Japanese prose is allowed and encouraged where appropriate. Metadata keys, artifact IDs, schema enum values, filenames and path slugs, generated markers, validator contracts, package interfaces, and installer interfaces remain English-compatible.
