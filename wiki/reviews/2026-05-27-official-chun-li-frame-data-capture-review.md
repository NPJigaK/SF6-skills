---
type: review
review_type: capture_validation
created: 2026-05-27
status: accepted
sources:
  - "[[sources/capcom-official-chun-li-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/chun-li]]"
tags:
  - review
  - frame-data
  - official
---

# Official Chun-Li Frame Data Capture Review - 2026-05-27

## Summary

The official Chun-Li frame-data raw snapshot and derived outputs were captured,
validated by tool checks, reviewed by the human, and accepted.

## Reviewed files

- `raw/official/frame-data/2026-05-27/chunli/classic/screenshot.png`
- `raw/official/frame-data/2026-05-27/chunli/modern/screenshot.png`
- `raw/official/frame-data/2026-05-27/chunli/classic/table.dom.json`
- `raw/official/frame-data/2026-05-27/chunli/modern/table.dom.json`
- `raw/official/frame-data/2026-05-27/chunli/classic/metadata.json`
- `raw/official/frame-data/2026-05-27/chunli/modern/metadata.json`
- `raw/official/frame-data/2026-05-27/chunli/manifest.json`
- `wiki/outputs/data/frame-data/chunli/classic.csv`
- `wiki/outputs/data/frame-data/chunli/modern.csv`
- `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json`
- `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json`

## Automated checks

- Raw placement under `raw/official/frame-data/2026-05-27/chunli/<classic|modern>/`
  follows the official frame-data snapshot convention.
- Metadata and manifest include publisher, source URL, capture timestamps,
  character slug, and control scheme.
- Classic and Modern tabs were captured separately.
- DOM captures retain move names, input icons, frame values, cancel values,
  damage, notes, and related fields.
- Classic DOM, manifest, and derived CSV all report 78 data rows.
- Modern DOM, manifest, and derived CSV all report 72 data rows.
- Overlay cleanup metadata reports no visible Cookiebot or navigation overlays
  after cleanup.
- Screenshots were visually checked by the LLM and appear to include the full
  table width for both control schemes.
- Field meanings JSON contains header explanations extracted from the table
  header.

## Final decision

Accepted.

## Requires human review

- No blocker remains for this capture.
