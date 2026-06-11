---
type: concept
title: "SF6 Range Comparisons"
created: 2026-06-11
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-game-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[concepts/system-data]]"
  - "[[concepts/terms/guaranteed-punish]]"
  - "[[concepts/terms/whiff-punish]]"
  - "[[entities/street-fighter-6]]"
aliases:
  - "Range Comparisons"
  - "Cancelable 2MK Range"
  - "4f Normal Range/Hitstun/Pushback"
  - "5f Punish Options"
  - "Sweep Ranges"
  - "リーチ比較"
tags:
  - sf6
  - range
  - frame-data
  - numeric-source
---

# SF6 Range Comparisons

## 要約

SF6 Range Comparisons は、SuperCombo Game Data page の range comparison tabs を計算・比較用に昇格した概念ページ。Cancelable 2MK、4f normal、5f punish option、sweep range の character / input / startup / range / notes を source-preserving table として保持する。

この page の数値は community numeric source。Raw integrity と tabber completeness は [[reviews/2026-06-11-supercombo-game-data-web-page-capture-review]] で確認済みだが、各 gameplay value の公式照合または実機検証は未完了。機械参照用の source-preserving JSON は `raw/web-pages/wiki.supercombo.gg/game-data/derived/tabber-tables.json`。

## Cancelable 2MK Range

| chara | input | startup | atkRange | Notes |
| --- | --- | --- | --- | --- |
| Elena | 2MK | 9 | 1.726 (1.669) | TC cancel only; 1st active frame: 1.669 |
| C.Viper | 2MK | 8 | 1.60 | High Jump cancel only (requires 1 bar) |
| Juri | 2MK | 8 | 1.517 (1.446) | 1st active frame: 1.446 |
| Terry | 2MK | 8 | 1.501 |  |
| Cammy | 2MK | 8 | 1.49 |  |
| Luke | 2MK | 8 | 1.482 (1.44) | 1st active frame: 1.44 |
| Ryu | 2MK | 8 | 1.482 |  |
| M.Bison | 2MK | 8 | 1.482 |  |
| Blanka | 2MK | 8 | 1.48 | Wide hurtbox (outpoked by shorter 2MKs) |
| Chun-Li | 2MK | 7 | 1.477 |  |
| Akuma | 2MK | 8 | 1.473 |  |
| Ken | 2MK | 7 | 1.46 |  |
| Jamie | 2MK | 7 | 1.46 |  |
| Ingrid | 2MK | 8 | 1.448 |  |
| Mai | 2MK | 7 | 1.438 |  |
| Ed | 2MP | 8 | 1.411 | 2MP (low poke, functions like 2MK for most characters) |
| Rashid | 2MK | 7 | 1.405 |  |
| Lily | 2MK | 9 | 1.364 |  |
| A.K.I. | 2MK | 7 | 1.34 | Super Cancel only |
| Dhalsim | 1MK | 8 | 1.19 |  |

## 4f Normal Range / Hitstun / Pushback

