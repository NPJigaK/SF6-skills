---
type: concept
title: "SF6 System Data"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-game-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[concepts/range-comparisons]]"
  - "[[concepts/terms/throw]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "System Data"
  - "General Data"
  - "Movement Data"
  - "Jump Data"
  - "システムデータ"
tags:
  - sf6
  - game-data
  - frame-data
  - numeric-source
---

# SF6 System Data

## 要約

SF6 System Data は、SuperCombo Game Data page の General Data、Movement Data、Jump Data tables を計算・比較用に昇格した概念ページ。HP、throw range、walk speed、dash speed / distance、jump speed / distance / apex を character row で保持する。

この page の数値は community numeric source。Raw integrity と tabber completeness は [[reviews/2026-06-11-supercombo-game-data-web-page-capture-review]] で確認済みだが、各 gameplay value の公式照合または実機検証は未完了。機械参照用の source-preserving JSON は `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`。

## General Data

| name | hp | throwRange |
| --- | --- | --- |
| Blanka | 10000 | 0.9 |
| Dee Jay | 10000 | 0.8 |
| Dhalsim | 10000 | 0.8 |
| Sagat | 10000 | 0.85 |
| Jamie | 10000 | 0.8 |
| Rashid | 10000 | 0.8 |
| Chun-Li | 10000 | 0.8 |
| E. Honda | 10500 | 0.9 |
| A.K.I. | 10000 | 0.8 |
| C. Viper | 10000 | 0.8 |
| Terry | 10000 | 0.8 |
| Lily | 10000 | 0.8 |
| Akuma | 9000 | 0.8 |
| JP | 10000 | 0.8 |
| Elena | 10000 | 0.8 |
| Juri | 10000 | 0.8 |
| Ken | 10000 | 0.8 |
| Kimberly | 10000 | 0.8 |
| Mai | 10000 | 0.8 |
| Cammy | 10000 | 0.8 |
| Luke | 10000 | 0.8 |
| Manon | 10000 | 0.8 |
| Alex | 10500 | 0.85 |
| Ed | 10000 | 0.8 |
| Marisa | 10500 | 0.9 |
| Zangief | 11000 | 1.02 |
| M. Bison | 10000 | 0.8 |
| Ryu | 10000 | 0.8 |
| Guile | 10000 | 0.8 |
| Ingrid | 10000 | 0.80 |

## Movement Data

| name | fwdWalkSpd | bwdWalkSpd | fwdDashSpd | bwdDashSpd | fwdDashDist | bwdDashDist |
| --- | --- | --- | --- | --- | --- | --- |
| Blanka | 0.047 | 0.032 | 19 | 23 | 1.578 | 1.169 |
| Dee Jay | 0.043 | 0.032 | 19 | 23 | 1.50 | 0.90 |
| Dhalsim | 0.028 | 0.025 | 25 | 23 | 1.467 | 1.00 |
| Sagat | 0.039 | 0.027 | 23 | 23 | 1.40 | 0.90 |
| Jamie | 0.048 | 0.035 | 19 | 23 | 1.50 | 0.85 |
| Rashid | 0.045 | 0.032 | 18 | 25 | 1.20 (1.86) | 1.10 (1.91) |
| Chun-Li | 0.050 | 0.035 | 19 | 25 | 1.508 | 1.211 |
| E. Honda | 0.045 | 0.025 | 19 | 23 | 1.058 | 0.601 |
| A.K.I. | 0.0452 | 0.032 | 19 | 23 | 1.300 | 1.079 |
| C. Viper | 0.0452 | 0.031 | 21 | 23 | 1.50 | 0.80 |
| Terry | 0.048 | 0.032 | 19 | 23 | 1.50 | 0.985 |
| Lily | 0.042 | 0.027 | 21 | 24 | 1.261 | 0.940 |
| Akuma | 0.052 | 0.035 | 19 | 23 | 1.352 | 0.923 |
| JP | 0.037 | 0.025 | 22 | 23 | 1.454 | 1.003 |
| Elena | 0.048 | 0.033 | 20 | 23 | 1.43 | 1.139 |
| Juri | 0.047 | 0.032 | 22 | 23 | 1.903 | 1.114 |
| Ken | 0.047 | 0.032 | 19 | 23 | 1.322 | 0.923 |
| Kimberly | 0.0505 (0.0561) | 0.033 (0.0366) | 18 | 23 | 1.409 | 0.893 |
| Mai | 0.050 | 0.035 | 18 | 23 | 1.450 | 0.900 |
| Cammy | 0.0505 | 0.033 | 18 | 23 | 1.32 | 1.002 |
| Luke | 0.047 | 0.032 | 19 | 23 | 1.467 | 0.751 |
| Manon | 0.0452 | 0.031 | 21 | 25 | 1.499 | 1.254 |
| Alex | 0.042 | 0.027 | 22 | 25 | 1.00 | 0.75 |
| Ed | 0.0475 | 0.032 | 19 | 23 | 1.348 | 0.803 |
| Marisa | 0.039 | 0.027 | 22 | 25 | 1.40 | 0.90 |
| Zangief | 0.0364 | 0.025 | 22 | 25 | 1.007 | 0.712 |
| M. Bison | 0.048 | 0.0312 | 19 | 23 | 1.54 | 0.754 |
| Ryu | 0.047 | 0.032 | 19 | 23 | 1.252 | 0.923 |
| Guile | 0.043 | 0.032 | 21 | 23 | 1.567 | 0.74 |
| Ingrid | 0.047 | 0.032 | 20 | 23 | 1.30 | 0.90 |

## Jump Data

| name | jumpSpd | fwdJumpDist | bwdJumpDist | jumpApex |
| --- | --- | --- | --- | --- |
| Blanka | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Dee Jay | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Dhalsim | 4+68+3 | 2.04 | 1.768 | 2.178 |
| Sagat | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Jamie | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Rashid | 4+38+3 | 1.90 (5.07) | 1.52 (3.63) | 2.115 |
| Chun-Li | 4+42+3 | 2.10 | 1.68 | 2.247 |
| E. Honda | 4+38+3 | 1.90 | 1.52 | 2.115 |
| A.K.I. | 4+40+3 | 2.00 | 1.60 | 2.176 |
| C. Viper | 4+38+3 (6+40+3) | 1.90 (3.00) | 1.52 | 2.11 (2.195) |
| Terry | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Lily | 5+39+3 | 1.95 | 1.56 | 2.139 |
| Akuma | 4+38+3 | 1.90 | 1.52 | 2.115 |
| JP | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Elena | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Juri | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Ken | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Kimberly | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Mai | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Cammy | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Luke | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Manon | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Alex | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Ed | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Marisa | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Zangief | 5+38+3 | 1.725 | 1.406 | 2.115 |
| M. Bison | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Ryu | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Guile | 4+38+3 | 1.90 | 1.52 | 2.115 |
| Ingrid | 4+38+3 | 1.90 | 1.52 | 2.11 |

## 意味差分

- `hp`、`throwRange`、walk / dash / jump values は SuperCombo Game Data の rendered table text を保持する。
- Dash values と jump values の単位・測定条件は source page 以上には正規化していない。
- 公式 source または実機検証と矛盾する場合は、この page の community values を上書き根拠にしない。

## 関連

- [[concepts/frame-data]]
- [[concepts/range-comparisons]]
- [[concepts/terms/throw]]
- [[entities/street-fighter-6]]
