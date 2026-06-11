---
type: source
source_type: wiki_page
title: "Street Fighter 6/Gauges"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/gauges/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges"
created: 2026-06-11
updated: 2026-06-11
source_updated_at: 2026-06-07T12:31:40Z
captured_at_utc: 2026-06-11T01:23:20Z
status: active
confidence: medium
tags:
  - sf6
  - gauges
  - drive-system
  - super-art
  - community-wiki
  - web-page-capture
  - numeric-source
  - visual-source
aliases:
  - "SF6 Gauges"
  - "Street Fighter 6 Gauges"
  - "ストリートファイター6 ゲージ"
related_concepts:
  - "[[concepts/drive-system]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/index]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 Gauges

## 1行要約

SuperCombo Wiki の Street Fighter 6 Gauges page を MediaWiki wikitext、HTML、rendered DOM、Drive / Super Gauge 関連画像、scoped screenshots として保存した raw source。Drive Gauge cost、Burnout、Drive Impact、Drive Reversal、Drive Parry、Drive Rush、Overdrive、Drive regeneration、Super Gauge build / depletion の数値情報を含む。

## 重要ポイント

1. Canonical raw capture は `raw/web-pages/wiki.supercombo.gg/gauges/manifest.json`。MediaWiki の原文を保つ取得物は `page.raw.wikitext`。
2. Source freshness は MediaWiki revid `365841`、revision timestamp `2026-06-07T12:31:40Z`。Raw 取得時刻は `2026-06-11T01:23:20Z`。
3. `validation.json` は `passed`。Rendered DOM は heading 18 件、table 14 件、image refs 64 件を記録した。
4. 本文の数値表は `rendered/main.dom.json` の table 0-12 に保存されている。table 13 は SF6 Navigation で、本文根拠として扱わない。
5. 数値 query 用に、content table 0-12 と主要な正規化数値を `wiki/outputs/data/gauges/supercombo/numeric-tables.json` に派生出力した。
6. 画像情報も重要なので、本文 media 8 original files と 28 rendered image files を保存した。Drive Gauge、Burnout、Drive Impact、DI armor、Drive Reversal、Drive Parry、Drive Rush、Overdrive の画像と、ボタン / Drive gauge icon の rendered media を含む。
7. この source は community wiki なので、公式 Capcom source と重なる mechanics claim は公式 source を優先する。ただし、Drive regeneration、cooldown、character range / distance tables など、この wiki に未収録の数値補助 source として重要。

## Numeric summary

この section は raw source の数値を wiki query で探しやすくするための compiled view。根拠は `raw/web-pages/wiki.supercombo.gg/gauges/page.raw.wikitext` と `raw/web-pages/wiki.supercombo.gg/gauges/rendered/main.dom.json`。機械利用向けの派生 JSON は `wiki/outputs/data/gauges/supercombo/numeric-tables.json`。

### Drive Gauge overview

| 項目 | SuperCombo Gauges source fact |
|---|---|
| Round start | 両プレイヤーは各 round を Drive Gauge 6 bars で開始する。 |
| Unit conversion | Frame data 上の `1 Bar` は Drive meter `10,000` と説明される。 |
| Passive recovery | Gauge が満タンでない時は時間経過で自動回復する。 |
| Defensive drain | Guard 時に Drive meter が削られる。弱い攻撃は約 `5%` bar、攻撃によっては `1` bar を削ると説明される。 |
| Last-pixel rule | Drive action は Drive Gauge が 1 pixel でも残っていれば実行できると説明される。 |
| Burnout carryover | Round 終了時の Burnout penalty は次 round へ持ち越されないと説明される。 |

### Drive action costs

| Drive action | Cost / source wording |
|---|---:|
| Drive Impact | `1` Drive Stock |
| Drive Parry | activation 約 `1/2` Drive gauge、hold 中も drain |
| Drive Rush from Parry | Source-internal conflict: cost table は `1/2` Drive Stock 相当の icon、Drive Rush section / caption text は `1` Drive Stock。component 分解は未解決 |
| Drive Rush cancel | `3` Drive Stocks |
| Overdrive Specials | `2` Drive Stocks |
| Drive Reversal | `2` Drive Stocks |

### Burnout

