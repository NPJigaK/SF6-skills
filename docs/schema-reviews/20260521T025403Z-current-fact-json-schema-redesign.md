# Current-Fact JSON Schema Redesign Review

This review records the first schema artifact boundary for normalized
current-fact records.

The schemas are structural contracts only. They do not implement parsing, do
not generate normalized exports, do not change retrieval or answer behavior,
and do not promote any source to daily-answer numeric authority.

## Inputs

- `docs/execplans/2026-05-23-current-fact-json-schema-redesign.md`
- `data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json`
- `data/field-mappings/20260521T025403Z-supercombo-canonical-field-mapping-summary.json`
- `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-and-enum-policy.json`
- `data/validator-audits/20260523-validator-test-fact-source-audit.json`

## Decisions

- Use JSON Schema Draft 2020-12.
- Keep `source_family` as a semantic category only.
- Keep source identity in `source_name`.
- Keep evidence role in `source_role`.
- Keep answer authority in `authority_status`.
- Require `raw_value` even when `parsed_value` is present.
- Allow `parsed_value` only as an optional policy-gated structure.
- Keep SuperCombo as enrichment or cross-reference candidate only.

## Fixture Coverage

- official signed frame
- official frame range
- official raw-preserved move name
- synthetic SuperCombo cross-reference signed frame
- synthetic SuperCombo review-required ordered-pair source case
- invalid `source_family: official`
- invalid SuperCombo authority promotion

## Limits

These schemas do not prove parser correctness or source truth. The SuperCombo
fixtures are synthetic contract fixtures, not observed game facts. The schemas
define the shape of records that later parser and export work must satisfy.
