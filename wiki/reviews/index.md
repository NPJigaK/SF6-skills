---
type: review
review_type: review_dashboard
status: active
created: 2026-06-16
updated: 2026-06-16
confidence: medium
tags:
  - sf6
  - review
  - dashboard
  - maintenance
---

# Review Dashboard

## Purpose

この page は `wiki/reviews/` の navigation dashboard である。review pages の source of truth ではなく、open / active / accepted review、refactor_plan、capture_validation、calculation_model_gap などを追跡するための薄い入口として扱う。

件数は 2026-06-16 の dashboard 作成直前時点の backlog snapshot。`wiki/reviews/index.md` 自身は除外している。review page の追加、status 変更、frontmatter 整理が入ると変わるため、この page の count を正本として扱わない。

| Snapshot item | Count |
|---|---:|
| Backlog review pages excluding this dashboard | 29 |
| `open` | 22 |
| `active` | 3 |
| `accepted` | 4 |
| `capture_validation` | 21 |
| `calculation_model_gap` | 3 |
| `refactor_plan` | 1 |

## How to use

- open / active items を優先して見る。
- P1/P2、source authority、calculation model、derived output の境界に関わる review を先に見る。
- capture_validation は source family ごとにまとめて見る。
- status 変更は個別 review page の本文と frontmatter で行う。
- dashboard は full review content を複製しない。

## Open high-risk / human-review items

| Review | Type | Status | Severity | Family / Topic | Unresolved item | Linked output/synthesis | Next action |
|---|---|---|---|---|---|---|---|
| [[reviews/2026-06-11-jp-year1-od-amnesia-combo-damage-calculation-model-gap]] | calculation_model_gap | open | P1 | combo damage / JP | delayed hits、patch rollback、Punish Counter、SA minimum scaling を含む ledger 手順と外部動画 raw policy。 | [[outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation]] | damage scaling source と外部動画の durable validation 方針を確認する。 |
| [[reviews/2026-06-16-battle-change-version-timeline-refactor-plan]] | refactor_plan | open | P2 | battle-change / patch-notes | official-only 4 update、launch row、SuperCombo detail 昇格粒度、freshness / `text_html` handling。 | [[syntheses/battle-change-version-timeline]] | synthesis の human-review items を確認し、official / community authority を混同しない。 |
| [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]] | capture_validation | open | none | SuperCombo frame-data | `enriched_review_required` 1295 行、SuperCombo-only 620 行、imageinfo missing 599 件。 | [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | queue / character のどちらを優先して review するか決める。 |
| [[reviews/2026-06-06-supercombo-field-conflict-queue-prereview]] | prereview | open | none | SuperCombo frame-data enrichment | Jamie 酔いLv damage、Terry jMP / jMK 入れ替わり疑い、Guile / Juri / Ken の差分。 | [[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]] | 条件付き値、source conflict、version 差を分ける。 |
| [[reviews/2026-05-27-health-check]] | health_check | open | none | early frame-data / glossary | 2026-05-27 に accepted された判断を保持しつつ、follow-up design work が残るため open。 | none | status と残タスクの意味を後続 health check で再確認する。 |

## Refactor plans

| Plan | Status | Target synthesis/output | Main unresolved items | Next action |
|---|---|---|---|---|
| [[reviews/2026-06-16-battle-change-version-timeline-refactor-plan]] | open | [[syntheses/battle-change-version-timeline]] | official-only 4 update、launch row、SuperCombo detail 昇格粒度、freshness / derived output 境界。 | synthesis を query で使い、human-review items を残したまま小さく改善する。 |

## Capture validation queue

| Source family | Review pages | Status summary | Notes |
|---|---|---|---|
| Official frame-data | [[reviews/2026-05-26-official-jp-frame-data-capture-review]]; [[reviews/2026-05-27-official-ryu-frame-data-capture-review]]; [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]]; [[reviews/2026-05-27-official-zangief-frame-data-capture-review]]; [[reviews/2026-05-30-official-frame-data-roster-capture-review]] | accepted 4 / open 1 | Initial 4 character captures are accepted; 2026-05-30 roster batch remains open. |
| SuperCombo frame-data | [[reviews/2026-05-31-supercombo-jp-frame-data-capture-review]]; [[reviews/2026-05-31-supercombo-ryu-frame-data-capture-review]]; [[reviews/2026-06-02-supercombo-zangief-frame-data-capture-review]]; [[reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review]]; [[reviews/2026-06-05-supercombo-all-frame-data-capture-review]] | open 5 | Batch capture passed, but enriched review queue and SuperCombo-only rows remain human-review work. |
| Battle Change / Patch Notes | [[reviews/2026-06-07-official-battle-change-capture-review]]; [[reviews/2026-06-11-supercombo-patch-notes-web-page-capture-review]] | open 2 | Official Battle Change and SuperCombo Patch Notes both passed automatic validation; authority and crosswalk handling remain review topics. |
| Capcom scoped web pages | [[reviews/2026-06-10-capcom-fightingground-battle-system-capture-review]]; [[reviews/2026-06-10-capcom-esports-base-terms-capture-review]] | open 2 | Scoped official captures for Battle System and terms. Do not treat scoped capture as full-page mirror. |
| SuperCombo system web pages | [[reviews/2026-06-09-supercombo-glossary-web-page-capture-review]]; [[reviews/2026-06-11-supercombo-controls-web-page-capture-review]]; [[reviews/2026-06-11-supercombo-hud-web-page-capture-review]]; [[reviews/2026-06-11-supercombo-gauges-web-page-capture-review]]; [[reviews/2026-06-11-supercombo-offense-web-page-capture-review]]; [[reviews/2026-06-11-supercombo-defense-web-page-capture-review]]; [[reviews/2026-06-11-supercombo-game-data-web-page-capture-review]] | open 7 | Community source family. Numeric or system claims should keep official / community / derived authority visible. |

