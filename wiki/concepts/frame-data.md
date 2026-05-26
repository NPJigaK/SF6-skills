---
type: concept
title: "Frame Data"
created: 2026-05-26
updated: 2026-05-27
status: active
confidence: medium
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/capcom-official-chun-li-frame-data]]"
  - "[[sources/capcom-official-zangief-frame-data]]"
  - "[[reviews/2026-05-27-health-check]]"
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[entities/jp]]"
  - "[[entities/ryu]]"
  - "[[entities/chun-li]]"
  - "[[entities/zangief]]"
tags:
  - mechanics
  - glossary
---

# Frame Data

## Summary

Frame data is the vocabulary and structured move data used to describe timing,
recovery, advantage, damage, scaling, cancel options, and related move
properties.

## Definition

The SuperCombo glossary source defines frame-data vocabulary such as active
frames, startup, recovery, cancel options, hit/block advantage, guard direction,
damage, damage scaling, hitconfirm windows, Drive Rush Cancel advantage, and
actionable recovery.

The official Capcom frame-data captures provide reviewed structured per-move
data for JP, Ryu, Chun-Li, and Zangief in Classic and Modern controls.

## Why it matters

Frame data terms, structured captures, and comparison conventions are needed
before later wiki pages can interpret move data, comparisons, or
timing-sensitive claims.

## Key claims

| Claim | Sources | Confidence |
|---|---|---|
| Active describes how many frames a move remains able to hurt opponents. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Recovery describes how many frames a move takes to finish after active frames end. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Startup values are written with the last startup frame and first active frame as the same frame. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Hit/block values describe frame advantage when an attack hits or is blocked. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| The accepted official JP capture contains 69 Classic data rows and 65 Modern data rows. | [[sources/capcom-official-jp-frame-data]] | high |
| The official Ryu capture contains 75 Classic data rows and 69 Modern data rows. | [[sources/capcom-official-ryu-frame-data]] | high |
| The official Chun-Li capture contains 78 Classic data rows and 72 Modern data rows. | [[sources/capcom-official-chun-li-frame-data]] | high |
| The official Zangief capture contains 72 Classic data rows and 66 Modern data rows. | [[sources/capcom-official-zangief-frame-data]] | high |
| The official captures store field explanations separately from per-move CSV rows. | [[sources/capcom-official-jp-frame-data]], [[sources/capcom-official-ryu-frame-data]], [[sources/capcom-official-chun-li-frame-data]], [[sources/capcom-official-zangief-frame-data]] | high |
| Classic/Modern comparisons should default to exact official move-name matching. | [[reviews/2026-05-27-health-check]] | high |
| Reader-facing command notation is currently a display-only transform; raw input tokens remain the source-preserving data. | [[reviews/2026-05-27-health-check]] | high |

## Comparison policy

For Classic/Modern frame-data comparisons, use exact official move-name
matching as the default. If two official names look like likely variants of the
same practical move, such as `しゃがみ強K（ビッグスタンプ）` and `ビッグスタンプ`,
annotate that relationship instead of silently merging the rows.

Reader-facing answers may render raw input tokens as readable command notation
such as `↓↘→ + 強P`. This is a display-only transform for explanations. The
source-preserving data remains the raw token data stored in the official capture
outputs.

## Connections

- [[concepts/drive-system]]
- [[concepts/juggle-system]]
- [[concepts/fighting-game-notation]]
- [[entities/jp]]
- [[entities/ryu]]
- [[entities/chun-li]]
- [[entities/zangief]]

## Contradictions / caveats

- This page does not yet summarize individual JP move values; those values
  remain in the raw DOM and derived CSV outputs.
- This page does not yet summarize individual Ryu move values; those values
  remain in the raw DOM and derived CSV outputs.
- This page does not yet summarize individual Chun-Li move values; those values
  remain in the raw DOM and derived CSV outputs.
- This page does not yet summarize individual Zangief move values; those values
  remain in the raw DOM and derived CSV outputs.
- `input_raw_display` in the derived CSV is a raw DOM-token display, not a
  normalized command notation.
- Display-only command notation is not yet a formal canonical notation schema
  for the wiki.

## Open questions

- When, if ever, should display-only command notation become a formal wiki
  notation schema?
- Which official source should be ingested to explain frame-data update history?
