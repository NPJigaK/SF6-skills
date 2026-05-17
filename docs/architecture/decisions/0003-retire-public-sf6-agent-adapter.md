---
id: adr-0003
title: Retire Public sf6-agent Adapter After Runtime Surface Relocation
status: accepted
date: 2026-05-17
decision_type: architecture_decision
scope: public_adapter_disposition
tracking_issue: "#246"

selected_disposition: remove_after_runtime_relocation
reactivate_public_distribution: false
immediate_deletion: false

depends_on:
  - adr-0002
  - frame-current-runtime-separation-plan
  - generated-reference-responsibility-plan

runtime_surfaces_to_relocate_first:
  - generated_knowledge_references
  - frame_current_runtime_assets
  - normalization_runtime_assets

surfaces_to_retire_later:
  - sf6_agent_public_adapter
  - sf6_agent_adapter_policy_references
  - release_bundle_dist
  - skill_installers_package

markers:
  - sf6.boundary.public_adapter_remove_after_runtime_relocation
  - sf6.boundary.public_adapter_not_reactivated
  - sf6.boundary.runtime_payloads_must_move_before_adapter_removal
  - sf6.boundary.no_public_adapter_behavior_change_in_adr
---

# Retire Public sf6-agent Adapter After Runtime Surface Relocation

## Decision

The selected disposition for `skills/sf6-agent/` is **remove after runtime
surface relocation**.

This means:

- Do not reactivate public `sf6-agent` distribution in v2.6.
- Do not relocate the whole `skills/sf6-agent/` adapter as another public skill
  package.
- First move reusable generated runtime payloads out of the deferred adapter
  path.
- Then retire and remove the remaining public adapter, installer, and release
  distribution surfaces through scoped PRs.

In short, the decision is: remove after runtime surface relocation.

This ADR is design-only. It does not delete files, move files, rebuild generated
outputs, or change public `sf6-agent` behavior.

## Context

ADR-0002 set the current priority to private Hermes-first operation and marked
public `skills/sf6-agent/` distribution as a deferred legacy surface with no
known external public-skill users.

Two Phase 2 mapping documents now separate the reusable runtime responsibilities
from the public adapter path:

- `docs/architecture/frame-current-runtime-separation-plan.md` maps
  `frame_current_runtime_assets` and proposes `runtime/frame-current/`.
- `docs/architecture/generated-reference-responsibility-plan.md` maps
  `generated_knowledge_references` and `sf6_agent_adapter_policy_references`,
  and proposes `runtime/generated-knowledge/`.

The remaining question is whether the public adapter itself should be removed,
relocated, or reactivated.

## Options Considered

### Option A: Reactivate

Reactivate public `skills/sf6-agent/` distribution as an active product surface.

Rejected for v2.6. The current repository focus is private Hermes-first
knowledge growth and maintainer operation. Reactivating public distribution now
would keep adapter behavior, runtime payloads, release bundle docs, installers,
and maintainer workflows active at the same time.

### Option B: Relocate Whole Adapter

Move `skills/sf6-agent/` to another public adapter path while preserving the
same product concept.

Rejected for v2.6. Relocating the whole adapter preserves most of the same
maintenance burden and does not match the current private-operation priority.
Only reusable runtime payloads should be relocated.

### Option C: Remove After Runtime Relocation

Move reusable generated runtime payloads to repo-local runtime surfaces, keep
temporary compatibility copies only when needed, then remove the remaining
public adapter surface.

Accepted. This keeps useful generated payloads while removing the public skill
distribution layer that is not the active product focus.

## Target State

Long-term target:

```text
knowledge/curated/
  -> runtime/generated-knowledge/

data/exports/
data/roster/
  -> runtime/frame-current/

data/aliases/
  -> runtime/normalization/
```

`skills/sf6-agent/` should not remain the primary home for generated runtime
payloads. If temporary compatibility copies are needed during migration, they
must be documented as deferred legacy bridge outputs, not authority.

`skills/sf6-agent/references/*-policy.md` is adapter behavior policy only. It
is not canonical SF6 knowledge. If the adapter is removed, these files should be
deleted or archived as historical design context, not promoted into
`knowledge/curated/`.

## Transition Order

1. Add this ADR and validators. No files move in this step.
2. Decide `.dist`, installer, and distribution docs handling.
3. Classify `packages/*` as active repo-local, deferred distribution, legacy, or
   shared infrastructure.
4. Relocate generated runtime payloads:
   - `runtime/frame-current/`
   - `runtime/generated-knowledge/`
   - `runtime/normalization/` if normalization runtime assets remain useful.
5. Add bridge validators only if compatibility copies remain under
   `skills/sf6-agent/`.
6. Remove or archive the remaining `skills/sf6-agent/` adapter surface.

## Consequences

- Future PRs should not add public adapter features to `skills/sf6-agent/`.
- Public distribution work requires a new ADR that explicitly reopens that
  product direction.
- Runtime payload migration can proceed without treating the public adapter as
  the primary product surface.
- Maintainer workflows remain under `workflows/`, `docs/architecture/`,
  `contracts/`, `tests/validation/`, and repo-local Hermes support.

## Non-Goals

- This ADR does not delete `skills/sf6-agent/`.
- This ADR does not move generated references, frame-current assets, or
  normalization assets.
- This ADR does not rebuild generated outputs.
- This ADR does not change current facts, `official_raw`, `data/exports/`,
  `data/roster/`, `knowledge/curated/`, or `.dist`.
- This ADR does not change public `sf6-agent` behavior.
- This ADR does not commit Hermes memory, sessions, local skills, raw
  transcripts, logs, caches, credentials, or secrets.
