# Latest Source Value-Shape Inventory

Status: Draft; planning-only ExecPlan.

## Purpose

Plan reviewed value-shape inventory artifacts from the latest source
acquisition outputs created by PR #305.

This unit comes after current-source acquisition and before current-fact JSON
Schema redesign. It exists to inspect the actual latest official and
SuperCombo raw artifacts, summarize the value shapes that appear, and hand
reviewed evidence to later schema and deterministic classifier work.

JSON Schema redesign remains blocked until this inventory is reviewed. This
ExecPlan does not implement schemas, parser/classifier rules, normalized
exports, retrieval changes, answer behavior, or authority promotion.

## Scope

Included:

- Plan value-shape inventory generation from the latest ignored local
  acquisition artifacts, when present:

  ```text
  .local/source-acquisition/current-source-acquisition/20260521T025403Z/
  ```

- Inventory official and SuperCombo separately.
- Use the committed acquisition report as the public run index:

  ```text
  docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
  ```

- Produce public summarized reviewed inventory artifacts, not raw HTML, full
  raw rows, or full source table dumps.
- Preserve source-native labels in the inventory:
  - official Japanese source header paths
  - SuperCombo English headings and labels
- Preserve exact raw example expressions when examples are included.
- Record counts, shape classes, representative examples, affected fields,
  source family, source role, and review items.
- Identify unclassified, rare, malformed-looking, structurally surprising, or
  source-specific expressions as explicit review items.
- Define privacy and source-boundary guard expectations for future inventory
  artifacts.
- Define graceful blocked/review-item behavior when ignored `.local` artifacts
  are missing.

Excluded:

- Do not run live official acquisition by default.
- Do not run live SuperCombo acquisition by default.
- Do not use `solve_cloudflare=True`.
- Do not use web access or source scraping in this unit by default.
- Do not implement current-fact JSON Schema redesign.
- Do not implement parser or classifier semantics.
- Do not implement normalized export.
- Do not infer numeric meaning.
- Do not calculate totals, active-frame counts, damage totals, or parsed
  values.
- Do not promote official captures to `current_fact_authority`.
- Do not promote SuperCombo beyond enrichment, cross-reference, or candidate
  evidence.
- Do not merge official Japanese labels and SuperCombo English labels.
- Do not introduce English canonical field keys in raw inventory artifacts.
- Do not change runtime, retrieval, answer behavior, Discord, VLM, API
  fallback, vector search, private vault, persistent DB, generated DB, or
  `sf6 ask`.
- Do not commit `.local/`, `.venv/`, `.agents/`, screenshots, raw HTML, raw
  rows, cookies, browser profiles, traces, debug dumps, answer logs, training
  logs, or private user data.

## Acceptance Criteria

- The plan identifies the latest source acquisition run ID:
  `20260521T025403Z`.
- The plan uses ignored `.local` artifacts only as local/reviewer input, never
  as public commit content.
- The plan defines public inventory artifact paths for summarized reviewed
  output.
- The plan inventories official and SuperCombo separately.
- The plan preserves source-native labels and exact representative raw
  examples.
- The plan records counts, shape classes, affected fields, source family, and
  review items.
- The plan covers the official special expressions already observed during
  PR #305 review.
- The plan requires a separate SuperCombo value-shape inventory based on
  SuperCombo English headings and labels.
- The plan states that official Japanese source labels and SuperCombo English
  labels must not be merged in this unit.
- The plan keeps English canonical keys deferred to a later normalized schema
  ExecPlan.
- The plan states that no field should be coerced to integer merely because
  most values look numeric.
- The plan keeps unknown or rare source expressions raw-preserved and
  unparsed until deterministic classifier rules are approved.
- The plan does not approve live acquisition, parser/classifier behavior,
  normalized export, retrieval changes, answer behavior, or authority
  promotion.
- Planning validation passes.

## Files / Interfaces

Changed by this planning ExecPlan:

- `docs/execplans/2026-05-23-latest-source-value-shape-inventory.md`

Existing inputs:

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-21-value-shape-inventory.md`
- `docs/execplans/2026-05-21-current-source-acquisition-implementation.md`
- `docs/execplans/2026-05-22-source-acquisition-ci-alignment.md`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`
- Ignored local artifacts under
  `.local/source-acquisition/current-source-acquisition/20260521T025403Z/`,
  when present.

