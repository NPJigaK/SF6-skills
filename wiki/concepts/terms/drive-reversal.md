---
type: concept
concept_type: term
title: "ドライブリバーサル"
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
  - "[[concepts/terms/invincible-move]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Drive Reversal"
  - "ドライブリバーサル"
tags:
  - sf6
  - terms
  - drive-system
---

# ドライブリバーサル

## 要約

ドライブリバーサルは、guard 中に自身の硬直を解除して反撃を出す Drive System の防御・切り返し手段。Capcom 公式 Fighting Ground source は、damage は低いが追い込まれた状況を打開できると説明している。SuperCombo Gauges page は cost と frame table を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-fightingground-battle-system]] | Guard 中にボタンを押すことで自身の硬直を解除して反撃を繰り出す。damage は低いが、追い込まれた状況を打開できる。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | Blocking 中に counterattack を出し、pressure されている tight situations から抜ける助けになる。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Cost は 2 Drive bars。Frame data は startup `20(18)`、active `3`、recovery `26(31)*`、hit KD `+23*`、block `-6`、damage `500` とする。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Cost | `2` Drive bars | [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs[action=Drive Reversal]` |
| Frame data | startup `20(18)`, active `3`, recovery `26(31)*`, damage `500` recoverable, on hit KD `+23*`, on block `-6` | [[sources/supercombo-street-fighter-6-gauges#Drive Reversal]]; `drive_reversal_frame_data` |
| Recovery Drive Reversal startup | `18f` | [[sources/supercombo-street-fighter-6-gauges#Drive Reversal]]; `drive_reversal_frame_data.recovery_drive_reversal_startup_frames` |
| Blockstun screen freeze | startup `6` 後に `4f` freeze | [[sources/supercombo-street-fighter-6-gauges#Drive Reversal]]; `drive_reversal_frame_data` |
| Throw interaction | `12f` screen freeze、`1` Drive bar refund | [[sources/supercombo-street-fighter-6-gauges#Drive Reversal]]; `drive_reversal_frame_data` |
| Drive regeneration cooldown | `120f` | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration cooldown]]; `drive_regeneration_cooldowns` |

## 意味差分

- 現時点では公式 source と SuperCombo glossary の大枠は一致している。
- 個別キャラの Drive Reversal 反撃可否や避け方は Battle Change / frame-data source が必要。
- SuperCombo Gauges page は Recovery Drive Reversal の startup を 18f、throw freeze 12f 中の throw interaction では 1 Drive bar が返ると説明する。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/invincible-move]]
