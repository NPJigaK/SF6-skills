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
  - "[[sources/supercombo-street-fighter-6-game-data]]"
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

ダメージ補正は、combo や特定条件によって後続 hit の damage が下がる仕組み。Capcom eSports BASE は、combo が長くなるほど一発ごとの damage が下がることを [[concepts/terms/scaling-reset|補正切り]] の説明で扱い、SuperCombo glossary は starter / combo / immediate / multiplier / minimum scaling の分類を説明している。SuperCombo Gauges page は Drive Impact、Drive Rush、Perfect Parry の system-specific scaling 値を補う。SuperCombo Game Data page は標準 scaling progression、Super Art minimum、Level 3 cancel penalty、character-specific scaling tabs をまとめる community numeric source。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] | Combo が長くなるほど damage scaling で一発ごとの damage が下がり、あえて combo を止めて scaling を reset する行為を補正切りと呼ぶ。 | high |
| [[sources/supercombo-street-fighter-6-glossary]] | 一部の技は combo 中に追加 damage scaling を発生させ、starter / combo / immediate / multiplier / minimum scaling などの種類がある。 | medium |
| [[sources/supercombo-street-fighter-6-glossary]] | Perfect Parry 後や mid-combo Drive Rush の multiplier scaling、Super Art level ごとの minimum scaling などを説明している。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Drive Impact は hit 時に `20%` starter scaling、block 後の follow-up に `20%` multiplier reduction を適用すると説明する。mid-combo Drive Rush は one-time `15%` damage scaling、Perfect Parry は `50%` damage scaling と説明する。 | medium |
| [[sources/supercombo-street-fighter-6-game-data]] | 標準 scaling progression は `100 / 100 / 80 / 70 / 60 / 50 / 40 / 30 / 20 / 10%`、Light Normal or 2MK starter は `100 / 80 / 70 / 60 / 50 / 40 / 30 / 20 / 10 / 10%` とする。 | medium |
| [[sources/supercombo-street-fighter-6-game-data]] | Super Arts の minimum scaling は SA1 `30%`、SA2 `40%`、SA3 / CA `50%`。Special cancel からの Level 3 は追加 `10%` damage scaling penalty と説明する。 | medium |
| [[sources/supercombo-street-fighter-6-game-data]] | Character-specific scaling は 30 character tabs / 30 tables として保持され、derived output の table indices `1..30` に対応する。 | medium |

## 数値データ

この section は SuperCombo Game Data の damage scaling 数値を、計算時に参照しやすい形へ昇格したもの。値は community numeric source であり、公式 source または実機検証と矛盾する場合はそちらを優先する。正本 raw は [[sources/supercombo-street-fighter-6-game-data]] と `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`。

### SF6 Damage Scaling progression

| Attack # | General Scaling | Light Normal or 2MK Combo Starter |
| --- | --- | --- |
| 1st Attack | 100% | 100% |
| 2nd Attack | 100% | 80% |
| 3rd Attack | 80% | 70% |
| 4th Attack | 70% | 60% |
| 5th Attack | 60% | 50% |
| 6th Attack | 50% | 40% |
| 7th Attack | 40% | 30% |
| 8th Attack | 30% | 20% |
| 9th Attack | 20% | 10% |
| 10th + Attack | 10% | 10% |

### System-wide scaling rules

