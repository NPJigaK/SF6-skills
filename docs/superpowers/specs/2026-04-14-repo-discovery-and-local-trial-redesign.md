# Repo Discovery And Local Trial Redesign

## Goal

Realign repository structure around a single tracked public skill source at `skills/`, remove the tracked repo-root `.agents/skills/` mirror, and establish `local/` as the personal trial workspace for trying distributed skills in a way that matches actual Codex usage more closely.

## Confirmed Repo Facts

- `skills/` is the canonical public source for distributable skills.
- `maintainer-skills/` is for shared repository-only workflows.
- `local/` is ignored maintainer-private scratch space and is not a canonical source surface.
- The current repo still treats root `.agents/skills/` as an exact tracked mirror of `skills/`.
- The current root `.agents/skills/` mirror is maintained by `scripts/dev/sync-dogfood-skills.ps1` and enforced by `tests/install/validate-dogfood-mirror.ps1`.
- The current install/distribution flow targets `~/.agents/skills/sf6-skills`.
- The user's actual personal trial workflow uses `E:/github/SF6-skills/local` as the workspace root when invoking Codex.
- `obra/superpowers` uses `skills/` as tracked source and connects Codex discovery through a user-environment symlink or junction under `~/.agents/skills/`.

## Problem

The repo currently mixes two separate concerns:

1. tracked source authoring
2. repo-local discovery compatibility

That creates avoidable friction:

- root `.agents/skills/` cannot safely host repo-development-only skills because the mirror sync removes extras
- validators and docs treat a tracked mirror as a structural contract even though it is derived
- the repo-root dogfood setup does not match the user's actual personal trial workspace under `local/`

## Decision

Adopt a source/discovery split closer to `obra/superpowers`.

### Tracked Source

- `skills/` remains the only tracked public skill source.
- `maintainer-skills/` remains the tracked surface for shared repo-only workflows.
- `local/` becomes the tracked skeleton for a personal trial workspace, but not a shared source surface.

### Discovery Surfaces

- Remove the tracked repo-root `.agents/skills/` mirror.
- Stop treating root `.agents/skills/` as a repository contract surface.
- Keep distribution/install support for the Codex discovery target `~/.agents/skills/sf6-skills`, but implement it as a thin install-time adapter such as a symlink or junction to the checked-out repo `skills/` directory.
- Use `local/` as the place for repo-adjacent personal trial discovery and generated artifacts.

## Desired Repository Roles

### Repo Root

- author public skills under `skills/`
- author shared repo-only workflows under `maintainer-skills/`
- document installation and distribution
- validate high-value repository boundaries only

### `local/`

- personal trial workspace for distributed skills
- may contain a tracked minimal skeleton:
  - `local/AGENTS.md`
  - `local/.codex/`
  - `local/.agents/`
- may contain ignored generated subtrees for downloaded media, transcripts, outputs, local junctions, and personal notes
- must not become a canonical source or shared maintainer workflow surface

### User-Environment Discovery

- install docs should describe a `superpowers`-style flow:
  - clone or place the repo checkout
  - link `~/.agents/skills/sf6-skills` to `<checkout>/skills`
  - restart Codex

## Migration Scope

### Remove

- root `.agents/skills/`
- root `.agents/AGENTS.md`
- `scripts/dev/sync-dogfood-skills.ps1`
- `tests/install/validate-dogfood-mirror.ps1`
- validators that require repo-root `.agents/skills/` inventory parity
- docs that describe the tracked mirror as a repo-local contract

### Add Or Change

- update root docs and validators so `.agents/skills/` is no longer a tracked repo contract surface
- add tracked `local/` skeleton files for personal trial usage
- define how `local` root should guide Codex toward public skills and local-only experimentation
- update installer docs and scripts to prefer source-plus-link behavior over copying mirrored trees
- keep raw inputs, generated outputs, and personal experimental skills inside ignored paths under `local/`

## Local Trial Design

The `local` workspace should support this workflow:

1. open Codex with `E:/github/SF6-skills/local` as the root
2. use local guidance that points Codex at the public skills from the parent repo
3. optionally create or refresh a local discovery link under `local/.agents/skills/`
4. run personal experiments, including YouTube-download-driven video analysis
5. keep generated media and outputs ignored

This workspace is intentionally personal-first. It is for trying the distributed skills, not for defining public contracts.

## Non-Goals

- do not move public source out of `skills/`
- do not add another generic shared framework
- do not turn `local/` into a public distribution surface
- do not keep a second tracked mirror of public skills inside the repo

## Validation Strategy

- keep existing high-value validators for layout, public skill boundaries, distribution surface, maintainer surface, and public skill location
- replace mirror-specific validation with checks that ensure no tracked repo-root `.agents/skills/` mirror remains
- verify docs no longer claim repo-root `.agents/skills/` is an exact tracked mirror
- verify `local/` skeleton exists and remains compatible with the personal trial workflow

## Risks And Mitigations

### Risk: install docs drift from Codex discovery behavior

Mitigation:
- keep install docs explicit and narrow
- use a simple junction or symlink pattern rather than a copied mirror

### Risk: `local/` becomes a dumping ground

Mitigation:
- keep only a small tracked skeleton
- ignore generated trees
- document `local/` as personal trial workspace, not shared source

### Risk: removing the root mirror breaks existing repo-local habits

Mitigation:
- document the new local trial workflow clearly
- keep distribution install instructions aligned with the same source/discovery split
