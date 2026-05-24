# Annotated Official Parser-Schema Implementation Slice

Status: Implemented; validation passed; ready for mandatory review.

## Purpose

Plan the smallest implementation slice for official annotated numeric
candidates after PR #342 and PR #344. This is an implementation ExecPlan, but
this PR is docs-only. Parser, schema, classifier, calculator, retrieval,
answer, export, runtime, SymPy, and live acquisition behavior must not be
changed until this plan receives mandatory review and the value double-check
gate is complete.

The central contract remains:

- parse possible is not calculation-safe;
- annotated numeric tokens are condition-bound candidates only;
- nested numeric candidates must never be consumed as ordinary scalar
  calculator, export, retrieval, or answer inputs.

## Inputs

- `docs/execplans/2026-05-24-annotated-official-parser-schema-slice.md`
- `docs/execplans/2026-05-24-annotated-official-parser-schema-slice-amendment.md`
- `docs/source-reviews/20260524-official-note-linkage-source-review.md`
- `data/source-reviews/20260524-official-note-linkage-source-review-summary.json`
- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`
- `contracts/current-facts/current_fact_record.schema.json`
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- `tests/test_parsed_value_classifier.py`
- `tests/validation/validate_parsed_value_classifier.py`
- Issue #343 roadmap and value double-check gate

## Scope

Included for later implementation planning only:

- startup annotated suffix-marker frames;
- explicit negative `block_advantage` annotated frames;
- explicit negative `hit_advantage` annotated frames;
- source-review records whose PR #341 result is
  `structured_row_note_evidence_found` and whose PR #344 amendment status
  remains in the narrowed first implementation slice;
- raw-value-level partial acceptance where the review item contains both
  included and deferred raw variants;
- schema, classifier, fixture, and validator requirements for annotated
  numeric candidates that are not calculation-safe.

Excluded:

- `recovery` / total-duration / `全体` values;
- `recovery` `※NN` values, including `※16`;
- positive unsigned advantage values such as `※1`;
- ambiguous PR #341 groups:
  - `sa_gain`
  - `combo_scaling`
  - `damage`
  - `active`
- non-note active grammar blockers;
- all SuperCombo values;
- parser/schema/classifier/calculator/retrieval/answer/export/runtime
  implementation in this docs-only PR;
- SymPy logic;
- live acquisition for application artifacts;
- calculation-safe promotion;
- numeric authority promotion;
- current-fact authority promotion.

Reviewer-only Scrapling screenshot capture for the value double-check gate is
allowed after this plan is reviewed. It is not a live acquisition artifact
update, must not run in CI, and must not be committed.

## Exact Target Table

| Target | Review item | Field | Source header | Included raw surfaces | Planned parser rule | Planned parsed kind | Calculation status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| startup suffix marker | `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100` | `startup` | `動作フレーム > 発生` | `122※`, `128※` only | `annotated_frame.official_suffix_marker.v1` | `annotated_numeric_candidate` with unsigned frame candidate | `annotated_candidate_not_calculation_safe` |
| block advantage explicit negative prefix marker | `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb` | `block_advantage` | `硬直差 > ガード` | `※-4`, `※-2` only | `annotated_signed_frame.official_prefix_marker.negative.v1` | `annotated_numeric_candidate` with signed frame candidate | `annotated_candidate_not_calculation_safe` |
| hit advantage explicit negative prefix marker | `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69` | `hit_advantage` | `硬直差 > ヒット` | `※-3`, `※-1`, `※-4` only; `※1` is excluded | `annotated_signed_frame.official_prefix_marker.negative.v1` | `annotated_numeric_candidate` with signed frame candidate | `annotated_candidate_not_calculation_safe` |

The implementation must derive the exact raw variants from reviewed source
artifacts and focused fixtures. This table authorizes only the grammar family
and review item IDs, not blanket acceptance of every note-bearing value in the
same field.

After mandatory review, implementation was further narrowed to the exact
Issue #343 double-check-passed raw values listed above. Same-grammar variants
that were not recorded in the double-check gate remain blocked.

## Explicitly Blocked Variants

| Blocked variant or group | Status required in first implementation | Reason |
| --- | --- | --- |
| `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_4b3674d32cef` | `review_required` / blocked | Recovery mixes ordinary recovery-like values with `全体` total-duration semantics. |
| `全体 ※43` and other `全体 ※NN` values | `review_required` / blocked | Requires a total-duration field/schema decision. |
| `※16` and other recovery `※NN` values | `review_required` / blocked | Deferred with the mixed recovery group until split/subset semantics are approved. |
| `※1` and other positive unsigned advantage values | `review_required` / blocked | Requires explicit plus-sign / column-context normalization policy. |
| `124※` in startup | `review_required` / blocked raw variant | Same-grammar variant was not included in the Issue #343 double-check gate. |
| `※-15`, `※-5`, `※-10` in block advantage | `review_required` / blocked raw variants | Same-grammar variants were not included in the Issue #343 double-check gate. |
| `sa_gain`, `combo_scaling`, `damage`, `active` ambiguous groups | `blocked_pending_source_review` | PR #341 marks these ambiguous. |
| `30-34.35`, `20-24.25`, `23--33` | `review_required` / blocked | Non-note active grammar blockers remain outside this parser slice. |
| SuperCombo values | non-authoritative and out of scope | SuperCombo remains enrichment/cross-reference/candidate only. |

## Required Value Double-Check Gate

Before implementation approval, Codex must create a reviewer-only bundle under:

```text
.local/reviewer-evidence/value-double-check/<run-id>/
```

Required bundle contents:

- Scrapling full-page screenshots for the target official frame-data pages;
- focused screenshots for target rows/cells/notes when useful;
- `manifest.json` with counts, file names, source page labels, target review
  item IDs, and raw value length/hash summaries only;
- a target value summary listing character, move identity, source column,
  raw visible value, hidden detail value if present, row-note candidate count,
  note text excerpt, and expected review question;
- `chatgpt-prompt.md` asking ChatGPT/VLM to cross-check whether the
  screenshot shows the same value, source column, note marker attachment,
  row-note linkage, and visible/hidden detail separation as the artifact;
- a zip at:

```text
.local/reviewer-evidence/value-double-check/<run-id>.zip
```

Workflow:

1. Codex creates the local bundle and zip with Scrapling screenshot evidence.
2. A human manually uploads the zip and prompt to ChatGPT.
3. ChatGPT/VLM output is treated only as `observation_candidate`.
4. Any mismatch, uncertainty, unreadable screenshot, row/cell ambiguity, or
   value/header/note disagreement blocks parser/schema implementation and
   returns the item to source review.
5. The implementation PR may record only a short reviewer status summary, not
   the full ChatGPT output.

Forbidden in Git:

- `.local/` artifacts;
- zip files;
- screenshots;
- raw HTML;
- full raw rows;
- local absolute paths;
- cookies, browser profiles, headers, tokens, traces, debug dumps;
- answer logs, training logs, private data;
- full ChatGPT/VLM output.

The double-check gate is reviewer assistance only. It is not source truth,
validator evidence, parser approval, calculation-safe promotion, or authority.

## Schema Placement Decision

Use a new outer `parsed_value.kind` for annotated values:

```text
annotated_numeric_candidate
```

This is required because the existing `parsed_value` scalar kinds, such as
`integer` and `signed_frame`, cannot represent condition-bound note metadata
and would be too easy for future consumers to treat as ordinary numeric facts.

The planned outer object must contain separate sections for:

- numeric candidate:
  - candidate type, such as unsigned frame or signed frame;
  - source-native unit, currently `frame`;
  - parsed integer value;
- annotation:
  - `note_marker`, currently literal `※`;
  - marker placement, such as `suffix` or `prefix`;
  - `note_id`, nullable;
  - `note_text_status`;
  - `note_scope`;
  - row-note candidate count and linkage status from source-review evidence;
- source context:
  - source review ID or review item ID;
  - source column path or a validator-checked reference to the record-level
    source column path;
- calculation gate:
  - `calculation_input_status == "annotated_candidate_not_calculation_safe"`;
  - reason that the value is condition-bound and not scalar calculation input.

`value_shape` should continue to carry classifier status, parser rule ID, and
shape classes. It should not become the storage location for note text or
numeric candidate data. Record-level `source_header_path` and `field_key` remain
the authoritative source column fields; validators must prove they match the
target rule instead of duplicating unchecked values.

If implementation review finds that `parsed_value` cannot safely hold source
review metadata without bloating current facts, the plan must be amended before
coding. The fallback cannot be plain `integer` or plain `signed_frame`.

## Raw-Value-Level Partial Acceptance Decision

The implementation must support raw-value-level partial acceptance before it
parses the hit-advantage review item, because that item includes explicit
negative variants such as `※-3` and deferred positive unsigned variants such as
`※1`.

Required coverage model:

- bump the classifier coverage artifact schema version before adding partial
  coverage fields;
- add closed, validated per-raw-value variant results under the affected
  coverage record;
- store enough public-safe data to identify the variant, such as `raw_value`,
  `raw_value_length`, `raw_value_sha256`, parser rule ID, classifier decision,
  calculation input status, and block reason;
- use a top-level coverage decision that cannot be mistaken for full review
  item coverage when blocked variants remain, such as
  `partial_raw_value_coverage`;
- keep top-level and per-variant counts deterministic and validator-checked;
- render the Markdown coverage so reviewers can see which variants parsed and
  which variants remain blocked.

The raw classifier must still operate per value:

- accepted explicit-negative variants return `parsed` value shape,
  `annotated_numeric_candidate`, and
  `annotated_candidate_not_calculation_safe`;
- deferred variants such as `※1` return `review_required` and no parsed value;
- any value outside the approved target ID, field, source, and grammar remains
  blocked.

If implementation cannot represent partial acceptance without implying that an
entire mixed review item is parsed, the whole mixed hit-advantage item must be
deferred and the ExecPlan amended.

## Calculation Status Decision

Use the closed validated calculation input status:

```text
annotated_candidate_not_calculation_safe
```

This status means:

- the raw value was parsed into a structured annotated candidate;
- the candidate is condition-bound by an official note;
- no scalar calculator may consume it;
- no normalized scalar export may flatten it;
- answer preparation may display the raw annotated value with a caveat only
  after a future answer-specific plan, but may not answer it as an exact
  numeric fact;
- retrieval/numeric tables may index it only as annotated metadata, not an
  exact scalar advantage or startup value.

This status must be closed and validator-enforced. It must not be a free-form
string and must not be treated as equivalent to
`eligible_only_after_domain_source_and_unit_checks`.

## Consumer Guard Decision

The implementation must include tests or validators proving that nested numeric
candidates cannot be used as scalar values.

Required guards:

- scalar consumers must check `parsed_value.kind`, not only the presence of an
  integer field;
- calculators must reject `annotated_numeric_candidate` unless a later
  annotated-condition-aware calculator contract is approved;
- normalized exports must preserve the outer annotated wrapper or omit the
  value; they must not emit the nested candidate as `signed_frame` or
  `integer`;
- retrieval and answer preparation must not index or answer the nested
  candidate as an exact numeric fact;
- official source records remain `authority_candidate` only;
- SuperCombo source records remain non-authoritative and out of scope.

The first implementation PR does not need to implement export, retrieval,
answer, or calculator behavior. It must, however, leave schema and validator
evidence that future consumers cannot mistake the wrapper for scalar data.

## Parser Rule Requirements

Parser rules must be source-, field-, review-item-, and grammar-limited.

Required rules:

- `annotated_frame.official_suffix_marker.v1`
  - source: `official`
  - source role: `authority_candidate`
  - review item:
    `value-shape:official--source_specific_expression--u_fdb49a2113ba--u_a23f1a4e4100`
  - field: `startup`
  - grammar: unsigned integer followed by literal `※`
  - examples: `122※`, `128※`
- `annotated_signed_frame.official_prefix_marker.negative.v1`
  - source: `official`
  - source role: `authority_candidate`
  - review items:
    - `value-shape:official--source_specific_expression--u_c135db53355f--u_522ba9f47afb`
    - `value-shape:official--source_specific_expression--u_c135db53355f--u_7acd6c7b6e69`
  - fields: `block_advantage`, `hit_advantage`
  - grammar: literal `※` followed by explicit negative integer
  - examples: `※-4`, `※-2`, `※-3`

Rules must reject:

- ASCII `*` and any non-`※` marker;
- `※1` and any unsigned positive advantage value;
- recovery `※NN`;
- `全体 ※NN`;
- note IDs or bracketed active forms;
- visible/hidden detail concatenations;
- dot and double-dash active grammar;
- SuperCombo values;
- values with multiple numeric candidates unless a later plan approves the
  grammar and fixtures.

## Fixture Strategy

Positive fixtures:

- startup:
  - `122※` preserves raw value and parses as annotated unsigned frame
    candidate;
  - `128※` preserves raw value and parses as annotated unsigned frame
    candidate;
- block advantage:
  - `※-4` preserves raw value and parses as annotated signed frame candidate;
  - `※-2` preserves raw value and parses as annotated signed frame candidate;
- hit advantage:
  - `※-3` preserves raw value and parses as annotated signed frame candidate;
  - any additional explicit-negative hit examples must be backed by source
    review evidence or synthetic contract fixtures that do not claim source
    occurrence.

Negative fixtures:

- `※1` remains `review_required`;
- recovery `全体 ※43` remains `review_required`;
- recovery `※16` remains `review_required`;
- `※500`, `※3000`, `※即時補正10%`, and active note-bearing representatives
  from ambiguous PR #341 groups remain blocked;
- `30-34.35`, `20-24.25`, and `23--33` remain blocked;
- `122*` and `*122` are not accepted by the `※` rules;
- SuperCombo values with similar surfaces remain blocked or
  non-authoritative;
- no annotated candidate has calculation-safe status;
- no annotated candidate is emitted as plain `integer` or `signed_frame`.

Schema fixtures must include valid and invalid current-fact records for the new
`annotated_numeric_candidate` wrapper. Validator fixtures must include mixed
coverage for the hit-advantage review item so `※-3` and `※1` cannot collapse
into the same status.

## Future Implementation Files

A later implementation PR may touch only files required by this plan, such as:

- `contracts/current-facts/parsed_value.schema.json`
- `contracts/current-facts/value_shape.schema.json`, only if new closed
  classes or parser-status values are required
- `contracts/current-facts/current_fact_record.schema.json`, only if the
  wrapper cannot hold required metadata and review approves record-level fields
- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- `tests/test_parsed_value_classifier.py`
- `tests/validation/validate_parsed_value_classifier.py`
- focused schema fixtures/tests if present or added by the implementation plan
- generated parsed-value classifier coverage JSON/Markdown artifacts if
  classifier output changes
- this ExecPlan

The implementation PR must not touch retrieval, answer behavior, normalized
exports, calculators, live acquisition, SuperCombo parser behavior, or
authority policy.

## Acceptance Criteria

- Value double-check bundle is created under ignored `.local/` using Scrapling
  screenshots before implementation approval.
- ChatGPT/VLM review is completed manually and any mismatch blocks
  implementation.
- Only startup suffix-marker, explicit negative block-advantage, and explicit
  negative hit-advantage official annotated values are implemented.
- Recovery, total-duration, positive unsigned advantage, ambiguous PR #341
  groups, non-note active grammar blockers, and SuperCombo values remain
  blocked or out of scope.
- `raw_value` is preserved exactly.
- Note marker, note ID, row-note candidate evidence, note text status, note
  scope, source column, numeric candidate, and calculation safety are modeled
  separately.
- Annotated candidates use a non-scalar outer parsed-value kind.
- `annotated_candidate_not_calculation_safe` is closed and validator-enforced.
- Raw-value-level partial acceptance is represented without implying whole
  mixed review items are parsed.
- No value becomes calculation-safe, numeric authority, or current-fact
  authority.
- Validation commands pass.

## Validation Commands

Run from repository root:

```bash
git diff --check
uv lock --check
PYTHONPATH=src uv run --locked python tests/validation/validate_official_note_linkage_source_review.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.parsed_value_classifier validate
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-24 JST) PR #344 was marked ready and merged with normal merge
  commit `cece9176103d2eb68176fb4dab9db37db248036b`.
