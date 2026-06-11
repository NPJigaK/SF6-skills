---
type: source
source_type: wiki_page
title: "Street Fighter 6/Game Data"
author: "SuperCombo Wiki contributors"
raw_path: "raw/web-pages/wiki.supercombo.gg/game-data/manifest.json"
original_url: "https://wiki.supercombo.gg/w/Street_Fighter_6/Game_Data"
created: 2026-06-11
updated: 2026-06-11
source_updated_at: 2026-06-04T23:19:26Z
captured_at_utc: 2026-06-11T13:38:34Z
status: active
confidence: medium
tags:
  - sf6
  - game-data
  - frame-data
  - damage-scaling
  - system-data
  - community-wiki
  - web-page-capture
  - numeric-source
aliases:
  - "SF6 Game Data"
  - "Street Fighter 6 Game Data"
  - "ストリートファイター6 ゲームデータ"
related_concepts:
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/system-data]]"
  - "[[concepts/range-comparisons]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/terms/guaranteed-punish]]"
related_entities:
  - "[[entities/street-fighter-6]]"
  - "[[entities/supercombo-wiki]]"
---

# ソース: SuperCombo Wiki Street Fighter 6 Game Data

## 1行要約

SuperCombo Wiki の Street Fighter 6 Game Data page は、move stage、hitstun / blockstun / hitstop、input buffer、priority、hurtbox、damage scaling、system data、range comparison、punish option table をまとめた community numeric source。

## 重要ポイント

- Canonical raw は `raw/web-pages/wiki.supercombo.gg/game-data/page.raw.wikitext`。MediaWiki revision は `365507`、source updated は `2026-06-04T23:19:26Z`、capture は `2026-06-11T13:38:34Z`。
- Raw package は `validation.json` と `validation.tabbers.json` が `passed`。この page は tabber 付き table が多いため、wikitext、page HTML、scoped HTML、rendered DOM、live DOM click validation を照合している。
- Rendered table は全体 40 件。本文 table は 39 件で、SF6 Navigation table 1 件は content から除外した。
- Tabber group は 4 件。tab 数は `30 / 3 / 4 / 9`、合計 46 tabs。source 上で table または Cargo query を持つ tabs は `30 / 3 / 4 / 1`。
- Table text は raw package 内の source-preserving artifact `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` に保持する。これは正規化済み move schema ではなく、rendered table text の保存と索引用 artifact。`tools/web_pages/supercombo_page.py` が `rendered/tabbers.dom.json`、`validation.tabbers.json`、`tabber-tables.json` を同じ capture pass で再生成する。
- SuperCombo は community source なので、Capcom 公式 source と重なる mechanics / frame 値では公式 source を優先する。

## Section summary

| Section | 内容 |
|---|---|
| Frame data / Move Stages | Startup、active、recovery、FAF などの技 stage と `1 frame = 1/60 second` の前提。 |
| Hitstun / Blockstun / Hitstop | Hit / block 後の硬直、hitstop、delayed cancel などの timing context。 |
| Input Buffer / Screen Freeze Buffers | 通常 input buffer、Perfect Parry、Super activation、Drive Rush screen freeze 中の buffer notes。 |
| Priority Systems | Hit priority、projectile priority、move input priority。 |
| Standing / Crouching Hurtboxes | 立ち / しゃがみ hurtbox と Parry 入力時の crouching hurtbox note。 |
| Combo-Only Hitboxes / Recoverable HP | Combo-only hitbox、recoverable HP の説明。 |
| Damage Scaling | 標準 scaling progression、system-wide scaling、character-specific scaling tabs。 |
| System Data | General / movement / jump data の 3 tabbed tables。 |
| Range Comparisons | 2MK、4f normal、5f punish、sweep range の 4 tabbed tables。 |
| Longest Punish Option | `≤4F` table と、`≤5F` から `≤12F` までの source-side `(to-do)` tabs。 |

## 数値・table 索引

### Damage Scaling progression

| Attack # | General Scaling | Light Normal or 2MK Combo Starter |
|---|---:|---:|
| 1st Attack | 100% | 100% |
| 2nd Attack | 100% | 80% |
| 3rd Attack | 80% | 70% |
| 4th Attack | 70% | 60% |
| 5th Attack | 60% | 50% |
| 6th Attack | 50% | 40% |
| 7th Attack | 40% | 30% |
| 8th Attack | 30% | 20% |
| 9th Attack | 20% | 10% |
| 10th+ Attack | 10% | 10% |

根拠: `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json` の `tables[0]`。

### System-wide scaling

