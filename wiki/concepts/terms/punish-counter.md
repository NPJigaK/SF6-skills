---
type: concept
concept_type: term
title: "パニッシュカウンター"
created: 2026-06-10
updated: 2026-06-11
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-offense]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/offense]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[concepts/terms/counter-hit]]"
  - "[[concepts/terms/hard-knockdown]]"
  - "[[concepts/terms/throw]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Punish Counter"
  - "punish counter"
  - "パニカン"
  - "ぱにっしゅかうんたー"
tags:
  - sf6
  - terms
  - frame-data
  - hud
---

# パニッシュカウンター

## 要約

パニッシュカウンターは、相手の技の戻り際など大きな隙へ攻撃を当てた時の counter state。Capcom eSports BASE は、通常 hit より damage が増え、有利 frame も増えるため、通常ではつながらない combo が可能になると説明している。SuperCombo HUD page は表示 cue を、SuperCombo Offense page は recovery への punish、特殊な move properties、Punish Counter throw の追加効果を説明している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-10` | 出掛かりに hit すると counter、戻り際に hit すると punish counter。どちらも通常 hit より damage 1.2 倍。counter は +2、punish counter は +4 の advantage 増加。punish counter は相手の Drive Gauge も削る。 | high |
| [[sources/supercombo-street-fighter-6-hud]] | `Punish Counter` icon は、相手攻撃の recovery frames を punish した時に表示される。 | medium |
| [[sources/supercombo-street-fighter-6-offense]] | Punish Counter は相手 recovery frames への攻撃で発生し、`+4` frame advantage、`20%` extra damage、Drive meter depletion を得る。通常投げも Punish Counter になり、`+70%` damage、Hard Knockdown、相手 Drive Gauge `1` bar drain を得る。 | medium |

## 数値データ

| 条件 | 値 | 根拠 |
|---|---:|---|
| General Punish Counter advantage | `+4` | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-offense#Counter / Punish Counter]] |
| General Punish Counter damage | `1.2x` / `20%` extra | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-offense#Counter / Punish Counter]] |
| Punish Counter throw damage boost | `+70%` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Punish Counter throw Drive drain | `1` Drive bar | [[sources/supercombo-street-fighter-6-offense#Throws]] |

## 意味差分

- 個別技ごとの Punish Counter 時効果は frame-data output に依存する。この page は共通用語としての説明に留める。
- SuperCombo HUD page は表示 cue の説明であり、advantage / damage 数値は Capcom eSports BASE source を優先する。
- SuperCombo Offense page の Punish Counter throw 追加効果は community source fact として保持する。公式 source または実機検証がある場合はそちらを優先する。

## 関連

- [[concepts/frame-data]]
- [[concepts/offense]]
- [[concepts/terms/frame-advantage]]
- [[concepts/terms/counter-hit]]
- [[concepts/terms/whiff-punish]]
- [[concepts/terms/shimmy]]
- [[concepts/terms/hard-knockdown]]
- [[concepts/terms/throw]]