- [x] (2026-05-24 JST) Local `main` was updated to `origin/main` at merge
  commit `cece9176103d2eb68176fb4dab9db37db248036b`.
- [x] (2026-05-24 JST) Confirmed main CI passed for the PR #344 merge commit:
  run `26353656870`.
- [x] (2026-05-24 JST) Created branch
  `plan/annotated-official-parser-schema-implementation`.
- [x] (2026-05-24 JST) Drafted this docs-only implementation ExecPlan.
- [x] (2026-05-24 JST) Validation passed: `git diff --check`,
  new-file whitespace check, `uv lock --check`, official note-linkage
  source-review validator, parsed-value classifier validator, clean-slate
  validator, and `git status --short --branch`.
- [x] (2026-05-24 JST) Completed mandatory review for PR #345 with no
  blocking findings.
- [x] (2026-05-24 JST) PR #345 was marked ready and merged with normal merge
  commit `86d1fdbe37c797f5a256b50f921327e2fda8b86e`.
- [x] (2026-05-24 JST) Local `main` was updated to `origin/main` at merge
  commit `86d1fdbe37c797f5a256b50f921327e2fda8b86e`; main CI passed in run
  `26354404361`.
- [x] (2026-05-24 JST) Completed Issue #343 value double-check gate before
  implementation approval. The reviewer result passed the narrowed included
  targets as `observation_candidate` only; `sa_gain` `※3000` remained
  uncertain and excluded.
