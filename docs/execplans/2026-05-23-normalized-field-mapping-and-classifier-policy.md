# Normalized Field Mapping And Classifier Policy

Status: Drafted for review.

## Purpose

Plan the normalized field mapping and deterministic value-shape classifier
policy that must be reviewed before current-fact JSON Schema redesign.

This ExecPlan is intentionally docs-only. It does not implement schemas,
parsers, classifiers, normalized exports, retrieval changes, answer behavior,
or authority promotion.

The immediate goal is to define the boundary between:

- source-native raw/inventory labels;
- future English canonical field keys;
- deterministic value-shape classification;
- authority status for official and SuperCombo sources.

JSON Schema redesign remains blocked until this ExecPlan is reviewed and
approved.

## Scope

Included:

- Define mapping design from official Japanese source headers to future English
  canonical field keys.
- Define mapping design from SuperCombo English labels/headings to future
  English canonical field keys.
- Define separation of these future fields:
  - `field_key`
  - `source_label`
  - `source_header_path`
  - `source_family`
  - `source_name`
  - `source_role`
  - `display_label_ja`
  - `raw_value`
  - `parsed_value`
  - `value_shape`
  - `authority_status`
- Define deterministic classifier policy for known value shapes observed in
  the latest source inventory.
- Define how unclassified and source-specific expressions block JSON Schema
  redesign or become explicit review items.
- Preserve official and SuperCombo authority boundaries.

Excluded:

- Do not implement JSON Schema redesign.
- Do not implement parser or classifier code.
- Do not implement normalized export.
- Do not change retrieval or answer behavior.
- Do not change runtime behavior.
- Do not add dependencies.
- Do not run live official or SuperCombo acquisition.
- Do not use `solve_cloudflare=True`.
- Do not promote any numeric authority.
- Do not merge official and SuperCombo data into current facts.
- Do not commit `.local/`, `.venv/`, `.agents/`, raw HTML, raw rows,
  screenshots, cookies, profiles, traces, debug dumps, answer logs, training
  logs, private data, or ignored local artifacts.

## Acceptance Criteria

- The plan defines the future field separation for normalized current facts.
- The plan gives an initial official Japanese header to English canonical key
  mapping.
- The plan gives a SuperCombo English label to English canonical key mapping
  strategy.
- The plan keeps raw source labels source-native.
- The plan keeps official as authority candidate only.
- The plan keeps SuperCombo as enrichment, cross-reference, or candidate only.
- The plan defines deterministic classifier policy by value shape.
- The plan defines blockers for unclassified or source-specific expressions.
- The plan states that JSON Schema redesign remains blocked until review.
- No runtime/schema/parser/retrieval/answer/data implementation is changed.
- Planning validation passes.

## Files / Interfaces

Created in this step:

- `docs/execplans/2026-05-23-normalized-field-mapping-and-classifier-policy.md`

Reference inputs:

- `docs/PLAN.md`
- `AGENTS.md`
- `docs/execplans/2026-05-23-latest-source-value-shape-inventory.md`
- `docs/value-shape-inventories/20260521T025403Z-latest-source-value-shape-inventory.md`
- `data/value-shape-inventories/20260521T025403Z-latest-source-value-shape-summary.json`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`

No source code, schema, parser, retrieval, answer, CI, runtime, or data
artifact files are changed by this docs-only ExecPlan.

## Source Inputs

The latest reviewed inventory run is:

```text
20260521T025403Z
```

Relevant inventory facts:

- official field summaries: 15
- official observations: 34,290
- official review item groups: 16
- SuperCombo field summaries: 403
- SuperCombo observations: 78,501
- SuperCombo review item groups: 231
- total review item groups: 247
- omitted review item groups: 0
- long examples are public excerpts only, with hash and length metadata.

These facts mean schema redesign must not start from assumptions about simple
integers. The source data already includes blanks, note-bearing values, ranges,
categorical values, prose, hidden details, and unclassified expressions.

## Layer Boundary

### Raw Acquisition Artifacts

Raw acquisition artifacts are source-fidelity records.

Rules:

- preserve source-native labels;
- preserve source-native values;
- do not translate labels;
- do not infer canonical keys;
- do not coerce numeric-looking values;
- do not promote authority.

Official raw labels remain Japanese, such as:

```text
動作フレーム > 発生
硬直差 > ガード
Dゲージ減少 > パニッシュカウンター
```

SuperCombo raw labels remain source-native English, such as:

```text
Command Normals > Startup
Command Normals > Block Advantage
Character Vitals > HP
```

### Value-Shape Inventory

The value-shape inventory is a reviewed summary of observed value forms.

Rules:

- preserve source-native labels;
- group and count value shapes;
- keep representative examples bounded;
- record review items;
- do not emit parsed values;
- do not define final schema.

### Future Normalized Current-Fact Layer

The future normalized current-fact layer may introduce English canonical keys,
but only after mapping and classifier policy are approved.

Future records should separate:

```yaml
normalized_fact:
  field_key: block_advantage
  source_label: ガード
  source_header_path: ["硬直差", "ガード"]
  source_family: advantage
  source_name: official
  source_role: authority_candidate
  display_label_ja: ガード硬直差
  raw_value: "-4"
  parsed_value:
    kind: signed_frame
    value: -4
    unit: frame
  value_shape:
    classes: ["signed_frame"]
    classifier_status: parsed
  authority_status: authority_candidate
