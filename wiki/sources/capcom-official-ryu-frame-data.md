---
type: source
source_type: official_frame_data
title: "Capcom official Ryu frame data"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/official/frame-data/2026-05-27/ryu/manifest.json"
original_url: "https://www.streetfighter.com/6/ja-jp/character/ryu/frame"
created: 2026-05-27
updated: 2026-05-30
captured_at_utc: "2026-05-26T20:37:11Z"
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
  - "[[entities/ryu]]"
---

# Source: Capcom Official Ryu Frame Data

## One-line summary

Capcom's official Street Fighter 6 frame data page for Ryu, captured as raw
HTML, table DOM, screenshots, and derived CSV/field-meaning outputs for Classic
and Modern controls.

## Key takeaways

1. The raw source is stored as a dated immutable snapshot under
   `raw/official/frame-data/2026-05-27/ryu/`.
2. The Classic capture contains 75 data rows; the Modern capture contains 69
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
| The source publisher is Capcom and the page is the official Ryu frame data URL. | `raw/official/frame-data/2026-05-27/ryu/manifest.json`; `raw/official/frame-data/2026-05-27/ryu/*/metadata.json` | high | Metadata records publisher, source URL, locale, character slug, and control scheme. |
| Classic and Modern were captured as separate tabs from the same official page. | `raw/official/frame-data/2026-05-27/ryu/classic/metadata.json`; `raw/official/frame-data/2026-05-27/ryu/modern/metadata.json` | high | Metadata records tab index 0 for Classic and 1 for Modern. |
| The derived data has 75 Classic rows and 69 Modern rows. | `raw/official/frame-data/2026-05-27/ryu/manifest.json`; `wiki/outputs/data/frame-data/ryu/classic.csv`; `wiki/outputs/data/frame-data/ryu/modern.csv` | high | The extract command reproduced the same row counts from raw DOM. |
| Header help text is captured outside the row CSV. | `wiki/outputs/data/frame-data/ryu/classic.field-meanings.json`; `wiki/outputs/data/frame-data/ryu/modern.field-meanings.json` | high | This separates field semantics from per-move rows. |

## Related concepts

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[concepts/drive-system]]

## Related entities

- [[entities/capcom]]
- [[entities/street-fighter-6]]
- [[entities/ryu]]

## Contradictions or updates to existing wiki

- This source adds a second official character frame-data capture after JP.
- A later 2026-05-30 batch expanded coverage to the full roster of 30 character data slugs; this page remains the accepted Ryu snapshot.

## Open questions

- Should command input tokens be normalized before comparing inputs across
  characters?
- Should move-name variants across Classic and Modern be normalized for some
  comparison tasks, or should exact official move names remain the default?

## Source notes

- Raw manifest: `raw/official/frame-data/2026-05-27/ryu/manifest.json`
- Classic raw capture: `raw/official/frame-data/2026-05-27/ryu/classic/`
- Modern raw capture: `raw/official/frame-data/2026-05-27/ryu/modern/`
- Derived Classic CSV: `wiki/outputs/data/frame-data/ryu/classic.csv`
- Derived Modern CSV: `wiki/outputs/data/frame-data/ryu/modern.csv`
- Derived field meanings:
  - `wiki/outputs/data/frame-data/ryu/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/ryu/modern.field-meanings.json`
