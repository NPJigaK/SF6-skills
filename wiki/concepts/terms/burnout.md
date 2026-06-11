---
type: concept
concept_type: term
title: "バーンアウト"
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
  - "[[concepts/terms/chip-damage]]"
  - "[[concepts/terms/stun]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Burnout"
  - "burnout"
  - "バーンアウト状態"
tags:
  - sf6
  - terms
  - drive-system
---

# バーンアウト

## 要約

バーンアウトは、Drive Gauge が 0 になった時の resource exhaustion 状態。Capcom 公式 Fighting Ground source は、回復するまで Drive System を利用する技が一時的に使えなくなる状態として説明している。SuperCombo Gauges page は community numeric source として、Burnout 中の blockstun 増加、chip damage、Drive regeneration を補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-fightingground-battle-system]] | Drive Gauge が 0 になるとバーンアウト状態になり、回復するまで Drive System を利用する技は一時的に使えなくなる。 | high |
| [[sources/capcom-esports-base-terms]] | Burnout 中は必殺技 guard 時に体力が削られ、削り K.O. も可能。Burnout 中に Drive Impact を guard して画面端へ到達すると stun になる。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | Drive gauge が空になると Burnout に入り、gauge が回復するまで Drive-related techniques を使えない。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Burnout 中は全ての blockstun が +4f され、special / Super を block した時の chip damage は通常 damage の約 25%、Drive options は完全回復まで使用不可と説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| 追加 blockstun | `+4f` | [[sources/supercombo-street-fighter-6-gauges#Burnout]]; `burnout_values.additional_blockstun_frames` |
| Burnout chip damage | 通常 damage の約 `25%` | [[sources/supercombo-street-fighter-6-gauges#Burnout]]; `burnout_values.chip_damage_percent_of_normal_damage` |
| Base Drive Regen during Burnout | `50` Drive/frame, `30%` bar/sec | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration]]; `drive_regeneration_rates` |
| Hitstun regen during Burnout | `25` Drive/frame, `15%` bar/sec | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration]]; `drive_regeneration_rates` |
| Walking forward frame 11+ during Burnout | `50 x2 + 20 = 120` Drive/frame, `0.72` bars/sec | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration]]; `drive_regeneration_walk_forward_formulas` |
| Stun recovery note | stun 回復後に Drive Gauge が full replenish | [[sources/supercombo-street-fighter-6-gauges#Burnout]]; `burnout_values.stun_replenishes_drive_gauge` |

## 意味差分

- 現時点では、公式 source と SuperCombo glossary の大枠は一致している。
- SuperCombo Gauges page は Base Drive Regeneration などの回復速度を数値化しているが、community source なので公式 source または実機検証がある場合はそちらを優先する。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/chip-damage]]
- [[concepts/terms/stun]]
- [[concepts/terms/drive-impact]]
