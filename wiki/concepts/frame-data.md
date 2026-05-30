---
type: concept
title: "Frame Data"
created: 2026-05-26
updated: 2026-05-30
status: active
confidence: high
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/capcom-official-luke-frame-data]]"
  - "[[sources/capcom-official-jamie-frame-data]]"
  - "[[sources/capcom-official-chun-li-frame-data]]"
  - "[[sources/capcom-official-guile-frame-data]]"
  - "[[sources/capcom-official-kimberly-frame-data]]"
  - "[[sources/capcom-official-juri-frame-data]]"
  - "[[sources/capcom-official-ken-frame-data]]"
  - "[[sources/capcom-official-blanka-frame-data]]"
  - "[[sources/capcom-official-dhalsim-frame-data]]"
  - "[[sources/capcom-official-e-honda-frame-data]]"
  - "[[sources/capcom-official-dee-jay-frame-data]]"
  - "[[sources/capcom-official-manon-frame-data]]"
  - "[[sources/capcom-official-marisa-frame-data]]"
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/capcom-official-zangief-frame-data]]"
  - "[[sources/capcom-official-lily-frame-data]]"
  - "[[sources/capcom-official-cammy-frame-data]]"
  - "[[sources/capcom-official-rashid-frame-data]]"
  - "[[sources/capcom-official-aki-frame-data]]"
  - "[[sources/capcom-official-ed-frame-data]]"
  - "[[sources/capcom-official-gouki-akuma-frame-data]]"
  - "[[sources/capcom-official-vega-m-bison-frame-data]]"
  - "[[sources/capcom-official-terry-frame-data]]"
  - "[[sources/capcom-official-mai-frame-data]]"
  - "[[sources/capcom-official-elena-frame-data]]"
  - "[[sources/capcom-official-sagat-frame-data]]"
  - "[[sources/capcom-official-c-viper-frame-data]]"
  - "[[sources/capcom-official-alex-frame-data]]"
  - "[[sources/capcom-official-ingrid-frame-data]]"
  - "[[reviews/2026-05-27-health-check]]"
  - "[[reviews/2026-05-30-official-frame-data-roster-capture-review]]"
  - "[[outputs/reports/2026-05-30-official-frame-data-coverage]]"
related:
  - "[[concepts/drive-system]]"
  - "[[concepts/juggle-system]]"
  - "[[concepts/fighting-game-notation]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/ryu]]"
  - "[[entities/luke]]"
  - "[[entities/jamie]]"
  - "[[entities/chun-li]]"
  - "[[entities/guile]]"
  - "[[entities/kimberly]]"
  - "[[entities/juri]]"
  - "[[entities/ken]]"
  - "[[entities/blanka]]"
  - "[[entities/dhalsim]]"
  - "[[entities/e-honda]]"
  - "[[entities/dee-jay]]"
  - "[[entities/manon]]"
  - "[[entities/marisa]]"
  - "[[entities/jp]]"
  - "[[entities/zangief]]"
  - "[[entities/lily]]"
  - "[[entities/cammy]]"
  - "[[entities/rashid]]"
  - "[[entities/aki]]"
  - "[[entities/ed]]"
  - "[[entities/gouki-akuma]]"
  - "[[entities/vega-m-bison]]"
  - "[[entities/terry]]"
  - "[[entities/mai]]"
  - "[[entities/elena]]"
  - "[[entities/sagat]]"
  - "[[entities/c-viper]]"
  - "[[entities/alex]]"
  - "[[entities/ingrid]]"
tags:
  - mechanics
  - glossary
---

# Frame Data

## Summary

Frame data is the vocabulary and structured move data used to describe timing,
recovery, advantage, damage, scaling, cancel options, and related move
properties. The wiki now has official Capcom Classic and Modern frame-data
outputs for 30 Street Fighter 6 character data slugs.

## Definition

The SuperCombo glossary source defines frame-data vocabulary such as active
frames, startup, recovery, cancel options, hit/block advantage, guard direction,
damage, damage scaling, hitconfirm windows, Drive Rush Cancel advantage, and
actionable recovery.

The official Capcom frame-data captures provide structured per-move data in
Classic and Modern controls. JP, Ryu, Chun-Li, and Zangief were previously
human-accepted. The 26 new 2026-05-30 captures passed automated validation and
are pending human review.

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
| The wiki has derived Classic and Modern official frame-data outputs for 30 character data slugs. | [[outputs/reports/2026-05-30-official-frame-data-coverage]] | high |
| JP, Ryu, Chun-Li, and Zangief captures were previously accepted by human review. | [[reviews/2026-05-26-official-jp-frame-data-capture-review]], [[reviews/2026-05-27-official-ryu-frame-data-capture-review]], [[reviews/2026-05-27-official-chun-li-frame-data-capture-review]], [[reviews/2026-05-27-official-zangief-frame-data-capture-review]] | high |
| The 26 new 2026-05-30 official captures passed automated validation and are pending human review. | [[reviews/2026-05-30-official-frame-data-roster-capture-review]] | high |
| Official captures store field explanations separately from per-move CSV rows. | [[outputs/reports/2026-05-30-official-frame-data-coverage]] | high |
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
- [[entities/street-fighter-6]]

## Contradictions / caveats

- This page does not summarize individual move values; those values remain in
  the raw DOM and derived CSV outputs until a specific reusable question or
  synthesis needs them.
- `input_raw_display` in the derived CSV is a raw DOM-token display, not a
  normalized command notation.
- Display-only command notation is not yet a formal canonical notation schema
  for the wiki.
- The 30-character coverage is not a single-date roster snapshot: JP is from
  2026-05-26; Ryu, Chun-Li, and Zangief are from 2026-05-27; the other 26
  characters are from 2026-05-30.

## Open questions

- When, if ever, should display-only command notation become a formal wiki
  notation schema?
- Which official source should be ingested to explain frame-data update history?
- Should JP, Ryu, Chun-Li, and Zangief be recaptured under a 2026-05-30 date
  label to make the full-roster snapshot single-date?