| 条件 | Source claim | 根拠 |
|---|---|---|
| Super Arts minimum | SA1 `30%`、SA2 `40%`、SA3 / CA `50%` minimum。 | `page.raw.wikitext`; Damage Scaling / System-Wide Scaling |
| Level 3 Super Arts cancel | Special cancel からの Level 3 は追加 `10%` damage scaling penalty。 | `page.raw.wikitext`; Damage Scaling / System-Wide Scaling |
| Perfect Parry punish | Perfect Parry 後の punish は damage scaling を `50%` multiplier にし、Super gain `80%`、attacker Drive gain `50%`、defender Drive damage `50%` と説明する。 | `page.raw.wikitext`; Damage Scaling / System-Wide Scaling |
| Mid-combo Drive Rush | Mid-combo Drive Rush は残り hit に `15%` scaling penalty を適用し、複数回使っても追加 penalty は stack しないと説明する。 | `page.raw.wikitext`; Damage Scaling / System-Wide Scaling |
| Drive Impact | Blocked corner wallsplat follow-up は `20%` scaling multiplier、hit crumple / wallsplat / Burnout stun は `20%` starter scaling と説明する。 | `page.raw.wikitext`; Damage Scaling / System-Wide Scaling |
| Throws in combo | Stun、Drive Impact crumple、rare grounded Wall Splat などから throw に繋ぐと throw に immediate `20%` damage scaling がかかると説明する。 | `page.raw.wikitext`; Damage Scaling / System-Wide Scaling |

### Tabbed tables

| Group | Table indices | 内容 | Row count |
|---|---|---|---|
| Character-specific scaling | `1..30` | A.K.I. から Zangief まで 30 character tabs。 | 各 4-18 rows |
| System Data | `31..33` | General Data、Movement Data、Jump Data。 | 各 31 rows |
| Range Comparisons | `34..37` | Cancelable 2MK Range、4f Normal Range / Hitstun / Pushback、5f Punish Options、Sweep Ranges。 | 21 / 50 / 44 / 40 rows |
| Longest Punish Options | `38` | `≤4F` tab の Character / Button / Range / Notes table。 | 29 rows |

`≤5F`、`≤6F`、`≤7F`、`≤8F`、`≤9F`、`≤10F`、`≤11F`、`≤12F` tabs は source 上で `(to-do)` で、table は存在しない。

## Media / visual evidence

本文 media として `File:FAF Move Stages.png` と `File:SF6 Health Bars SA3 Scaling.png` を取得した。Navigation / character icon 30 件は content media ではないため、raw package では excluded provenance として扱う。

## Capture / validation

- `raw/web-pages/wiki.supercombo.gg/game-data/validation.json`: `passed`
- `raw/web-pages/wiki.supercombo.gg/game-data/validation.tabbers.json`: `passed`
- `validation.tabbers.json` は live revision `365507` と capture revision の一致、4 tabber groups、46 tabs、tab label 一致、panel 数一致、table presence 一致、全 tabs クリック後の table count 安定、requested tab selection を確認した。
- `page_html_table_count` は 40、`scoped_html_table_count` は 39。差分 1 件は SF6 Navigation table。
- manifest の `game_data_tabber_pipeline` は、tabber DOM、tabber validation、derived table output の再生成経路を `tools/web_pages/supercombo_page.py` として記録する。

## 既存 wiki との関係

- [[concepts/terms/damage-scaling]] の system-specific scaling 値を補強する。特に標準 scaling progression、SA minimum、Level 3 cancel penalty、Perfect Parry / Drive Rush / Drive Impact / throw scaling の community source。
- [[concepts/system-data]] は General Data、Movement Data、Jump Data tables を full table として保持する。
- [[concepts/range-comparisons]] は Cancelable 2MK Range、4f Normal Range / Hitstun / Pushback、5f Punish Options、Sweep Ranges を full table として保持する。
- [[concepts/terms/guaranteed-punish]] は Longest Punish `≤4F` table を full table として保持する。ただし `≤5F` から `≤12F` は source 上で `(to-do)`。
- [[concepts/frame-data]] の scalar timing values、system data、range comparison、punish option table への入口になる。ただし individual move frame-data は Capcom official frame-data output と SuperCombo per-character frame-data output を優先する。
- [[sources/supercombo-street-fighter-6-gauges]] と重なる Perfect Parry、Drive Rush、Drive Impact scaling は community source 同士の相互確認として扱う。公式 source と矛盾する場合は公式 source を優先する。

## 未解決の質問

- Character-specific scaling、system data、range comparison、`≤4F` punish option values を公式 source または実機検証で照合するか。
- Character-specific scaling tabs を moveId-linked data に正規化するか、source-preserving table output のまま保持するか。
- Range comparison tables を queryable schema に派生する場合、Range、Pushback、Notes の単位と条件をどう表現するか。

## ソースメモ

- Raw entrypoint: `raw/web-pages/wiki.supercombo.gg/game-data/manifest.json`
- Canonical raw: `raw/web-pages/wiki.supercombo.gg/game-data/page.raw.wikitext`
- Render evidence: `raw/web-pages/wiki.supercombo.gg/game-data/page.html`, `raw/web-pages/wiki.supercombo.gg/game-data/rendered/main.dom.json`, `raw/web-pages/wiki.supercombo.gg/game-data/rendered/tabbers.dom.json`
- Validation: `raw/web-pages/wiki.supercombo.gg/game-data/validation.json`, `raw/web-pages/wiki.supercombo.gg/game-data/validation.tabbers.json`
- Raw-derived table artifact: `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`
