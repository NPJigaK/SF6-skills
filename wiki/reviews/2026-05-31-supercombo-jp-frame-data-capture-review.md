---
type: review
review_type: capture_validation
created: 2026-05-31
status: open
sources:
  - "[[sources/supercombo-jp-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/supercombo-wiki]]"
  - "[[entities/jp]]"
aliases:
  - "SuperCombo JP capture review"
tags:
  - review
  - frame-data
  - supercombo
---

# SuperCombo JP フレームデータ capture review - 2026-05-31

## 要約

SuperCombo Wiki JP フレームデータの raw capture は、自動検証で passed。生 wikitext、Cargo API、表示 DOM、5タブ分のページ全体スクリーンショット、画像 download を保存し、raw/Cargo/DOM の表値照合まで通した。人間レビューは未完了なので status は open。

## レビュー対象

- `raw/supercombo/frame-data/2026-05-31/jp/data.raw.wikitext`
- `raw/supercombo/frame-data/2026-05-31/jp/frame-data.raw.wikitext`
- `raw/supercombo/frame-data/2026-05-31/jp/data.templates.json`
- `raw/supercombo/frame-data/2026-05-31/jp/frame-data.cargo-queries.json`
- `raw/supercombo/frame-data/2026-05-31/jp/cargo/frame-data.json`
- `raw/supercombo/frame-data/2026-05-31/jp/cargo/character-data.json`
- `raw/supercombo/frame-data/2026-05-31/jp/rendered/tables.dom.json`
- `raw/supercombo/frame-data/2026-05-31/jp/screenshots/general.png`
- `raw/supercombo/frame-data/2026-05-31/jp/screenshots/details.png`
- `raw/supercombo/frame-data/2026-05-31/jp/screenshots/meter.png`
- `raw/supercombo/frame-data/2026-05-31/jp/screenshots/properties.png`
- `raw/supercombo/frame-data/2026-05-31/jp/screenshots/notes.png`
- `raw/supercombo/frame-data/2026-05-31/jp/imageinfo.json`
- `raw/supercombo/frame-data/2026-05-31/jp/image-manifest.json`
- `raw/supercombo/frame-data/2026-05-31/jp/images/files/`
- `raw/supercombo/frame-data/2026-05-31/jp/metadata.json`
- `raw/supercombo/frame-data/2026-05-31/jp/validation.json`
- `raw/supercombo/frame-data/2026-05-31/jp/manifest.json`

## 履歴上の raw path 注記

この review page の date-based raw path は 2026-05-31 時点の履歴表記。現在の raw entrypoint は `raw/frame-data/supercombo/jp/manifest.json` の latest mirror 固定パスで、source freshness は `source_updated_at` / `source_revision`、raw 取得時刻は `captured_at_utc` で確認する。

## 確認内容

- Scrapling `StealthySession` で SuperCombo から直接取得した。Jina などの第三者 cache/API は使っていない。
- `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 64 件を抽出した。
- Cargo API の `SF6_FrameData` 64 行、`SF6_CharacterData` 1 行が raw template 件数と一致した。
- `Frame_data?action=raw` にある表示 Cargo query 21 件を保存した。
- 表示 DOM は `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 tab state を含む。
- 4 section x 5 tab = 20 table comparisons で、header、row count、input order、cell values を照合した。
- 5枚の full-page screenshot は目視で確認した。ページ上部、Character Data、該当タブの 4 section table、下部 navigation、footer が写っている。
- screenshot state では iframe と visible ad count が 0。capture 用に ad/iframe/sticky UI は除去している。
- 123 件の resolved image を download した。failed image download は 0。
- `python3 -m py_compile tools/capture_supercombo_frame_data.py tools/validate_supercombo_frame_data.py` は成功。

## 検証サマリー

| 項目 | 値 |
|---|---:|
| character templates | 1 |
| frame templates | 64 |
| display Cargo queries | 21 |
| Cargo frame rows | 64 |
| Cargo character rows | 1 |
| rendered tab states | 5 |
| table comparisons | 20 |
| image refs | 143 |
| imageinfo resolved | 123 |
| imageinfo missing | 11 |
| downloaded images | 123 |
| failed image downloads | 0 |

## 注意点

- `validation.json` の warning は `11 imageinfo titles are missing`。raw wikitext 内の参照は保持しているが、MediaWiki `imageinfo` では解決できなかった。
- duplicate input は `6HPHK` と `236236K`。input は主キーにせず、SuperCombo raw 内では `moveId` を行識別子として扱う。
- official data との crosswalk はまだ作成していない。公式にある基本フレーム値は Capcom 公式 data を優先し、SuperCombo は raw source として完全保存する。

## 人間レビューが必要な項目

- missing imageinfo 11 件が source 側の欠損なのか、filename 正規化で再解決可能なのか。
- duplicate input rows の差分を、後続の merge schema で `notes`、`moveId`、condition、variant としてどう表すか。
- official JP data と SuperCombo JP data の crosswalk policy。
