# SF6 Frame Data Ingestion v3

`ingest/frame_data` is the v3 ingestion package for Street Fighter 6 frame data.
It keeps scraping/runtime code under `ingest/frame_data/` and does not place fetch code under `.agents/skills/`.

The checked-in current artifact surface is:

- v3 code
- v3 published exports under `data/exports/<character_slug>/`
- the minimal raw snapshots under `data/raw/` needed to reproduce those published exports

`data/normalized/` is run-local audit state and is not part of the durable checked-in artifact surface.

Configured character roster lives in `data/roster/current-character-roster.json`.
`official` is required for every roster character.
The current roster also configures `supercombo` for every checked-in character through `sources.supercombo_data`.

## Contracts

- `official_raw` is canonical.
- `derived_metrics` is recomputed only from `official_raw`.
- `supercombo_enrichment` is reduced-contract enrichment only.
- Published main exports are safe-only.
- Published `supercombo_enrichment` main is an authoritative-`official_raw` safe-subset only.
- Published `*_manual_review.{json,csv}` sidecars hold every row withheld from main, including anchor-missing `supercombo` rows.
- `snapshot_manifest.json` dataset entries are the authoritative published provenance surface.

## Fetch Strategy

- `official`: Scrapling `Fetcher`
- `supercombo`: Scrapling `StealthyFetcher` against the per-character `sources.supercombo_data` URL from `data/roster/current-character-roster.json`
- raw snapshot first: fetch writes the authoritative byte payload plus `metadata.json` before parse
- parser input is deterministically decoded from the stored raw bytes

The authoritative raw artifact is the on-disk response byte payload. Any decoded HTML text is derived from those bytes and is not the source of truth.

## Raw Snapshot Minimality

Checked-in raw snapshots are a reproducibility surface only. They are not
public-answer evidence and they are not a place to retain historical audit
state by default.

The minimum checked-in raw set is derived from
`data/exports/<character_slug>/snapshot_manifest.json`:

- `official_raw` keeps `data/raw/official/<character_slug>/<snapshot_id>/`
- `derived_metrics` keeps `data/raw/official/<character_slug>/<snapshot_id>/`
- `supercombo_enrichment` keeps `data/raw/supercombo/<character_slug>/<snapshot_id>/`

Only datasets with `publication_state = available` contribute
`published_snapshot_ids` to the keep set. A tracked raw snapshot directory that
is not referenced by the current published manifests is removable residue unless
a future reviewed retention-exception artifact explicitly allows it. This repo
currently has no raw snapshot retention exceptions.

ADR-0005 fixes this as the repository retention model:
`docs/architecture/decisions/0005-raw-snapshot-retention.md`. Checked-in raw
snapshots are the minimal Git-tracked reproducibility set for current published
exports. Broader raw-history or raw-cache work must stay repo-external by
default and may commit only reviewed metadata/hash references after a later
artifact contract is defined.

Validate the checked-in surface from the repo root:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-raw-snapshot-minimality.ps1
```

## Source Selection

- `official` is the canonical source for current published frame data
- `supercombo` is enrichment-only and may be `unavailable` if it cannot be safely published under the current v3 path
- `--source all` means all configured sources for the selected character
- `/JP/Frame_data` is dropped in v3 and is not part of runtime ingestion

## Setup

Core-only install:

```powershell
cd ingest/frame_data
python -m pip install -e .[dev]
```

Fetch-capable install:

```powershell
cd ingest/frame_data
python -m pip install -e .[fetch,dev]
```

Known-good Python target is `3.13+`.

## Commands

Fetch raw snapshots:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli fetch --character luke --source all
```

Parse from saved raw snapshots:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli parse-from-raw --character luke --source all --official-snapshot-id <official_snapshot_id> --supercombo-snapshot-id <supercombo_snapshot_id>
```

Publish a normalized run:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli publish --character luke --run-id <run_id>
```

End-to-end run:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli run --character luke --source all
```

Prune to latest published state only:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli prune --character luke --dry-run
python -m sf6_ingest.cli prune --character luke --apply
```

## Data Layout

Raw snapshots:

