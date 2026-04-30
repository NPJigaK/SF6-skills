# Root AGENTS To Public Skill Guidance Redesign

## Goal

Realign instruction surfaces so repository-root `AGENTS.md` is maintainer-facing repo guidance only, while user-facing runtime behavior and answer policy live inside each distributed public skill under `skills/`.

## Confirmed Repo Facts

- Root `AGENTS.md` currently mixes repo structure guidance with user-facing answer policy such as response labels, source tiers, and current-fact lookup rules.
- `README.md` defines `skills/` as the canonical public source for distributed skills.
- `skills/README.md` defines each direct child under `skills/` as an independent public skill unit.
- Public skills already hold substantial runtime behavior in their own `SKILL.md` files:
  - `skills/kb-sf6-core/SKILL.md`
  - `skills/kb-sf6-frame-current/SKILL.md`
  - `skills/video-analysis-core/SKILL.md`
- `tests/packaging/validate-doc-links.ps1` still treats root `AGENTS.md` as the place where public-skill guidance must appear.
- The local `superpowers` distribution model exposes `skills/` to Codex discovery, and the runtime unit is each skill directory, not a library-wide `AGENTS.md`.

## Problem

The current layout mixes two different responsibilities in one file:

1. maintainer-facing repo guidance
2. user-facing distributed skill behavior

That mismatch creates unnecessary coupling:

- root `AGENTS.md` looks like a repo-development entry surface, but it contains runtime answer policy for end-user tasks
- validators enforce public behavior in the wrong place
- public skills appear less self-contained than they actually are
- the repo structure contract says `skills/` is the public source, but the most important answer policy still lives at the repo root

## Options Considered

### Option A: Move public behavior into each skill and shrink root `AGENTS.md`

- matches the public unit boundary at `skills/<skill-name>/`
- aligns with the `superpowers` distribution model and common skill packaging guidance
- keeps each skill self-describing at runtime
- requires some intentional duplication across skills where policies overlap

### Option B: Add `skills/AGENTS.md` as a shared public entrypoint

- keeps one shared user-facing instruction file
- still moves behavior out of root
- but introduces a library-wide runtime surface that is outside the portable skill unit
- weaker fit for skill packaging and future standalone distribution

### Option C: Keep root `AGENTS.md` and only rewrite its wording

- smallest edit
- but preserves the structural mismatch between repo root and public runtime surface
- does not align validators or documentation with the actual public unit

## Decision

Adopt Option A.

- Root `AGENTS.md` becomes maintainer-facing repo guidance only.
- User-facing answer policy moves into the relevant public skills.
- `skills/README.md` remains a human-facing overview of the public source surface, not a runtime instruction layer.
- Validators should check public behavior where it now lives: in the affected skill directories.

## Guidance Mapping

### Keep At Root `AGENTS.md`

- repository purpose and structure guidance needed by contributors
- source-of-truth notes for maintainers such as:
  - `skills/` is the canonical public source
  - `local/` is the personal trial workspace
  - published data responsibilities and repo-level layout boundaries
- maintainer workflow routing such as:
  - use `maintainer-skills/sync-knowledge/` for knowledge integration
  - use `maintainer-skills/update-frame-data/` for patch-driven frame-data updates

### Move To `skills/kb-sf6-core/`

- `[概念のみ]` as the default label for concept answers
- concept-first answer shape
- explicit prohibition on treating community terms as official definitions
- the boundary that concept answers do not assert current fact or exact current values

Preferred placement:

- keep the high-signal behavior in `skills/kb-sf6-core/SKILL.md`
- keep any expanded rationale in `skills/kb-sf6-core/references/SOURCE_POLICY.md`

### Move To `skills/kb-sf6-frame-current/`

- `[検証済み]` and `[保留]` runtime label policy for published current-fact answers
- source-tier handling for current facts
- the rule that current-fact lookup starts from `snapshot_manifest.json`
- the rule that only `publication_state = available` datasets are valid
- the rule that packaged published exports are the final runtime surface

Preferred placement:

- keep answer-path rules in `skills/kb-sf6-frame-current/SKILL.md`
- keep deeper file-role and fallback detail in `references/export-contract.md`
- add a local reference file only if the existing export contract cannot hold the moved policy cleanly