| chara | input | hitstun | atkRange | Pushback (Hit) | Pushback (Block) |
| --- | --- | --- | --- | --- | --- |
| Dhalsim | 2LK | 18 | 1.44 (0.814) | 0.422 | 0.431 |
| Zangief | 2LK | 15 | 1.39 | 0.373 | 0.433 |
| E.Honda | 2LP | 17 | 1.23 | 0.402 | 0.412 |
| Sagat | 2LP | 17 | 1.20 | 0.487 | 0.415 |
| Marisa | 2LP | 16 | 1.17 | 0.363 | 0.389 |
| E.Honda | 5LK | 16 | 1.12 | 0.531 | 0.550 |
| Rashid | 5LP | 15 | 1.11 | 0.405 | 0.418 |
| Blanka | 5LK | 16 | 1.11 | 0.499 | 0.522 |
| Luke | 2LP | 16 | 1.11 | 0.351 | 0.330 |
| M.Bison | 5LK | 15 | 1.097 | 0.213 | 0.218 |
| Manon | 2LP | 16 | 1.09 | 0.427 | 0.436 |
| Alex | 5LP | 16 | 1.08 | 0.319 | 0.330 |
| JP | 2LP | 17 | 1.07 | 0.371 | 0.325 |
| Elena | 2LP | 16 | 1.07 | 0.361 | 0.338 |
| M.Bison | 2LP | 16 | 1.06 | 0.404 | 0.385 |
| Cammy | 5LP | 15 | 1.05 | 0.352 | 0.304 |
| Cammy | 2LP | 15 | 1.05 | 0.352 | 0.304 |
| Chun-Li | 5LP | 15 | 1.05 | 0.320 | 0.343 |
| A.K.I. | 5LK | 18 | 1.04 | 0.211 | 0.379 |
| Dee_Jay | 5LP | 13 | 1.04 | 0.409 | 0.428 |
| Guile | 2LP | 16 | 1.03 | 0.468 | 0.389 |
| Mai | 2LP | 14 | 1.03 | 0.321 | 0.311 |
| Ed | 2LP | 16 | 1.02 | 0.361 | 0.338 |
| Akuma | 5LP | 14 | 1.02 | 0.364 | 0.378 |
| Ken | 5LP | 14 | 1.01 | 0.375 | 0.333 |
| Terry | 5LP | 14 | 1.01 | 0.289 | 0.333 |
| Ryu | 5LP | 14 | 1.01 | 0.289 | 0.378 |
| Rashid | 5LK | 16 | 1.01 | 0.266 | 0.271 |
| Kimberly | 2LP | 14 | 1.01 | 0.289 | 0.259 |
| Manon | 5LP | 17 | 1.01 | 0.424 | 0.433 |
| C.Viper | 5LP | 15 | 1.01 | 0.288 | 0.333 |
| Ingrid | 2LP | 15 | 1.00 | 0.320 | 0.330 |
| Akuma | 2LP | 16 | 1.00 | 0.383 | 0.341 |
| Jamie | 2LP | 16 | 0.98 | 0.361 | 0.374 |
| Ingrid | 5LP | 15 | 0.97 | 0.363 | 0.378 |
| Mai | 5LP | 15 | 0.97 | 0.320 | 0.315 |
| A.K.I. | 2LP | 15 | 0.96 | 0.277 | 0.286 |
| C.Viper | 2LP | 16 | 0.95 | 0.276 | 0.330 |
| Ryu | 2LP | 15 | 0.94 | 0.277 | 0.330 |
| Ed | 5LP | 14 | 0.92 | 0.289 | 0.278 |
| Juri | 2LP | 15 | 0.92 | 0.320 | 0.330 |
| Terry | 2LP | 15 | 0.91 | 0.299 | 0.330 |
| Chun-Li | 2LP | 14 | 0.91 | 0.321 | 0.338 |
| Ken | 2LP | 16 | 0.89 | 0.351 | 0.330 |
| Dhalsim | 5LP | 15 | 0.88 | 0.373 | 0.385 |
| Chun-Li | 2LK | 12 | 0.85 | 0.325 | 0.330 |
| Juri | 5LP | 16 | 0.85 | 0.319 | 0.333 |
| Lily | 5LK | 16 | 0.82 | 0.425 | 0.436 |
| Mai | 5LK | 12 | 0.77 | 0.325 | 0.330 |

## 5f Punish Options

| chara | input | atkRange | Notes |
| --- | --- | --- | --- |
| Jamie | 5HP | 1.732 (0.924) | Short range on frame 5 (0.924) but very rewarding if it can reach |
| Zangief | 360+LP | 1.62 | Zangief's best 5F punish at max range (2LK conversions are weak especially if farther away) |
| Chun-Li | 236LK | 1.485 (1.315) | Special move, but included for being an important long-range 5f punish (1.315 Range on frame 5, comparable to Shoto 5LK) |
| Juri | 5MK | 1.427 (0.74) | Extremely short range as a 5-frame punish (0.74), but more rewarding when landed |
| Blanka | 5LP | 1.36 |  |
| Manon | 5LK | 1.35 |  |
| Marisa | 2LK | 1.34 | Terrible punish, but the only 5-frame option when outside of 2LP range |
| Ken | 5LK | 1.32 |  |
| Alex | 2LK | 1.31 | Punish allows the 2LK~2HK Target Combo to connect (longest range 5f punish and especially important for Modern controls) |
| Elena | 5LK | 1.31 |  |
| Akuma | 5LK | 1.303 |  |
| Ryu | 5LK | 1.30 |  |
| Ed | 2LK | 1.30 |  |
| E.Honda | 5LP | 1.28 |  |
| Cammy | 5LK | 1.27 |  |
| Guile | 5LK | 1.27 |  |
| Sagat | 5LP | 1.26 |  |
| M.Bison | 5LP | 1.26 |  |
| Luke | 5LK | 1.26 |  |
| Dee_Jay | 5LK | 1.239 |  |
| Lily | 5LP | 1.23 |  |
| Alex | 2LP | 1.23 |  |
| Jamie | 5LP | 1.213 | (DL1) Jamie's best 5-frame punish once he has taken at least 1 drink |
| Kimberly | 5LK | 1.20 |  |
| C.Viper | 5LK | 1.20 |  |
| Terry | 5LK | 1.19 |  |
| A.K.I. | 2LK | 1.19 | Only useful as max range Punish Counter linked into 2MK |
| Dee_Jay | 2LP | 1.18 | Slightly shorter than 5LK but better follow-ups |
| Elena | 5LP | 1.16 | Much stronger link options than 5LK |
| Juri | 5LK | 1.16 |  |
| Dhalsim | 2LP | 1.14 |  |
| Jamie | 5LK | 1.13 |  |
| Ingrid | 5LK | 1.13 |  |
| Chun-Li | 5LK | 1.13 | Chun's longest 5-frame normal, short compared to most 5f punishes (may need to use 236LK instead) |
| JP | 5LK | 1.12 | JP's longest range 5f punish (among the shortest in the game) |
| Guile | 5LP | 1.07 | Slightly more range than 2LP while still allowing link to 5HP |
| Rashid | 2LP | 1.02 | Less range than 5LP (4f startup), but links to 5HP on Punish Counter |
| Kimberly | 5LP | 0.97 | Kimberly's shortest light punish, but links into 5HP on Punish Counter for stronger conversions |
| Jamie | 5LP | 0.97 | (DL0) Listed for comparison only; use 2LP or 5LK at Drink Lv.0 |
| Ken | 5MP | 0.914 | Short range but strong 5f punish starter if it reaches |
| A.K.I. | 5LP | 0.90 | Short range punish into 5LP~LP Target Combo |
| Cammy | 4MP | 0.826 | Short range but strong 5f punish starter if it reaches |
| Chun-Li | 5MP | 0.803 | Short range, but strong 5f punish starter if it reaches |