| Burnout effect | Value / condition |
|---|---|
| Blockstun | すべての blocked attacks に追加 `4` frames の blockstun |
| Chip damage | Burnout 中の special moves / supers guard は chip damage。通常は move normal damage の `25%`、例外あり |
| Stun condition | Burnout 中の corner Drive Impact wall splat は hit / block どちらでも Stun |
| Drive options | Gauge が完全回復するまで Drive options は使えない |
| Stun recovery note | Burnout 中の cornered player が Drive Impact で stun した場合、stun 回復後に Drive Gauge が full replenish されると説明される |

### Drive Impact frame / drain values

| Startup | Active | Recovery | Block adv. | Damage |
|---:|---:|---:|---:|---:|
| `26(27)` | `2` | `35` | `-3` | `800` |

| Drive Impact hit context | Opponent Drive Gauge drain |
|---|---:|
| On block | `0.5` Bar |
| On hit | `1` Bar |
| On Counter-hit | `1.2` Bars |
| On Punish / Crumple | `1.5` Bars |

Additional Drive Impact numeric facts:

- Drive Impact has `2` hits of armor during startup and active frames.
- Damage scaling after Drive Impact on hit is described as `20%` starter scaling, with example sequence `100 -> 80 -> 70 -> 60`.
- Damage scaling after Drive Impact on block is described as a `20%` multiplier reduction for follow-ups, with example sequence `80 -> 80 -> 64 -> 56 -> 48`.
- Stun combo on dizzy opponents begins at `80%` damage scaling, then continues decreasing by `10%` per hit.
- After Drive Impact stun, the opponent can be hit for the next `195` frames from the moment they hit the wall.
- The last `7` frames before falling have a crouch-sized hurtbox while still counted as standing state.
- Against projectiles, Drive Impact has `6` frames of armor hit-freeze.
- Drive Impact startup becomes `1f` slower after absorbing an attack.
- If two Drive Impacts clash simultaneously, both players are refunded the `1` Drive bar spent.

### Drive Impact range table

Rendered DOM table 4: `Drive Impact - Forward Movement & Maximum Range`.

| Character | Forward movement startup | Maximum range 2nd active frame |
|---|---:|---:|
| A.K.I. | 1.400 | 2.500 |
| Akuma | 1.511 | 2.561 |
| Alex | 1.627 | 2.477 |
| Blanka | 1.373 | 2.523 |
| C. Viper | 1.479 | 2.549 |
| Cammy | 1.644 | 2.544 |
| Chun-Li | 1.406 | 2.506 |
| Dee Jay | 1.480 | 2.520 |
| Dhalsim | 1.558 | 2.258 |
| Ed | 1.495 | 2.545 |
| E. Honda | 1.739 | 2.539 |
| Elena | 1.441 | 2.541 |
| Guile | 1.321 | 2.481 |
| Ingrid | 1.433 | 2.483 |
| Jamie | 1.670 | 2.490 |
| JP | 1.455 | 2.535 |
| Juri | 1.461 | 2.511 |
| Ken | 1.390 | 2.470 |
| Kimberly | 1.843 | 2.543 |
| Lily | 1.489 | 2.389 |
| Luke | 1.510 | 2.450 |
| M. Bison | 1.217 | 2.537 |
| Mai | 1.781 | 2.541 |
| Manon | 1.200 | 2.500 |
| Marisa | 1.537 | 2.527 |
| Rashid | 1.419 | 2.579 |
| Ryu | 1.491 | 2.541 |
| Sagat | 1.839 | 2.529 |
| Terry | 1.300 | 2.500 |
| Zangief | 1.606 | 2.496 |

### Drive Reversal

| Startup | Active | Recovery | Damage | On hit | On block |
|---:|---:|---:|---:|---|---:|
| `20(18)` | `3` | `26(31)*` | `500 (recoverable)` | KD `+23*` | `-6` |

Additional Drive Reversal numeric facts:

- Recovery Drive Reversal uses `18f` startup; the rest of its frame data is described as the same as regular Drive Reversal.
- Advantage on hit is `+24` for Dhalsim.
- Chun-Li and Dhalsim have `2-hit` Drive Reversals, with active frames `3(10)3` and `3(6)3` respectively.
- Alex and Marisa have `4f` less hitstop on blocked Drive Reversal.
- Drive Reversal from blockstun has a short `4-frame` screen freeze after the `6th` startup frame.
- Recovery Drive Reversal against an incoming throw triggers a `12f` screen freeze and refunds `1` Drive bar.

