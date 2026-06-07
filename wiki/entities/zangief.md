---
type: entity
entity_type: character
created: 2026-05-27
updated: 2026-06-08
status: active
sources:
  - "[[sources/capcom-official-zangief-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[concepts/frame-data]]"
  - "[[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]]"
  - "[[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]]"
aliases:
  - "Zangief"
  - "ザンギエフ"
tags:
  - character
  - frame-data
---

# Zangief（ザンギエフ）

## 要約

Zangief（ザンギエフ） は、この wiki で Capcom 公式フレームデータ取得データと SuperCombo Wiki community frame-data 取得データが保存されている Street Fighter 6 character。公式 frame-data table の data slug は `zangief`。

## 年表

| 日付 | 出来事 | ソース |
|---|---|---|
| 2026-05-27 | 公式 frame-data page を Classic / Modern の raw snapshot として保存し、JSON output を派生生成した。 | [[sources/capcom-official-zangief-frame-data]] |
| 2026-06-02 | SuperCombo Wiki の Zangief frame-data page を raw wikitext、Cargo API、DOM、5タブのスクリーンショット、画像として保存し、公式 Classic との照合 / 補助列付き output を生成した。 | [[sources/supercombo-zangief-frame-data]], [[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]], [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] |

## 関連する主張

- 公式 capture は Classic 72 行、Modern 66 行の frame-data rows を持つ。
- SuperCombo 取得データは `FrameData-SF6` 68 行、character template 1 件、表示 table comparisons 20 件を持つ。
- 公式 Classic との SuperCombo 照合は 46 件の自動一致、24 件の name override による一致、2 件の公式側未照合を含む。公式側未照合は前方ステップ / 後方ステップ。
- 入力 icon や Modern control token は `input_tokens` に raw token sequence として保持されている。
- 個別技の値は entity page では要約せず、`wiki/outputs/data/frame-data/official/zangief/classic.json` / `wiki/outputs/data/frame-data/official/zangief/modern.json` の公式 JSON output と raw DOM を source-preserving data として参照する。
- 公式 capture は人間レビューで accepted になっている。
- SuperCombo 補助列付き output はレビュー済みで、公式列を上書きしない。Zangief 専用 name override 24 件を含むレビュー対象 25 行は `accepted` 済み。

## 関連概念

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]

## 未解決の質問

- Zangief（ザンギエフ） のどの技データを、再利用できる質問・統合分析として wiki に昇格すべきか。
- SuperCombo の `imageinfo` missing 4 件を source 側の欠損として扱うか、filename 正規化で再解決できるか。
