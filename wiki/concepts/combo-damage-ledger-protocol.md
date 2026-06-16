---
type: concept
title: "Combo Damage Ledger Protocol"
created: 2026-06-16
updated: 2026-06-16
status: active
confidence: medium
sources:
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/juggle-system]]"
  - "[[sources/supercombo-street-fighter-6-game-data]]"
  - "[[sources/supercombo-street-fighter-6-gauges]]"
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[reviews/2026-06-11-jp-year1-od-amnesia-combo-damage-calculation-model-gap]]"
  - "[[reviews/2026-06-15-jp-combo-damage-ledger-regression]]"
  - "[[reviews/2026-06-15-mai-combo-damage-ledger-regression]]"
related:
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/juggle-system]]"
  - "[[outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation]]"
  - "[[reviews/2026-06-15-jp-combo-damage-ledger-regression]]"
aliases:
  - "combo damage ledger"
  - "damage ledger protocol"
  - "コンボダメージ台帳"
tags:
  - sf6
  - combo-damage
  - calculation
---

# Combo Damage Ledger Protocol

## 要約

Exact combo damage は、route text をそのまま damage formula に入れる作業ではない。先に source-backed な hit ledger を作り、その ledger が確定してから `base_damage * condition_multiplier * effective_scaling` を hit ごとに floor して合計する。計算 tool はこの最後の算術だけを deterministic に扱い、route text から hit 順、状態遷移、juggle 条件、距離条件、補正状態を推測しない。

今回の JP `SA2 ラヴーシュカ` route の誤答は、計算式の問題ではなく、hit ledger preflight を省いたことが原因だった。`最速入力`、delayed projectile、portal、target combo、多段技、character-specific scaling が含まれる route では、damage 計算前に hit order proof を作る。

## なぜ最初に計算できなかったか

`5HK > Zilant > SA2 > 5MK > 2HP > weak Departure > 5HP > 236MK > 6HK > 236HP > 236MK > 22P` の誤答では、次の中間層を省略した。

| 見落とし | 何をすべきだったか | そうしていれば |
|---|---|---|
| route text の順番を damaging hit の順番だと扱った | `SA2 ラヴーシュカ` の 4 projectile、`弱ヴィーハト` auto spike、`6HK` / `236HP` の multi-hit split を先に展開する | `2HP` や後続 `5HP` が通常の attack step ではなく、SA2 中の delayed-hit route state で当たることを疑えた |
| `最速入力` を検証条件に使わなかった | startup、cancel timing、scheduled projectile timing、portal auto-hit timing から relative event table を作る | source だけで完全確定できなくても、少なくとも「線形 ledger は未証明」と判断できた |
| `SA2 即時補正25%` を SA2 projectile だけに閉じた | 公式 / community source の補正文と training-mode 表示の per-hit scaling を照合する | `2HP 280 (35%)`、`5HP 200 (25%)`、`236MK 150 (15%)` を ledger に入れられた |
| `6HK` を 300+600 の両 hit として足した | multi-hit 技は実際に damage に入った segment だけを ledger に入れる | `6HK` の 300 damage segment を足して `30` damage 過大にするミスを避けられた |
| 最終 total だけで検証した | hit count、last hit damage、visible per-hit scaling、cumulative total を可能な限り照合する | 誤答 `3695` が複数ミスの相殺で近く見えていることを検出できた |

## Preflight gate

Exact combo damage を回答する前に、次を順番に確認する。

1. **Version / source gate**: 動画日付、patch 指定、current-only 指定を確定する。過去 route なら current frame-data だけでなく Battle Change / Patch Notes を確認する。
2. **Move resolution gate**: 表記を source move に対応させる。target combo follow-up、強度、Modern / Classic、派生、install 中 version、manual / auto activation を分ける。
3. **Non-linear hit gate**: delayed projectile、設置、爆弾、portal、SA projectile、install follow-up、multi-hit、throw into juggle、Drive Rush、Perfect Parry、Counter / Punish Counter があれば、route text の順番を damaging hit 順として使わない。
4. **Hit order proof gate**: `最速入力` や source timing がある場合は、startup / active / cancel window / scheduled hit timing / auto-hit timing から relative event table を作る。cancel anchor、hitstop、距離、juggle height が source にない場合は、その部分を `unknown` として止める。
5. **Attack-step gate**: `hit_index` と `attack_step` を分ける。multi-hit が同じ attack step なのか、source が「各 hit が別 attack」「next attack に extra scaling」と言っているのかを確認する。
6. **Scaling-state gate**: starter、immediate、multiplier、minimum、Drive Rush one-time penalty、Super Art minimum、character-specific scaling、condition multiplier を別列で扱う。
7. **Arithmetic gate**: source-backed ledger ができてから、per-hit floor で合計する。`jq` や combo damage calculator で hit damage list と total を検算する。
8. **Validation gate**: 可能なら training-mode 表示の hit count、last hit damage、visible scaling、cumulative total と照合する。expected total がない場合は、candidate ledger と不確実点を出し、確定値として断定しない。

