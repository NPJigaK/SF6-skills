---
type: review
review_type: capture_validation
title: "CAPCOM eSports BASE terms scoped capture review"
created: 2026-06-10
status: open
sources:
  - "[[sources/capcom-esports-base-terms]]"
raw_paths:
  - "raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json"
tags:
  - sf6
  - official
  - glossary
  - capcom-esports
  - web-page-capture
  - capture-validation
  - scoped-capture
aliases:
  - "CAPCOM eSports BASE terms capture review"
  - "CAPCOM eSports BASE 用語取得レビュー"
---

# CAPCOM eSports BASE terms scoped capture review - 2026-06-10

## 要約

Capcom 公式 `CAPCOM eSports BASE` から、CPT / SFL 観戦向けの `実況ワード解説` セクションだけを `raw/web-pages/` 配下の scoped Web page capture として保存した。full page HTML と full page JavaScript は保存せず、source provenance には response metadata と hash を残した。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/sf.esports.capcom.com/base-terms/manifest.json` |
| Source URL | `https://sf.esports.capcom.com/base/` |
| Source type | `official_scoped_web_page_capture` |
| Scope policy | `capcom_esports_base_words_only` |
| Captured at | `2026-06-09T17:48:14Z` |
| Page HTML Last-Modified | `2025-11-11T06:17:24Z` |
| Page JS Last-Modified | `2025-11-11T06:17:24Z` |
| Canonical raw 取得物 | `source/word-section.raw.html`, `source/modal-open-close.raw.js`, `api/terms.raw.json`, `rendered/word-section.dom.json`, `rendered/modals/` |
| Display evidence | `screenshots/word-section.png`, `screenshots/modal-word-00.png` |
| Term count | 23 |
| Group count | 3 |
| Downloaded assets | 47 |
| Modal DOM count | 23 |

## 保存した範囲

- `実況ワード解説 / word explanation section`
- word card source HTML
- 各 term の clicked modal DOM
- word thumbnails
- word modal mp4 files
- term usage text で使う microphone icon

## 意図的に保存しなかった範囲

- top page hero
- news and external links
- word section 外の movie list
- consult / coaching content
- logos, page chrome, unrelated images
- full page HTML
- full page JavaScript
- full CSS

## Validation

`validation.json` は `passed`。主な確認内容は以下。

- full page HTML と full page JavaScript を raw artifact として保存していない。
- word section raw HTML と modal open / close JavaScript snippet が存在する。
- 23 語が存在し、term index は連続している。
- すべての term に core text、thumbnail path、video path がある。
- 3 group がすべての term を cover している。
- downloaded assets は期待数で、asset failure は 0。
- modal DOM は 23 件あり、modal words と video src が terms data と一致する。
- word section screenshot と first modal screenshot が存在する。

## 判断

自動 validation は passed。人間レビューでは、用語の意味内容そのものの妥当性ではなく、scoped capture の範囲、asset 保存範囲、HTTP `Last-Modified` を source freshness として扱うかを確認する必要がある。この source は公式の観戦用語説明として high confidence で扱えるが、ページ全体の情報源ではない。

## 未解決事項

- HTTP `Last-Modified` を source freshness として wiki 上で表示するか、artifact metadata としてのみ扱うか。
- 23 語は `wiki/concepts/terms/` に昇格済み。今後の source 追加時に、term page と source page の claim 粒度をどう分けるか。
- SuperCombo glossary の community terms と対応表を作るか。
