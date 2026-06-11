---
type: concept
concept_type: term
title: "削り"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "chip damage"
  - "chip K.O."
  - "けずり"
tags:
  - sf6
  - terms
  - drive-system
---

# 削り

## 要約

削りは、guard 時の Drive Gauge 減少と、Burnout 中の特殊な体力削りを説明する用語。通常時は防御側の Drive Gauge が減り、Burnout 中は必殺技を guard した時に体力が削られ、K.O. にもつながる。SuperCombo Gauges page は Burnout chip damage の目安値を補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-00` | Guard すると Drive Gauge が少しずつ減り、Burnout 中に必殺技を guard すると体力が削られる。Burnout 中は削り K.O. も可能。 | high |
| [[sources/supercombo-street-fighter-6-gauges]] | 通常時の guard では防御側 Drive Gauge が減り、Burnout 中の chip damage は special / Super の通常 damage の約 25% と説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| 通常時の guard drain 目安 | 弱い攻撃は約 `5%` Drive bar、攻撃によっては `1` bar | [[sources/supercombo-street-fighter-6-gauges#Drive Gauge overview]] |
| Burnout chip damage | special / Super の通常 damage の約 `25%` | [[sources/supercombo-street-fighter-6-gauges#Burnout]]; `burnout_values.chip_damage_percent_of_normal_damage` |
| Burnout stun condition | corner Drive Impact wall splat は hit / block どちらでも stun | [[sources/supercombo-street-fighter-6-gauges#Burnout]] |

## 意味差分

- Capcom eSports BASE は公式の観戦用語説明、SuperCombo Gauges page は community numeric source。chip damage の exact formula は公式 source または実機検証があればそちらを優先する。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/stun]]
- [[concepts/terms/lethal]]
