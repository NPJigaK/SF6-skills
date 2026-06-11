---
type: concept
title: "Fighting Game Notation"
created: 2026-05-26
updated: 2026-06-11
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/supercombo-street-fighter-6-controls]]"
  - "[[reviews/2026-05-27-health-check]]"
  - "[[reviews/2026-06-09-supercombo-glossary-web-page-capture-review]]"
  - "[[reviews/2026-06-11-supercombo-controls-web-page-capture-review]]"
related:
  - "[[concepts/frame-data]]"
  - "[[concepts/terms/cancel]]"
  - "[[concepts/terms/chain]]"
aliases:
  - "格闘ゲーム表記"
  - "コマンド表記"
  - "Fighting Game Notation"
tags:
  - notation
  - glossary
---

# Fighting Game Notation（格闘ゲーム表記）

## 要約

Fighting-game notation は、link、[[concepts/terms/cancel|cancel]]、hold/release、[[concepts/terms/chain|chain]]、hit state、air action、delay、tiger-knee input、whiff、directional input、button notation などを短く表すための表記体系。SuperCombo controls source は、この wiki の standard として numpad notation と LP / MP / HP / LK / MK / HK の button notation を説明している。

## 定義

[[sources/supercombo-street-fighter-6-glossary]] は Notation Glossary を `ComboLegend-SF6` 由来の表として保持している。この source は次のような例を説明する。

- `A,B`: A の recovery 後に B を link する。
- `A > B`: A の animation 中に B へ [[concepts/terms/cancel|cancel]] する。
- `(N)`: multi-hit move の一部 hit だけを使う。
- `xN`: [[concepts/terms/chain|chained]] normal を繰り返す。
- `[X]`: input を hold する。
- `]X[`: input を release する。
- `X~Y`: 入力を素早く連続して行う。
- `CH`, `j.`, `jc`, `dl`, `TK`, whiff notation など。

[[sources/supercombo-street-fighter-6-controls]] は、directional input の表記として numpad notation を説明する。5 を lever neutral、6 をキャラクターが向いている方向として扱い、例として `2LK` と `236HP` を示している。旧 Street Fighter notation との対応として、QCF = 236、QCB = 214、DP / SRK = 623、RDP = 421、HCF = 41236、HCB = 63214、SPD / 360、720 も説明している。

## なぜ重要か

notation は、source wording を保ちながら combo や input を簡潔に説明するために必要。公式 frame-data answers では、読者向けに `↓↘→ + 強P` のような display-only 表記を使う場合があるが、source-preserving data は raw input tokens である。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| `A,B` は A の recovery 後に B を link する意味。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `A > B` は A の animation 中に B へ cancel する意味。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `[X]` と `]X[` は hold / release notation。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `TK` は air move を地上近くで出す tiger knee input timing を表す。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| SuperCombo controls page は numpad notation をこの wiki の notation standard として説明し、5 neutral / 6 forward-facing direction の対応を示している。 | [[sources/supercombo-street-fighter-6-controls]] | medium |
| LP / MP / HP / LK / MK / HK は Light / Medium / Heavy Punch と Light / Medium / Heavy Kick の button notation。 | [[sources/supercombo-street-fighter-6-controls]] | medium |
| QCF / QCB / DP / RDP / HCF / HCB は、それぞれ 236 / 214 / 623 / 421 / 41236 / 63214 に対応する旧来表記として説明されている。 | [[sources/supercombo-street-fighter-6-controls]] | medium |
| 公式 frame-data answers の読者向け command notation は、現時点では canonical normalized input schema ではなく display-only transform。 | [[reviews/2026-05-27-health-check]] | high |

## 関連

- [[concepts/frame-data]]
- [[concepts/terms/cancel]]
- [[concepts/terms/chain]]

## 矛盾 / 注意点

- [[sources/supercombo-street-fighter-6-glossary]] の Notation Glossary は `ComboLegend-SF6` template 依存を持つ。template provenance が必要な場合は source page と [[reviews/2026-06-09-supercombo-glossary-web-page-capture-review]] を確認する。
- [[sources/supercombo-street-fighter-6-controls]] の numpad / classic notation / button nickname は page 本文由来。capture provenance が必要な場合は source page と [[reviews/2026-06-11-supercombo-controls-web-page-capture-review]] を確認する。
- raw input tokens は引き続き source-preserving data として扱う。

## 未解決の質問

- 追加 notation source を ingest した後、独立した durable notation reference を作るべきか。
- display-only command notation を formal normalized input notation schema に昇格する条件は何か。
- Capcom 公式 controls / control type source を ingest して、community source の button mapping と Modern Controls claim を照合するべきか。
