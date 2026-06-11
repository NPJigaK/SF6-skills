---
type: review
review_type: capture_validation
title: "SuperCombo Gauges web-page capture review"
created: 2026-06-11
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-gauges]]"
raw_paths:
  - "raw/web-pages/wiki.supercombo.gg/gauges/manifest.json"
tags:
  - sf6
  - supercombo
  - gauges
  - drive-system
  - web-page-capture
  - capture-validation
  - numeric-source
aliases:
  - "SuperCombo Gauges web page capture review"
  - "SuperCombo Gauges Webページ取得レビュー"
---

# SuperCombo Gauges Webページ取得レビュー - 2026-06-11

## 要約

SuperCombo Wiki の `Street Fighter 6/Gauges` を `raw/web-pages/` 配下の Web page 取得一式として保存し、wiki source page へ ingest した。Drive / Super Gauge の数値が重要な source なので、source page には rendered table 0-12 の主要数値を compiled view として保持し、`wiki/outputs/data/gauges/supercombo/numeric-tables.json` に source-preserving derived JSON も作成した。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/wiki.supercombo.gg/gauges/manifest.json` |
| Source URL | `https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges` |
| Platform | MediaWiki |
| Canonical raw 取得物 | `page.raw.wikitext` |
| Original content media | `images/files/` |
| Rendered content media | `images/rendered/` |
| Display evidence | `page.html`, `rendered/main.dom.json`, `rendered/media.dom.json`, `rendered/content.scoped.html`, `screenshots/*.png` |
| Template 依存 | `api/templates.json` |
| `storage_policy` | `updateable_web_page_capture` |
| Source revision | revid `365841`, `2026-06-07T12:31:40Z` |
| Captured at | `2026-06-11T01:23:20Z` |

## Validation

`validation.json` は `passed`。HTTP page、`action=raw`、MediaWiki API、template API、render fetch はすべて取得できた。API の revision wikitext と `action=raw` の wikitext は一致した。

Rendered DOM は heading 18 件、table 14 件、image refs 64 件を記録する。本文 table は 0-12、table 13 は SF6 Navigation。Content media は 8 original files と 28 rendered image files を保存した。MediaWiki API の `prop=images` 45 件のうち、navigation / template 由来など本文 media ではない 37 件は `metadata.json` の excluded provenance として記録した。

## Recompile result

[[sources/supercombo-street-fighter-6-gauges]] を作成し、[[concepts/drive-system]]、[[concepts/frame-data]]、主要 Drive / Super Art term pages、[[entities/street-fighter-6]]、[[entities/supercombo-wiki]] を更新した。特に `Drive Impact - Forward Movement & Maximum Range` と `Drive Rush Distance Comparison` の 30 character table は省略せず source page と `wiki/outputs/data/gauges/supercombo/numeric-tables.json` に保持した。

## 判断

- Gauges page は `raw/web-pages/wiki.supercombo.gg/gauges/` に置く。Street Fighter 6 専用 repo なので raw path の page slug では game prefix を省く。
- Source freshness は `source_revision.revision_timestamp` の `2026-06-07T12:31:40Z` を優先し、raw 取得時刻 `2026-06-11T01:23:20Z` と混同しない。
- `page.raw.wikitext` を source text の正本とする。Rendered DOM の table text は数値確認の補助、画像と screenshots は visual evidence として扱う。
- この source は community wiki なので、公式 source と重なる mechanics claim では公式 source を優先する。公式 source が未収録の regeneration、cooldown、character distance values は community source fact として明示して使う。
- Drive action cost table の icon template は rendered DOM で text 化されないため、cost claim は source section text と raw wikitext template notationを併用して読む。

## 未解決事項

- Drive regeneration、cooldown、Drive Impact range、Drive Rush distance values を公式 source または実機検証で照合するか。
- `wiki/outputs/data/gauges/supercombo/numeric-tables.json` の schema を、他の gauge / system numeric source にも使う標準 schema として固定するか。
- `Drive Rush from Parry` の cost 表記を、cost table の `1/2` と section / caption text の `1 Drive Stock` の component 分解として扱うか、source-internal conflict として保持するか。
