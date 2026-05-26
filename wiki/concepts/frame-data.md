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
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[entities/ryu]]"
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
data for JP and Ryu in Classic and Modern controls.

## Why it matters

Frame data terms and structured captures are needed before later wiki pages can
interpret move data, comparisons, or timing-sensitive claims.

## Key claims

| Claim | Sources | Confidence |
|---|---|---|
| Active describes how many frames a move remains able to hurt opponents. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Recovery describes how many frames a move takes to finish after active frames end. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Startup values are written with the last startup frame and first active frame as the same frame. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| Hit/block values describe frame advantage when an attack hits or is blocked. | [[sources/supercombo-street-fighter-6-glossary]] | medium |
| The accepted official JP capture contains 69 Classic data rows and 65 Modern data rows. | [[sources/capcom-official-jp-frame-data]] | high |
| The official Ryu capture contains 75 Classic data rows and 69 Modern data rows. | [[sources/capcom-official-ryu-frame-data]] | high |
| The official captures store field explanations separately from per-move CSV rows. | [[sources/capcom-official-jp-frame-data]], [[sources/capcom-official-ryu-frame-data]] | high |

## Connections

- [[concepts/drive-system]]
- [[concepts/juggle-system]]
- [[concepts/fighting-game-notation]]
- [[entities/jp]]
- [[entities/ryu]]

## Contradictions / caveats

- This page does not yet summarize individual JP move values; those values
  remain in the raw DOM and derived CSV outputs.
- This page does not yet summarize individual Ryu move values; those values
  remain in the raw DOM and derived CSV outputs.
- `input_raw_display` in the derived CSV is a raw DOM-token display, not a
  normalized command notation.

## Open questions

- Should the wiki define a normalized command-input notation after more official
  frame-data captures exist?
- Which official source should be ingested to explain frame-data update history?
