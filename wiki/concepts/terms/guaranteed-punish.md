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
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/defense]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[concepts/terms/punish-counter]]"
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

確定反撃は、相手の攻撃を guard した後の隙に、相手へ確実に当たる反撃。Capcom eSports BASE は guard 後不利 frame の把握を説明し、SuperCombo Defense page は punish combo route の first attack が追加 hit advantage を得ることを補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-17` | 相手の攻撃を guard した後の隙に確実に hit させられる攻撃。技ごとの guard 後不利 frame を把握することが重要。 | high |
| [[sources/supercombo-street-fighter-6-defense]] | Punish combo route では first attack が `4` extra frames of hit advantage を持つため、通常より強い combo route が開く場合がある。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Punish combo first attack hit advantage bonus | `+4` frames | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] |

## 意味差分

- 確定するかどうかは距離、pushback、発生、range に依存する。この page は用語説明であり、個別 punish 判定は frame-data と状況検証が必要。
- Punish Counter の共通 bonus と個別 punish combo route は分けて扱う。個別 route は starter、距離、cancel、damage scaling に依存する。

## 関連

- [[concepts/defense]]
- [[concepts/frame-data]]
- [[concepts/terms/frame-advantage]]
- [[concepts/terms/punish-counter]]
- [[concepts/terms/invincible-move]]