Future implementation may create only reviewed summary artifacts and focused
generation/validation code after review. Preferred future public artifact
paths:

- `docs/value-shape-inventories/20260521T025403Z-latest-source-value-shape-inventory.md`
- `data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json`

Preferred future implementation helpers, if needed:

- `src/sf6_knowledge_coach/value_shape_inventory.py`
- `tests/test_value_shape_inventory.py`
- `tests/validation/validate_value_shape_inventory.py`

Those future files are not created by this planning-only ExecPlan. The future
implementation ExecPlan must approve exact paths before editing.

## Source Inputs

The latest source acquisition report records:

- run ID: `20260521T025403Z`
- official captures: 29 of 29
- official raw rows: 2,286
- official tables: 29
- SuperCombo captures: 29 of 29
- SuperCombo tables: 2,281
- review items: 0
- full raw HTML public commit: `prohibited_without_explicit_review`
- source-boundary review: `pending`

The future inventory implementation should first validate the committed public
report and then check whether the ignored local artifact directory exists.

If `.local/source-acquisition/current-source-acquisition/20260521T025403Z/`
is present:

- use it as local reviewer input;
- validate it with `source_acquisition validate-artifacts` before inventory;
- produce summarized inventory artifacts only.

If the ignored local artifacts are missing:

- do not run live acquisition by default;
- do not fetch official or SuperCombo sources;
- do not use `solve_cloudflare=True`;
- record the implementation as blocked or create an explicit review item that
  says the ignored local artifacts are required.

## Public Artifact Boundary

Allowed public inventory content:

- summarized source family counts;
- per-field shape counts;
- source-native field names and heading paths;
- shape names;
- bounded representative examples;
- raw example expressions copied exactly when included;
- raw example hashes or short source references;
- affected character counts;
- affected row/cell/table counts;
- explicit review items;
- notes that values are inventory-only and not numeric authority.

Forbidden public inventory content:

- raw HTML;
- full raw row dumps;
- full source table dumps;
- complete per-move frame tables;
- cookies;
- request headers with secrets;
- credentials, tokens, or auth headers;
- local absolute paths;
- private vault references;
- real user profile data;
- answer logs;
- training logs;
- browser profiles;
- screenshots;
- traces;
- debug dumps.

The future public JSON artifact must be a summary, not a lossless copy of raw
source artifacts.

## Inventory Model

The inventory should separate these levels:

```yaml
inventory_run:
  run_id: "20260521T025403Z"
  acquisition_report: docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
  inventory_status: reviewed_summary
  source_families:
    - official
    - supercombo
  authority_status: inventory_only_not_authority

field_shape_summary:
  source_family: official | supercombo
  source_role: current_fact_authority_candidate | enrichment_candidate
  source_label: string
  source_header_path: [string]
  character_count: integer
  row_or_cell_count: integer
  shape_counts:
    scalar: integer
    signed_frame: integer
    range: integer
    plus_expression: integer
    note_prefixed: integer
    note_suffixed: integer
    hidden_detail: integer
    categorical: integer
    prose: integer
    blank: integer
    dash_variant: integer
    raw_only: integer
    unclassified: integer
  representative_examples:
    - raw_value: string
      source_family: official | supercombo
      source_label: string
      source_header_path: [string]
      character_slug: string
      example_scope: bounded_representative
  review_items:
    - kind: unclassified_expression | rare_expression | malformed_looking_source_value | missing_artifact | drift_candidate
      source_family: official | supercombo
      source_label: string
      raw_value: string
      affected_count: integer
      review_question: string
```

Rules:

- `source_label` and `source_header_path` remain source-native.
- Official Japanese source labels stay Japanese.
- SuperCombo English source labels stay English.
- English canonical keys are not introduced here.
- `raw_value` examples preserve the exact source expression used in the
  summary.
- The inventory may group examples by exact string or shape class, but must
  not replace exact raw examples with inferred values.
- A value may have multiple shape classes.
- Shape classes are descriptive and do not imply parse safety.

## Official Inventory Requirements

Official inventory must use the official raw artifact fields from PR #305,
including:

