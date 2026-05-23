# Validator Test Fact Source Audit

This audit classifies what each current test or validator is allowed to prove.
It is not a claim that every source value has been semantically parsed.

## Rule

A passing validator may prove only its declared evidence class. Do not adjust a
validator to match generated output unless the expected value is grounded in a
source artifact, approved policy artifact, synthetic contract fixture, or
privacy/security boundary.

## Findings

| File | Evidence class | Status | Limitation |
| --- | --- | --- | --- |
| `tests/test_cli.py` | source-derived | accepted with limits | JP 5LP smoke only; not full roster validation |
| `tests/test_source_acquisition.py` | synthetic contract | accepted with limits | synthetic HTML tests parser/guard behavior, not live source truth |
| `tests/test_supercombo_field_mapping.py` | policy-derived | accepted with limits | mapping counts are reviewed policy output, not live SuperCombo proof |
| `tests/test_value_shape_disposition.py` | artifact consistency | accepted with limits | disposition coverage is not parse semantics |
| `tests/test_parsed_value_classifier.py` | policy-derived | accepted with limits | parser/classifier behavior is policy-derived and not calculation correctness |
| `tests/test_value_shape_inventory.py` | source-derived | accepted with limits | representative shape checks are not parser semantics |
| `tests/validation/validate_clean_slate.py` | governance boundary | accepted with limits | repo shape only |
| `tests/validation/validate_current_fact_schemas.py` | synthetic contract | accepted with limits | schema and fixture contracts only; no parser/source truth |
| `tests/validation/validate_official_note_linkage_source_review.py` | source-derived | accepted with limits | source-review summary; full row-note context remains ignored local evidence |
| `tests/validation/validate_parsed_value_classifier.py` | artifact consistency | accepted with limits | coverage artifact, mechanics anchors, and schema-compatible samples only |
| `tests/validation/validate_validator_test_audit.py` | governance boundary | accepted with limits | audit coverage and evidence metadata only |
| `tests/validation/validate_supercombo_field_mapping.py` | policy-derived | accepted with limits | delegates to mapping artifact validation |
| `tests/validation/validate_value_shape_disposition.py` | artifact consistency | accepted with limits | validates disposition structure, not source truth |
| `tests/validation/validate_value_shape_inventory.py` | source-derived | accepted with limits | summarized inventory; no live re-fetch |
| `tests/validation/validate_value_shape_policy.py` | policy-derived | accepted with limits | policy coverage only; no parser correctness |
| `tests/validation/validate_value_shape_source_review.py` | source-derived | accepted with limits | source-review summary; full raw context remains ignored local data |

## Schema Gate

JSON Schema redesign may use these artifacts as reviewed inputs, but it must
not treat artifact-consistency or policy-derived validators as proof of source
truth. Parser/classifier implementation still needs its own evidence and tests.
