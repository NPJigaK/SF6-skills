---
type: review
review_type: capture_validation
title: "SuperCombo Game Data web-page capture review"
created: 2026-06-11
updated: 2026-06-11
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-game-data]]"
raw_paths:
  - "raw/web-pages/wiki.supercombo.gg/game-data/manifest.json"
  - "raw/web-pages/wiki.supercombo.gg/game-data/validation.json"
  - "raw/web-pages/wiki.supercombo.gg/game-data/validation.tabbers.json"
raw_derived_artifacts:
  - "raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json"
tags:
  - review
  - capture-validation
  - supercombo
  - game-data
  - tabber
---

# SuperCombo Game Data web-page capture review

## Summary

SuperCombo Wiki の Street Fighter 6 Game Data page を `raw/web-pages/wiki.supercombo.gg/game-data/` に raw web-page capture として保存した。通常の MediaWiki wikitext / HTML / rendered DOM に加えて、この page 固有の tabber 付き table を検証するため `rendered/tabbers.dom.json` と `validation.tabbers.json` を追加した。

## Capture artifacts

- Canonical raw: `raw/web-pages/wiki.supercombo.gg/game-data/page.raw.wikitext`
- API response: `raw/web-pages/wiki.supercombo.gg/game-data/api/query.json`
- Template dependencies: `raw/web-pages/wiki.supercombo.gg/game-data/api/templates.json`
- Rendered evidence: `raw/web-pages/wiki.supercombo.gg/game-data/page.html`, `raw/web-pages/wiki.supercombo.gg/game-data/rendered/main.dom.json`, `raw/web-pages/wiki.supercombo.gg/game-data/rendered/content.scoped.html`, `raw/web-pages/wiki.supercombo.gg/game-data/rendered/tabbers.dom.json`
- Screenshots: `raw/web-pages/wiki.supercombo.gg/game-data/screenshots/`
- Media: `raw/web-pages/wiki.supercombo.gg/game-data/images/`
- Raw-derived table artifact: `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`

## Validation

| Check | Result |
|---|---|
| `validation.json` | `passed` |
| `validation.tabbers.json` | `passed` |
| Source revision | `365507` |
| Source updated | `2026-06-04T23:19:26Z` |
| Captured at | `2026-06-11T13:38:34Z` |
| Wikitext tabber groups | 4 |
| Tab counts by group | `30 / 3 / 4 / 9` |
| Total tabs | 46 |
| Source table or Cargo tabs | `30 / 3 / 4 / 1` |
| Page HTML tables by tabber group | `30 / 3 / 4 / 1` |
| Scoped HTML tables by tabber group | `30 / 3 / 4 / 1` |
| Rendered main DOM table count | 40 |
| Scoped content table count | 39 |

`validation.tabbers.json` は、live revision と capture revision の一致、tab label 一致、panel count 一致、source table presence と rendered table count の一致、全 tabs の live click 後に table count が安定すること、クリックした tab が requested tab として選択されることを確認している。

## Decisions

- `page.raw.wikitext` を canonical raw とし、HTML / DOM / screenshot は表示証拠として保持する。
- SF6 Navigation table は content table から除外し、raw-derived table artifact では `excluded_tables` に分離する。
- Game Data の 39 content tables は `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` に source-preserving text として保持する。これは正規化済み move schema ではない。
- `tools/web_pages/supercombo_page.py` を Game Data tabber の正式再生成 tool とし、`rendered/tabbers.dom.json`、`validation.tabbers.json`、`raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` を同じ capture pass で更新する。manifest の `game_data_tabber_pipeline` にこの経路を記録する。
- `≤5F` から `≤12F` までの Longest Punish tabs は source 上で `(to-do)` のため、table 欠落ではなく source content として記録する。

## Review notes

- Game Data は community numeric source なので、公式 Capcom source と重なる claims では公式 source を優先する。
- Character-specific scaling、System Data、Range Comparisons、Longest Punish `≤4F` は有用だが、値の公式照合または実機検証は未完了。
- この capture は raw integrity と tabber completeness の自動検証であり、各 table value の gameplay correctness を accepted にするレビューではない。

## Follow-up

- Character-specific scaling tabs を moveId-linked schema に正規化するか判断する。
- System Data / Range Comparisons / Punish option values の照合 source を決める。
- Longest Punish `≤5F` 以降が source 上で更新されたら、`tools/web_pages/supercombo_page.py` で raw、tabber validation、derived table output を一体で再生成する。
