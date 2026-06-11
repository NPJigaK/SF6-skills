---
type: concept
concept_type: term
title: "Combo Counter"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-hud]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/hit-confirm]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "combo counter"
  - "コンボカウンター"
  - "コンボ数表示"
tags:
  - sf6
  - terms
  - hud
  - frame-data
---

# Combo Counter

## 要約

Combo Counter は、現在の combo hit 数を HUD 上に表示する cue。SuperCombo HUD page は、攻撃 sequence が true combo かどうかを判断する補助になると説明している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-hud]] | `Combo Counter` は現在の combo hit 数を示し、sequence of attacks が true combo かどうかを判断する補助になる。 | medium |

## 意味差分

- この page は HUD 表示 cue としての Combo Counter を扱う。Combo route の成立条件や damage scaling は、個別技の frame-data output と [[concepts/terms/damage-scaling]] を確認する。

## 関連

- [[concepts/frame-data]]
- [[concepts/terms/hit-confirm]]
- [[concepts/terms/damage-scaling]]
