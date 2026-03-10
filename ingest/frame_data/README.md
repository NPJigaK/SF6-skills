# SF6 JP Frame Data Ingestion v3

`ingest/frame_data` is the v3 ingestion package for Street Fighter 6 JP frame data.
It keeps scraping/runtime code under `ingest/frame_data/` and does not place fetch code under `.agents/skills/`.

The checked-in current artifact surface is:

- v3 code
- v3 published exports under `data/exports/jp/`
- the minimal raw snapshots under `data/raw/` needed to reproduce those published exports

`data/normalized/` is run-local audit state and is not part of the durable checked-in artifact surface.

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
- `supercombo`: Scrapling `StealthyFetcher` against `/JP/Data`
- raw snapshot first: fetch writes the authoritative byte payload plus `metadata.json` before parse
- parser input is deterministically decoded from the stored raw bytes

The authoritative raw artifact is the on-disk response byte payload. Any decoded HTML text is derived from those bytes and is not the source of truth.

## Source Selection

- `official` is the canonical source for current published frame data
- `supercombo` is enrichment-only and may be `unavailable` if it cannot be safely published under the current v3 path
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
python -m sf6_ingest.cli fetch --character jp --source all
```

Parse from saved raw snapshots:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli parse-from-raw --character jp --source all --official-snapshot-id <official_snapshot_id> --supercombo-snapshot-id <supercombo_snapshot_id>
```

Publish a normalized run:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli publish --character jp --run-id <run_id>
```

End-to-end run:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli run --character jp --source all
```

Prune to latest published state only:

```powershell
cd ingest/frame_data
python -m sf6_ingest.cli prune --character jp --dry-run
python -m sf6_ingest.cli prune --character jp --apply
```

## Data Layout

Raw snapshots:

- `data/raw/official/jp/<snapshot_id>/page.html`
- `data/raw/official/jp/<snapshot_id>/metadata.json`
- `data/raw/supercombo/jp/<snapshot_id>/page.html`
- `data/raw/supercombo/jp/<snapshot_id>/metadata.json`

Normalized runs:

- `data/normalized/jp/<run_id>/run_manifest.json`
- `data/normalized/jp/<run_id>/official_raw/records.{json,csv}`
- `data/normalized/jp/<run_id>/supercombo_enrichment/records.{json,csv}`
- `data/normalized/jp/<run_id>/derived_metrics/records.{json,csv}`

Published exports:

- `data/exports/jp/official_raw.{json,csv}`
- `data/exports/jp/supercombo_enrichment.{json,csv}`
- `data/exports/jp/derived_metrics.{json,csv}`
- `data/exports/jp/snapshot_manifest.json`

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
