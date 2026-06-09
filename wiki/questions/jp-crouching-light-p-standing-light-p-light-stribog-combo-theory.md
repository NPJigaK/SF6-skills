---
type: question
created: 2026-06-08
updated: 2026-06-10
status: active
question: "JPのしゃがみ弱P＞立ち弱P＞弱ストリボーグは、なぜ理論上つながる？"
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
related:
  - "[[entities/jp]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[concepts/terms/chain]]"
  - "[[concepts/terms/cancel]]"
  - "[[concepts/terms/frame-advantage]]"
tags:
  - sf6
  - frame-data
  - jp
  - combos
  - links
  - cancels
---

# 質問: JPのしゃがみ弱P＞立ち弱P＞弱ストリボーグは、なぜ理論上つながる？

## 答え

このコンボは、`しゃがみ弱P` の `+4F` から発生 `6F` の `立ち弱P` を
「リンク」しているわけではない。構造は次の2段階。

1. `しゃがみ弱P` → `立ち弱P` は、弱攻撃の連打キャンセル / chain。
2. `立ち弱P` → `弱 ストリボーグ` は、`立ち弱P` の `C` キャンセルによる必殺技キャンセル。

したがって、単純なリンク式だけで見ると誤解する。

```text
しゃがみ弱P ヒット時有利: +4F
立ち弱P 発生:              6F
リンクとして見ると:        +4F - 6F = -2F なので足りない
```

それでもつながるのは、`しゃがみ弱P` が連打キャンセル対応で、SuperCombo 側でも
`5LP/2LP/2LK` へ chain できると記録されているため。前の技の硬直が終わるまで待つ
リンクではなく、弱攻撃 chain で `立ち弱P` を出している。

次に、`立ち弱P` から `弱 ストリボーグ` もリンクではない。

```text
立ち弱P ヒット時有利: +4F
弱 ストリボーグ 発生: 16F
リンクとして見ると:    +4F - 16F = -12F なので不可能
```

ここは `立ち弱P` のキャンセル欄が `C` で、公式説明上 `C` は必殺技、ドライブインパクト、
ドライブラッシュ、SA でキャンセル可能という意味。`弱 ストリボーグ` は必殺技なので、
`立ち弱P` の動作を途中で切って出せる。

## フレームで見る

該当技の公式 Classic 値は次の通り。

| 技 | 発生 | 持続 | 硬直 | ヒット時 | ガード時 | キャンセル | 備考 |
|---|---:|---|---:|---:|---:|---|---|
| しゃがみ弱P（ブィストルイ・ウダール） | 4F | 4-5F | 11F | +4F | -1F | C | 連打キャンセル対応 |
| 立ち弱P（ノーシ） | 6F | 6-8F | 10F | +4F | -2F | C | 連打キャンセル対応 |
| 弱 ストリボーグ | 16F | 16-21F | 全体49F | D | -10F | SA3 | 飛び道具相殺判定あり |

`立ち弱P` から `弱 ストリボーグ` が成立する理屈は、`立ち弱P` を最後まで出し切らずに
キャンセルする点にある。`立ち弱P` は発生6F、持続6-8F、硬直10F、ヒット時+4F。
仮に最初の持続で当たった場合、通常ならヒット後に残る自分側の動作は、おおまかに
残り持続2F + 硬直10F = 12F。さらにヒット時+4Fなので、相手の硬直はそのぶん長い。

```text
立ち弱Pが出し切りなら:
残り持続 2F + 硬直 10F + ヒット有利 4F = 16F

弱 ストリボーグ:
発生 16F
```

必殺技キャンセルはこの残り動作を切って `弱 ストリボーグ` を始めるため、弱版の16F発生が
相手の硬直に間に合う、という説明になる。中版は20F、強版は28Fなので、同じ理屈で
当然に入るとは扱えない。

## 実戦上の注意

- `しゃがみ弱P` → `立ち弱P` は、フレーム表の `+4F` だけを見るとリンク不可。連打キャンセル / chain として出す必要がある。
- `立ち弱P` → `弱 ストリボーグ` は、通常技を出し切った後のリンクではなく、必殺技キャンセル。
- 距離、押し戻し、先端ヒット、相手の食らい判定で実戦の安定性は変わる。
- SuperCombo 側では `弱 ストリボーグ` の2段目は1段目より長く、1段目ヒット時に2段目がコンボ安定用に拡大すると説明されている。ただし、公式と重なる基本フレーム値は Capcom 公式 data を優先する。

## 根拠

- [[sources/capcom-official-jp-frame-data]]
- [[sources/supercombo-jp-frame-data]]
- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- `wiki/outputs/data/frame-data/official/jp/classic.json`
- `wiki/outputs/data/frame-data/supercombo/jp/frames.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json`

## 注意 / 不確実性

- この答えは Classic の `弱P` / `↓↘→ + 弱P` 入力を前提にする。Modern では入力と弱ストリボーグのダメージ表示が変わるが、共通技名のフレーム系値はこの capture では一致している。
- この wiki に保存されている JP 公式 capture は 2026-05-26 時点のデータ。後続アップデートで変わる可能性がある。
