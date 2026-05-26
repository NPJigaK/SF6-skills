---
type: source
source_type: official_frame_data
title: "Capcom official Chun-Li frame data"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/official/frame-data/2026-05-27/chunli/manifest.json"
original_url: "https://www.streetfighter.com/6/ja-jp/character/chunli/frame"
created: 2026-05-27
updated: 2026-05-27
captured_at_utc: "2026-05-26T21:11:01Z"
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
  - "[[entities/chun-li]]"
---

# Source: Capcom Official Chun-Li Frame Data

## One-line summary

Capcom's official Street Fighter 6 frame data page for Chun-Li, captured as
raw HTML, table DOM, screenshots, and derived CSV/field-meaning outputs for
Classic and Modern controls.

## Key takeaways

1. The raw source is stored as a dated immutable snapshot under
   `raw/official/frame-data/2026-05-27/chunli/`.
2. The Classic capture contains 78 data rows; the Modern capture contains 72
   data rows.
3. The derived CSVs keep move names, raw input token displays, full input token
   JSON, frame values, cancel values, damage, combo scaling, Drive gauge values,
   SA gain, attributes, and notes.
4. Header tooltip/explanatory text is stored separately in
   `*.field-meanings.json`.
5. The raw capture was reviewed and accepted by the human reviewer.

## Important claims

| Claim | Evidence | Confidence | Notes |
|---|---|---|---|
| The source publisher is Capcom and the page is the official Chun-Li frame data URL. | `raw/official/frame-data/2026-05-27/chunli/manifest.json`; `raw/official/frame-data/2026-05-27/chunli/*/metadata.json` | high | Metadata records publisher, source URL, locale, character slug, and control scheme. |
| Classic and Modern were captured as separate tabs from the same official page. | `raw/official/frame-data/2026-05-27/chunli/classic/metadata.json`; `raw/official/frame-data/2026-05-27/chunli/modern/metadata.json` | high | Metadata records tab index 0 for Classic and 1 for Modern. |
| The derived data has 78 Classic rows and 72 Modern rows. | `raw/official/frame-data/2026-05-27/chunli/manifest.json`; `wiki/outputs/data/frame-data/chunli/classic.csv`; `wiki/outputs/data/frame-data/chunli/modern.csv` | high | The extract command reproduced the same row counts from raw DOM. |
| Header help text is captured outside the row CSV. | `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json`; `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json` | high | This separates field semantics from per-move rows. |

## Related concepts

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[concepts/drive-system]]

## Related entities

- [[entities/capcom]]
- [[entities/street-fighter-6]]
- [[entities/chun-li]]

## Contradictions or updates to existing wiki

- This source adds a third official character frame-data capture after JP and
  Ryu.
- It helps stress-test the capture schema against a character with stance-like
  and special move table complexity, but it should not be generalized until
  human review accepts the capture.

## Open questions

- Should Chun-Li's Classic/Modern differences be filed back as a durable
  question page?
- Should command input tokens be normalized before comparing inputs across
  characters?
- Which character should be used next to stress-test unusual move table formats?

## Source notes

- Raw manifest: `raw/official/frame-data/2026-05-27/chunli/manifest.json`
- Classic raw capture: `raw/official/frame-data/2026-05-27/chunli/classic/`
- Modern raw capture: `raw/official/frame-data/2026-05-27/chunli/modern/`
- Derived Classic CSV: `wiki/outputs/data/frame-data/chunli/classic.csv`
- Derived Modern CSV: `wiki/outputs/data/frame-data/chunli/modern.csv`
- Derived field meanings:
  - `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json`
