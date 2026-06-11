---
type: review
review_type: capture_validation
title: "SuperCombo Offense web-page capture review"
created: 2026-06-11
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-offense]]"
raw_paths:
  - "raw/web-pages/wiki.supercombo.gg/offense/manifest.json"
tags:
  - sf6
  - supercombo
  - offense
  - web-page-capture
  - capture-validation
  - numeric-source
aliases:
  - "SuperCombo Offense web page capture review"
  - "SuperCombo Offense Webページ取得レビュー"
---

# SuperCombo Offense Webページ取得レビュー - 2026-06-11

## 要約

SuperCombo Wiki の `Street Fighter 6/Offense` を `raw/web-pages/` 配下の Web page 取得一式として保存し、wiki source page へ ingest した。Offense page は通常投げ、throw range、throw invincibility、throw loop、counter / punish counter、corner dizzy、blockstring、safe jump、empty jump mixup など、攻めの timing と community tactical claim を含む source として扱う。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/wiki.supercombo.gg/offense/manifest.json` |
| Source URL | `https://wiki.supercombo.gg/w/Street_Fighter_6/Offense` |
| Platform | MediaWiki |
| Canonical raw 取得物 | `page.raw.wikitext` |
| Original content media | none |
| Rendered content media | none |
| Display evidence | `page.html`, `rendered/main.dom.json`, `rendered/media.dom.json`, `rendered/content.scoped.html`, `screenshots/*.png` |
| Template 依存 | `api/templates.json` |
| `storage_policy` | `updateable_web_page_capture` |
| Source revision | revid `364971`, `2026-05-30T00:03:21Z` |
| Captured at | `2026-06-11T11:03:16Z` |

## Validation

`validation.json` は `passed`。HTTP page、`action=raw`、MediaWiki API、template API、render fetch はすべて取得できた。API の revision wikitext と `action=raw` の wikitext は一致した。

Rendered DOM は heading 17 件、table 2 件、image refs 30 件を記録する。本文 table は Throw Ranges 1 件、もう 1 件は SF6 Navigation。Content media は 0 件。MediaWiki API の `prop=images` 30 件は navigation / template 由来の character icons で、`metadata.json` の excluded provenance として記録し、download はしない。

## Recompile result

[[sources/supercombo-street-fighter-6-offense]] と [[concepts/offense]] を作成した。Offense page 固有の用語として [[concepts/terms/throw]]、[[concepts/terms/throw-loop]]、[[concepts/terms/safe-jump]]、[[concepts/terms/empty-jump-mixup]]、[[concepts/terms/blockstring]] を作成し、[[concepts/terms/counter-hit]]、[[concepts/terms/punish-counter]]、[[concepts/terms/stun]]、[[concepts/frame-data]]、[[concepts/drive-system]]、[[concepts/terms/index]]、[[entities/street-fighter-6]]、[[entities/supercombo-wiki]] を更新した。

## 判断

- Offense page は `raw/web-pages/wiki.supercombo.gg/offense/` に置く。Street Fighter 6 専用 repo なので raw path の page slug では game prefix を省く。
- Source freshness は `source_revision.revision_timestamp` の `2026-05-30T00:03:21Z` を優先し、raw 取得時刻 `2026-06-11T11:03:16Z` と混同しない。
- `page.raw.wikitext` を source text の正本とする。Rendered DOM の table text は throw range table の確認補助、screenshots は visual evidence として扱う。
- この source は community wiki なので、公式 source と重なる mechanics claim では公式 source を優先する。Counter / Punish Counter の一般値は Capcom eSports BASE を優先し、Offense page は throw-specific / safe-jump / tactical context の補助 source とする。
- Throw range table は source page に保持する。表は 1 件だけなので、現時点では `wiki/outputs/data/` に derived JSON を作らない。
- Character-specific throw loop notes は community tactical claim であり、公式 frame-data と同じ confidence では扱わない。

## 未解決事項

- Throw range、throw hurtbox、throw loop、safe jump values を公式 source または実機検証で照合するか。
- Character-specific throw loop notes を character entity / character source page へどの粒度で backlink するか。
- Offense / Defense / Movement / Game Data のような system page 由来の小規模 numeric tables を derived JSON にする基準をどうするか。
