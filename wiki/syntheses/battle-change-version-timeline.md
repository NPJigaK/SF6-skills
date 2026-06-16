---
type: synthesis
title: "Battle Change / SuperCombo Patch Notes version timeline"
status: review-needed
created: 2026-06-16
updated: 2026-06-16
confidence: medium
sources:
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
related:
  - "[[reviews/2026-06-16-battle-change-version-timeline-refactor-plan]]"
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Battle Change version timeline"
  - "SF6 patch version timeline"
  - "Battle Change / Patch Notes timeline"
tags:
  - sf6
  - battle-change
  - patch-notes
  - version-timeline
  - synthesis
---

# Battle Change / SuperCombo Patch Notes version timeline

## Overview

この synthesis は、Capcom 公式 Battle Change List と SuperCombo Patch Notes を、patch / version query の入口として同時に読むための authority model と timeline をまとめる。Capcom 公式 Battle Change List は公式 update text と raw capture の source、SuperCombo Patch Notes は community detail / terminology / combo context の source として扱う。両者は対応関係を持つが、source authority は同格ではない。

現在の根拠は [[sources/capcom-official-battle-change-list]]、[[sources/supercombo-street-fighter-6-patch-notes]]、`wiki/outputs/data/battle-change/official/`、`wiki/outputs/data/battle-change/supercombo-patch-notes/`、および [[reviews/2026-06-16-battle-change-version-timeline-refactor-plan]]。この draft は未解決の human-review items を残すため、`status: review-needed`、`confidence: medium` とする。

## Read order quick reference

- Current frame value / move property を知りたい時は、Battle Change / Patch Notes ではなく [[concepts/frame-data]] と `wiki/outputs/data/frame-data/official/<data-slug>/` を入口にする。
- Historical update explanation を知りたい時は、この synthesis の version timeline から対象 version を見つけ、[[sources/capcom-official-battle-change-list]]、`wiki/outputs/data/battle-change/official/versions.json`、`changes.json` へ戻る。
- SuperCombo Patch Notes は community detail、terminology、combo / juggle / blockstring context の補助として使い、official fact の代替にしない。
- Version 対応や coverage を確認する時は `official-battle-change-crosswalk.json` を使い、16 matched / 1 launch / 4 official-only を分けて扱う。
- Freshness 確認では source updated time、raw captured time、derived output generation / validation を混同しない。
- 未解決の official-only 4 update、launch row、SuperCombo detail 昇格粒度は、この synthesis では review-needed として扱う。

## Authority model

| Evidence class | Use for | Do not use for | Evidence |
|---|---|---|---|
| Capcom official Battle Change source | 公式 update text、公式 version id、公式 raw capture へ戻る根拠 | SuperCombo detail の代替、community explanation の裏取りなし昇格 | [[sources/capcom-official-battle-change-list]]; `raw/battle-change/official/manifest.json`; `wiki/outputs/data/battle-change/official/versions.json` |
| SuperCombo Patch Notes source | community detail、terminology、combo / juggle / blockstring への影響説明、version detail page の探索 | Capcom 公式 change text の上書き、公式 source fact への昇格 | [[sources/supercombo-street-fighter-6-patch-notes]]; `raw/web-pages/wiki.supercombo.gg/patch-notes/manifest.json`; `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json` |
| derived versions / crosswalk | version 対応、row count、launch row、official-only update の確認 | 公式本文の代替、source にない因果説明 | `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json` |
| derived change-event / move index | combo / frame-data query の原因候補検索、character_slug join の入口 | current frame value の正本、非数値変更の数値計算 | `wiki/outputs/data/battle-change/official/change-events.json`; `wiki/outputs/data/battle-change/*/move-change-index.json` |
| frame-data outputs | 現在値 query、Classic / Modern per-move values | historical patch reason の単独説明 | [[concepts/frame-data]]; `wiki/outputs/data/frame-data/official/` |
| review notes | capture validation、未解決項目、人間レビュー待ちの注意 | source fact の置き換え | [[reviews/2026-06-07-official-battle-change-capture-review]]; [[reviews/2026-06-11-supercombo-patch-notes-web-page-capture-review]]; [[reviews/2026-06-16-battle-change-version-timeline-refactor-plan]] |

current frame value query では、現在の技値は frame-data output を優先する。Battle Change / Patch Notes は historical explanation source として使い、過去 update の原因候補や変更理由を探す入口にする。これは [[concepts/frame-data]] の「現在値は frame-data output、変更説明は Battle Change / Patch Notes」という方針に従う。

## Version timeline

この表は SuperCombo Patch Notes の version row を軸にし、明示 link がある場合だけ official Battle Change id を併記する。`authority` はその行の summary がどの source class に属するかを示す。SuperCombo summary は community summary であり、Capcom 公式本文ではない。根拠は `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json` と `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`。