- [x] (2026-05-24 JST) Created branch
  `impl/annotated-official-parser-schema`.
- [x] (2026-05-24 JST) Added `parsed_value.kind ==
  "annotated_numeric_candidate"` schema wrapper for note-bound numeric
  candidates.
- [x] (2026-05-24 JST) Added target-limited parser rules for startup suffix
  marker frames and explicit negative annotated advantage frames.
- [x] (2026-05-24 JST) Added closed calculation status
  `annotated_candidate_not_calculation_safe`.
- [x] (2026-05-24 JST) Bumped parsed-value classifier coverage artifact schema
  to v2 and added raw-value-level variant coverage for annotated targets.
- [x] (2026-05-24 JST) Added focused parser, schema compatibility, coverage,
  partial-acceptance, consumer-guard, and exclusion tests/validators.
- [x] (2026-05-24 JST) Updated the official note-linkage source-review
  validator to keep the 9 source-review records fixed while allowing only the
  narrowed implemented annotated coverage states; deferred and ambiguous
  records must remain `review_required`.
- [x] (2026-05-24 JST) Regenerated parsed-value classifier coverage JSON and
  Markdown artifacts.
- [x] (2026-05-24 JST) Fixed mandatory review blocker by choosing the
  narrow-implementation path: only the 7 Issue #343 double-check-passed raw
  values parse, while `124※`, `※-15`, `※-5`, and `※-10` remain
  `review_required`.
