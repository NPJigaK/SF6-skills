---
type: concept
title: "Drive System"
created: 2026-05-26
updated: 2026-06-15
status: active
confidence: high
sources:
  - "[[sources/capcom-esports-base-terms]]"
  - "[[sources/capcom-official-fightingground-battle-system]]"
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-hud]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/supercombo-street-fighter-6-offense]]"
  - "[[sources/supercombo-street-fighter-6-defense]]"
related:
  - "[[concepts/terms/index]]"
  - "[[concepts/defense]]"
  - "[[concepts/offense]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/burnout]]"
  - "[[concepts/terms/drive-impact]]"
  - "[[concepts/terms/drive-parry]]"
  - "[[concepts/terms/drive-reversal]]"
  - "[[concepts/terms/drive-rush-cancel]]"
  - "[[concepts/terms/raw-drive-rush]]"
  - "[[concepts/terms/armor]]"
  - "[[concepts/terms/throw]]"
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

Drive System は、Street Fighter 6 の攻撃・防御・移動を横断する共通 system。Capcom 公式 Fighting Ground source では、Drive Gauge はバトル開始時から使用でき、使いすぎると枯渇状態や [[concepts/terms/burnout|バーンアウト]] に関わる resource として説明されている。Capcom 公式 eSports BASE 用語解説は、[[concepts/terms/chip-damage|削り]]、[[concepts/terms/stun|スタン]]、[[concepts/terms/raw-drive-rush|生ラッシュ]]、[[concepts/terms/drive-impact-counter|インパクト返し]]、[[concepts/terms/perfect-parry|ジャストパリィ]]などの観戦用語として Drive System 周辺の具体例を補う。SuperCombo HUD page は Battle HUD 上の Drive Gauge / Super Art Gauge と、Drive Impact・Burnout に関係する HUD icon の表示証拠を補う。SuperCombo Gauges page は community numeric source として、Drive Gauge の cost、regeneration、cooldown、Drive Impact / Drive Rush の range table などを補う。SuperCombo Offense page は、Drive Rush を使った strike/throw mixup、Drive Parry に対する Punish Counter throw、corner dizzy 後の Drive regeneration choice を攻めの文脈で補う。SuperCombo Defense page は、Drive Parry を high/low と left/right を受ける defensive option として、Drive Impact / armor / Drive Reversal を守りの文脈で補う。

## 定義

Capcom 公式 Fighting Ground source は `DRIVE GAUGE` と `COMMON SYSTEM` として [[concepts/terms/drive-impact|Drive Impact]]、[[concepts/terms/drive-parry|Drive Parry]]、[[concepts/terms/overdrive|Overdrive]]、Drive Rush、[[concepts/terms/drive-reversal|Drive Reversal]] を説明している。Capcom 公式 eSports BASE は観戦用語として、Burnout 中の [[concepts/terms/chip-damage|削り]]、Burnout 中の Drive Impact による [[concepts/terms/stun|stun]]、Drive Parry から出す [[concepts/terms/raw-drive-rush|生ラッシュ]]、Drive Impact への [[concepts/terms/drive-impact-counter|インパクト返し]]、[[concepts/terms/perfect-parry|ジャストパリィ]] を説明している。Capcom 公式 Battle Change は `10000（1ブロック）` という Drive Gauge 内部値表記を補う。SuperCombo glossary は community source として Burnout、Drive Impact、Drive Parry、Drive Reversal、Drive Rush、Drive System、Overdrive を列挙している。SuperCombo HUD page は visual/community source として、Battle HUD 上の Drive Gauge と Drive Impact / Burnout 関連 icon の見え方を補助する。SuperCombo Gauges page は、1 Bar = 10,000 Drive、Drive action cost、Drive regeneration / cooldown、Drive move の frame / distance / gauge-damage 数値を表で示す。

## なぜ重要か