| Date | SuperCombo version | Official Battle Change id | Authority | Summary / handling |
|---|---|---|---|---|
| 2026-05-28 | `2.0301` | `20260528` | matched official + community | SuperCombo summary: Ingrid release, minor system changes and bug fixes. |
| 2026-04-15 | `2.0202` | `20260415` | matched official + community | SuperCombo summary: game system, JP, and M. Bison bug fixes. |
| 2026-03-17 | `2.02` | `20260317` | matched official + community | SuperCombo summary: Alex release and all-character balance changes. |
| 2025-12-16 | `2.0111` | `20251216` | matched official + community | SuperCombo summary: bug fixes and minor adjustments, primarily Elena, Mai, and Sagat. |
| 2025-10-15 | `2.01` | `20251015` | matched official + community | SuperCombo summary: C. Viper release, minor bug fixes and adjustments. |
| 2025-08-05 | `2.00` | `20250805` | matched official + community | SuperCombo summary: Sagat release, minor bug fixes and adjustments. |
| 2025-06-03 | `1.10` | `202506` | matched official + community | SuperCombo summary: Elena release and all-character balance changes. |
| 2025-02-05 | `1.09` | `20250205` | matched official + community | SuperCombo summary: Mai release and minor bug fixes. |
| 2024-12-02 | `1.08` | `20241202` | matched official + community | SuperCombo summary: minor balance changes for all characters. |
| 2024-09-24 | `1.07` | `20240924` | matched official + community | SuperCombo summary: Terry release, minor balance changes and bug fixes. |
| 2024-06-26 | `1.06` | `20240626` | matched official + community | SuperCombo summary: M. Bison release, minor balance changes and bug fixes. |
| 2024-05-22 | `1.05` | `202405` | matched official + community | SuperCombo summary: Akuma release and all-character balance changes. |
| 2024-02-27 | `1.04` | `20240227` | matched official + community | SuperCombo summary: Ed release, balance changes and bug fixes. |
| 2023-12-01 | `1.03` | `20231201` | matched official + community | SuperCombo summary: Costume 3 release and minor bug fixes. |
| 2023-09-27 | `1.02` | `20230927` | matched official + community | SuperCombo summary: A.K.I. release and bug fixes with minor bug-related changes. |
| 2023-07-24 | `1.01` | `20230724` | matched official + community | SuperCombo summary: Rashid release and minor balance changes mainly for Modern controls. |
| 2023-06-02 | `1.00` | none | community launch row | Launch version. This row has no official Battle Change 1:1 row. |

公式 Battle Change 側だけにある update は、この draft では unresolved review item として保持する。SuperCombo Patch Notes table から直接 link されていない理由は推測しない。根拠は `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json` の `.official_unmatched_ids` と `wiki/outputs/data/battle-change/official/versions.json`。

| Official Battle Change id | Official title | Official row counts | Handling |
|---|---|---|---|
| `20251113` | `2025.11.13 update` | common 2 / fighter 2 | official-only update; unresolved. |
| `20251022` | `2025.10.22 update` | common 1 / fighter 4 | official-only update; unresolved. |
| `20250901` | `2025.09.01 update` | common 0 / fighter 5 | official-only update; unresolved. |
| `20230808` | `2023.08.08 update` | common 1 / fighter 5 | official-only update; unresolved. |

## Official vs SuperCombo mapping

`jq` で確認した derived counts は次の通り。

| Item | Count / Value | Evidence |
|---|---:|---|
| official versions | 20 | `wiki/outputs/data/battle-change/official/versions.json`; `.row_count` |
| official change events | 1820 | `wiki/outputs/data/battle-change/official/change-events.json`; `.row_count` |
| official move-index rows | 1419 | `wiki/outputs/data/battle-change/official/move-change-index.json`; `.row_count` |
| SuperCombo versions | 17 | `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`; `.row_count` |
| SuperCombo change events | 1374 | `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json`; `.row_count` |
| SuperCombo move-index rows | 1118 | `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json`; `.row_count` |
| matched versions | 16 | `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`; `.summary.matched_count` |
| launch row | 1 | `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json`; row `version == "1.00"` |
| official-only updates | 4 | `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json`; `.official_unmatched_ids` |

mapping rule:

- 明示 link がある SuperCombo Patch Notes row は、Capcom official Battle Change id との 1:1 対応として扱ってよい。
- `1.00` は SuperCombo launch row として扱う。official Battle Change row との 1:1 対応は持たない。
- official-only 4 update は、SuperCombo table から直接 link されていない official update として保持する。SuperCombo 側にない理由や意図は推測しない。
- SuperCombo detail は community detail / terminology / background として使い、official source の代替にしない。

## Freshness rules

Capcom official Battle Change の source freshness / capture は [[sources/capcom-official-battle-change-list]] と `raw/battle-change/official/manifest.json` を入口に確認する。source page は capture 対象を 2023-07-24 update から 2026-05-28 update までの 20 version とし、最新 `current_version` を `20260528` としている。raw capture の時刻は source page の `captured_at_utc: "2026-06-06T15:22:50Z"` を参照する。

SuperCombo Patch Notes は root page と detail pages の freshness を分ける。[[sources/supercombo-street-fighter-6-patch-notes]] は root page の `source_updated_at` を `2023-09-27T14:23:05Z`、detail pages の最新 freshness を `latest_detail_source_updated_at: 2026-06-02T03:12:40Z`、raw capture time を `captured_at_utc: 2026-06-11T03:22:47Z` としている。

