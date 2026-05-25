# Current-Fact Source-Record Input

- JSON artifact: `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`
- Run ID: `20260525T000000Z`
- Source candidate input: `data/current-facts/candidate-inputs/20260525T000000Z-row-move-cell-candidates.json`
- Total records: `13`
- Source-record boundary: parsed-value-only, non-scalar values remain not calculation-safe.
- Authority boundary: official values remain authority candidates only.
- Legacy raw exports, ignored local artifacts, raw source payloads, reviewer observations, and private data are excluded as authority.

## Counts

| Dimension | Value | Count |
| --- | --- | --- |
| calculation_input_status | `annotated_candidate_not_calculation_safe` | 9 |
| calculation_input_status | `parsed_range_not_single_value_calculation_safe` | 4 |
| field_key | `block_advantage` | 5 |
| field_key | `hit_advantage` | 4 |
| field_key | `startup` | 4 |

## Boundaries

- No production current-fact export artifact is generated.
- Runtime lookup and answer behavior are unchanged.
- `annotated_numeric_candidate` and `frame_range` must not be flattened into scalar values.