| Condition | Value / rule | Calculation note |
| --- | --- | --- |
| Super Art minimum | SA1 30%; SA2 40%; SA3 / CA 50% | Super Arts always do at least the listed minimum, even if combo scaling would be lower. |
| Level 3 special cancel penalty | additional 10% damage scaling penalty | Raw Special > SA3 is described as 100% -> 90%; outside that case the page says it acts as one additional hit of scaling, 100% -> 100% -> 70%. |
| Perfect Parry punish | damage scaling x50% | A normal progression becomes 50 -> 50 -> 40 -> 35 -> 30...; delaying to avoid scaling means it was not a true punish. |
| Perfect Parry meter scaling | Super gain 80%; attacker Drive gain 50%; defender Drive damage 50% | Applies to all hits of a punish combo; Super Drive damage is also reduced. |
| Raw Drive Rush starter | no additional scaling penalty | Other applicable penalties, such as 2MK starter scaling, still apply. |
| Mid-combo Drive Rush | additional 15% scaling penalty to all remaining hits | Rounded down to whole numbers; multiple Drive Rush uses do not stack this penalty. Example progression: 100 -> 85 -> 68 -> 59 -> 51 -> 42 -> 34 -> 25 -> 17 -> 8... |
| Perfect Parry + Drive Rush | multiplicative; example 80% * 0.5 * 0.85 = 34% | Can bring effective scaling below the normal 10% floor, as low as 4% when combined. |
| Blocked Drive Impact corner wallsplat | 20% scaling multiplier | DI does not count as first combo hit; first attack after wallsplat can still apply starter scaling. |
| Drive Impact hit crumple / wallsplat / Burnout stun | 20% starter scaling | Follow-up example is 80% -> 70% -> 60%... |
| Throw comboed after stun / DI crumple / grounded wall splat | immediate 20% damage scaling to the throw | Often applies to command throws, but not universally; separate from throws that start combos. |
| Attack count definition | one attack corresponds to each player-input move, not each hit | Example: Chun-Li Lightning Kicks count as one attack; Jamie Freeflow Kicks sequence counts as three unless otherwise stated. |

### System-specific scaling index