query では、source が更新された時刻、raw を取得した時刻、derived output を生成した時刻を混同しない。derived output の件数や crosswalk は便利な入口だが、source text の freshness を判断する時は source page、raw manifest、validation に戻る。

## Derived outputs and their limits

| Output | Use | Limit |
|---|---|---|
| `wiki/outputs/data/battle-change/official/versions.json` | official 20 version の id、title、row counts を確認する | official text の読者向け要約ではない |
| `wiki/outputs/data/battle-change/official/changes.json` | official change rows と `text_html` へ戻る | `text_html` をそのまま reader-facing Markdown として扱わない |
| `wiki/outputs/data/battle-change/official/change-events.json` | official change rows の検索補助、明示 before/after、change type candidate | 非数値 bugfix / hitbox / behavior を数値計算に使わない |
| `wiki/outputs/data/battle-change/official/move-change-index.json` | character / move から official update 候補を探す | current move value の正本ではない |
| `wiki/outputs/data/battle-change/supercombo-patch-notes/versions.json` | SuperCombo 17 version rows、launch row、detail page metadata を確認する | official Battle Change の完全な version list ではない |
| `wiki/outputs/data/battle-change/supercombo-patch-notes/official-battle-change-crosswalk.json` | 16 matched / 1 launch / 4 official-only の対応を確認する | official-only の理由を説明しない |
| `wiki/outputs/data/battle-change/supercombo-patch-notes/change-events.json` | community detail、nested explanation、combo / juggle / blockstring context の検索 | official source fact に昇格しない |
| `wiki/outputs/data/battle-change/supercombo-patch-notes/move-change-index.json` | community target index から affected move / character を探す | current frame-data value や公式 update text の代替ではない |

## Query recipes

### Current value query

1. `wiki/index.md` から [[concepts/frame-data]] または character source / output へ入る。
2. 現在の per-move value は `wiki/outputs/data/frame-data/official/<data-slug>/` を優先する。
3. SuperCombo enriched output は公式列を上書きせず、補助列または review-needed 補助情報として読む。
4. Battle Change / Patch Notes は「その値が過去にどう変わったか」「なぜ現在値になった可能性があるか」を調べる historical explanation source として読む。

### Historical update explanation query

1. まずこの synthesis で official / community / derived authority を確認する。
2. 対象 version がある場合は [[sources/capcom-official-battle-change-list]] と `wiki/outputs/data/battle-change/official/versions.json` で official id を確認する。
3. 公式本文の根拠は official raw / `changes.json` / source page に戻す。
4. 補足背景や combo / juggle / blockstring への影響は [[sources/supercombo-street-fighter-6-patch-notes]] と SuperCombo `change-events.json` / `move-change-index.json` で探す。
5. 回答では official fact と community detail を同じ文で混ぜず、authority を明示する。

### Combo / frame-data change cause search

1. character / move 名がある場合は official `move-change-index.json` と SuperCombo `move-change-index.json` を検索入口にする。
2. official output に candidate があれば、公式 source text と現在 frame-data output を照合する。
3. SuperCombo output の candidate は community background として扱う。official source にない combo result や intent は断定しない。
4. route / damage / juggle の計算 claim は、この synthesis だけでは確定しない。必要なら source-backed ledger / accepted review fixture へ戻る。

### Freshness or coverage query

1. official Battle Change の coverage は official source page と `raw/battle-change/official/manifest.json` で確認する。
2. SuperCombo Patch Notes の root freshness と detail freshness は分けて確認する。
3. derived output の row count は `jq` で確認する。
4. stale / incomplete / recapture-needed に見える場合は、raw をこの query で直接更新せず、review note または capture/update workflow に回す。

## Open questions / human review needed

- official-only 4 update (`20230808`, `20250901`, `20251022`, `20251113`) を timeline でどう見せるか。現時点では SuperCombo Patch Notes table に直接 link がない official update として保持し、SuperCombo 側にない理由は推測しない。
- launch row `1.00` を timeline のどの位置に置くか。現時点では SuperCombo launch row として保持し、official Battle Change row との 1:1 対応は持たないと明記する。
- SuperCombo detail をどの粒度で synthesis / character page / term page へ昇格するか。全 event の複製は避け、query demand がある version / character / move から昇格する候補。
- community detail と official source text が異なる場合、どの差分を review note にするか。
- derived output の freshness 確認と再生成のタイミング。今回の synthesis は raw update / derived regeneration を行っていない。
- official `text_html` を reader-facing Markdown / plain text に変換する標準手順をどこで固定するか。

## Not source facts / do not infer

- official-only 4 update が SuperCombo にない理由を推測しない。
- SuperCombo launch row `1.00` を official Battle Change row として扱わない。
- SuperCombo community detail を Capcom official fact として書かない。
- derived `change_types`、`value_changes`、move index match を、source text にない確定理由や現在値として扱わない。
- Battle Change / Patch Notes から current frame value を直接答えない。current value は frame-data output と source pageを優先する。
- source page、raw、derived output、accepted review にない patch fact、frame value、validation status を追加しない。
