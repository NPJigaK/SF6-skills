# SF6 Skills Repo

SF6 の concept-first knowledge と、JP 向け frame data の v3 published exports を管理するリポジトリです。

## Durable Checked-In Surface

- code
  - `ingest/frame_data/`
- docs
  - `README.md`
  - `AGENTS.md`
  - `.agents/skills/`
- published current-fact artifacts
  - `data/exports/jp/`
- minimal raw snapshots only
  - `data/raw/official/jp/`
  - `data/raw/supercombo/jp/`
  - 現在 publish されている dataset を裏づける最小限の snapshot だけを残す

## Not Durable Surface

- `data/normalized/jp/<run_id>/`
  - run-local audit state
  - 中間成果物と run manifest の置き場であり、durable checked-in artifact surface ではない
- `__pycache__/`, `.pytest_cache/`
  - local / generated state

## Current Fact Policy

- current fact は `data/exports/jp/snapshot_manifest.json` を入口に確認する
- `publication_state = available` の dataset だけを current-fact lookup に使う
- `official_raw` を先に読む
- `derived_metrics` は official 由来の機械計算として使う
- `supercombo_enrichment` は supplemental join のみで、`official_raw` の後に `move_id` で参照する
- `*_manual_review.*`, `data/raw/...`, `data/normalized/...` は通常の current-fact 回答では使わない

## Data Layout

- `data/exports/jp/`
  - shared published surface
  - `snapshot_manifest.json`
  - `official_raw.*`
  - `derived_metrics.*`
  - `supercombo_enrichment.*`
  - `*_manual_review.*`
- `data/raw/<source>/jp/<snapshot_id>/`
  - published datasets を裏づける minimal raw snapshots

詳細は `ingest/frame_data/README.md` を参照してください。