- `data/raw/official/jp/<snapshot_id>/page.html`
- `data/raw/official/jp/<snapshot_id>/metadata.json`
- `data/raw/supercombo/jp/<snapshot_id>/page.html`
- `data/raw/supercombo/jp/<snapshot_id>/metadata.json`
- `data/raw/official/<character_slug>/<snapshot_id>/page.html`
- `data/raw/official/<character_slug>/<snapshot_id>/metadata.json`
- `data/raw/supercombo/<character_slug>/<snapshot_id>/page.html`
- `data/raw/supercombo/<character_slug>/<snapshot_id>/metadata.json`

Normalized runs:

- `data/normalized/jp/<run_id>/run_manifest.json`
- `data/normalized/jp/<run_id>/official_raw/records.{json,csv}`
- `data/normalized/jp/<run_id>/supercombo_enrichment/records.{json,csv}`
- `data/normalized/jp/<run_id>/derived_metrics/records.{json,csv}`
- `data/normalized/<character_slug>/<run_id>/run_manifest.json`
- `data/normalized/<character_slug>/<run_id>/official_raw/records.{json,csv}`
- `data/normalized/<character_slug>/<run_id>/supercombo_enrichment/records.{json,csv}`
- `data/normalized/<character_slug>/<run_id>/derived_metrics/records.{json,csv}`

Published exports:

- `data/exports/jp/official_raw.{json,csv}`
- `data/exports/jp/supercombo_enrichment.{json,csv}`
- `data/exports/jp/derived_metrics.{json,csv}`
- `data/exports/jp/snapshot_manifest.json`
- `data/exports/<character_slug>/official_raw.{json,csv}`
- `data/exports/<character_slug>/supercombo_enrichment.{json,csv}`
- `data/exports/<character_slug>/derived_metrics.{json,csv}`
- `data/exports/<character_slug>/snapshot_manifest.json`

See `data/exports/README.md` for the current-fact export authority boundary.
See `docs/architecture/noncanonical-data-authority-boundaries.md` for the
cross-surface rule that keeps raw snapshots, normalized intermediate state,
manual-review sidecars, and manual-review debt observability out of normal
public answer authority.
`snapshot_manifest.json` follows
`contracts/current-fact-export-manifest.schema.json` for structural validation.
`data/exports/_index/manual-review-debt.json` is a generated observability index
for withheld rows and review reasons; it is not normal public answer authority.

## Manifest Rules

`run_manifest.json` records a normalized attempt and includes:

- `schema_version`
- `export_contract_version`
- `derivation_rule_version`
- `registry_version`
- `registry_sha256`
- `binding_policy_version`
- `binding_policy_sha256`
- source-level fetch/parse state
- dataset-level publication outcome

`snapshot_manifest.json` records only the current published surface:

- top-level repo-generation metadata for registry/binding-policy versions and hashes
- dataset-entry authoritative published provenance:
  - `publication_state` (`available` / `unavailable` only)
  - `published_run_id`
  - `published_snapshot_ids`
  - `published_record_count`
  - `withheld_review_count`
  - `registry_version`
  - `registry_sha256`
  - `binding_policy_version` / `binding_policy_sha256` for `supercombo_enrichment` only

If `supercombo_enrichment` is unavailable, its dataset entry remains present with a fixed unavailable shape and no on-disk published export files.

## Last-Known-Good Rules

- Failed `official` runs do not overwrite published `official_raw` or `derived_metrics`.
- Failed or non-publishable `supercombo` runs do not overwrite published `supercombo_enrichment` or its published sidecar when the current published supercombo surface is still a subset of the authoritative official safe set.
- If the authoritative official safe set changes and the published supercombo surface is no longer a subset, supercombo is dropped to `unavailable` instead of retaining stale exports.
- Failed runs still keep their own run-local normalized artifacts and run manifest for audit until prune removes non-published runs.

## Baseline Reset Policy

The active published baseline should be v3-native.
Do not carry legacy official raw artifacts forward into the current published artifact surface.
If a new official baseline is minted, the kept snapshot must come from the current v3 fetch path and gets its own v3 `snapshot_id`.
