---
type: concept
concept_type: term
title: "ジャストパリィ"
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
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Perfect Parry"
  - "perfect parry"
  - "just parry"
  - "じゃすとぱりぃ"
tags:
  - sf6
  - terms
  - drive-system
---

# ジャストパリィ

## 要約

ジャストパリィは、攻撃を正確な timing で parry した時に発生する防御選択肢。Capcom eSports BASE は、2 frame window、slow 演出、反撃に向けた有利時間、後続 combo damage への scaling を説明している。SuperCombo Gauges page は 60f freeze、projectile Perfect Parry、Super / Drive gain scaling を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-08` | Parry timing が合うと発生し、猶予は 2 frame。成功時は slow 演出と反撃機会が増える一方、後続 combo に 50% damage scaling がかかる。 | high |
| [[sources/supercombo-street-fighter-6-gauges]] | Perfect Parry は Drive Parry の最初の 2 active frames で発生し、50% damage scaling、60f screen freeze、Super gauge gain 20% less、attacker Drive gain / defender Drive damage 50% less と説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Timing window | `2` frames | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_frame_data.perfect_parry_window_frames` |
| Strike Perfect Parry freeze | `60f` / `1` second | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values.strike_freeze_frames` |
| Projectile Perfect Parry recovery | fixed `11f` recovery = `1f` Parry + `10f` extra recovery | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values.projectile_recovery_frames`, `projectile_extra_recovery_frames` |
| Projectile hold grace | Parry input を追加 `13f` hold しても standard recovery を受けない | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values.projectile_hold_extra_frames_without_standard_recovery` |
| Damage scaling | punish に `50%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values.damage_scaling_percent` |
| Meter scaling | Super gauge gain `20%` less、attacker Drive gain / defender Drive damage `50%` less | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values` |
| No-freeze timing extra | `3000` Drive extra gain | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_costs_and_gains.perfect_parry_extra_gain_without_freeze_drive_units` |

## 意味差分

- 公式 frame-data output には system row としてさらに細かい説明がある。現時点では eSports BASE の観戦者向け説明を高信頼度の根拠とし、SuperCombo Gauges page の追加数値は community numeric source として扱う。
- SuperCombo Gauges page は projectile Perfect Parry の固定 recovery を `11f`（`1f` Parry + `10f` extra recovery）とする。これは通常 Perfect Parry の `2 frame window` とは別の recovery 値として扱い、source 間差分が出た場合は公式・実機検証を優先する。

## 関連

- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[concepts/terms/scaling-reset]]
