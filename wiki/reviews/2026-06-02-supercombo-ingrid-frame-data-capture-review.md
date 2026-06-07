---
type: review
review_type: capture_validation
created: 2026-06-02
status: open
sources:
  - "[[sources/supercombo-ingrid-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/supercombo-wiki]]"
  - "[[entities/ingrid]]"
  - "[[reviews/2026-06-02-supercombo-ingrid-supercombo-only-prereview]]"
  - "[[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]"
  - "[[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]"
aliases:
  - "SuperCombo Ingrid capture review"
tags:
  - review
  - frame-data
  - supercombo
---

# SuperCombo Ingrid フレームデータ取得レビュー - 2026-06-02

## 要約

SuperCombo Wiki Ingrid フレームデータの raw 取得データは、自動検証を通過した。生 wikitext、Cargo API、表示 DOM、5タブ分のページ全体スクリーンショット、画像ダウンロード結果を保存し、raw/Cargo/DOM の表値照合まで通した。

公式 Classic との crosswalk と補助列付き output も作成し、レビュー対象 26 行は人間レビュー済み `accepted` とした。残る未解決事項は、`imageinfo` missing 156 件と、公式 row に直接照合しない SuperCombo-only 9 行の schema 上の扱いなので、capture review の status は `open` のままにする。

## レビュー対象

- `raw/frame-data/supercombo/ingrid/data.raw.wikitext`
- `raw/frame-data/supercombo/ingrid/frame-data.raw.wikitext`
- `raw/frame-data/supercombo/ingrid/data.templates.json`
- `raw/frame-data/supercombo/ingrid/frame-data.cargo-queries.json`
- `raw/frame-data/supercombo/ingrid/cargo/frame-data.json`
- `raw/frame-data/supercombo/ingrid/cargo/character-data.json`
- `raw/frame-data/supercombo/ingrid/rendered/tables.dom.json`
- `raw/frame-data/supercombo/ingrid/screenshots/general.png`
- `raw/frame-data/supercombo/ingrid/screenshots/details.png`
- `raw/frame-data/supercombo/ingrid/screenshots/meter.png`
- `raw/frame-data/supercombo/ingrid/screenshots/properties.png`
- `raw/frame-data/supercombo/ingrid/screenshots/notes.png`
- `raw/frame-data/supercombo/ingrid/imageinfo.json`
- `raw/frame-data/supercombo/ingrid/image-manifest.json`
- `raw/frame-data/supercombo/ingrid/images/files/`
- `raw/frame-data/supercombo/ingrid/metadata.json`
- `raw/frame-data/supercombo/ingrid/validation.json`
- `raw/frame-data/supercombo/ingrid/manifest.json`

## 確認内容

- SuperCombo の `Street_Fighter_6/Ingrid/Frame_data` と `Street_Fighter_6/Ingrid/Data` を raw source として取得している。
- `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 83 件を抽出した。
- Cargo API の `SF6_FrameData` 83 行、`SF6_CharacterData` 1 行が raw template 件数と一致した。
- `Frame_data?action=raw` にある表示 Cargo query 21 件を保存した。
- 表示 DOM は `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 種類の tab state を含む。
- 4 section x 5 tab = 20 table comparisons で、header、row count、input order、cell values を照合した。
- 解決できた画像 2 件をダウンロードした。画像ダウンロード失敗は 0 件。
- `validation.json` の status は `passed`。

## 検証サマリー

| 項目 | 値 |
|---|---:|
| character template 数 | 1 |
| frame template 数 | 83 |
| 表示 Cargo query 数 | 21 |
| Cargo frame row 数 | 83 |
| Cargo character row 数 | 1 |
| 表示 tab state 数 | 5 |
| table comparison 数 | 20 |
| 画像参照数 | 164 |
| imageinfo 解決 title 数 | 2 |
| imageinfo missing title 数 | 156 |
| ダウンロード画像数 | 2 |
| 画像ダウンロード失敗数 | 0 |

## 公式照合 / 補助データレビュー

| 項目 | 値 |
|---|---:|
| 公式 Classic rows | 75 |
| SuperCombo frame rows | 83 |
| crosswalk 自動一致 | 47 |
| crosswalk name override 一致 | 26 |
| 公式側未照合 | 2 |
| enriched | 47 |
| enriched_reviewed | 26 |
| official_only | 2 |
| human review accepted | 26 |
| enriched_review_required | 0 |
| SuperCombo-only row | 13 |

レビュー済み 26 行は、Sun Crest stock level、OD Sun Shot 共有 row、SA1 / SA2 stock level、Drive Rush などを `move_id` で補助リンクしたもの。公式列は上書きせず、SuperCombo 値は `supercombo_*` 補助列として保持する。

## moveType 件数

| moveType | rows |
|---|---:|
| ground_normal | 19 |
| air_normal | 7 |
| drive | 6 |
| throw | 2 |
| special | 36 |
| super | 9 |
| taunt | 4 |

## 注意点

- `validation.json` の warning は `156 imageinfo titles are missing`。resolved は `File:SF6 Ingrid Face.png` と `File:SF6 Ingrid Portrait.png` の 2 件のみ。
- move / hitbox 画像の大半は `imageinfo` で解決できていない。raw wikitext と image refs は保持しているが、画像そのものは face / portrait 以外ほぼ欠けている。
- duplicate input は `6HPHK` と `236236P` の 2 種類。block/recovery variant と SA3/CA variant が同じ input を共有するため、input は主キーにせず、SuperCombo raw 内では `moveId` を行識別子として扱う。
- `moveType` には `Special` / `Super` の大文字表記が混じるため、後続の派生データ生成では小文字正規化して section と照合する必要がある。
- official data との crosswalk は作成済み。公式にある基本フレーム値は Capcom 公式 data を優先し、SuperCombo は raw source と補助情報として保持する。
- `enriched_review_required` は 0。レビュー対象 26 行は `human_review_status: accepted` として記録済み。
- SuperCombo-only 9 行については [[reviews/2026-06-02-supercombo-ingrid-supercombo-only-prereview]] で事前レビューした。これは accept ではなく、公式 row への照合や `human_review_status` の変更も行っていない。特殊隠しコマンド / Monoid 操作に関係する通常利用外 row として、通常の Ingrid frame-data 回答からは分離する。

## 人間レビューが必要な項目

- imageinfo missing 156 件が source 側の欠損なのか、filename 正規化や API title 変換で再解決可能なのか。
- 公式 row に直接照合しない SuperCombo-only 9 行（Big Laser?、Burnout Attack?、Sun Octopus?、Monoid 関連）について、既存の `suggested_handling` の `supercombo_only` を将来 `supercombo_only_hidden_command` や `supercombo_only_taunt_summon` のように細分化する必要があるか。事前レビューは [[reviews/2026-06-02-supercombo-ingrid-supercombo-only-prereview]] に記録済みだが、accept にはしていない。

## 追加生成した成果物

- [[outputs/reports/2026-06-02-supercombo-ingrid-official-crosswalk]]
- [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]
- `wiki/outputs/data/frame-data/supercombo/ingrid/`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/`
