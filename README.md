# SF6 Skills Repo

SF6 の concept-first knowledge と、現行 roster 全体の v3 published frame-data exports を管理するリポジトリです。

## Current Character Roster

- canonical source: `shared/roster/current-character-roster.json`
- current fact / runtime asset / packaging / validator の character inventory はこの roster source に追従する
- roster source は checked-in official raw snapshot に含まれる character-select links を根拠に管理する

## Repository Structure

- public skills live under `skills/<skill-name>/`
- maintainer-only workflows live under `maintainer-skills/<skill-name>/`
- personal trial workspace lives under `local/`
- shared executable infrastructure lives under `packages/`
- shared non-code artifacts live under `shared/`
- repository docs, tests, and scripts live under `docs/`, `tests/`, and `scripts/`
- data production code lives under `ingest/frame_data/`
- published current-fact artifacts live under `data/exports/<character_slug>/`

## Repo Structure Contract

- simple, explicit structure beats flexible abstraction
- new public skills start as independent units under `skills/`
- move artifacts to `packages/` or `shared/` only after a second real consumer exists
- local PowerShell validators are the canonical structure guard

Detailed contract:

- [repo-structure-contract.md](./docs/architecture/repo-structure-contract.md)

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
- repo-level canonical published data は `data/exports/<character_slug>/...`
- current roster の canonical source は `shared/roster/current-character-roster.json`
- public distributed `skills/kb-sf6-frame-current` は generated packaged runtime assets `skills/kb-sf6-frame-current/assets/published/<character_slug>/...` を read し、これらは `data/exports/<character_slug>/...` から生成される
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
