---
type: source
source_type: official_frame_data
title: "Capcom official JP frame data"
author: "Capcom"
publisher: "Capcom"
raw_path: "raw/official/frame-data/2026-05-26/jp/manifest.json"
original_url: "https://www.streetfighter.com/6/ja-jp/character/jp/frame"
created: 2026-05-26
updated: 2026-05-30
captured_at_utc: "2026-05-26T09:04:33Z"
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
  - "[[entities/jp]]"
---

# Source: Capcom Official JP Frame Data

## One-line summary

Capcom's official Street Fighter 6 frame data page for JP, captured as reviewed raw HTML, table DOM, screenshots, and derived CSV/field-meaning outputs for Classic and Modern controls.

## Key takeaways

1. The raw source is stored as a dated immutable snapshot under `raw/official/frame-data/2026-05-26/jp/`.
2. The Classic capture contains 69 data rows; the Modern capture contains 65 data rows.
3. The derived CSVs keep move names, raw input token displays, full input token JSON, frame values, cancel values, damage, combo scaling, Drive gauge values, SA gain, attributes, and notes.
4. Input icons are preserved in `input_token_json`; `input_raw_display` is a raw DOM-token display, not a normalized command notation.
5. Header tooltip/explanatory text is stored separately in `*.field-meanings.json`, including cancel meanings, combo scaling meanings, Drive gauge meanings, attribute meanings, and the Modern SP-button damage note.

## Important claims

| Claim | Evidence | Confidence | Notes |
|---|---|---|---|
| The source publisher is Capcom and the page is the official JP frame data URL. | `raw/official/frame-data/2026-05-26/jp/manifest.json`; `raw/official/frame-data/2026-05-26/jp/*/metadata.json` | high | Metadata records publisher, source URL, locale, character slug, and control scheme. |
| Classic and Modern were captured as separate tabs from the same official page. | `raw/official/frame-data/2026-05-26/jp/classic/metadata.json`; `raw/official/frame-data/2026-05-26/jp/modern/metadata.json` | high | Metadata records tab index 0 for Classic and 1 for Modern. |
| The reviewed derived data has 69 Classic rows and 65 Modern rows. | `raw/official/frame-data/2026-05-26/jp/manifest.json`; `wiki/outputs/data/frame-data/jp/classic.csv`; `wiki/outputs/data/frame-data/jp/modern.csv` | high | Human review accepted the row counts against DOM-derived counts. |
| Header help text is captured outside the row CSV. | `wiki/outputs/data/frame-data/jp/classic.field-meanings.json`; `wiki/outputs/data/frame-data/jp/modern.field-meanings.json` | high | This separates field semantics from per-move rows. |

## Related concepts

- [[concepts/frame-data]]
- [[concepts/fighting-game-notation]]
- [[concepts/drive-system]]

## Related entities

- [[entities/capcom]]
- [[entities/street-fighter-6]]
- [[entities/jp]]

## Contradictions or updates to existing wiki

- This source remains the accepted JP frame-data snapshot after the 2026-05-30 batch expanded coverage to the full roster of 30 character data slugs.
- It does not replace community glossary terminology for juggle concepts; it provides official per-move frame data and field meanings.

## Open questions

- Should `input_token_json` be transformed into a normalized command notation later, or preserved as raw token data only?
- Should move-name variants across Classic and Modern be normalized for some
  comparison tasks, or should exact official move names remain the default?
- Should JP be recaptured under a 2026-05-30 date label to align with the new full-roster batch?
- Should official balance-change pages be ingested separately to explain why frame data changes over time?

## Source notes

- Raw manifest: `raw/official/frame-data/2026-05-26/jp/manifest.json`
- Classic raw capture: `raw/official/frame-data/2026-05-26/jp/classic/`
- Modern raw capture: `raw/official/frame-data/2026-05-26/jp/modern/`
- Derived Classic CSV: `wiki/outputs/data/frame-data/jp/classic.csv`
- Derived Modern CSV: `wiki/outputs/data/frame-data/jp/modern.csv`
- Derived field meanings:
  - `wiki/outputs/data/frame-data/jp/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/jp/modern.field-meanings.json`
