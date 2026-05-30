---
type: review
review_type: capture_validation
created: 2026-05-26
status: accepted
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/jp]]"
aliases:
  - "JP capture review"
tags:
  - review
  - frame-data
  - official
---

# 公式 JP フレームデータ capture review - 2026-05-26

## 要約

JP の Capcom 公式 frame-data raw snapshot と派生 outputs は、人間レビュー済みで accepted。

## レビュー対象

- `raw/official/frame-data/2026-05-26/jp/classic/screenshot.png`
- `raw/official/frame-data/2026-05-26/jp/modern/screenshot.png`
- `raw/official/frame-data/2026-05-26/jp/classic/table.dom.json`
- `raw/official/frame-data/2026-05-26/jp/modern/table.dom.json`
- `raw/official/frame-data/2026-05-26/jp/classic/metadata.json`
- `raw/official/frame-data/2026-05-26/jp/modern/metadata.json`
- `raw/official/frame-data/2026-05-26/jp/manifest.json`
- `wiki/outputs/data/frame-data/jp/classic.csv`
- `wiki/outputs/data/frame-data/jp/modern.csv`
- `wiki/outputs/data/frame-data/jp/classic.field-meanings.json`
- `wiki/outputs/data/frame-data/jp/modern.field-meanings.json`

## 確認内容

- raw snapshot は `raw/official/frame-data/<date>/<data-slug>/<classic|modern>/` の convention に従っている。
- metadata と manifest は publisher、source URL、capture timestamp、character slug、control scheme を含む。
- Classic と Modern は別 capture として保存されている。
- DOM capture は技名、入力 icon、frame values、cancel values、damage、notes、関連 fields を保持している。
- Classic は 69 rows、Modern は 65 rows。
- field-meaning JSON は table header 由来の説明を保持している。

## 最終判断

Accepted。

## 人間レビューが必要な項目

- この capture について blocker は残っていない。
