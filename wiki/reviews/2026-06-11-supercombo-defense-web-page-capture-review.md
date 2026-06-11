---
type: review
review_type: capture_validation
title: "SuperCombo Defense web-page capture review"
created: 2026-06-11
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-defense]]"
raw_paths:
  - "raw/web-pages/wiki.supercombo.gg/defense/manifest.json"
tags:
  - sf6
  - supercombo
  - defense
  - web-page-capture
  - capture-validation
  - numeric-source
aliases:
  - "SuperCombo Defense web page capture review"
  - "SuperCombo Defense Webページ取得レビュー"
---

# SuperCombo Defense Webページ取得レビュー - 2026-06-11

## 要約

SuperCombo Wiki の `Street Fighter 6/Defense` を `raw/web-pages/` 配下の Web page 取得一式として保存し、wiki source page へ ingest した。Defense page は blocking、throw escape、Drive Parry、wake-up、reversal buffer、armor、anti-air、punish route など、守りの timing と community tactical claim を含む source として扱う。

## 取得一式

| 項目 | 値 |
|---|---|
| Raw manifest | `raw/web-pages/wiki.supercombo.gg/defense/manifest.json` |
| Source URL | `https://wiki.supercombo.gg/w/Street_Fighter_6/Defense` |
| Platform | MediaWiki |
| Canonical raw 取得物 | `page.raw.wikitext` |
| Original content media | none |
| Rendered content media | 14 files under `images/rendered/` |
| Display evidence | `page.html`, `rendered/main.dom.json`, `rendered/media.dom.json`, `rendered/content.scoped.html`, `screenshots/*.png` |
| Template 依存 | `api/templates.json` |
| `storage_policy` | `updateable_web_page_capture` |
| Source revision | revid `364973`, `2026-05-30T00:09:39Z` |
| Captured at | `2026-06-11T11:35:33Z` |

## Validation

`validation.json` は `passed`。HTTP page、`action=raw`、MediaWiki API、template API、render fetch はすべて取得できた。API の revision wikitext と `action=raw` の wikitext は一致した。

Rendered DOM は heading 9 件、table 1 件、image refs 41 件を記録する。Table 1 件は SF6 Navigation で、本文数値表ではない。Content media は 11 refs と判定され、rendered button / direction images 14 件を保存した。MediaWiki API の `prop=images` 37 件は navigation / template 由来を含むため、excluded provenance として記録し、original media download はしない。

## Recompile result

[[sources/supercombo-street-fighter-6-defense]] と [[concepts/defense]] を作成した。Defense page 固有の入口として [[concepts/terms/blocking]]、[[concepts/terms/wake-up]]、[[concepts/terms/armor]] を作成し、既存の [[concepts/terms/throw-escape]]、[[concepts/terms/drive-parry]]、[[concepts/terms/reversal]]、[[concepts/terms/anti-air]]、[[concepts/terms/cross-up]]、[[concepts/terms/blockstring]]、[[concepts/terms/invincible-move]]、[[concepts/terms/guaranteed-punish]]、[[concepts/frame-data]]、[[concepts/drive-system]]、[[concepts/terms/index]]、[[entities/street-fighter-6]]、[[entities/supercombo-wiki]] を更新した。

## 判断

- Defense page は `raw/web-pages/wiki.supercombo.gg/defense/` に置く。Street Fighter 6 専用 repo なので raw path の page slug では game prefix を省く。
- Source freshness は `source_revision.revision_timestamp` の `2026-05-30T00:09:39Z` を優先し、raw 取得時刻 `2026-06-11T11:35:33Z` と混同しない。
- `page.raw.wikitext` を source text の正本とする。Rendered DOM は navigation table と rendered button / direction media の確認補助、screenshots は visual evidence として扱う。
- この source は community wiki なので、公式 source と重なる mechanics claim では公式 source を優先する。Drive Parry / Drive Reversal / Drive Impact / Overdrive / Super Art の一般説明は公式 Fighting Ground source を優先し、Defense page は defensive timing / tactical context の補助 source とする。
- Defense page の table は navigation table のみなので、今回は `wiki/outputs/data/` に derived JSON を作らない。
- Wake-up forced standing frames、reversal buffer、throw escape option-select restriction、dash buffer bug note は community tactical claim として保持し、公式値として断定しない。

## 未解決事項

- Throw escape window、reversal buffer、wake-up forced standing frames、armor damage を公式 source または実機検証で照合するか。
- Defense と Offense を横断して、strike / throw / shimmy / reversal / parry の defensive decision tree を synthesis にするか。
- Offense / Defense / Movement / Game Data のような system page 由来の小規模 numeric facts を derived JSON にする基準をどうするか。
