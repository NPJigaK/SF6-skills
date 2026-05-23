# Review-Required Parser Schema Expansion

Status: Drafted for review; mandatory local review passed.

## Purpose

Plan the next parser/schema design unit for the `207` parsed-value classifier
groups that remain `review_required`.

This ExecPlan is docs-only. It analyzes and prioritizes the remaining blockers
so a later approved implementation plan can add focused `parsed_value` schema
kinds and deterministic parsers without adding calculators, retrieval changes,
answer behavior changes, or authority promotion.

## Current Evidence

Inputs:

- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-and-enum-policy.json`
- `docs/system-mechanics/20260523-supercombo-system-mechanics-parser-inputs.md`
- `contracts/current-facts/*.schema.json`

Current `review_required` count:

| Source | Source role | Count |
| --- | --- | ---: |
| `official` | `authority_candidate` | 11 |
| `supercombo` | `enrichment_candidate` | 141 |
| `supercombo` | `cross_reference_candidate` | 55 |
| Total | | 207 |

Counts by semantic family:

| Family | Official | SuperCombo | Total |
| --- | ---: | ---: | ---: |
| `timing` | 4 | 59 | 63 |
| `advantage` | 4 | 46 | 50 |
| `gauge` | 1 | 43 | 44 |
| `metadata` | 0 | 21 | 21 |
| `damage` | 1 | 17 | 18 |
| `mobility` | 0 | 7 | 7 |
| `projectile` | 0 | 3 | 3 |
| `scaling` | 1 | 0 | 1 |
| Total | 11 | 196 | 207 |

Expression-shape diagnostics are overlapping, because one group can contain
more than one blocker shape:

| Expression shape | Groups |
| --- | ---: |
| `parenthesized` | 139 |
| `prose_modifier` | 125 |
| `multihit` | 54 |
| `active_window` | 49 |
| `gauge_context` | 44 |
| `bracketed` | 43 |
| `plus_sequence` | 31 |
| `kd_stateful_advantage` | 26 |
| `slash_component` | 26 |
| `juggle` | 12 |
| `range_tilde` | 10 |
| `note_prefixed` | 7 |
| `note_suffixed` | 3 |
| `scaling` | 1 |
| `malformed_or_simple_review_required` | 1 |

The single `malformed_or_simple_review_required` group is an official active
frame group with examples such as `30-34.35`, `20-24.25`, and `23--33`. It
was source-reviewed as real official raw notation, but still needs explicit
parser policy and schema design before use. It must not be parsed by guessing.

## Scope

Included:

- Analyze all `207` classifier coverage groups whose
  `classifier_decision == "review_required"`.
- Prioritize official authority-candidate groups first, then SuperCombo
  cross-reference/enrichment groups.
- Group blockers by expression family:
  - note-prefixed and note-suffixed official values;
  - parenthesized values;
  - bracketed alternates or tags;
  - multihit values;
  - active-window expressions;
  - scaling expressions;
  - juggle fields;
  - `KD` and other stateful advantage values;
  - gauge context and unit/event requirements;
  - prose modifiers.
- Decide which groups need new `parsed_value` schema kinds, which can become
  `raw_preserved`, and which require later source review before parsing.
- Define future parser/schema acceptance criteria and validation needs.
- Preserve raw values and source labels as evidence in any future design.

Excluded:

- No parser implementation.
- No schema implementation.
- No calculator implementation.
- No normalized export generation.
- No retrieval changes.
- No answer behavior changes.
- No live acquisition.
- No official authority promotion.
- No SuperCombo numeric authority promotion.
- No LLM interpretation of raw values as authority.
- No SymPy calculation logic. SymPy remains reserved for a later calculator
  ExecPlan that consumes approved formulas and parsed values.

## Prioritization

Priority 1: official authority-candidate blockers.

These are the only remaining official groups in `review_required` and must be
resolved before any official numeric calculator can safely consume their
domains:

| Family | Field keys | Blocking shapes | Direction |
| --- | --- | --- | --- |
| `timing` | `startup`, `active`, `recovery` | note markers, bracketed notes, comma/range active windows, malformed-looking active ranges | New structured timing schemas plus explicit parser policy for source-reviewed malformed-looking notation |
| `advantage` | `block_advantage`, `hit_advantage` | note-prefixed signed frames, tilde ranges | Reuse existing plain frame schemas where possible; add annotated or conditioned wrappers only when notes/conditions require them |
| `damage` | `damage` | note-prefixed integer damage | New annotated numeric value schema or note-source review before parsing |
| `gauge` | `sa_gain` | note-prefixed Super Art gain | New annotated gauge value schema plus unit/event policy |
| `scaling` | `combo_scaling` | note-prefixed percent and combined scaling expressions | New scaling-rule schema, not a plain percent |

Priority 2: SuperCombo groups that cross-reference official concepts.

These remain enrichment/cross-reference only. They can inform parser design and
fixture coverage, but must not become daily-answer numeric authority:

| Family | Main blockers | Direction |
| --- | --- | --- |
| `timing` | active-window `X(n)Y`, total/recovery parenthesized values, landing or component sequences | New timing sequence and conditioned timing schemas |
| `advantage` | `KD`, `PC`, `CH`, Drive Rush, burnout, parenthesized alternates | New stateful or conditioned advantage schema |
| `damage` | multihit, bracketed alternates, parenthesized totals or scaled values | New hit-series and conditioned damage schemas |
| `gauge` | Drive/Super event context, multihit gain/damage, parenthesized hit/block variants | New resource-event amount schema with unit and event context |
| `metadata` | juggle fields, attack range alternates | New juggle schema and spatial metric variants |
| `mobility` | walk speeds, dash/jump distance, apex values with exceptions | New spatial/mobility metric schemas or raw-preserved if non-calculation |
| `projectile` | source-native speed notes and slash variants | Later source review before any calculator use |

## Schema Direction

Future schema/parser implementation should split the 207 groups into these
outcomes:

New `parsed_value` schema kinds likely required:

- `annotated_numeric`: numeric value plus source note marker or source note
  reference, for official `※` values when the note text is reviewed.
- `timing_sequence`: active windows, landing components, and plus-separated
  timing components with labels.
- `active_window_sequence`: `X(n)Y` style active windows with active and gap
  components preserved.
- `conditioned_value`: parenthesized, bracketed, or tagged alternate values
  with reviewed condition labels.
- `hit_series`: multihit damage/gauge/timing components with per-hit values
  and optional totals.
- `stateful_advantage`: advantage values with `knockdown`, `counter_hit`,
  `punish_counter`, `burnout_block`, `drive_rush_cancel`, or similar state.
- `scaling_rule`: scaling type, trigger, target, amount, stacking rule, and
  exception note.
- `resource_event_amount`: Drive or Super Art amount plus unit, event
  context, rate context, and hit/block/parry/burnout labels.
- `juggle_value`: juggle start/increase/limit/count semantics with Capcom and
  community terminology mapped explicitly.
- `spatial_metric_variant`: source-native distance/speed values with
  condition labels and source-native unit boundaries.

Existing `parsed_value` schema kinds to reuse or extend:

- `signed_frame`: reuse for plain signed frame values that already fit the
  approved schema.
- `frame_range`: reuse for plain signed or unsigned frame ranges that already
  fit the approved schema. Note-marked, conditioned, tilde-suffixed, or
  source-specific ranges need an annotated/conditioned wrapper or a separate
  reviewed extension before calculator use.

Potential `raw_preserved` outcomes:

- Descriptive prose or source-native labels that do not affect calculation
  after review.
- Display-only condition text that a later calculator explicitly excludes.
- Source rows whose value should remain quote-only context because no
  deterministic tool will consume the field.

Parser-policy or later source-review outcomes:

- Official malformed-looking active-frame examples such as `30-34.35`,
  `20-24.25`, and `23--33` need explicit parser policy because source review
  already confirmed the raw notation.
- Official note-marked values when the corresponding note text is not yet
  available in a reviewed public artifact.
- SuperCombo bracketed or parenthesized values whose condition labels cannot be
  derived from committed reviewed mechanics summaries.
- Projectile and spatial values where source-native units or measurement
  semantics are insufficient for deterministic use.

## Acceptance Criteria

- The ExecPlan accounts for all `207` `review_required` groups.
- Official authority-candidate groups are listed and prioritized before
  SuperCombo enrichment/cross-reference groups.
- Each major blocker expression family has a future disposition:
  new schema/parser, raw-preserved after review, or later source review.
- SuperCombo remains enrichment/cross-reference only.
- No parser, schema, calculator, retrieval, answer, normalized export, live
  acquisition, or SymPy calculation logic is implemented.
- Validation commands pass.

## Files / Interfaces

This docs-only planning unit changes only:

- `docs/execplans/2026-05-23-review-required-parser-schema-expansion.md`

Future implementation plans may touch, after review and approval:

- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- parser/classifier fixtures and validators
- value-shape coverage artifacts

Those future files are explicitly not changed by this ExecPlan draft.

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Created branch
  `docs/review-required-parser-schema-expansion`.
- [x] (2026-05-23 JST) Analyzed the 207 `review_required` coverage groups.
- [x] (2026-05-23 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-23 JST) Validation passed:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate`,
  and `git status --short --branch`.
- [x] (2026-05-23 JST) Mandatory local review passed:
  `codex review --uncommitted` reported no blocking findings.
- [ ] Domain-review and approve this ExecPlan before any parser/schema
  implementation.
- [ ] Create a separate implementation ExecPlan if schema/parser changes are
  approved.

## Decision Log

- Decision: Keep this unit docs-only.
  Rationale: The next change needs schema and parser design review before any
  runtime or validator surface changes are made.
  Date/Author: 2026-05-23 / Codex

- Decision: Prioritize official authority-candidate blockers before SuperCombo
  blockers.
  Rationale: Official values are the only candidates for future daily-answer
  numeric authority; SuperCombo remains enrichment/cross-reference only.
  Date/Author: 2026-05-23 / Codex

- Decision: Treat expression-shape counts as overlapping diagnostics.
  Rationale: A single raw value can be parenthesized, multihit, bracketed, and
  gauge-related at the same time. Parser design must preserve all semantics
  rather than forcing a lossy single bucket.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep SymPy out of this parser/schema expansion plan.
  Rationale: This work classifies and structures raw values. Exact arithmetic
  belongs to a later calculator ExecPlan after formulas and parsed inputs are
  approved.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- The proposed schema-kind names are planning labels, not approved public
  interfaces.
- Some official note-marked values may require additional public note evidence
  before parsing can be implemented safely.
- SuperCombo examples are useful for parser-shape coverage but remain
  non-authoritative for numeric answers.
- Several groups combine multiple blocker shapes, so implementation should
  avoid one-pass regex parsing that drops condition labels or components.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only ExecPlan | Drafted parser/schema expansion plan for all 207 `review_required` groups | `docs/execplans/2026-05-23-review-required-parser-schema-expansion.md` | `git diff --check`; clean-slate validator; parsed-value classifier validator; `git status --short --branch`; `codex review --uncommitted` | Passed | None | Domain approval pending before implementation | Schema names are planning labels |
| Preserve scope exclusions | No parser/schema/calculator/retrieval/answer/export/live acquisition/SymPy logic added | This ExecPlan only | Diff/status review | Passed | None | Future implementation ExecPlan required | Later work must keep SuperCombo non-authoritative |