## Active investigations

| Review | Type | Topic | Current purpose | Next action |
|---|---|---|---|---|
| [[reviews/2026-06-15-jp-combo-damage-ledger-regression]] | calculation_model_gap | JP combo damage ledger | Starter scaling、mid-combo Drive Rush penalty、SA2 delayed-hit route を regression fixture として保持する。 | 外部動画 raw policy と ledger promotion policy を確認する。 |
| [[reviews/2026-06-15-mai-combo-damage-ledger-regression]] | calculation_model_gap | Mai combo damage ledger | `214HP (No Flame)` の character-specific scaling、Counter / Punish Counter、SA3 minimum を fixture 化する。 | route parser へ昇格せず、source-backed ledger 前提を維持する。 |
| [[reviews/2026-06-15-pdr-cost-component-video-observation]] | mechanics_evidence_review | Drive Rush from Parry cost component | Drive Parry activation `0.5` + transition `0.5` と、Burnout / hold drain の未解決点を分ける。 | frame 4 hold drain と input history からの分類可能性を追加検証する。 |

## Accepted / resolved archive

| Review | Type | Accepted meaning |
|---|---|---|
| [[reviews/2026-05-26-official-jp-frame-data-capture-review]] | capture_validation | JP official frame-data capture accepted. |
| [[reviews/2026-05-27-official-ryu-frame-data-capture-review]] | capture_validation | Ryu official frame-data capture accepted. |
| [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]] | capture_validation | Chun-Li official frame-data capture accepted. |
| [[reviews/2026-05-27-official-zangief-frame-data-capture-review]] | capture_validation | Zangief official frame-data capture accepted. |

## Frontmatter hygiene queue

2026-06-16 pass:

- [[reviews/2026-06-15-pdr-cost-component-video-observation]] は `sources:` から concept link を外し、`related:` に concept / navigation link を残す形に整理済み。review status、source authority、本文 claim は変更していない。
- [[reviews/2026-06-15-jp-combo-damage-ledger-regression]] は `sources:` から [[concepts/terms/damage-scaling]] / [[concepts/terms/punish-counter]] を外し、`related:` 側に保持する形に整理済み。fixture authority、damage total、route interpretation、本文 claim は変更していない。
- [[reviews/2026-06-15-mai-combo-damage-ledger-regression]] は `sources:` から [[concepts/terms/damage-scaling]] / [[concepts/terms/counter-hit]] / [[concepts/terms/punish-counter]] を外し、`related:` 側に保持する形に整理済み。fixture authority、damage total、route interpretation、本文 claim は変更していない。
- Review Frontmatter Hygiene rule は PDR / JP / Mai の 3 例を根拠に、2026-06-16 に `$sf6-wiki-refactor` へ追加済み。

現時点でこの dashboard に残す具体的な frontmatter hygiene candidate はない。

## Dashboard update policy

- Review page 追加時にこの dashboard を更新する。
- Review status 変更時にこの dashboard を更新する。
- Dashboard は full review content を複製しない。
- Source facts、derived facts、validation details は個別 review page に残す。
- Dashboard の大きな更新は必要に応じて `wiki/log.md` に追記する。
- Stale が気になる場合は `$sf6-wiki-health-check` で scope-limited freshness check を行う。

## Next maintenance candidates

1. [[syntheses/battle-change-version-timeline]] の human-review items を確認する。
2. Review Frontmatter Hygiene rule の適用状況は、次回 dashboard freshness check で確認する。
3. `wiki/index.md` の Reviews section を将来 `[[reviews/index]]` へ寄せる hub 化 plan を作る。