- `source_column_header_path`
- `source_column_leaf_header`
- `visible_text`
- `source_text`
- `source_text_stripped`
- `hidden_detail_text`
- row-level group headings and input image metadata when needed for review.

Official special expressions already observed must be included in the
downstream handoff:

- `動作フレーム > 発生`:
  - blank values;
  - note-suffixed values such as `122※`;
  - plus expressions such as `6+0`.
- `動作フレーム > 持続`:
  - ranges;
  - hidden-detail multihit values;
  - until-landing text such as `着地まで`;
  - unusual or malformed-looking source ranges such as `20-24.25` and
    `23--33`;
  - note-bearing ranges.
- `動作フレーム > 硬直`:
  - landing recovery expressions such as `着地後N`;
  - compound landing expressions such as `N+着地後M`;
  - note-prefixed or note-suffixed integers such as `※11`;
  - compound note values.
- `硬直差 > ヒット` and `硬直差 > ガード`:
  - `D`;
  - blanks;
  - dash variants such as `-`, `―`, and `ー`;
  - signed integers;
  - ranges such as `0～11`;
  - note-prefixed signed values such as `※-10`;
  - alternate or note-separated values such as `-60※-93`.
- `キャンセル`:
  - categorical values such as `C`, `SA`, `SA2`, and `SA3`;
  - note variants such as `※SA2`;
  - not numeric.
- `ダメージ`:
  - note-prefixed values such as `※500`;
  - alternate or note-separated values such as `2200※1850`.
- `コンボ補正値`:
  - Japanese correction expressions such as `始動補正20%`;
  - immediate correction expressions such as `即時補正10%`;
  - multiple concatenated correction terms;
  - ASCII and full-width percent signs.
- Gauge fields:
  - mostly numeric values;
  - blanks;
  - note-prefixed values.
- `属性` and `備考`:
  - category, prose, and free text;
  - not numeric authority.

No official field may be coerced to an integer merely because most values in
that field are numeric-looking.

## SuperCombo Inventory Requirements

SuperCombo must have a separate value-shape inventory from official.

The SuperCombo inventory must use SuperCombo raw artifact fields, including:

- `heading_chain`;
- `table_index`;
- `row_index`;
- `cell_index`;
- source-native table headings and labels;
- exact cell text from `supercombo_tables.raw.json`.

Requirements:

- Keep SuperCombo source labels and headings in English/source-native form.
- Do not map SuperCombo fields to official Japanese labels in this unit.
- Do not reconcile SuperCombo values with official values in this unit.
- Do not promote SuperCombo to daily-answer numeric authority.
- Record SuperCombo-specific shape classes and review items separately.
- Treat SuperCombo as enrichment, cross-reference, or candidate evidence only.

SuperCombo visual review from PR #305 is reviewer evidence only. It does not
make SuperCombo deterministic authority and does not replace inventory from
the ignored raw artifacts.

## Shape Vocabulary

The future implementation should include at least these top-level shape
classes, and may add source-specific subtypes after review:

- `scalar`
- `signed_frame`
- `range`
- `plus_expression`
- `note_prefixed`
- `note_suffixed`
- `note_separated_alternate`
- `hidden_detail`
- `multihit`
- `conditional`
- `landing_expression`
- `until_landing`
- `categorical`
- `prose`
- `blank`
- `dash_variant`
- `percent_expression`
- `raw_only`
- `unclassified`

The inventory should distinguish shape observation from semantic
interpretation. For example:

- `6+0` is a `plus_expression`; this unit does not decide what it means.
- `D` is a source expression; this unit does not convert it to a number.
- `0～11` is a range-like expression; this unit does not infer a single value.
- `2200※1850` is an alternate or note-separated expression; this unit does
  not choose one value.

## Validation Strategy

Future implementation validation should include:

- public inventory artifact guard:
  - reject local absolute paths;
  - reject `.local/`, `.venv/`, `.agents/`, `/tmp`, browser profile, cookie,
    trace, screenshot, answer log, training log, private vault, and secret
    references;
  - reject raw HTML;
  - reject full raw row dumps;
  - reject full source table dumps;
  - reject complete per-move frame tables.
- source-boundary guard:
  - ensure public artifacts are summaries only;
  - ensure representative examples are bounded;
  - ensure no artifact claims `current_fact_authority`.
