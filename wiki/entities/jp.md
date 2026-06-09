---
type: entity
entity_type: character
created: 2026-05-26
updated: 2026-06-10
status: active
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[concepts/frame-data]]"
  - "[[questions/jp-modern-vs-classic-frame-data-moves-and-inputs]]"
  - "[[questions/jp-crouching-light-p-standing-light-p-light-stribog-combo-theory]]"
  - "[[questions/jp-crouching-medium-p-drc-crouching-heavy-p-heavy-stribog-medium-torbalan-triglav-combo-theory]]"
  - "[[syntheses/frame-data-raw-layout]]"
aliases:
  - "JP"
  - "JP"
tags:
  - character
  - frame-data
---

# JP

## 要約

JP は、この wiki で Capcom 公式フレームデータ capture と SuperCombo Wiki raw community frame-data capture が保存されている Street Fighter 6 character。公式 frame-data table の data slug は `jp`。現在の raw entrypoint は `raw/frame-data/official/jp/` と `raw/frame-data/supercombo/jp/`。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-26 | 公式 frame-data page を Classic / Modern の raw snapshot として保存し、JSON output を派生生成した。 | [[sources/capcom-official-jp-frame-data]] |
| 2026-05-31 | SuperCombo Wiki の JP frame-data page を raw wikitext、Cargo API、DOM、5タブ screenshot、画像として保存した。 | [[sources/supercombo-jp-frame-data]] |

## 関連する主張

- 公式 capture は Classic 69 行、Modern 65 行の frame-data rows を持つ。
- official raw は `raw/frame-data/official/jp/manifest.json`、SuperCombo raw は `raw/frame-data/supercombo/jp/manifest.json` から辿る。capture date / source revision は manifest fields で確認する。
- 入力 icon や Modern control token は `input_tokens` に raw token sequence として保持されている。
- 個別技の値は entity page では要約せず、`wiki/outputs/data/frame-data/official/jp/classic.json` / `wiki/outputs/data/frame-data/official/jp/modern.json` の公式 JSON output と raw DOM を source-preserving data として参照する。
- この capture は人間レビューで accepted になっている。
- SuperCombo capture は 64 件の `FrameData-SF6` template と 123 件の resolved image download を保持する。
- SuperCombo raw では `6HPHK` と `236236K` に duplicate input row があるため、input ではなく `moveId` を行識別子として扱う。
- 公式 data と SuperCombo data が重なる項目では、公式 data を正とし、SuperCombo は公式にない補助項目や notes の統合候補として扱う。

## 関連概念

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[syntheses/frame-data-raw-layout]]

## 関連質問

- [[questions/jp-modern-vs-classic-frame-data-moves-and-inputs]]
- [[questions/jp-crouching-light-p-standing-light-p-light-stribog-combo-theory]]
- [[questions/jp-crouching-medium-p-drc-crouching-heavy-p-heavy-stribog-medium-torbalan-triglav-combo-theory]]

## 未解決の質問

- JP のどの技データを、再利用できる質問・統合分析として wiki に昇格すべきか。
- 公式 JP rows と SuperCombo `moveId` rows の crosswalk をどの rule で作るべきか。
