---
type: output
output_type: report
created: 2026-05-31
updated: 2026-05-31
status: active
sources:
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/supercombo-ryu-frame-data]]"
related:
  - "[[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]]"
  - "[[concepts/frame-data]]"
  - "[[entities/ryu]]"
aliases:
  - "Ryu official SuperCombo enriched data"
  - "Ryu 公式 SuperCombo 補助データ"
---

# Ryu 公式データ + SuperCombo 補助データ - 2026-05-31

## 要約

Capcom 公式 Ryu Classic CSV を正として保持したまま、SuperCombo Ryu の `move_id`、range、juggle、notes、画像、hitbox などを `supercombo_*` 列で付与した enriched output。公式 row を置き換えず、SuperCombo-only rows は別 CSV に分離している。

## 生成ファイル

- `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.csv`
- `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.json`
- `wiki/outputs/data/enriched/frame-data/ryu/supercombo-only.csv`
- `wiki/outputs/data/enriched/frame-data/ryu/schema.json`
- `wiki/outputs/data/enriched/frame-data/ryu/summary.json`

## 方針

| 項目 | 方針 |
|---|---|
| 公式列 | `wiki/outputs/data/frame-data/ryu/classic.csv` の列をそのまま保持する。 |
| SuperCombo 補助列 | すべて `supercombo_*` prefix で追加し、公式値を上書きしない。 |
| review flag | ambiguous match、manual match、基本値 conflict、多候補、SuperCombo row reuse を `enrichment_review_flags` に残す。 |
| 人間レビュー | Ryu の review-required 13件は未承認。accepted 扱いにしない。 |
| SuperCombo-only rows | 公式 row に直接紐づけず、`supercombo-only.csv` に分離する。 |

## サマリー

| 項目 | 値 |
|---|---:|
| 公式 rows | 75 |
| SuperCombo rows | 77 |
| enriched rows | 75 |
| enriched | 60 |
| enriched review required | 13 |
| official only | 2 |
| SuperCombo-only rows | 14 |

## レビュー対象行

| 公式 row | 公式技名 | SuperCombo move_id | review flags | conflict |
|---:|---|---|---|---|
| 30 | [電刃錬気]波動拳 | `ryu_236hp` | `ambiguous_match;basic_field_conflict:damage;multiple_candidates;supercombo_row_reused` | damage |
| 31 | OD 波動拳 | `ryu_236pp` | `ambiguous_match;multiple_candidates;supercombo_row_reused` |  |
| 32 | [電刃錬気]OD 波動拳 | `ryu_236pp` | `ambiguous_match;multiple_candidates;supercombo_row_reused` |  |
| 50 | [電刃錬気]波掌撃 | `ryu_214mp` | `ambiguous_match;basic_field_conflict:recovery,startup;multiple_candidates;supercombo_row_reused` | recovery,startup |
| 51 | OD 波掌撃 | `ryu_214pp` | `basic_field_conflict:active_duration;multiple_candidates` | active_duration |
| 54 | SA1 真空波動拳 | `ryu_236236p` | `ambiguous_match;multiple_candidates;supercombo_row_reused` |  |
| 55 | [電刃錬気]SA1 真空波動拳 | `ryu_236236p` | `ambiguous_match;multiple_candidates;supercombo_row_reused` |  |
| 57 | SA2 真波掌撃（Lv2） | `ryu_214214p` | `ambiguous_match;basic_field_conflict:damage,startup;multiple_candidates;supercombo_row_reused` | damage,startup |
| 58 | SA2 真波掌撃（Lv3） | `ryu_214214p` | `ambiguous_match;basic_field_conflict:damage,startup;multiple_candidates;supercombo_row_reused` | damage,startup |
| 60 | [電刃錬気]SA2 真波掌撃（Lv2） | `ryu_214214p` | `ambiguous_match;basic_field_conflict:damage,startup;multiple_candidates;supercombo_row_reused` | damage,startup |
| 61 | [電刃錬気]SA2 真波掌撃（Lv3） | `ryu_214214p` | `ambiguous_match;basic_field_conflict:damage,startup;multiple_candidates;supercombo_row_reused` | damage,startup |
| 74 | パリィドライブラッシュ | `ryu_mpmk_66_pdr` | `manual_match` |  |
| 75 | キャンセルドライブラッシュ | `ryu_mpmk_66_drc` | `manual_match` |  |

## 公式のみの行

| 公式 row | 公式技名 | 理由 |
|---:|---|---|
| 66 | 前方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |
| 67 | 後方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |

## SuperCombo-only 行

| 分類 | 件数 | 内容 |
|---|---:|---|
| supercombo_only | 10 | Denjin / charged / hold / follow-up variants。 |
| supercombo_only_taunt | 4 | `ryu_5pppkkk`, `ryu_6pppkkk`, `ryu_4pppkkk`, `ryu_2pppkkk` |

## 注意点

- この enriched output は「公式 + 補助情報」であり、公式 CSV を置き換えるものではない。
- `enriched_review_required` の 13 行は、人間レビューなしに最終 merge policy へ昇格しない。
- `パリィドライブラッシュ` と `キャンセルドライブラッシュ` は generic name override で紐づいたが、Ryu ではまだ accepted ではない。
- Denjin / hold level / duplicate input の粒度差があるため、damage や startup conflict は単純な数値ミスと断定しない。
- `supercombo_row_reused` は、公式の Denjin / hold level などが SuperCombo の collapsed row に集約されるケースを示す。これは不正とは限らないが、統合時には明示する。

## 根拠

- 公式 source: [[sources/capcom-official-ryu-frame-data]]
- SuperCombo source: [[sources/supercombo-ryu-frame-data]]
- 候補 crosswalk: [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]]
- Enriched summary: `wiki/outputs/data/enriched/frame-data/ryu/summary.json`
