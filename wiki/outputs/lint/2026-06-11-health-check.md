---
type: output
output_type: lint_report
title: "Wiki Health Check - 2026-06-11"
created: 2026-06-11
updated: 2026-06-15
status: superseded
confidence: medium
superseded_by:
  - "[[reviews/2026-06-15-pdr-cost-component-video-observation]]"
  - "[[concepts/terms/raw-drive-rush]]"
sources:
  - "[[index]]"
  - "[[log]]"
  - "[[outputs/lint/2026-06-10-health-check]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/supercombo-street-fighter-6-game-data]]"
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
  - "[[sources/capcom-official-battle-change-list]]"
tags:
  - lint
  - health-check
  - review-needed
---

# Wiki Health Check - 2026-06-11

## 2026-06-15 追記

この report の `Drive Rush from Parry` cost 表記揺れに関する未解決事項は、2026-06-15 の PDR cost component 整理で superseded とする。現行方針では、Capcom 公式の cost `1` を Drive Parry activation `0.5` + Drive Rush from Parry transition component `0.5` の最小総消費として扱う。ただし、`wiki/outputs/data/gauges/supercombo/numeric-tables.json` の `cost_bars` は単一 direct cost 用 field として維持し、PDR では `null` のまま、component / total は専用 field に分ける。

## Scope

この health check は、[[outputs/lint/2026-06-10-health-check]] 以後に増えた 2026-06-11 の web-page capture、Game Data tabber pipeline、Battle Change / Patch Notes derived output、既存 source page provenance を中心に確認した。`raw/` の再取得、source text の事実修正、未確定値の確定は行っていない。日付は Asia/Tokyo の 2026-06-11 を使う。

## Executive Summary

- P0 Integrity として、[[sources/supercombo-jp-frame-data]] と [[sources/supercombo-ryu-frame-data]] の `captured_at_utc` が raw manifest とずれていたため、source page frontmatter を manifest に同期した。
- Follow-up として、[[sources/supercombo-street-fighter-6-patch-notes]] の `source_updated_at` を root page freshness に戻し、detail pages の最新 freshness を `latest_detail_source_updated_at` に分けた。
- Follow-up として、[[sources/supercombo-street-fighter-6-frame-data-batch]] の `raw_path` を実在 batch root にし、manifest pattern は `raw_path_pattern` に分けた。
- 通常 wiki page の broken wikilink、missing frontmatter、missing index entry、orphan-like page、duplicate title は見つからなかった。
- `wiki/outputs/**/*.json` 371 件、`raw/**/*.json` 793 件は parse error なし。`raw/**/validation*.json` 59 件は pass 系 status。
- 公式 frame-data 30 source page の Classic / Modern row count は derived JSON の `row_count` と一致した。
- Battle Change / Patch Notes / Game Data / Gauges の主要 derived count は source page / index の記述と一致した。
- P1 Evidence は新規に確定変更しない。`Drive Rush from Parry` の cost 表記揺れ、SuperCombo enriched review queue、Patch Notes source freshness の batch 表現は review-needed / policy-needed として残す。

## 機械チェック結果

| 項目 | 結果 | メモ |
|---|---:|---|
| Markdown files | 197 | この report 作成前の検査値 |
| Non-template pages | 187 | `wiki/templates/`、`wiki/index.md`、`wiki/log.md` を除外 |
| Missing frontmatter | 0 | `index.md` / `log.md` は対象外 |
| Missing `type` frontmatter | 0 | non-template page 対象 |
| Broken wikilinks | 0 real pages / 5 template placeholders | `wiki/templates/*.md` の `\[\[concepts/...\]\]` などは placeholder として除外 |
| Missing direct index entries | 0 | templates / index / log は除外 |
| Orphan-like pages | 0 | index/log/templates を除く |
| Duplicate titles | 0 | frontmatter `title` の exact match |
| Lint report frontmatter issues | 0 | `type: output` / `output_type: lint_report` |
| Review frontmatter issues | 0 | `type: review` |
| `wiki` JSON parse errors | 0 / 371 | `jq empty` |
| `raw` JSON parse errors | 0 / 793 | `jq empty` |
| Raw validation non-pass | 0 / 59 | `validation.json` / `validation.batch.json` / `validation.tabbers.json` |
| Schema JSON non-object | 0 / 62 | `wiki/outputs/data/<family>/schema.json` pattern |
| Unknown raw `storage_policy` | 0 / 143 | AGENTS.md の許可値内 |
| Official frame-data row-count mismatch | 0 / 30 | source page の Classic / Modern 件数と JSON `row_count` |
| Open review pages | 21 | capture review / prereview / calculation model gap |

