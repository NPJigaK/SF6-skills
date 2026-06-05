---
type: review
review_type: capture_validation
created: 2026-06-05
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-frame-data-batch]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
  - "[[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]"
aliases:
  - "SuperCombo all frame data capture review"
  - "SuperCombo 全キャラフレームデータ取得レビュー"
tags:
  - review
  - frame-data
  - supercombo
  - batch-capture
---

# SuperCombo 全キャラフレームデータ取得レビュー - 2026-06-05

## 要約

SuperCombo Wiki の Street Fighter 6 frame-data は、30 キャラ分の raw capture、Cargo API、表示 DOM、5タブ別スクリーンショット、画像参照情報まで保存し、自動検証は 30/30 で `passed`。raw 取得の completeness については、現時点で追加の人間判断待ちはない。

ただし、公式 Classic data との統合では、`enriched_review_required` が合計 1296 行、SuperCombo-only が合計 620 行残る。これは「取得が不完全」という意味ではなく、公式値を正とした補助リンクとして accept してよいか、また SuperCombo-only row を通常回答に混ぜてよいかを人間が判断する必要がある、という意味。

## 検証サマリー

| 項目 | 値 |
|---|---:|
| SuperCombo frame-data pages | 30 |
| validation `passed` | 30 |
| validation `failed` | 0 |
| SuperCombo frame rows | 2306 |
| 公式 Classic rows | 2361 |
| enriched | 591 |
| enriched_reviewed | 69 |
| enriched_review_required | 1296 |
| official_only | 405 |
| SuperCombo-only rows | 620 |
| imageinfo missing titles | 599 |
| downloaded images | 423 |

## 検証で確認したこと

- 各 character の `Data?action=raw` から `CharacterData-SF6` と `FrameData-SF6` template を抽出した。
- SuperCombo Cargo API の `SF6_FrameData` / `SF6_CharacterData` 行数が raw template 件数と一致することを確認した。
- `Frame_data?action=raw` の Cargo query を保存し、表示ページの DOM table と raw/Cargo 由来の期待値を照合した。
- 表示 DOM は `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 tab state を保存した。
- 公式 Classic CSV との crosswalk と、公式列を正として SuperCombo を `supercombo_*` 補助列に入れる enriched output を 30 キャラ分生成した。

## 検証中に反映した補正

| 補正 | 理由 | 方針 |
|---|---|---|
| Chun-Li の `serenity_stream` を Normals / Target Combos の moveType に含めた。 | SuperCombo 表示ページの Cargo query が `moveType="serenity_stream"` を Normals 側に含めているため。 | source query に従って section を分類する。 |
| Dee Jay の Cargo query では page title `Dee Jay` ではなく `CharacterData-SF6.chara=Dee_Jay` を使った。 | page title と Cargo key が一致しないため、page title のままだと Cargo rows が 0 になる。 | Data page の character template を Cargo key の根拠にする。 |
| C.Viper の `cancel=*SA3` は表示比較では `SA3` として扱った。 | MediaWiki の行頭 `*` は list marker として DOM 表示で落ちるため。 | raw は変えず、表示正規化だけで合わせる。`notes` の単一行 `*...*` は壊さない。 |
| Jamie Specials の 55 rows は DOM では 50 rows 表示として比較した。 | SuperCombo の dynamic table が 1ページ 50 rows の pagination で表示されるため。 | raw/Cargo では 55 rows を保持し、DOM は先頭 50 rows の表示値を比較する。 |

## 人間レビューが必要な項目

| slug | SuperCombo title | enriched_review_required | SuperCombo-only | official_only |
|---|---|---:|---:|---:|
| `aki` | A.K.I. | 34 | 13 | 11 |
| `alex` | Alex | 46 | 28 | 13 |
| `blanka` | Blanka | 42 | 34 | 34 |
| `cammy` | Cammy | 38 | 21 | 17 |
| `chunli` | Chun-Li | 47 | 27 | 18 |
| `cviper` | C.Viper | 36 | 18 | 14 |
| `deejay` | Dee Jay | 33 | 47 | 52 |
| `dhalsim` | Dhalsim | 53 | 9 | 11 |
| `ed` | Ed | 39 | 13 | 11 |
| `ehonda` | E.Honda | 32 | 21 | 19 |
| `elena` | Elena | 43 | 19 | 14 |
| `gouki_akuma` | Akuma | 59 | 25 | 10 |
| `guile` | Guile | 25 | 23 | 32 |
| `ingrid` | Ingrid | 23 | 13 | 2 |
| `jamie` | Jamie | 75 | 25 | 7 |
| `jp` | JP | 36 | 7 | 2 |
| `juri` | Juri | 76 | 35 | 9 |
| `ken` | Ken | 47 | 22 | 15 |
| `kimberly` | Kimberly | 38 | 27 | 25 |
| `lily` | Lily | 46 | 20 | 5 |
| `luke` | Luke | 46 | 17 | 9 |
| `mai` | Mai | 69 | 32 | 4 |
| `manon` | Manon | 31 | 7 | 4 |
| `marisa` | Marisa | 56 | 26 | 10 |
| `rashid` | Rashid | 55 | 24 | 11 |
| `ryu` | Ryu | 43 | 6 | 2 |
| `sagat` | Sagat | 39 | 15 | 12 |
| `terry` | Terry | 43 | 8 | 5 |
| `vega_mbison` | M.Bison | 24 | 34 | 25 |
| `zangief` | Zangief | 22 | 4 | 2 |

JP / Ryu / Zangief / Ingrid の既存 accepted decision 69 行は保持した。2026-06-06 の fail-closed policy 以降は、それ以外の複数候補、SuperCombo row 再利用、基本 field conflict、比較不能 field、条件付き SuperCombo field を持つ行も `enriched_review_required` に落としている。`着地後N` と `N land` は landing recovery の表記差として正規化したが、括弧付き damage / startup / recovery は条件付き値として review queue に残している。

## 注意点

- 新規 26 キャラは `--no-download-images` で capture したため、画像ファイル本体は保存していない。画像参照、DOM、`imageinfo.json`、`image-manifest.json` は保存済み。
- `imageinfo missing titles` は合計 599 件。フレーム表の数値検証とは別の警告として扱う。
- Jamie の warning 5 件は Specials table の pagination によるもの。raw/Cargo の 55 rows は保持している。
- C.Viper には `moveType=air_normal8` の `c.viper_8jhk` が 1 行ある。SuperCombo 表示 query には含まれていない非標準 moveType なので、勝手に `air_normal` と同一扱いにはしない。
- SuperCombo は community data であり、公式 data と重なる基本フレーム値では Capcom 公式 Classic CSV を正とする。

## 未解決の質問

- `enriched_review_required` 1296 行を、character ごとにどの順序で accept / reject / supplemental-only に分けるか。
- SuperCombo-only 620 行を taunt、conditional variant、hidden / non-standard row、公式未掲載 row などに細分化する必要があるか。
- imageinfo missing 599 件について、source 側の欠損として扱うか、filename 正規化で再解決を試すか。
- C.Viper の `air_normal8` を、今後の extractor / validator の通常 section に含めるべきか、非標準 row として明示的に分離するべきか。

## 追加生成した成果物

- [[sources/supercombo-street-fighter-6-frame-data-batch]]
- [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]
- `raw/frame-data/supercombo/<character_slug>/`
- `wiki/outputs/data/supercombo/frame-data/<character_slug>/`
- `wiki/outputs/data/enriched/frame-data/<character_slug>/`