Drive System は movement、offense、defense、resource exhaustion を横断するため、後続の frame-data 解釈、combo route、matchup explanation の前提になる。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| Drive Gauge はバトル開始時から使用可能な Drive System の核心として説明されている。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| Drive Gauge が 0 になると [[concepts/terms/burnout|バーンアウト]] 状態になり、回復するまで Drive System を利用する技は一時的に使用できなくなる。 | [[sources/capcom-official-fightingground-battle-system]] | high |
| SuperCombo HUD page は Battle HUD 上の Drive Gauge を表示要素として示し、Gauge が空になると Burnout になり、完全回復まで Drive-related techniques が使えないと説明する。 | [[sources/supercombo-street-fighter-6-hud]] | medium |
| SuperCombo Gauges page は、各 round 開始時の Drive Gauge を 6 bars、1 Bar を 10,000 Drive とし、Drive Gauge は時間経過で受動回復し、guard 時や Drive action 使用時に消費されると説明する。 | [[sources/supercombo-street-fighter-6-gauges]] | medium |
| Capcom official Battle Change は Just Parry の Drive Gauge 増加量を `10000（1ブロック）` と表記する。 | [[sources/capcom-official-battle-change-list]] | high |
| SuperCombo Gauges page は、Base Drive Regeneration を 40 Drive/frame（0.24 bars/sec）、Burnout 中の Base Drive Regeneration を 50 Drive/frame（0.3 bars/sec）とし、Hitstun / Jumping / Walking 中の modifier も表で示す。 | [[sources/supercombo-street-fighter-6-gauges]] | medium |
| SuperCombo Gauges page は、Drive regeneration cooldown を block / Punish Counter / Super hit 90f、OD Special / Drive Impact / Drive Reversal / Drive Rush Cancel 120f、Whiff Parry / Parry Drive Rush 240f、Successful Parry 20f とする。 | [[sources/supercombo-street-fighter-6-gauges]] | medium |
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
| SuperCombo Gauges page は、Drive Impact cost 1、Drive Reversal cost 2、Overdrive Special cost 2、Drive Rush Cancel cost 3、Drive Parry activation 約 1/2 bar、Drive Rush from Parry transition 1/2 bar を表で示す。Capcom 公式の Drive Parry からの Drive Rush cost `1` は、Drive Parry activation `0.5` + Drive Rush from Parry transition `0.5` の最小総消費として扱う。 | [[sources/supercombo-street-fighter-6-gauges]], [[concepts/terms/raw-drive-rush]] | medium |
| SuperCombo Offense page は、Drive Rush が midscreen でも strike/throw mixup を作れること、Drive Parry に対する throw は常に Punish Counter になり、相手 Drive Gauge `1` bar を drain すること、corner dizzy 後は Drive gauge が満タンでなければ前歩きで regeneration を稼ぐ選択があることを説明する。 | [[sources/supercombo-street-fighter-6-offense]] | medium |
| SuperCombo Defense page は、Drive Parry が high/low と left/right を parry でき、block と同じ frame advantage になること、wake-up Super Art bait では Parry hold で Drive を大きく refill できる場合があることを説明する。 | [[sources/supercombo-street-fighter-6-defense]] | medium |
| SuperCombo Defense page は、Drive Impact や一部 special moves の armor は strike / projectile を吸収するが throw に負け、absorbed attack の normal damage `50%` を recoverable damage として受けると説明する。 | [[sources/supercombo-street-fighter-6-defense]] | medium |

## 数値索引

この section は回答時に source page と derived JSON へ戻るための入口。値は SuperCombo Gauges の community numeric source fact なので、公式 source または実機検証と重なる場合はそちらを優先する。

