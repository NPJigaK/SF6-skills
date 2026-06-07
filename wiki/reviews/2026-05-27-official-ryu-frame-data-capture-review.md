---
type: review
review_type: capture_validation
created: 2026-05-27
status: accepted
sources:
  - "[[sources/capcom-official-ryu-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/ryu]]"
aliases:
  - "Ryu（リュウ） capture review"
tags:
  - review
  - frame-data
  - official
---

# 公式 Ryu（リュウ） フレームデータ capture review - 2026-05-27

## 要約

Ryu（リュウ） の Capcom 公式 frame-data raw snapshot と派生 outputs は、人間レビュー済みで accepted。

## レビュー対象

- `raw/official/frame-data/2026-05-27/ryu/classic/screenshot.png`
- `raw/official/frame-data/2026-05-27/ryu/modern/screenshot.png`
- `raw/official/frame-data/2026-05-27/ryu/classic/table.dom.json`
- `raw/official/frame-data/2026-05-27/ryu/modern/table.dom.json`
- `raw/official/frame-data/2026-05-27/ryu/classic/metadata.json`
- `raw/official/frame-data/2026-05-27/ryu/modern/metadata.json`
- `raw/official/frame-data/2026-05-27/ryu/manifest.json`
- `wiki/outputs/data/frame-data/official/ryu/classic.json`
- `wiki/outputs/data/frame-data/official/ryu/modern.json`
- `wiki/outputs/data/frame-data/official/ryu/classic.json`
- `wiki/outputs/data/frame-data/official/ryu/modern.json`

## 確認内容

- raw snapshot は `raw/official/frame-data/<date>/<data-slug>/<classic|modern>/` の convention に従っている。
- metadata と manifest は publisher、source URL、capture timestamp、character slug、control scheme を含む。
- Classic と Modern は別 capture として保存されている。
- DOM capture は技名、入力 icon、frame values、cancel values、damage、notes、関連 fields を保持している。
- Classic は 75 rows、Modern は 69 rows。
- `field_meanings.records` は table header 由来の説明を保持している。

## 最終判断

Accepted。

## 人間レビューが必要な項目

- この capture について blocker は残っていない。
