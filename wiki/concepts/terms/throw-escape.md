---
type: concept
concept_type: term
title: "Throw Escape"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-defense]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/defense]]"
  - "[[concepts/terms/throw]]"
  - "[[concepts/terms/shimmy]]"
  - "[[concepts/terms/punish-counter]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "throw escape"
  - "Throw Tech"
  - "throw tech"
  - "投げ抜け"
  - "投げ抜け表示"
tags:
  - sf6
  - terms
  - hud
  - defense
---

# Throw Escape

## 要約

Throw Escape は、grounded normal throw を tech して damage を防ぐ防御行動であり、成功時に出る HUD 表示 cue。SuperCombo HUD page は表示名を、SuperCombo Defense page は input、tech window、Drive gain、tech できない状況を説明している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-hud]] | `Throw Escape` は Throw に対する防御が成功した時に表示され、`Throw Tech` とも呼ばれる。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Throw 接続直後に `LP+LK` を押すと grounded normal throw を escape / tech できる。Command grabs と air throws はこの方法で防げない。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Throw Escape 成功時は damage を防ぎ、相手を押し離し、defender が `5000` Drive Gauge / `1/2` bar を得る。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Throw Escape window は throw 接続 frame を含む thrown state の `9th` frame まで。DR movement frames 中に接続した throw は Counter-hit 扱いになり、escape できない。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Defender Drive gain on successful Throw Escape | `5000` Drive / `1/2` bar | [[sources/supercombo-street-fighter-6-defense#Throw Escape]] |
| Throw Escape input window | thrown state の `9th` frame まで | [[sources/supercombo-street-fighter-6-defense#Throw Escape]] |

## 意味差分

- Capcom eSports BASE の [[concepts/terms/shimmy]] は、throw tech whiff を誘って punish する崩しを説明している。この page は Throw Escape の成功時 cue と defensive input / timing を扱う。
- Throw Escape が可能かどうかは throw type と接続時の state に依存する。Command grab、air throw、DR movement throw などを通常投げと混同しない。

## 関連

- [[concepts/defense]]
- [[concepts/terms/throw]]
- [[concepts/terms/shimmy]]
- [[concepts/terms/punish-counter]]
