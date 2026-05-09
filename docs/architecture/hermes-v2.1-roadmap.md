# Hermes v2.1 Roadmap

## Purpose

Hermes v2.1 establishes Hermes as the primary repo-local orchestration harness when a configured maintainer profile is available.

This does not make Hermes state canonical, does not make Hermes a public distribution target, and does not replace `skills/sf6-agent/`. The public answer adapter remains `skills/sf6-agent/`; reusable maintainer output must remain as repository artifacts.

This roadmap records the completed v2.1 foundation work, the dependency model, the non-goals, and the current Hermes capability coverage.

## Invariants

- Hermes is primary only when a configured maintainer profile is available.
- Hermes remains repo-local orchestration support.
- Hermes state is non-canonical.
- `skills/sf6-agent/` remains the only public answer adapter.
- Repo artifacts are the source of truth.
- Canonical maintainer procedures remain under `workflows/*`.
- Exact current facts remain grounded in `data/exports/` and `data/roster/`.
- Web sources do not override packaged frame-current `official_raw`.
- Query-normalization aliases are not exact current-fact authority.
- Future normalization runtime assets must remain separate from `skills/sf6-agent/assets/frame-current/`.

## Completed v2.1 PR Sequence

### #85 / PR #89: Hermes Orchestration ADR And Architecture Marker Validator

Added:

- `docs/architecture/decisions/0001-hermes-primary-orchestration.md`
- machine-readable Hermes architecture markers and invariant fields
- `tests/validation/validate-architecture-markers.ps1`
- docs references to the ADR
- removal of detailed Hermes prose validation from `validate-v2-surfaces.ps1`

Intentionally not added:

- Hermes pack skeleton
- prompt bodies
- normalization aliases
- ingest wrappers
- generated runtime payloads

Why it matters:

This fixed the architecture boundary first. Later Hermes work can reference a machine-readable ADR instead of relying on exact natural-language marker text.

### #86 / PR #90: Hermes Pack Skeleton And Boundary Validator

Added:

- boundary-only skeleton docs under `packs/hermes-sf6/`
- markdown-only profile guidance
- `tests/validation/validate-hermes-pack.ps1`
- pack boundary checks for repo-local support, non-canonical state, and forbidden local-state or secret-like files

Intentionally not added:

- operational answer prompts
- JSON profile config
- executable Hermes runtime config
- normalization aliases
- article or video ingest wrappers
- public answer behavior

Why it matters:

This prepared the Hermes pack location without letting prompt files or profile config become the de facto specification before contracts existed.

### #87 / PR #91: Answer Orchestration Contracts And Evidence Gate/Web Policy

Added:

- `contracts/answer-intent.schema.json`
- `contracts/evidence-card.schema.json`
- `contracts/answer-plan.schema.json`
- `contracts/evidence-gate.md`
- `contracts/web-research-policy.md`
- six answer-plan fixtures for current fact, stable concept, strategy, observation, hold, and web-needed paths
- `tests/validation/validate-answer-orchestration-contracts.ps1`

Intentionally not added:

- Hermes answer prompts
- retrieval or lookup code
- normalization aliases
- public `sf6-agent` distribution changes
- generated runtime payloads

Why it matters:

This made contracts and evidence policy the source of truth before any Hermes answer prompt bodies are introduced. It also fixed the web boundary: web sources may assist research and freshness checks, but they do not override packaged frame-current `official_raw`.

### #88 / PR #92: Japanese Normalization Alias Surface

Added:

- `data/aliases/README.md`
- `data/aliases/ja-query-fixtures.json`
- `contracts/normalization-aliases.schema.json`
- `tests/validation/validate-normalization-aliases.ps1`
- a minimal fixture mapping `リュウの屈中Pってガードで何F？` to `ryu / 2MP / block_adv`

Intentionally not added:

- full roster alias coverage
- runtime normalization asset generation
- `skills/sf6-agent/assets/normalization/`
- frame-current asset changes
- retrieval or lookup code
- Hermes prompt bodies

Why it matters:

This created a canonical query-normalization support surface while preserving the current-fact boundary. Aliases can map user wording to lookup inputs, but they do not prove frame values, damage values, patch metadata, matchup judgments, or strategy claims.

## Dependency Model

- #85 is the architecture foundation.
- #86 depends on #85 and creates the Hermes pack skeleton plus boundary validator.
- #87 depends on #85 and creates answer contracts plus evidence gate/web policy before any prompt bodies.
- #88 depends on #85 and aligns with #87 by creating query-normalization support without current-fact authority.
- Operational Hermes prompt wrappers must come after contracts and boundaries.
- Runtime normalization asset generation must come after the `data/aliases/` surface and validator.

## Non-Goals

The v2.1 initial foundation work does not implement:

- Hermes operational prompt bodies.
- Full roster alias coverage.
- Runtime normalization asset generation.
- Article/video ingest wrappers.
- Cron jobs.
- MCP integrations.
- Gateway / platform notifications.
- Hermes memory as canonical knowledge.
- Any replacement for `skills/sf6-agent/`.
- Any change to packaged frame-current authority.

## Hermes Capability Coverage

| Hermes capability | v2.1 status | Planned use | Boundary |
|---|---|---|---|
| Profiles | constrained / prepared | ingest and smoke profile guidance | profile state outside repo; not executable config yet |
| Subagents | active operational pattern | read-only scope/docs/validator reviews | summaries are not source of truth |
| Memory | constrained / deferred | local preferences and operator notes only | never canonical SF6 knowledge |
| Skills / wrappers | prepared | thin wrappers around workflows/contracts | wrappers do not replace workflows |
| Cron | deferred | freshness audits / review reminders | no automatic canonical promotion |
| Web/browser/vision | policy-defined, implementation deferred | article/video research and freshness checks | evidence gate required |
| MCP | deferred | possible future external tool bridge | filtered tools and no authority change |
| Gateway / notifications | deferred | optional notifications | no secrets or sessions in repo |
| Session search | deferred | recall workflow context | not evidence |
| Execution sandbox | deferred | safer ingest execution | profiles are not sandbox |

This table is documentation-only. It does not add Hermes runtime config, prompts, profile files, cron jobs, MCP configuration, gateway configuration, or runtime assets.

## Next Phase Candidates

These are candidate follow-up issues, not implemented by this roadmap PR:

- Normalization runtime asset generator.
- Hermes answer smoke skeleton.
- Article ingest templates and validator.
- Article ingest wrapper and smoke.
- Video observation schema-aware validator.
- Video observation wrapper and smoke.
- Hermes memory usage policy.
- Hermes cron/freshness audit policy.
- Hermes MCP/tooling evaluation.
