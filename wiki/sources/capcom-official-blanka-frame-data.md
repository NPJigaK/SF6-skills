---
type: source
source_type: official_frame_data
title: "Capcom official Blanka frame data"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/official/frame-data/2026-05-30/blanka/manifest.json"
original_url: "https://www.streetfighter.com/6/ja-jp/character/blanka/frame"
created: 2026-05-30
updated: 2026-05-30
captured_at_utc: "2026-05-30T06:43:33Z"
status: active
confidence: high
tags:
  - sf6
  - official
  - frame-data
related_concepts:
  - "[[concepts/frame-data]]"
related_entities:
  - "[[entities/capcom]]"
  - "[[entities/street-fighter-6]]"
  - "[[entities/blanka]]"
---

# Source: Capcom Official Blanka Frame Data

## One-line summary

Capcom's official Street Fighter 6 frame data page for Blanka (ブランカ),
captured as raw HTML, table DOM, screenshots, and derived CSV/field-meaning
outputs for Classic and Modern controls.

## Key takeaways

1. The raw source is stored as a dated immutable snapshot under
   `raw/official/frame-data/2026-05-30/blanka/`.
2. The Classic capture contains 91 data rows; the Modern capture contains
   83 data rows.
3. The derived CSVs keep move names, raw input token displays, full input token
   JSON, frame values, cancel values, damage, combo scaling, Drive gauge values,
   SA gain, attributes, and notes.
4. Header tooltip/explanatory text is stored separately in
   `*.field-meanings.json`.
5. The raw capture has passed automated validation and is pending human review.

## Important claims

| Claim | Evidence | Confidence | Notes |
|---|---|---|---|
| The source publisher is Capcom and the page is the official Blanka frame data URL. | `raw/official/frame-data/2026-05-30/blanka/manifest.json`; `raw/official/frame-data/2026-05-30/blanka/*/metadata.json` | high | Metadata records publisher, source URL, locale, character slug, and control scheme. |
| Classic and Modern were captured as separate tabs from the same official page. | `raw/official/frame-data/2026-05-30/blanka/classic/metadata.json`; `raw/official/frame-data/2026-05-30/blanka/modern/metadata.json` | high | Metadata records tab index 0 for Classic and 1 for Modern. |
| The derived data has 91 Classic rows and 83 Modern rows. | `raw/official/frame-data/2026-05-30/blanka/manifest.json`; `wiki/outputs/data/frame-data/blanka/classic.csv`; `wiki/outputs/data/frame-data/blanka/modern.csv` | high | Validation reproduced the same row counts from raw DOM and saved CSV. |
| Header help text is captured outside the row CSV. | `wiki/outputs/data/frame-data/blanka/classic.field-meanings.json`; `wiki/outputs/data/frame-data/blanka/modern.field-meanings.json` | high | This separates field semantics from per-move rows. |

## Related concepts

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[concepts/drive-system]]

## Related entities

- [[entities/capcom]]
- [[entities/street-fighter-6]]
- [[entities/blanka]]

## Contradictions or updates to existing wiki

- This source expands official frame-data coverage beyond the previously
  ingested JP, Ryu, Chun-Li, and Zangief captures.
- It does not promote individual move values into durable move-specific wiki
  summaries; those remain in the raw DOM and derived CSV outputs.

## Open questions

- Should this capture be marked accepted after human screenshot/source review?
- Which Blanka move values, if any, should be promoted into durable
  move-specific wiki summaries instead of remaining only in source and output
  data?

## Source notes

- Raw manifest: `raw/official/frame-data/2026-05-30/blanka/manifest.json`
- Classic raw capture: `raw/official/frame-data/2026-05-30/blanka/classic/`
- Modern raw capture: `raw/official/frame-data/2026-05-30/blanka/modern/`
- Derived Classic CSV: `wiki/outputs/data/frame-data/blanka/classic.csv`
- Derived Modern CSV: `wiki/outputs/data/frame-data/blanka/modern.csv`
- Derived field meanings:
  - `wiki/outputs/data/frame-data/blanka/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/blanka/modern.field-meanings.json`
