---
type: review
review_type: calculation_model_gap
title: "Mai combo damage ledger regression"
created: 2026-06-15
updated: 2026-06-15
status: active
confidence: medium
sources:
  - "[[sources/capcom-official-mai-frame-data]]"
  - "[[sources/supercombo-street-fighter-6-game-data]]"
related:
  - "[[entities/mai]]"
  - "[[concepts/terms/damage-scaling]]"
  - "[[concepts/terms/counter-hit]]"
  - "[[concepts/terms/punish-counter]]"
external_sources:
  - title: "【スト６】舞　最強コンボ集【解説付き】"
    url: "https://www.youtube.com/watch?v=f78kDhtzHlY"
    published_at: 2026-04-21
tags:
  - sf6
  - review
  - combo-damage
  - mai
---

# Mai combo damage ledger regression

## Finding

Mai Classic の `214HP (No Flame)` を含む combo damage ledger で、`214HP` が comboed into された時の character-specific scaling を見落とすと、後続の `236LK` が 1 step 高い scaling で計算される。

SuperCombo Game Data 由来の [[concepts/terms/damage-scaling#Mai]] は `214HP (No Flame)` について、comboed into された場合に `2 hits of scaling when comboed into (applies to next attack)` とする。この repo の計算器は route text からこの状態を推測しないため、ledger 側で `effective_scaling`、`attack_step`、`scaling_note` に明示する必要がある。

## Regression cases

ユーザー提示の training-mode 検証値は [YouTube video](https://www.youtube.com/watch?v=f78kDhtzHlY) とスクリーンショット由来。`yt-dlp` metadata で title `【スト６】舞　最強コンボ集【解説付き】`、`upload_date: 20260421` を確認した。動画・画像はこの review では raw capture として ingest していないため、damage 表示の authority は `human-provided validation` に留めるが、source date は `2026-04-21` として扱う。

| Route | Correct total | Ledger fixture |
|---|---:|---|
| `5MP > DRC 4HK > 2MP > 214HP > 236LK` | `2496` | `tests/calculations/combo_damage/fixtures/mai/classic/2026-04-21-5mp-2496.ledger.json` |
| `5LP CH > 2MK > 236HK` | `1460` | `tests/calculations/combo_damage/fixtures/mai/classic/2026-04-21-5lp-ch-1460.ledger.json` |
| `5LP PC > 5HP > 214HP > 236LK` | `1960` | `tests/calculations/combo_damage/fixtures/mai/classic/2026-04-21-5lp-pc-1960.ledger.json` |
| `Raw DR 6MP > 2MP > DRC 5HK > 2MP > DRC 5HK > 2MP > 214HP > 236LK > SA3` | `5285` | `tests/calculations/combo_damage/fixtures/mai/classic/2026-04-21-raw-dr-6mp-5285.ledger.json` |

## Corrected scaling interpretation

- `5MP > DRC 4HK > 2MP > 214HP > 236LK`: `214HP` は `4th attack` の scaling を使うが、2 hits of scaling を消費するため、次の `236LK` は DRC 付き `6th attack` の `42%` を使う。
- `5LP PC > 5HP > 214HP > 236LK`: Light starter progression で `214HP` は `3rd attack` の `70%` を使うが、次の `236LK` は `5th attack` の `50%` を使う。
- `Raw DR 6MP > 2MP > DRC 5HK > 2MP > DRC 5HK > 2MP > 214HP > 236LK > SA3`: raw Drive Rush starter は追加 damage penalty なし、mid-combo Drive Rush の `15%` penalty は重複なしで後続に適用する。`214HP` により `236LK` は DRC 付き `9th attack` の `17%` を使い、SA3 は `50%` minimum で `2000` damage になる。
- `5LP CH > 2MK > 236HK`: `214HP` を含まないため、既存の Light starter progression と Counter Hit 初段 `1.2x` で `1460` に一致する。

## Guardrail

`tools.calculations.combo_damage` は `attack_step` と `scaling_note` を output row に伝播する。これらは計算値を変える field ではなく、character-specific scaling を ledger 化した根拠を review しやすくする trace field。

## Evidence gaps

- YouTube / スクリーンショットは今回 raw package として保存していない。将来、外部動画を durable validation source にする場合は、別途 raw capture policy と manifest を整備する。
- `combo_damage` は今後も route parser ではない。source-backed ledger が不足している route は fail closed し、LLM が move-specific scaling を補完しない。
