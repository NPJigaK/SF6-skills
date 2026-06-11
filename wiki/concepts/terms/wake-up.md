---
type: concept
concept_type: term
title: "Wake-up"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-defense]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/defense]]"
  - "[[concepts/offense]]"
  - "[[concepts/terms/oki]]"
  - "[[concepts/terms/meaty]]"
  - "[[concepts/terms/reversal]]"
  - "[[concepts/terms/hard-knockdown]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "wake up"
  - "okizeme defense"
  - "Normal Rise"
  - "Back Rise"
  - "起き上がり"
  - "受け身"
tags:
  - sf6
  - terms
  - defense
  - frame-data
---

# Wake-up

## 要約

Wake-up は、knockdown から起き上がって再行動可能になる局面。SuperCombo Defense page は、Normal Rise / Back Rise、Hard Knockdown、wake-up crouch transition、air reset landing の forced standing frames を community source fact として説明している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/supercombo-street-fighter-6-defense]] | SF6 の wake-up には Normal Rise と Back Rise があり、knockdown frame advantage に差はない。距離が保たれる限り meaty setup は影響を受けない。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Landing 時に 2 buttons を hold / input すると Back Rise、そうでなければ Normal Rise になる。Hard Knockdown は Back Rise を防ぐ。 | medium |
| [[sources/supercombo-street-fighter-6-defense]] | Wake-up の crouch animation は最初 `4f` が forced standing で、hurtbox shrink は frame `5`。Air reset 後は landing frame 自体を除いて `2` forced standing frames。 | medium |
| [[sources/supercombo-street-fighter-6-hud]] | `Hard Knockdown` は、2HK や Punish Counter Throw など、相手の Back Rising を防ぐ knockdown 後に表示される。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Wake-up forced standing before crouch hurtbox shrink | `4f`; hurtbox shrinks on frame `5` | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Air reset forced standing | `2f`, landing frame excluded | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |

## 意味差分

- [[concepts/terms/oki]] は attacker 側の wake-up pressure、[[concepts/terms/wake-up]] は defender 側の rising state と defensive timing を扱う。
- Hard Knockdown は Back Rise を防ぐが、すべての knockdown が Hard Knockdown ではない。個別状況は source と frame-data を確認する。
- Source の wake-up crouch block note は lab setup に依存する。Training Mode dummy の `Crouch + Block` は wake-up crouch block の再現として不十分だと source は注意している。

## 関連

- [[concepts/defense]]
- [[concepts/offense]]
- [[concepts/terms/oki]]
- [[concepts/terms/meaty]]
- [[concepts/terms/reversal]]
- [[concepts/terms/hard-knockdown]]
