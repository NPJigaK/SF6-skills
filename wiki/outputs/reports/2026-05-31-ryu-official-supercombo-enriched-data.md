---
type: output
output_type: report
created: 2026-05-31
updated: 2026-06-01
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

- `wiki/outputs/data/frame-data/official-supercombo-enriched/ryu/classic-supercombo.csv`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/ryu/classic-supercombo.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/ryu/supercombo-only.csv`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/ryu/schema.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/ryu/summary.json`

## 方針

| 項目 | 方針 |
|---|---|
| 公式列 | `wiki/outputs/data/frame-data/official/ryu/classic.csv` の列をそのまま保持する。 |
| SuperCombo 補助列 | すべて `supercombo_*` prefix で追加し、公式値を上書きしない。 |
| review flag | ambiguous match、manual match、基本値 conflict、多候補、SuperCombo row reuse を `enrichment_review_flags` に残す。 |
| 人間レビュー | Ryu の review 対象 13件は人間レビュー済み。公式値を正としたまま補助リンクとして採用する。 |
| SuperCombo-only rows | 公式 row に直接紐づけず、`supercombo-only.csv` に分離する。 |

## サマリー

| 項目 | 値 |
|---|---:|
| 公式 rows | 75 |
| SuperCombo rows | 77 |
| enriched rows | 75 |
| enriched | 60 |
| enriched reviewed | 13 |
| official only | 2 |
| SuperCombo-only rows | 6 |

## レビュー反映済み行

| 公式 row | 公式技名 | SuperCombo move_id | decision | 数値方針 |
|---:|---|---|---|---|
| 30 | [電刃錬気]波動拳 | `ryu_236p(charged)` | `supplemental_link` | SC damage `500x2` は公式 damage 1000 の分解情報。公式 damage を保持する。 |
| 31 | OD 波動拳 | `ryu_236pp` | `supplemental_link` | SC damage `500x2` は公式 damage 1000 の分解情報。公式 damage を保持する。 |
| 32 | [電刃錬気]OD 波動拳 | `ryu_236pp(charged)` | `supplemental_link` | SC damage `400x3 (1200)`、total 38、block +2 は公式値と対応する。 |
| 50 | [電刃錬気]波掌撃 | `ryu_214p(charged)` | `supplemental_link` | SC damage `400x2` は公式 damage 800 の分解情報。SC recovery `19(31)` は補助分解として扱う。 |
| 51 | OD 波掌撃 | `ryu_214pp` | `conflict_supplemental_only` | 公式 active `18-22` と SC active 6 は単純一致しないため、公式 active を正とする。 |
| 54 | SA1 真空波動拳 | `ryu_236236p` | `supplemental_link` | SC damage `400x5 (2000)`、total 86、block -24 は公式値と対応する。 |
| 55 | [電刃錬気]SA1 真空波動拳 | `ryu_236236p_denjin` | `supplemental_link` | SC damage `200x7,1000 (2400)` と total 89 は公式値と対応する。 |
| 57 | SA2 真波掌撃（Lv2） | `ryu_214214p_lv2` | `hold_level_supplemental_link` | SC damage 2900 は公式と一致。SC startup `18~` は hold-level 補助情報で、公式 startup 20 を保持する。 |
| 58 | SA2 真波掌撃（Lv3） | `ryu_214214p_lv3` | `hold_level_supplemental_link` | SC damage 3000 は公式と一致。SC startup `50~` は hold-level 補助情報で、公式 startup 70 を保持する。 |
| 60 | [電刃錬気]SA2 真波掌撃（Lv2） | `ryu_214214p_denjin_lv2` | `hold_level_supplemental_link` | SC damage 3300 は公式と一致。SC startup `18~` は hold-level 補助情報で、公式 startup 20 を保持する。 |
| 61 | [電刃錬気]SA2 真波掌撃（Lv3） | `ryu_214214p_denjin_lv3` | `hold_level_supplemental_link` | SC damage 3400 は公式と一致。SC startup `50~` は hold-level 補助情報で、公式 startup 70 を保持する。 |
| 74 | パリィドライブラッシュ | `ryu_mpmk_66_pdr` | `supplemental_link` | SC の startup/recovery/total 分解は公式全体45Fの置換ではなく補助情報。 |
| 75 | キャンセルドライブラッシュ | `ryu_mpmk_66_drc` | `supplemental_link` | SC total `24(46)` の括弧内 total は公式全体46Fと対応する。 |

## 公式のみの行

| 公式 row | 公式技名 | 理由 |
|---:|---|---|
| 66 | 前方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |
| 67 | 後方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |

## SuperCombo-only 行

| 分類 | 件数 | 内容 |
|---|---:|---|
| supplemental_variant_row | 2 | `6HK~214K` / `6HK~214KK` の Aerial Tatsumaki Senpu-kyaku 条件付き派生。 |
| supercombo_only_taunt | 4 | `ryu_5pppkkk`, `ryu_6pppkkk`, `ryu_4pppkkk`, `ryu_2pppkkk` |

## SuperCombo-only variant links

| SuperCombo move_id | primary official row | enabled by | 方針 |
|---|---|---|---|
| `ryu_6hk_214k` | 41 `空中竜巻旋風脚` | 23 `旋風脚` | `6HK` からキャンセルした空中竜巻旋風脚の条件付き variant。row 23 の `旋風脚` damage 800 / startup 16 とは混ぜない。 |
| `ryu_6hk_214kk` | 42 `OD 空中竜巻旋風脚` | 23 `旋風脚` | `6HK` からキャンセルした OD 空中竜巻旋風脚の条件付き variant。row 23 の `旋風脚` damage 800 / startup 16 とは混ぜない。 |

## 注意点

- この enriched output は「公式 + 補助情報」であり、公式 CSV を置き換えるものではない。
- 公式列と enriched output の公式由来列は全行一致する。SuperCombo の数値は `supercombo_*` 補助列にのみ入れる。
- Denjin / hold level の対応は `move_id` で明示し、同じ input の別 variant を混同しない。
- `6HK~214K` / `6HK~214KK` は SuperCombo-only に残したまま、primary official row と enabled-by row を分けて記録する。`旋風脚` 本体の数値と空中竜巻派生の数値は合算・上書きしない。
- SA2 Lv2 / Lv3 の SuperCombo startup `18~` / `50~` は hold-level 補助情報であり、公式 startup 20 / 70 を上書きしない。
- OD 波掌撃の active duration は conflict 付き補助情報として保持し、公式 active `18-22` を正とする。
- `パリィドライブラッシュ` と `キャンセルドライブラッシュ` は accepted だが、SuperCombo の cancel/recovery decomposition は公式全体フレームの置換ではない。

## 根拠

- 公式 source: [[sources/capcom-official-ryu-frame-data]]
- SuperCombo source: [[sources/supercombo-ryu-frame-data]]
- 候補 crosswalk: [[outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk]]
- Enriched summary: `wiki/outputs/data/frame-data/official-supercombo-enriched/ryu/summary.json`
