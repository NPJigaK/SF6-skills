---
type: concept
concept_type: term
title: "生ラッシュ"
created: 2026-06-10
updated: 2026-06-15
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[sources/capcom-official-luke-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[reviews/2026-06-15-pdr-cost-component-video-observation]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[reviews/2026-06-15-pdr-cost-component-video-observation]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "raw Drive Rush"
  - "raw drive rush"
  - "なまらっしゅ"
tags:
  - sf6
  - terms
  - drive-system
---

# 生ラッシュ

## 要約

生ラッシュは、Drive Parry の構えから出す Drive Rush。Capcom 公式 source は Drive Parry から出す Drive Rush の cost を `1`、通常技 cancel 版を `3` と説明する。SuperCombo Gauges page は、この `1` を Drive Parry activation `0.5` + Drive Rush from Parry transition `0.5` の component として読める形で、cost table と Drive Parry section に分解している。

## Source claims

| Source | Claim | Confidence |
|---|---|---|
| [[sources/capcom-esports-base-terms]] `word-06` | Drive Rush は cancel rush と raw Drive Rush の 2 種類。通常技 cancel 版は D gauge 3、Drive Parry から出す生ラッシュは D gauge 1 を使う。Drive Rush 中は通常技性能も上がる。 | high |
| [[sources/capcom-official-fightingground-battle-system]] | Drive Rush は Drive Parry の構え、または cancel 可能な通常技から出せる。Drive Parry からは cost 1、通常技からは cost 3。 | high |
| [[sources/capcom-official-battle-change-list]] | Capcom 公式 Battle Change は Just Parry の Drive Gauge 増加量を `10000（1ブロック）` と表記しており、Drive Gauge の内部単位として `10000 = 1 block` を使う根拠になる。 | high |
| [[sources/capcom-official-luke-frame-data]] | official frame-data は Drive Parry について「動作の4F目からドライブラッシュでキャンセル可」と注記する。 | high |
| [[sources/supercombo-street-fighter-6-gauges]] | Drive Parry activation は `5000` Drive on frame `2`、hold drain は frame `4` から `50` Drive/frame。cost table では Drive Rush from Parry が `1/2`、Drive Rush section / caption では Parry からの Drive Rush が `1 Drive Stock` と説明される。 | medium |
| [[reviews/2026-06-15-pdr-cost-component-video-observation]] | ユーザー提供の実機動画観察では、`0.5` 本以上で Drive Rush が出て Burnout する例と、`0.5` 本未満では Drive Rush へ進まず Burnout する例が確認された。 | medium |

## 数値データ

| 項目 | 値 | 根拠 |
|---|---:|---|
| Official / eSports BASE cost | `1` Drive gauge | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]] |
| Drive Gauge unit | `10000 = 1 block / 1 bar` | [[sources/capcom-official-battle-change-list]], [[sources/supercombo-street-fighter-6-gauges#Drive Gauge overview]] |
| Drive Parry activation component | `5000` Drive = `0.5` bar、frame `2` に消費 | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]] |
| Drive Rush from Parry transition component | `0.5` bar | [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs[action=Drive Rush from Parry].transition_component_cost_bars` |
| Minimum total cost interpretation | `0.5 + 0.5 = 1.0` bar | [[sources/capcom-official-fightingground-battle-system]], [[sources/capcom-esports-base-terms]], [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs[action=Drive Rush from Parry].minimum_total_cost_bars` |
| SuperCombo wording resolution | cost table の `1/2` は PDR transition component、section / caption の `1 Drive Stock` は Parry activation 込みの最小総消費として扱う。PDR は単一の direct cost として `cost_bars` に値を入れず、component / total 専用 field で扱う。 | `wiki/outputs/data/gauges/supercombo/numeric-tables.json`; [[reviews/2026-06-15-pdr-cost-component-video-observation]] |
| Minimum Drive threshold | `0.5` bar 未満では initial Parry cost で Burnout するため raw Drive Rush へ進めない | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]], [[reviews/2026-06-15-pdr-cost-component-video-observation]] |
| `0.5` bar 以上の Burnout-with-rush case | Parry activation は成立し得るため、Drive Rush が出た後に transition cost / hold drain で Burnout する場合がある | [[reviews/2026-06-15-pdr-cost-component-video-observation]] |
| Parry hold drain | frame `4` から `50` Drive/frame | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]] |
| Cost with hold drain | 最小総消費 `10000` Drive に、入力タイミング次第で `50 * n` Drive が乗る可能性がある | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]], [[reviews/2026-06-15-pdr-cost-component-video-observation]] |
| Official Drive Parry cancel note | Drive Parry は動作の `4F` 目から Drive Rush cancel 可 | `wiki/outputs/data/frame-data/official/luke/classic.json`; `rows[].move_name == "ドライブパリィ"` |
| Frame data | startup `3+8`, attack-cancelable recovery `15`, fully-cancelable recovery `22`, total recovery `37` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_frame_data[type=Parry~DR]` |
| Successful Parry route | held successful Parry 後は `1+8` まで短くなると説明 | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]] |
| Screen freeze / advantage | screen freeze `10f`; Drive Rush 中の normal / command normal は `+4` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_values` |
| Distance table | 30 characters 分。term には全行を複製しない | [[sources/supercombo-street-fighter-6-gauges#Drive Rush distance table]]; `drive_rush_distance_by_character` |

## Cost interpretation

Capcom 公式の「Drive Parry からの Drive Rush は cost `1`」は、Drive Parry activation `0.5` と Drive Rush from Parry transition `0.5` を合計した最小総消費として扱う。SuperCombo Gauges の cost table はこのうち transition component を `1/2` として示し、Drive Rush section / caption は Parry からの Drive Rush 全体を `1 Drive Stock` と説明しているため、両者は矛盾ではなく粒度の違いとして読む。

ただし、Drive Parry を保持したまま Drive Rush へ移行するため、入力タイミング次第では frame `4` 以降の hold drain `50` Drive/frame が最小総消費に追加される。未確定なのは `0.5 + 0.5` そのものではなく、特定入力で hold drain が何 frame 分乗るか、また official frame-data の「動作4F目」と SuperCombo の「active frame 3 onward」をどう数えるかである。

## 意味差分

- 現時点では Capcom 公式 source 同士で大きな意味差分はない。
- SuperCombo Gauges page の `1/2` と Capcom 公式の `1` は、Drive Rush from Parry transition component と Parry activation 込みの最小総消費として分けて読める。
- 未解決なのは、特定の入力履歴から frame `4` の hold drain が乗ったかをどこまで確定できるかであり、入力履歴だけで Burnout / no-Burnout を完全分類できるとは扱わない。

## 関連

- [[concepts/drive-system]]
- [[concepts/terms/frame-advantage]]
- [[concepts/terms/shikomi]]
