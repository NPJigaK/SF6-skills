---
type: concept
concept_type: term
title: "キャンセルドライブラッシュ"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/raw-drive-rush]]"
  - "[[concepts/terms/cancel]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Drive Rush Cancel"
  - "DRC"
  - "cancel Drive Rush"
  - "キャンセルラッシュ"
tags:
  - sf6
  - terms
  - drive-system
  - frame-data
---

# キャンセルドライブラッシュ

## 要約

キャンセルドライブラッシュは、cancel 可能な通常技などから Drive Rush へ移る行動。公式 Fighting Ground source は、Drive Rush は Drive Parry の構えまたは cancel 可能な通常技から出せ、通常技からの dash は Drive cost 3 と説明している。SuperCombo Gauges page は DRC の frame table、cooldown、mid-combo scaling を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-fightingground-battle-system]] | Drive Rush は Drive Parry の構え、または cancel 可能な通常技から出せる。Drive Parry からは cost 1、通常技からは cost 3。 | high |
| [[sources/capcom-esports-base-terms]] | Drive Rush は cancel rush と raw Drive Rush の 2 種類。通常技 cancel 版は D gauge 3、Drive Parry からの生ラッシュは D gauge 1。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | `Drive Rush Cancel Advantage` は normal / command normal / Target Combo を Drive Rush へ cancel した時の hit / block frame advantage を指し、DRC と略される。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | DRC は cost 3 Drive bars、startup `9`、first actionable `15`、recovery `22`、total `37`、mid-combo one-time 15% damage scaling、Drive regeneration cooldown 120f とする。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Cost | `3` Drive bars | [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs[action=Drive Rush cancel]` |
| Frame data | startup `9`, attack-cancelable recovery `15`, fully-cancelable recovery `22`, total recovery `37` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_frame_data[type=DR Cancel]` |
| Drive Rush screen freeze | `10f` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values.screen_freeze_frames` |
| Normal / command normal bonus | `+4` advantage on hit or block | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values.normal_command_normal_advantage_bonus` |
| Mid-combo scaling | one-time `15%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values.mid_combo_damage_scaling_percent` |
| Drive regeneration cooldown | `120f`; combo 中は Forward Walk 以外の追加 regen を防ぐ | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration cooldown]]; `drive_regeneration_cooldowns` |

## 意味差分

- 公式 source は行動と cost の説明、SuperCombo source は DRC 後の frame advantage 解釈を詳しく扱う。
- Query では、cost / system eligibility は公式 source、DRC advantage / combo timing は SuperCombo 補助 source と公式 frame-data を併用する。
- SuperCombo Gauges page の DRC frame / scaling / cooldown は community numeric source なので、公式・実機検証の値がある場合はそちらを優先する。

## 関連

- [[concepts/terms/raw-drive-rush]]
- [[concepts/terms/cancel]]
- [[concepts/terms/frame-advantage]]
