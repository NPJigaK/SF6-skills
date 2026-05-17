# Current Fact Exports

`data/exports/` は、公開済みの exact current-fact export surface です。

この directory は通常回答で使う move-specific current facts の authority ですが、
すべての tracked file が同じ authority を持つわけではありません。

## Authority Boundary

- `official_raw.{json,csv}` は公式 raw frame-data export の公開面です。
- `derived_metrics.{json,csv}` は `official_raw` だけから再計算された派生 metric です。
- `supercombo_enrichment.{json,csv}` は `official_raw` の safe subset に束縛された enrichment です。
- `snapshot_manifest.json` は character ごとの published export provenance です。
- `*_manual_review.{json,csv}` は withheld row / review reason / audit sidecar です。

`*_manual_review.*` は normal public answer authority ではありません。通常回答や
runtime current-fact lookup に混ぜる前に、review と publish workflow を通して
main export へ昇格させる必要があります。

## Layout

Character ごとの directory は次の形を持ちます。

```text
data/exports/<character_slug>/
  official_raw.json
  official_raw.csv
  official_raw_manual_review.json
  official_raw_manual_review.csv
  derived_metrics.json
  derived_metrics.csv
  derived_metrics_manual_review.json
  derived_metrics_manual_review.csv
  supercombo_enrichment.json
  supercombo_enrichment.csv
  supercombo_enrichment_manual_review.json
  supercombo_enrichment_manual_review.csv
  snapshot_manifest.json
```

`snapshot_manifest.json` は `contracts/current-fact-export-manifest.schema.json`
に従います。この schema は structural validation 用です。published raw
snapshot の keep-set、runtime asset reproducibility、manual-review debt などの
cross-file semantics は専用 validator が扱います。

## Manual-Review Debt Index

`data/exports/_index/manual-review-debt.json` は、すべての
`*_manual_review.json` sidecar と `snapshot_manifest.json` から生成される
横断 index です。

この index は、character / dataset ごとに次を見える化します。

- `publication_state`
- `published_record_count`
- manifest 上の `withheld_review_count`
- actual manual-review sidecar row count
- reason-code counts
- `publish_eligible` / `confirmation_status` counts

この index は observability surface です。normal public answer authority では
ありません。生成元の manual-review rows も、review と publish workflow を通る
までは通常回答に使ってはいけません。

Regenerate and validate the index:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-manual-review-debt-index.ps1 -Update
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-manual-review-debt-index.ps1
```

## Dataset Semantics

Current dataset keys are:

- `official_raw`
- `derived_metrics`
- `supercombo_enrichment`

Each dataset entry records:

- `publication_state`
- `published_run_id`
- `published_snapshot_ids`
- `published_record_count`
- `withheld_review_count`
- `registry_version` / `registry_sha256`
- `binding_policy_version` / `binding_policy_sha256`
- `content_hash`

`publication_state` is `available` or `unavailable`. Available datasets have
published export files and provenance. Unavailable datasets keep an explicit
manifest entry so downstream code can distinguish absence from omission.

## Non-Authority Surfaces

The following are not normal public answer authority:

- `data/raw/`
- `data/normalized/`
- `*_manual_review.*`
- run-local scraper state
- browser/cache/log output
- Hermes memory, sessions, local skills, Curator output, checkpoints, or raw transcripts

Exact current facts must not be inferred from those surfaces alone.

## Validation

Run the focused structural contract check:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-json-schema-manifest.ps1
```

Run related semantic checks:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-frame-current-assets.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-raw-snapshot-minimality.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-manual-review-debt-index.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-current-fact-boundaries.ps1
```

Use `tests/validation/run-all.ps1` before claiming broad validation.
