---
type: concept
title: "Defense"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/supercombo-street-fighter-6-defense]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/offense]]"
  - "[[concepts/terms/blocking]]"
  - "[[concepts/terms/throw-escape]]"
  - "[[concepts/terms/drive-parry]]"
  - "[[concepts/terms/wake-up]]"
  - "[[concepts/terms/reversal]]"
  - "[[concepts/terms/armor]]"
  - "[[concepts/terms/anti-air]]"
  - "[[concepts/terms/guaranteed-punish]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "守り"
  - "SF6 defense"
  - "スト6 守り"
tags:
  - sf6
  - mechanics
  - defense
---

# Defense（守り）

## 要約

Defense は、相手の offense に対して damage、position loss、resource loss を抑え、neutral または有利状況へ戻すための行動群。Capcom 公式 source は Drive Parry、Drive Reversal、Drive Impact、無敵技、対空などの基礎 mechanics / terms を提供する。SuperCombo Defense page は community source として、blocking、throw escape、wake-up、reversal buffer、armor、anti-air、punish route の timing と実戦上の注意点を補う。

## 定義

この wiki では、Defense を次の入口として扱う。

- Guard / block: [[concepts/terms/blocking]]、[[concepts/terms/blockstring]]
- Throw defense: [[concepts/terms/throw-escape]]、[[concepts/terms/shimmy]]、[[concepts/terms/throw]]
- Drive-linked defense: [[concepts/terms/drive-parry]]、[[concepts/terms/perfect-parry]]、[[concepts/terms/drive-reversal]]、[[concepts/terms/drive-impact]]
- Wake-up / reversal: [[concepts/terms/wake-up]]、[[concepts/terms/reversal]]、[[concepts/terms/invincible-move]]、[[concepts/terms/meaty]]
- Strike / jump defense: [[concepts/terms/armor]]、[[concepts/terms/anti-air]]、[[concepts/terms/cross-up]]
- Punish conversion: [[concepts/terms/guaranteed-punish]]、[[concepts/terms/punish-counter]]、[[concepts/frame-data]]

## なぜ重要か

守りの説明は、guard direction、throw tech window、wake-up timing、reversal buffer、invincibility、armor、Drive Gauge、Punish Counter / punish route を横断する。個別技の frame-data だけでは、なぜ block できないか、どの timing で reversal が出るか、throw escape や anti-air の失敗条件が何かを説明しにくい。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| Drive Parry は相手攻撃を自動で guard し、guard 時に Drive Gauge が回復する。タイミングよく受けると Perfect Parry になる。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| めくりに対して Drive Parry は表裏両方に対応し得る defensive option として説明される。 | [[sources/capcom-esports-base-terms]] | high |
| 無敵技は不利状況を切り返せるが、外れると大きな隙になる high-risk な defensive option として説明される。 | [[sources/capcom-esports-base-terms]] | high |
| 対空は空中の相手を迎撃する行動で、通常技、必殺技、空対空、parry 対空などがある。 | [[sources/capcom-esports-base-terms]] | high |
| SuperCombo Defense page は、blocking は相手から離れる方向入力で行い、空中や自分の recovery 中はできないと説明する。 | [[sources/supercombo-street-fighter-6-defense#Blocking]] | medium |
| SuperCombo Defense page は、throw escape は grounded normal throw に対して `LP+LK` で行い、success 時に `5000` Drive / `1/2` bar を得ると説明する。 | [[sources/supercombo-street-fighter-6-defense#Throw Escape]] | medium |
| SuperCombo Defense page は、Normal Rise と Back Rise で knockdown frame advantage に差はなく、Hard Knockdown は Back Rise を防ぐと説明する。 | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] | medium |
| SuperCombo Defense page は、wake-up reversal buffer を `10f`、hitstun / blockstun / air reset 後を `4f` とし、true reversal frame を含めてそれぞれ total `11f` / `5f` window と説明する。 | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] | medium |
| SuperCombo Defense page は、armor は strike / projectile を吸収するが throw に負け、absorbed attack の `50%` normal damage を recoverable damage として受けると説明する。 | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] | medium |
| SuperCombo Defense page は、punish combo の first attack には `4` extra frames of hit advantage があるため、通常より強い route が開く場合があると説明する。 | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] | medium |

## 数値索引

この section は回答時に source page へ戻るための入口。値は SuperCombo Defense の community source fact なので、公式 source または実機検証と重なる場合はそちらを優先する。

| 領域 | 主要値 | 詳細 |
|---|---|---|
| Throw escape | input `LP+LK`; success gain `5000` Drive / `1/2` bar; window は thrown state `9th` frame まで | [[sources/supercombo-street-fighter-6-defense#Throw Escape]] |
| Wake-up | Back Rise は landing 時 2 buttons; Normal / Back Rise で knockdown frame advantage 差なし; Hard Knockdown は Back Rise 不可 | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Forced standing | wake-up crouch animation は `4f` forced standing、hurtbox shrink frame `5`; air reset landing は `2` forced standing frames | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Reversal buffer | wake-up `10f` buffer / total `11f`; hitstun, blockstun, air reset 後 `4f` buffer / total `5f`; dash buffer intended `7f` | [[sources/supercombo-street-fighter-6-defense#Wake-up / reversal timing]] |
| Armor | absorbed damage は normal damage の `50%` recoverable damage; any Throw beats armor | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] |
| Punish route | punish combo first attack gets `4` extra frames of hit advantage | [[sources/supercombo-street-fighter-6-defense#Armor / punish]] |

## 関連

- [[concepts/terms/blocking]]
- [[concepts/terms/throw-escape]]
- [[concepts/terms/drive-parry]]
- [[concepts/terms/wake-up]]
- [[concepts/terms/reversal]]
- [[concepts/terms/armor]]
- [[concepts/terms/anti-air]]
- [[concepts/terms/guaranteed-punish]]
- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[concepts/offense]]

## 矛盾 / 注意点

- SuperCombo Defense は community source なので、公式 Capcom source と重なる mechanics では公式 source を優先する。
- Wake-up forced standing、reversal buffer、throw escape option-select restriction、dash buffer bug などは lab / community tactical claim として扱い、公式値として断定しない。
- Blocking / cross-up / proximity guard は spacing、hurtbox、corner、recording input に依存する。source page の note は実機検証時の注意として保持する。
- Armor は true invincibility とは違う。Armor が吸収した damage は recoverable damage になり、low health では K.O. され得る。

## 未解決の質問

- Throw escape / reversal buffer / wake-up crouch block の数値を公式 source または実機検証で照合するか。
- Defense と Offense を横断して strike / throw / shimmy / reversal / parry の defensive decision tree を synthesis にするか。
- Defense page の small numeric facts を今後 `wiki/outputs/data/` へ派生する基準をどうするか。
