---
type: output
output_type: report
created: 2026-05-31
updated: 2026-05-31
status: active
sources:
  - "[[sources/supercombo-ryu-frame-data]]"
  - "[[sources/capcom-official-ryu-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/ryu]]"
  - "[[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]]"
aliases:
  - "SuperCombo Ryu official crosswalk"
  - "Ryu SuperCombo 公式照合"
---

# SuperCombo Ryu / 公式 Ryu フレームデータ照合 - 2026-05-31

## 要約

SuperCombo Ryu raw capture から review 用の派生 CSV/JSON を作成し、Capcom 公式 Ryu Classic CSV との候補 crosswalk を生成した。これは最終マージではなく、公式 data を正としたまま SuperCombo の `moveId`、range、juggle、notes、画像をどの公式 row に紐づけられるか確認するためのレビュー面。

この crosswalk を使った enriched output は [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]] に保存している。

## 生成ファイル

- `wiki/outputs/data/supercombo/frame-data/ryu/frames.csv`
- `wiki/outputs/data/supercombo/frame-data/ryu/frames.json`
- `wiki/outputs/data/supercombo/frame-data/ryu/character.csv`
- `wiki/outputs/data/supercombo/frame-data/ryu/schema.json`
- `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-official-classic.csv`
- `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
- `wiki/outputs/data/supercombo/frame-data/ryu/supercombo-unmatched.csv`

## 方針

| 項目 | 方針 |
|---|---|
| 正とする source | 公式に存在する基本フレーム値は Capcom 公式 Ryu data を正とする。 |
| SuperCombo の扱い | SuperCombo raw は削らず保持し、公式にない補助情報の候補 source として使う。 |
| SuperCombo row key | input ではなく `move_id` を使う。Ryu には duplicate input が 10 種類あるため。 |
| crosswalk の意味 | 自動候補。Ryu の review-required 行は未承認で、人間レビュー待ち。 |
| 比較対象 | startup、active duration、recovery、damage は単純数値化できる場合だけ比較する。 |

## 照合サマリー

| 項目 | 値 |
|---|---:|
| 公式 Classic rows | 75 |
| SuperCombo frame rows | 77 |
| 自動 matched | 61 |
| ambiguous matched | 10 |
| generic name override matched | 2 |
| 公式側 unmatched | 2 |
| matched した distinct SuperCombo rows | 63 |
| SuperCombo 側 unmatched | 14 |

公式側で unmatched の 2 件は `前方ステップ` と `後方ステップ`。SuperCombo capture では dash speed/distance は `SF6_CharacterData` にあり、`SF6_FrameData` row ではないため、frame-row crosswalk では未対応になる。

## 汎用 name override 行

| 公式 row | 公式技名 | SuperCombo move_id | match method |
|---:|---|---|---|
| 74 | パリィドライブラッシュ | `ryu_mpmk_66_pdr` | `generic_name_override+category_move_type` |
| 75 | キャンセルドライブラッシュ | `ryu_mpmk_66_drc` | `generic_name_override+category_move_type` |

## ambiguous 行

| 公式 row | 公式技名 | input | 現候補 | candidate count |
|---:|---|---|---|---:|
| 30 | [電刃錬気]波動拳 | `236P` | `ryu_236hp` | 4 |
| 31 | OD 波動拳 | `236PP` | `ryu_236pp` | 2 |
| 32 | [電刃錬気]OD 波動拳 | `236PP` | `ryu_236pp` | 2 |
| 50 | [電刃錬気]波掌撃 | `214P` | `ryu_214mp` | 4 |
| 54 | SA1 真空波動拳 | `236236P` | `ryu_236236p` | 2 |
| 55 | [電刃錬気]SA1 真空波動拳 | `236236P` | `ryu_236236p` | 2 |
| 57 | SA2 真波掌撃（Lv2） | `214214P` | `ryu_214214p` | 2 |
| 58 | SA2 真波掌撃（Lv3） | `214214P` | `ryu_214214p` | 2 |
| 60 | [電刃錬気]SA2 真波掌撃（Lv2） | `214214P` | `ryu_214214p` | 2 |
| 61 | [電刃錬気]SA2 真波掌撃（Lv3） | `214214P` | `ryu_214214p` | 2 |

## SuperCombo 側未照合行

| 分類 | 件数 | 内容 |
|---|---:|---|
| Denjin / charged / hold / follow-up variants | 10 | `ryu_236p(charged)`, `ryu_236pp(charged)`, `ryu_6hk_214k`, `ryu_6hk_214kk`, `ryu_214p(charged)`, `ryu_236236p_denjin`, `ryu_214214p_lv2`, `ryu_214214p_denjin_lv2`, `ryu_214214p_lv3`, `ryu_214214p_denjin_lv3` |
| taunt | 4 | `ryu_5pppkkk`, `ryu_6pppkkk`, `ryu_4pppkkk`, `ryu_2pppkkk` |

## 注意点

- `ambiguous` 10件は、Denjin / hold level / duplicate input の粒度差が原因の候補を含む。enriched output では `ambiguous_match` として review-required にしている。
- `パリィドライブラッシュ` と `キャンセルドライブラッシュ` は generic name override で SuperCombo row に紐づいたが、Ryu ではまだ人間レビュー未承認。
- 公式の active は `6-8` のような発生フレーム範囲、SuperCombo の active は `3` のような持続フレーム数で表されることがある。単純比較では active duration に変換できる場合だけ比較する。
- この report は review 用であり、`wiki/outputs/data/frame-data/ryu/` の公式 CSV を置き換えない。

## 根拠

- SuperCombo source: [[sources/supercombo-ryu-frame-data]]
- 公式 source: [[sources/capcom-official-ryu-frame-data]]
- SuperCombo validation: [[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]]
- Raw SuperCombo manifest: `raw/supercombo/frame-data/2026-05-31/ryu/manifest.json`
- Crosswalk summary: `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
- Enriched output report: [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]]