```

This example is illustrative only. This ExecPlan does not approve the final
JSON Schema.

## Field Separation Policy

The future normalized layer must keep these concerns separate.

| Field | Meaning | Rule |
| --- | --- | --- |
| `field_key` | English canonical internal key | introduced only in normalized layer |
| `source_label` | source-native leaf label | copied from source, not translated |
| `source_header_path` | source-native path | copied from source, not normalized |
| `source_family` | semantic category | examples: `timing`, `advantage`, `damage`, `gauge`, `cancel`, `attribute`, `note`, `vital`, `mobility` |
| `source_name` | origin source | examples: `official`, `supercombo` |
| `source_role` | evidence role | examples: `authority_candidate`, `enrichment_candidate`, `cross_reference_candidate` |
| `display_label_ja` | Japanese display label | answer/display concern, not source identity |
| `raw_value` | exact source value | always preserved when a normalized fact exists |
| `parsed_value` | deterministic parse result | absent unless classifier rules approve it |
| `value_shape` | observed shape metadata | descriptive and deterministic |
| `authority_status` | answer authority boundary | never promoted by this ExecPlan |

`source_family` must not be used for `official` or `supercombo`. Those belong
in `source_name` or `source_role`.

## Official Mapping Seed

The official source has 15 reviewed source header paths in the latest
inventory. The following mapping seed is for review. It is not yet schema
implementation.

| Official source header path | Proposed `field_key` | Proposed `source_family` | `display_label_ja` |
| --- | --- | --- | --- |
| `技名` | `move_name` | `identity` | 技名 |
| `動作フレーム > 発生` | `startup` | `timing` | 発生 |
| `動作フレーム > 持続` | `active` | `timing` | 持続 |
| `動作フレーム > 硬直` | `recovery` | `timing` | 硬直 |
| `硬直差 > ヒット` | `hit_advantage` | `advantage` | ヒット硬直差 |
| `硬直差 > ガード` | `block_advantage` | `advantage` | ガード硬直差 |
| `キャンセル` | `cancel` | `cancel` | キャンセル |
| `ダメージ` | `damage` | `damage` | ダメージ |
| `コンボ補正値` | `combo_scaling` | `scaling` | コンボ補正値 |
| `Dゲージ増加 > ヒット` | `drive_gain_on_hit` | `gauge` | Dゲージ増加 ヒット |
| `Dゲージ減少 > ガード` | `drive_loss_on_block` | `gauge` | Dゲージ減少 ガード |
| `Dゲージ減少 > パニッシュカウンター` | `drive_loss_on_punish_counter` | `gauge` | Dゲージ減少 パニッシュカウンター |
| `SAゲージ増加` | `sa_gain` | `gauge` | SAゲージ増加 |
| `属性` | `attribute` | `attribute` | 属性 |
| `備考` | `remarks` | `note` | 備考 |

Official mapping rules:

- official source labels stay in `source_label` and `source_header_path`;
- English canonical keys are additional normalized-layer fields;
- every official source header path must map to exactly one canonical
  `field_key` or become an explicit review item;
- if official columns are added, removed, renamed, or reordered, mapping work
  must hard fail or create a human review item;
- official records remain `authority_candidate` until deterministic schema,
  parser, validator, and review gates are approved.

## SuperCombo Mapping Strategy

SuperCombo has 403 reviewed field summaries in the latest inventory. It must
not be mapped wholesale by string similarity.

SuperCombo mapping should be reviewed in groups:

1. Character vitals and mobility
   - examples: `Character Vitals > HP`, `Forward Walk Speed`, `Jump Speed`;
   - likely future families: `vital`, `mobility`;
   - likely role: enrichment/cross-reference candidate.

2. Frame timing fields
   - examples: `Startup`, `Active`, `Recovery`, `Total`, `Blockstun`,
     `Hitstun`, `Hitstop`;
   - likely future families: `timing`, `advantage`;
   - mapping must account for SuperCombo-specific meanings and units.

3. Advantage fields
   - examples: `Block Advantage`, `Hit Advantage`, `After DR Blk`,
     `After DR Hit`, `DR Cancel Blk`, `DR Cancel Hit`;
   - these must not automatically overwrite official values.

4. Damage and scaling fields
   - examples: `Damage`, `Chip Dmg`, `Dmg Scaling`;
   - SuperCombo remains candidate/enrichment unless later cross-source rules
     approve otherwise.

5. Gauge and drive fields
   - examples: `Drive Gain`, `DriveDmg Blk`, `DriveDmg Hit [PC]`;
   - mapping to official gauge fields requires explicit source-role review.

6. Cancel, guard, armor, invulnerability, airborne, projectile, and throw
   metadata
   - examples: `Cancel`, `Guard`, `Armor`, `Invuln`, `Airborne`;
   - usually categorical or note-like, not simple numeric facts.

SuperCombo mapping rules:

- keep SuperCombo `source_name: supercombo`;
- keep SuperCombo `source_role: enrichment_candidate` or
  `cross_reference_candidate`;
- never set SuperCombo to daily-answer numeric authority in this ExecPlan;
- map only reviewed source labels/headings;
- keep official Japanese labels and SuperCombo English labels separate until
  explicit mapping review approves a relationship;
- if a SuperCombo field has no approved canonical mapping, keep it as a
  review item rather than guessing.

## Deterministic Classifier Policy

The deterministic classifier must be conservative. It should classify only
what is structurally understood and should preserve raw values for every
record.

Classifier output should distinguish:

```yaml
value_shape:
  classes: ["signed_frame"]
  classifier_status: parsed | raw_preserved | review_required | rejected
  parser_rule_id: optional string
  review_item_id: optional string
