---
type: review
review_type: capture_validation
created: 2026-05-27
status: accepted
sources:
  - "[[sources/capcom-official-ryu-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/ryu]]"
tags:
  - review
  - frame-data
  - official
---

# Official Ryu Frame Data Capture Review - 2026-05-27

## Summary

The official Ryu frame-data raw snapshot and derived outputs were captured,
validated by tool checks, reviewed by the human, and accepted.

## Reviewed files

- `raw/official/frame-data/2026-05-27/ryu/classic/screenshot.png`
- `raw/official/frame-data/2026-05-27/ryu/modern/screenshot.png`
- `raw/official/frame-data/2026-05-27/ryu/classic/table.dom.json`
- `raw/official/frame-data/2026-05-27/ryu/modern/table.dom.json`
- `raw/official/frame-data/2026-05-27/ryu/classic/metadata.json`
- `raw/official/frame-data/2026-05-27/ryu/modern/metadata.json`
- `raw/official/frame-data/2026-05-27/ryu/manifest.json`
- `wiki/outputs/data/frame-data/ryu/classic.csv`
- `wiki/outputs/data/frame-data/ryu/modern.csv`
- `wiki/outputs/data/frame-data/ryu/classic.field-meanings.json`
- `wiki/outputs/data/frame-data/ryu/modern.field-meanings.json`

## Automated checks

- Raw placement under `raw/official/frame-data/2026-05-27/ryu/<classic|modern>/`
  follows the official frame-data snapshot convention.
- Metadata and manifest include publisher, source URL, capture timestamps,
  character slug, and control scheme.
- Classic and Modern tabs were captured separately.
- DOM captures retain move names, input icons, frame values, cancel values,
  damage, notes, and related fields.
- Classic DOM, manifest, and derived CSV all report 75 data rows.
- Modern DOM, manifest, and derived CSV all report 69 data rows.
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