### Keep Inside `skills/video-analysis-core/`

- observation-first surface
- 60fps normalized canonical timeline
- prohibition on exact current-fact lookup and verdict-heavy interpretation

This skill already carries the correct runtime boundary and likely needs only minor wording alignment.

## Detailed File Changes

### Modify

- `AGENTS.md`
- `skills/kb-sf6-core/SKILL.md`
- `skills/kb-sf6-core/references/SOURCE_POLICY.md`
- `skills/kb-sf6-frame-current/SKILL.md`
- `skills/kb-sf6-frame-current/references/export-contract.md`
- `skills/video-analysis-core/SKILL.md`
- `skills/README.md`
- `tests/packaging/validate-doc-links.ps1`

### Optional Additions

- `skills/kb-sf6-frame-current/references/SOURCE_POLICY.md`

Only add this file if `references/export-contract.md` becomes overloaded by answer-policy content. Prefer keeping one clear local reference rather than forcing too much detail into `SKILL.md`.

## Root `AGENTS.md` Target Shape

The root file should read like a maintainer contract, not a runtime answer guide.

It should:

- describe repo purpose and durable source surfaces
- define repo-level source boundaries and publication responsibilities
- route maintainers to the correct public or maintainer skill directories
- avoid response templates and user-facing answer labels
- avoid presenting itself as the canonical runtime instruction surface for distributed skills

It should not include:

- `## 回答ラベル`
- user-facing response templates
- concept-answer output format blocks
- direct end-user current-fact answer procedures that belong to distributed skills

## Skill-Level Design Rules

- Keep each public skill self-contained enough to function when distributed independently.
- Do not create skill-to-skill dependencies just to centralize wording.
- Allow small, intentional duplication where the same label or boundary must be visible inside more than one public skill.
- Keep high-frequency runtime guidance in `SKILL.md`.
- Move detailed explanations to one-level-deep local references when needed.

## Validation Strategy

### Documentation Validator

Update `tests/packaging/validate-doc-links.ps1` so it checks:

- root `AGENTS.md` no longer contains `## 回答ラベル`
- root `AGENTS.md` no longer contains `[検証済み]`
- root `AGENTS.md` no longer contains `[概念のみ]`
- root `AGENTS.md` no longer contains `[保留]`
- `skills/kb-sf6-core/SKILL.md` contains `[概念のみ]`
- `skills/kb-sf6-frame-current/SKILL.md` contains `[検証済み]`
- `skills/kb-sf6-frame-current/SKILL.md` contains `[保留]`
- `skills/kb-sf6-frame-current/SKILL.md` still points to `snapshot_manifest.json`
- `skills/README.md` still states that `skills/` is the canonical public source

### Manual Review

Perform one explicit read-through after edits to confirm:

- root `AGENTS.md` still gives maintainers enough repo context
- no current-fact runtime policy remains stranded only at root
- no skill now depends on another skill directory for core answer behavior
- wording across the three public skills is mutually consistent

## Non-Goals

- do not introduce `skills/AGENTS.md` as a new runtime contract layer
- do not remove root `AGENTS.md` entirely
- do not move published exports or packaged runtime assets
- do not change data-production code or current publication semantics
- do not turn `skills/README.md` into a second runtime instruction surface

## Risks And Mitigations

### Risk: policy duplication drifts across skills

Mitigation:

- keep duplicated policy minimal
- place deeper rationale in each skill's local references
- protect the moved phrases with a narrow validator

### Risk: root guidance becomes too thin for maintainers

Mitigation:

- keep repo-purpose, source-boundary, and workflow-routing content at root
- make the root file explicitly maintainer-oriented rather than merely shorter

### Risk: an agent opened at repo root misses critical SF6 answer policy

Mitigation:

- public behavior remains inside the skills that should trigger for those tasks
- root guidance can point contributors to the relevant skill directories without restating their full runtime behavior

### Risk: `kb-sf6-frame-current` becomes too dense

Mitigation:

- keep only answer-path essentials in `SKILL.md`
- move expanded wording into a single local reference file if needed