| 領域 | 主要値 | 詳細 |
|---|---|---|
| Drive Gauge unit | official Battle Change は `10000（1ブロック）` と表記。SuperCombo は round start `6` bars、`1 Bar = 10,000` Drive | [[sources/capcom-official-battle-change-list]], [[sources/supercombo-street-fighter-6-gauges#Drive Gauge overview]] |
| Drive action cost | DI `1`, Drive Parry activation `0.5`, DRC `3`, OD `2`, DRev `2` bars | [[sources/supercombo-street-fighter-6-gauges#Drive action costs]]; `drive_action_costs` |
| Drive Rush from Parry | transition component `0.5` + Drive Parry activation `0.5` = minimum total `1.0`; hold drain は frame `4` から `50` Drive/frame | [[concepts/terms/raw-drive-rush]], [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]] |
| Burnout | blockstun `+4f`, chip damage 約 `25%`, Drive options は full recovery まで不可 | [[sources/supercombo-street-fighter-6-gauges#Burnout]]; `burnout_values` |
| Drive regeneration | base `40` Drive/frame、Burnout base `50` Drive/frame、walking frame 11+ は standard `100` / Burnout `120` Drive/frame | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration]]; `drive_regeneration_rates`, `drive_regeneration_walk_forward_formulas` |
| Drive regeneration cooldown | block / Punish Counter / Super hit `90f`; OD / DI / DRev / DRC `120f`; whiff Parry / Parry Drive Rush `240f`; successful Parry `20f` | [[sources/supercombo-street-fighter-6-gauges#Drive regeneration cooldown]]; `drive_regeneration_cooldowns` |
| Drive Impact | cost `1`, startup `26(27)`, active `2`, recovery `35`, block `-3`, damage `800`; drain block `0.5`, hit `1`, counter hit `1.2`, punish/crumple `1.5` bars | [[sources/supercombo-street-fighter-6-gauges#Drive Impact frame / drain values]]; `drive_impact_frame_data`, `drive_impact_drive_gauge_drain` |
| Drive Parry / Perfect Parry | Parry startup `1`, PP window `2f`; activation `5000` Drive、hold `50`/frame、gains `5000` / `10000` / `20000`、PP extra `3000`; PP projectile recovery `11f` | [[sources/supercombo-street-fighter-6-gauges#Drive Parry and Perfect Parry]]; `drive_parry_*`, `perfect_parry_values` |
| Drive Rush | Parry~DR startup `3+8`, DRC startup `9`, actionable recovery `15`, full recovery `22`, total `37`; screen freeze `10f`, normal bonus `+4`, mid-combo scaling `15%` | [[sources/supercombo-street-fighter-6-gauges#Drive Rush frames and scaling]]; `drive_rush_frame_data`, `drive_rush_values` |
| Character tables | Drive Impact range と Drive Rush distance は 30 characters 分を source page と JSON に保持 | [[sources/supercombo-street-fighter-6-gauges#Drive Impact range table]], [[sources/supercombo-street-fighter-6-gauges#Drive Rush distance table]]; `drive_impact_range_by_character`, `drive_rush_distance_by_character` |
| Super Gauge | match start empty、max `3` bars、round carryover、CA threshold `25%`; SA depletion SA1 `0.5`, SA2 `1`, SA3 `1.5`, CA `2` Drive bars | [[sources/supercombo-street-fighter-6-gauges#Super Gauge and Super Art]]; `super_gauge` |

## 関連

- [[concepts/defense]]
- [[concepts/frame-data]]
- [[concepts/offense]]
- [[concepts/terms/index]]
- [[concepts/terms/burnout]]
- [[concepts/terms/drive-impact]]
- [[concepts/terms/drive-parry]]
- [[concepts/terms/drive-reversal]]
- [[concepts/terms/drive-rush-cancel]]
- [[concepts/terms/armor]]
- [[concepts/terms/throw]]
- [[concepts/terms/overdrive]]
- [[entities/street-fighter-6]]

## 矛盾 / 注意点

- Capcom 公式 Fighting Ground source は Battle System 範囲の scoped capture であり、Fighting Ground 全体の全 section を保存したものではない。
- Capcom eSports BASE source は観戦用語の scoped capture であり、`CAPCOM eSports BASE` ページ全体の根拠ではない。
- SuperCombo glossary は community source なので、公式 source と異なる wording がある場合は公式 source を優先して差異を明示する。
- SuperCombo HUD page は HUD 表示と icon visual evidence の community source として使い、公式 source と重なる Drive / Burnout mechanics claim では公式 source を優先する。
- SuperCombo Gauges page は community numeric source として使う。公式 source または検証済み data と重なる cost / frame / damage 値は、公式・実機検証結果を優先し、SuperCombo 値は補助根拠として扱う。
- SuperCombo Offense page は Drive System そのものの正本ではなく、Drive Rush / Drive Parry / corner dizzy が攻めに接続する場面の community tactical source として使う。
- SuperCombo Defense page は Drive System そのものの正本ではなく、Drive Parry / armor / Drive Reversal が守りに接続する場面の community tactical source として使う。

## 未解決の質問

- Drive Gauge recovery、burnout duration、Drive move の細かな frame / system detail は、公式 source または実機検証でどこまで照合するか。
- SuperCombo Gauges の `numeric-tables.json` schema を、他の gauge / system numeric source にも使う標準 schema として固定するか。
