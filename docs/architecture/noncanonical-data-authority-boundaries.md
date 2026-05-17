---
title: Non-canonical Data Authority Boundaries
status: accepted
last_reviewed: 2026-05-18
tracking_issue: "#260"
---

# Non-canonical Data Authority Boundaries

この文書は、`data/raw/`、`data/normalized/`、`*_manual_review.*`、
`data/exports/_index/manual-review-debt.json` を normal public answer authority
として扱わないための境界を定義する。

## Scope

対象 surface は次のとおり。

| Surface | Registry ID | Boundary |
|---|---|---|
| `data/raw/` | `raw_snapshots` | current published exports を再現するための最小 raw input。normal public answer authority ではない。 |
| `data/normalized/` | `normalized_intermediate_state` | run-local audit / intermediate state。現在は tracked durable artifact ではない。 |
| `data/exports/*/*_manual_review.*` | `manual_review_sidecars` | withheld rows / review holds。review と publish workflow 前の normal public answer authority ではない。 |
| `data/exports/_index/manual-review-debt.json` | `manual_review_debt_index` | manual-review debt の observability index。current-fact authority ではない。 |

## Authority Rule

これらの surface から exact current facts を直接推論して通常回答に使ってはいけない。
通常回答で使える current-fact authority は、published export / runtime asset / roster
など、明示された canonical または derived current-fact surface に限る。

`data/raw/` は byte-level reproducibility input であり、published export の根拠を
再検証するために使う。raw snapshot 自体をユーザー回答の evidence として
昇格しない。

`data/normalized/` は ingestion run の中間状態である。tracked durable surface として
導入する場合でも、後続 policy が変更しない限り non-canonical のまま扱う。

`*_manual_review.*` は withheld rows、unresolved rows、review reason を記録する。
通常回答や runtime lookup に入れるには、review / publish workflow を通して main export
へ昇格させる必要がある。

`data/exports/_index/manual-review-debt.json` は manual-review debt を見える化する
observability surface である。生成元が manual-review sidecar であるため、この index
自体も normal public answer authority ではない。

## Promotion Paths

| Source surface | Allowed promotion path |
|---|---|
| `data/raw/` | ingestion / parse / publish workflow により `data/exports/` と `snapshot_manifest.json` に反映する。 |
| `data/normalized/` | publish workflow により accepted published export surface へ反映する。tracked intermediate state を正本化しない。 |
| `*_manual_review.*` | review / publish workflow により safe rows だけを main export に移す。 |
| `manual-review-debt.json` | promotion path なし。observability と prioritization のみ。 |

## Validator Coverage

この boundary は次の validator と docs に分散している。

- `tests/validation/validate-noncanonical-data-authority-boundaries.ps1`
- `tests/validation/validate-raw-snapshot-minimality.ps1`
- `tests/validation/validate-raw-snapshot-retention-adr.ps1`
- `tests/validation/validate-manual-review-debt-index.ps1`
- `tests/validation/validate-current-fact-boundaries.ps1`
- `tests/validation/validate-frame-current-assets.ps1`
- `data/repository-surfaces.json`
- `docs/architecture/repository-surface-registry-policy.md`
- `data/exports/README.md`
- `ingest/frame_data/README.md`

`validate-noncanonical-data-authority-boundaries.ps1` は、registry と docs がこの
non-canonical boundary を同じ意味で説明しているかを read-only に確認する。

## Non-goals

- `data/raw/`、`data/normalized/`、`data/exports/` の data content を変更しない。
- `official_raw`、`derived_metrics`、`supercombo_enrichment` の authority を変更しない。
- `data/raw/` や manual-review sidecar を normal public answer authority にしない。
- generated frame-current assets、normalization assets、`.dist` を変更しない。
- Hermes memory、sessions、local skills、Curator output、logs、caches、raw transcript を commit しない。
