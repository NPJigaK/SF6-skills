---
type: output
output_type: report
created: 2026-05-31
updated: 2026-05-31
status: active
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
related:
  - "[[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]]"
  - "[[concepts/frame-data]]"
  - "[[entities/jp]]"
aliases:
  - "JP official SuperCombo enriched data"
  - "JP 公式 SuperCombo 補助データ"
---

# JP 公式データ + SuperCombo 補助データ - 2026-05-31

## 要約

Capcom 公式 JP Classic CSV を正として保持したまま、SuperCombo JP の `move_id`、range、juggle、notes、画像、hitbox などを `supercombo_*` 列で付与した enriched output。公式 row を置き換えず、SuperCombo-only rows は別 CSV に分離している。

## 生成ファイル

- `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.csv`
- `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.json`
- `wiki/outputs/data/enriched/frame-data/jp/supercombo-only.csv`
- `wiki/outputs/data/enriched/frame-data/jp/schema.json`
- `wiki/outputs/data/enriched/frame-data/jp/summary.json`

## 方針

| 項目 | 方針 |
|---|---|
| 公式列 | `wiki/outputs/data/frame-data/jp/classic.csv` の列をそのまま保持する。 |
| SuperCombo 補助列 | すべて `supercombo_*` prefix で追加し、公式値を上書きしない。 |
| review flag | manual match、基本値 conflict、多候補、SuperCombo row reuse を `enrichment_review_flags` に残す。 |
| SuperCombo-only rows | 公式 row に直接紐づけず、`supercombo-only.csv` に分離する。 |

## サマリー

| 項目 | 値 |
|---|---:|
| 公式 rows | 69 |
| SuperCombo rows | 64 |
| enriched rows | 69 |
| enriched | 62 |
| enriched review required | 5 |
| official only | 2 |
| SuperCombo-only rows | 7 |

## Review Required Rows

| 公式 row | 公式技名 | SuperCombo move_id | 理由 |
|---:|---|---|---|
| 43 | ヴィーハト・アクノ | `jp_214p_214lp_mp` | JP 固有名 override。 |
| 44 | ヴィーハト・チェーニ | `jp_214p_214hp` | JP 固有名 override、damage conflict。 |
| 54 | SA2 ラヴーシュカ | `jp_214214p` | startup conflict。 |
| 68 | パリィドライブラッシュ | `jp_mpmk_66_pdr` | JP 固有名 override。 |
| 69 | キャンセルドライブラッシュ | `jp_mpmk_66_drc` | JP 固有名 override。 |

## Official Only Rows

| 公式 row | 公式技名 | 理由 |
|---:|---|---|
| 60 | 前方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |
| 61 | 後方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |

## SuperCombo-only Rows

| 分類 | 件数 | 内容 |
|---|---:|---|
| supplemental_variant_row | 2 | `jp_214pp_214hp`, `jp_236k_hold` |
| supplemental_followup_row | 2 | `jp_22k_bomb`, `jp_22kk_bomb` |
| supercombo_only_taunt | 3 | `jp_5pppkkk`, `jp_6pppkkk`, `jp_4pppkkk` |

## 注意点

- この enriched output は「公式 + 補助情報」であり、公式 CSV を置き換えるものではない。
- `enriched_review_required` の 5 行は、人間レビューなしに最終 merge policy へ昇格しない。
- `supercombo_row_reused` は、公式の弱/中/強やジャストパリィ系が SuperCombo の collapsed row に集約されるケースを示す。これは不正とは限らないが、統合時には明示する。

## 根拠

- 公式 source: [[sources/capcom-official-jp-frame-data]]
- SuperCombo source: [[sources/supercombo-jp-frame-data]]
- 候補 crosswalk: [[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]]
- Enriched summary: `wiki/outputs/data/enriched/frame-data/jp/summary.json`
