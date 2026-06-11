---
type: concept
concept_type: term
title: "Throw"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-offense]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/offense]]"
  - "[[concepts/terms/throw-loop]]"
  - "[[concepts/terms/command-throw]]"
  - "[[concepts/terms/throw-escape]]"
  - "[[concepts/terms/punish-counter]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "throw"
  - "投げ"
  - "通常投げ"
  - "normal throw"
tags:
  - sf6
  - terms
  - offense
  - throws
---

# Throw

## 要約

Throw は、近距離で相手を掴む攻撃。SuperCombo Offense page は、SF6 の通常投げを close range の `LP+LK`、back throw を `4+LP+LK` と説明し、通常投げの startup / active / whiff、throw range、throw invincibility、Punish Counter throw の追加効果を community source fact として示している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-offense]] | 通常投げは close range の `LP+LK`、back throw は `4+LP+LK`。通常投げは `5f` startup、`3f` active、whiff animation `30f` total。 | medium |
| [[sources/supercombo-street-fighter-6-offense]] | 通常投げは grounded opponent にだけ機能し、pre-jump / airborne / hitstun / blockstun / knockdown 中の相手には通常つながらない。同 frame で throw と strike が当たる場合、strike が勝つ。 | medium |
| [[sources/supercombo-street-fighter-6-offense]] | Punish Counter throw は `+70%` damage、Hard Knockdown、相手 Drive Gauge `1` bar drain を得る。Drive Parry に対する throw は常に Punish Counter になる。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Startup | `5f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Active | `3f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Whiff animation | `30f` total | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Backdash throw invincibility | first `15f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Grounded wakeup throw invincibility | `1f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| After hitstun / blockstun throw invulnerability | `2f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Air reset landing recovery throw immunity | `2f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Punish Counter throw damage boost | `+70%` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Punish Counter throw Drive drain | `1` Drive bar | [[sources/supercombo-street-fighter-6-offense#Throws]] |

## Throw range

| Character group | Throw range | Throw hurtbox | Relative throw range |
|---|---:|---:|---:|
| Zangief | `1.02` | `0.49` | `0.53` |
| Marisa | `0.90` | `0.38` | `0.52` |
| Blanka / E. Honda | `0.90` | `0.43` | `0.47` |
| Alex / Sagat | `0.85` | `0.38` | `0.47` |
| Everyone Else | `0.80` | `0.33` | `0.47` |

SuperCombo Offense defines relative throw range as throw range minus throw hurtbox width. These are community numeric source facts, not official Capcom data.

## 意味差分

- [[concepts/terms/command-throw]] は special / command throw を扱い、この page は通常投げを中心に扱う。
- [[concepts/terms/throw-escape]] は throw defense / HUD display cue を扱う。
- Throw range や character-specific throw loop は community source なので、公式 source または実機検証がある場合はそちらを優先する。

## 関連

- [[concepts/offense]]
- [[concepts/terms/throw-loop]]
- [[concepts/terms/command-throw]]
- [[concepts/terms/throw-escape]]
- [[concepts/terms/punish-counter]]
- [[concepts/terms/oki]]