## 検証した derived output

| Family | 結果 | 根拠 |
|---|---|---|
| Official Battle Change | 20 versions、1820 change rows、1820 change events、1419 move-index rows。各 `row_count == rows.length`。 | [[sources/capcom-official-battle-change-list]]; `wiki/outputs/data/battle-change/official/<json-file>` pattern |
| SuperCombo Patch Notes | 17 version rows、1374 community events、1118 target rows。公式 crosswalk は 16 matched / 1 launch / 4 official-only。 | [[sources/supercombo-street-fighter-6-patch-notes]]; `wiki/outputs/data/battle-change/supercombo-patch-notes/<json-file>` pattern |
| SuperCombo Game Data | tabber groups 4、tabs 46、content tables 39、navigation table 1、tabber validation `passed`。 | [[sources/supercombo-street-fighter-6-game-data]]; `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` |
| SuperCombo Gauges | raw content tables 13、normalized numeric tables 18。 | [[sources/supercombo-street-fighter-6-gauges]]; `wiki/outputs/data/gauges/supercombo/numeric-tables.json` |

## 修正済み

### P0: source page `captured_at_utc` と manifest の同期

以下の source page frontmatter は raw manifest と数分ずれていた。source facts ではなく provenance metadata の同期なので、LLM が安全に修正した。

| Page | Before | After / manifest |
|---|---:|---:|
| [[sources/supercombo-jp-frame-data]] | `2026-05-30T21:38:52Z` | `2026-05-30T21:40:27Z` |
| [[sources/supercombo-ryu-frame-data]] | `2026-05-31T06:56:44Z` | `2026-05-31T07:05:25Z` |

### P1/P2: Patch Notes root/detail freshness の分離

[[sources/supercombo-street-fighter-6-patch-notes]] の frontmatter は、root Patch Notes page の freshness と detail pages の最新 freshness を分ける形に修正した。`source_updated_at` は raw root manifest の root page revid `276775` / `2023-09-27T14:23:05Z`、`latest_detail_source_updated_at` は detail pages 最新の `2026-06-02T03:12:40Z` とする。

### P2: batch source `raw_path` placeholder の分離

[[sources/supercombo-street-fighter-6-frame-data-batch]] の `raw_path` は実在する batch root `raw/frame-data/supercombo/` に変更し、character manifest の pattern は `raw_path_pattern: "raw/frame-data/supercombo/<character_slug>/manifest.json"` に分けた。

## 未確定のため修正しない項目

### P1: `Drive Rush from Parry` cost 表記揺れ

[[sources/supercombo-street-fighter-6-gauges]] は、Drive Rush from Parry の cost について cost table の `1/2` と section / caption text の `1 Drive Stock` が揺れると明記している。[[reviews/2026-06-11-supercombo-gauges-web-page-capture-review]] にも未解決事項として残っているため、単一値へ正規化しない。

2026-06-15 追記: この判断は [[reviews/2026-06-15-pdr-cost-component-video-observation]] と [[concepts/terms/raw-drive-rush]] の component / total 整理で superseded。現行方針では `1/2` を transition component、`1 Drive Stock` を Drive Parry activation 込みの最小総消費として扱う。ただし PDR の `cost_bars` は単一 direct cost としては使わない。

## Review-needed

- SuperCombo enriched output は未レビュー補助行と SuperCombo-only rows が残る。既存方針どおり、公式値を上書きせず review queue に残す。
- Game Data / Gauges / Offense / Defense の community numeric facts は、公式 source または実機検証と矛盾する場合に公式・検証済み data を優先する。
- Patch Notes / Battle Change の event index は検索補助であり、回答では source page、raw、公式本文、現在 frame-data output に戻る。

## 未解決の質問

- `Drive Rush from Parry` の cost 表記揺れを component 分解として扱うか、source-internal conflict として保持し続けるか。2026-06-15 時点では component 分解を採用し、PDR の `cost_bars` は単一 direct cost として使わない方針に更新済み。
- Open review pages 21 件のうち、capture validation と prereview を別々の review dashboard / synthesis にまとめるか。
