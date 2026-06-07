---
type: review
review_type: prereview
created: 2026-06-02
status: open
sources:
  - "[[sources/supercombo-ingrid-frame-data]]"
  - "[[sources/capcom-official-ingrid-frame-data]]"
related:
  - "[[reviews/2026-06-02-supercombo-ingrid-frame-data-capture-review]]"
  - "[[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]]"
  - "[[entities/ingrid]]"
  - "[[concepts/frame-data]]"
external_sources:
  - "https://twistedvoxel.com/street-fighter-6-players-discover-secret-method-to-unlock-dark-ingrid-transformation/"
  - "https://www.reddit.com/r/StreetFighter/comments/1trzius/play_as_dark_ingrid_see_description_for/"
  - "https://streetfighter.fandom.com/wiki/Dark_Ingrid"
  - "https://streetfighter.fandom.com/wiki/Monoid"
  - "https://steamcommunity.com/app/1364780/allnews/"
  - "https://news.capcomusa.com/go/network/media"
  - "https://ultimateframedata.com/sf6/ingrid"
aliases:
  - "SuperCombo Ingrid SuperCombo-only prereview"
  - "Ingrid SuperCombo-only 事前レビュー"
tags:
  - review
  - prereview
  - frame-data
  - supercombo
  - hidden-command
  - taunt-summon
  - community-only
  - nonstandard
---

# SuperCombo Ingrid SuperCombo-only 9 行 事前レビュー - 2026-06-02

## 位置づけ

これは accept ではない。`supercombo-only.csv` にある公式 row 非対応の 9 行について、外部 web evidence も使って事前レビューした記録である。`human_review_status`、`human_review_decision`、公式 row への照合、補助列付き output の accepted 判定は変更しない。

対象は `wiki/outputs/data/frame-data/official-supercombo-enriched/ingrid/supercombo-only.csv` のうち、`suggested_handling` が `supercombo_only` の 9 行。4 件の taunt row は対象外だが、`ingrid_4pppkkk` Back Taunt は Monoid と Shin Ingrid の enable condition として参照する。

この repo の現段階では、domain-specific な answer policy field や新しい community-extra schema は導入しない。通常の Ingrid frame-data への質問では、Capcom 公式 row と公式 row に紐づく補助列付き output を優先し、この 9 行は「特殊隠しコマンド / taunt-summon が明示された質問」でだけ参照する補足 evidence として扱う。

## ローカル根拠

- [[outputs/reports/2026-06-02-ingrid-official-supercombo-enriched-data]] では、公式 Classic 75 rows を正として保持し、SuperCombo row は 83 rows。公式に照合できない `supercombo_only` は 9 行、`supercombo_only_taunt` は 4 行。
- [[sources/capcom-official-ingrid-frame-data]] の公式 Classic row には、Monoid 関連、Big Laser?、Burnout Attack?、Sun Octopus? に相当する row は見当たらない。
- [[sources/supercombo-ingrid-frame-data]] 由来の Back Taunt note は、Monoid 召喚、Monoid 操作、`LP~LP~4~LK~HK` による Shin Ingrid 変身、`22PPP` / `214214K` / `360+KK` の追加技を説明している。
- したがって、9 行は公式フレーム表の通常 move row ではなく、hidden-command / taunt-summon / community-only data として既存の `supercombo-only.csv` に隔離して扱うのが現時点の安全な読み。

## Web evidence

