---
type: output
output_type: report
created: 2026-05-31
updated: 2026-05-31
status: active
sources:
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/capcom-official-jp-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/jp]]"
  - "[[reviews/2026-05-31-supercombo-jp-frame-data-capture-review]]"
aliases:
  - "SuperCombo JP official crosswalk"
  - "JP SuperCombo 公式照合"
---

# SuperCombo JP / 公式 JP フレームデータ照合 - 2026-05-31

## 要約

SuperCombo JP raw capture から review 用の派生 CSV/JSON を作成し、Capcom 公式 JP Classic CSV との候補 crosswalk を生成した。これは最終マージではなく、公式 data を正としたまま SuperCombo の `moveId`、range、juggle、notes、画像をどの公式 row に紐づけられるか確認するためのレビュー面。

この crosswalk を使った enriched output は [[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]] に保存している。

## 生成ファイル

- `wiki/outputs/data/supercombo/frame-data/jp/frames.csv`
- `wiki/outputs/data/supercombo/frame-data/jp/frames.json`
- `wiki/outputs/data/supercombo/frame-data/jp/character.csv`
- `wiki/outputs/data/supercombo/frame-data/jp/schema.json`
- `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-official-classic.csv`
- `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-summary.json`
- `wiki/outputs/data/supercombo/frame-data/jp/supercombo-unmatched.csv`

## 方針

| 項目 | 方針 |
|---|---|
| 正とする source | 公式に存在する基本フレーム値は Capcom 公式 JP data を正とする。 |
| SuperCombo の扱い | SuperCombo raw は削らず保持し、公式にない補助情報の候補 source として使う。 |
| SuperCombo row key | input ではなく `move_id` を使う。`6HPHK` と `236236K` のような duplicate input があるため。 |
| crosswalk の意味 | 自動候補。enriched output の5件は人間レビュー済み。未レビュー行は引き続き候補扱い。 |
| 比較対象 | startup、active duration、recovery、damage は単純数値化できる場合だけ比較する。 |

## 照合サマリー

| 項目 | 値 |
|---|---:|
| 公式 Classic rows | 69 |
| SuperCombo frame rows | 64 |
| 自動 matched | 63 |
| JP 固有名 override matched | 4 |
| 公式側 unmatched | 2 |
| matched した distinct SuperCombo rows | 57 |
| SuperCombo 側 unmatched | 7 |

公式側で unmatched の 2 件は `前方ステップ` と `後方ステップ`。SuperCombo capture では dash speed/distance は `SF6_CharacterData` にあり、`SF6_FrameData` row ではないため、frame-row crosswalk では未対応になる。

## 多対一対応

| SuperCombo move_id | 理由 |
|---|---|
| `jp_214p` | 公式の弱/中/強 ヴィーハトが SuperCombo の strength-collapsed `214P` に対応する。 |
| `jp_214pp` | 公式の OD 弱/中/強 ヴィーハトが SuperCombo の `214PP` に対応する。 |
| `jp_22p` | 公式の弱/中/強 トリグラフが SuperCombo の `22P` に対応する。 |
| `jp_22pp` | 公式の OD 弱/中/強 トリグラフが SuperCombo の `22PP` に対応する。 |
| `jp_mpmk` | 公式のドライブパリィ/ジャストパリィ rows が同じ `MPMK` input で SuperCombo の Drive Parry row に対応候補として集まる。 |

## SuperCombo 側 unmatched rows

| move_id | input | name | メモ |
|---|---|---|---|
| `jp_214pp_214hp` | `214PP~214HP` | OD Departure: Shadow | 公式 Classic CSV には独立 row がない候補。 |
| `jp_236k_hold` | `236[K]` | Torbalan Feint | hold/feint 系の補助 row。 |
| `jp_22k_bomb` | `22K (Bomb)` | Amnesia Bomb | 当身成立後の bomb row。 |
| `jp_22kk_bomb` | `22KK (Bomb)` | Amnesia Bomb | OD 当身成立後の bomb row。 |
| `jp_5pppkkk` | `5PPPKKK` | Neutral Taunt | 公式 Classic CSV には taunt row がない。 |
| `jp_6pppkkk` | `6PPPKKK` | Forward Taunt | 公式 Classic CSV には taunt row がない。 |
| `jp_4pppkkk` | `4PPPKKK` | Back Taunt | 公式 Classic CSV には taunt row がない。 |

## 注意点

- `matched_manual` の4件は enriched output で人間レビュー済み。`ヴィーハト・アクノ`、`パリィドライブラッシュ`、`キャンセルドライブラッシュ` は `supplemental_link`、`ヴィーハト・チェーニ` は `non_additive_supplemental_damage` として扱う。
- `SA2 ラヴーシュカ` の startup conflict は、enriched output で `conflict_supplemental_only` として人間レビュー済み。公式 startup 29 を正とする。
- 公式の active は `6-8` のような発生フレーム範囲、SuperCombo の active は `3` のような持続フレーム数で表されることがある。単純比較では active duration に変換できる場合だけ比較する。
- この report は review 用であり、`wiki/outputs/data/frame-data/jp/` の公式 CSV を置き換えない。

## 根拠

- SuperCombo source: [[sources/supercombo-jp-frame-data]]
- 公式 source: [[sources/capcom-official-jp-frame-data]]
- SuperCombo validation: [[reviews/2026-05-31-supercombo-jp-frame-data-capture-review]]
- Raw SuperCombo manifest: `raw/supercombo/frame-data/2026-05-31/jp/manifest.json`
- Crosswalk summary: `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-summary.json`
- Enriched output report: [[outputs/reports/2026-05-31-jp-official-supercombo-enriched-data]]