- [x] (2026-05-24 JST) Final validation passed: `git diff --check`,
  `git diff --cached --check`, `uv lock --check`, unittest discovery,
  clean-slate validator, official note-linkage source-review validator,
  parsed-value classifier coverage validator, and focused parsed-value
  classifier validator.
- [ ] Complete implementation review.

## Decision Log

- Decision: Use an outer `parsed_value.kind ==
  "annotated_numeric_candidate"` for this slice.
  Rationale: Plain scalar kinds cannot carry note linkage and would be unsafe
  for future consumers.
  Date/Author: 2026-05-24 / Codex

- Decision: Use `annotated_candidate_not_calculation_safe` as the closed
  calculation input status for parsed annotated candidates.
  Rationale: The values are syntactically parsed but condition-bound by note
  text and must not be scalar calculation inputs.
  Date/Author: 2026-05-24 / Codex

- Decision: Require raw-value-level partial acceptance for each annotated
  target review item.
  Rationale: The review items contain both Issue #343 double-check-passed raw
  values and same-grammar or policy-deferred variants that must remain blocked.
  Date/Author: 2026-05-24 / Codex

- Decision: Make the Issue #343 Scrapling screenshot plus ChatGPT/VLM
  double-check gate mandatory before implementation approval.
  Rationale: Value-handling decisions need a reviewer-only visual
  cross-check, while deterministic artifacts remain the implementation
  authority.
  Date/Author: 2026-05-24 / Codex

