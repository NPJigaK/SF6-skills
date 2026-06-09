---
type: concept
title: "Drive System"
created: 2026-05-26
updated: 2026-06-10
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/burnout]]"
  - "[[concepts/terms/drive-impact]]"
  - "[[concepts/terms/drive-parry]]"
  - "[[concepts/terms/drive-reversal]]"
  - "[[concepts/terms/drive-rush-cancel]]"
  - "[[concepts/terms/overdrive]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "ドライブシステム"
  - "Drive System"
tags:
  - mechanics
---

# Drive System（ドライブシステム）

## 要約

Drive System は、Street Fighter 6 の攻撃・防御・移動を横断する共通 system。Capcom 公式 Fighting Ground source では、Drive Gauge はバトル開始時から使用でき、使いすぎると枯渇状態や [[concepts/terms/burnout|バーンアウト]] に関わる resource として説明されている。Capcom 公式 eSports BASE 用語解説は、[[concepts/terms/chip-damage|削り]]、[[concepts/terms/stun|スタン]]、[[concepts/terms/raw-drive-rush|生ラッシュ]]、[[concepts/terms/drive-impact-counter|インパクト返し]]、[[concepts/terms/perfect-parry|ジャストパリィ]]などの観戦用語として Drive System 周辺の具体例を補う。

## 定義

Capcom 公式 Fighting Ground source は `DRIVE GAUGE` と `COMMON SYSTEM` として [[concepts/terms/drive-impact|Drive Impact]]、[[concepts/terms/drive-parry|Drive Parry]]、[[concepts/terms/overdrive|Overdrive]]、Drive Rush、[[concepts/terms/drive-reversal|Drive Reversal]] を説明している。Capcom 公式 eSports BASE は観戦用語として、Burnout 中の [[concepts/terms/chip-damage|削り]]、Burnout 中の Drive Impact による [[concepts/terms/stun|stun]]、Drive Parry から出す [[concepts/terms/raw-drive-rush|生ラッシュ]]、Drive Impact への [[concepts/terms/drive-impact-counter|インパクト返し]]、[[concepts/terms/perfect-parry|ジャストパリィ]] を説明している。SuperCombo glossary は community source として Burnout、Drive Impact、Drive Parry、Drive Reversal、Drive Rush、Drive System、Overdrive を列挙している。

## なぜ重要か

Drive System は movement、offense、defense、resource exhaustion を横断するため、後続の frame-data 解釈、combo route、matchup explanation の前提になる。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| Drive Gauge はバトル開始時から使用可能な Drive System の核心として説明されている。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| Drive Gauge が 0 になると [[concepts/terms/burnout|バーンアウト]] 状態になり、回復するまで Drive System を利用する技は一時的に使用できなくなる。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| Guard 時には Drive Gauge が削られ、Burnout 中に必殺技を guard すると体力が削られ、[[concepts/terms/chip-damage|削り K.O.]] も可能になる。 | [[sources/capcom-esports-base-terms]] | high |
| Burnout 中に Drive Impact を guard して [[concepts/terms/corner|画面端]] に到達すると [[concepts/terms/stun|stun]] 状態になり、stun 後は Burnout 状態が解除される。 | [[sources/capcom-esports-base-terms]] | high |
| Drive Rush は [[concepts/terms/drive-parry|Drive Parry]] の構え、または cancel 可能な通常技から出せる。Drive Parry からはコスト 1、通常技からはコスト 3。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| [[concepts/terms/raw-drive-rush|生ラッシュ]] は Drive Parry の構えを cancel して出す Drive Rush、[[concepts/terms/drive-rush-cancel|キャンセルラッシュ]] は通常技を cancel して出す Drive Rush として説明される。 | [[sources/capcom-esports-base-terms]] | high |
| [[concepts/terms/drive-impact|Drive Impact]]、[[concepts/terms/drive-parry|Drive Parry]]、[[concepts/terms/overdrive|Overdrive]]、[[concepts/terms/drive-reversal|Drive Reversal]] は公式 Fighting Ground source の Common System として説明されている。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| [[concepts/terms/drive-impact-counter|インパクト返し]] は Drive Impact に Drive Impact を打ち返す対策として説明される。 | [[sources/capcom-esports-base-terms]] | high |
| [[concepts/terms/perfect-parry|ジャストパリィ]] は 2 frame window の parry timing で、成功後は反撃に向けた有利時間が増えるが、後続 combo に 50% damage scaling がかかると説明される。 | [[sources/capcom-esports-base-terms]] | high |
| Drive System は universal movement、offense、defense mechanics への gateway となる meter として説明されている。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Burnout は Drive gauge が空になった時の状態で、Drive-related techniques に制限がかかる。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Drive Rush は Drive Parry または cancelable normal attack から出せる。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |

## 関連

- [[concepts/frame-data]]
- [[concepts/terms/index]]
- [[concepts/terms/burnout]]
- [[concepts/terms/drive-impact]]
- [[concepts/terms/drive-parry]]
- [[concepts/terms/drive-reversal]]
- [[concepts/terms/drive-rush-cancel]]
- [[concepts/terms/overdrive]]
- [[entities/street-fighter-6]]

## 矛盾 / 注意点

- Capcom 公式 Fighting Ground source は Battle System 範囲の scoped capture であり、Fighting Ground 全体の全 section を保存したものではない。
- Capcom eSports BASE source は観戦用語の scoped capture であり、`CAPCOM eSports BASE` ページ全体の根拠ではない。
- SuperCombo glossary は community source なので、公式 source と異なる wording がある場合は公式 source を優先して差異を明示する。

## 未解決の質問

- Drive Gauge recovery、burnout duration、Drive move の細かな frame / system detail はどの公式 source または派生 data で補うか。
