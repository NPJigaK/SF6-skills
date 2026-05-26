---
type: review
review_type: capture_validation
created: 2026-05-27
status: accepted
sources:
  - "[[sources/capcom-official-zangief-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/zangief]]"
tags:
  - review
  - frame-data
  - official
---

# Official Zangief Frame Data Capture Review - 2026-05-27

## Summary

The official Zangief frame-data raw snapshot and derived outputs were captured,
validated by full-row tool checks, reviewed by the human, and accepted.

## Reviewed files

- `raw/official/frame-data/2026-05-27/zangief/classic/screenshot.png`
- `raw/official/frame-data/2026-05-27/zangief/modern/screenshot.png`
- `raw/official/frame-data/2026-05-27/zangief/classic/table.dom.json`
- `raw/official/frame-data/2026-05-27/zangief/modern/table.dom.json`
- `raw/official/frame-data/2026-05-27/zangief/classic/metadata.json`
- `raw/official/frame-data/2026-05-27/zangief/modern/metadata.json`
- `raw/official/frame-data/2026-05-27/zangief/manifest.json`
- `wiki/outputs/data/frame-data/zangief/classic.csv`
- `wiki/outputs/data/frame-data/zangief/modern.csv`
- `wiki/outputs/data/frame-data/zangief/classic.field-meanings.json`
- `wiki/outputs/data/frame-data/zangief/modern.field-meanings.json`

## Automated checks

- Raw placement under `raw/official/frame-data/2026-05-27/zangief/<classic|modern>/`
  follows the official frame-data snapshot convention.
- Metadata and manifest include publisher, source URL, capture timestamps,
  character slug, and control scheme.
- Classic and Modern outputs were captured separately.
- DOM captures retain move names, input icons, frame values, cancel values,
  damage, notes, and related fields.
- `page.html` table hashes match the corresponding `table.dom.json`
  `table_sha256` values for both control schemes.
- Every row and every CSV field exactly matches data regenerated from the raw
  DOM for both Classic and Modern.
- The field-meanings JSON files exactly match tooltip/header explanations
  regenerated from the raw DOM for both Classic and Modern.
- Classic DOM, manifest, and derived CSV all report 72 data rows.
- Modern DOM, manifest, and derived CSV all report 66 data rows.
- Overlay cleanup metadata reports zero visible Cookiebot and navigation
  elements after cleanup.
- Screenshot coverage checks show both Classic and Modern screenshots are wide
  enough to include the table right edge and tall enough to include the table
  height; visual inspection also confirms the Zangief page, selected tab, table,
  character select, and footer are visible.
- Field meanings JSON contains header explanations extracted from the table
  header: Classic has 7 records and Modern has 8 records, including the Modern
  SP-button 80% damage note.
- Zangief-specific inputs such as `key-circle`, `key-circle key-circle`,
  Modern SP shortcuts, and one/two-circle command-grab rows are retained in
  `input_token_json`.

## All-row data validation

Command:

```bash
uv run python tools/validate_capcom_frame_data.py --character-slug zangief --date-label 2026-05-27
```

Result:

| Mode | Rows | Category rows | Field-meaning records | Screenshot size |
|---|---:|---:|---:|---|
| Classic | 72 | 6 | 7 | 2271 x 10421 |
| Modern | 66 | 6 | 8 | 2367 x 10056 |

This validates all table rows and fields against the raw HTML / raw DOM-derived
data, not only representative rows. The screenshot is used to validate visual
coverage of the captured table and page state; cell-value correctness is
validated against raw HTML and DOM because OCR from a raster screenshot would be
less reliable than the captured source data.

## Final decision

Accepted.

## Requires human review

- No blocker remains for this capture.
