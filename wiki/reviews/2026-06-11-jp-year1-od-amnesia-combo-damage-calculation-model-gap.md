---
type: review
review_type: calculation_model_gap
created: 2026-06-11
updated: 2026-06-11
status: open
severity: P1
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/capcom-official-battle-change-list]]"
  - "[[sources/supercombo-street-fighter-6-patch-notes]]"
related:
  - "[[outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation]]"
  - "[[entities/jp]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/terms/damage-scaling]]"
external_sources:
  - "https://www.youtube.com/shorts/g-m0AFGe4jY"
aliases:
  - "JP Year1 OD Amnesia 5790 damage calculation model gap"
  - "JP Year1 ODアムネジア5790ダメージ計算モデル gap"
tags:
  - review
  - calculation-model-gap
  - combo
  - damage
  - jp
---

# JP Year1 ODアムネジア 5790 damage calculation model gap - 2026-06-11

## 要約

最初の見立てでは、この件を YouTube source 未取り込みによる `evidence_gap` とした。しかし再検証の結果、それは本質ではない。提示された YouTube Short を `yt-dlp` で確認し、repo 内の official / SuperCombo derived JSON と 2024-02-27 Battle Change を使うと、Year1 初期 JP の `ODアムネジア > 立中K > 強ヴィーハト設置 > 中トルバラン > 強トリグラフ > ヴィーハト爆発 > 中トルバラン > OD中強トリグラフ > SA3` は hit-by-hit で 5790 damage まで再計算できる。

問題は source 不足ではなく、combo damage query で delayed hits、patch rollback、Punish Counter multiplier、Super Art minimum scaling を含む hit ledger を作らなかったこと。

詳細計算は [[outputs/reports/2026-06-11-jp-year1-od-amnesia-5790-damage-calculation]] に残す。

## 何を見落としたか

1. `ODアムネジア` は route の開始条件だけではなく、`OD Amnesia Bomb` の 600 damage x2 が delayed hit として入る。動画の `510 (85%)` x2 はこの爆弾であり、これを damage table から落とした。
2. `Year1 初期` という指定に対して、2024-02-27 変更前へ補正値を戻す必要があった。公式 Battle Change は `【通常/OD】アムネジア` の即時補正を `15%=>60%` に変更し、50% starter scaling を追加したと記録している。したがって初期版は current frame-data の `50% Starter; 60% Immediate` ではなく、少なくとも旧 `15% immediate` として計算すべきだった。
3. `立中K` は Punish Counter で raw 600 から 720 になっている。通常技 raw damage だけを見ると 600 で止まり、動画の1段目 720 を説明できない。
4. `OD中強トリグラフ` は 1000 damage の単発ではなく、SuperCombo JSON 上は `500x2`。動画でも `125 (25%)` x2 として入っている。
5. SA3 は combo scaling が 25% まで下がっていても、SA3 の minimum scaling 50% により 4000 * 50% = 2000 が入る。

## 再計算の要点

動画で読める sequence は次の通り。

| Hit | 推定技 | 表示 damage / scaling | 累計 |
|---:|---|---:|---:|
| 1 | 立中K Punish Counter | 720 (100%) | 720 |
| 2 | OD Amnesia Bomb 1 | 510 (85%) | 1230 |
| 3 | OD Amnesia Bomb 2 | 510 (85%) | 1740 |
| 4 | 中トルバラン | 650 (65%) | 2390 |
| 5 | 強トリグラフ | 440 (55%) | 2830 |
| 6 | ヴィーハト爆発 / Departure: Shadow | 360 (45%) | 3190 |
| 7 | 中トルバラン | 350 (35%) | 3540 |
| 8 | OD中強トリグラフ 1 | 125 (25%) | 3665 |
| 9 | OD中強トリグラフ 2 | 125 (25%) | 3790 |
| 10-16 | SA3 | 2000 total (50% minimum) | 5790 |

`jq -n '[720,510,510,650,440,360,350,125,125,2000] | add'` は `5790` を返す。

## 根本原因

根本原因は、repo に必要な数値が存在したかどうかではなく、回答側がそれらを組み合わせる手順を持っていなかったこと。

- route text を「技名列」として扱い、delayed projectile / bomb / portal hit を自動的に damage ledger へ展開しなかった。
- current frame-data を見たあと、Battle Change から version-specific scaling を逆算する pass を入れなかった。
- combo damage の質問なのに、hit-by-hit の `base damage * condition multiplier * scaling` 表を作らなかった。
- exact damage を聞かれているのに、動画/トレモ表示と repo JSON の arithmetic reconciliation を実行せず、route family evidence から range を出した。

## 必要な改善

1. exact damage query では、回答前に必ず hit ledger を作る。各行は `move`, `source damage`, `condition multiplier`, `effective scaling`, `hit damage`, `cumulative damage`, `source path` を持つ。
2. route に `ODアムネジア`、爆弾、設置、罠、追加入力、Super cancel が含まれる場合、非明示の delayed hit を SuperCombo `damage` / `notes` から展開する。
3. `Year1`、`初期`、`patch前` の指定がある場合、Battle Change の before/after を使って current frame-data をその時点へ戻す。
4. Super Art を含む場合、minimum scaling を通常 scaling より優先して計算する。
5. 再発防止として、この route を combo damage calculator の regression fixture にする。汎用 tool 化する場合は、まず手書き hit ledger を入力にする deterministic calculator から始める。

## 未解決の質問

- 通常 combo hit scaling の基礎表を、どの source を正として wiki に取り込むか。
- YouTube Shorts の動画フレームを raw source として保存する policy を定義するか。それとも外部動画は review note の verification evidence に留めるか。
