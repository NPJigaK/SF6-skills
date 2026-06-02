---
type: review
review_type: capture_validation
created: 2026-06-02
status: open
sources:
  - "[[sources/supercombo-zangief-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/supercombo-wiki]]"
  - "[[entities/zangief]]"
aliases:
  - "SuperCombo Zangief capture review"
tags:
  - review
  - frame-data
  - supercombo
---

# SuperCombo Zangief フレームデータ取得レビュー - 2026-06-02

## 要約

SuperCombo Wiki Zangief フレームデータの raw 取得データは、自動検証を通過した。生 wikitext、Cargo API、表示 DOM、5タブ分のページ全体スクリーンショット、画像ダウンロード結果を保存し、raw/Cargo/DOM の表値照合まで通した。raw 取得データ全体の review status は `open` のままだが、公式補助データのレビュー対象 25 行は [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] で `accepted` 済み。

## レビュー対象

- `raw/frame-data/supercombo/zangief/data.raw.wikitext`
- `raw/frame-data/supercombo/zangief/frame-data.raw.wikitext`
- `raw/frame-data/supercombo/zangief/data.templates.json`
- `raw/frame-data/supercombo/zangief/frame-data.cargo-queries.json`
- `raw/frame-data/supercombo/zangief/cargo/frame-data.json`
- `raw/frame-data/supercombo/zangief/cargo/character-data.json`
- `raw/frame-data/supercombo/zangief/rendered/tables.dom.json`
- `raw/frame-data/supercombo/zangief/screenshots/general.png`
- `raw/frame-data/supercombo/zangief/screenshots/details.png`
- `raw/frame-data/supercombo/zangief/screenshots/meter.png`
- `raw/frame-data/supercombo/zangief/screenshots/properties.png`
- `raw/frame-data/supercombo/zangief/screenshots/notes.png`
- `raw/frame-data/supercombo/zangief/imageinfo.json`
- `raw/frame-data/supercombo/zangief/image-manifest.json`
- `raw/frame-data/supercombo/zangief/images/files/`
- `raw/frame-data/supercombo/zangief/metadata.json`
- `raw/frame-data/supercombo/zangief/validation.json`
- `raw/frame-data/supercombo/zangief/manifest.json`

## 確認内容

- Scrapling `StealthySession` で SuperCombo から直接取得した。Jina などの第三者 cache/API は使っていない。
- `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 68 件を抽出した。
- Cargo API の `SF6_FrameData` 68 行、`SF6_CharacterData` 1 行が raw template 件数と一致した。
- `Frame_data?action=raw` にある表示 Cargo query 21 件を保存した。
- 表示 DOM は `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 種類の tab state を含む。
- 4 section x 5 tab = 20 table comparisons で、header、row count、input order、cell values を照合した。
- screenshot state では iframe と visible ad count が 0。取得用に ad/iframe/sticky UI は除去している。
- 解決できた画像 165 件をダウンロードした。画像ダウンロード失敗は 0 件。
- `python -m py_compile tools/extract_supercombo_frame_data.py` は成功。

## 検証サマリー

| 項目 | 値 |
|---|---:|
| character template 数 | 1 |
| frame template 数 | 68 |
| 表示 Cargo query 数 | 21 |
| Cargo frame row 数 | 68 |
| Cargo character row 数 | 1 |
| 表示 tab state 数 | 5 |
| table comparison 数 | 20 |
| 画像参照数 | 185 |
| imageinfo 解決数 | 165 |
| imageinfo missing 数 | 4 |
| ダウンロード画像数 | 165 |
| 画像ダウンロード失敗数 | 0 |

## moveType 件数

| moveType | rows |
|---|---:|
| ground_normal | 23 |
| air_normal | 9 |
| drive | 6 |
| throw | 6 |
| special | 15 |
| super | 5 |
| taunt | 4 |

## 注意点

- `validation.json` の warning は `4 imageinfo titles are missing`。未解決 title は `File:SF6 Zangief 360hp.png`、`File:SF6 Zangief 360mp.png`、`File:SF6 Zangief 63214k mid.png`、`File:SF6 Zangief jhk hold.png`。
- duplicate input は `6HPHK` と `720+P` の 2 種類。block/recovery variant と SA3/CA variant が同じ input を共有するため、input は主キーにせず、SuperCombo raw 内では `moveId` を行識別子として扱う。
- official data との照合はレビュー用候補。公式にある基本フレーム値は Capcom 公式 data を優先し、SuperCombo は raw source として完全保存する。
- `ツンドラストーム` は公式値と SuperCombo 値で startup / active duration の単純比較差分があるため、enriched 側では conflict flag を残している。

## 残る人間レビューが必要な項目

- imageinfo missing 4 件が source 側の欠損なのか、filename 正規化で再解決可能なのか。

## 補助データレビュー反映済み

- `enriched_review_required` だった 25 行は、公式値を正とした補助リンクとして人間レビュー済み。
- Zangief 専用 name override 24 件は `accepted`。`zangief_236236p` の row 再利用は `movement_variant_supplemental_link` として扱う。
- `ツンドラストーム` の startup / active duration 差分は `conflict_supplemental_only` として保持し、公式値を上書きしない。