## Hit order proof の扱い

Hit order proof は、次のどれかで支える。

| Evidence | 扱い |
|---|---|
| training-mode damage display / video frame で per-hit damage, scaling, cumulative が読める | 最も強い実測 validation。raw capture していない場合は human/video validation として明記する |
| source-backed frame simulation で relative hit order が導ける | source fact / derived fact。startup、cancel anchor、scheduled projectile timing、hitstop、距離条件が揃う範囲だけ使う |
| source note が hit order / scaling application を直接説明する | source fact。個別 move note と damage scaling table を citation する |
| route text だけ | 不十分。特に delayed hit、設置、SA/install、multi-hit、juggle、距離依存がある場合は確定 ledger にしない |

`最速入力` は強いヒントだが、単独では hit order proof ではない。最速であるほど frame simulation の前提を置きやすいだけで、cancel 可能 frame、hitstop、projectile 接触 frame、相手位置、juggle height が不足していれば確定しない。

## JP SA2 route での適用例

JP route では、source に次の timing / property があった。

| Move | Relevant source fact |
|---|---|
| `SA2 ラヴーシュカ` | 4 separate 1-hit Super projectiles、projectile sequence timing、`40% Minimum; 25% Starter; 25% Immediate` |
| `弱ヴィーハト` | portal automatic spike は total startup 150f / auto spike timing を持つ delayed hit |
| `6HK` | `300,600` split、2nd hit only cancelable |
| `236HP` | `300,500` split |
| `236MK` | projectile / distance-dependent startup、SA2 active 中は使用制約がある |

この情報だけでも、route text の順番をそのまま damaging hit 順にするのは危険だと分かる。完全な frame simulation には cancel anchor、hitstop、距離、juggle height などの追加条件が必要なため、source だけで確定できない部分は video / training-mode 表示で検証するべきだった。実測では `2HP 280 (35%)`、`5HP 200 (25%)`、`236MK 150 (15%)`、`6HK` は 600 damage segment だけで、total は `3660` だった。詳細は [[reviews/2026-06-15-jp-combo-damage-ledger-regression]]。

## Tooling boundary

`tools.calculations.combo_damage` は route parser ではない。tool が扱うのは、すでに人間または source-backed process で確定した hit ledger の算術だけ。

tool に入れてよいもの:

- per-hit、明示された 1 damage segment、または `damage_granularity: "move_total"` で明示した full move total ごとの base damage、condition multiplier、effective scaling、rounding policy
- 非空 source path、共通 authority field、input hash、calculator version
- `attack_step`、`scaling_note`、`damage_granularity`、`segment_type` などの trace field

tool に入れないもの:

- route text からの hit order 推測
- candidate fixture や working hypothesis の authority
- `hit_span: "10-16"` のような multi-hit subtotal row
- full move total を内部 hit split の modeled ledger と誤読させる trace
- delayed hit の接触 frame 推測
- juggle height / distance / corner state の補完
- source にない internal rule の補完

## Stop conditions

次の条件が 1 つでもあり、hit order proof または training-mode validation がない場合、確定 damage として答えない。

- `最速入力`、`微遅らせ`、`ディレイ` など timing-dependent route
- SA2 / install / 独立 projectile / 設置 / portal / bomb / delayed hit
- target combo と通常技の表記が曖昧
- multi-hit の一部だけが当たる可能性
- juggle state、distance、corner、height、character hurtbox に依存する可能性
- route が過去 patch のもの
- source が community-only で、人間レビューまたは実機表示がない補正 rule

この場合の回答は、「現時点では candidate ledger まで。確定値には per-hit display または追加 source が必要」とする。

## 関連

- [[concepts/terms/damage-scaling]]
- [[concepts/frame-data]]
- [[concepts/juggle-system]]
- [[outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation]]
- [[reviews/2026-06-15-jp-combo-damage-ledger-regression]]
- [[reviews/2026-06-15-mai-combo-damage-ledger-regression]]
