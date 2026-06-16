---
type: review
review_type: calculation_model_gap
title: "JP combo damage ledger regression"
created: 2026-06-15
updated: 2026-06-15
status: active
confidence: medium
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-game-data]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/terms/punish-counter]]"
related:
  - "[[entities/jp]]"
  - "[[concepts/terms/damage-scaling]]"
external_sources:
  - title: "これ一本で全てわかるJPコンボ講座【りゅうせい・スト６】"
    url: "https://www.youtube.com/watch?v=nyFNgnzjV3M"
    published_at: 2025-10-25
tags:
  - sf6
  - review
  - combo-damage
  - jp
---

# JP combo damage ledger regression

## Finding

JP Classic の `5HP PC > PDR 5HP > 236HP > 236MK > 22PP > 22P` は、`5HP` の `20% Starter` とコンボ中 Drive Rush の one-time `15%` penalty を両方 ledger に明示すれば、training-mode 表示の `3178` damage と一致する。

どちらかを落とすと、計算結果は別値になる。`5HP` starter scaling を落とすと `3620`、mid-combo Drive Rush penalty を落とすと `3580` になるため、この route は starter scaling と Drive Rush multiplier の合成を検証する回帰ケースとして使える。

同じ動画の `5HK > Zilant > SA2 > 5MK > 2HP > weak Departure > 5HP > 236MK > 6HK > 236HP > 236MK > 22P` は、JP `SA2 ラヴーシュカ` の `即時補正25%` を delayed-hit route の ledger に明示する回帰ケースとして使える。動画 12:25 付近の training-mode 表示は `3660` damage で、`2HP` が `280 (35%)`、後続 `5HP` が `200 (25%)`、中トルバランが `150 (15%)` になる。これらを通常補正または SA2 弾だけの補正として扱うと別値になる。

## Regression case

ユーザー提示の training-mode 検証値は [YouTube video](https://www.youtube.com/watch?v=nyFNgnzjV3M) とスクリーンショット由来。`yt-dlp` metadata で title `これ一本で全てわかるJPコンボ講座【りゅうせい・スト６】`、`upload_date: 20251025` を確認した。動画・画像はこの review では raw capture として ingest していないため、damage 表示の authority は `human-provided validation` に留める。

| Route | Correct total | Ledger fixture |
|---|---:|---|
| `5HP PC > PDR 5HP > 236HP > 236MK > 22PP > 22P` | `3178` | `tests/calculations/combo_damage/fixtures/jp/classic/2025-10-25-5hp-pc-3178.ledger.json` |
| `5HK > Zilant > SA2 > 5MK > 2HP > weak Departure > 5HP > 236MK > 6HK > 236HP > 236MK > 22P` | `3660` | `tests/calculations/combo_damage/fixtures/jp/classic/2025-10-25-5hk-3660.ledger.json` |

## Correct scaling interpretation

| Hit | Move | Scaling | Damage |
|---:|---|---:|---:|
| 1 | `5HP Punish Counter` | `100% * 1.2` | `960` |
| 2 | `PDR 5HP` | `80% * 0.85 = 68%` | `544` |
| 3.1 | `236HP Stribog hit 1` | `70% * 0.85 = 59%` | `177` |
| 3.2 | `236HP Stribog hit 2` | `59%` | `295` |
| 4 | `236MK Torbalan` | `60% * 0.85 = 51%` | `510` |
| 5.1 | `22PP OD Triglav hit 1` | `50% * 0.85 = 42%` | `210` |
| 5.2 | `22PP OD Triglav hit 2` | `42%` | `210` |
| 6 | `22P Triglav` | `40% * 0.85 = 34%` | `272` |

`jq -n '[960,544,177,295,510,210,210,272] | add'` は `3178` を返す。

## SA2 delayed-hit route

動画 12:25 付近の training-mode 表示から読める hit damage は次の通り。

| Hit | Move | Displayed scaling | Damage | Cumulative |
|---:|---|---:|---:|---:|
| 1 | `5HK` | `100%` | `800` | `800` |
| 2 | `5HK~HP Zilant` | `100%` | `500` | `1300` |
| 3 | `5MK` | `80%` | `480` | `1780` |
| 4 | `SA2 Lovushka projectile 1` | `45%` | `225` | `2005` |
| 5 | `SA2 Lovushka projectile 2` | `45%` | `225` | `2230` |
| 6 | `2HP` | `35%` | `280` | `2510` |
| 7 | `SA2 Lovushka projectile 3` | `40%` | `200` | `2710` |
| 8 | `SA2 Lovushka projectile 4` | `40%` | `200` | `2910` |
| 9 | `5HP` | `25%` | `200` | `3110` |
| 10 | `236MK Torbalan` | `15%` | `150` | `3260` |
| 11 | `weak Departure auto spike` | `10%` | `80` | `3340` |
| 12 | `6HK Bylina 600-damage segment` | `10%` | `60` | `3400` |
| 13 | `236HP Stribog hit 1` | `10%` | `30` | `3430` |
| 14 | `236HP Stribog hit 2` | `10%` | `50` | `3480` |
| 15 | `236MK Torbalan` | `10%` | `100` | `3580` |
| 16 | `22P Triglav` | `10%` | `80` | `3660` |

`jq -n '[800,500,480,225,225,280,200,200,200,150,80,60,30,50,100,80] | add'` は `3660` を返す。

この route では、`SA2 ラヴーシュカ` の `即時補正25%` を「SA2 弾だけ」として閉じると、`2HP` / `5HP` / `236MK` の補正が高くなりすぎる。また `6HK` は 900 damage の両 hit ではなく、600 damage segment だけを ledger に入れる。`6HK` の 300 damage segment を足すと `30` damage 分だけ過大になる。

## Version note

動画投稿日は `2025-10-25`。SuperCombo Patch Notes の JP 関連 event では、route 使用技に対して `2025-10-25` 以後の damage / starter scaling 変更は見つけていない。`2026-03-17` の `MK/HK/OD Torbalan` 変更は juggle 中の whiff 防止に関する vertical detection range 変更であり、この fixture の damage arithmetic には使わない。

## Guardrail

`tools.calculations.combo_damage` は route parser ではない。`5HP` starter scaling、PDR による mid-combo Drive Rush penalty、`236HP` / `22PP` の multi-hit split は、ledger 側で source-backed に展開する。

## Evidence gaps

- YouTube / スクリーンショットは今回 raw package として保存していない。外部動画を durable validation source にする場合は、別途 raw capture policy と manifest を整備する。
- 最後の `トリグラフ` は入力強度が route text では曖昧だが、Capcom official / SuperCombo とも通常 `22P` の damage は強度にかかわらず `800` のため、damage ledger では `22P` として扱う。
