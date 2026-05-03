# Harness And Distribution Roles

SF6 Knowledge Agent Kit separates public answer distribution from repo-local maintenance.

The public package should help agents answer Street Fighter 6 questions. Repo-local maintainer surfaces should help maintainers grow and validate this repository after cloning it.

## Public Answer Adapter

`skills/sf6-agent/` is the public answer adapter.

It is the surface intended for users and agents that need SF6 answers, not repository maintenance behavior.

Public distribution should focus on:

- `skills/sf6-agent/SKILL.md`
- hand-written adapter policies under `skills/sf6-agent/references/`
- generated reference payloads under `skills/sf6-agent/references/generated-*`
- frame-current runtime assets under `skills/sf6-agent/assets/frame-current/`
- release bundles derived from those adapter surfaces

Do not create a separate `sf6-agent-ja` adapter at this stage.

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

## Hermes Maintainer Harness

Hermes is an optional maintainer harness for knowledge ingest, review, image observation, video observation, and repeated workflow execution.

Hermes is recommended when a configured maintainer profile is available, but it is not required. Maintainers may use Codex, other agents, or manual workflows when Hermes is unavailable.

Hermes memory, sessions, profile state, browser state, cron state, and local managed skills are not canonical SF6 knowledge.

Final outputs must be repo artifacts, such as:

- `knowledge/sources/*`
- `knowledge/evidence/claims/*`
- `knowledge/evidence/video-observations/*`
- `knowledge/review/*`
- `knowledge/curated/*` after review and promotion
- `docs/testing/smoke-runs/*`

## Hermes Wrappers

`packs/hermes-sf6/*` is repo-local optional Hermes harness support.

Hermes wrappers, if added later, should be thin wrappers around canonical workflows such as:

- `workflows/ingest-article.md`
- `workflows/ingest-video.md`
- `workflows/review-claims.md`
- `workflows/media-scratch-cache-policy.md`
- `workflows/hermes-ingest-profile-setup.md`

Wrappers must not become independent source-of-truth procedures. If a wrapper discovers a better procedure, update the canonical workflow first or in the same PR.

## Codex And Repo Development

Codex, humans, or other agents may be used for repo development, PR work, validators, packaging, and GitHub operations.

`workflows/github-management.md` is repo-local maintainer workflow guidance. It is not public answer skill behavior.

Repository development work belongs in repo-local surfaces such as `AGENTS.md`, `workflows/*`, `tests/validation/*`, `packages/*`, and `contracts/*`.

## APM And Agent Skills

APM or Agent Skills may be considered for public `sf6-agent` distribution.

APM may also support repo-local maintainer setup manifests after cloning this repository.

Do not create a public repo-maintainer skill package at this stage. Repo maintainer workflows require a clone of this repository and should remain repo-local unless a later architecture decision says otherwise.

## Language Policy

This boundary follows the Japanese-first operating policy in `docs/architecture/language-policy.md`.

Japanese prose is allowed and encouraged where appropriate. Metadata keys, artifact IDs, schema enum values, filenames and path slugs, generated markers, validator contracts, package interfaces, and installer interfaces remain English-compatible.