- Decision: Represent all annotated target groups with top-level
  `partial_raw_value_coverage` and per-raw-value variant statuses.
  Rationale: Only Issue #343 double-check-passed raw values can parse in this
  implementation. `124※`, `※-15`, `※-5`, `※-10`, and `※1` remain blocked
  until they receive their own review gate or policy approval.
  Date/Author: 2026-05-24 / Codex

## Deviations

- None.

## Remaining Risks

- Export, retrieval, answer, and calculator consumers are still not
  implemented; future consumer PRs must reject `annotated_numeric_candidate`
  as scalar input unless a later annotated-condition-aware contract is
  approved.
- The `annotated_numeric_candidate` field shape is now implemented and
  validator-checked, but remains review pending.
- Partial coverage schema v2 is implemented and validator-checked, but remains
  review pending.
- Recovery and total-duration parsing still need a separate plan.
- Positive unsigned advantage parsing still needs a plus-sign /
  column-context policy.
- Same-grammar annotated variants that were not included in the Issue #343
  double-check gate remain blocked pending supplemental double-check or a
  later approved expansion plan.
- `sa_gain` `※3000` remains `uncertain_blocks_implementation` from the
  double-check gate and stays excluded with the other ambiguous PR #341
  groups.

## Completion Review Table

| PLAN item | Planned outcome | Changed files in this docs-only PR | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Annotated official parser/schema implementation planning | Draft docs-only implementation plan narrowed by PR #344 and gated by Issue #343 double-check workflow | `docs/execplans/2026-05-24-annotated-official-parser-schema-implementation.md` | `git diff --check`; new-file whitespace check; `uv lock --check`; official note-linkage source-review validator; parsed-value classifier validator; clean-slate validator; status check | Passed | None | Complete | None |
| Double-check gate | Used Issue #343 reviewer-only Scrapling screenshot bundle and human ChatGPT/VLM observation to gate implementation; included targets passed, `sa_gain` control stayed excluded | No committed bundle files; `.local/reviewer-evidence/value-double-check/20260524T065431Z-annotated-official-parser-schema/` remained ignored | Human review recorded on Issue #343 | Passed for included targets | None | Complete | ChatGPT/VLM remains observation_candidate only |
| Annotated parsed-value schema | Added non-scalar `annotated_numeric_candidate` wrapper with separate numeric candidate, annotation, source context, and calculation gate sections | `contracts/current-facts/parsed_value.schema.json` | Schema compatibility through parsed-value classifier validator and unittest fixtures | Passed | None | Review pending | Future consumers must not treat nested numeric candidate as scalar |
| Annotated parser rules | Added target-limited parser support for startup suffix-marker frames and explicit negative annotated advantage frames | `src/sf6_knowledge_coach/parsed_value_classifier.py`; tests | Unit tests; parsed-value classifier validator | Passed | None | Review pending | Positive unsigned advantage remains blocked |
| Partial raw-value coverage | Bumped coverage artifact schema to v2 and recorded per-raw-value variants so `※1` remains blocked while explicit negatives parse | coverage JSON/Markdown; classifier; validator | parsed-value classifier build/validate; validator tests | Passed | None | Review pending | Partial coverage semantics must remain validator-locked |
| Scope exclusions | Recovery, total-duration, `※16`, `※1`, ambiguous groups, active grammar blockers, SuperCombo, calculators, SymPy, retrieval, answer, export, runtime, live acquisition, and authority promotion remain out of scope | classifier/tests/validator coverage only | Unit tests and validators | Passed | None | Review pending | Deferred groups require separate plans |