### Drive Parry and Perfect Parry

| Startup | Active | Recovery |
|---:|---|---|
| `1` | `12~ [2]` | `33 [1]` |

`[]` values refer to Perfect Parry.

| Drive Parry cost / gain | Value |
|---|---:|
| Activation cost | `5000` Drive on frame `2` |
| Hold drain | `50` Drive per frame starting on frame `4` |
| Minimum whiffed parry cost | `5450` Drive |
| Parry vs projectile | `5000` Drive gain |
| Parry vs Normal / Special / Drive Reversal | `10000` Drive gain |
| Parry vs Super Art / Critical Art / Drive Impact | `20000` Drive gain |
| Extra gain for Perfect Parry timing without freeze | `3000` Drive |
| Throw punish against Parry | drains `1` Drive bar |

Additional Drive Parry / Perfect Parry numeric facts:

- Regular Parry is active for `12f` before recovery and parries strikes/projectiles from frame `1`.
- From active frame `3` onward, Parry can be canceled into Drive Rush with Forward Dash.
- Perfect Parry occurs only on the first `2` Parry active frames and cannot be buffered by holding the buttons.
- Attempting Perfect Parry with under `1/2` Drive bar requires frame-perfect timing and enters Burnout on frame `2` of Parry.
- Perfect Parry applies a `50%` damage scaling multiplier to the punish.
- After Perfect Parry, both characters build `20%` less Super gauge for subsequent hits.
- After Perfect Parry, the attacker builds `50%` less Drive gauge and the defender takes `50%` less Drive damage.
- A successful Perfect Parry against a strike causes `60f` / `1 second` screen freeze.
- Perfect Parrying a projectile causes fixed `11f` recovery: `1f` Parry plus `10f` extra recovery.
- Parry input can be held up to `13` additional frames after projectile Perfect Parry without incurring standard recovery.

### Drive Rush frames and scaling

| Drive Rush type | Startup | Attack-cancelable recovery | Fully-cancelable recovery | Total recovery |
|---|---:|---:|---:|---:|
| Parry~Drive Rush | `3+8` | `15` | `22` | `37` |
| Drive Rush cancel | `9` | `15` | `22` | `37` |

Additional Drive Rush numeric facts:

- Parry~Drive Rush requires at least `3` Parry frames plus `8` startup frames; after holding a successful Parry, this can be `1+8`.
- Drive Rush begins with a `10-frame` screen freeze.
- Normal / Command Normal during Drive Rush gets `+4` advantage on hit or block.
- Mid-combo Drive Rush adds a one-time `15%` damage scaling penalty.
- To safely bait a `6-frame` reversal from Drive Rush, SuperCombo says knockdown advantage of at least `+21` is needed to block; whiffing a fast light may bait at KD `+18~20`.
- Directional movement transition after Drive Rush plays `2` additional recovery frames.
- Raw Drive Rush cannot be performed with under `1/2` Drive bar because the initial Parry cost is paid immediately.

### Drive Rush distance table

Rendered DOM table 8: `Drive Rush Distance Comparison`.

| Character | Min distance immediate throw | Min distance crouch block | Max distance no input |
|---|---:|---:|---:|
| A.K.I. | 0.907 | 2.437 | 4.049 |
| Akuma | 0.880 | 2.121 | 3.425 |
| Alex | 0.393 | 1.722 | 3.530 |
| Blanka | 0.476 | 2.082 | 2.867 |
| C. Viper | 0.374 | 1.756 | 3.355 |
| Cammy | 0.603 | 2.027 | 2.796 |
| Chun-Li | 1.044 | 2.222 | 3.163 |
| Dee Jay | 0.763 | 2.535 | 2.713 |
| Dhalsim | 0.471 | 1.787 | 2.700 |
| Ed | 0.910 | 2.190 | 3.374 |
| E. Honda | 0.213 | 1.769 | 3.375 |
| Elena | 0.548 | 2.100 | 3.011 |
| Guile | 0.805 | 1.898 | 3.461 |
| Ingrid | 0.375 | 1.502 | 3.083 |
| Jamie | 0.988 | 2.030 | 3.002 |
| JP | 0.525 | 1.857 | 3.628 |
| Juri | 0.641 | 2.479 | 3.999 |
| Ken | 0.745 | 2.449 | 3.721 |
| Kimberly | 0.817 | 2.479 | 3.565 |
| Lily | 0.434 | 1.900 | 3.044 |
| Luke | 0.817 | 2.499 | 3.461 |
| M. Bison | 0.593 | 2.650 | 4.426 |
| Mai | 0.669 | 2.383 | 2.977 |
| Manon | 0.506 | 1.417 | 2.347 |
| Marisa | 0.544 | 1.903 | 3.081 |
| Rashid | 0.796 | 2.253 | 2.998 |
| Ryu | 0.525 | 1.878 | 3.628 |
| Sagat | 0.546 | 1.869 | 3.156 |
| Terry | 0.634 | 2.416 | 3.181 |
| Zangief | 0.327 | 1.455 | 3.040 |