```

`parsed_value` may be emitted only when:

- the source field mapping is approved;
- the value shape has an approved deterministic rule;
- the source role allows that value to be used for the target purpose;
- the parse result preserves enough source context to audit it;
- tests cover representative source examples and review-item regressions.

If any condition is false, keep `parsed_value` absent and set
`classifier_status` to `raw_preserved` or `review_required`.

## Shape Policy

The latest inventory uses these shape classes:

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

Initial policy by class:

| Shape | Policy before parser implementation |
| --- | --- |
| `scalar` | parse only after field mapping and unit are approved |
| `signed_frame` | parse only for approved frame/advantage fields |
| `range` | review required unless the field explicitly supports range output |
| `plus_expression` | review required; do not reduce to a single number |
| `note_prefixed` | review required; preserve note marker |
| `note_suffixed` | review required; preserve note marker |
| `note_separated_alternate` | review required; do not choose one side |
| `hidden_detail` | review required; visible and hidden/source detail must remain auditable |
| `multihit` | review required; do not sum or flatten |
| `conditional` | raw preserved unless a field-specific condition model is approved |
| `landing_expression` | review required; do not coerce to recovery integer |
| `until_landing` | review required; not numeric |
| `categorical` | parse only into approved enum values |
| `prose` | raw preserved; no numeric authority |
| `blank` | explicit blank/missing source value, not zero |
| `dash_variant` | explicit source dash/none marker, not zero |
| `percent_expression` | parse only after scaling semantics are approved |
| `raw_only` | raw preserved; review required before interpretation |
| `unclassified` | blocks parser/schema promotion until classified or explicitly scoped out |

No field should be coerced to an integer merely because most examples in that
field look numeric.

## Review Item Policy

The latest inventory emits 247 grouped review items:

- official: 16
- SuperCombo: 231
- omitted: 0

Policy:

- all review item groups must be carried into mapping/classifier review;
- unclassified expressions block parser implementation for their affected
  field unless explicitly scoped out;
- source-specific expressions require a deterministic interpretation rule or
  must remain raw-preserved;
- malformed-looking expressions require source review before any parse rule;
- rare values must not be silently dropped;
- review decisions must identify:
  - source family;
  - source name;
  - source header path;
  - affected field key if known;
  - shape class;
  - affected count;
  - whether schema design is blocked.

JSON Schema redesign may proceed only when the reviewer accepts one of these
outcomes for every review item group:

- parse rule required before schema;
- schema field supports raw-only values;
- source-specific enum/category required;
- out of scope for the first normalized export;
- blocked pending source review.

## Authority Policy

Official:

- `source_name: official`
- future default `source_role: authority_candidate`
- may become current-fact authority only after deterministic acquisition,
  schema validation, parser validation, and human review.

SuperCombo:

- `source_name: supercombo`
- future default `source_role: enrichment_candidate` or
  `cross_reference_candidate`
- must not become daily-answer numeric authority in this ExecPlan;
- must not override official current values;
- may help identify drift, missing context, or candidate cross-reference
  issues.

Manual review, prose, FTS, LLM memory, screenshots, and reviewer-only browser
observation are not numeric authority.

## JSON Schema Redesign Gate

Current-fact JSON Schema redesign remains blocked until:

- this mapping/classifier policy is reviewed and approved;
- official field-key mapping is approved or unresolved fields are explicit
  review items;
- SuperCombo mapping strategy is approved or unresolved fields are explicit
  review items;
- all 247 review item groups have a reviewed disposition;
- classifier status vocabulary is accepted;
- authority boundary fields are accepted;
- future schema implementation scope is split into a smaller ExecPlan.

This ExecPlan does not itself unblock schema implementation. It only defines
the policy that must be reviewed first.

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Confirmed `main` and `origin/main` are at
  `1623fe1b6159ff64125a59b16d3602fa34493d63`.
- [x] (2026-05-23 JST) Created branch
  `plan/normalized-field-mapping-and-classifier-policy`.
- [x] (2026-05-23 JST) Reviewed `AGENTS.md`, `docs/PLAN.md`, and latest
  value-shape inventory outputs.
- [x] (2026-05-23 JST) Drafted docs-only mapping and classifier policy
  ExecPlan.
- [x] (2026-05-23 JST) Completed planning validation:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Keep source-native labels in raw and inventory layers, and add
  English canonical keys only in the future normalized layer.
  Rationale: Source fidelity and internal schema ergonomics are separate
  concerns.
  Date/Author: 2026-05-23 / Codex

- Decision: Treat `source_family` as a semantic category, not the source
  origin.
  Rationale: `official` and `supercombo` belong in `source_name` or
  `source_role`; semantic categories are needed for mapping and classifier
  work.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep SuperCombo enrichment/cross-reference/candidate only.
  Rationale: SuperCombo is useful for comparison and context, but the project
  authority model does not allow it to become daily-answer numeric authority
  here.
  Date/Author: 2026-05-23 / Codex

- Decision: Treat unclassified and source-specific expressions as schema
  blockers unless reviewed into an explicit raw-only or scoped-out path.
  Rationale: Silent coercion would make deterministic numeric answers
  unreliable.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- Exact English canonical key names for all SuperCombo labels.
- Whether selected SuperCombo labels should map to the same `field_key` as
  official fields or remain source-specific fields.
- Exact enum values for categorical fields such as cancel, guard, armor,
  airborne, and attribute.
- Whether range-like values become structured ranges or raw-preserved strings
  in the first normalized schema.
- How note markers such as `※` should be represented in parsed output.
- Whether hidden detail values require a separate `visible_value` /
  `source_detail_value` schema.
- Which review item groups are first-release blockers versus deferred
  raw-only support.

## Deviations

- None.

## Risks

- Mapping too many SuperCombo labels at once may smuggle in schema decisions.
- Treating shape classification as parsing could accidentally promote
  unreviewed values.
- Choosing English canonical keys too early may hide official Japanese label
  nuance.
- Deferring all review items would leave schema redesign under-specified.
- Public inventory examples are bounded summaries; full context remains in
  ignored local artifacts and reviewed acquisition outputs.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Docs-only mapping/classifier policy | Drafted ExecPlan for review | `docs/execplans/2026-05-23-normalized-field-mapping-and-classifier-policy.md` | `git diff --check` | Pass | None | Mandatory review pending | SuperCombo mapping remains broad |
| Preserve authority boundary | Official stays candidate; SuperCombo stays enrichment/cross-reference/candidate | ExecPlan only | reviewer check | Pending | None | Schema implementation not started | None |
| Keep JSON Schema blocked | Explicit gate remains before schema redesign | ExecPlan only | reviewer check | Pending | None | Mapping/classifier decisions unresolved | Schema work must wait |
