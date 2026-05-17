---
id: adr-0004
title: Retire Deferred Distribution Surfaces With Public Adapter Removal
status: accepted
date: 2026-05-17
decision_type: architecture_decision
scope: deferred_distribution_surfaces
tracking_issue: "#248"

selected_disposition: legacy_lane_until_public_adapter_removal_then_delete
legacy_distribution_lane: interim_only
retain_distribution_docs_long_term: false
retain_installers_long_term: false
retain_release_bundle_long_term: false
immediate_deletion: false

depends_on:
  - adr-0002
  - adr-0003

surfaces_to_keep_interim:
  - release_bundle_dist
  - skill_installers_package
  - distribution_docs

surfaces_to_delete_later:
  - release_bundle_dist
  - skill_installers_package
  - distribution_docs

markers:
  - sf6.boundary.deferred_distribution_legacy_lane_interim_only
  - sf6.boundary.deferred_distribution_surfaces_delete_after_adapter_removal
  - sf6.boundary.no_distribution_reactivation_in_adr
  - sf6.boundary.no_distribution_files_deleted_in_adr
---

# Retire Deferred Distribution Surfaces With Public Adapter Removal

## Decision

The selected disposition for `.dist`, installer tooling, and distribution docs
is **legacy lane until public adapter removal, then delete**.

This means:

- Keep `legacy-distribution` validation only as an interim guard while
  `skills/sf6-agent/` still exists.
- Do not treat `.dist`, installer scripts, or public install docs as long-term
  maintained product surfaces.
- Do not reactivate public distribution through installer or release-bundle
  work.
- Delete or retire these surfaces in the same sequence that removes the public
  adapter after reusable runtime payloads are relocated.

This ADR is design-only. It does not delete files, move files, rebuild generated
outputs, and does not change public `sf6-agent` behavior.

## Context

ADR-0002 deferred public `sf6-agent` distribution while private Hermes-first
operation is stabilized.

ADR-0003 selected `remove_after_runtime_relocation` for `skills/sf6-agent/`.
That decision makes the remaining public distribution surfaces transitional:

- `.dist/sf6-agent-bundle.zip`
- `packages/skill-installers/*`
- `packages/skill-packaging/build-release-bundle.ps1`
- `docs/distribution/*`

These surfaces currently help validate or explain the deferred public adapter,
but they should not survive as a separate long-term lane after the adapter is
removed.

## Options Considered

### Option A: Keep In Legacy Lane Long-Term

Keep `.dist`, installers, and distribution docs as a permanent
`legacy-distribution` lane.

Rejected. This would preserve a public distribution product surface after the
repository has already selected public adapter retirement.

### Option B: Delete Immediately

Delete `.dist`, installer tooling, release-bundle tooling, and distribution docs
now.

Rejected for this step. Runtime payloads still live under `skills/sf6-agent/`,
and existing validators use the bundle as a boundary check. Immediate deletion
would mix the decision with implementation and runtime relocation work.

### Option C: Keep Interim, Delete With Adapter Removal

Keep the current distribution surfaces only as interim legacy-lane checks until
runtime payloads move and the public adapter is removed.

Accepted. This keeps validation coverage during transition while preventing the
legacy lane from becoming a permanent product surface.

## Interim State

Until the public adapter is removed:

- `.dist/sf6-agent-bundle.zip` remains generated and untracked.
- `packages/skill-packaging/build-release-bundle.ps1` may remain as the
  legacy-distribution preflight generator.
- `packages/skill-installers/*` may remain only for deferred public adapter
  install coverage.
- `docs/distribution/*` may remain only as deferred public distribution docs.
- `tests/validation/validate-distribution.ps1` may remain in the
  `legacy-distribution` lane.

These files must not become normal private-operation dependencies.

## Retirement Conditions

The follow-up removal PR may delete or archive the distribution surfaces after:

- `runtime/frame-current/` exists or the frame-current runtime migration has an
  accepted alternative.
- `runtime/generated-knowledge/` exists or generated concept runtime migration
  has an accepted alternative.
- `runtime/normalization/` is either created or explicitly deferred / removed.
- `skills/sf6-agent/` removal has a scoped PR plan.

When deletion happens, update:

- `data/repository-surfaces.json`
- `tests/validation/run-all.ps1`
- `tests/validation/validate-distribution.ps1`
- `packages/skill-packaging/`
- `packages/skill-installers/`
- `docs/distribution/`
- README / architecture docs

## Non-Goals

- This ADR does not delete `.dist`, installer scripts, distribution docs,
  release-bundle tooling, or `skills/sf6-agent/`.
- This ADR does not move generated references, frame-current assets, or
  normalization assets.
- This ADR does not rebuild generated outputs.
- This ADR does not change current facts, `official_raw`, `data/exports`,
  `data/roster`, `knowledge/curated`, or public `sf6-agent` behavior.
- This ADR does not commit Hermes memory, sessions, local skills, raw
  transcripts, logs, caches, credentials, or secrets.
