---
type: output
output_type: report
title: "JP Year1 ODアムネジア 5790 damage calculation"
created: 2026-06-11
updated: 2026-06-16
status: active
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
related:
  - "[[reviews/2026-06-11-jp-year1-od-amnesia-combo-damage-calculation-model-gap]]"
  - "[[entities/jp]]"
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/juggle-system]]"
external_sources:
  - "https://www.youtube.com/shorts/g-m0AFGe4jY"
tags:
  - sf6
  - jp
  - combo
  - damage
  - report
---

# JP Year1 ODアムネジア 5790 damage calculation - 2026-06-11

## 結論

JP の Year1 初期ルート `ODアムネジア > 立中K > 強ヴィーハト設置 > 中トルバラン > 強トリグラフ > ヴィーハト爆発 > 中トルバラン > OD中強トリグラフ > SA3` は、SA3 を source-backed full move total として扱う ledger で 5790 damage まで照合できる。

この 5790 は、外部動画を覚える必要がある値ではない。repo 内の JP frame-data、SuperCombo 補助値、2024-02-27 Battle Change の補正変更から再計算できる。

2026-06-16 追記: この route は legacy regression fixture として `tests/calculations/combo_damage/fixtures/jp/classic/2024-02-24-od-amnesia-5790.ledger.json` に保持する。ただし SA3 内部 hit split は modeled としない。SA3 は `damage_granularity: "move_total"` / `segment_type: "super_art_full_move_total"` の source-backed full move total として扱う。

## Video verification

`yt-dlp 2026.06.09` で `https://www.youtube.com/shorts/g-m0AFGe4jY` を確認した。

| Field | Value |
|---|---|
| Title | 【スト6】Year1で遊んでみた！今だから笑える初期JPのぶっ壊れ技 |
| Uploader | ACQUA |
| Upload date | 2026-04-30 |
| Duration | 25 seconds |

動画フレームでは、2.5s 付近から実ダメージが表示され、14.9-15.0s 付近で `16 HITS`、現在 hit `1000 (50%)`、combo damage `5790` が読める。

## Hit ledger

この表の SA3 部分は training-mode 表示から読める total reconciliation であり、SA3 内部 hit split の per-hit ledger ではない。fixture では full move total segment として明示する。

| Hit | Time | 技 | Raw / 条件 | 表示 scaling | Hit damage | Cumulative |
|---:|---:|---|---:|---:|---:|---:|
| 1 | 2.5s | 立中K Punish Counter | 600 * 1.2 | 100% | 720 | 720 |
| 2 | 3.0s | OD Amnesia Bomb 1 | 600 | 85% | 510 | 1230 |
| 3 | 3.5s | OD Amnesia Bomb 2 | 600 | 85% | 510 | 1740 |
| 4 | 4.5s | 中トルバラン | 1000 | 65% | 650 | 2390 |
| 5 | 5.0s | 強トリグラフ | 800 | 55% | 440 | 2830 |
| 6 | 5.5s | ヴィーハト爆発 / Departure: Shadow | 800 | 45% | 360 | 3190 |
| 7 | 6.0s | 中トルバラン | 1000 | 35% | 350 | 3540 |
| 8 | 6.5s | OD中強トリグラフ 1 | 500 | 25% | 125 | 3665 |
| 9 | 7.0s | OD中強トリグラフ 2 | 500 | 25% | 125 | 3790 |
| 10-15 | 13.8s | SA3 small hits subtotal | 2000 | 50% minimum | 1000 | 4790 |
| 16 | 14.9s | SA3 final hit | 2000 | 50% minimum | 1000 | 5790 |

検算:

```text
720 + 510 + 510 + 650 + 440 + 360 + 350 + 125 + 125 + 2000 = 5790
```

`jq -n '[720,510,510,650,440,360,350,125,125,2000] | add'` でも `5790` を確認した。

## Source mapping

| 計算要素 | repo evidence |
|---|---|
| `立ち中K` raw 600 | `wiki/outputs/data/frame-data/official/jp/classic.json`: `move_name == "立ち中K（ウームヌィ・ウダール）"` |
| `OD Amnesia Bomb` 600x2 | `wiki/outputs/data/frame-data/supercombo/jp/frames.json`: `move_id == "jp_22kk_bomb"` |
| Year1 初期の ODアムネジア即時補正 15% | `wiki/outputs/data/battle-change/official/change-events.json`: `20240227` の `【通常/OD】アムネジア` が `即時補正を15％⇒60％` と記録 |
| `中トルバラン` raw 1000 | `wiki/outputs/data/frame-data/official/jp/classic.json`: `move_name == "中 トルバラン"` |
| `強トリグラフ` raw 800 | `wiki/outputs/data/frame-data/official/jp/classic.json`: `move_name == "強 トリグラフ"` |
| `Departure: Shadow` raw 800 | `wiki/outputs/data/frame-data/supercombo/jp/frames.json`: `move_id == "jp_214p_214hp"` |
| `OD Triglav` 500x2 | `wiki/outputs/data/frame-data/supercombo/jp/frames.json`: `move_id == "jp_22pp"` |
| SA3 raw 4000 / minimum 50% | `wiki/outputs/data/frame-data/official/jp/classic.json`: `move_name == "SA3 ザプリェット"`; SuperCombo `move_id == "jp_236236k"` |

## Scaling reconstruction

動画の表示 scaling は `100, 85, 85, 65, 55, 45, 35, 25, 25, SA3 50% minimum`。

重要なのは、`ODアムネジア` を route starter として読むだけでは足りないこと。OD版は Bomb が 600x2 の delayed hit として入り、Year1 初期では 2024-02-27 変更前の 15% immediate scaling を持つ。これにより、通常の hit-count scaling 側が `85,85,65,55,45,35,25,25` として現れる。

SA3 は通常 scaling が 25% まで落ちても、minimum scaling 50% が優先されるため、4000 * 50% = 2000 が入る。

## Root cause

前回の失敗は evidence shortage ではなく arithmetic workflow failure。

- delayed hit を route から展開しなかった。
- `Year1 初期` に対して Battle Change before value を適用しなかった。
- `立中K` の Punish Counter 1.2倍を計算に入れなかった。
- `OD中強トリグラフ` を 500x2 として扱わず、SA3 minimum 50% も計算表に落とさなかった。
- exact damage を問われているのに、hit-by-hit ledger を作らず、近い route evidence から range を出した。

## Reuse rule

今後、exact combo damage を回答する場合は、先に次の表を作る。

| Required field | Description |
|---|---|
| `hit_index` | damaging hit index。非明示の bomb / portal / projectile hit も含める。 |
| `move` | 技名。route text と internal hit を分ける。 |
| `base_damage` | official または SuperCombo derived JSON から取る。 |
| `version_adjustment` | patch before/after から戻す値。 |
| `condition_multiplier` | Punish Counter、Modern、Perfect Parry など。 |
| `effective_scaling` | hit-count scaling、starter / immediate / multiplier、Super Art minimum を適用した最終率。 |
| `hit_damage` | `base_damage * condition_multiplier * effective_scaling`。 |
| `cumulative` | 合計。 |

この route は、`tools/calculations/combo_damage/` の deterministic regression fixture として保持する。ただし SA3 は source-backed full move total segment として扱い、SA3 small hits の内部 breakdown までは modeled としない。model-gap observation としても、delayed hit、patch rollback、PC倍率、SA最低保証を見落とさないための反省材料にする。
