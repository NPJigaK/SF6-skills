# Repo Structure Contract

## Design Goal

This repository prefers simple, explicit structure over flexible but harder-to-reason-about abstractions.

The structure contract exists to keep three things true:

- a new skill can be understood by reading its own directory first
- shared infrastructure appears only after real duplication exists
- public source, maintainer-only workflows, and derived surfaces do not get mixed together

## Top-Level Principles

- simplicity first
  - if a directory rule cannot be explained in a few sentences, the rule is too complex
- independent skill first
  - `skills/<skill-name>/` is the primary unit of authoring and future distribution
- shared later
  - move something to `packages/` or `shared/` only after a second real consumer exists
- one-way dependencies
  - skills may depend on `packages/` or `shared/` when needed
  - skills must not depend on other skills
  - `packages/` and `shared/` must not depend on a specific skill directory
- derived surfaces are never source
  - repo-local mirrors, release bundles, and generated packaged assets are outputs, not canonical source
- local validator first
  - repository contract checks live in local PowerShell validators first
  - CI may call the same validators later, but CI is not the canonical contract layer

## Top-Level Directory Contract

### `skills/`

- canonical public source for distributable skills
- contains independent public units at `skills/<skill-name>/`
- must not contain maintainer-only workflows or repo-local mirrors

### `maintainer-skills/`

- repository-only skill workflows
- not part of the public distribution unit
- used for curation, sync, review, and other maintainer tasks

### `.agents/skills/`

- exact top-level mirror of `skills/` for repo-local dogfooding
- derived from `skills/`
- must not be treated as canonical source

### `packages/`

- shared executable infrastructure
- examples: packaging, installers, validators
- do not move skill-specific logic here until at least two skills need the same contract

### `shared/`

- shared non-code artifacts
- examples: templates, schemas, stable vocabulary
- use only after shared demand is real

### `docs/`

- repository contract, authoring, architecture, distribution, and testing documentation
- documents the structure contract, but is not itself a skill source surface

### `ingest/`

- data production and publishing implementation
- scraping, normalization, and publishing logic stays here
- skill directories must not contain ingestion code

### `data/`

- published exports and minimal backing raw snapshots
- supports current-fact workflows
- not itself a skill authoring surface

### `tests/`

- minimal repository contract validators
- preferred location for layout, distribution, packaging, and boundary checks
- tests should stay small and only protect high-value invariants

### `scripts/`

- repository maintenance helpers
- convenience layer only, not source of truth

### Agent Entry Surfaces

- `.codex/`
- `.opencode/`
- `.claude-plugin/`
- `.cursor-plugin/`

These directories exist as install and onboarding front doors.
They are never the canonical source of a skill.

## Public Skill Unit Contract

The public unit is `skills/<skill-name>/`.

The directory must be understandable on its own and must stay thin enough to copy, bundle, and install as a standalone unit.

### Required

- `SKILL.md`

### Optional

- `references/`
  - stable supporting knowledge for the skill
- `assets/`
  - distributable runtime artifacts that are safe to check in
- `agents/`
  - agent-specific metadata such as `openai.yaml`

### Not Allowed By Default

- dependencies on another skill directory
- ingestion or scraping implementations
- maintainer-only editorial workflows
- raw snapshots or review-only artifacts
- installer or bundle machinery

## Shared Extraction Rule

Keep an artifact inside a skill when only that skill needs it.

Promote it only when the second real consumer appears:

- executable or code-like reuse goes to `packages/`
- non-code reuse goes to `shared/`

This repository intentionally avoids pre-emptive abstraction.

## Derived Surface Contract

### Repo-Local Dogfooding

- `.agents/skills/` is an exact top-level mirror of `skills/`
- it exists for local usage only
- sync should remove stale extra directories

### Runtime Packaged Assets

- packaged runtime assets inside a skill are derived outputs
- they may exist when the skill needs distributable static data
- they must be generated from repo-level canonical source, never treated as the canonical source themselves

### Release Bundles

- release bundles are derived distribution artifacts
- they are built from canonical source under `skills/`
- they must not redefine repository structure rules

## Dependency Boundaries

- `skills/<skill-name>/` may read from its own files
- `skills/<skill-name>/` may use `packages/` or `shared/` only when shared demand is proven
- `skills/<skill-name>/` must not import or read another skill as a dependency
- `packages/` must stay skill-agnostic
- `shared/` must stay skill-agnostic
- `.agents/skills/` must not become a hand-maintained parallel tree

## Validator Policy

This repository keeps only the minimum validator set needed to protect structure:

- layout contract
- public skill dependency boundary checks
- public skill location and mirror integrity
- distribution surface boundary checks
- release bundle boundary checks
- packaged runtime asset boundary checks where a skill needs packaged data

The repository does not aim to exhaustively test every wording detail of every skill.
Tests should exist only when a broken boundary would cause real confusion or bad distribution behavior.

## Authoring Consequences

When adding a new public skill:

1. create `skills/<skill-name>/`
2. add `SKILL.md`
3. add `references/`, `assets/`, or `agents/` only if the skill actually needs them
4. keep skill-specific artifacts local to that skill
5. extract to `packages/` or `shared/` only after duplication becomes real

For example, a future video-analysis skill should be introduced as another independent unit under `skills/`.
It should not require restructuring the repo or introducing a skill-to-skill dependency.

## Non-Goals

- building a highly generic plugin platform inside this repository
- forcing every skill to have the same optional subdirectories
- moving all possible reuse into shared layers before it is needed
- making CI the primary contract surface before the local contract is stable
