---
type: concept
concept_type: term
title: "スタン"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/corner]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "stun"
  - "Dizzy"
  - "dizzy"
  - "Stun/Dizzy"
  - "ピヨる"
  - "すたん"
tags:
  - sf6
  - terms
  - drive-system
  - hud
---

# スタン

## 要約

スタンは、相手が無防備になり大きな combo 機会が生まれる状態。Capcom eSports BASE では、Burnout 中の相手に Drive Impact を guard させ、画面端に到達した時に発生する状態として説明されている。SuperCombo HUD page は `Stun/Dizzy` icon の表示 cue として、Burnout 中の cornered opponent に Drive Impact が connect した時に出ると説明している。SuperCombo Gauges page は stun duration と follow-up scaling を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-01` | Burnout 中の相手に Drive Impact を guard させて画面端に到達すると stun にできる。stun した相手には大 damage の機会があり、stun 後は Burnout が解除される。 | high |
| [[sources/supercombo-street-fighter-6-hud]] | `Stun/Dizzy` icon は、Burnout 中の cornered opponent に Drive Impact が connect し、free combo followup が可能になる時に表示される。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Burnout 中の corner Drive Impact hit / block は stun を発生させ、follow-up combo は 80% scaling から開始、stun duration は 195f、最後の 7f は crouching hurtbox size になると説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Stun condition | Burnout 中の corner Drive Impact wall splat は hit / block どちらでも stun | [[sources/supercombo-street-fighter-6-gauges#Burnout]] |
| Follow-up combo start | `80%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.dizzy_combo_start_scaling_percent` |
| Hit window after wall impact | `195f` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.dizzy_hit_window_frames` |
| Last crouch-sized hurtbox frames | last `7f` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.last_crouch_sized_hurtbox_frames` |
| Stun recovery note | stun 回復後に Drive Gauge が full replenish | [[sources/supercombo-street-fighter-6-gauges#Burnout]]; `burnout_values.stun_replenishes_drive_gauge` |

## 意味差分

- 現時点では SF6 の Burnout / Drive Impact / 画面端に紐づく説明として扱う。旧作一般の stun とは条件が異なる可能性がある。
- Capcom eSports BASE は Drive Impact を guard させて画面端に到達する条件を説明する。SuperCombo HUD page の `connects` wording は HUD 表示 cue の community source として残し、条件説明では公式 source を優先する。
- SuperCombo Gauges page の stun duration / hurtbox / scaling 値は community numeric source として扱い、公式 source または実機検証があればそちらを優先する。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/corner]]
- [[concepts/terms/burnout]]
- [[concepts/terms/drive-impact]]
- [[concepts/terms/drive-impact-counter]]
