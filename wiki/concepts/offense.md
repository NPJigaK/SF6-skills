---
type: concept
title: "Offense"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/supercombo-street-fighter-6-offense]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/throw]]"
  - "[[concepts/terms/throw-loop]]"
  - "[[concepts/terms/safe-jump]]"
  - "[[concepts/terms/empty-jump-mixup]]"
  - "[[concepts/terms/blockstring]]"
  - "[[concepts/terms/oki]]"
  - "[[concepts/terms/meaty]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "攻め"
  - "SF6 offense"
  - "スト6 攻め"
tags:
  - sf6
  - mechanics
  - offense
---

# Offense（攻め）

## 要約

Offense は、相手に guard / hit / wake-up / corner / resource pressure を迫って damage または有利状況を作る行動群。Capcom eSports BASE は起き攻め、重ね、セットプレイ、shimmy、hit confirm などを観戦用語として説明する。SuperCombo Offense page は community source として、通常投げ、throw loop、counter / punish counter、corner dizzy follow-up、combo / blockstring、safe jump、empty jump mixup、kara defensive bait の timing と実戦上の使い分けを補う。

## 定義

この wiki では、Offense を次の入口として扱う。

- 投げ / strike-throw: [[concepts/terms/throw]]、[[concepts/terms/throw-loop]]、[[concepts/terms/command-throw]]、[[concepts/terms/shimmy]]
- Wake-up pressure: [[concepts/terms/oki]]、[[concepts/terms/meaty]]、[[concepts/terms/setplay]]、[[concepts/terms/safe-jump]]、[[concepts/terms/empty-jump-mixup]]
- Hit / guard sequencing: [[concepts/terms/blockstring]]、[[concepts/terms/cancel]]、[[concepts/terms/chain]]、[[concepts/terms/hit-confirm]]
- Reward states: [[concepts/terms/counter-hit]]、[[concepts/terms/punish-counter]]、[[concepts/terms/stun]]、[[concepts/terms/damage-scaling]]
- Drive-linked offense: [[concepts/terms/raw-drive-rush]]、[[concepts/terms/drive-rush-cancel]]、[[concepts/terms/drive-impact]]、[[concepts/drive-system]]

## なぜ重要か

攻めの説明は、frame advantage、throw invincibility、wake-up timing、Drive meter、counter state、damage scaling を横断する。個別技の frame-data だけでは、throw loop、safe jump、empty jump、blockstring、corner stun follow-up のような攻め継続の理由を説明しにくい。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| 起き攻めは相手の起き上がり timing に攻めを仕掛け、打撃重ね、投げ、表裏などで選択肢を迫る。 | [[sources/capcom-esports-base-terms]] | high |
| SuperCombo Offense page は、通常投げを `5f` startup、`3f` active、whiff animation `30f` total とし、投げは pre-jump / airborne / hitstun / blockstun / knockdown 中の相手には通常つながらないと説明する。 | [[sources/supercombo-street-fighter-6-offense#Throws]] | medium |
| SuperCombo Offense page は、throw loop を、投げ後の frame advantage から相手 wake-up にもう一度 meaty throw を迫る community term と説明する。 | [[sources/supercombo-street-fighter-6-offense#Throws]] | medium |
| Counter-hit / Punish Counter は攻めの reward state として combo route や punish route を変える。一般値は公式 source を優先し、throw-specific Punish Counter や tactical context は Offense page を補助 source とする。 | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-offense#Counter / Punish Counter]] | high / medium |
| Corner Dizzy では、Burnout 中の corner Drive Impact stun 後に、Drive regeneration のために歩く、または character-specific stock / setup を作る選択がある。 | [[sources/supercombo-street-fighter-6-offense#Section summary]], [[sources/supercombo-street-fighter-6-gauges#Burnout]] | medium |
| Safe jump は knockdown timing によって jump attack を wake-up に重ね、landing 後に reversal を guard できる setup として説明される。 | [[sources/supercombo-street-fighter-6-offense#Combo / blockstring / safe jump values]] | medium |
| Empty jump mixup は safe jump に似た見た目で、着地投げや低打撃を迫るが、invincible reversal には安全ではない。 | [[sources/supercombo-street-fighter-6-offense#Combo / blockstring / safe jump values]] | medium |

## 数値索引

この section は回答時に source page へ戻るための入口。値は SuperCombo Offense の community source fact なので、公式 source または実機検証と重なる場合はそちらを優先する。

| 領域 | 主要値 | 詳細 |
|---|---|---|
| Normal throw | startup `5f`, active `3f`, whiff animation `30f`; PC throw `+70%` damage / Hard Knockdown / `1` Drive bar drain | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Throw invincibility | grounded wakeup `1f`; after hitstun / blockstun `2f`; air reset landing recovery `2f`; backdash first `15f` | [[sources/supercombo-street-fighter-6-offense#Throws]] |
| Throw range | Zangief `1.02 / 0.49 / 0.53`; Marisa `0.90 / 0.38 / 0.52`; Blanka / E. Honda `0.90 / 0.43 / 0.47`; Alex / Sagat `0.85 / 0.38 / 0.47`; others `0.80 / 0.33 / 0.47` | [[sources/supercombo-street-fighter-6-offense#Throw range table]] |
| Counter state | Counter-hit `+2` / `20%`; Punish Counter `+4` / `20%`; throw Punish Counter `+70%` / Hard Knockdown / Drive drain `1` | [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-offense#Counter / Punish Counter]] |
| Combo / link timing | input buffer generally `4f`; tightest links have `5f` input timing | [[sources/supercombo-street-fighter-6-offense#Combo / blockstring / safe jump values]] |
| Safe jump | standard `45f` jump: `+42` vs 5f anti-air, `+41` vs 6f reversal; slow jump characters need more | [[sources/supercombo-street-fighter-6-offense#Combo / blockstring / safe jump values]] |
| Empty jump | `+45` or slightly better knockdown advantage can threaten immediate throw or `5f` `2LK` while safe from immediate `4f` buttons | [[sources/supercombo-street-fighter-6-offense#Combo / blockstring / safe jump values]] |
| Advanced bait | kara-Parry at `0` on hit/block; kara-DP/Super from `+11` into immediate Drive Rush button | [[sources/supercombo-street-fighter-6-offense#Combo / blockstring / safe jump values]] |

## 関連

- [[concepts/terms/throw]]
- [[concepts/terms/throw-loop]]
- [[concepts/terms/safe-jump]]
- [[concepts/terms/empty-jump-mixup]]
- [[concepts/terms/blockstring]]
- [[concepts/terms/oki]]
- [[concepts/terms/meaty]]
- [[concepts/terms/setplay]]
- [[concepts/terms/counter-hit]]
- [[concepts/terms/punish-counter]]
- [[concepts/drive-system]]
- [[concepts/frame-data]]

## 矛盾 / 注意点

- SuperCombo Offense は community source なので、公式 Capcom source と重なる一般 mechanics では公式 source を優先する。
- Character-specific throw loop notes は matchplay / lab knowledge の要素が強く、公式 frame-data と同じ confidence では扱わない。
- Safe jump / empty jump values は setup の前提、jump duration、landing timing、defender options に依存する。数値だけで成立を断定しない。
- Corner Dizzy の character-specific stock examples は current patch の source fact として保持するが、patch 後に stale になる可能性がある。

## 未解決の質問

- Throw range / safe jump / throw loop の数値を公式 source または実機検証で照合するか。
- Offense と Defense / Movement / Game Data を同じ system-page family として順次 ingest し、攻防の source graph をそろえるか。
- Character-specific throw loop notes を character entity / character source page に backlink する粒度をどうするか。
