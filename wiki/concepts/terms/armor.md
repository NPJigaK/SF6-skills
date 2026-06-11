---
type: concept
concept_type: term
title: "Armor"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-defense]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/defense]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/drive-impact]]"
  - "[[concepts/terms/drive-reversal]]"
  - "[[concepts/terms/armor-break]]"
  - "[[concepts/terms/invincible-move]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "armor"
  - "armored move"
  - "armor absorption"
  - "アーマー"
tags:
  - sf6
  - terms
  - defense
  - drive-system
---

# Armor

## 要約

Armor は、strike / projectile を受け止めながら動作を続ける defensive property。SuperCombo Defense page は、armor が throw に負け、吸収した damage の一部を recoverable damage として受け、Armor Break property で破られると説明している。SuperCombo Gauges page は Drive Impact の armor hit 数や hit-freeze を community numeric source として補う。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-defense]] | Drive Impact や一部 special moves は armor を持ち、strikes / projectiles を吸収できるが、any Throw は armored move に勝つ。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Armor で攻撃を吸収すると、その move の normal damage `50%` を recoverable damage として受ける。Low health では K.O. され得る。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Super Arts や Drive Reversals のような Armor Break property は armor absorption を防ぐ。 | medium |
| [[sources/supercombo-street-fighter-6-gauges]] | Drive Impact は `2` armor hits を持ち、projectile armor hit-freeze は `6f`、absorb 後 startup は `+1f` と説明する。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Armor absorbed damage | normal damage の `50%` recoverable damage | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] |
| Drive Impact armor hits | `2` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]] |
| Projectile armor hit-freeze | `6f` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]] |
| Startup after absorb | `+1f` | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]] |

## 意味差分

- Armor は [[concepts/terms/invincible-move]] とは違う。攻撃を受けないのではなく、受け止めながら damage / recoverable damage を受ける。
- [[concepts/terms/armor-break]] は HUD 表示 cue と armor を破る property の説明。この page は armor property そのものを扱う。
- Throw は armor に勝つため、armor move は strike / projectile 対策であって throw 対策ではない。

## 関連

- [[concepts/defense]]
- [[concepts/drive-system]]
- [[concepts/terms/drive-impact]]
- [[concepts/terms/drive-reversal]]
- [[concepts/terms/armor-break]]
- [[concepts/terms/invincible-move]]
