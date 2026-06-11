---
type: concept
concept_type: term
title: "ドライブインパクト"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/drive-impact-counter]]"
  - "[[concepts/terms/corner]]"
  - "[[concepts/terms/stun]]"
  - "[[concepts/terms/armor-break]]"
  - "[[concepts/terms/crush]]"
  - "[[concepts/terms/lock]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Drive Impact"
  - "DI"
  - "ドライブインパクト"
tags:
  - sf6
  - terms
  - drive-system
---

# ドライブインパクト

## 要約

ドライブインパクトは、相手の攻撃を受け止めつつ攻撃できる Drive System の打撃技。Capcom 公式 Fighting Ground source は、相手をステージ端へ追い詰めた状況では guard されても壁やられを誘発できると説明している。SuperCombo Gauges page は frame、Drive drain、stun、character-specific range を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-official-fightingground-battle-system]] | 相手の攻撃を受け止めつつ攻撃できる強力な打撃技。ステージ端では guard されても壁やられを誘発できる。 | high |
| [[sources/capcom-esports-base-terms]] | Drive Impact への対策として Drive Impact を打ち返す「インパクト返し」を説明し、画面端の Drive Impact は特に重要だとしている。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | Incoming attack を absorb でき、corner の相手に対して block されても wall splat を誘発できる strike と説明している。 | medium |
| [[sources/supercombo-street-fighter-6-hud]] | HUD icon として、Drive Impact に関連する `Stun/Dizzy`、`Armor Break`、`Crush`、`Lock` の表示説明を含む。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Cost は 1 Drive bar。Frame data は startup `26(27)`、active `2`、recovery `35`、block `-3`、damage `800`。Drive drain は block `0.5`、hit `1`、counter hit `1.2`、punish counter crumple `1.5` とする。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Cost | `1` Drive bar | [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs[action=Drive Impact]` |
| Frame data | startup `26(27)`, active `2`, recovery `35`, block `-3`, damage `800` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_frame_data` |
| Opponent Drive drain | block `0.5`, hit `1`, counter hit `1.2`, punish / crumple `1.5` bars | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_drive_gauge_drain` |
| Armor / projectile interaction | `2` armor hits; projectile armor hit-freeze `6f`; absorb 後 startup `+1f` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values` |
| Damage scaling | hit `20%` starter scaling; block follow-up `20%` multiplier reduction | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values` |
| Stun follow-up | combo start `80%`, hit window `195f`, last `7f` は crouch-sized hurtbox | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values` |
| Character range table | 30 characters 分。term には全行を複製しない | [[sources/supercombo-street-fighter-6-gauges#Drive Impact range table]]; `drive_impact_range_by_character` |

## 意味差分

- 公式 source は「壁やられ」、SuperCombo は `wall splat` と表現する。wiki では source wording を残し、同一現象として扱えるかは context ごとに確認する。
- SuperCombo Gauges page は Drive Impact range を 30 characters 分の distance table として保持する。character-specific range query では source page の表に戻る。
- Frame / damage / Drive drain は community numeric source 由来なので、公式 frame-data や実機検証と矛盾する場合は公式・検証済み data を優先する。

## 関連

- [[concepts/terms/drive-impact-counter]]
- [[concepts/terms/corner]]
- [[concepts/terms/wall-bounce]]
- [[concepts/terms/stun]]
- [[concepts/terms/armor-break]]
- [[concepts/terms/crush]]
- [[concepts/terms/lock]]