## Sweep Ranges

| chara | input | startup | atkRange | Notes |
| --- | --- | --- | --- | --- |
| M.Bison | 3HK | 15 | 3.47 (1.753) | Slides forward; Range 1.75 on 1st active frame |
| Blanka | 3HP | 14 | 3.10 (2.413) | Slides forward; Range 2.41 on 1st active frame |
| Dhalsim | 2HK | 12 | 3.057 (1.50) | Slides forward; Range 1.50 on 1st active frame |
| Elena | 3HK | 14 | 2.88 (1.69) | Slides forward; Range 1.69 on 1st active frame |
| JP | 3HP | 16 | 2.414 |  |
| Chun-Li | 214P~MP | 6 | 2.30 (1.753) | Slides forward; Range 1.75 on 1st active frame |
| Dee_Jay | 2HK | 14 | 2.186 (1.622) | Slides forward; Range 1.62 on 1st active frame |
| E.Honda | 6HK | 14 | 2.114 | Only knocks down on Punish Counter |
| Guile | 2HK | 9 | 2.037 (1.739) | 2 hits; Range: 2nd / 1st; Range 1.76 on final active frame of 1st hit |
| Jamie | 2HK | 9 | 2.02 (1.662) | 2 hits; Range: 2nd / 1st; Range 1.67 on final active frame of 1st hit |
| Manon | 2HK | 11 | 2.01 |  |
| M.Bison | 2HK | 11 | 1.991 |  |
| Elena | 2HK | 11 | 1.967 (1.962) |  |
| Marisa | 2[HK] | 20(4) | 1.956 |  |
| Zangief | 2HK | 12 | 1.955 |  |
| Lily | 2HK | 11 | 1.938 (1.666) | 2 hits; Range 1.67 on 1st active frame of 1st hit |
| A.K.I. | 2HP | 10 | 1.923 | Does not actually slide forward during active frames like the animation suggests |
| Sagat | 2HK | 11 | 1.91 |  |
| C.Viper | 2HK | 10 | 1.89 |  |
| Alex | 2HK | 10 | 1.88 |  |
| Blanka | 2HK | 11 | 1.865 |  |
| Marisa | 2HK | 11 | 1.856 |  |
| Juri | 2HK | 10 | 1.798 (1.787) |  |
| Ryu | 2HK | 9 | 1.793 |  |
| Akuma | 2HK | 9 | 1.783 | Moves forward during animation |
| Ed | 2HP | 10 | 1.782 |  |
| Cammy | 2HK | 9 | 1.73 |  |
| Chun-Li | 2HK | 9 | 1.715 |  |
| Rashid | 2HK | 9 | 1.711 |  |
| Ingrid | 2HK | 10 | 1.71 |  |
| Mai | 2HK | 9 | 1.703 |  |
| Luke | 2HK | 10 | 1.661 |  |
| Ken | 2HK | 8 | 1.645 |  |
| Terry | 2HK | 10 | 1.629 |  |
| E.Honda | 2HK | 11 | 1.605 |  |
| Kimberly | 2HK | 8 | 1.52 | Less range on active frames 2-3 |
| Dee_Jay | 2MK | 8 | 1.52 | Faster/safer than traditional sweep |
| JP | 2HK | 10 | 1.38 | Short range but very safe when spaced |
| Dhalsim | 1HK | 9 | 1.29 |  |

## 意味差分

- `atkRange`、Pushback、Notes は SuperCombo rendered table text を保持し、単位や条件を追加正規化していない。
- Parentheses 付き range は source text のまま保持する。多くは first active frame などの条件付き値として Notes に説明がある。
- Range は確定反撃、差し返し、先端キャンセル、sweep punish の候補検索に使えるが、hurtbox extension、pushback、stance、timing、character-specific state に依存する。

## 関連

- [[concepts/frame-data]]
- [[concepts/system-data]]
- [[concepts/terms/guaranteed-punish]]
- [[concepts/terms/whiff-punish]]
- [[entities/street-fighter-6]]