## Next Reviewer Prompt

```text
Review the implementation of docs/execplans/2026-05-24-annotated-official-parser-schema-implementation.md.

Check:
- scope is limited to startup suffix-marker frames, explicit negative
  block_advantage annotated frames, and explicit negative hit_advantage
  annotated frames;
- recovery / total_duration / 全体 values, recovery ※NN values, positive
  unsigned advantage values like ※1, ambiguous PR #341 groups, non-note active
  grammar blockers, and SuperCombo values remain excluded;
- annotated candidate schema placement is explicit and non-scalar;
- raw-value-level partial acceptance is required before parsing mixed
  hit_advantage variants;
- coverage and validators must distinguish parsed annotated candidates from
  blocked raw variants;
- calculation status is the closed value
  annotated_candidate_not_calculation_safe;
- nested numeric candidates cannot be consumed as scalar calculator, export,
  retrieval, or answer inputs;
- fixture strategy covers positive and negative cases;
- Issue #343 Scrapling screenshot plus ChatGPT/VLM double-check gate is
  mandatory before implementation approval;
- ChatGPT/VLM output remains observation_candidate only;
- parser/schema/classifier implementation is limited to this approved slice;
- no calculator/retrieval/answer/export/runtime implementation, SymPy logic,
  live acquisition, calculation-safe promotion, numeric authority promotion,
  or current-fact authority promotion is included.

Return blocking findings first, validation results, coverage count changes,
PLAN deviations, remaining risks, and whether implementation is stage-ready.
```
