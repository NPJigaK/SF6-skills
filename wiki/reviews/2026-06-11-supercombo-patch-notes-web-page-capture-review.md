---
type: review
review_type: capture_validation
created: 2026-06-11
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
related:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
aliases:
  - "SuperCombo Patch Notes capture review"
tags:
  - review
  - patch-notes
  - battle-change
  - supercombo
---

# SuperCombo Patch Notes capture review - 2026-06-11

## 要約

SuperCombo Wiki の Street Fighter 6 Patch Notes page と、rendered table から見つかった 17 件の `Street Fighter 6/Version/*` detail page を raw web-page capture として保存した。自動 validation は通過しているが、人間レビューは未実施なので status は open のままにする。

## Capture 対象

| 項目 | 値 |
|---|---|
| Source URL | `https://wiki.supercombo.gg/w/Street_Fighter_6/Patch_Notes` |
| Raw manifest | `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json` |
| Version capture root | `raw/web-pages/wiki.supercombo.gg/patch-notes/versions/` |
| Version rows | 17 |
| Detail validations | 17 passed / 17 captured |
| Derived output | `wiki/outputs/data/battle-change/supercombo-patch-notes/` |

## 自動検証

- `tools/web_pages/supercombo_page.py` で Patch Notes 本体と 17 detail pages を取得した。
- Patch Notes 本体の `validation.json` は `passed`。
- `validation.batch.json` は、Patch Notes table 17 rows、detail page capture 17/17、detail validation 17/17 passed を確認した。
- `versions.json` は rendered table 0 から `version`、`gameversion`、`date`、`summary`、external Patch Notes link を抽出し、各 detail raw capture へリンクする。
- `official-battle-change-crosswalk.json` は SuperCombo の external Patch Notes link から Capcom official Battle Change id を抽出し、既存 `wiki/outputs/data/battle-change/official/versions.json` と突き合わせる。

## 集計

| Metric | Count |
|---|---:|
| SuperCombo version rows | 17 |
| Captured detail pages | 17 |
| Detail validation passed | 17 |
| Official Battle Change matched rows | 16 |
| SuperCombo rows without official Battle Change link | 1 |
| Official Battle Change rows without SuperCombo link | 4 |

## 注意点

- Patch Notes 本体の wikitext は Cargo query だけなので、一覧 row の source-preserving evidence は rendered DOM と derived JSON にある。各 version の詳細本文は detail page の `page.raw.wikitext` が正本。
- Official Battle Change と SuperCombo Patch Notes は authority が異なる。Capcom 公式 source と重なる変更説明では公式を優先し、SuperCombo は community detail / terminology source として扱う。
- Official Battle Change の `20251113`、`20251022`、`20250901`、`20230808` は SuperCombo Patch Notes table から直接リンクされていない。
- `1.00` は launch version で公式 `battle_change` id を持たない。

## 最終判断

自動 validation は passed。人間レビューでは、代表 version の wikitext と rendered display、official crosswalk の対応方針、official-only update 4 件の扱いを確認する必要がある。
