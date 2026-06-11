---
type: concept
concept_type: term
title: "生ラッシュ"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "raw Drive Rush"
  - "raw drive rush"
  - "なまらっしゅ"
tags:
  - sf6
  - terms
  - drive-system
---

# 生ラッシュ

## 要約

生ラッシュは、Drive Parry の構えから出す Drive Rush。Capcom eSports BASE は、通常技 cancel から出す cancel rush と分け、Drive Gauge cost の差を説明している。SuperCombo Gauges page は Parry からの Drive Rush の startup / travel / total frames と distance を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-06` | Drive Rush は cancel rush と raw Drive Rush の 2 種類。通常技 cancel 版は D gauge 3、Drive Parry から出す生ラッシュは D gauge 1 を使う。Drive Rush 中は通常技性能も上がる。 | high |
| [[sources/capcom-official-fightingground-battle-system]] | Drive Rush は Drive Parry の構え、または cancel 可能な通常技から出せる。Drive Parry からは cost 1、通常技からは cost 3。 | high |
| [[sources/supercombo-street-fighter-6-gauges]] | Parry からの Drive Rush は `3+8` startup、first actionable `15`、recovery `22`、total `37` とし、10f screen freeze、通常技 +4 advantage、30 characters 分の distance table を示す。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Official / eSports BASE cost | `1` Drive gauge | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]] |
| SuperCombo cost ambiguity | cost table `0.5` vs section / caption `1.0`; JSON は `cost_bars: null` | [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs[action=Drive Rush from Parry]` |
| Frame data | startup `3+8`, attack-cancelable recovery `15`, fully-cancelable recovery `22`, total recovery `37` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_frame_data[type=Parry~DR]` |
| Successful Parry route | held successful Parry 後は `1+8` まで短くなると説明 | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]] |
| Screen freeze / advantage | screen freeze `10f`; Drive Rush 中の normal / command normal は `+4` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values` |
| Minimum Drive threshold | raw Drive Rush は `1/2` Drive bar 未満では出せない | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values.raw_drive_rush_minimum_drive_bars` |
| Distance table | 30 characters 分。term には全行を複製しない | [[sources/supercombo-street-fighter-6-gauges#Drive Rush distance table]]; `drive_rush_distance_by_character` |

## 意味差分

- 現時点では Capcom 公式 source 同士で大きな意味差分はない。
- SuperCombo Gauges page は raw Drive Rush が 1/2 bar 未満では出せないとも説明する。cost / threshold は公式 source または実機検証で照合する。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/frame-advantage]]
- [[concepts/terms/shikomi]]
