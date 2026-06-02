---
type: output
output_type: report
created: 2026-06-02
updated: 2026-06-02
status: active
sources:
  - "[[sources/capcom-official-ingrid-frame-data]]"
  - "[[sources/supercombo-ingrid-frame-data]]"
related:
  - "[[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]"
  - "[[concepts/frame-data]]"
  - "[[entities/ingrid]]"
aliases:
  - "Ingrid official SuperCombo enriched data"
  - "Ingrid 公式 SuperCombo 補助データ"
---

# Ingrid 公式データ + SuperCombo 補助データ - 2026-06-02

## 要約

Capcom 公式 Ingrid Classic CSV を正として保持したまま、SuperCombo Ingrid の `move_id`、range、juggle、notes、画像、hitbox などを `supercombo_*` 列で付与した補助列付き output。公式 row を置き換えず、SuperCombo-only row は別 CSV に分離している。2026-06-02 にレビュー対象 26 行を人間レビュー済みにし、すべて `accepted` とした。

SuperCombo-only 13 行のうち 9 行は、特殊隠しコマンド / Monoid 操作に関係する通常利用外の row である。通常の Ingrid frame-data 質問では公式 row と公式 row に紐づく補助列付き output を優先し、hidden / Dark / Shin Ingrid / Monoid / taunt-summon / SuperCombo-only が明示された場合だけ参照する。

## 生成ファイル

- `wiki/outputs/data/enriched/frame-data/ingrid/classic-supercombo.csv`
- `wiki/outputs/data/enriched/frame-data/ingrid/classic-supercombo.json`
- `wiki/outputs/data/enriched/frame-data/ingrid/supercombo-only.csv`
- `wiki/outputs/data/enriched/frame-data/ingrid/schema.json`
- `wiki/outputs/data/enriched/frame-data/ingrid/summary.json`

## 方針

| 項目 | 方針 |
|---|---|
| 公式列 | `wiki/outputs/data/frame-data/ingrid/classic.csv` の列をそのまま保持する。 |
| SuperCombo 補助列 | すべて `supercombo_*` prefix で追加し、公式値を上書きしない。 |
| レビュー flag | manual match、多候補、SuperCombo row 再利用を `enrichment_review_flags` に残す。 |
| 人間レビュー | Ingrid のレビュー対象 26 行は人間レビュー済み。公式値を正とし、SuperCombo は補助情報として扱う。 |
| SuperCombo-only row | 公式 row に直接紐づけず、`supercombo-only.csv` に分離する。 |
| 特殊隠しコマンド / Monoid row | 通常の Ingrid frame-data 回答には混ぜず、hidden / Dark / Shin Ingrid / Monoid / taunt-summon / SuperCombo-only が明示された質問でだけ参照する。 |

## サマリー

| 項目 | 値 |
|---|---:|
| 公式 row | 75 |
| SuperCombo row | 83 |
| 補助列付き row | 75 |
| `enriched` | 47 |
| `enriched_reviewed` | 26 |
| `official_only` | 2 |
| human review accepted | 26 |
| supplemental link decisions | 4 |
| shared variant supplemental link decisions | 2 |
| stock build supplemental link decisions | 2 |
| stock level supplemental link decisions | 18 |
| SuperCombo-only row | 13 |

## 公式のみの行

| 公式 row | 公式技名 | 理由 |
|---:|---|---|
| 66 | 前方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |
| 67 | 後方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |

## 人間レビュー済み行

