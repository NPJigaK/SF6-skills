---
type: entity
entity_type: character
created: 2026-05-27
updated: 2026-06-10
status: active
sources:
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[concepts/frame-data]]"
  - "[[questions/ryu-modern-vs-classic-frame-data-moves-and-inputs]]"
  - "[[syntheses/frame-data-raw-layout]]"
aliases:
  - "Ryu"
  - "リュウ"
tags:
  - character
  - frame-data
---

# Ryu（リュウ）

## 要約

Ryu（リュウ） は、この wiki で Capcom 公式フレームデータ capture と SuperCombo Wiki community frame-data capture が保存されている Street Fighter 6 character。公式 frame-data table の data slug は `ryu`。現在の raw entrypoint は `raw/frame-data/official/ryu/` と `raw/frame-data/supercombo/ryu/`。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-27 | 公式 frame-data page を Classic / Modern の raw snapshot として保存し、JSON output を派生生成した。 | [[sources/capcom-official-ryu-frame-data]] |
| 2026-05-31 | SuperCombo frame-data page を raw wikitext、Cargo API、表示 DOM、tab screenshots、画像として保存し、公式 Classic との候補 crosswalk と enriched output を作成した。 | [[sources/supercombo-ryu-frame-data]], [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]], [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]] |

## 関連する主張

- 公式 capture は Classic 75 行、Modern 69 行の frame-data rows を持つ。
- official raw は `raw/frame-data/official/ryu/manifest.json`、SuperCombo raw は `raw/frame-data/supercombo/ryu/manifest.json` から辿る。capture date / source revision は manifest fields で確認する。
- 入力 icon や Modern control token は `input_tokens` に raw token sequence として保持されている。
- 個別技の値は entity page では要約せず、`wiki/outputs/data/frame-data/official/ryu/classic.json` / `wiki/outputs/data/frame-data/official/ryu/modern.json` の公式 JSON output と raw DOM を source-preserving data として参照する。
- この capture は人間レビューで accepted になっている。
- SuperCombo Ryu capture は `FrameData-SF6` 77 rows と `CharacterData-SF6` 1 row を含み、自動 validation は passed。
- Ryu enriched output は公式 Classic 75 rows を保持し、SuperCombo 補助列を付与する。13 rows は人間レビュー済みの `enriched_reviewed` として保持し、公式数値を上書きしない。

## 関連概念

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[syntheses/frame-data-raw-layout]]

## 関連質問

- [[questions/ryu-modern-vs-classic-frame-data-moves-and-inputs]]

## 未解決の質問

- Ryu（リュウ） のどの技データを、再利用できる質問・統合分析として wiki に昇格すべきか。
- SuperCombo-only conditional variant link を他 character にも使う場合、どこまで汎用 schema 化するか。
