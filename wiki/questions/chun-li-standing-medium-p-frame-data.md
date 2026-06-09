---
type: question
created: 2026-05-30
updated: 2026-06-10
status: active
question: "春麗の立ち中Pは、発生・ヒット時・ガード時・キャンセル可否・ダメージはいくつですか？"
sources:
  - "[[sources/capcom-official-chun-li-frame-data]]"
related:
  - "[[entities/chun-li]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/cancel]]"
  - "[[concepts/terms/drive-impact]]"
  - "[[concepts/terms/drive-rush-cancel]]"
  - "[[concepts/terms/super-art]]"
tags:
  - sf6
  - frame-data
  - chun-li
---

# 質問: 春麗の立ち中Pは、発生・ヒット時・ガード時・キャンセル可否・ダメージはいくつですか？

## 答え

春麗の `立ち中P（頸穿刀）` は、Capcom公式フレームデータの Classic / Modern
どちらでも同じ値。ガード時が `+1F` なので、ガードさせても春麗側が 1F 有利。

| 技 | 操作タイプ | 発生 | 持続 | 硬直 | ヒット時 | ガード時 | キャンセル | ダメージ |
|---|---|---:|---|---:|---:|---:|---|---:|
| 立ち中P（頸穿刀） | Classic | 5F | 5-8F | 10F | +6F | +1F | C | 600 |
| 立ち中P（頸穿刀） | Modern | 5F | 5-8F | 10F | +6F | +1F | C | 600 |

`C` は公式のキャンセル欄の記号で、必殺技、ドライブインパクト、ドライブラッシュ、
SA でキャンセル可能。

## 根拠

- [[sources/capcom-official-chun-li-frame-data]]
- `wiki/outputs/data/frame-data/official/chunli/classic.json`
- `wiki/outputs/data/frame-data/official/chunli/modern.json`
- `classic.json` / `modern.json` 内の `rows[]` と `field_meanings.records[]`

## Limits / uncertainty

- この答えは 2026-05-27 に保存された Chun-Li 公式フレームデータ capture に基づく。
- 個別技の値は公式 JSON output の `rows[]` の該当行をそのまま読む。別日付の再captureが追加された場合は、
  その時点の source date を確認する必要がある。
