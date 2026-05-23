# Official Note Linkage Source Review

This is a source-review summary only. It does not implement parser, schema,
classifier, calculator, retrieval, answer behavior, export behavior, or
numeric authority.

- Run ID: `20260524`
- Input coverage:
  `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- Input disposition:
  `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- Review records: `9`

## Source Evidence Summary

The current structured official table-row artifacts preserve source-native
column paths, raw cell text, visible text, hidden detail text, and row
identity. They do not expose row-local note text as structured fields.

Reviewer inspection of the ignored official HTML captures found row-local note
evidence for the note-bearing groups. Because those notes are not present as
structured table-row fields, every note-bearing group remains blocked pending
acquisition-field support before parser work.

No live acquisition was run for this source review.

## Decisions

| Review item | Field | Source header path | Affected | Result | Later parser eligibility | Notes |
| --- | --- | --- | ---: | --- | --- | --- |
| `value-shape:official--source_specific_expression--sa` | `sa_gain` | `SAゲージ増加` | 8 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | Marker links to row-local medal-level SA gauge conditions in reviewer evidence, but row notes are not structured in the table-row artifact. |
| `value-shape:official--source_specific_expression--u_55d872f6091a` | `combo_scaling` | `コンボ補正値` | 55 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | Row-local scaling notes vary by move; parser work needs per-row notes, not group-level assumptions. |
| `value-shape:official--source_specific_expression--u_202a059d9b1b` | `damage` | `ダメージ` | 36 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | `※` damage examples are confirmed inside the source-native damage column, not adjacent cancel cells. Row notes still need structured extraction. |
| `value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1` | `active` | `動作フレーム > 持続` | 3 | `source_confirmed_non_note_grammar_blocked` | `not_note_linkage_target` | Dot and double-hyphen active values are source-confirmed active cells, but this review does not resolve their grammar or calculation meaning. |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1` | `active` | `動作フレーム > 持続` | 44 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | Active cells mix standalone markers, bracketed note ids, component markers, and hidden-detail text. Future parsing must use separated visible and hidden fields. |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `startup` | `動作フレーム > 発生` | 6 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | Suffix markers are row-local conditional startup values. |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | `recovery` | `動作フレーム > 硬直` | 28 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | `全体` values must not be treated as ordinary recovery frames. |
| `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `block_advantage` | `硬直差 > ガード` | 6 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | Block advantage markers are row-local conditions; embedded alternate forms require a separate parser rule. |
| `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `hit_advantage` | `硬直差 > ヒット` | 4 | `source_evidence_found_acquisition_field_gap` | `blocked_pending_acquisition_fields` | Hit advantage markers are row-local conditions; positive values remain column-context dependent. |

## Boundary Notes

- Official remains authority candidate only.
- No current-fact authority is added.
- No parser output or calculation-safe value is emitted.
- No full source rows, raw source dumps, browser images, local paths, cookies,
  browser profiles, traces, debug dumps, answer logs, training logs, or
  private data are included.
