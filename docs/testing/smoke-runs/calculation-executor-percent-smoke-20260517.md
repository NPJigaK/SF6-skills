# Calculation Executor Percent Smoke - 2026-05-17

## Summary

This smoke run verifies that the deterministic calculation executor can handle
SF6-shaped percentage arithmetic without becoming SF6 authority.

The calculation is intentionally hypothetical:

- base value: `80`
- modifier: `85%`
- computed output: `68`

This smoke run does not define or accept any SF6 combo scaling formula,
rounding rule, damage formula, current system mechanic, or public answer
behavior.

## Command

```bash
python packages/calculation-executor/sf6_calculation_executor.py \
  --input tests/fixtures/calculation-executor/hypothetical-percent-consistency.json \
  --pretty
```

## Trace Summary

| Field | Value |
|---|---|
| `trace_id` | `hypothetical-percent-consistency-001` |
| `trace_schema_version` | `sf6-calculation-trace/v1` |
| `executor_id` | `sf6_calculation_executor.py@v1` |
| `executor_role` | `calculation_executor` |
| `calculation_intent` | `hypothetical_arithmetic_check` |
| `input_status` | `hypothetical` |
| `calculation_instruction_status` | `hypothetical` |
| `rounding_instruction_status` | `not_applicable` |
| `operation_kind` | `percent_of` |
| `output_values.composed_percent` | `68` |
| `status` | `hypothetical_arithmetic_only` |
| `public_answer_allowed` | `false` |
| `generated_reference_allowed` | `false` |
| `accepted_current_fact_authority` | `false` |

## Boundary Audit

- The executor output is arithmetic trace evidence only.
- The trace is not SF6 authority.
- The trace is not formula authority.
- The trace is not rounding authority.
- The trace is not current-fact authority.
- The fixture has no non-hypothetical `input_reference_refs` because the values
  are hypothetical.
- The trace does not cite generated references, video observations,
  review-only candidates, combo fixtures, or current-fact surfaces as
  calculation authority.
- The trace must not support public current-fact answers.

## What Was Not Done

- No third-party math skill was installed.
- No SF6 formula was accepted.
- No combo damage, scaling table, minimum guarantee, frame timing, punish
  window, meaty/oki, resource, or rounding policy was added.
- No public `sf6-agent` behavior changed.
- No generated references, frame-current assets, normalization assets,
  `data/exports`, `data/roster`, `official_raw`, `.dist`, or current facts were
  changed.
- No Hermes memory, sessions, raw transcripts, logs, caches, credentials,
  secrets, tokens, or hidden tool state were committed.

## Validation

- `python packages/calculation-executor/sf6_calculation_executor.py --input tests/fixtures/calculation-executor/hypothetical-percent-consistency.json --pretty`
  - PASS
- `pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-calculation-executor.ps1`
  - PASS