| 公式 row | 公式技名 | SuperCombo move_id | decision | 方針 |
|---:|---|---|---|---|
| 26 | サテライトリープ | `ingrid_jhk_jhk` | `supplemental_link` | SuperCombo の jump normal follow-up row を補助情報として紐づける。 |
| 30 | OD 弱 サンシュート | `ingrid_236lpmp` | `shared_variant_supplemental_link` | OD 弱 / 中は SuperCombo の shared row を補助情報として共有する。 |
| 31 | OD 中 サンシュート | `ingrid_236lpmp` | `shared_variant_supplemental_link` | OD 弱 / 中は SuperCombo の shared row を補助情報として共有する。 |
| 32 | OD 強 サンシュート | `ingrid_236mphp` | `supplemental_link` | OD 強 variant の SuperCombo row を補助情報として紐づける。 |
| 33 | 弱 サンフレア | `ingrid_214lp` | `stock_build_supplemental_link` | Sun Crest stock build row として補助情報を保持する。 |
| 34 | サンフレア(Lv1) | `ingrid_214mp` | `stock_level_supplemental_link` | stock level row として補助情報を保持する。 |
| 35 | サンフレア(Lv2) | `ingrid_214hp_1stock` | `stock_level_supplemental_link` | stock level row として補助情報を保持する。 |
| 36 | サンフレア(Lv3) | `ingrid_214hp_2stock` | `stock_level_supplemental_link` | stock level row として補助情報を保持する。 |
| 37 | OD サンフレア(Lv1) | `ingrid_214pp` | `stock_level_supplemental_link` | OD stock level row として補助情報を保持する。 |
| 38 | OD サンフレア(Lv2) | `ingrid_214pp_1stock` | `stock_level_supplemental_link` | OD stock level row として補助情報を保持する。 |
| 39 | OD サンフレア(Lv3) | `ingrid_214pp_2stock` | `stock_level_supplemental_link` | OD stock level row として補助情報を保持する。 |
| 40 | 弱ソーラーフレア | `ingrid_j214lp` | `stock_build_supplemental_link` | air Sun Crest stock build row として補助情報を保持する。 |
| 41 | ソーラーフレア(Lv1) | `ingrid_j214mp` | `stock_level_supplemental_link` | air stock level row として補助情報を保持する。 |
| 42 | ソーラーフレア(Lv2) | `ingrid_j214hp_1stock` | `stock_level_supplemental_link` | air stock level row として補助情報を保持する。 |
| 43 | ソーラーフレア(Lv3) | `ingrid_j214hp_2stock` | `stock_level_supplemental_link` | air stock level row として補助情報を保持する。 |
| 44 | OD ソーラーフレア(Lv1) | `ingrid_j214pp` | `stock_level_supplemental_link` | OD air stock level row として補助情報を保持する。 |
| 45 | OD ソーラーフレア(Lv2) | `ingrid_j214pp_1stock` | `stock_level_supplemental_link` | OD air stock level row として補助情報を保持する。 |
| 46 | OD ソーラーフレア(Lv3) | `ingrid_j214pp_2stock` | `stock_level_supplemental_link` | OD air stock level row として補助情報を保持する。 |
| 56 | SA1 サンシャイン(Lv1) | `ingrid_236236k_0stock` | `stock_level_supplemental_link` | SA1 stock level row として補助情報を保持する。 |
| 57 | SA1 サンシャイン(Lv2) | `ingrid_236236k_hold_1stock` | `stock_level_supplemental_link` | SA1 hold / stock level row として補助情報を保持する。 |
| 58 | SA1 サンシャイン(Lv3) | `ingrid_236236k_hold_2stock` | `stock_level_supplemental_link` | SA1 hold / stock level row として補助情報を保持する。 |
| 59 | SA2 サンオーダー(Lv1) | `ingrid_214214p_0stock` | `stock_level_supplemental_link` | SA2 stock level row として補助情報を保持する。公式 startup marker `※` と total 13 は上書きしない。 |
| 60 | SA2 サンオーダー(Lv2) | `ingrid_214214p_hold_1stock` | `stock_level_supplemental_link` | SA2 hold / stock level row として補助情報を保持する。公式 startup marker `※` と total 13 は上書きしない。 |
| 61 | SA2 サンオーダー(Lv3) | `ingrid_214214p_hold_2stock` | `stock_level_supplemental_link` | SA2 hold / stock level row として補助情報を保持する。公式 startup marker `※` と total 13 は上書きしない。 |
| 74 | パリィドライブラッシュ | `ingrid_mpmk_66_pdr` | `supplemental_link` | SuperCombo の startup/recovery/total 分解は公式全体値の置換ではなく補助情報として扱う。 |
| 75 | キャンセルドライブラッシュ | `ingrid_mpmk_66_drc` | `supplemental_link` | SuperCombo の startup/recovery/total 分解は公式全体値の置換ではなく補助情報として扱う。 |

## review flag の扱い

| flag | 件数/扱い |
|---|---|
| `manual_match` | 26 件。Ingrid の Sun Crest stock level、OD Sun Shot 共有 row、SA1 / SA2 stock level、Drive Rush などを name override で対応させ、人間レビューで accepted にした。 |
| `multiple_candidates` | 10 件。候補集合は残すが、accepted 行は `human_review_*` 列で明示している。 |
| `supercombo_row_reused` | 5 件。OD 弱 / 中 Sun Shot と Drive Rush 系の共有候補を、補助リンクとして accepted にした。 |

## SuperCombo-only 行

| 分類 | 件数 | 内容 |
|---|---:|---|
| supercombo_only_taunt | 4 | `ingrid_5pppkkk`, `ingrid_6pppkkk`, `ingrid_4pppkkk`, `ingrid_2pppkkk` |
| supercombo_only | 9 | 特殊隠しコマンド / Monoid 操作に関係する通常利用外の row。`ingrid_22ppp`, `ingrid_214214k`, `ingrid_360kk`, `ingrid_monoid_l`, `ingrid_monoid_m`, `ingrid_monoid_h`, `ingrid_monoid_hphk`, `ingrid_monoid_jx`, `ingrid_monoid_super` |

## 注意点

- この補助列付き output は「公式 + 補助情報」であり、公式 CSV を置き換えるものではない。
- 公式列と補助列付き output の公式由来列は全行一致する。SuperCombo の数値は `supercombo_*` 補助列にのみ入れる。
- SuperCombo-only 9 行は特殊隠しコマンド / Monoid 操作に関係するため、通常の Ingrid frame-data 回答には混ぜない。
- Ingrid 専用 name override 26 件は人間レビュー済みで accepted。公式値を正とし、SuperCombo は補助情報として扱う。
- `前方ステップ` / `後方ステップ` は official only。SuperCombo 側の movement data は `character.csv` の dash fields を確認する。
- Ingrid は imageinfo missing 156 件が残るため、hitbox / move 画像の利用には追加確認が必要。

## 根拠

- 公式 source（根拠）: [[sources/capcom-official-ingrid-frame-data]]
- SuperCombo source（根拠）: [[sources/supercombo-ingrid-frame-data]]
- 候補照合: [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]
- 補助列付き summary: `wiki/outputs/data/enriched/frame-data/ingrid/summary.json`
- Human review decisions: `wiki/outputs/data/enriched/frame-data/ingrid/classic-supercombo.csv` の `human_review_*` 列
