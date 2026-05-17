---
id: adr-0005
title: Raw Snapshot Retention Boundary
status: accepted
date: 2026-05-18
decision_type: architecture_decision
scope: raw_snapshot_retention
tracking_issue: "#258"

selected_retention_model: current_published_manifest_minimal_git_set
git_tracked_raw_snapshot_role: minimal_reproducibility_artifact
repo_external_raw_cache_role: future_metadata_reference_only
retention_exception_artifact: required_for_unreferenced_git_raw_retention
normal_public_answer_authority: false
immediate_data_change: false

depends_on:
  - raw_snapshot_minimality_validator
  - current_fact_export_manifest_contract
  - manual_review_debt_index

markers:
  - sf6.boundary.raw_snapshots_git_tracked_minimal_reproducibility
  - sf6.boundary.unreferenced_raw_snapshots_removable_without_exception
  - sf6.boundary.repo_external_raw_cache_metadata_only
  - sf6.boundary.raw_snapshots_not_public_answer_authority
  - sf6.boundary.no_raw_snapshot_data_change_in_adr
---

# Raw Snapshot Retention Boundary

## Decision

Use **current published manifest minimal Git set** as the raw snapshot retention
model.

This means:

- Git-tracked `data/raw/` snapshots are retained only as the minimal
  reproducibility input for the current published exports in `data/exports/`.
- `data/exports/<character_slug>/snapshot_manifest.json` is the reviewed keep
  set source for checked-in raw snapshot directories.
- A tracked raw snapshot directory that is not referenced by the current
  published manifests is removable residue unless a later reviewed
  retention-exception artifact explicitly allows it.
- Future repo-external raw caches may be used only as maintainer-local or
  repo-external storage. The repository may commit sanitized metadata, content
  hashes, or source references for those caches only after a later reviewed
  issue defines the artifact shape.
- Raw snapshots are not normal public answer authority.

In short, Git keeps the minimum raw input needed to reproduce the current
published export surface. Anything broader belongs outside the repo unless a
reviewed exception artifact says otherwise.

This ADR is design-only. It does not add, delete, refetch, rewrite, normalize,
or re-hash raw snapshots. It does not change current facts, exports, roster
data, generated runtime assets, normalized runs, manual-review sidecars, or
public adapter behavior.

Design-only guard: this ADR does not add, delete, refetch, rewrite, normalize, or re-hash raw snapshots.

## Context

The frame-data ingestion pipeline writes raw snapshots before parsing. The raw
byte payload plus `metadata.json` is the reproducibility input for current
published exports, while decoded HTML and normalized rows are derived from those
snapshots.

The repository already has:

- `data/exports/<character_slug>/snapshot_manifest.json` as the current
  published provenance surface.
- `tests/validation/validate-raw-snapshot-minimality.ps1` to verify every
  checked-in raw snapshot directory is referenced by the current published
  manifests.
- `data/exports/_index/manual-review-debt.json` to expose withheld row debt
  without promoting manual-review rows to normal public answer authority.

The missing repository-level decision was whether raw snapshots should become a
historical archive, an external cache reference surface, or a minimal
reproducibility surface.

## Options Considered

### Option A: Keep All Historical Raw Snapshots In Git

Keep every fetched raw snapshot as checked-in history.

Rejected. This turns `data/raw/` into a growing historical archive and weakens
the current published manifest boundary. It also makes future patch refreshes
carry unrelated raw residue unless every old snapshot receives a separate
retention justification.

### Option B: Keep No Raw Snapshots In Git

Remove checked-in raw snapshots and rely on refetching or external caches.

Rejected for the current repository. The published export surface would lose its
reviewable reproduction input. Missing source pages or upstream changes would
make current checked-in exports harder to audit.

### Option C: Keep Only Current Published Manifest References

Keep only the raw snapshot directories referenced by current published
`snapshot_manifest.json` files.

Accepted. This is the existing validator model and matches the current
reproducibility need without making Git the long-term raw archive.

## Retention Rules

Git-tracked raw snapshots:

- must live under `data/raw/official/<character_slug>/<snapshot_id>/` or
  `data/raw/supercombo/<character_slug>/<snapshot_id>/`;
- must contain the expected snapshot payload and metadata files for the ingest
  source;
- must be referenced by an `available` dataset in the current published
  manifest keep set;
- are reproducibility artifacts only;
- are not normal public answer authority.

Unreferenced checked-in raw snapshots:

- are removable residue by default;
- must not be kept for historical curiosity alone;
- may be retained only if a later reviewed retention-exception artifact defines
  the exception id, source, reason, review owner, expiry or review date, and
  validation expectations.

Missing referenced raw snapshots:

- break current export reproducibility;
- must be restored, regenerated through the ingest workflow, or resolved by
  republishing the affected dataset before broad validation is claimed.

## Repo-External Cache Boundary

Future raw cache or raw-history work must use a repo-external location by
default, such as a maintainer-local cache root under `$XDG_CACHE_HOME` or another
reviewed external storage mechanism.

Repo-external raw cache references, if introduced later, may commit only
sanitized metadata such as:

- source id;
- source URL or reviewed source reference;
- content hash;
- byte size;
- acquisition time;
- cache policy;
- review status;
- intentionally non-local storage locator or opaque external reference.

They must not commit:

- raw cache payloads outside the minimal manifest keep set;
- local absolute cache paths;
- browser cache state;
- credentials, tokens, sessions, or cookies;
- Hermes memory, raw transcripts, logs, local skills, Curator state, or
  checkpoints.

This ADR does not implement repo-external cache sync. A later issue must define
the artifact contract and validators before any raw cache/hash reference surface
is introduced.

## Validation

The current strict validator remains:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-raw-snapshot-minimality.ps1
```

The validator must continue to fail when:

- a referenced raw snapshot directory is missing;
- a tracked raw snapshot directory is not referenced by current published
  manifests;
- a tracked raw file uses an unexpected layout.

If a retention-exception artifact is introduced later, that PR must update this
ADR or add a follow-up ADR, update the validator, and make the exception
machine-reviewable.

## Non-Goals

- This ADR does not add, remove, refetch, rewrite, normalize, or re-hash raw
  snapshots.
- This ADR does not implement repo-external raw cache sync or cache manifests.
- This ADR does not change `data/exports`, `data/roster`, `data/normalized`,
  generated runtime assets, manual-review sidecars, or public adapter behavior.
- This ADR does not make `data/raw/` normal public answer authority.
- This ADR does not commit local cache paths, raw media, browser state, Hermes
  memory, sessions, raw transcripts, logs, credentials, secrets, or tokens.
