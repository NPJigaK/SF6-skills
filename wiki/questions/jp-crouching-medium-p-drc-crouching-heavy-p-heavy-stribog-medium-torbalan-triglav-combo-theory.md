---
type: question
created: 2026-06-08
updated: 2026-06-10
status: active
question: "JPのしゃがみ中P＞キャンセルラッシュ＞しゃがみ強P＞強ストリボーグ＞中トルバラン＞トリグラフは、なぜ理論上つながる？"
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/supercombo-jp-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/capcom-official-battle-change-list]]"
related:
  - "[[entities/jp]]"
  - "[[concepts/frame-data]]"
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[concepts/terms/drive-rush-cancel]]"
  - "[[concepts/terms/cancel]]"
  - "[[concepts/terms/frame-advantage]]"
  - "[[concepts/terms/wall-bounce]]"
  - "[[concepts/terms/damage-scaling]]"
tags:
  - sf6
  - frame-data
  - jp
  - combos
  - drive-rush
  - juggles
---

# 質問: JPのしゃがみ中P＞キャンセルラッシュ＞しゃがみ強P＞強ストリボーグ＞中トルバラン＞トリグラフは、なぜ理論上つながる？

## 答え

このルートは、全部を地上リンクとしてつないでいるわけではない。構造は次の4段階。

1. `しゃがみ中P` は `C` 対応なので、ヒット時にキャンセルドライブラッシュへ移れる。
2. キャンセルドライブラッシュ後の `しゃがみ強P` は Drive Rush 強化通常技として出るため、通常より `+4F` 有利が増え、次の `強 ストリボーグ` へのキャンセルが成立しやすくなる。
3. `しゃがみ強P` → `強 ストリボーグ` はリンクではなく `C` の必殺技キャンセル。`強 ストリボーグ` はヒット時に壁バウンド / limited juggle 状態を作る。
4. `中 トルバラン` → `トリグラフ` は、地上硬直差のリンクではなく、空中の相手を projectile と juggle limit で拾う部分。

つまり前半はキャンセルDRの補正とキャンセル、後半は強ストリボーグからの limited juggle が本体。

## 該当技の値

公式 Classic 値と SuperCombo 補助値を合わせると、重要な値は次の通り。

| 技 | 公式: 発生 | 公式: ヒット時 | 公式: キャンセル | SuperCombo 補助 |
|---|---:|---:|---|---|
| しゃがみ中P（ズミヤー） | 7F | +6F | C | DR / 必殺技キャンセルは active 後に遅れて可能 |
| キャンセルドライブラッシュ | - | - | ※ | 最速で9F後に攻撃でキャンセル可能。通常技 / 特殊技は +4F 有利と juggle 性能強化 |
| しゃがみ強P（マリートヴァ） | 9F | +1F | C | Drive Rush route で使いやすい。juggle potential が高い |
| 強 ストリボーグ | 28F | D | SA3 | KD +67(+87)。2段目が wall bounce / limited juggle を作る |
| 中 トルバラン | 26F | +6F | SA3 | 空中相手への juggle start、juggle limit 10 |
| トリグラフ | 22F | D | SA3 | button 強度で位置が変わる。juggle limit 26 |

`C` は公式説明上、必殺技、ドライブインパクト、ドライブラッシュ、SAでキャンセル可能という意味。

## しゃがみ中PからDRしゃがみ強Pがつながる理由

`しゃがみ中P` は通常ヒット `+6F`、`しゃがみ強P` は発生 `9F`。素のリンクなら、

```text
しゃがみ中P ヒット時有利: +6F
しゃがみ強P 発生:          9F
素のリンク判定:            +6F - 9F = -3F
```

なので足りない。

ここで使っているのが `C` からのキャンセルドライブラッシュ。SuperCombo 側の補助値では、
Drive Rush Cancel は最速で9F後に攻撃でキャンセルでき、公式側でもキャンセルDRは暗転9F、
10F目から攻撃行動にキャンセル可能と記録されている。

`しゃがみ中P` は発生7F、持続7-10F、硬直14F、ヒット+6F。単純化して見ると、ヒット後の
相手の硬直は「残り持続 + 硬直 + ヒット有利」で見積もれる。

```text
しゃがみ中Pが最終持続で当たった場合の概算:
残り持続 0F + 硬直 14F + ヒット有利 6F = 20F

DRCからしゃがみ強P初段までの概算:
DRC攻撃可能まで 9F + しゃがみ強P発生 9F = 18F
```

最終持続ヒットでも概算上は `20F - 18F = 2F` 程度残る。最初の持続で当たる場合は、
active 終了まで待つ分を含めても概算上まだ間に合う。したがって、ここは通常リンクではなく
「キャンセルDRで動作を切り、DRCから最速通常技を出す」ことで成立する。

## DRしゃがみ強Pから強ストリボーグがつながる理由

`しゃがみ強P` は通常ヒット `+1F`、`強 ストリボーグ` は発生 `28F`。素のリンクなら当然無理。

