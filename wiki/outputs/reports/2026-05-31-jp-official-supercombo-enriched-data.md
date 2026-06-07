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

Capcom 公式 JP Classic JSON を正として保持したまま、SuperCombo JP の `move_id`、range、juggle、notes、画像、hitbox などを `supercombo_*` 列で付与した enriched output。公式 row を置き換えず、SuperCombo-only rows は別 JSON に分離している。

## 生成ファイル

- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/supercombo-only.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/schema.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/summary.json`

## 方針

| 項目 | 方針 |
|---|---|
| 公式列 | `wiki/outputs/data/frame-data/official/jp/classic.json` の列をそのまま保持する。 |
| SuperCombo 補助列 | すべて `supercombo_*` prefix で追加し、公式値を上書きしない。 |
| review flag | manual match、基本値 conflict、多候補、SuperCombo row reuse を `enrichment_review_flags` に残す。 |
| 人間レビュー | 5件の review-required 候補は人間レビュー済み。公式値を正とし、SuperCombo は補助情報として扱う。 |
| SuperCombo-only rows | 公式 row に直接紐づけず、`supercombo-only.json` に分離する。 |

## サマリー

| 項目 | 値 |
|---|---:|
| 公式 rows | 69 |
| SuperCombo rows | 64 |
| enriched rows | 69 |
| enriched | 62 |
| enriched reviewed | 5 |
| official only | 2 |
| human review accepted | 5 |
| supplemental link decisions | 3 |
| non-additive supplemental damage decisions | 1 |
| conflict supplemental-only decisions | 1 |
| SuperCombo-only rows | 7 |

## 人間レビュー済み行

| 公式 row | 公式技名 | SuperCombo move_id | decision | 方針 |
|---:|---|---|---|---|
| 43 | ヴィーハト・アクノ | `jp_214p_214lp_mp` | `supplemental_link` | 補助リンクとして採用する。公式値は保持する。 |
| 44 | ヴィーハト・チェーニ | `jp_214p_214hp` | `non_additive_supplemental_damage` | ヴィーハトを任意タイミングで発火させる技として扱う。SuperCombo damage 800 は発火した spike damage の補助情報で、元ヴィーハト damage と合算しない。 |
| 54 | SA2 ラヴーシュカ | `jp_214214p` | `conflict_supplemental_only` | 公式 startup 29 を正とし、SuperCombo startup 1 / sequence startup notes は conflict付き補助情報として保持する。 |
| 68 | パリィドライブラッシュ | `jp_mpmk_66_pdr` | `supplemental_link` | cancel/recovery decomposition を補助情報として採用する。 |
| 69 | キャンセルドライブラッシュ | `jp_mpmk_66_drc` | `supplemental_link` | startup/total decomposition を補助情報として採用する。 |

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

- この enriched output は「公式 + 補助情報」であり、公式 JSON を置き換えるものではない。
- `enriched_reviewed` の 5 行は人間レビュー済み。公式列は引き続き正で、SuperCombo 列は補助情報として扱う。
- `ヴィーハト・チェーニ` は non-additive 扱い。`supercombo_damage=800` を元ヴィーハト damage と合算しない。
- `SA2 ラヴーシュカ` は startup conflict が残るため、公式 startup 29 を正とし、SuperCombo startup 1 / projectile sequence は conflict付き補助情報に留める。
- `supercombo_row_reused` は、公式の弱/中/強やジャストパリィ系が SuperCombo の collapsed row に集約されるケースを示す。これは不正とは限らないが、統合時には明示する。

## 根拠

- 公式 source: [[sources/capcom-official-jp-frame-data]]
- SuperCombo source: [[sources/supercombo-jp-frame-data]]
- 候補 crosswalk: [[outputs/reports/2026-05-31-supercombo-jp-official-crosswalk]]
- Enriched summary: `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/summary.json`
- Human review decisions: `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json` の `human_review_*` 列
