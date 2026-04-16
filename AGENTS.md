# SF6 Codex Repo Guidance

## 目的
- このリポジトリは SF6 の知識を concept-first で扱う。
- repo-level canonical published current-fact source は `data/exports/<character_slug>/...`。
- current roster characters の canonical source は `shared/roster/current-character-roster.json`。

## Repo Surfaces
- `skills/` is the canonical public source.
- `local/` is the personal trial workspace for trying distributed skills.
- Do not treat repo-root `.agents/` as a tracked source or mirror surface.
- 不変概念の runtime guidance は `skills/kb-sf6-core/` に置く。
- current roster characters の current-fact runtime guidance は `skills/kb-sf6-frame-current/` に置く。
- observation-first video-analysis guidance は `skills/video-analysis-core/` に置く。

## ソース階層
- `T1`: 公式一次情報
- `T2`: 公式相当の再現可能なゲーム内観測
- `T3`: 継続メンテされている第三者情報
- `T4`: コミュニティ知見・仮説

## Published Data Responsibilities
- published data の責務は守る。
  - `official_raw`: canonical な published official source
  - `derived_metrics`: official-only の機械計算結果
  - `supercombo_enrichment`: supplemental な補完のみ
- packaged runtime assets `skills/kb-sf6-frame-current/assets/published/<character_slug>/...` は repo-level canonical published source `data/exports/<character_slug>/...` から生成される。
- `*_manual_review.*`, `data/raw/...`, `data/normalized/...` は distributed skills の通常回答における最終根拠として扱わない。

## Maintainer Workflows
- knowledge の統合作業は `maintainer-skills/sync-knowledge/` を使う。
- パッチ/調整対応の current roster frame-data 更新は `maintainer-skills/update-frame-data/` を使う。

## Ingestion / Data
- 実装コードは `ingest/frame_data/` に置く。`.agents/skills/` に取得コードは置かない。
- raw snapshots は「現在 publish されている dataset を裏づけるために必要な最小限のものだけ」を保持する。
- published main exports は safe-only とし、review 行は `*_manual_review.{json,csv}` に分離する。
