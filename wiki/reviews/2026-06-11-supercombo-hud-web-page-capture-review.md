---
type: review
review_type: capture_validation
title: "SuperCombo HUD web-page capture review"
created: 2026-06-11
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-hud]]"
raw_paths:
  - "raw/web-pages/wiki.supercombo.gg/hud/manifest.json"
tags:
  - sf6
  - supercombo
  - hud
  - visual-source
  - web-page-capture
  - capture-validation
aliases:
  - "SuperCombo HUD web page capture review"
  - "SuperCombo HUD Webページ取得レビュー"
---

# SuperCombo HUD Webページ取得レビュー - 2026-06-11

## 要約

SuperCombo Wiki の `Street Fighter 6/HUD` を `raw/web-pages/` 配下の Web page 取得一式として保存した。HUD は画像情報の比重が高いため、MediaWiki wikitext に加えて、本文に属する HUD semantic media、rendered media、navigation を除いた scoped screenshots を保存した。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/wiki.supercombo.gg/hud/manifest.json` |
| Source URL | `https://wiki.supercombo.gg/w/Street_Fighter_6/HUD` |
| Platform | MediaWiki |
| Canonical raw 取得物 | `page.raw.wikitext` |
| Original content media | `images/files/` |
| Rendered content media | `images/rendered/` |
| Display evidence | `page.html`, `rendered/main.dom.json`, `rendered/media.dom.json`, `rendered/content.scoped.html`, `screenshots/*.png` |
| Template 依存 | `api/templates.json` |
| `storage_policy` | `updateable_web_page_capture` |
| Source revision | revid `345794`, `2026-01-03T12:40:35Z` |
| Captured at | `2026-06-11T01:00:31Z` |

## Validation

`validation.json` は `passed`。HTTP page、`action=raw`、MediaWiki API、template API、render fetch はすべて取得できた。API の revision wikitext と `action=raw` の wikitext は一致した。Rendered DOM は heading 4 件、link 115 件、table 2 件、image refs 44 件を記録する。

MediaWiki API の `prop=images` は template transclusion 後の画像を返すため、HUD page 本文に属さない navigation / character icon も含む。今回の raw media scope では、HUD semantic content media 14 件だけを `imageinfo.json` と `images/files/` に保存し、navigation / template 由来の 30 件は `metadata.json` の excluded provenance として記録した。これにより、character icon 画像を HUD source content と誤認しない。

## Recompile result

Source page と [[concepts/drive-system]]、[[concepts/frame-data]]、[[entities/street-fighter-6]]、[[entities/supercombo-wiki]] を更新した。HUD page 由来の claim は、HUD 表示や icon 表示の community / visual source として扱い、Drive Gauge、Burnout、Super Art、Counter / Punish Counter など公式 source と重なる mechanics claim では公式 source を優先する方針にした。

## 判断

- HUD page は `raw/web-pages/wiki.supercombo.gg/hud/` に置く。Street Fighter 6 専用 repo なので raw path の page slug では game prefix を省く。
- Source freshness は `source_revision.revision_timestamp` の `2026-01-03T12:40:35Z` を優先し、raw 取得時刻 `2026-06-11T01:00:31Z` と混同しない。
- `page.raw.wikitext` を source text の正本とする。画像は source text の置き換えではなく、HUD 表示・icon visual evidence として扱う。
- `api/query.json` は MediaWiki の `prop=images` response を原文に近い provenance として保持する。一方、downloaded raw media は本文の HUD semantic content media に限定する。
- この取得一式は `storage_policy: updateable_web_page_capture` なので、原文・元データを保つ再取得、manifest / metadata / validation / hash の補正を許す。翻訳、要約、正規化した置き換え版は raw に置かない。

## 未解決事項

- Capcom 公式の HUD / game screen 説明 source を追加 ingest し、HUD 表示要素と icon 表示の official evidence と照合するか。
- HUD icon の個別 term page 反映は、公式 source 追加後に行うか、community visual source として先に薄く追加するか。
- large video / long image sequence を扱う raw package の保存基準を、今回の scoped screenshot policy から拡張するか。
