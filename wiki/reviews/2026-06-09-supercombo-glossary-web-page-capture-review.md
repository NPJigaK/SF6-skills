---
type: review
review_type: capture_validation
title: "SuperCombo glossary web-page capture review"
created: 2026-06-09
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
raw_paths:
  - "raw/web-pages/wiki.supercombo.gg/glossary/manifest.json"
tags:
  - sf6
  - supercombo
  - web-page-capture
  - capture-validation
aliases:
  - "SuperCombo glossary web page capture review"
  - "SuperCombo glossary Webページ取得レビュー"
---

# SuperCombo glossary Webページ取得レビュー - 2026-06-09

## 要約

SuperCombo Wiki の `Street Fighter 6/Glossary` を `raw/web-pages/` 配下の Web page 取得一式として保存した。MediaWiki なので `page.raw.wikitext` を原文を保つ取得物とし、`page.html` と `rendered/*.dom.json` は表示構造、table、link、image refs の検証証拠として扱う。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/wiki.supercombo.gg/glossary/manifest.json` |
| Source URL | `https://wiki.supercombo.gg/w/Street_Fighter_6/Glossary` |
| Platform | MediaWiki |
| Canonical raw 取得物 | `page.raw.wikitext` |
| Display evidence | `page.html`, `rendered/main.dom.json`, `rendered/tables.dom.json` |
| Template 依存 | `api/templates.json`, `api/template-combo-legend-sf6.json`, `templates/combo-legend-sf6.raw.wikitext` |
| `storage_policy` | `updateable_web_page_capture` |
| Source revision | revid `351898`, `2026-01-31T11:22:26Z` |
| Notation template の revision | `Template:ComboLegend-SF6` revid `283225`, `2023-12-11T18:45:25Z` |
| Captured at | `2026-06-09T13:47:52Z` |

## Validation

`validation.json` は `passed`。HTTP page、`action=raw`、MediaWiki API はすべて status 200。API の revision wikitext と `action=raw` の wikitext は一致した。Rendered DOM は heading 25 件、link 128 件、image ref 47 件、table 6 件を保持する。

2026-06-10 に、Notation Glossary の rendered table が `{{ComboLegend-SF6}}` に依存することを manifest に追記した。validation は template 一覧、`ComboLegend-SF6` revision、raw wikitext の非空、API の content と raw wikitext の一致だけを確認する。template 内容の意味検証や再帰的な template 展開は、この wiki の claim が必要とするまで増やさない。

旧 Obsidian Web Clipper capture で malformed に見えた numpad-direction table は、`rendered/tables.dom.json` の table 1 から table 4 に分かれて構造を確認できる。今後 directional notation に依存する回答では、この DOM capture を参照する。

## Recompile result

新しい web-page raw から source page と concept pages を再点検した結果、Drive System、Frame Data、Juggles の説明は旧 clipping 由来の wiki と意味内容が変わらなかった。差分は主に由来情報で、Notation Glossary は page wikitext では `{{ComboLegend-SF6}}` の template invocation として保存され、展開後の notation table は `rendered/tables.dom.json` に保存されている。notation table の本文と revision は `templates/combo-legend-sf6.raw.wikitext` と `api/template-combo-legend-sf6.json` に辿れる。

## 判断

- `raw/articles/2026-05-26-supercombo-street-fighter-6-glossary.md` は web-page capture で置き換えたため削除した。
- `raw/` は原則不変だが、manifest の `storage_policy` で最新ミラーまたは更新可能な取得一式と示されている raw 一式は更新可能にする。SuperCombo glossary は `updateable_web_page_capture` として扱う。許可する更新は原文・元データを保つ取得物の再取得、manifest / metadata / validation / hash の補正、layout 調整に限る。
- 今後の Web page source は、その source 固有の取得物を `manifest.json` で明示し、`raw/web-pages/<domain>/<repo-local-page-slug>/` に置く方針が扱いやすい。capture date や revision は path ではなく manifest に残す。この repo は Street Fighter 6 専用なので、SuperCombo Wiki の `Street Fighter 6/Glossary` は `raw/web-pages/wiki.supercombo.gg/glossary/` に置く。
- Source freshness は `source_revision.revision_timestamp` を優先し、`captured_at_utc` と混同しない。

## 未解決事項

- Web page capture で screenshot を常に保存するか、table-heavy / JS-heavy page のみ保存するか。
