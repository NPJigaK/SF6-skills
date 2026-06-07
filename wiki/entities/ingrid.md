---
type: entity
entity_type: character
created: 2026-05-30
updated: 2026-06-08
status: active
sources:
  - "[[sources/capcom-official-ingrid-frame-data]]"
  - "[[sources/supercombo-ingrid-frame-data]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[concepts/frame-data]]"
  - "[[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]"
  - "[[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]"
aliases:
  - "Ingrid"
  - "イングリッド"
tags:
  - character
  - frame-data
---

# Ingrid（イングリッド）

## 要約

Ingrid（イングリッド） は、この wiki で Capcom 公式フレームデータ capture、SuperCombo community raw frame-data 取得データ、公式 Classic + SuperCombo 補助データが保存されている Street Fighter 6 character。公式 frame-data table の data slug は `ingrid`。SuperCombo raw は `raw/frame-data/supercombo/ingrid/` にある。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-30 | 公式 frame-data page を Classic / Modern の raw snapshot として保存し、JSON output を派生生成した。 | [[sources/capcom-official-ingrid-frame-data]] |
| 2026-06-02 | SuperCombo Wiki の Ingrid frame-data page を raw wikitext、Cargo API、DOM、5タブのスクリーンショット、画像参照情報として保存した。 | [[sources/supercombo-ingrid-frame-data]] |
| 2026-06-02 | SuperCombo 派生 output、公式 Classic との crosswalk、公式 + SuperCombo 補助 output を作成し、レビュー対象 26 行を accepted にした。 | [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]], [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] |

## 関連する主張

- 公式 capture は Classic 75 行、Modern 74 行の frame-data rows を持つ。
- SuperCombo raw capture は 1 件の character template、83 件の frame template、20 件の DOM table comparison を含む。
- SuperCombo raw capture は imageinfo で face / portrait の 2 件だけ解決でき、156 title は missing だった。
- 公式 Classic 75 rows と SuperCombo 83 rows の crosswalk は、自動一致 47、レビュー済み name override 一致 26、公式側未照合 2。
- 補助列付き output は `enriched` 47、`enriched_reviewed` 26、`official_only` 2。`enriched_review_required` は 0。
- 入力 icon や Modern control token は `input_tokens` に raw token sequence として保持されている。
- 個別技の値は entity page では要約せず、`wiki/outputs/data/frame-data/official/ingrid/classic.json` / `wiki/outputs/data/frame-data/official/ingrid/modern.json` の公式 JSON output、`wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/classic-supercombo.json` / `wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/supercombo-only.json` の補助列付き JSON output、raw DOM を source-preserving data として参照する。
- SuperCombo 補助データのレビュー対象 26 行は人間レビュー済み accepted。raw capture review は imageinfo missing と SuperCombo-only 行の扱いが残るため open。

## 関連概念

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]

## 未解決の質問

- Ingrid（イングリッド） のどの技データを、再利用できる質問・統合分析として wiki に昇格すべきか。
- SuperCombo Ingrid の公式 row に直接照合しない Monoid など 9 行を、extra / hidden / community-only data としてどう扱うか。
- SuperCombo Ingrid の imageinfo missing 156 件を filename 正規化で再解決できるか。
