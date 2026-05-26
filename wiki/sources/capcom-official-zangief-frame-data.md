---
type: source
source_type: official_frame_data
title: "Capcom official Zangief frame data"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/official/frame-data/2026-05-27/zangief/manifest.json"
original_url: "https://www.streetfighter.com/6/ja-jp/character/zangief/frame"
created: 2026-05-27
updated: 2026-05-27
captured_at_utc: "2026-05-26T21:41:49Z"
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
  - "[[entities/zangief]]"
---

# Source: Capcom Official Zangief Frame Data

## One-line summary

Capcom's official Street Fighter 6 frame data page for Zangief, captured as raw
HTML, table DOM, screenshots, and derived CSV/field-meaning outputs for Classic
and Modern controls.

## Key takeaways

1. The raw source is stored as a dated immutable snapshot under
   `raw/official/frame-data/2026-05-27/zangief/`.
2. The Classic capture contains 72 data rows; the Modern capture contains 66
   data rows.
3. The derived CSVs keep move names, raw input token displays, full input token
   JSON, frame values, cancel values, damage, combo scaling, Drive gauge values,
   SA gain, attributes, and notes.
4. Header tooltip/explanatory text is stored separately in
   `*.field-meanings.json`.
5. The capture includes Zangief-specific command-grab and one/two-circle input
   patterns, which makes it useful for stress-testing command input capture.
6. The raw capture was reviewed and accepted by the human reviewer.

## Important claims

| Claim | Evidence | Confidence | Notes |
|---|---|---|---|
| The source publisher is Capcom and the page is the official Zangief frame data URL. | `raw/official/frame-data/2026-05-27/zangief/manifest.json`; `raw/official/frame-data/2026-05-27/zangief/*/metadata.json` | high | Metadata records publisher, source URL, locale, character slug, and control scheme. |
| Classic and Modern were captured as separate control-scheme outputs from the same official page. | `raw/official/frame-data/2026-05-27/zangief/classic/metadata.json`; `raw/official/frame-data/2026-05-27/zangief/modern/metadata.json` | high | The raw paths, metadata, screenshots, and table DOM files are separated by control scheme. |
| The derived data has 72 Classic rows and 66 Modern rows. | `raw/official/frame-data/2026-05-27/zangief/manifest.json`; `wiki/outputs/data/frame-data/zangief/classic.csv`; `wiki/outputs/data/frame-data/zangief/modern.csv` | high | The extract command reproduced the same row counts from raw DOM. |
| Header help text is captured outside the row CSV. | `wiki/outputs/data/frame-data/zangief/classic.field-meanings.json`; `wiki/outputs/data/frame-data/zangief/modern.field-meanings.json` | high | This separates field semantics from per-move rows. |

## Related concepts

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[concepts/drive-system]]

## Related entities

- [[entities/capcom]]
- [[entities/street-fighter-6]]
- [[entities/zangief]]

## Contradictions or updates to existing wiki

- This source adds a fourth official character frame-data capture after JP, Ryu,
  and Chun-Li.
- It helps stress-test the capture schema against one/two-circle inputs,
  command grabs, and throw-heavy move data.

## Open questions

- Should Zangief's Classic/Modern differences be filed back as a durable
  question page?
- Should command input tokens such as `key-circle` be normalized into readable
  command notation for future answer pages?
- Which character should be used next to stress-test unusual move table formats?

## Source notes

- Raw manifest: `raw/official/frame-data/2026-05-27/zangief/manifest.json`
- Classic raw capture: `raw/official/frame-data/2026-05-27/zangief/classic/`
- Modern raw capture: `raw/official/frame-data/2026-05-27/zangief/modern/`
- Derived Classic CSV: `wiki/outputs/data/frame-data/zangief/classic.csv`
- Derived Modern CSV: `wiki/outputs/data/frame-data/zangief/modern.csv`
- Derived field meanings:
  - `wiki/outputs/data/frame-data/zangief/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/zangief/modern.field-meanings.json`
