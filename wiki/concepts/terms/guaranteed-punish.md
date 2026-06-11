---
type: concept
concept_type: term
title: "確定反撃"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-defense]]"
  - "[[sources/supercombo-street-fighter-6-game-data]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/defense]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[concepts/terms/punish-counter]]"
  - "[[concepts/range-comparisons]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "guaranteed punish"
  - "punish"
  - "確反"
  - "確定"
  - "かくていはんげき"
tags:
  - sf6
  - terms
  - frame-data
---

# 確定反撃

## 要約

確定反撃は、相手の攻撃を guard した後の隙に、相手へ確実に当たる反撃。Capcom eSports BASE は guard 後不利 frame の把握を説明し、SuperCombo Defense page は punish combo route の first attack が追加 hit advantage を得ることを補う。SuperCombo Game Data page は Longest Punish `≤4F` table を提供し、距離込みの確反候補検索に使える community numeric source になる。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-17` | 相手の攻撃を guard した後の隙に確実に hit させられる攻撃。技ごとの guard 後不利 frame を把握することが重要。 | high |
| [[sources/supercombo-street-fighter-6-defense]] | Punish combo route では first attack が `4` extra frames of hit advantage を持つため、通常より強い combo route が開く場合がある。 | medium |
| [[sources/supercombo-street-fighter-6-game-data]] | Longest Punish Option `≤4F` tab は character ごとの 4F 確反候補、range、notes を保持する。`≤5F` から `≤12F` tabs は source 上で `(to-do)`。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Punish combo first attack hit advantage bonus | `+4` frames | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] |
| Longest Punish Option tabber coverage | `≤4F` table only; `≤5F`..`≤12F` are source `(to-do)` | [[sources/supercombo-street-fighter-6-game-data]]; `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` table `38` |

### Longest Punish Option at Each Frame Disadvantage: ≤4F

| Character | Button | Range | Notes |
| --- | --- | --- | --- |
| Zangief | 2LK | 1.39 | Only +4 on PC, no extra reward beyond Light chains |
| E. Honda | 2LP | 1.23 | At meterless max range, can only cancel into Headbutt or MP Hands |
| Sagat | 2LP | 1.20 | At meterless max range, can only cancel into MK Tiger Nexus; slightly closer gives 5LK > MP Uppercut |
| Marisa | 2LP | 1.17 | At meterless max range, can only cancel into LP Dimachaerus; slightly closer gives 2MP > LK Quadriga, or 5MP~MP when closer |
| Luke | 2LP | 1.14 | At meterless max range, can only cancel into LP/MP Flash Knuckle or link 5MK; slightly closer gives 2MK |
| Blanka | 5LK | 1.11 | At meterless max range, can only cancel into Electricity or MP Roll; slightly closer gives 5MK |
| Rashid | 5LP | 1.11 | At meterless max range, can only link 5MK or cancel into LK Eagle Spike or LP/MP Spinning Mixer; slightly closer gives 2MK |
| M. Bison | 5LK | 1.10 | Links to 2MP even at max range (2LP punish is more rewarding if closer) |
| Manon | 2LP | 1.09 | At meterless max range, can only cancel into any Rond-point (236K) or LK/MK Dégagé (214K); slightly closer gives 5MP |
| Elena | 2LP | 1.07 | Links to 5MP/2MP/2MK even at max range |
| JP | 2LP | 1.07 | Links to 5MK even at max range (a direct cancel to MP Stribog also works well vs. extended hurtbox punish) |
| Cammy | 5LP/2LP | 1.05 | Links to 5HP/2MK even at max range |
| Chun-Li | 5LP | 1.05 | Links to 2MK/4MP even at max range |
| A.K.I. | 5LK | 1.04 | Links to 5MP/2MP even at max range |
| Dee Jay | 5LP | 1.04 | At max range, cancels to MK/HK Sobat, links to 2HP/2MK, or chains to 5LP~MK~MK; must be close for a more substantial punish |
| Guile | 2LP | 1.03 | Links to 4HP/2HK even at max range; direct cancel to HK Flash Kick is often easier/better |
| Mai | 2LP | 1.03 | Links to 5MP/2MK even at max range (2LP punish is more rewarding into 5HP if closer) |
| Akuma | 5LP | 1.02 | Links to 2MK even at max range (2LP punish is more rewarding into 5HP if closer) |
| Ed | 2LP | 1.02 | Not cancelable; at ranges where 2LP is required over 5LP, Ed can only link into 5LK~LK~LK 5LP has 0.92 Range; can always link into 2MP, and gets 5MP~HP at farther ranges than 2LP |
| C. Viper | 5LP | 1.01 | Links to 5MK/2MK even at max range (2LP punish is more rewarding into 2HP if closer) |
| Ken | 5LP | 1.01 | Links to 5MK/2MK/2HK even at max range |
| Kimberly | 2LP | 1.01 | Links to 5MK/2HK even at max range; 2MP/5MP require closer range punish |
| Ryu | 5LP | 1.01 | Links to 2MK even at max range |
| Terry | 5LP | 1.01 | Links to 5MP/2MK~2HK even at max range |
| Jamie | 2LP | 0.98 | Links to 5MK/2MK/2HK even at max range |
| Juri | 2LP | 0.92 | Links to 2MK/6MP even at max range |
| Dhalsim | 5LP | 0.88 | At meterless max range, can only cancel into LP Yoga Flame; slightly closer gives 4MK > MP Yoga Flame |
| Lily | 5LK | 0.82 | Links to 2MK even at max range (into LK Spire / HP Tomahawk / Windclad HK Spire) |

## 意味差分

- 確定するかどうかは距離、pushback、発生、range に依存する。この page は用語説明であり、個別 punish 判定は frame-data と状況検証が必要。
- Punish Counter の共通 bonus と個別 punish combo route は分けて扱う。個別 route は starter、距離、cancel、damage scaling に依存する。

## 関連

- [[concepts/defense]]
- [[concepts/frame-data]]
- [[concepts/terms/frame-advantage]]
- [[concepts/terms/punish-counter]]
- [[concepts/terms/invincible-move]]
- [[concepts/range-comparisons]]
