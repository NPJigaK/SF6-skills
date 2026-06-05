---
type: output
output_type: report
created: 2026-06-05
updated: 2026-06-06
status: active
sources:
  - "[[sources/supercombo-street-fighter-6-frame-data-batch]]"
related:
  - "[[reviews/2026-06-05-supercombo-all-frame-data-capture-review]]"
  - "[[concepts/frame-data]]"
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "SuperCombo all frame data coverage"
  - "SuperCombo 全キャラフレームデータ coverage"
---

# SuperCombo 全キャラフレームデータ coverage - 2026-06-05

## 要約

SuperCombo Wiki の Street Fighter 6 frame-data は 30 キャラ分の raw capture と派生 output がそろった。全キャラの `validation.json` は `passed`。公式 Classic との enriched output も全キャラ分生成済みだが、複数候補、SuperCombo row 再利用、基本 field conflict、比較不能 field、条件付き SuperCombo field を持つ補助リンクは人間レビューなしでは `enriched` にしない。

## 全体サマリー

| 項目 | 値 |
|---|---:|
| SuperCombo frame-data pages | 30 |
| validation `passed` | 30 |
| SuperCombo frame rows | 2306 |
| 公式 Classic rows | 2361 |
| enriched | 591 |
| enriched_reviewed | 69 |
| enriched_review_required | 1296 |
| official_only | 405 |
| SuperCombo-only rows | 620 |
| downloaded images | 423 |
| imageinfo missing titles | 599 |

## 網羅表

| slug | SuperCombo title | SuperCombo rows | official rows | review_required | official_only | SuperCombo-only | validation | warnings |
|---|---|---:|---:|---:|---:|---:|---|---:|
| `aki` | A.K.I. | 64 | 64 | 34 | 11 | 13 | passed | 1 |
| `alex` | Alex | 76 | 74 | 46 | 13 | 28 | passed | 1 |
| `blanka` | Blanka | 84 | 91 | 42 | 34 | 34 | passed | 1 |
| `cammy` | Cammy | 74 | 75 | 38 | 17 | 21 | passed | 1 |
| `chunli` | Chun-Li | 79 | 78 | 47 | 18 | 27 | passed | 1 |
| `cviper` | C.Viper | 64 | 69 | 36 | 14 | 18 | passed | 0 |
| `deejay` | Dee Jay | 98 | 105 | 33 | 52 | 47 | passed | 1 |
| `dhalsim` | Dhalsim | 69 | 89 | 53 | 11 | 9 | passed | 1 |
| `ed` | Ed | 65 | 70 | 39 | 11 | 13 | passed | 0 |
| `ehonda` | E.Honda | 65 | 70 | 32 | 19 | 21 | passed | 1 |
| `elena` | Elena | 82 | 79 | 43 | 14 | 19 | passed | 1 |
| `gouki_akuma` | Akuma | 91 | 91 | 59 | 10 | 25 | passed | 1 |
| `guile` | Guile | 67 | 80 | 25 | 32 | 23 | passed | 1 |
| `ingrid` | Ingrid | 83 | 75 | 23 | 2 | 13 | passed | 1 |
| `jamie` | Jamie | 115 | 103 | 75 | 7 | 25 | passed | 6 |
| `jp` | JP | 64 | 69 | 36 | 2 | 7 | passed | 1 |
| `juri` | Juri | 87 | 87 | 76 | 9 | 35 | passed | 1 |
| `ken` | Ken | 75 | 76 | 47 | 15 | 22 | passed | 1 |
| `kimberly` | Kimberly | 84 | 86 | 38 | 25 | 27 | passed | 1 |
| `lily` | Lily | 75 | 74 | 46 | 5 | 20 | passed | 1 |
| `luke` | Luke | 74 | 76 | 46 | 9 | 17 | passed | 1 |
| `mai` | Mai | 87 | 90 | 69 | 4 | 32 | passed | 1 |
| `manon` | Manon | 60 | 59 | 31 | 4 | 7 | passed | 1 |
| `marisa` | Marisa | 90 | 91 | 56 | 10 | 26 | passed | 1 |
| `rashid` | Rashid | 79 | 85 | 55 | 11 | 24 | passed | 1 |
| `ryu` | Ryu | 77 | 75 | 43 | 2 | 6 | passed | 1 |
| `sagat` | Sagat | 69 | 70 | 39 | 12 | 15 | passed | 1 |
| `terry` | Terry | 66 | 66 | 43 | 5 | 8 | passed | 1 |
| `vega_mbison` | M.Bison | 75 | 72 | 24 | 25 | 34 | passed | 1 |
| `zangief` | Zangief | 68 | 72 | 22 | 2 | 4 | passed | 1 |

