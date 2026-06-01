---
type: output
output_type: report
created: 2026-05-31
updated: 2026-06-01
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
| crosswalk の意味 | 自動候補に、人間レビュー済みの Ryu Denjin / hold-level name override と Drive Rush override を反映した review 面。 |
| 比較対象 | startup、active duration、recovery、damage は単純数値化できる場合だけ比較する。 |

## 照合サマリー

| 項目 | 値 |
|---|---:|
| 公式 Classic rows | 75 |
| SuperCombo frame rows | 77 |
| 自動 matched | 61 |
| Ryu / generic name override matched | 10 |
| ambiguous matched | 2 |
| 公式側 unmatched | 2 |
| matched した distinct SuperCombo rows | 71 |
| SuperCombo 側 unmatched | 6 |

公式側で unmatched の 2 件は `前方ステップ` と `後方ステップ`。SuperCombo capture では dash speed/distance は `SF6_CharacterData` にあり、`SF6_FrameData` row ではないため、frame-row crosswalk では未対応になる。

## レビュー済み name override 行

| 公式 row | 公式技名 | SuperCombo move_id | match method |
|---:|---|---|---|
| 30 | [電刃錬気]波動拳 | `ryu_236p(charged)` | `ryu_name_override+same_family+category_move_type+startup_match` |
| 32 | [電刃錬気]OD 波動拳 | `ryu_236pp(charged)` | `ryu_name_override+exact_input+family_input+same_family+category_move_type+startup_match` |
| 50 | [電刃錬気]波掌撃 | `ryu_214p(charged)` | `ryu_name_override+same_family+category_move_type+startup_match` |
| 55 | [電刃錬気]SA1 真空波動拳 | `ryu_236236p_denjin` | `ryu_name_override+exact_input+family_input+same_family+category_move_type+startup_match` |
| 57 | SA2 真波掌撃（Lv2） | `ryu_214214p_lv2` | `ryu_name_override+category_move_type+active_duration_match+recovery_match+damage_match` |
| 58 | SA2 真波掌撃（Lv3） | `ryu_214214p_lv3` | `ryu_name_override+category_move_type+active_duration_match+recovery_match+damage_match` |
| 60 | [電刃錬気]SA2 真波掌撃（Lv2） | `ryu_214214p_denjin_lv2` | `ryu_name_override+category_move_type+active_duration_match+recovery_match+damage_match` |
| 61 | [電刃錬気]SA2 真波掌撃（Lv3） | `ryu_214214p_denjin_lv3` | `ryu_name_override+category_move_type+active_duration_match+recovery_match+damage_match` |
| 74 | パリィドライブラッシュ | `ryu_mpmk_66_pdr` | `generic_name_override+category_move_type` |
| 75 | キャンセルドライブラッシュ | `ryu_mpmk_66_drc` | `generic_name_override+category_move_type` |

## ambiguous 行

| 公式 row | 公式技名 | input | 現候補 | candidate count |
|---:|---|---|---|---:|
| 31 | OD 波動拳 | `236PP` | `ryu_236pp` | 2 |
| 54 | SA1 真空波動拳 | `236236P` | `ryu_236236p` | 2 |

この 2 行は同じ input に Denjin / charged variant が存在するため ambiguous flag は残るが、人間レビューでは通常版への補助リンクとして accepted 済み。

## SuperCombo 側未照合行

| 分類 | 件数 | 内容 |
|---|---:|---|
| conditional variants | 2 | `ryu_6hk_214k`, `ryu_6hk_214kk` |
| taunt | 4 | `ryu_5pppkkk`, `ryu_6pppkkk`, `ryu_4pppkkk`, `ryu_2pppkkk` |

`ryu_6hk_214k` と `ryu_6hk_214kk` は frame-row crosswalk には直接統合しない。公式 row 23 `旋風脚` が「空中竜巻旋風脚(OD版を含む)でキャンセル可能」と記録しており、SuperCombo 側はそのキャンセル後に出る空中竜巻の条件付き variant を別 `move_id` として持つ。したがって enriched 側の SuperCombo-only link fields では、primary row を 41 `空中竜巻旋風脚` / 42 `OD 空中竜巻旋風脚`、enabled-by row を 23 `旋風脚` として分ける。

## 注意点

- Denjin / hold level の duplicate input は `move_id` override で明示的に対応させる。input だけでは主キーにしない。
- `ambiguous` 2件は、通常版と charged / Denjin 版の同一 input による候補重複。人間レビュー済みだが、候補重複の事実は flag として残す。
- `6HK~214K` / `6HK~214KK` は `旋風脚` 本体の数値とは混ぜず、SuperCombo-only の conditional variant link として保持する。
- 公式の active は `6-8` のような発生フレーム範囲、SuperCombo の active は `3` のような持続フレーム数で表されることがある。単純比較では active duration に変換できる場合だけ比較する。
- SA2 Lv2 / Lv3 の SuperCombo startup `18~` / `50~` は hold-level 補助情報であり、公式 startup 20 / 70 を置き換えない。
- この report は review 用であり、`wiki/outputs/data/frame-data/ryu/` の公式 CSV を置き換えない。

## 根拠

- SuperCombo source: [[sources/supercombo-ryu-frame-data]]
- 公式 source: [[sources/capcom-official-ryu-frame-data]]
- SuperCombo validation: [[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]]
- Raw SuperCombo manifest: `raw/supercombo/frame-data/2026-05-31/ryu/manifest.json`
- Crosswalk summary: `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
- Enriched output report: [[outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data]]