| Source | 確認できたこと | このレビューでの扱い |
|---|---|---|
| [Capcom News](https://news.capcomusa.com/go/network/media) / [Steam Community official announcements](https://steamcommunity.com/app/1364780/allnews/) | Ingrid の配信、World Tour、通常の kit 紹介、Sun Crest などは公式 announcement 上で確認できる。調査範囲では hidden 9 行に相当する move list / frame-data 記載は見つからなかった。 | 公式側の通常掲載範囲を示す negative evidence。hidden 9 行の受理根拠にはしない。 |
| [Twisted Voxel](https://twistedvoxel.com/street-fighter-6-players-discover-secret-method-to-unlock-dark-ingrid-transformation/) | community discovery として、Back+Taunt から Monoid を経由する Dark Ingrid 変身、`22+PPP`、`214214+K`、`412369+KK` の報告を掲載している。 | Shin/Dark Ingrid 追加技の存在を補強する secondary evidence。フレーム値や正式名称の受理根拠にはしない。 |
| [Reddit r/StreetFighter](https://www.reddit.com/r/StreetFighter/comments/1trzius/play_as_dark_ingrid_see_description_for/) | プレイヤー投稿として、Monoid 召喚後の手順、`22+PPP`、`214214+K`、`412369+KK`、およびコメントで `LP > LP > 4 > LK > HK` や 360 系入力の補足がある。 | 発見経路と入力差分の参考。一次検証ではなく、accept には使わない。 |
| [Street Fighter Wiki - Dark Ingrid](https://streetfighter.fandom.com/wiki/Dark_Ingrid) | community wiki として、Dark Ingrid、Avatar Arcade boss、Sun Octopus、Burnout 付与 special、強化 Sun Flare などを説明している。 | 名称・存在の補強候補。ただし community wiki なので公式扱いしない。 |
| [Street Fighter Wiki - Monoid](https://streetfighter.fandom.com/wiki/Monoid) | Monoid が SF6 の Ingrid 周辺に登場する存在であることを説明している。 | Monoid 行を Back Taunt 周辺の extra action と見る補助根拠。フレーム値の根拠にはしない。 |
| [Ultimate Frame Data - Ingrid](https://ultimateframedata.com/sf6/ingrid) | Ingrid frame data と hitbox が公開されているが、調査時点のページ検索では Monoid / Laser / Burnout / Octopus / Taunt に相当する項目は見つからなかった。 | 別 community frame-data site でも通常掲載範囲から外れている可能性を示す弱い negative evidence。 |

## 行別事前レビュー

| move_id | SuperCombo name | local condition | external support | prereview classification | risk |
|---|---|---|---|---|---|
| `ingrid_22ppp` | Big Laser? | Shin Ingrid only。Back Taunt 経由の変身後に `22PPP`。 | Twisted Voxel と Reddit が `22+PPP` の large beam を報告。Dark Ingrid wiki も強化 beam 系を説明。 | `prereview_hidden_art_candidate` | 高。名称末尾の `?`、公式 frame row 不在、frame 値は SuperCombo-only。 |
| `ingrid_214214k` | Burnout Attack? | Shin Ingrid only。Back Taunt 経由の変身後に `214214K`。 | Twisted Voxel と Reddit が burnout 付与技を報告。Dark Ingrid wiki も burnout 付与 special を説明。 | `prereview_hidden_art_candidate` | 高。正式名称未確定、公式 frame row 不在、frame 値は SuperCombo-only。 |
| `ingrid_360kk` | Sun Octopus? | Shin Ingrid only。command grab Super。 | Twisted Voxel / Reddit は `412369+KK`、Reddit comment は 360 系入力と補足。Dark Ingrid wiki は Sun Octopus を exclusive Level 2 Super Art と説明。 | `prereview_hidden_super_candidate` | 中-高。入力表記 `360+KK` と `412369+KK` の扱い、公式 frame row 不在、正式な playable/hidden condition の範囲が未確定。 |
| `ingrid_monoid_l` | Monoid Low Dive | Back Taunt で Monoid を召喚した後の Monoid 操作。 | Monoid wiki は SF6 の Ingrid 周辺存在として Monoid を説明。Reddit/Twisted Voxel は変身経路で Monoid を参照。 | `prereview_taunt_summon_subaction` | 高。存在条件は補強されるが、技名・frame 値は SuperCombo-only。 |
| `ingrid_monoid_m` | Monoid Overhead Hammer | Back Taunt Monoid 操作。 | 同上。 | `prereview_taunt_summon_subaction` | 高。 |
| `ingrid_monoid_h` | Monoid Star Thrust | Back Taunt Monoid 操作。 | 同上。 | `prereview_taunt_summon_subaction` | 高。 |
| `ingrid_monoid_hphk` | Monoid Beam | Back Taunt Monoid 操作。 | 同上。 | `prereview_taunt_summon_subaction` | 高。 |
| `ingrid_monoid_jx` | Monoid Aerial Strike | Back Taunt Monoid 操作。 | 同上。 | `prereview_taunt_summon_subaction` | 高。 |
| `ingrid_monoid_super` | Monoid Super | Back Taunt Monoid 操作。hit 時の high-five と Shin Ingrid 変身入力に関係。 | Reddit/Twisted Voxel は high-five/Monoid 経由の変身を報告。 | `prereview_taunt_summon_subaction_or_hidden_transform_route` | 高。SuperCombo-only で、公式 frame row や正式名称の裏取りが不足。 |

## 事前結論

現時点では、9 行の「存在条件」については外部 community evidence が複数あり、特に Shin/Dark Ingrid 変身後の `22PPP`、`214214K`、`360/412369+KK` については SuperCombo の note と外部報告が整合する。一方で、公式 frame-data への掲載、正式名称、フレーム値、hitbox 画像の裏取りは不足している。

推奨は次の通り。

1. 9 行は `supercombo-only.csv` に隔離したまま維持する。
2. `human_review_status: accepted` にはしない。
3. 公式 Ingrid Classic enriched rows へ統合しない。
4. 通常の frame-data 質問では回答に混ぜない。ユーザーが hidden / Dark / Shin Ingrid / Monoid / taunt-summon / SuperCombo-only を明示した場合だけ参照する。
5. 読者向けに出す場合は `SuperCombo-only / hidden-command / taunt-summon / prereview` と明示し、公式値ではないことを表示する。
6. 現段階では新 schema を作らず、既存の `supercombo-only.csv` と `suggested_handling`、この review note の tags / 説明で分離する。より強い分類が必要になった場合だけ、後続の domain design step として検討する。

## 人間判断が必要な点

- hidden / Dark / Shin Ingrid と Monoid 操作 row を reader-facing data として公開する場合、通常の Ingrid frame-data とは分けて表示するか。
- 「存在条件」は community evidence で暫定掲載し、フレーム値は SuperCombo-only として pending に分けるか。
- 既存の `suggested_handling` の `supercombo_only` を、将来 `supercombo_only_hidden_command` や `supercombo_only_taunt_summon` のように細分化する必要があるか。
- accept 前に Capcom 公式動画、公式 command list、in-game training/frame meter で追加検証するか。

## 未解決事項

- Big Laser?、Burnout Attack?、Sun Octopus? は正式名称なのか、SuperCombo 上の説明名なのか。
- `360+KK` と `412369+KK` は同じ 360 系入力の表記差として扱ってよいか。
- Monoid 5 attack と Monoid Super の frame 値は、実測なのか、ゲームデータ抽出なのか、wiki 編集者の暫定値なのか。
- `imageinfo` missing 156 件のうち、これら hidden / Monoid rows の hitbox image を再解決できるか。
