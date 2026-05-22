# Value-Shape Blocked Source Review

This is a source-review summary only. It does not implement schema, parser,
retrieval, answer behavior, or numeric authority.

- Run ID: `20260521T025403Z`
- Input disposition: `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- Review records: `3`

## Decisions

| Review item | Source | Source header path | Recommendation | Notes |
| --- | --- | --- | --- | --- |
| `value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1` | `official` | `動作フレーム > 持続` | `parse_rule_required_before_schema` | Values such as `30-34.35`, `20-24.25`, and `23--33` are source-confirmed raw official active-frame strings. Preserve exactly; parser policy must decide dot and double-dash active-window notation. |
| `value-shape:official--source_specific_expression--u_1aa6a6f86513` | `official` | `技名` | `schema_supports_raw_only` | Note-bearing move names are source-confirmed raw labels. First normalized export can keep the full source move label raw. |
| `value-shape:supercombo--unclassified_expression--character_vitals--throw_range_hurtbox` | `supercombo` | `Character Vitals > Throw Range / Hurtbox` | `parse_rule_required_before_schema` | Source label names an ordered paired value: `Throw Range / Hurtbox`. Proposed components are `throw_range` and `hurtbox`; SuperCombo remains enrichment only. |

## Boundary Notes

- Official remains authority candidate only.
- SuperCombo remains enrichment/cross-reference/candidate only.
- No current-fact authority is added.
- No full raw rows, raw HTML, screenshots, local paths, cookies, browser
  profiles, traces, debug dumps, answer logs, training logs, or private data are
  included.
