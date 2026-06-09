---
type: concept
title: "Fighting Game Notation"
created: 2026-05-26
updated: 2026-06-10
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[reviews/2026-05-27-health-check]]"
  - "[[reviews/2026-06-09-supercombo-glossary-web-page-capture-review]]"
related:
  - "[[concepts/frame-data]]"
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

Fighting-game notation は、link、cancel、hold/release、chain、hit state、air action、delay、tiger-knee input、whiff、directional input などを短く表すための表記体系。

## 定義

SuperCombo glossary の page wikitext は Notation Glossary を `{{ComboLegend-SF6}}` テンプレートとして呼び出している。展開後の `rendered/tables.dom.json` は次のような例を保持している。template 本文は `raw/web-pages/wiki.supercombo.gg/glossary/templates/combo-legend-sf6.raw.wikitext` に保存され、manifest では revid `283225` / timestamp `2023-12-11T18:45:25Z` の依存として記録されている。

- `A,B`: A の recovery 後に B を link する。
- `A > B`: A の animation 中に B へ cancel する。
- `(N)`: multi-hit move の一部 hit だけを使う。
- `xN`: chained normal を繰り返す。
- `[X]`: input を hold する。
- `]X[`: input を release する。
- `X~Y`: 入力を素早く連続して行う。
- `CH`, `j.`, `jc`, `dl`, `TK`, whiff notation など。

## なぜ重要か

notation は、source wording を保ちながら combo や input を簡潔に説明するために必要。公式 frame-data answers では、読者向けに `↓↘→ + 強P` のような display-only 表記を使う場合があるが、source-preserving data は raw input tokens である。

## 主要な主張

| 主張 | ソース | 信頼度 |
|---|---|---|
| `A,B` は A の recovery 後に B を link する意味。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `A > B` は A の animation 中に B へ cancel する意味。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `[X]` と `]X[` は hold / release notation。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| `TK` は air move を地上近くで出す tiger knee input timing を表す。 | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| 公式 frame-data answers の読者向け command notation は、現時点では canonical normalized input schema ではなく display-only transform。 | [[reviews/2026-05-27-health-check]] | high |

## 関連

- [[concepts/frame-data]]

## 矛盾 / 注意点

- 2026-06-09 の web-page capture では、Notation Glossary の直接 wikitext は `{{ComboLegend-SF6}}` であり、展開後の表は `rendered/tables.dom.json` に保存されている。directional notation に依存する場合は、表示 DOM 取得物と `Template:ComboLegend-SF6` の raw wikitext / revision の両方を参照する。
- raw input tokens は引き続き source-preserving data として扱う。

## 未解決の質問

- 追加 notation source を ingest した後、独立した durable notation reference を作るべきか。
- display-only command notation を formal normalized input notation schema に昇格する条件は何か。
