---
type: concept
concept_type: term
title: "スーパーアーツ"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/critical-art]]"
  - "[[concepts/terms/cancel]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Super Art"
  - "SA"
  - "SA1"
  - "SA2"
  - "SA3"
  - "スーパーアーツ"
tags:
  - sf6
  - terms
  - frame-data
---

# スーパーアーツ

## 要約

スーパーアーツは、Super Art gauge を消費して使用する強力な技。Capcom 公式 Fighting Ground source は、技を hit させると gauge が増え、最大3 stock まで溜められ、未使用分は次 round に持ち越せると説明している。SuperCombo Gauges page は build / depletion / timer-freeze の community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-fightingground-battle-system]] | Super Art gauge を消費して強力な Super Arts を使用できる。技を hit させると gauge が増え、最大3 stock まで溜められ、次 round に持ち越せる。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | Cancel field の `SA` は Super Art を指し、数字がある場合は特定 level の Super を指す。`SA3` は Lv.3 Super Art。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Super Gauge は round start で空、最大 3 bars、round 間で持ち越し。CA は health 25% 未満で使用可能。SA depletion は level 1 / 2 / 3 / CA で 0.5 / 1 / 1.5 / 2 bars と説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Match start | Super Gauge starts empty | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.match_start_empty` |
| Max stock | `3` bars | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.max_bars` |
| Round carryover | unused Super meter carries over | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.round_carryover` |
| Critical Art threshold | health `25%` 未満 | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.critical_art_health_threshold_percent` |
| Super Art timer | Super Art 中は round timer freeze | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.timer_frozen_during_super_art` |
| Attacker build on block | base の `50%` | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.build_rules` |
| Defender build | hit `70%`, block `25%`, armor absorb `35%` | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.build_rules` |
| Super Art Drive Gauge depletion | SA1 `0.5`, SA2 `1`, SA3 `1.5`, CA `2` bars | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.super_art_drive_gauge_depletion_bars` |

## 意味差分

- 公式 source は gauge と使用条件、SuperCombo source は frame-data / cancel 表記上の `SA` を説明する。
- `SA3` と [[concepts/terms/critical-art|Critical Art]] の variant は、個別 character data で分けて確認する。
- SuperCombo Gauges page は timer freeze 中の Super Gauge build 停止と、attacker / defender の build formulas も表で示す。community numeric source なので、公式・実機検証がある場合はそちらを優先する。

## 関連

- [[concepts/terms/critical-art]]
- [[concepts/terms/cancel]]
- [[concepts/frame-data]]
