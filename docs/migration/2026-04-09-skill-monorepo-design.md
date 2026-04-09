# SF6 Skill Monorepo Migration Design

Date: 2026-04-09

## Goal

This repository should evolve from a mixed "SF6 knowledge/data repo with embedded skills" into a skill authoring and distribution monorepo.

The target shape is a repository where:

- each distributed skill lives as an independent unit under `skills/<skill-name>/`
- shared authoring, packaging, validation, and installer logic lives outside individual skills
- repository-maintainer-only workflows do not leak into the public distribution surface
- future skills can be added alongside existing SF6 skills without reshaping the repo again

## Why Change

The current layout mixes several concerns:

- distributed skills under `.agents/skills/`
- maintainer-only workflows such as `sync-knowledge`
- repo-local automation prompts
- source data and ingestion code that some skills depend on directly

This makes it unclear whether the repository is meant to be:

- a workspace-local Codex repo
- a public skill library
- an SF6 data and knowledge repo

Popular skill repositories separate those concerns more clearly. They keep `skills/` as the public source surface and move packaging, docs, tests, templates, and agent-specific distribution metadata outside the skill directories.

## Design Principles

1. `skills/<skill-name>/` is the canonical source for distributed skills.
2. Every skill must remain understandable and packageable as a mostly independent unit.
3. Shared code belongs in `packages/`; shared non-code artifacts belong in `shared/`.
4. Maintainer-only workflows must not sit beside public distribution units.
5. Repo-local dogfooding is optional and must not define the public structure.
6. Do not centralize domain knowledge too early. Only promote something to shared once two or more skills need the same contract.

## Repository Roles

### Distributed Skills

Distributed skills are the public units intended for installation in external agent environments.

Examples in this repository:

- `kb-sf6-core`
- `kb-sf6-frame-current`
- future skills such as `video-combo-analysis`

These belong under `skills/`.

### Maintainer Skills

Maintainer skills help operate this repository and curate knowledge or datasets. They are not part of the public distribution surface by default.

Example:

- `sync-knowledge`

These belong under `maintainer-skills/`.

### Shared Infrastructure

Shared infrastructure supports multiple skills or multiple distribution targets.

Examples:

- installer generation
- packaging logic
- validation logic
- common schemas
- authoring templates
- brand assets and icons

These belong under `packages/`, `shared/`, `docs/`, `tests/`, and `scripts/`.

## Target Repository Structure

```text
SF6-skills/
  skills/
    kb-sf6-core/
      SKILL.md
      references/
      assets/
      scripts/
      tests/
    kb-sf6-frame-current/
      SKILL.md
      references/
      assets/
      scripts/
      tests/
    video-combo-analysis/
      SKILL.md
      references/
      assets/
      scripts/
      tests/

  maintainer-skills/
    sync-knowledge/
      SKILL.md
      references/
      templates/

  packages/
    skill-packaging/
    skill-validator/
    skill-installers/
    sf6-data-contracts/
    video-analysis-contracts/

  shared/
    templates/
    schemas/
    vocab/
    branding/

  docs/
    architecture/
    authoring/
    distribution/
    migration/
    testing/

  tests/
    install/
    packaging/
    integration/
    fixtures/

  scripts/
    build/
    release/
    sync/
    dev/

  .codex/
    INSTALL.md
    plugins/

  .claude-plugin/
    marketplace.json

  .cursor-plugin/
    marketplace.json

  .opencode/
    INSTALL.md

  README.md
  CONTRIBUTING.md
```

## What Lives Where

### `skills/`

Put only publicly distributed skills here.

Each skill should own:

- its `SKILL.md`
- skill-local references
- skill-local assets
- skill-local helper scripts
- skill-local tests

The default assumption is that a new skill starts fully self-contained here.

### `maintainer-skills/`

Put repository operation skills here.

These skills may assume repository-specific workflows, internal data layouts, or editorial processes.

### `packages/`

Put reusable implementation here when the reuse is real and cross-skill.

Expected package categories:

- `skill-packaging`: build zip or distribution bundles from `skills/*`
- `skill-validator`: validate skill shape, metadata, and packaging outputs
- `skill-installers`: generate agent-specific install materials
- `sf6-data-contracts`: shared contracts for published SF6 data snapshots
- `video-analysis-contracts`: shared contracts for future video/combo skills

### `shared/`

Put non-code artifacts here that multiple skills or packages need.

Expected contents:

- authoring templates
- metadata templates
- schema files
- output labels and vocabulary
- shared branding assets

`shared/` should not become a dumping ground for raw knowledge or skill-specific content.

### `docs/`

Keep repository-level documentation here, especially:

- authoring guidance
- distribution guidance for each agent
- migration records
- testing guidance
- architecture notes

### `tests/`

Use root-level tests for things that span multiple skills or multiple distribution targets:

- install tests
- packaging tests
- integration tests
- cross-skill fixtures

## Future-Proofing Rules

The structure must support new skills without forcing a second reorganization.

### Rule 1: New skills enter as independent units

