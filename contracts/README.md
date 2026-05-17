# Contracts

`contracts/` is canonical for schemas and structured artifact contracts.

Contracts distinguish canonical surfaces from derived surfaces and use generic source/evidence metadata.

Some contracts describe Markdown front matter or agent-readable artifacts that are enforced by dedicated validators rather than by a generic JSON Schema runtime. Validators under `tests/validation/` are the executable contract layer for the current repo.

`tests/validation/validate-ingest-artifacts.ps1` is the executable contract layer for artifact-level review-only metadata under `knowledge/evidence/claims/*.claims.md`.

`tests/validation/validate-current-fact-boundaries.ps1` is the executable contract layer for review-only current-fact candidate metadata under `knowledge/review/current-fact-candidates/`.

When `source_refs.path` points to a migrated legacy file, `source_revision` identifies the commit where that historical path can be reviewed.

## Human-Readable Contracts

- `calculation-executor-trace.md`: boundary for calculation tools as executors and trace generators only.
- `combo-notation.md`: notation rules for `evals/fixtures/combo-damage/*.yaml`.
- `evidence-gate.md`: answer evidence authority boundaries for current facts, review claims, observations, and Hermes state.
- `frame-current-runtime-assets.md`: runtime asset boundary for generated frame-current payloads.
- `video-observation.md`: timestamped video observation artifact contract.
- `web-research-policy.md`: web source ranking, freshness, and current-fact conflict policy.

## Answer Orchestration Schemas

- `answer-intent.schema.json`: intent and answer-mode classification contract.
- `evidence-card.schema.json`: evidence authority and source-boundary card contract.
- `answer-plan.schema.json`: answer planning contract combining intent, evidence cards, web state, hold reasons, and response requirements.

## Query Normalization Contracts

- `normalization-aliases.schema.json`: query-normalization alias contract for mapping user language to structured lookup inputs.
- `data/aliases/`: canonical query-normalization support, not exact current-fact authority. Exact current facts remain grounded in `data/exports/` and `data/roster/`.

## Maintainer Toolchain Contracts

- `agent-toolchain.schema.json`: maintainer agent toolchain policy contract for reviewed capabilities and freshness expectations.
- `data/toolchain/`: canonical maintainer-toolchain policy data, not SF6 gameplay knowledge or exact current-fact authority.

## Repository Surface Registry

- `repository-surface.schema.json`: machine-readable index contract for canonical, derived, deferred legacy, repo-local support, historical, and non-canonical repository surfaces.
- `data/repository-surfaces.json`: seed registry of existing reviewed boundaries. The registry indexes current policy; it does not replace `AGENTS.md`, ADRs, workflows, or validators as policy sources yet.
