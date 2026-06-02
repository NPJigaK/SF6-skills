---
type: output
output_type: report
created: 2026-06-02
updated: 2026-06-02
status: active
sources:
  - "[[sources/capcom-official-zangief-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
related:
  - "[[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]]"
  - "[[concepts/frame-data]]"
  - "[[entities/zangief]]"
aliases:
  - "Zangief official SuperCombo enriched data"
  - "Zangief 公式 SuperCombo 補助データ"
---

# Zangief 公式データ + SuperCombo 補助データ - 2026-06-02

## 要約

Capcom 公式 Zangief Classic CSV を正として保持したまま、SuperCombo Zangief の `move_id`、range、juggle、notes、画像、hitbox などを `supercombo_*` 列で付与した補助列付き output。公式 row を置き換えず、SuperCombo-only row は別 CSV に分離している。2026-06-02 にレビュー対象 25 行を人間レビュー済みにし、すべて `accepted` とした。

## 生成ファイル

- `wiki/outputs/data/enriched/frame-data/zangief/classic-supercombo.csv`
- `wiki/outputs/data/enriched/frame-data/zangief/classic-supercombo.json`
- `wiki/outputs/data/enriched/frame-data/zangief/supercombo-only.csv`
- `wiki/outputs/data/enriched/frame-data/zangief/schema.json`
- `wiki/outputs/data/enriched/frame-data/zangief/summary.json`

## 方針

| 項目 | 方針 |
|---|---|
| 公式列 | `wiki/outputs/data/frame-data/zangief/classic.csv` の列をそのまま保持する。 |
| SuperCombo 補助列 | すべて `supercombo_*` prefix で追加し、公式値を上書きしない。 |
| レビュー flag | manual match、基本値 conflict、多候補、SuperCombo row 再利用を `enrichment_review_flags` に残す。 |
| 人間レビュー | Zangief のレビュー対象 25 行は人間レビュー済み。公式値を正とし、SuperCombo は補助情報として扱う。 |
| SuperCombo-only row | 公式 row に直接紐づけず、`supercombo-only.csv` に分離する。 |

## サマリー

| 項目 | 値 |
|---|---:|
| 公式 row | 72 |
| SuperCombo row | 68 |
| 補助列付き row | 72 |
| `enriched` | 45 |
| `enriched_reviewed` | 25 |
| `official_only` | 2 |
| human review accepted | 25 |
| supplemental link decisions | 19 |
| hold supplemental link decisions | 3 |
| movement variant supplemental link decisions | 2 |
| conflict supplemental-only decisions | 1 |
| SuperCombo-only row | 4 |

## 公式のみの行

| 公式 row | 公式技名 | 理由 |
|---:|---|---|
| 63 | 前方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |
| 64 | 後方ステップ | SuperCombo では frame row ではなく character data の dash fields に対応する可能性が高い。 |

## 人間レビュー済み行

