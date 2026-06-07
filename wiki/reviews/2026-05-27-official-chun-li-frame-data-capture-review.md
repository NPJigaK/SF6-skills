---
type: review
review_type: capture_validation
created: 2026-05-27
status: accepted
sources:
  - "[[sources/capcom-official-chun-li-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/chun-li]]"
aliases:
  - "Chun-Li（春麗） capture review"
tags:
  - review
  - frame-data
  - official
---

# 公式 Chun-Li（春麗） フレームデータ capture review - 2026-05-27

## 要約

Chun-Li（春麗） の Capcom 公式 frame-data raw snapshot と派生 outputs は、人間レビュー済みで accepted。

## レビュー対象

- `raw/official/frame-data/2026-05-27/chunli/classic/screenshot.png`
- `raw/official/frame-data/2026-05-27/chunli/modern/screenshot.png`
- `raw/official/frame-data/2026-05-27/chunli/classic/table.dom.json`
- `raw/official/frame-data/2026-05-27/chunli/modern/table.dom.json`
- `raw/official/frame-data/2026-05-27/chunli/classic/metadata.json`
- `raw/official/frame-data/2026-05-27/chunli/modern/metadata.json`
- `raw/official/frame-data/2026-05-27/chunli/manifest.json`
- `wiki/outputs/data/frame-data/official/chunli/classic.csv`
- `wiki/outputs/data/frame-data/official/chunli/modern.csv`
- `wiki/outputs/data/frame-data/official/chunli/classic.field-meanings.json`
- `wiki/outputs/data/frame-data/official/chunli/modern.field-meanings.json`

## 確認内容

- raw snapshot は `raw/official/frame-data/<date>/<data-slug>/<classic|modern>/` の convention に従っている。
- metadata と manifest は publisher、source URL、capture timestamp、character slug、control scheme を含む。
- Classic と Modern は別 capture として保存されている。
- DOM capture は技名、入力 icon、frame values、cancel values、damage、notes、関連 fields を保持している。
- Classic は 78 rows、Modern は 72 rows。
- field-meaning JSON は table header 由来の説明を保持している。

## 最終判断

Accepted。

## 人間レビューが必要な項目

- この capture について blocker は残っていない。
