---
type: output
output_type: report
created: 2026-06-02
updated: 2026-06-02
status: active
sources:
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[sources/capcom-official-zangief-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/zangief]]"
  - "[[reviews/2026-06-02-supercombo-zangief-frame-data-capture-review]]"
  - "[[syntheses/frame-data-raw-layout]]"
aliases:
  - "SuperCombo Zangief official crosswalk"
  - "Zangief SuperCombo 公式照合"
---

# SuperCombo Zangief / 公式 Zangief フレームデータ照合 - 2026-06-02

## 要約

SuperCombo Zangief raw 取得データからレビュー用の派生 JSON を作成し、Capcom 公式 Zangief Classic JSON との候補照合を生成した。これは最終マージではなく、公式 data を正としたまま SuperCombo の `move_id`、range、juggle、notes、画像をどの公式 row に紐づけられるか確認するためのレビュー面。2026-06-02 にレビュー対象 25 行を人間レビューし、公式値を正とした補助リンクとして accepted にした。

この照合を使った補助列付き output は [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] に保存している。

## 生成ファイル

- `wiki/outputs/data/frame-data/supercombo/zangief/frames.json`
- `wiki/outputs/data/frame-data/supercombo/zangief/frames.json`
- `wiki/outputs/data/frame-data/supercombo/zangief/character.json`
- `wiki/outputs/data/frame-data/supercombo/zangief/schema.json`
- `wiki/outputs/data/frame-data/supercombo/zangief/crosswalk-official-classic.json`
- `wiki/outputs/data/frame-data/supercombo/zangief/crosswalk-summary.json`
- `wiki/outputs/data/frame-data/supercombo/zangief/supercombo-unmatched.json`

## 方針

| 項目 | 方針 |
|---|---|
| 正とする source | 公式に存在する基本フレーム値は Capcom 公式 Zangief data を正とする。 |
| SuperCombo の扱い | SuperCombo raw は削らず保持し、公式にない補助情報の候補 source として使う。 |
| SuperCombo row key | input ではなく `move_id` を使う。Zangief には `6HPHK` と `720+P` の duplicate input があるため。 |
| 照合の意味 | 自動候補に、Zangief の 360 / 720、hold、近距離/中距離/遠距離、CA variant name override と Drive Rush override を反映したレビュー面。 |
| 比較対象 | startup、active duration、recovery、damage は単純数値化できる場合だけ比較する。 |

## 照合サマリー

| 項目 | 値 |
|---|---:|
| 公式 Classic rows | 72 |
| SuperCombo frame rows | 68 |
| 自動一致 | 46 |
| Zangief / 汎用 name override による一致 | 24 |
| 公式側未照合 | 2 |
| 一致した distinct SuperCombo row | 64 |
| SuperCombo 側未照合 | 4 |

公式側で未照合の 2 件は `前方ステップ` と `後方ステップ`。SuperCombo 取得データでは dash speed/distance は `SF6_CharacterData` にあり、`SF6_FrameData` row ではないため、frame-row 照合では未対応になる。

## name override 行

| 分類 | 件数 | 例 |
|---|---:|---|
| hold / 空中 command normal | 4 | `zangief_5hp_hold`, `zangief_jhk_hold`, `zangief_j2hp`, `zangief_j8hp` |
| 360 / 720 command throws | 8 | `zangief_360lp`, `zangief_360pp`, `zangief_720+p`, `zangief_720+p(ca)` |
| 近距離/中距離/遠距離 command throw variant | 6 | `zangief_63214k_close`, `zangief_63214k_mid`, `zangief_63214k_far` |
| SA2 / Drive Rush variant | 6 | `zangief_236236p_hold_p`, `zangief_236236p`, `zangief_mpmk_66_pdr`, `zangief_mpmk_66_drc` |

これら 24 件の name override match は、人間レビューで補助リンクとして accepted。公式列は上書きせず、SuperCombo の range、notes、juggle、hitbox などを補助列として扱う。

## SuperCombo row 再利用

| SuperCombo move_id | 理由 |
|---|---|
| `zangief_236236p` | 公式側の SA2 `その場` / `移動` が SuperCombo の同一 base row に対応する候補。 |
| `zangief_2lk` | 公式側の通常版 / 連打版が SuperCombo の同一 row に対応する候補。 |
| `zangief_2lp` | 公式側の通常版 / 連打版が SuperCombo の同一 row に対応する候補。 |
| `zangief_5lp` | 公式側の通常版 / 連打版が SuperCombo の同一 row に対応する候補。 |
| `zangief_mpmk` | ドライブパリィ / ジャストパリィ rows が SuperCombo の同一 row に対応する候補。 |

## SuperCombo 側未照合行

| 分類 | 件数 | 内容 |
|---|---:|---|
| taunt | 4 | `zangief_5pppkkk`, `zangief_6pppkkk`, `zangief_4pppkkk`, `zangief_2pppkkk` |

## 注意点

- Zangief の公式 input token には `key-circle` がある。照合では `key-circle` を `360+`、2回転を `720+` として SuperCombo input と照合している。
- 近距離/中距離/遠距離版は input だけでは区別しづらいため、name override で `move_id` を明示している。
- `ツンドラストーム` は official startup 5 / active duration 51、SuperCombo startup 6 / active 50 と単純比較差分がある。人間レビューでは `conflict_supplemental_only` とし、公式値は上書きしない。
- この report はレビュー用であり、`wiki/outputs/data/frame-data/official/zangief/` の公式 JSON を置き換えない。

## 根拠

- SuperCombo source（根拠）: [[sources/supercombo-zangief-frame-data]]
- 公式 source（根拠）: [[sources/capcom-official-zangief-frame-data]]
- SuperCombo 検証: [[reviews/2026-06-02-supercombo-zangief-frame-data-capture-review]]
- SuperCombo 原本 manifest: `raw/frame-data/supercombo/zangief/manifest.json`
- 照合 summary: `wiki/outputs/data/frame-data/supercombo/zangief/crosswalk-summary.json`
- 補助列付き output report: [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]]
