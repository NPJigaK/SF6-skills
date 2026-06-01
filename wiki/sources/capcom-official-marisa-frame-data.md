---
type: source
source_type: official_frame_data
title: "Capcom 公式 Marisa（マリーザ） フレームデータ"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/frame-data/official/marisa/manifest.json"
original_url: "https://www.streetfighter.com/6/ja-jp/character/marisa/frame"
created: 2026-05-30
updated: 2026-06-01
captured_at_utc: "2026-05-30T06:56:58Z"
status: active
confidence: high
tags:
  - sf6
  - official
  - frame-data
aliases:
  - "Marisa frame data"
  - "マリーザ フレームデータ"
related_concepts:
  - "[[concepts/frame-data]]"
related_entities:
  - "[[entities/capcom]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/marisa]]"
---

# ソース: Capcom 公式 Marisa（マリーザ） フレームデータ

## 1行要約

Capcom 公式サイトの Marisa（マリーザ） フレームデータを、Classic / Modern の raw HTML、DOM、screenshot、metadata として保存し、CSV と field-meaning JSON に派生抽出した source page。

## 重要ポイント

1. raw snapshot は `raw/frame-data/official/marisa/` 配下の latest mirror 固定パスに保存されている。capture date はパスではなく manifest の `capture_label` で追う。`raw/` は原本保存層なので、この wiki 再コンパイルでは変更しない。
2. Classic は 91 行、Modern は 80 行の技データを持つ。
3. 派生 CSV は技名、入力 token 表示、入力 token JSON、発生、持続、硬直、ヒット/ガード硬直差、キャンセル、ダメージ、補正、Drive gauge、SA 増加、属性、備考を保持する。
4. 表ヘッダの説明は `wiki/outputs/data/frame-data/marisa/classic.field-meanings.json` と `wiki/outputs/data/frame-data/marisa/modern.field-meanings.json` に分離して保存されている。
5. この capture の review 状態は「自動検証済み。人間レビューは未完了」。

## 重要な主張

| 主張 | 根拠 | 信頼度 | メモ |
|---|---|---|---|
| publisher は Capcom で、source URL は公式 Street Fighter 6 サイトの Marisa（マリーザ） frame page。 | `raw/frame-data/official/marisa/manifest.json`; `raw/frame-data/official/marisa/*/metadata.json` | high | metadata が publisher、locale、source URL、character slug、control scheme を記録している。 |
| Classic と Modern は同じ公式 page の別 tab として保存されている。 | `raw/frame-data/official/marisa/classic/metadata.json`; `raw/frame-data/official/marisa/modern/metadata.json` | high | metadata が Classic tab index 0、Modern tab index 1 を記録している。 |
| 派生データは Classic 91 行、Modern 80 行。 | `raw/frame-data/official/marisa/manifest.json`; `wiki/outputs/data/frame-data/marisa/classic.csv`; `wiki/outputs/data/frame-data/marisa/modern.csv` | high | CSV 行数は raw DOM 由来の table row count と対応する。 |
| field meanings は per-move CSV とは別に保存されている。 | `wiki/outputs/data/frame-data/marisa/classic.field-meanings.json`; `wiki/outputs/data/frame-data/marisa/modern.field-meanings.json` | high | Classic 7 records、Modern 8 records。 |

## 関連概念

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[concepts/drive-system]]

## 関連エンティティ

- [[entities/capcom]]
- [[entities/street-fighter-6]]
- [[entities/marisa]]

## 既存 wiki との矛盾または更新

- 個別技の値は、この source page では要約しない。再利用できる質問や統合分析が必要になった時に、raw DOM と派生 CSV から必要な範囲だけ昇格する。
- `input_raw_display` は raw DOM token の表示であり、正規化されたコマンド表記ではない。

## 未解決の質問

- この character のどの技データを、CSV から durable な技別 wiki page または synthesis に昇格すべきか。

## ソースメモ

- Raw manifest: `raw/frame-data/official/marisa/manifest.json`
- Classic raw capture: `raw/frame-data/official/marisa/classic/`
- Modern raw capture: `raw/frame-data/official/marisa/modern/`
- Derived Classic CSV: `wiki/outputs/data/frame-data/marisa/classic.csv`
- Derived Modern CSV: `wiki/outputs/data/frame-data/marisa/modern.csv`
- Derived field meanings:
  - `wiki/outputs/data/frame-data/marisa/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/marisa/modern.field-meanings.json`
