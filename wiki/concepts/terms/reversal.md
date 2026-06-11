---
type: concept
concept_type: term
title: "Reversal"
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
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/wake-up]]"
  - "[[concepts/terms/invincible-move]]"
  - "[[concepts/terms/drive-reversal]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "reversal"
  - "リバーサル"
  - "最速リバーサル"
tags:
  - sf6
  - terms
  - hud
  - defense
---

# Reversal

## 要約

Reversal は、hitstun、blockstun、knockdown、air reset などの行動不能明けに、最速 timing で攻撃を出す defensive timing / HUD 表示 cue。SuperCombo HUD page は表示 cue を、SuperCombo Defense page は wake-up と hitstun / blockstun / air reset 後の input buffer を説明している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-hud]] | `Reversal` は、hitstun、blockstun、knockdown、air reset 後の最速可能 timing で Special または Super move を入力した時に表示される。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Wake-up または hitstun / blockstun 明け直前に attack を入力すると Reversal として buffer でき、timing が取りやすくなる。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Wake-up reversal buffer は `10f`、hitstun / blockstun / air reset 後は `4f`。True reversal frame を含めると total window は wake-up `11f`、その他 `5f`。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Drive Parry は reversal buffer で Perfect Parry にはならず、攻撃が接続する瞬間に正確に timed する必要がある。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Wake-up reversal buffer | `10f`; true reversal frame 含め total `11f` | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Hitstun / blockstun / air reset reversal buffer | `4f`; true reversal frame 含め total `5f` | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Dash buffer | intended `7f`; source は一部 bugged case を note | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |

## 意味差分

- `Reversal` は HUD 表示 cue、[[concepts/terms/drive-reversal]] は Drive System の固有行動。名前は似ているが同一 term として扱わない。
- Reversal 表示が出ても、その行動が無敵技かどうかは別問題。個別技の invincibility は frame-data source を確認する。
- Source の dash buffer bug note は community observation として扱い、個別状況では実機検証する。

## 関連

- [[concepts/defense]]
- [[concepts/frame-data]]
- [[concepts/terms/wake-up]]
- [[concepts/terms/invincible-move]]
- [[concepts/terms/drive-reversal]]
