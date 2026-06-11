---
type: concept
concept_type: term
title: "ドライブパリィ"
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
  - "[[concepts/terms/perfect-parry]]"
  - "[[concepts/terms/raw-drive-rush]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Drive Parry"
  - "パリィ"
  - "ドライブパリィ"
tags:
  - sf6
  - terms
  - drive-system
---

# ドライブパリィ

## 要約

ドライブパリィは、相手の攻撃を自動で guard し、成功時に Drive Gauge を回復する防御手段。タイミングよく受け止めると [[concepts/terms/perfect-parry|ジャストパリィ]] が発生する。SuperCombo Gauges page は Parry の cost、gain、Perfect Parry window を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-fightingground-battle-system]] | 相手の攻撃を自動で guard し、guard 時に Drive Gauge が回復する。タイミングよく受け止めるとジャストパリィが発生する。 | high |
| [[sources/capcom-esports-base-terms]] | めくりに対して、Drive Parry は表裏両方に対応し得る対抗策として説明される。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | Opponent attack を repel し、成功時に Drive を replenish する。Perfect Parry は攻撃が当たる直前に parry すると発生する。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Frame data は startup `1`、active `12~ [2]`、recovery `33 [1]`。Activation cost は frame 2 に 5,000 Drive、frame 4 以降 hold は 50 Drive/frame、最小 whiff cost は 5,450 Drive と説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Frame data | startup `1`, active `12~ [2]`, recovery `33 [1]`; `[]` は Perfect Parry | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_frame_data` |
| Activation cost | frame `2` に `5000` Drive | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.activation_cost_drive_units` |
| Hold drain | frame `4` から `50` Drive/frame | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.hold_drain_drive_units_per_frame` |
| Minimum whiff cost | `5450` Drive | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.minimum_whiff_cost_drive_units` |
| Gain vs projectile | `5000` Drive | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.gain_vs_projectile_drive_units` |
| Gain vs Normal / Special / Drive Reversal | `10000` Drive | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.gain_vs_normal_special_drive_reversal_drive_units` |
| Gain vs Super Art / Critical Art / Drive Impact | `20000` Drive | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.gain_vs_super_critical_drive_impact_drive_units` |
| Perfect Parry timing extra without freeze | `3000` Drive | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.perfect_parry_extra_gain_without_freeze_drive_units` |
| Throw punish against Parry | drains `1` Drive bar | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.throw_punish_parry_drain_bars` |

## 意味差分

- 公式 Fighting Ground source は Drive Gauge 回復と Perfect Parry を中心に説明する。
- eSports BASE source は観戦用語として、めくり対策の文脈で使っている。
- SuperCombo Gauges page は successful parry の Drive gain を projectile `5,000`、Normal / Special / Drive Reversal `10,000`、Super Art / Critical Art / Drive Impact `20,000` とし、freeze のない Perfect Parry timing では extra gain `3,000` も記録する。community numeric source なので公式 source または実機検証があればそちらを優先する。

## 関連

- [[concepts/terms/perfect-parry]]
- [[concepts/terms/raw-drive-rush]]
- [[concepts/terms/cross-up]]
