---
type: source
source_type: community_patch_notes
title: "Street Fighter 6/Patch Notes"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Patch_Notes"
created: 2026-06-11
updated: 2026-06-11
source_updated_at: 2026-06-02T03:12:40Z
captured_at_utc: 2026-06-11T03:22:47Z
status: active
confidence: medium
tags:
  - sf6
  - patch-notes
  - battle-change
  - supercombo
  - community-wiki
  - web-page-capture
aliases:
  - "SF6 Patch Notes"
  - "Street Fighter 6 Patch Notes"
  - "SuperCombo SF6 Patch Notes"
related_concepts:
  - "[[concepts/frame-data]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 Patch Notes

## 1行要約

SuperCombo Wiki の Street Fighter 6 Patch Notes page と、そこからリンクされる 17 件の `Street Fighter 6/Version/*` detail page を raw web-page capture として保存した community source。各 version detail page の wikitext が、システム変更、character 変更、bug fix、release patch の本文根拠になる。

## 重要ポイント

1. Raw entrypoint は `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json`。Patch Notes 本体の canonical raw は `page.raw.wikitext` だが、本体 wikitext は Cargo query を持つだけなので、version 一覧は `rendered/main.dom.json` table 0 と `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json` で確認する。
2. Detail page は `raw/web-pages/wiki.supercombo.gg/patch-notes/versions/<version-slug>/manifest.json` に 17 件保存した。全 detail page の `validation.json` は `passed`。
3. Patch Notes 本体の MediaWiki revid は `276775`、revision timestamp は `2023-09-27T14:23:05Z`。detail pages の最新 source freshness は `2.0301` の `2026-06-02T03:12:40Z`。
4. `validation.batch.json` は `passed`。Patch Notes table 17 rows、detail page capture 17/17、official Battle Change link match 16 rows、official link なし 1 row、official 側だけにある update 4 rows を記録する。
5. 派生 output は `wiki/outputs/data/battle-change/supercombo-patch-notes/` に置いた。`versions.json` は SuperCombo version rows、`official-battle-change-crosswalk.json` は Capcom 公式 Battle Change List との明示 link 対応、`change-events.json` / `move-change-index.json` は detail page の top-level bullet 1374 events / 1118 targets を community source index として保持する。
6. `change-events.json` は nested bullet と wikitext table text も event に保持するため、SuperCombo 側の「この変更で何が可能/不可能になったか」「どの combo / juggle / blockstring へ影響したか」という説明を検索しやすい。556 events は明示的な `A → B` 数値変更を持つ。
7. SuperCombo version pages は community detail / synthesis source であり、Capcom 公式 Battle Change List を上書きする source ではない。公式 update text は [[sources/capcom-official-battle-change-list]] を優先し、SuperCombo は補助的な detail / wiki terminology source として扱う。
8. `tools.battle_change.supercombo.extract` は、root DOM table と 17 detail page manifests から `versions.json`、`official-battle-change-crosswalk.json`、`version-captures.json`、`validation.batch.json` を再生成し、その後 `change-events.json` / `move-change-index.json` を更新する。
9. fighter event は SuperCombo 表示名由来の `fighter_key` を保持し、frame-data output との join には `character_slug` を使う。`Akuma` / `E. Honda` / `M. Bison` は `gouki_akuma` / `ehonda` / `vega_mbison` に対応する。

## Version summary

根拠は `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json` と各 detail page の `page.raw.wikitext`。

