---
type: concept
concept_type: term
title: "ダメージ補正"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/scaling-reset]]"
  - "[[concepts/terms/perfect-parry]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "damage scaling"
  - "combo scaling"
  - "補正"
  - "コンボ補正"
tags:
  - sf6
  - terms
  - frame-data
---

# ダメージ補正

## 要約

ダメージ補正は、combo や特定条件によって後続 hit の damage が下がる仕組み。Capcom eSports BASE は、combo が長くなるほど一発ごとの damage が下がることを [[concepts/terms/scaling-reset|補正切り]] の説明で扱い、SuperCombo glossary は starter / combo / immediate / multiplier / minimum scaling の分類を説明している。SuperCombo Gauges page は Drive Impact、Drive Rush、Perfect Parry の system-specific scaling 値を補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] | Combo が長くなるほど damage scaling で一発ごとの damage が下がり、あえて combo を止めて scaling を reset する行為を補正切りと呼ぶ。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | 一部の技は combo 中に追加 damage scaling を発生させ、starter / combo / immediate / multiplier / minimum scaling などの種類がある。 | medium |
| [[sources/supercombo-street-fighter-6-glossary]] | Perfect Parry 後や mid-combo Drive Rush の multiplier scaling、Super Art level ごとの minimum scaling などを説明している。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Drive Impact は hit 時に `20%` starter scaling、block 後の follow-up に `20%` multiplier reduction を適用すると説明する。mid-combo Drive Rush は one-time `15%` damage scaling、Perfect Parry は `50%` damage scaling と説明する。 | medium |

## 数値データ

| 条件 | 値 | 根拠 |
|---|---:|---|
| Drive Impact on hit | `20%` starter scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.hit_starter_scaling_percent` |
| Drive Impact on block follow-up | `20%` multiplier reduction | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.block_followup_multiplier_reduction_percent` |
| Stun combo start | `80%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.dizzy_combo_start_scaling_percent` |
| Mid-combo Drive Rush | one-time `15%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values.mid_combo_damage_scaling_percent` |
| Perfect Parry punish | `50%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values.damage_scaling_percent` |
| Perfect Parry meter scaling | Super gauge gain `20%` less、attacker Drive gain / defender Drive damage `50%` less | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values` |

## 意味差分

- Capcom eSports BASE は観戦向けの大枠、SuperCombo glossary は community frame-data 用語として詳細分類を説明する。
- 個別 move の補正値は raw / official-supercombo enriched data を確認する。
- SuperCombo Gauges page の system-specific scaling 値は community numeric source なので、公式・実機検証と矛盾する場合はそちらを優先する。

## 関連

- [[concepts/terms/scaling-reset]]
- [[concepts/terms/perfect-parry]]
- [[concepts/frame-data]]
