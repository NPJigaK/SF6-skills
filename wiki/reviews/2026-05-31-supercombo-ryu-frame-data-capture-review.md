---
type: review
review_type: capture_validation
created: 2026-05-31
status: open
sources:
  - "[[sources/supercombo-ryu-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/supercombo-wiki]]"
  - "[[entities/ryu]]"
aliases:
  - "SuperCombo Ryu capture review"
tags:
  - review
  - frame-data
  - supercombo
---

# SuperCombo Ryu フレームデータ capture review - 2026-05-31

## 要約

SuperCombo Wiki Ryu フレームデータの raw capture は、自動検証で passed。生 wikitext、Cargo API、表示 DOM、5タブ分のページ全体スクリーンショット、画像 download を保存し、raw/Cargo/DOM の表値照合まで通した。人間レビューは未完了なので status は open。

## レビュー対象

- `raw/supercombo/frame-data/2026-05-31/ryu/data.raw.wikitext`
- `raw/supercombo/frame-data/2026-05-31/ryu/frame-data.raw.wikitext`
- `raw/supercombo/frame-data/2026-05-31/ryu/data.templates.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/frame-data.cargo-queries.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/cargo/frame-data.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/cargo/character-data.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/rendered/tables.dom.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/screenshots/general.png`
- `raw/supercombo/frame-data/2026-05-31/ryu/screenshots/details.png`
- `raw/supercombo/frame-data/2026-05-31/ryu/screenshots/meter.png`
- `raw/supercombo/frame-data/2026-05-31/ryu/screenshots/properties.png`
- `raw/supercombo/frame-data/2026-05-31/ryu/screenshots/notes.png`
- `raw/supercombo/frame-data/2026-05-31/ryu/imageinfo.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/image-manifest.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/images/files/`
- `raw/supercombo/frame-data/2026-05-31/ryu/metadata.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/validation.json`
- `raw/supercombo/frame-data/2026-05-31/ryu/manifest.json`

## 確認内容

- Scrapling `StealthySession` で SuperCombo から直接取得した。Jina などの第三者 cache/API は使っていない。
- `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 77 件を抽出した。
- Cargo API の `SF6_FrameData` 77 行、`SF6_CharacterData` 1 行が raw template 件数と一致した。
- `Frame_data?action=raw` にある表示 Cargo query 21 件を保存した。
- 表示 DOM は `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 tab state を含む。
- 4 section x 5 tab = 20 table comparisons で、header、row count、input order、cell values を照合した。
- 5枚の full-page screenshot は目視で確認した。ページ上部、Character Data、該当タブの 4 section table、下部 navigation、footer が写っている。
- screenshot state では iframe と visible ad count が 0。capture 用に ad/iframe/sticky UI は除去している。
- 133 件の resolved image を download した。failed image download は 0。
- `uv run python -m py_compile tools/capture_supercombo_frame_data.py tools/validate_supercombo_frame_data.py` は成功。

## 検証サマリー

| 項目 | 値 |
|---|---:|
| character templates | 1 |
| frame templates | 77 |
| display Cargo queries | 21 |
| Cargo frame rows | 77 |
| Cargo character rows | 1 |
| rendered tab states | 5 |
| table comparisons | 20 |
| image refs | 173 |
| imageinfo resolved | 133 |
| imageinfo missing | 1 |
| downloaded images | 133 |
| failed image downloads | 0 |

## 注意点

- `validation.json` の warning は `1 imageinfo titles are missing`。missing title は `File:SF6 Ryu 236p hitbox.png`。
- duplicate input は 10 種類。Denjin / hold level / CA などで同じ input を複数 row が共有するため、input は主キーにせず、SuperCombo raw 内では `moveId` を行識別子として扱う。
- Ryu では `moveType` に `Special` / `Super` の大文字表記があるため、validator と派生データ生成で小文字正規化している。
- official data との crosswalk は review 用候補。公式にある基本フレーム値は Capcom 公式 data を優先し、SuperCombo は raw source として完全保存する。

## 人間レビューが必要な項目

- missing imageinfo 1 件が source 側の欠損なのか、filename 正規化で再解決可能なのか。
- duplicate input rows の差分を、後続の merge schema で `notes`、`moveId`、condition、variant としてどう表すか。
- Ryu の `enriched_review_required` 13件を補助リンクとして採用できるか。