- coverage validation:
  - official source family represented or explicitly blocked;
  - SuperCombo source family represented or explicitly blocked;
  - every captured roster character represented or explicitly recorded as a
    review item;
  - every observed source label/header path summarized or explicitly recorded
    as excluded with a reason.
- reproducibility validation:
  - if `.local` artifacts are present, inventory generation is reproducible
    from them;
  - if `.local` artifacts are missing, implementation blocks or emits an
    explicit review item instead of fetching live sources.
- authority validation:
  - official remains authority candidate only;
  - SuperCombo remains enrichment/cross-reference/candidate only;
  - no parsed numeric values are emitted.

Planned local validation for future implementation may include:

```bash
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.value_shape_inventory build --run-id 20260521T025403Z
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_inventory.py
```

Those commands are illustrative for future implementation planning. They are
not implemented by this docs-only ExecPlan.

## Validation Commands

Run from the repository root for this planning-only step:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Started from updated `main` at
  `988d776c81ede22fe1a5780c195e334067c3b01a`.
- [x] (2026-05-23 JST) Created branch
  `plan/latest-source-value-shape-inventory`.
- [x] (2026-05-23 JST) Reviewed Phase 1 roadmap, prior value-shape planning,
  current-source acquisition implementation notes, CI alignment, acquisition
  report, and local ignored artifact availability.
- [x] (2026-05-23 JST) Drafted this docs-only ExecPlan.
- [x] (2026-05-23 JST) Ran planning validation:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Use the PR #305 acquisition run `20260521T025403Z` as the first
  latest-source inventory target.
  Rationale: It is the reviewed current-source acquisition output with 29 of
  29 official captures and 29 of 29 SuperCombo captures.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep official and SuperCombo inventories separate.
  Rationale: Official Japanese source labels and SuperCombo English headings
  are not yet mapped. Merging them before value-shape review would smuggle in
  schema and canonical-key decisions.
  Date/Author: 2026-05-23 / Codex

- Decision: Publish only summarized reviewed inventory artifacts.
  Rationale: Raw HTML, full raw rows, and full source table dumps are outside
  the public artifact boundary. The inventory needs enough examples for schema
  design without becoming a source dump.
  Date/Author: 2026-05-23 / Codex

- Decision: Do not run live acquisition in this unit by default.
  Rationale: Current source artifacts already exist locally from PR #305. If
  they are missing, the correct behavior is a blocker or review item, not
  implicit web acquisition.
  Date/Author: 2026-05-23 / Codex

- Decision: Defer English canonical keys to normalized schema design.
  Rationale: Raw and inventory layers must preserve source-native labels.
  Canonical field keys require explicit mapping design after inventory review.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- Exact future implementation file list for generator and validator.
- Exact JSON summary schema for the public inventory artifact.
- Maximum number of representative examples per source family, field, and
  shape class.
- Whether a Markdown-only inventory is enough for first review, or whether the
  first implementation should include both Markdown and JSON summary.
- How to represent SuperCombo heading/table variations without turning the
  artifact into a full source dump.

## Deviations

- None.

## Risks

- If ignored `.local` artifacts are missing on a future machine, the
  implementation must block or emit review items instead of fetching live
  sources.
- Overly large representative-example sets could become de facto source table
  dumps. The future implementation must keep examples bounded.
- Shape classification can drift into semantic parsing. This unit must remain
  descriptive and inventory-only.
- Official and SuperCombo label mapping is intentionally deferred. Later
  schema work must not skip the mapping review.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan latest-source value-shape inventory | Drafted this ExecPlan only | `docs/execplans/2026-05-23-latest-source-value-shape-inventory.md` | `git diff --check` | Pass | None | Implementation not started | Exact artifact schema deferred |
| Preserve source boundaries | Planned summarized artifacts only; raw HTML/full rows/source dumps forbidden | `docs/execplans/2026-05-23-latest-source-value-shape-inventory.md` | `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py` | Pass | None | Implementation not started | Representative examples must remain bounded |
| Keep authority unchanged | Planned no parser/schema/retrieval/answer changes and no authority promotion | `docs/execplans/2026-05-23-latest-source-value-shape-inventory.md` | Reviewer check | Pending | None | Implementation not started | None |
