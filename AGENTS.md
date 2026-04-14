# SF6 Codex Repo Guidance

## 目的
- このリポジトリは SF6 の知識を concept-first で扱う。
- current fact は published exports を正本として参照し、raw / normalized は監査や再解析に限る。
- current roster characters の canonical source は `shared/roster/current-character-roster.json`。

## 回答ラベル
- `[検証済み]`: `T1` または `T2` の根拠で current fact を確認した回答
- `[概念のみ]`: 概念だけを説明し、current fact や exact 数値は断定しない回答
- `[保留]`: current fact や exact 数値を断定するための根拠や条件が足りない回答

## ソース階層
- `T1`: 公式一次情報
- `T2`: 公式相当の再現可能なゲーム内観測
- `T3`: 継続メンテされている第三者情報
- `T4`: コミュニティ知見・仮説

## 基本ルール
- current の仕様・数値・差分は `T1` または `T2` が無ければ断定しない。
- 公式ソースが存在する領域では `T3` 単独を最終根拠にしない。
- 概念質問にはまず概念で答え、current fact が必要な部分だけ published data を確認する。
- current roster characters の current fact の最終根拠は published exports only とする。
- `skills/` is the canonical public source.
- `local/` is the personal trial workspace for trying distributed skills.
- Do not treat repo-root `.agents/` as a tracked source or mirror surface.
- published data の責務は守る。
  - `official_raw`: canonical な正本
  - `derived_metrics`: official-only の機械計算結果
  - `supercombo_enrichment`: supplemental な補完のみ
- current fact を答えるときは `data/exports/<character_slug>/snapshot_manifest.json` を入口にし、`publication_state = available` の dataset だけ使う。
- public distributed `skills/kb-sf6-frame-current/` は、この repo-level canonical published source から生成された packaged runtime assets `skills/kb-sf6-frame-current/assets/published/<character_slug>/...` を読む。
- `*_manual_review.*`, `data/raw/...`, `data/normalized/...` は通常回答の最終根拠にしない。

## Knowledge と Skills
- 不変概念は `skills/kb-sf6-core/` に寄せる。
- current roster characters の current fact は `skills/kb-sf6-frame-current/` を使い、published exports だけを読む。
- 動画観測の canonical segment timeline は `skills/video-analysis-core/` に寄せる。
- `skills/video-analysis-core/` は raw video を 60fps に正規化した observation-first surface を返す。
- exact current fact や verdict-heavy interpretation はこの skill で断定しない。
- knowledge の統合作業は `maintainer-skills/sync-knowledge/` を使う。
- パッチ/調整対応の current roster frame-data 更新は `maintainer-skills/update-frame-data/` を使う。

## Ingestion / Data
- 実装コードは `ingest/frame_data/` に置く。`.agents/skills/` に取得コードは置かない。
- raw snapshots は「現在 publish されている dataset を裏づけるために必要な最小限のものだけ」を保持する。
- published main exports は safe-only とし、review 行は `*_manual_review.{json,csv}` に分離する。
