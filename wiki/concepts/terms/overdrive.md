---
type: concept
concept_type: term
title: "オーバードライブ"
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
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/burnout]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Overdrive"
  - "OD"
  - "OD技"
  - "オーバードライブ技"
tags:
  - sf6
  - terms
  - drive-system
---

# オーバードライブ

## 要約

オーバードライブは、必殺技の発動ボタンを複数同時押しして出す強化版の必殺技。Capcom 公式 Fighting Ground source は、過去シリーズの EX 技と同等の action と説明している。SuperCombo Gauges page は OD cost と Burnout interaction を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-fightingground-battle-system]] | 必殺技の発動ボタンを2つ同時押しすることで、強化された必殺技を出せる。過去シリーズの EX 技と同等の action。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | Special move 実行時に同種 button を2つ以上押すことで Overdrive Art になり、過去作の EX Special Moves と同じ攻撃だと説明している。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | OD Special は 2 Drive bars を使う。2 bars 未満で OD を使用すると即座に Burnout になると説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Cost | `2` Drive bars | [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs[action=Overdrive Specials]`, `overdrive_values.cost_bars` |
| Input | special move input 中に `2` Punches or `2` Kicks | [[sources/supercombo-street-fighter-6-gauges#Overdrive]]; `overdrive_values.input` |
| Burnout edge case | `2` bars 未満で OD を使うと即 Burnout | [[sources/supercombo-street-fighter-6-gauges#Overdrive]]; `overdrive_values.burnout_if_used_under_bars` |
| Super cancel note | Super-cancelable OD は Level `2` Super Art へ cancel 可能 | [[sources/supercombo-street-fighter-6-gauges#Overdrive]]; `overdrive_values.super_cancelable_od_can_cancel_to_level` |
| Drive regeneration cooldown | `120f` | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration cooldown]]; `drive_regeneration_cooldowns` |

## 意味差分

- 公式 source は「オーバードライブ」、SuperCombo source は `Overdrive Art` と表現する。
- 個別 OD 技の性能差や Burnout 中の制限は、各 character の frame-data / Battle Change source を確認する。
- SuperCombo Gauges page は、Super-cancel 可能な OD Specials は Level 2 Super へ cancel 可能とも説明する。個別可否は character frame-data で確認する。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/burnout]]
