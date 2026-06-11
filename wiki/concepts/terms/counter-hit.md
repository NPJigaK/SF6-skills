---
type: concept
concept_type: term
title: "Counter-hit"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-offense]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/offense]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[concepts/terms/punish-counter]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "counter hit"
  - "Counter Hit"
  - "カウンターヒット"
  - "CH"
tags:
  - sf6
  - terms
  - hud
  - frame-data
---

# Counter-hit

## 要約

Counter-hit は、相手の攻撃の startup または active frames へ攻撃を当てた時の counter state。Capcom eSports BASE は Counter-hit による damage / advantage 増加を説明し、SuperCombo HUD / Offense pages は startup / active への割り込みと、攻撃同士の trade では両者が Counter-hit になることを説明している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-10` | Counter は相手の技の出掛かりに hit した時に発生し、通常 hit より damage 1.2 倍、+2 advantage 増加になる。 | high |
| [[sources/supercombo-street-fighter-6-hud]] | `Counter-hit` は相手攻撃の startup または active frames を interrupt した時に表示される。攻撃同士が trade した場合は両者が Counter-hit を得る。 | medium |
| [[sources/supercombo-street-fighter-6-offense]] | Counter-hit は相手の startup または active frames 中に strike した時に発生し、trade では両者が Counter-hit になる。`+2` frame advantage と `20%` extra damage を得るが、knockdown は通常追加の knockdown advantage を得ないと説明する。 | medium |

## 意味差分

- Capcom eSports BASE は公式観戦用語 source。SuperCombo HUD は表示 cue、SuperCombo Offense は tactical / timing context の community source として扱う。
- Advantage / damage の一般値は Capcom eSports BASE を優先する。SuperCombo Offense の `+2` / `20%` は一致する補助 claim として保持する。

## 関連

- [[concepts/frame-data]]
- [[concepts/offense]]
- [[concepts/terms/frame-advantage]]
- [[concepts/terms/punish-counter]]