| Version | Date | Summary | Official Battle Change link | Detail volume |
|---|---:|---|---|---:|
| `2.0301` | 2026-05-28 | Ingrid Release. Minor system changes and bug fixes. | `20260528` | 68 bullet lines |
| `2.0202` | 2026-04-15 | Bug fixes for the game system as well as JP and M. Bison. | `20260415` | 13 bullet lines |
| `2.02` | 2026-03-17 | Alex Release. Balance changes for all characters. | `20260317` | 288 bullet lines |
| `2.0111` | 2025-12-16 | Bug fixes and minor adjustments, primarily for Elena, Mai, and Sagat. | `20251216` | 38 bullet lines |
| `2.01` | 2025-10-15 | C. Viper Release. Minor bug fixes and adjustments for some characters. | `20251015` | 48 bullet lines |
| `2.00` | 2025-08-05 | Sagat Release. Minor bug fixes and adjustments. | `20250805` | 36 bullet lines |
| `1.10` | 2025-06-03 | Elena Release. Balance changes for all characters. | `202506` | 591 bullet lines |
| `1.09` | 2025-02-05 | Mai Release. Minor bug fixes. | `20250205` | 41 bullet lines |
| `1.08` | 2024-12-02 | Minor balance changes for all characters. | `20241202` | 520 bullet lines |
| `1.07` | 2024-09-24 | Terry Release. Minor balance changes and bug fixes. | `20240924` | 208 bullet lines |
| `1.06` | 2024-06-26 | M. Bison Release. Minor balance changes and bug fixes. | `20240626` | 89 bullet lines |
| `1.05` | 2024-05-22 | Akuma Release. Balance changes for all characters. | `202405` | 377 bullet lines |
| `1.04` | 2024-02-27 | Ed Release. Several balance changes and bug fixes. | `20240227` | 99 bullet lines |
| `1.03` | 2023-12-01 | Costume 3 release. Minor bug fixes. | `20231201` | 76 bullet lines |
| `1.02` | 2023-09-27 | A.K.I. Release. Bug fixes with some minor changes due to bugs. | `20230927` | 313 bullet lines |
| `1.01` | 2023-07-24 | Rashid Release. Bug fixes with some minor balance changes mainly for Modern controls. | `20230724` | 64 bullet lines |
| `1.00` | 2023-06-02 | Launch version. | none | 1 bullet line |

## 公式 Battle Change との対応

SuperCombo Patch Notes table の external link から、16 rows は Capcom 公式 Battle Change List の version id に対応する。`1.00` は launch version で、公式 `battle_change` link ではなく `https://streetfighter.com/6` へリンクしているため、公式 Battle Change row との 1:1 対応は持たない。

公式側の `20251113`、`20251022`、`20250901`、`20230808` は、SuperCombo Patch Notes table から直接リンクされていない。したがって、この wiki では「明示リンクがある row は 1:1 対応として扱うが、SuperCombo version と公式 update version が常に全件 1:1 になるとは仮定しない」方針にする。根拠は `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`。

## 関連概念

- [[concepts/frame-data]]

## 関連エンティティ

- [[entities/street-fighter-6]]
- [[entities/supercombo-wiki]]

## 既存 wiki との矛盾または更新

- [[sources/capcom-official-battle-change-list]] は公式 source、こちらは SuperCombo community source として分ける。公式と community の説明が重なる場合は公式 source を優先する。
- version detail page の top-level bullet は `change-events.json` と `move-change-index.json` に community event index として派生済み。ただし character page / concept page へ個別変更を統合する作業は未実施。回答時は source page と derived JSON から raw detail に戻る。
- Patch Notes 本体の wikitext は Cargo query であり、17 version row の実体は rendered table / derived output / detail pages にある。
- `fighter_key` は SuperCombo source-local key、`character_slug` は repo 内 frame-data join key として分ける。Vega / M. Bison などの地域名差分があるため、`fighter_key` を直接 frame-data path として扱わない。

## 未解決の質問

- SuperCombo detail page の community events を、version 別 synthesis、character 別 synthesis、または official Battle Change の補助列としてどの粒度で昇格するか。
- SuperCombo の community terminology と Capcom 公式 change text が異なる場合、差分を review note にする基準をどうするか。
- official Battle Change にはあるが SuperCombo Patch Notes table からリンクされていない 4 update を、SuperCombo version timeline の gap として扱うか、公式 hotfix-only update として分けるか。

## ソースメモ

- Raw manifest: `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json`
- Batch capture list: `raw/web-pages/wiki.supercombo.gg/patch-notes/version-captures.json`
- Batch validation: `raw/web-pages/wiki.supercombo.gg/patch-notes/validation.batch.json`
- Version raw captures: `raw/web-pages/wiki.supercombo.gg/patch-notes/versions/<version-slug>/`
- Derived versions JSON: `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`
- Official crosswalk JSON: `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`
- Community change events JSON: `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json`
- Community move change index JSON: `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json`
- Derived schema: `wiki/outputs/data/battle-change/supercombo-patch-notes/schema.json`
- Regeneration tool: `tools/battle_change/supercombo/extract.py`
- Capture review: [[reviews/2026-06-11-supercombo-patch-notes-web-page-capture-review]]
