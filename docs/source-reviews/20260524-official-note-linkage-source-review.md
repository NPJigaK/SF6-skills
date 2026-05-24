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

The v4 structured official table-row artifacts preserve source-native column
paths, raw cell text, visible text, hidden detail text, row identity, row-local
notes, cell note markers, cell note ids, row note reference candidates, and note
linkage status. These fields are sufficient to distinguish groups with
deterministic single-candidate note evidence from groups that remain ambiguous.

This update used existing ignored official v4 artifacts as reviewer input only.
No live acquisition was run. No reviewer-only ChatGPT/VLM observation was used.

The review outcome is:

- `structured_row_note_evidence_found`: `4`
- `structured_row_note_evidence_ambiguous`: `4`
- `source_confirmed_non_note_grammar_blocked`: `1`

The `4` ambiguous groups remain blocked pending source review. The `4` found
groups are only later annotated-parser candidates; no parser approval,
calculation-safe value, numeric authority, or current-fact authority is added.

## Decisions

| Review item | Field | Source header path | Affected | Result | Later parser eligibility | Notes |
| --- | --- | --- | ---: | --- | --- | --- |
| `value-shape:official--source_specific_expression--sa` | `sa_gain` | `SAゲージ増加` | 8 | `structured_row_note_evidence_ambiguous` | `blocked_pending_source_review` | v4 row notes expose row-local text, but representative cells have multiple same-row `※` candidates, including damage and SA-gauge notes. |
| `value-shape:official--source_specific_expression--u_55d872f6091a` | `combo_scaling` | `コンボ補正値` | 55 | `structured_row_note_evidence_ambiguous` | `blocked_pending_source_review` | Most representative rows have a single candidate, but some rows still have multiple same-row `※` candidates. |
| `value-shape:official--source_specific_expression--u_202a059d9b1b` | `damage` | `ダメージ` | 36 | `structured_row_note_evidence_ambiguous` | `blocked_pending_source_review` | v4 evidence confirms damage column boundaries, but at least one representative row has multiple same-row `※` candidates. |
| `value-shape:official--malformed_looking_source_value--u_fdb49a2113ba--u_c2b75204faf1` | `active` | `動作フレーム > 持続` | 3 | `source_confirmed_non_note_grammar_blocked` | `not_note_linkage_target` | v4 evidence confirms representative active values have no cell note markers; dot and double-hyphen grammar remains outside this review. |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_c2b75204faf1` | `active` | `動作フレーム > 持続` | 44 | `structured_row_note_evidence_ambiguous` | `blocked_pending_source_review` | Active cells still mix standalone markers, bracketed note ids, and visible/hidden detail concatenation, with ambiguous representative rows. |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `startup` | `動作フレーム > 発生` | 6 | `structured_row_note_evidence_found` | `later_annotated_parser_eligible` | Representative startup suffix-marker values have a single same-row note candidate. |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | `recovery` | `動作フレーム > 硬直` | 28 | `structured_row_note_evidence_found` | `later_annotated_parser_eligible` | Representative recovery-column values have a single same-row note candidate; `全体` remains a later total-duration/schema concern. |
| `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `block_advantage` | `硬直差 > ガード` | 6 | `structured_row_note_evidence_found` | `later_annotated_parser_eligible` | Representative block-advantage marker values have a single same-row note candidate; this is not scalar advantage calculation approval. |
| `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `hit_advantage` | `硬直差 > ヒット` | 4 | `structured_row_note_evidence_found` | `later_annotated_parser_eligible` | Representative hit-advantage marker values have a single same-row note candidate; this is not scalar advantage calculation approval. |

## Boundary Notes

- Official remains authority candidate only.
- No current-fact authority is added.
- No parser output or calculation-safe value is emitted.
- `later_annotated_parser_eligible` means source-review readiness for a future
  ExecPlan only.
- No full source rows, raw source dumps, browser images, local paths, cookies,
  browser profiles, traces, debug dumps, answer logs, training logs, or
  private data are included.
