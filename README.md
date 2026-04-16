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

## Current Fact Surfaces

- repo-level canonical published current-fact source lives under `data/exports/<character_slug>/...`
- current roster の canonical source は `shared/roster/current-character-roster.json`
- exact runtime answer rules live in `skills/kb-sf6-frame-current/`
- concept-only runtime guidance lives in `skills/kb-sf6-core/`
- generated packaged runtime assets under `skills/kb-sf6-frame-current/assets/published/<character_slug>/...` are built from `data/exports/<character_slug>/...`

## Data Layout

- `data/exports/<character_slug>/`
  - shared published export surface for one character
  - exact runtime lookup contract lives in `skills/kb-sf6-frame-current/references/export-contract.md`
- `data/raw/<source>/<character_slug>/<snapshot_id>/`
  - currently published datasets を裏づける minimal backing raw snapshots

詳説は `ingest/frame_data/README.md` を参照してください。
