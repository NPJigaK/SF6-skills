# Current-Fact Export

- JSON artifact: `data/current-facts/20260525T000000Z-current-fact-export.json`
- Run ID: `20260525T000000Z`
- Source-record input: `data/current-facts/source-records/20260525T000000Z-current-fact-source-records.json`
- Total records: `13`
- Export boundary: source-record sidecar fields are excluded.
- Calculation boundary: non-scalar values remain not calculation-safe.
- Authority boundary: official values remain authority candidates only.
- Runtime lookup and answer behavior are unchanged.

## Counts

| Dimension | Value | Count |
| --- | --- | --- |
| calculation_input_status | `annotated_candidate_not_calculation_safe` | 9 |
| calculation_input_status | `parsed_range_not_single_value_calculation_safe` | 4 |
| field_key | `block_advantage` | 5 |
| field_key | `hit_advantage` | 4 |
| field_key | `startup` | 4 |

## Boundaries

- No runtime current-fact lookup switch is included.
- `annotated_numeric_candidate` and `frame_range` must not be flattened into scalar values.
- Legacy raw exports, ignored local artifacts, raw source payloads, reviewer observations, and private data are excluded as authority.
