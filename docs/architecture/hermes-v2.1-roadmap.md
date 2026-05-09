# Hermes v2.1 Roadmap

## Purpose

Hermes v2.1 establishes Hermes as the primary repo-local orchestration harness when a configured maintainer profile is available.

This does not make Hermes state canonical, does not make Hermes a public distribution target, and does not replace `skills/sf6-agent/`. The public answer adapter remains `skills/sf6-agent/`; reusable maintainer output must remain as repository artifacts.

Hermes v2.1 is not only a safety boundary for answer orchestration. It is also the repo-local growth engine for improving the SF6 skill behavior, workflows, validators, ingest procedures, aliases, and review artifacts over time.

Hermes may learn procedural repo-maintenance skills locally. Reusable improvements from that learning loop must be promoted into repository artifacts through review.

This roadmap records the completed v2.1 foundation work, the dependency model, the non-goals, and the current Hermes capability coverage.

## Operating Lanes

### Repo Implementation Lane

Repo implementation remains Codex-first. Codex may implement issue-scoped PRs, validators, contracts, docs, packaging changes, and GitHub workflow operations.

Hermes does not replace Codex as the repo implementation executor. Hermes can assist with review patterns, procedural learning, and reusable workflow improvements, but committed changes must still land as reviewed repository artifacts.

### Hermes Growth Lane

Hermes is preferred when available for repeated knowledge-growth and maintainer-growth workflows, including source analysis, claim decomposition, observation drafting, review drafting, smoke report drafting, workflow learning, validator-pattern learning, and local procedural skill self-improvement.

Codex may be the entrypoint for this work and may delegate suitable knowledge-growth workflows to a configured Hermes maintainer profile. Hermes may draft artifacts, claims, observations, review notes, and smoke reports, but Hermes memory, sessions, and local skills are not canonical. Canonical promotion still requires repository artifacts, validators, and review.

Agent-managed skills, Curator, session search, subagents, `/goal` checkpoints, durable Kanban, and cron/freshness audits should not be disabled by default. They are useful for SF6 repo artifact growth when they stay within the boundaries in this roadmap.

### Public User Lane

End users do not need Hermes. Codex, Claude, Hermes, or other agents may use `skills/sf6-agent/` as the public answer adapter when they can import the skill.

`skills/sf6-agent/` remains the distribution surface for user answers. Hermes is repo-local maintainer orchestration support, not a requirement for public use.

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
- Codex remains the normal repo implementation executor.
- Hermes may assist or receive delegated knowledge-growth workflows when configured.
- End users do not need Hermes to use `skills/sf6-agent/`.

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
- Automatic promotion from Hermes memory, session search, agent-created skills, Curator output, or Kanban workers into canonical repo surfaces.
- Autonomous current-fact updates without the frame-data refresh workflow and review.
- Treating Hermes self-improvement output as canonical before it is promoted through reviewed repository artifacts.

## Hermes Capability Coverage

| Hermes capability | v2.1 status | Planned use | Boundary |
|---|---|---|---|
| Profiles | constrained / prepared | ingest and smoke profile guidance | profile state outside repo; not executable config yet |
| Subagents | active operational pattern | read-only scope/docs/validator reviews | summaries are not source of truth |
| Agent-managed skills | constrained / recommended | learn recurring SF6 repo-maintenance procedures | local skills are non-canonical until promoted through PR |
| Skill self-improvement | constrained / recommended | improve repeated maintainer workflows, validator patterns, review guards, and ingest procedures | improves procedure only; does not canonicalize SF6 facts |
| Curator | recommended for local skills | prune, patch, and consolidate agent-created procedural skills | must not mutate repo canonical surfaces directly |
| Memory | constrained / recommended | local preferences and operator notes only | never canonical SF6 knowledge |
| Skills / wrappers | prepared | thin wrappers around workflows/contracts | wrappers do not replace workflows |
| Durable Kanban | deferred / planned | coordinate multi-agent backlog work for aliases, ingest, validators, and reviews | workers draft/propose; promotion requires review |
| /goal + checkpoints | recommended for bounded repo tasks | keep long-running maintainer tasks aligned and resumable | checkpoints are non-canonical state |
| Cron | deferred / planned | freshness audits / review reminders | no automatic canonical promotion |
| Web/browser/vision | policy-defined, implementation deferred | article/video research and freshness checks | evidence gate required |
| MCP | deferred | possible future external tool bridge | filtered tools and no authority change |
| Gateway / notifications | deferred | optional notifications | no secrets or sessions in repo |
| Session search | constrained / recommended | recall prior workflow decisions and PR patterns | not SF6 evidence or current-fact authority |
| Execution sandbox | deferred | safer ingest execution | profiles are not sandbox |

This table is documentation-only. It does not add Hermes runtime config, prompts, profile files, cron jobs, MCP configuration, gateway configuration, or runtime assets.

## Next Phase Candidates

These are candidate follow-up issues, not implemented by this roadmap PR:

- Codex-to-Hermes delegation policy for knowledge-growth workflows.
- Normalization runtime asset generator.
- Hermes answer smoke skeleton.
- Article ingest templates and validator.
- Article ingest wrapper and smoke.
- Video observation schema-aware validator.
- Video observation wrapper and smoke.
- Hermes memory usage policy.
- Hermes cron/freshness audit policy.
- Hermes MCP/tooling evaluation.
- Hermes skill self-improvement and promotion policy.
- Hermes Curator policy for agent-created SF6 maintainer skills.
- Hermes durable Kanban policy for multi-agent repo artifact work.
- Hermes `/goal` and checkpoint usage policy for bounded maintainer tasks.
- Hermes session search policy for non-canonical workflow recall.
