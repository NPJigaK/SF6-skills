---
type: entity
entity_type: character
created: 2026-05-30
updated: 2026-05-30
status: active
sources:
  - "[[sources/capcom-official-e-honda-frame-data]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[concepts/frame-data]]"
aliases:
  - "E. Honda"
  - "エドモンド本田"
tags:
  - character
  - frame-data
---

# E. Honda（エドモンド本田）

## 要約

E. Honda（エドモンド本田） は、この wiki で Capcom 公式フレームデータ capture が保存されている Street Fighter 6 character。公式 frame-data table の data slug は `ehonda`。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-30 | 公式 frame-data page を Classic / Modern の raw snapshot として保存し、CSV / field-meaning JSON を派生生成した。 | [[sources/capcom-official-e-honda-frame-data]] |

## 関連する主張

- 公式 capture は Classic 70 行、Modern 65 行の frame-data rows を持つ。
- 入力 icon や Modern control token は `input_token_json` に raw token として保持されている。
- 個別技の値は entity page では要約せず、`wiki/outputs/data/frame-data/ehonda/` の CSV と raw DOM を source-preserving data として参照する。
- この capture は自動検証済みだが、人間レビューは未完了。

## 関連概念

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]

## 未解決の質問

- E. Honda（エドモンド本田） のどの技データを、再利用できる質問・統合分析として wiki に昇格すべきか。
