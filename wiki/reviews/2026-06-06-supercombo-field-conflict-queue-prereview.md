---
type: review
review_type: prereview
created: 2026-06-06
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-frame-data-batch]]"
related:
  - "[[outputs/reports/2026-06-05-supercombo-all-frame-data-coverage]]"
  - "[[reviews/2026-06-05-supercombo-all-frame-data-capture-review]]"
  - "[[concepts/frame-data]]"
  - "[[entities/supercombo-wiki]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "SuperCombo field_conflict queue prereview"
  - "SuperCombo field_conflict キュー事前レビュー"
tags:
  - review
  - frame-data
  - supercombo
  - prereview
---

# SuperCombo field_conflict キュー事前レビュー - 2026-06-06

## 要約

`enrichment_review_queues == field_conflict` 単独の 11 行を確認した。結論として、現時点で追加の自動 accept に進める行はない。

ただし 11 行は同じ理由ではない。Jamie の 4 行は SuperCombo notes が酔いLv別 damage を明示しており、単純な source conflict というより条件付き damage scaling として別 queue に分ける余地がある。Terry の 2 行は jump MP / jump MK の active と damage が相互に入れ替わっているように見えるため、source 側の行取り違えまたは version 差の確認が必要。

## 集計

| 分類 | 行数 | 方針 |
|---|---:|---|
| 条件付き damage scaling らしい行 | 4 | accept しない。`condition_dependent_field` 相当へ分離できるか検討する。 |
| 通常の source conflict | 6 | Capcom 公式を正とし、SuperCombo 補助値は pending のまま残す。 |
| 既存レビュー済み conflict | 1 | 既存 accepted decision を保持しつつ、conflict flag は透明性のため残す。 |

## 対象行

| slug | row | move | conflict | 公式値 | SuperCombo 値 | prereview |
|---|---:|---|---|---|---|---|
| `guile` | 22 | ニーバズーカ | active_duration | `8-11` = 4 | `5` | SuperCombo notes は最終 active frame や practical advantage に触れるが、公式 active と一致しない。人間レビュー待ち。 |
| `guile` | 28 | ダブルバレット | damage | `400` | `360` | startup / active / recovery は一致。damage だけ conflict。人間レビュー待ち。 |
| `jamie` | 32 | 酩酊襲（2段目） | damage | `600` | `630` | SuperCombo notes に `Damage DL3-DL4: 630/660`。酔いLv scaling の条件値として分離候補。 |
| `jamie` | 85 | OD 点辰 | damage | `650` | `682` | SuperCombo notes に `Damage DL3-DL4: 682/715`。酔いLv scaling の条件値として分離候補。 |
| `jamie` | 86 | 疾歩仙掌 | damage | `900` | `990` | 公式 notes は酔いLv4条件。SuperCombo は DL4 値を raw damage に持つ可能性。分離候補。 |
| `jamie` | 87 | OD 疾歩仙掌 | damage | `1000` | `880` | 公式 notes は酔いLv4条件。SuperCombo は OD follow-up 側の条件値または source conflict の可能性。人間レビュー待ち。 |
| `juri` | 47 | 死紋蹴（2段目） | recovery | `19` | `20` | 他 field は一致。1F 差なので source/version 確認が必要。 |
| `ken` | 51 | OD 迅雷脚 | active_duration | `13-15` = 3 | `2` | 他 field は一致。派生可能 frame notes はあるが active 差の説明にはならない。人間レビュー待ち。 |
| `terry` | 15 | ジャンプ中P（ジャンプバックナックル） | active_duration, damage | `7-12` = 6 / `500` | `4` / `700` | Terry jMP / jMK の active と damage が相互に入れ替わっている疑い。source 確認が必要。 |
| `terry` | 16 | ジャンプ中K（ナイト・ブレイカー） | active_duration, damage | `7-10` = 4 / `700` | `6` / `500` | Terry jMP / jMK の active と damage が相互に入れ替わっている疑い。source 確認が必要。 |
| `zangief` | 50 | ツンドラストーム | startup, active_duration | `5` / `5-55` = 51 | `6` / `50` | 既存レビュー済み。SuperCombo notes は counter active `6-55f` と明記。公式表記との差として flag を残す。 |

## 判断

- `field_conflict` 単独 11 行から、追加で `enriched` に戻してよい行は見つからない。
- Jamie の酔いLv damage は、今後 `condition_dependent_field` へ分類し直す候補。ただし raw value を公式値の代替として accept しない。
- Terry jMP / jMK は高優先で source 確認する価値がある。片方だけではなく2行セットで確認する。
- Zangief Tundra Storm は既存の人間レビュー済み行なので、今回の未レビュー削減対象からは外す。

## 未解決の質問

- Jamie の酔いLv damage scaling を、field conflict ではなく条件付き値として標準分類するか。
- Terry jMP / jMK の値入れ替わり疑いを、SuperCombo source の誤り、公式 source の patch 差、または抽出対応ミスのどれとして扱うか。
- Guile / Juri / Ken の 1F-単位差分を、version 差として外部確認するか、公式優先の pending conflict として残すか。