| 条件 | 値 | 根拠 |
|---|---:|---|
| Drive Impact on hit | `20%` starter scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.hit_starter_scaling_percent` |
| Drive Impact on block follow-up | `20%` multiplier reduction | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.block_followup_multiplier_reduction_percent` |
| Stun combo start | `80%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_additional_values.dizzy_combo_start_scaling_percent` |
| Mid-combo Drive Rush | one-time `15%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values.mid_combo_damage_scaling_percent`; [[sources/supercombo-street-fighter-6-game-data]] |
| Perfect Parry punish | `50%` damage scaling | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values.damage_scaling_percent`; [[sources/supercombo-street-fighter-6-game-data]] |
| Perfect Parry meter scaling | Super gauge gain `20%` less、attacker Drive gain / defender Drive damage `50%` less | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `perfect_parry_values`; [[sources/supercombo-street-fighter-6-game-data]] |
| Super Art minimum scaling | SA1 `30%`, SA2 `40%`, SA3 / CA `50%` | [[sources/supercombo-street-fighter-6-game-data]] |
| Level 3 special cancel penalty | additional `10%` damage scaling penalty | [[sources/supercombo-street-fighter-6-game-data]] |

### Character-Specific Scaling

Character-specific table は SuperCombo Game Data の tabber 30 tabs を source-preserving に展開したもの。Move 表記は SuperCombo rendered table text のまま保持する。

#### A.K.I.

| Move | Damage Scaling Notes |
| --- | --- |
| 6HK | 20% scaling when beginning a combo |
| j.HP | 20% scaling when beginning a combo |
| 214PP~6P | 2 hits of scaling when comboed into (applies to next attack) |
| 214HP | 15% immediate scaling when comboed into |
| 236PP | 20% scaling [Toxic Blossom: 10%] when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214K | 20% scaling when beginning a combo (meterless versions) |
| 2PP~LPLK | 20% immediate scaling when comboed into (Stun, DI Crumple, etc.) |

#### Alex

| Move | Damage Scaling Notes |
| --- | --- |
| 5HP | 10% scaling when beginning a combo |
| 5[HP] | 20% scaling when beginning a combo |
| 5HK 5[HK] | 15% scaling when beginning a combo |
| 4MK (Backturn) | Both hits count as separate attacks for damage scaling |
| 5MP~HP | 30% immediate scaling when comboed into |
| 2PP~6P | 20% scaling when beginning a combo |
| 2PP~LP | 20% scaling when beginning a combo |
| 2PP~HP 2PP~[HP] | 20% scaling when beginning a combo |
| 2PP~MK | 20% scaling when beginning a combo |
| 236LP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 63214P 63214PP | 20% immediate scaling when comboed into (Stun, DI Crumple, etc.) |
| 63214P (Backturn) | 20% immediate scaling when comboed into (e.g. after 236HP) |
| 63214PP (Backturn) | 40% scaling when beginning a combo 15% immediate scaling when comboed into (e.g. after 236HP) 2 hits of scaling when comboed into (applies to next attack) Ensures that PP SA2 (Omega Wing Buster) follow-up never deals more than 60% of its base damage 63214PP~6 maintains the same level of scaling as the initial throw |
| SA2 | 50% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |

#### Akuma

| Move | Damage Scaling Notes |
| --- | --- |
| 5HK | 2 hits of scaling when comboed into (applies to next attack) |
| 4HK | 20% scaling when beginning a combo |
| j.2MK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 5MP~MP | 2 hits of scaling when comboed into (applies to next attack) |
| 5MK~HK | 2 hits of scaling when comboed into (applies to next attack) |
| 236[P] (Lv.2/Lv.3 Charge) 236PP 236[PP] (Full Charge) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| j.236P | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) Also applies to Shin Akuma j.214PP (Double Zanku Hadoken) |
| 623P | 20% scaling when beginning a combo 30% total when combined with SA3 cancel scaling |
| 214LK 214MK | 2 hits of scaling when comboed into (applies to next attack) |
| j.214K | 30% scaling when beginning a combo |
| j.214KK | 2 hits of scaling when comboed into (applies to next attack) |
| 214PP | 20% scaling when beginning a combo |
| 214HP~6P | 3 hits of scaling when comboed into (applies to next attack) |
| 236K~K 236KK~K | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236KK~214K | 2 hits of scaling when comboed into (applies to next attack) |
| Air SA1 | 10% scaling when beginning a combo 5% extra scaling when comboed into (applies to next attack) |
| SA2 | 40% scaling when beginning a combo 4 hits of scaling when comboed into (applies to next attack) |

#### Blanka

| Move | Damage Scaling Notes |
| --- | --- |
| 6HP | 20% scaling when beginning a combo |
| [4]6LP (during SA2) [4]6MP (during SA2) | 10% scaling when beginning a combo 10% immediate scaling when comboed into |
| [4]6HP | 20% scaling when beginning a combo |
| [4]6HP (during SA2) | 20% scaling when beginning a combo 10% immediate scaling when comboed into |
| [4]6PP [4]6PP (during SA2) | 20% scaling when beginning a combo |
| [2]8K (during SA2) | 10% scaling when beginning a combo 10% immediate scaling when comboed into |
| [2]8KK (during SA2) | 40% scaling when beginning a combo 10% immediate scaling when comboed into |
| 63214K (during SA2) 63214KK (during SA2) | 10% scaling when beginning a combo 10% immediate scaling when comboed into |
| j.[4]6P (during SA2) j.[4]6PP (during SA2) | 10% scaling when beginning a combo 10% immediate scaling when comboed into |
| 22P (Blanka-Chan) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| Forward Throw | 20% scaling when beginning a combo into Blanka-chan Bomb (applies to 3rd hit of combo) e.g. Throw 100% -> Blanka-chan 100% (2-hit scaling) -> Follow-up 50% 3rd combo hit (usually 80%) is reduced 20% from Throw and another 10% by Blanka-chan |

#### C. Viper

| Move | Damage Scaling Notes |
| --- | --- |
| 6HK | 20% scaling when beginning a combo |
| 214PP | 30% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236KK | 30% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 623P 623PP | 20% scaling when beginning a combo |
| 214K Lv.1/2 214KK Lv.1/2 | 50% scaling when beginning a combo |
| 214[K] Lv.3 214[KK] Lv.3 | 20% scaling when beginning a combo |

#### Cammy

| Move | Damage Scaling Notes |
| --- | --- |
| 4HK | 20% scaling when beginning a combo |
| 6HK | 20% scaling when beginning a combo |
| 5HP~HK | Each hit of HK counts as a separate attack for scaling 2nd hit applies 2 hits of combo scaling to follow-up when comboed into |
| 236KK | 5% extra scaling when comboed into (applies to next attack) |
| 214MP | 20% scaling when beginning a combo |
| 214HP/PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| j.214K | 20% scaling when beginning a combo |
| j.214KK | 20% scaling when beginning a combo 10% immediate scaling when comboed into Also applies to OD Hooligan Divekick |
| 236P~Slide 236[HP]~Slide 236PP~Slide | 20% scaling when beginning a combo |
| 236P~K Divekick | 20% scaling when beginning a combo |
| 236[HP]~K Divekick 236PP~K Divekick | 20% scaling when beginning a combo 10% immediate scaling when comboed into |
| 236P~2K Overhead 236[HP]~2K Overhead 236PP~2K Overhead | 20% scaling when beginning a combo |
| 236[HP]~LPLK Throw | 20% scaling when beginning a combo |
| 236PP~LPLK Throw | 30% scaling when beginning a combo |

#### Chun-Li

| Move | Damage Scaling Notes |
| --- | --- |
| 5HK | 20% scaling when beginning a combo |
| j.2MK | 15% scaling when beginning a combo |
| [4]6PP | 20% scaling when beginning a combo |
| j.236K | 20% scaling when beginning a combo Weaker when used as a counter to throw loops |
| 214LK 214HK | 20% scaling when beginning a combo |
| 214MK | 30% scaling when beginning a combo |
| 214KK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| SA2 | 40% scaling when beginning a combo 3 hits of scaling when comboed into (applies to next attack) |

#### Dee Jay

| Move | Damage Scaling Notes |
| --- | --- |
| 5HP | 20% scaling when beginning a combo |
| 5HK | 20% scaling when beginning a combo |
| 5LP~MK | 20% scaling when beginning a combo with the MK |
| [4]6PP | 20% scaling when beginning a combo |
| 236HK | 25% scaling when beginning a combo |
| 236KK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214PP | 2 hits of scaling when comboed into (applies to next attack) |
| 214K~LK | 20% scaling when beginning a combo |
| PC 214K~MK | 30% scaling when beginning a combo |
| 214KK~HK | 2 hits of scaling when comboed into (applies to next attack) |
| SA1 | 40% scaling when beginning a combo (Counter-Hit/Punish Counter crumple follow-ups) |
| SA2 | 25% scaling when beginning a combo 3 hits of scaling when comboed into (applies to next attack) Follow-up rhythm hits do not add additional scaling |

#### Dhalsim

| Move | Damage Scaling Notes |
| --- | --- |
| 2LK | Does not have the usual light normal scaling 1LK acts as a standard 2LK with 20% starter scaling |
| 2MK | 20% scaling when beginning a combo (after well-spaced slide) 1MK acts as a standard cancelable 2MK with 20% starter scaling |
| 4HP | 20% scaling when beginning a combo |
| j.MP / j.MK j.HP / j.HK | 20% scaling when beginning a combo |
| j.2K | 20% scaling when beginning a combo |
| 236KK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| j.63214PP | 20% scaling when beginning a combo |

#### Ed

| Move | Damage Scaling Notes |
| --- | --- |
| 2MP | Acts as a standard cancelable 2MK with 20% starter scaling |
| 5[HP] (Lv.1) 5[HP] (Lv.2) | 20% scaling when beginning a combo |
| 5MP~HP | 2 hits of scaling when comboed into (applies to next attack) |
| 2HK~HP | 3 hits of scaling when comboed into (applies to next attack) |
| 623LP | 30% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214PP | 2 hits of scaling when comboed into (applies to next attack) |
| 236[K] (Charged LK/MK/HK version) | 20% scaling when beginning a combo 15% extra scaling when comboed into (applies to next attack) |
| 236KK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 5KK~6P (Early) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 5KK~6P (Late) | 20% scaling when beginning a combo |
| SA3 / CA | 30% immediate scaling when canceled into from 236LK/236MK |

#### E. Honda

| Move | Damage Scaling Notes |
| --- | --- |
| Enhanced 214P (Sumo Spirit) | 2 hits of scaling when comboed into (applies to next attack) Meterless versions only |
| [4]6P | 30% scaling when beginning a combo 40% total when combined with SA3 cancel scaling |
| [2]8K [2]8KK | 25% scaling when beginning a combo (Punish Counter OTG bounce) |
| 63214K 63214KK | 20% immediate scaling when comboed into (Stun, DI Crumple, etc.) |

#### Elena

| Move | Damage Scaling Notes |
| --- | --- |
| 2HP | 20% scaling when beginning a combo |
| 4HK | 20% scaling when beginning a combo |
| 5HP-HP | 20% scaling when beginning a combo (does not apply to 5HP) |
| 236LK 236KK | 30% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236MK 236HK | 2 hits of scaling when comboed into (applies to next attack) |
| 623K 623KK | 30% scaling when beginning a combo |
| 236P-6MK | 30% scaling when beginning a combo (applies to enhanced version as well) |
| 236P-6HK | 20% scaling when beginning a combo (applies to enhanced version as well) |
| 214LK 214MK | 20% scaling when beginning a combo |
| 214HK 214KK | 2 hits of scaling when comboed into (applies to next attack) |
| 214P-6P 214PP-6P | 5% extra scaling when comboed into (applies to next attack) |
| SA1 | 30% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) 10% immediate scaling when comboed into |

#### Guile

| Move | Damage Scaling Notes |
| --- | --- |
| 5HP | 20% scaling when beginning a combo |
| 2HK | 20% scaling when beginning a combo (2HK~3HK Punish or Drive Rush starter) |
| 2MP~2MP (Double Shot) | 10% immediate scaling on the 2nd attack Starting a combo (2MP~2MP > Special): 100% -> 90% -> 70% Comboed into (e.g. j.HK, 2MP~2MP > Special): 100% -> 100% -> 70% -> 60% |
| [4]6PP | 20% scaling when beginning a combo |
| [2]8K | 30% scaling when beginning a combo 40% total when combined with SA3 cancel scaling |

#### Ingrid

| Move | Damage Scaling Notes |
| --- | --- |
| 5HP | 20% scaling when beginning a combo |
| 5MP~MK (Pretty Heel Kick) | 2 hits of scaling when comboed into (applies to next attack) |
| 236P 236PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214MP 214HP 214PP | 30% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) Applies to all 0-stock, 1-stock, and 2-stock versions |
| j.214MP j.214HP (1) j.214PP (0) | 20% scaling when beginning a combo |
| j.214HP (2) j.214PP (1) | 30% scaling when beginning a combo |
| j.214PP (2) | 30% scaling when beginning a combo 5% extra scaling when comboed into (applies to next attack) |
| 236LK | 20% scaling when beginning a combo |
| 236MK 236KK | 2 hits of scaling when comboed into (applies to next attack) |
| 236HK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 2KKK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| SA2 | 20% immediate scaling when comboed into |
| Forward Throw | 20% scaling when beginning a combo into SA2 projectiles This scaling does not apply to Back Throw because it juggles before the throw deals damage |

#### Jamie

| Move | Damage Scaling Notes |
| --- | --- |
| Drink Levels (DL0 - DL4) | 90/95/100/105/110% scaling for DL0/1/2/3/4 respectively Reaching DL4 with SA2 install only gives 105% scaling |
| 6HK~4HK~P (DL4 Headbutt) | 2 hits of scaling when comboed into (applies to next attack) |
| 2KK | 20% scaling when beginning a combo |
| 236PP~6P~6P (DL0-DL4) | All 6P follow-ups do not count as separate attacks for damage scaling 6K follow-ups and meterless 6P follow-ups still count separately |
| 623LK | 30% scaling when beginning a combo |
| 214PP | 20% scaling when beginning a combo |
| 214P~6P (DL4) 214PP~6P (DL4) | 20% scaling when beginning a combo e.g. blocked palm + frame trap into 6P follow-up |
| j.214KK (DL1+) | 20% scaling when beginning a combo 10% immediate scaling when comboed into (e.g. j.MP > 214KK) |
| 63214K (DL3+) | 20% scaling when beginning a combo, applied to the 3rd hit of combo e.g. 63214K (100%), 2MP (100%) > 623K (60%) 20% immediate scaling when comboed into (e.g. after corner PC 214PP) |
| 63214KK (DL3+) | 30% scaling when beginning a combo |
| SA3 (Launch) | 2 hits of scaling when comboed into (applies to next attack) |

#### JP

| Move | Damage Scaling Notes |
| --- | --- |
| 5HP | 20% scaling when beginning a combo |
| 4MP~MP | 2 hits of scaling when comboed into (applies to next attack) |
| Forward Throw | 40% scaling when beginning a combo (juggle into SA2 or Amnesia bomb) Back Throw can also juggle before Throw damage is applied, causing no additional scaling |
| 214P (Portal Spike) 214PP (Portal Spike) | 20% scaling when beginning a combo Also applies to manual activation with 214HP |
| 22PP | 20% scaling when beginning a combo |
| 236KK | 20% scaling when beginning a combo |
| 214K 214KK | 10% immediate scaling when comboed into |
| 22K (Bomb Explosion) 22KK (Bomb Explosion) | 50% scaling when beginning a combo 60% immediate scaling when comboed into Canceling a move into SA3 immediately detonates bombs to prevent JP from bypassing this scaling |
| SA2 | 25% scaling when beginning a combo, applied to the 3rd hit of combo 25% immediate scaling when comboed into |

#### Juri

| Move | Damage Scaling Notes |
| --- | --- |
| 5HK (Regular/FSE) | 20% scaling when beginning a combo |
| 236LK (1-Stock) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236MK 236MK (1-Stock) 236LK+HK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236MK+HK | 20% scaling when beginning a combo |
| 214KK | 2 hits of scaling when comboed into (applies to next attack) |

#### Ken

| Move | Damage Scaling Notes |
| --- | --- |
| 5HK | 30% scaling when beginning a combo Applies to Punish Counter juggle follow-ups |
| 5MP~HP | 2 hits of scaling when comboed into (applies to next attack after HP) |
| 236PP | 20% scaling when beginning a combo |
| 623P | 20% scaling when beginning a combo 30% total when combined with SA3 cancel scaling |
| j.214K j.214KK | 30% scaling when beginning a combo |
| 623LK | 30% scaling when beginning a combo |
| 623MK 623HK | 30% scaling when beginning a combo 3 hits of scaling when comboed into (applies to next attack) |
| 623KK KK~623K | 5% extra scaling when comboed into Each hit counts separately for scaling when juggled into |
| 236K~6LK | 20% scaling when beginning a combo 5% extra scaling when comboed into (applies to next attack) |
| 236KK~6MK | 20% scaling when beginning a combo |
| 236KK~6LK~6K 236KK~6MK~6K | 2 hits of scaling when comboed into (applies to next attack) |
| KK~HK | 20% scaling when beginning a combo |
| KK~214K | 15% scaling when beginning a combo |

#### Kimberly

| Move | Damage Scaling Notes |
| --- | --- |
| 5MK | 15% scaling when beginning a combo |
| 3MK | 15% scaling when beginning a combo |
| 4HK | 25% scaling when beginning a combo |
| 6HK | 20% scaling when beginning a combo |
| 214KK | 30% scaling when beginning a combo |
| j.214K | 20% scaling when beginning a combo |
| j.214KK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236LP | 20% scaling when beginning a combo Mostly relevant after spaced +5 starter or when Light > Light > 236LP breaks DI armor as a Counter-hit |
| 236K~MK 236KK~MK | 20% scaling when beginning a combo |
| 236KK(close)~P (OD Arc Step > Throw) | 20% scaling when beginning a combo (OTG bounce) |
| j.236PP | 20% scaling when beginning a combo (OTG bounce) 2 hits of scaling when comboed into (applies to next attack) |
| 22P (Explosion) | 10% scaling when beginning a combo No difference between single/double spraycan detonation |
| Forward Throw | 20% scaling when beginning a combo into Spraycan explosion Total scaling will be: 100% (Throw) -> 80% (Bomb) -> 70% (Follow-up Juggle) ... |
| SA3 / CA | Upon activation, base damage scaling increased to 111% for the rest of the match Effectively brings Kimberly's damage values in line with the rest of the cast |

#### Lily

| Move | Damage Scaling Notes |
| --- | --- |
| 214PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236KK W.236K W.236KK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 623PP W.623PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| j.PPP W.j.PPP | 10% immediate scaling when comboed into (e.g. canceled from 623PP on hit) |
| 360+P 360+PP | 20% immediate scaling when comboed into (Stun, DI Crumple, etc.) |
| SA3 / CA | 10% immediate scaling when comboed into Unlike most SA3 scaling, this applies to any combo, not just from special moves |

#### Luke

| Move | Damage Scaling Notes |
| --- | --- |
| 2MP | 15% scaling when beginning a combo |
| 2HP | 5% extra scaling when comboed into (applies to next attack) |
| 6HP~6HP | 2 hits of scaling when comboed into (applies to next attack) Does not apply after Punish Counter 6HP starter |
| 236PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214[P] pf.214[P] | Each hit counts as a separate attack for scaling Does not apply to Perfect MP Flash Knuckle |
| 236KK~P 236KK~K | 50% scaling when beginning a combo |

#### M. Bison

| Move | Damage Scaling Notes |
| --- | --- |
| 5HP | 20% scaling when beginning a combo |
| Psycho Mine | Acts as 1 standard hit of damage scaling at the beginning or middle of combo Does not add extra scaling when automatically triggered by special moves |
| [4]6P [4]6PP | 30% scaling when beginning a combo 40% total when combined with SA3 cancel scaling Also applies with automatic Psycho Mine detonation |
| 236LK | 30% scaling when beginning a combo |
| 236MK | 20% scaling when beginning a combo |
| 236KK | 2 hits of scaling when comboed into (applies to next attack) |

#### Mai

| Move | Damage Scaling Notes |
| --- | --- |
| 5HK | 20% scaling when beginning a combo |
| 4HK~HK | 3 hits of scaling when comboed into (applies to next attack) |
| 236PP Flame 236PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236[P] (No Flame) | 20% scaling when beginning a combo |
| 214LP Flame 214LP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| Flame 214MP | 2 hits of scaling when comboed into (applies to next attack) |
| 214HP (No Flame) | 2 hits of scaling when comboed into (applies to next attack) |
| 236KK (No Flame) | 2 hits of scaling when comboed into (applies to next attack) |
| j.214PP Flame j.214PP | 30% scaling when beginning a combo |
| SA2 (ground) Flame SA2 (ground) | 40% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| Air SA2 Flame Air SA2 | 2 hits of scaling when comboed into (applies to next attack) |

#### Manon

| Move | Damage Scaling Notes |
| --- | --- |
| 214KK | 20% scaling when beginning a combo |
| 236P~K 236PP~K | 10% immediate scaling when comboed into |
| SA3 / CA | 5% immediate scaling when comboed into 15% when canceled from 236HK 1st hit Unlike most SA3 scaling, this applies to any combo, not just from special moves |

#### Marisa

| Move | Damage Scaling Notes |
| --- | --- |
| 5HP / 5[HP] | 10% scaling when beginning a combo Applies to 5HP~HP Target Combo or after PC/DR 5HP links |
| 5HK / 5[HK] | 10% scaling when beginning a combo Mostly relevant for Punish Counter 5HK juggles |
| 5LP~LP | 10% scaling when beginning a combo with the second 5LP 5% extra scaling when 2nd hit is comboed into (applies to next attack) 5LP~LP has a 3f gap on block, allowing the 2nd hit to frame trap and begin a combo The initial 5LP requires CH/PC/DR to combo into the 2nd hit of the TC |
| 214P~6P (MP/HP/PP versions) | 2 hits of scaling when comboed into (applies to next attack) |
| 236PP 236[PP] | 30% scaling when beginning a combo |
| 623PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| SA2 | 15% immediate scaling when comboed into |

#### Rashid

| Move | Damage Scaling Notes |
| --- | --- |
| 2HP | 20% scaling when beginning a combo |
| 6HK | 20% scaling when beginning a combo |
| j.2HP | 15% scaling when beginning a combo |
| 5MP~HK | 2 hits of scaling when comboed into (applies to next attack) |
| Run~6P | 20% scaling when beginning a combo |
| Run~6K | 15% scaling when beginning a combo |
| Run~6K (Air Current) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236LP (Regular) | 30% scaling when beginning a combo |
| 236LP (Air Current) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236MP (Regular) | 10% scaling when beginning a combo |
| 236PP (Regular/Air Current) | 20% scaling when beginning a combo |
| 214KK (Regular) | 2 hits of scaling when comboed into (applies to next attack) |
| 236KK (Uncharged) | 25% scaling when beginning a combo 15% extra scaling when comboed into (applies to next attack) |
| 236[KK] (Charged) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214P~6K~K (Nail Assault) | 20% scaling when beginning a combo |
| SA2 | 2 hits of scaling when comboed into (applies to next attack) |

#### Ryu

| Move | Damage Scaling Notes |
| --- | --- |
| 236PP Denjin 236HP Denjin 236PP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 623P | 30% scaling when beginning a combo 40% total when combined with SA3 cancel scaling |
| j.214K | 30% scaling when beginning a combo |
| j.214KK | 15% extra scaling when comboed into (applies to next attack) |
| 236KK | 5% extra scaling when comboed into (applies to next attack) |
| 214PP (Regular) | 2 hits of scaling when comboed into (applies to next attack) |

#### Sagat

| Move | Damage Scaling Notes |
| --- | --- |
| 5HK | 20% scaling when beginning a combo |
| 4HP | 10% scaling when beginning a combo |
| 6LK | 30% scaling when beginning a combo |
| 6HK | 10% scaling when beginning a combo 5% extra scaling when comboed into (applies to next attack) |
| 236LP | 2 hits of scaling when comboed into (applies to next attack) |
| 236PP (High or Low) | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 623LP | 30% scaling when beginning a combo 40% total when combined with SA3 cancel scaling |
| 623MP | 20% scaling when beginning a combo 30% total when combined with SA3 cancel scaling |
| 623HP (Uncharged) | 10% scaling when beginning a combo 20% total when combined with SA3 cancel scaling |
| 236LK 236MK | 20% scaling when beginning a combo |
| 236KK | 30% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 214LK 214MK | 20% scaling when beginning a combo |
| 214K~6LK 214KK~6LK | 20% scaling when beginning a combo |
| 214K~6MK 214KK~6MK | 2 hits of scaling when comboed into (applies to next attack) |
| 214K~6HK 214KK~6HK | 2 hits of scaling when comboed into (applies to next attack) |
| SA2~6 (Launcher) | 50% scaling when beginning a combo 4 hits of scaling when comboed into (applies to next attack) |

#### Terry

| Move | Damage Scaling Notes |
| --- | --- |
| 5MP~HP | 30% immediate scaling when HP is comboed into |
| 5MP~HK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 2MK~2HK | 2 hits of scaling when comboed into (applies to next attack) |
| 236PP | 20% scaling when beginning a combo |
| 214LP | 30% scaling when beginning a combo |
| 214LPMP | 20% scaling when beginning a combo |
| 214MPHP | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 623P | 20% scaling when beginning a combo 30% total when combined with SA3 cancel scaling |
| 236LK 236MK | 20% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| 236KK | 2 hits of scaling when comboed into (applies to next attack) |
| 214HK | 2 hits of scaling when comboed into (applies to next attack) |
| SA1 | 30% scaling when beginning a combo |
| SA2 (1st hit) | 50% scaling when beginning a combo |
| SA2 (2nd / 3rd hits) | 20% immediate scaling when comboed into |

#### Zangief

| Move | Damage Scaling Notes |
| --- | --- |
| 6HP | 25% scaling when beginning a combo 2 hits of scaling when comboed into (applies to next attack) |
| j.2HP | 2 hits of scaling when comboed into (applies to next attack) e.g. Drive Impact crumple, j.2HP, juggle SA1 |
| 360+P (Meterless) | 10% immediate scaling when comboed into (Stun, DI Crumple, corner PC 3HK) |
| j.360+K | 20% immediate scaling when comboed into |
| j.360+KK | 10% immediate scaling when comboed into |
| 63214K (Close) (Meterless) | 10% immediate scaling when comboed into (Stun, DI Crumple, corner PC 3HK) |
| SA1 | 10% immediate scaling when comboed into |
| SA3 / CA | 10% immediate scaling when comboed into (Stun, DI Crumple, corner PC 3HK) |

## 意味差分

- Capcom eSports BASE は観戦向けの大枠、SuperCombo glossary は community frame-data 用語として詳細分類を説明する。
- 個別 move の補正値は raw / official-supercombo enriched data を確認する。
- SuperCombo Gauges page と SuperCombo Game Data page の system-specific scaling 値は community numeric source なので、公式・実機検証と矛盾する場合はそちらを優先する。

## Exact combo damage の計算注意

Exact damage を問う combo query では、route text をそのまま足し算しない。必ず damaging hit ledger を作る。

- `ODアムネジア`、罠、爆弾、設置、portal、projectile のような delayed hit は、route text で1語しか書かれていなくても複数 hit に展開する。
- `Year1`、`初期`、`patch前` のような version 指定がある場合、current frame-data だけでなく Battle Change の before/after から当時の補正値に戻す。
- Punish Counter、Perfect Parry、Modern damage、Drive Rush、starter / immediate / multiplier scaling、Super Art minimum scaling は別々の column として扱う。
- exact damage を出す前に、`base_damage * condition_multiplier * effective_scaling` と cumulative total を hit ごとに検算する。

事例: [[outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation]] は、JP Year1 初期 `ODアムネジア` route を `立中K Punish Counter`、`OD Amnesia Bomb` x2、`中トルバラン`、`強トリグラフ`、`ヴィーハト爆発`、`ODトリグラフ` 500x2、SA3 minimum 50% に分解し、5790 damage を再計算する。

## 関連

- [[concepts/terms/scaling-reset]]
- [[concepts/terms/perfect-parry]]
- [[concepts/frame-data]]