```text
しゃがみ強P ヒット時有利: +1F
強ストリボーグ 発生:       28F
素のリンク判定:            +1F - 28F = -27F
```

ここは `しゃがみ強P` の `C` から必殺技キャンセルしている。さらに、直前が Drive Rush Cancel
なので `しゃがみ強P` は Drive Rush 強化通常技として扱われ、SuperCombo の説明では通常技 /
特殊技に `+4F` 有利と juggle 性能強化が付く。

この `+4F` がかなり重要。`しゃがみ強P` は発生9F、持続9-14F、硬直20F、通常ヒット+1F。
最初の持続で当たったと仮定すると、出し切り時の相手硬直は概算で次のようになる。

```text
通常しゃがみ強P:
残り持続 5F + 硬直 20F + ヒット有利 1F = 26F

DRしゃがみ強P:
残り持続 5F + 硬直 20F + (ヒット有利 1F + DR補正 4F) = 30F

強ストリボーグ:
発生 28F
```

素の `しゃがみ強P` からだと `26F` で足りないが、DR強化後は概算 `30F` になり、
`強 ストリボーグ` の28Fが間に合う。このルートで `キャンセルラッシュ＞しゃがみ強P` を挟む
意味は、単なる距離詰めではなく、この `+4F` と juggle 性能強化にある。

## 強ストリボーグ以降は地上リンクではない

`強 ストリボーグ` 以降は、通常の地上ヒット有利でつなぐ話から外れる。

SuperCombo 補助値では、`強 ストリボーグ` は `KD +67(+87)`、2段目が相手を wall bounce /
limited juggle にする。さらに、2段目は1段目より長く、1段目が当たると2段目がコンボ安定用に
拡大する、と説明されている。

ここからの `中 トルバラン` は、相手が浮いているあいだに ghost projectile を重ねて拾う部分。
`中 トルバラン` は公式上は密着発動時26F、SuperCombo では `14+12` と分解され、空中相手への
juggle start と `juggle limit 10` を持つ。2026-03-17 の公式変更リストでも、中・強・OD
トルバランの飛び道具が攻撃動作へ移るサーチ範囲を上方向に拡大し、空中コンボで空振りする
現象を緩和したと記録されている。

`中 トルバラン` の地上ヒット時有利は `+6F` なので、地上リンクとして `トリグラフ` 発生22Fを
つなぐことはできない。

```text
中トルバラン 地上ヒット時有利: +6F
トリグラフ 発生:              22F
地上リンク判定:               +6F - 22F = -16F
```

成立する理由は、`中 トルバラン` が空中の limited juggle 相手に当たり、そこから
`トリグラフ` の高い `juggle limit 26` でさらに拾えるから。`トリグラフ` は弱・中・強で
フレーム値は同じだが、SuperCombo 側では LP が近距離、MP が中距離、HP が遠距離の spike 位置を
選ぶと説明されている。したがって、このルートの最後の `トリグラフ` は、フレーム理論上は
どの強度も同じ22F / JL26だが、実戦では浮き位置と距離に合う強度を選ぶ必要がある。

## まとめ

このコンボを数式だけで見るなら、成立点は3つ。

```text
1. 2MP raw +6 から 2HP 9F は素リンク不可
   → C からキャンセルDR。DRC最速攻撃可能9Fを使って 2HP を出す。

2. 2HP raw +1 から 強ストリボーグ 28F は素リンク不可
   → DR通常技の +4F と C 必殺技キャンセルで間に合わせる。

3. 強ストリボーグ後の 中トルバラン > トリグラフ は地上リンク不可
   → 強ストリボーグの wall bounce / limited juggle を、Torbalan JL10 と Triglav JL26 で拾う。
```

## 注意 / 不確実性

- JP 公式フレームデータは 2026-05-26 capture。2026-05-28 公式変更リストでは、このルートの主要通常技・強ストリボーグ・中トルバラン・トリグラフのフレーム値を直接変える変更は確認していない。
- 2026-03-17 変更リストには、中・強・ODトルバランの上方向サーチ範囲拡大があり、このルートの空中拾い安定性に関係する。
- SuperCombo の `Juggle Start / Increase / Limit` は community source の補助値。公式表と重なる発生・硬直差などの基本値は Capcom 公式 data を優先する。
- 実戦では距離、画面端か中央か、`強 ストリボーグ` の何段目・どの高さで当たったか、最後の `トリグラフ` の強度選択で成否が変わる。

## 根拠

- [[sources/capcom-official-jp-frame-data]]
- [[sources/supercombo-jp-frame-data]]
- [[sources/supercombo-street-fighter-6-glossary]]
- [[sources/capcom-official-battle-change-list]]
- [[concepts/frame-data]]
- [[concepts/drive-system]]
- [[concepts/juggle-system]]
- `wiki/outputs/data/frame-data/official/jp/classic.json`
- `wiki/outputs/data/frame-data/supercombo/jp/frames.json`
- `wiki/outputs/data/frame-data/official-supercombo-enriched/jp/classic-supercombo.json`
- `wiki/outputs/data/battle-change/official/changes.json`