### Overdrive

| Item | Value / condition |
|---|---|
| Cost | `2` Drive Stocks |
| Input | `2` Punches or `2` Kicks while inputting a special move |
| Burnout edge case | OD Specials can be performed with less than `2` Drive bars, but the player is immediately put into Burnout |
| Super cancel note | Super-cancelable OD Specials can go into Level `2` Super Art; meterless specials only cancel to SA3 / CA in this source's wording |

### Drive regeneration

SuperCombo Gauges states that `1` Drive bar is `10,000` units and `1` frame is `1/60` second.

| State / action | Regen per frame / % bar per second | Burnout value |
|---|---:|---:|
| Base Drive Regen (passive) | `40` / `24%` | `50` / `30%` |
| In hitstun | `20` / `12%` | `25` / `15%` |
| Jumping | `20` / `12%` | not separately listed |
| Walking forward | `+20` / `+12%`; from frame `11`, Base Drive Regen is doubled | Applies during Burnout; source says total `70` Drive/frame before frame 11 boost |

Walking forward formulas:

| Formula context | Formula | Result |
|---|---|---:|
| Standard, frame 11+ | `40 x2 + 20` Drive/frame | `100` Drive/frame, `0.6` Drive bars/sec |
| Burnout, frame 11+ | `50 x2 + 20` Drive/frame | `120` Drive/frame, `0.72` Drive bars/sec |

### Drive regeneration cooldown

| Trigger | Cooldown frames | Notes |
|---|---:|---|
| Blocking attacks / getting Punish Countered | `90` | Counts from start of blockstun or punish hitstun; not inflicted on opponents in Burnout; multi-hit attacks reset timer to `90` on each hit |
| Getting hit by Super Art | `90` | Counts down after Super hitstun ends; freezes at `90` during cinematic periods |
| OD Special / Drive Impact / Drive Reversal | `120` | Counts down after all recovery frames finish |
| Drive Rush Cancel | `120` | Starts when Drive Rush dash active frames are canceled; additional Drive regen is prevented until combo ends except Forward Walk |
| Parry whiff / Parry Drive Rush | `240` | Counts from Parry recovery end; Parry Drive Rush timer starts when dash active frames are canceled |
| Successful Parry | `20` | Applies after parry freeze/blockstun for both regular and Perfect Parry; overwrites usual `240f` cooldown |

### Super Gauge and Super Art

| Item | Value / condition |
|---|---|
| Match start | Super Gauge starts empty |
| Max stock | `3` bars |
| Round carryover | Unspent Super meter carries over between rounds |
| Critical Art condition | Level 3 Super becomes Critical Art under `25%` health |
| Super Art timer | Round timer is frozen for the duration of Super Art, except install supers that allow independent action |

Super Gauge build rule:

| Actor | On hit | On block | On armor absorb |
|---|---:|---:|---:|
| Attacker | Base | `50%` | Base |
| Defender | `70%` | `25%` | `35%` |

Super Art Drive Gauge depletion:

| SA1 | SA2 | SA3 | CA |
|---:|---:|---:|---:|
| `0.5` Bar | `1` Bar | `1.5` Bar | `2` Bar |

The source notes that this can vary, especially for non-cinematic Super variations.

## Media / visual evidence

