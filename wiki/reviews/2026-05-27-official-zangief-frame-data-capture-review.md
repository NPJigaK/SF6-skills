---
type: review
review_type: capture_validation
created: 2026-05-27
status: accepted
sources:
  - "[[sources/capcom-official-zangief-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/zangief]]"
aliases:
  - "Zangief（ザンギエフ） capture review"
tags:
  - review
  - frame-data
  - official
---

# 公式 Zangief（ザンギエフ） フレームデータ capture review - 2026-05-27

## 要約

Zangief（ザンギエフ） の Capcom 公式 frame-data raw snapshot と派生 outputs は、人間レビュー済みで accepted。

## レビュー対象

- `raw/official/frame-data/2026-05-27/zangief/classic/screenshot.png`
- `raw/official/frame-data/2026-05-27/zangief/modern/screenshot.png`
- `raw/official/frame-data/2026-05-27/zangief/classic/table.dom.json`
- `raw/official/frame-data/2026-05-27/zangief/modern/table.dom.json`
- `raw/official/frame-data/2026-05-27/zangief/classic/metadata.json`
- `raw/official/frame-data/2026-05-27/zangief/modern/metadata.json`
- `raw/official/frame-data/2026-05-27/zangief/manifest.json`
- `wiki/outputs/data/frame-data/official/zangief/classic.json`
- `wiki/outputs/data/frame-data/official/zangief/modern.json`
- `wiki/outputs/data/frame-data/official/zangief/classic.json`
- `wiki/outputs/data/frame-data/official/zangief/modern.json`

## 確認内容

- raw snapshot は `raw/official/frame-data/<date>/<data-slug>/<classic|modern>/` の convention に従っている。
- metadata と manifest は publisher、source URL、capture timestamp、character slug、control scheme を含む。
- Classic と Modern は別 capture として保存されている。
- DOM capture は技名、入力 icon、frame values、cancel values、damage、notes、関連 fields を保持している。
- Classic は 72 rows、Modern は 66 rows。
- `field_meanings.records` は table header 由来の説明を保持している。

## 最終判断

Accepted。

## 人間レビューが必要な項目

- この capture について blocker は残っていない。
