---
type: concept
concept_type: term
title: "クリティカルアーツ"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/capcom-official-zangief-frame-data]]"
  - "[[sources/supercombo-zangief-frame-data]]"
  - "[[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/terms/super-art]]"
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Critical Art"
  - "CA"
  - "クリティカルアーツ"
  - "CA variant"
tags:
  - sf6
  - terms
  - frame-data
---

# クリティカルアーツ

## 要約

クリティカルアーツは、体力条件付きで強化され、公式 frame-data 上で `CA` として Super Art とは別 row / variant になることがある arts。SuperCombo Gauges page は health 25% 未満を CA 条件として説明し、現時点のこの wiki では Zangief の `SA3 ボリショイストームバスター` と `CA ボリショイストームバスター` の分離も明示的な根拠になっている。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-gauges]] | Health が 25% 未満になると Level 3 Super は Critical Art へ変化すると説明する。 | medium |
| [[sources/capcom-official-zangief-frame-data]] | Zangief 公式 frame-data は `SA3 ボリショイストームバスター` と、体力25%以下条件の `CA ボリショイストームバスター` を別 row として保持している。 | high |
| [[sources/supercombo-zangief-frame-data]] | Zangief の 720 input には SA3 / CA variant があり、公式 Classic との照合では `move_id` で分けて扱う。 | medium |
| [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] | `SA3 ボリショイストームバスター` と `CA ボリショイストームバスター` は separate variant として human review accepted。 | high |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Critical Art health threshold | health `25%` 未満 | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.critical_art_health_threshold_percent` |
| CA による Drive Gauge depletion | `2` Drive bars | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge.super_art_drive_gauge_depletion_bars.CA` |
| Zangief CA variant handling | SA3 / CA は別 row / separate variant | [[sources/capcom-official-zangief-frame-data]], [[outputs/reports/2026-06-02-zangief-official-supercombo-enriched-data]] |

## 意味差分

- この page は、現時点では `CA` の一般公式定義よりも、frame-data / crosswalk 上の variant handling を主に説明する。SuperCombo Gauges page は一般条件の community source として補う。
- 全 character の Critical Art 条件と Super Art との差分を一般化するには、公式 manual / frame-data の横断確認が必要。

## 関連

- [[concepts/terms/super-art]]
- [[concepts/frame-data]]
