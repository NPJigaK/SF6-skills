---
type: review
review_type: human_review
created: 2026-05-26
status: accepted
sources:
  - "[[sources/capcom-official-jp-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/jp]]"
tags:
  - review
  - frame-data
  - official
---

# Official JP Frame Data Capture Review - 2026-05-26

## Summary

The official JP frame-data raw snapshot and derived outputs were reviewed and accepted for wiki ingest.

## Reviewed files

- `raw/official/frame-data/2026-05-26/jp/classic/screenshot.png`
- `raw/official/frame-data/2026-05-26/jp/modern/screenshot.png`
- `raw/official/frame-data/2026-05-26/jp/classic/table.dom.json`
- `raw/official/frame-data/2026-05-26/jp/modern/table.dom.json`
- `raw/official/frame-data/2026-05-26/jp/classic/metadata.json`
- `raw/official/frame-data/2026-05-26/jp/modern/metadata.json`
- `raw/official/frame-data/2026-05-26/jp/manifest.json`
- `wiki/outputs/data/frame-data/jp/classic.csv`
- `wiki/outputs/data/frame-data/jp/modern.csv`
- `wiki/outputs/data/frame-data/jp/classic.field-meanings.json`
- `wiki/outputs/data/frame-data/jp/modern.field-meanings.json`
- `tools/capture_capcom_frame_data.py`
- `tools/extract_capcom_frame_data.py`
- `pyproject.toml`
- `uv.lock`
- `README.md`

## Findings

### Medium: default source URL was JP-specific

`tools/capture_capcom_frame_data.py` previously defaulted `--source-url` to the JP page. This was safe for the reviewed JP capture but would be unsafe for future character captures if only `--character-slug` changed.

Resolution: fixed before ingest. The capture tool now derives the URL from `--character-slug` when `--source-url` is omitted and validates that an explicit URL matches the slug.

### Low: raw HTML has trailing whitespace

`git diff --cached --check` reports trailing whitespace in raw `page.html` files.

Resolution: no raw normalization. These files are raw official page snapshots, so whitespace checks should exclude `raw/official/**/page.html` if enforced later.

## Accepted checks

- Raw placement under `raw/official/frame-data/2026-05-26/jp/<classic|modern>/` is suitable for immutable official snapshots.
- Metadata and manifest include publisher, source URL, capture timestamps, character slug, and control scheme.
- Screenshots include the full official table for Classic and Modern.
- Classic and Modern tabs were captured separately.
- DOM captures retain move names, input icons, frame values, cancel values, damage, notes, and related fields.
- Classic CSV contains 69 data rows and Modern CSV contains 65 data rows, matching the DOM counts.
- Modern input tokens such as `modern_auto`, `modern_sp`, `key-or`, and parenthesized alternate inputs are retained in `input_token_json`.
- Field meanings JSON contains header explanations for cancel values, active frames, combo scaling, Drive gauge gain/loss, attributes, and Modern SP-button damage.

## Final decision

The raw snapshot and derived outputs are accepted. Wiki ingest may proceed.

## Requires human review

- No blocker remains for this capture.