| 公式 row | 公式技名 | SuperCombo move_id | decision | 方針 |
|---:|---|---|---|---|
| 7 | 立ち強P（ダイナマイトパンチ）（ホールド） | `zangief_5hp_hold` | `hold_supplemental_link` | startup 32、active duration 3、damage 1400 が公式値と対応する。SuperCombo の armor / whiff recovery 分解は補助情報として保持する。 |
| 23 | ジャンプ強K（ドロップキック）（ホールド） | `zangief_jhk_hold` | `hold_supplemental_link` | startup 32、active duration 6、damage 1500 が公式値と対応する。landing recovery、wall splat、projectile invuln notes は補助情報として保持する。 |
| 29 | フライングボディプレス | `zangief_j2hp` | `supplemental_link` | input、startup 9、active duration 9、damage 800 が公式値と対応する。cross-up / landing recovery notes は補助情報として扱う。 |
| 30 | フライングヘッドバット | `zangief_j8hp` | `supplemental_link` | input、startup 8、active duration 4、damage 900 が公式値と対応する。cancel / juggle notes は補助情報として扱う。 |
| 37 | OD ダブルラリアット | `zangief_ppp` | `supplemental_link` | startup 12 と recovery 26 は公式値と対応する。SuperCombo damage `700,1000 (1700)` は公式 damage 1700 の分解情報として保持する。 |
| 38 | 弱 スクリューパイルドライバー | `zangief_360lp` | `supplemental_link` | startup 5、active duration 3、recovery 54 が公式値と対応する。Punish Counter damage と range notes は補助情報として扱う。 |
| 39 | 中 スクリューパイルドライバー | `zangief_360mp` | `supplemental_link` | startup 5、active duration 3、recovery 54 が公式値と対応する。Punish Counter damage と range notes は補助情報として扱う。 |
| 40 | 強 スクリューパイルドライバー | `zangief_360hp` | `supplemental_link` | startup 5、active duration 3、recovery 54 が公式値と対応する。Punish Counter damage と range notes は補助情報として扱う。 |
| 41 | OD スクリューパイルドライバー | `zangief_360pp` | `supplemental_link` | startup 5、active duration 3、recovery 54 が公式値と対応する。Punish Counter damage と range notes は補助情報として扱う。 |
| 42 | ボルシチダイナマイト | `zangief_j360k` | `supplemental_link` | startup 4、active duration 3、damage 2900 が公式値と対応する。landing recovery と juggle notes は補助情報として扱う。 |
| 43 | OD ボルシチダイナマイト | `zangief_j360kk` | `supplemental_link` | startup 4、active duration 3、damage 3000 が公式値と対応する。landing recovery と juggle notes は補助情報として扱う。 |
| 44 | ロシアンスープレックス | `zangief_63214k_close` | `supplemental_link` | startup 10、active duration 2、recovery 50 が公式値と対応する。close proximity 条件と side-switch notes は補助情報として扱う。 |
| 45 | OD ロシアンスープレックス | `zangief_63214kk_close` | `supplemental_link` | startup 10、active duration 2、recovery 50 が公式値と対応する。close proximity 条件と side-switch notes は補助情報として扱う。 |
| 46 | シベリアンエクスプレス（近距離版） | `zangief_63214k_mid` | `supplemental_link` | startup 28、active duration 2、recovery 41 が公式値と対応する。SuperCombo の mid range 条件と run speed notes は補助情報として扱う。 |
| 47 | OD シベリアンエクスプレス（近距離版） | `zangief_63214kk_mid` | `supplemental_link` | startup 23、active duration 2、recovery 44 が公式値と対応する。SuperCombo の mid range 条件と run speed notes は補助情報として扱う。 |
| 48 | シベリアンエクスプレス（遠距離版） | `zangief_63214k_far` | `supplemental_link` | active duration 2 と recovery 40 は公式値と対応する。SuperCombo startup `55(81)` は距離による増加を含む補助情報として扱い、公式 startup 55 は上書きしない。 |
| 49 | OD シベリアンエクスプレス（遠距離版） | `zangief_63214kk_far` | `supplemental_link` | active duration 2 と recovery 40 は公式値と対応する。SuperCombo startup `54(81)` は距離による増加を含む補助情報として扱い、公式 startup 54 は上書きしない。 |
| 50 | ツンドラストーム | `zangief_22hk` | `conflict_supplemental_only` | 公式 startup 5 / active 5-55 と SuperCombo startup 6 / active 50 は単純一致しない。公式値を正とし、SuperCombo 値は conflict 付き補助情報として保持する。 |
| 52 | SA2 サイクロンラリアット（ホールド） | `zangief_236236p_hold_p` | `hold_supplemental_link` | startup 18、active duration 105、damage 1100 が公式値と対応する。multihit damage と vacuum distribution は補助情報として扱う。 |
| 53 | SA2 サイクロンラリアット（その場） | `zangief_236236p` | `movement_variant_supplemental_link` | SuperCombo はその場 / 移動を同一 row で説明している。公式 damage 3100 を正とし、shared row と movement notes は補助情報として扱う。 |
| 54 | SA2 サイクロンラリアット（移動） | `zangief_236236p` | `movement_variant_supplemental_link` | SuperCombo はその場 / 移動を同一 row で説明している。公式 damage 3000 を正とし、shared row と movement notes は補助情報として扱う。 |
| 55 | SA3 ボリショイストームバスター | `zangief_720+p` | `supplemental_link` | active duration 2、recovery 116、damage 4800 が公式値と対応する。SA3 / CA variant は `move_id` で分けて扱う。 |
| 56 | CA ボリショイストームバスター | `zangief_720+p(ca)` | `supplemental_link` | active duration 2、recovery 116、damage 5300 が公式値と対応する。SA3 / CA variant は `move_id` で分けて扱う。 |
| 71 | パリィドライブラッシュ | `zangief_mpmk_66_pdr` | `supplemental_link` | SuperCombo の startup/recovery/total 分解は公式全体45Fの置換ではなく補助情報として扱う。 |
| 72 | キャンセルドライブラッシュ | `zangief_mpmk_66_drc` | `supplemental_link` | SuperCombo total `24(46)` の括弧内 total は公式全体46Fと対応し、decomposition は補助情報として扱う。 |

## review flag の扱い

| flag | 件数/扱い |
|---|---|
| `manual_match` | 24 件。Zangief の 360 / 720、hold、近距離/中距離/遠距離、CA variant などを name override で対応させ、人間レビューで accepted にした。 |
| `supercombo_row_reused` | 11 件。連打版、SA2 `その場` / `移動`、ドライブパリィ系が同一 SuperCombo row を共有する候補。レビュー対象だった SA2 2 行は `movement_variant_supplemental_link` として accepted。 |
| `multiple_candidates` | 2 件。Drive Reversal の block/recovery variant は startup / active duration により自動対応できているため、JP/Ryu と同じく `enriched` のまま保持する。 |
| `basic_field_conflict:active_duration,startup` | 1 件。`ツンドラストーム` は `conflict_supplemental_only` として accepted。公式 startup / active を正とする。 |

## SuperCombo-only 行

| 分類 | 件数 | 内容 |
|---|---:|---|
| supercombo_only_taunt | 4 | `zangief_5pppkkk`, `zangief_6pppkkk`, `zangief_4pppkkk`, `zangief_2pppkkk` |

## 注意点

- この補助列付き output は「公式 + 補助情報」であり、公式 CSV を置き換えるものではない。
- 公式列と補助列付き output の公式由来列は全行一致する。SuperCombo の数値は `supercombo_*` 補助列にのみ入れる。
- Zangief 専用 name override 24 件は人間レビュー済みで accepted。公式値を正とし、SuperCombo は補助情報として扱う。
- `ツンドラストーム` は公式と SuperCombo の単純比較で startup / active duration が異なるため、公式値を正としつつ conflict 付き補助情報として保持する。
- `前方ステップ` / `後方ステップ` は official only。SuperCombo 側の movement data は `character.csv` の dash fields を確認する。

## 根拠

- 公式 source（根拠）: [[sources/capcom-official-zangief-frame-data]]
- SuperCombo source（根拠）: [[sources/supercombo-zangief-frame-data]]
- 候補照合: [[outputs/reports/2026-06-02-supercombo-zangief-official-crosswalk]]
- 補助列付き summary: `wiki/outputs/data/enriched/frame-data/zangief/summary.json`
- Human review decisions: `wiki/outputs/data/enriched/frame-data/zangief/classic-supercombo.csv` の `human_review_*` 列
