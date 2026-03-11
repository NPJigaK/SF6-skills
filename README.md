# SF6 Skills Repo

SF6 の concept-first knowledge と、supported baseline characters `jp` / `luke` の v3 published frame-data exports を管理するリポジトリです。

## Supported Baseline Characters

- `jp`
- `luke`

## Durable Checked-In Surface

- code
  - `ingest/frame_data/`
- docs
  - `README.md`
  - `AGENTS.md`
  - `.agents/skills/`
- published current-fact artifacts
  - `data/exports/<character_slug>/`
- minimal backing raw snapshots only
  - `data/raw/<source>/<character_slug>/<snapshot_id>/`
  - currently published datasets を裏づけるために必要な最小限の raw snapshot のみを保持する

## Not Durable Surface

- `.git/`
  - repository metadata
  - durable checked-in artifact surface ではない
- `data/normalized/<character_slug>/<run_id>/`
  - run-local audit state
  - durable checked-in artifact surface ではない
- `__pycache__/`, `.pytest_cache/`
  - local / generated state
- review zip artifacts
  - `SF6skill.zip` のような shared zip artifact を含む
  - durable checked-in artifact surface ではない

## Current Fact Policy

- current fact は `data/exports/<character_slug>/snapshot_manifest.json` を entrypoint に確認する
- `publication_state = available` の dataset だけを current-fact lookup に使う
- lookup order は `official_raw` -> `derived_metrics` -> `supercombo_enrichment`
- `official_raw` を canonical source として先に読む
- `derived_metrics` は official-only の機械計算結果として使う
- `supercombo_enrichment` は supplemental join のみで、official を上書きしない
- `*_manual_review.*`, `data/raw/...`, `data/normalized/...` は通常の current-fact 回答の最終根拠にしない

## Data Layout

- `data/exports/<character_slug>/`
  - shared published surface
  - `snapshot_manifest.json`
  - `official_raw.*`
  - `derived_metrics.*`
  - `supercombo_enrichment.*`
  - `*_manual_review.*`
- `data/raw/<source>/<character_slug>/<snapshot_id>/`
  - currently published datasets を裏づける minimal backing raw snapshots

詳説は `ingest/frame_data/README.md` を参照してください。
