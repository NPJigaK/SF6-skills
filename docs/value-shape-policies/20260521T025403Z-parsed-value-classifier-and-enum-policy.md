# Parsed-Value Classifier And Enum Policy

This is a policy summary only. It does not implement parsers, classifiers,
schema, retrieval, answer behavior, or numeric authority.

- Run ID: `20260521T025403Z`
- Input disposition: `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- Parse-rule policy records covered: `208`
- Enum policy records covered: `16`
- JSON Schema redesign status: `ready_for_schema_design_after_policy_review`

## Parse-Rule Policy Counts

| Semantic family | Records | Schema shapes |
| --- | ---: | --- |
| `advantage` | 50 | signed frame, knockdown, wall splat, stagger, parenthesized alternate, range advantage |
| `damage` | 18 | scalar, multihit, bracketed alternate, parenthesized total/scaled |
| `gauge` | 44 | scalar, parenthesized alternate, bracketed tagged value, multihit |
| `metadata` | 21 | decimal metric, juggle marker, range metric, bracketed marker |
| `mobility` | 7 | decimal metric, plus sequence |
| `projectile` | 3 | decimal metric, source-native speed note |
| `scaling` | 1 | percent note |
| `throw` | 1 | ordered pair: throw range, hurtbox |
| `timing` | 63 | frame scalar, range, active-window sequence, parenthesized alternate, total duration, plus sequence, landing condition, source note marker |

## Enum Policy Counts

| Semantic family | Records | Policy |
| --- | ---: | --- |
| `attribute` | 1 | source-native enum required |
| `cancel` | 6 | source-native enum required |
| `defense` | 9 | source-native enum required |

## Boundary Notes

- Official remains authority candidate only.
- SuperCombo remains enrichment/cross-reference/candidate only.
- The policy defines schema-design input shapes, not parser output.
- Parser/classifier implementation remains a later ExecPlan.