A new skill such as `video-combo-analysis` should begin life under `skills/video-combo-analysis/`.

It should not require moving old files around just to exist.

### Rule 2: Share late, not early

If a capability exists in only one skill, keep it in that skill.

Promote it into `packages/` or `shared/` only when:

- at least two skills need it, or
- agent-specific distribution tooling clearly benefits from centralization

### Rule 3: Public distribution and repo-local usage are different concerns

The source repo should primarily optimize for:

- clear authoring
- clear packaging
- clear installation paths for different agents

Repo-local dogfooding remains useful, but it must be implemented as a compatibility layer rather than as the canonical structure.

### Rule 4: Data-heavy skills need an explicit packaging boundary

Skills like `kb-sf6-frame-current` that depend on repository data must not remain vague about runtime inputs.

They need one of the following:

- packaged skill-local assets
- a documented build step that materializes runtime assets
- explicit classification as repo-local-only until packaging is solved

## Current Repository Mapping

Current to target mapping:

- `.agents/skills/kb-sf6-core` -> `skills/kb-sf6-core`
- `.agents/skills/kb-sf6-frame-current` -> `skills/kb-sf6-frame-current`
- `.agents/skills/sync-knowledge` -> `maintainer-skills/sync-knowledge`
- `.agents/automation-prompts` -> `docs/` or `scripts/` depending on actual usage
- `data/` stays outside public skills as source material or build input
- `ingest/` stays outside public skills as source tooling

## Agent Distribution Model

The repository should support multiple agent environments explicitly instead of assuming users will open the repo directly.

At minimum, maintain distribution guidance for:

- Codex
- Claude
- Cursor
- OpenCode

This follows the pattern used by established skill repositories where the repo is the source of truth and agent-specific installation instructions or metadata are maintained beside it.

## Migration Strategy

### Phase 1: Establish target boundaries

Create the high-level directories:

- `skills/`
- `maintainer-skills/`
- `packages/`
- `shared/`
- `docs/`
- `tests/`
- `scripts/`

Do not move everything immediately. First make the intended shape explicit.

Completion criteria:

- target structure exists
- README explains repository roles
- maintainers know which surface is public

### Phase 2: Pilot one simple public skill

Move `kb-sf6-core` first.

Why:

- low runtime dependency
- easy to package
- good reference for future skill layout

Completion criteria:

- `skills/kb-sf6-core/` is canonical
- packaging and validation assumptions are documented
- new skill template can imitate this layout

### Phase 3: Separate maintainer-only workflows

Move `sync-knowledge` into `maintainer-skills/`.

Completion criteria:

- public skill surface no longer contains maintainer-only flows
- maintainer docs point to the new location

### Phase 4: Add minimal distribution infrastructure

Introduce the smallest useful shared infrastructure:

- installer docs under `.codex/`, `.opencode/`, and plugin metadata directories
- packaging helper under `packages/skill-packaging`
- validator under `packages/skill-validator`

Completion criteria:

- the repo documents how a public skill gets distributed to at least one agent
- packaging responsibilities are no longer implicit

### Phase 5: Resolve data-heavy skill packaging

Investigate `kb-sf6-frame-current`.

Questions to answer:

- Can the required published exports be bundled into skill-local assets?
- Is a generated asset subset enough?
- Should this skill stay repo-local until packaging is defined?

Completion criteria:

- runtime dependency boundary is explicit
- the skill is classified as distributable or repo-local-only

### Phase 6: Introduce new-skill path

Once the first two skills are separated cleanly, document how a future skill such as `video-combo-analysis` enters the repo.

Completion criteria:

- `docs/authoring/` describes new-skill onboarding
- template files exist
- shared contracts are only added where justified

## Risks

### Risk: premature centralization

Moving too much into `shared/` or `packages/` too early will recreate coupling under a different name.

Mitigation:

- require at least two consumers before extracting shared pieces

### Risk: hidden runtime dependencies

A skill can appear distributable while actually depending on repo-local files.

Mitigation:

- require every skill to declare its runtime inputs clearly
- validate packaging outputs against those declared inputs

### Risk: maintaining two structures at once

Keeping both `skills/` and `.agents/skills/` indefinitely can create drift.

Mitigation:

- if dogfooding needs `.agents/skills/`, treat it as generated or mirrored
- never treat both as authoritative

## Recommended Decisions

1. Adopt `skills/` as the canonical source for distributed skills.
2. Adopt `maintainer-skills/` for repository-only workflows.
3. Keep each new skill independent by default.
4. Use `packages/` for shared executable logic and `shared/` for shared non-code artifacts.
5. Treat `.agents/skills/` as optional compatibility output, not as the source of truth.
6. Delay packaging decisions for `kb-sf6-frame-current` until its data boundary is documented.

## Open Questions

These questions should be resolved during implementation planning, not before approving this design:

- Whether repo-local dogfooding needs a generated `.agents/skills/` mirror
- Whether `kb-sf6-frame-current` can ship asset snapshots cleanly
- Which agent distributions are in scope for the first release wave
- Whether packaging outputs should be committed or release-generated only
