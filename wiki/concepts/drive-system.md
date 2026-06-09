---
type: concept
title: "Drive System"
created: 2026-05-26
updated: 2026-06-10
status: active
confidence: high
sources:
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "ドライブシステム"
  - "Drive System"
tags:
  - mechanics
---

# Drive System（ドライブシステム）

## 要約

Drive System は、Street Fighter 6 の攻撃・防御・移動を横断する共通 system。Capcom 公式 Fighting Ground source では、Drive Gauge はバトル開始時から使用でき、使いすぎると枯渇状態やバーンアウトに関わる resource として説明されている。

## 定義

Capcom 公式 source は `DRIVE GAUGE` と `COMMON SYSTEM` として Drive Impact、Drive Parry、Overdrive、Drive Rush、Drive Reversal を説明している。SuperCombo glossary は community source として Burnout、Drive Impact、Drive Parry、Drive Reversal、Drive Rush、Drive System、Overdrive を列挙している。

## なぜ重要か

Drive System は movement、offense、defense、resource exhaustion を横断するため、後続の frame-data 解釈、combo route、matchup explanation の前提になる。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| Drive Gauge はバトル開始時から使用可能な Drive System の核心として説明されている。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| Drive Gauge が 0 になるとバーンアウト状態になり、回復するまで Drive System を利用する技は一時的に使用できなくなる。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| Drive Rush は Drive Parry の構え、またはキャンセル可能な通常技から出せる。Drive Parry からはコスト 1、通常技からはコスト 3。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| Drive Impact、Drive Parry、Overdrive、Drive Reversal は公式 Fighting Ground source の Common System として説明されている。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| Drive System は universal movement、offense、defense mechanics への gateway となる meter として説明されている。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Burnout は Drive gauge が空になった時の状態で、Drive-related techniques に制限がかかる。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Drive Rush は Drive Parry または cancelable normal attack から出せる。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |

## 関連

- [[concepts/frame-data]]
- [[entities/street-fighter-6]]

## 矛盾 / 注意点

- Capcom 公式 Fighting Ground source は Battle System 範囲の scoped capture であり、Fighting Ground 全体の全 section を保存したものではない。
- SuperCombo glossary は community source なので、公式 source と異なる wording がある場合は公式 source を優先して差異を明示する。

## 未解決の質問

- Drive Gauge recovery、burnout duration、Drive move の細かな frame / system detail はどの公式 source または派生 data で補うか。
