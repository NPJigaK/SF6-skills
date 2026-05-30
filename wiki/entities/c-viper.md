---
type: entity
entity_type: character
created: 2026-05-30
updated: 2026-05-30
status: active
sources:
  - "[[sources/capcom-official-c-viper-frame-data]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[concepts/frame-data]]"
aliases:
  - "C. Viper"
  - "C.ヴァイパー"
tags:
  - character
  - frame-data
---

# C. Viper（C.ヴァイパー）

## 要約

C. Viper（C.ヴァイパー） は、この wiki で Capcom 公式フレームデータ capture が保存されている Street Fighter 6 character。公式 frame-data table の data slug は `cviper`。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-30 | 公式 frame-data page を Classic / Modern の raw snapshot として保存し、CSV / field-meaning JSON を派生生成した。 | [[sources/capcom-official-c-viper-frame-data]] |

## 関連する主張

- 公式 capture は Classic 69 行、Modern 67 行の frame-data rows を持つ。
- 入力 icon や Modern control token は `input_token_json` に raw token として保持されている。
- 個別技の値は entity page では要約せず、`wiki/outputs/data/frame-data/cviper/` の CSV と raw DOM を source-preserving data として参照する。
- この capture は自動検証済みだが、人間レビューは未完了。

## 関連概念

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]

## 未解決の質問

- C. Viper（C.ヴァイパー） のどの技データを、再利用できる質問・統合分析として wiki に昇格すべきか。
