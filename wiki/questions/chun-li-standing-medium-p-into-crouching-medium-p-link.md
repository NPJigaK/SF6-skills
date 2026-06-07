---
type: question
created: 2026-05-30
updated: 2026-06-08
status: active
question: "春麗の立ち中Pが通常ヒットしたあと、発生6Fのしゃがみ中Pは理論上つながる？理由もフレームで説明して。"
sources:
  - "[[sources/capcom-official-chun-li-frame-data]]"
related:
  - "[[entities/chun-li]]"
  - "[[concepts/frame-data]]"
  - "[[questions/chun-li-standing-medium-p-frame-data]]"
tags:
  - sf6
  - frame-data
  - chun-li
  - links
---

# 質問: 春麗の立ち中Pが通常ヒットしたあと、発生6Fのしゃがみ中Pは理論上つながる？

## 答え

理論上はつながる。春麗の `立ち中P（頸穿刀）` は通常ヒット時 `+6F`、
`しゃがみ中P（丹頂拳）` は発生 `6F` なので、差し引きは `+6F - 6F = 0F`。
最速で出せば連続ヒットするが、数値上の余裕はない。

これは `立ち中P` の硬直が終わったあとに `しゃがみ中P` を出すリンクの話で、
通常技から通常技へキャンセルしているわけではない。

| 前の技 | 条件 | ヒット時硬直差 | 次の技 | 発生 | 判定 |
|---|---|---:|---|---:|---|
| 立ち中P（頸穿刀） | 通常ヒット | +6F | しゃがみ中P（丹頂拳） | 6F | 理論上つながる |

## フレーム説明

`+6F` は、立ち中Pが通常ヒットしたあと、春麗が相手より 6F 早く動けるという意味。
その最速行動として発生6Fのしゃがみ中Pを出すと、しゃがみ中Pの最初の攻撃判定が
相手の硬直が解けるタイミングに間に合う。

式で見ると、リンク可否は基本的に次の技の発生がヒット時有利以下かで判断する。

```text
立ち中Pのヒット時有利: +6F
しゃがみ中Pの発生:       6F
残り猶予:               +6F - 6F = 0F
```

`0F` なので、フレーム上は最速ならつながる。1Fでも遅れると相手がガード可能になる。

## 根拠

- [[sources/capcom-official-chun-li-frame-data]]
- `wiki/outputs/data/frame-data/official/chunli/classic.json`
- `wiki/outputs/data/frame-data/official/chunli/modern.json`
- `classic.json` / `modern.json` 内の `rows[]` と `field_meanings.records[]`

確認した公式 JSON output の値:

| 操作タイプ | 立ち中P ヒット時 | しゃがみ中P 発生 | しゃがみ中P 持続 |
|---|---:|---:|---|
| Classic | +6F | 6F | 6-9F |
| Modern | +6F | 6F | 6-9F |

## 注意 / 不確実性

- これはフレーム上の理論判定。実際に当たるかは距離、押し戻し、食らい判定にも左右される。
- この答えは通常ヒット前提。カウンター、パニッシュカウンター、ドライブラッシュ補正などで
  硬直差が変わる状況は別計算になる。
- この答えは 2026-05-27 に保存された Chun-Li 公式フレームデータ capture に基づく。