| Media | Raw artifact | Context |
|---|---|---|
| Drive Gauge | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_Drive_Gauge.jpg` | Drive Overview, `1 Bar = 10,000 Drive meter` caption |
| Burnout | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_Burnout.png` | Burnout |
| Drive Impact | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_drive_impact.jpg` | Drive Impact |
| DI armor example | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_DI_Armor_Example.png` | Armor lasts through active frames, disappears during recovery |
| Drive Reversal | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_drive_reversal.jpg` | Drive Reversal |
| Drive Parry | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_drive_parry.jpg` | Drive Parry |
| Drive Rush | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_drive_rush.jpg` | Drive Rush |
| Overdrive | `raw/web-pages/wiki.supercombo.gg/gauges/images/files/SF6_drive_overdrive.jpg` | Overdrive |

`rendered/media.dom.json` records each image's nearest heading, caption, dimensions, and rendered position. `screenshots/page-scoped.png` and `screenshots/content-scoped.png` preserve page-level display evidence after navigation removal.

## 関連概念

- [[concepts/drive-system]]
- [[concepts/frame-data]]
- [[concepts/terms/index]]
- [[concepts/terms/burnout]]
- [[concepts/terms/drive-impact]]
- [[concepts/terms/drive-parry]]
- [[concepts/terms/drive-reversal]]
- [[concepts/terms/raw-drive-rush]]
- [[concepts/terms/drive-rush-cancel]]
- [[concepts/terms/overdrive]]
- [[concepts/terms/super-art]]
- [[concepts/terms/damage-scaling]]

## 関連エンティティ

- [[entities/street-fighter-6]]
- [[entities/supercombo-wiki]]

## 既存 wiki との矛盾または更新

- この source は community wiki であり、公式 Capcom source より低い confidence で扱う。
- Drive Gauge、Burnout、Drive Impact、Drive Parry、Drive Rush、Overdrive、Super Art など、公式 source と重なる mechanics claim は公式 source を優先する。
- ただし、Drive regeneration、cooldown、Drive Impact range、Drive Rush distance、Drive Parry gain/cost など、この wiki の既存公式 source にない数値は、SuperCombo community source fact として保持する。
- Cost table の icon template は rendered DOM では text 化されないため、Drive action cost は `page.raw.wikitext` の section text と table template notation を併用して確認する。
- Drive Rush from Parry は cost table と section / caption text で値が揺れるため、derived JSON は単一 `cost_bars` に正規化せず ambiguous alternatives を保持する。
- 30 character range/distance values は source fact として保存するが、公式値または実機検証値ではない。character-specific query では community source であることを明示する。
- `wiki/outputs/data/gauges/supercombo/numeric-tables.json` は source-preserving derived output で、raw content table 0-12 と、Drive action cost、Drive Impact / Drive Rush distance、regeneration / cooldown、Super Gauge などの正規化数値を保持する。

## 未解決の質問

- Drive regeneration、cooldown、range / distance values を公式 source または実機検証で照合するか。
- `Drive Rush from Parry` の cost 表記は、cost table の `1/2` と section / caption text の `1 Drive Stock` を component 分解として扱うか、source-internal conflict として保持し続けるか。
- `wiki/outputs/data/gauges/supercombo/numeric-tables.json` の schema を、他の gauge / system numeric source にも使う標準 schema として固定するか。

## ソースメモ

- Raw manifest: `raw/web-pages/wiki.supercombo.gg/gauges/manifest.json`
- Canonical raw wikitext: `raw/web-pages/wiki.supercombo.gg/gauges/page.raw.wikitext`
- Rendered DOM: `raw/web-pages/wiki.supercombo.gg/gauges/rendered/main.dom.json`
- Media DOM: `raw/web-pages/wiki.supercombo.gg/gauges/rendered/media.dom.json`
- Image manifest: `raw/web-pages/wiki.supercombo.gg/gauges/images/manifest.json`
- Derived numeric output: `wiki/outputs/data/gauges/supercombo/numeric-tables.json`
- Original media: `raw/web-pages/wiki.supercombo.gg/gauges/images/files/`
- Rendered media: `raw/web-pages/wiki.supercombo.gg/gauges/images/rendered/`
- Scoped screenshots: `raw/web-pages/wiki.supercombo.gg/gauges/screenshots/`
- Validation: `raw/web-pages/wiki.supercombo.gg/gauges/validation.json`
- Original URL: https://wiki.supercombo.gg/w/Street_Fighter_6/Gauges