## 生成ファイル

各 character slug について、以下を生成または更新した。

- raw capture: `raw/frame-data/supercombo/<character_slug>/`
- SuperCombo 派生 output: `wiki/outputs/data/supercombo/frame-data/<character_slug>/`
- 公式 + SuperCombo 補助 output: `wiki/outputs/data/enriched/frame-data/<character_slug>/`

SuperCombo 派生 output には `frames.csv`、`frames.json`、`character.csv`、`crosswalk-official-classic.csv`、`crosswalk-summary.json`、`supercombo-unmatched.csv`、`schema.json` がある。

公式 + SuperCombo 補助 output には `classic-supercombo.csv`、`classic-supercombo.json`、`supercombo-only.csv`、`summary.json`、`schema.json` がある。

## レビュー状態

JP / Ryu / Zangief / Ingrid は既存の作業で一部補助リンクを人間レビュー済みにしており、accepted 69 行は `enriched_reviewed` として保持している。2026-06-06 の fail-closed policy 以降は、複数候補、SuperCombo row 再利用、基本 field conflict、比較不能 field、条件付き SuperCombo field を持つ行を `enriched_review_required` に落とす。`着地後N` と `N land` のような landing recovery 表記差は機械正規化したが、damage / startup / recovery の括弧付き条件値は `condition_dependent_supercombo_field` として review queue に残す。未レビュー補助列は 30 キャラ全体で 1296 行。

| 分類 | 対象 | 状態 |
|---|---|---|
| raw capture | 30 キャラ | 自動検証 `passed`。 |
| 既存 review 済み補助列 | JP / Ryu / Zangief / Ingrid | 既存の `human_review_status: accepted` 69 行を保持。 |
| 未レビュー補助列 | 30 キャラ | `enriched_review_required` 1296 行。勝手に accept していない。 |
| SuperCombo-only | 30 キャラ | 620 行。通常回答に混ぜるかは行分類レビューが必要。 |
| official_only | 30 キャラ | 405 行。公式 row に対応する SuperCombo frame row が直接見つからないか、character data / dash data 側にある可能性がある。 |

## 警告の内訳

- imageinfo missing: 28 キャラで合計 599 title。画像参照は保存済みだが、MediaWiki `imageinfo` で解決できない title がある。
- Jamie Specials pagination: `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 table で、raw/Cargo は 55 rows、DOM 表示は pagination により先頭 50 rows。validator は先頭 50 rows の表示値を比較し、raw/Cargo 55 rows を保持している。

## 注意点

- 新規 26 キャラは画像ファイル本体をダウンロードしていない。これは時間と安定性のための capture option であり、画像 refs と imageinfo は保存している。
- SuperCombo は community source なので、公式 data と重なる基本フレーム値では Capcom 公式 Classic CSV を正とする。
- C.Viper の `air_normal8` row は SuperCombo raw/Cargo にあるが、表示 query には含まれていない。現時点では非標準 moveType として保持し、通常 section には推測で含めない。
- Ingrid の特殊隠しコマンド / Monoid rows は既存レビューで通常回答から分離する方針を記録済み。他キャラの SuperCombo-only rows についても、同様の noise control が必要かは今後の review で判断する。

## 根拠

- batch source summary: [[sources/supercombo-street-fighter-6-frame-data-batch]]
- capture review: [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]]
- raw validation: `raw/frame-data/supercombo/<character_slug>/validation.json`
- enriched summaries: `wiki/outputs/data/enriched/frame-data/<character_slug>/summary.json`
