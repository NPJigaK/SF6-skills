---
type: review
review_type: capture_validation
title: "SuperCombo controls web-page capture review"
created: 2026-06-11
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-controls]]"
raw_paths:
  - "raw/web-pages/wiki.supercombo.gg/controls/manifest.json"
tags:
  - sf6
  - supercombo
  - controls
  - web-page-capture
  - capture-validation
aliases:
  - "SuperCombo controls web page capture review"
  - "SuperCombo controls Webページ取得レビュー"
---

# SuperCombo controls Webページ取得レビュー - 2026-06-11

## 要約

SuperCombo Wiki の `Street Fighter 6/Controls` を `raw/web-pages/` 配下の Web page 取得一式として保存した。MediaWiki なので `page.raw.wikitext` を原文を保つ取得物とし、`page.html` と `rendered/*.dom.json` は表示構造、table、link、image refs の検証証拠として扱う。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/wiki.supercombo.gg/controls/manifest.json` |
| Source URL | `https://wiki.supercombo.gg/w/Street_Fighter_6/Controls` |
| Platform | MediaWiki |
| Canonical raw 取得物 | `page.raw.wikitext` |
| Display evidence | `page.html`, `rendered/main.dom.json`, `rendered/tables.dom.json` |
| Template 依存 | `api/templates.json` |
| `storage_policy` | `updateable_web_page_capture` |
| Source revision | revid `365425`, `2026-06-03T09:40:46Z` |
| Captured at | `2026-06-11T00:01:49Z` |

## Validation

`validation.json` は `passed`。HTTP page、`action=raw`、MediaWiki API、template API はすべて取得できた。API の revision wikitext と `action=raw` の wikitext は一致した。Rendered DOM は heading 7 件、link 109 件、image ref 32 件、table 4 件を保持する。

Direct template dependencies は `Template:Clr` と `Template:Navbox-SF6` 系で、主要本文を別 template に逃がしている形ではない。`Template:Clr` は Modern Controls の inline label formatting、`Navbox` 系は navigation として扱い、本文の canonical raw は `page.raw.wikitext` とする。

## Recompile result

Source page と [[concepts/fighting-game-notation]] を更新し、Controls page 由来の numpad notation、Classic notation、button nickname、Classic / Modern control type の source claim を追加した。公式 source ではないため、Modern Controls の damage penalty claim や simple input の評価は community source fact として保持し、公式確認待ちの扱いにした。

## 判断

- Controls page は `raw/web-pages/wiki.supercombo.gg/controls/` に置く。Street Fighter 6 専用 repo なので raw path の page slug では game prefix を省く。
- Source freshness は `source_revision.revision_timestamp` の `2026-06-03T09:40:46Z` を優先し、raw 取得時刻 `2026-06-11T00:01:49Z` と混同しない。
- この取得一式は `storage_policy: updateable_web_page_capture` なので、原文・元データを保つ再取得、manifest / metadata / validation / hash の補正を許す。翻訳、要約、正規化した置き換え版は raw に置かない。

## 未解決事項

- Capcom 公式 controls / control type source を追加 ingest し、Modern Controls、simple input damage penalty、button mapping の official evidence と照合するか。
