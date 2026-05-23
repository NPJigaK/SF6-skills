# Deterministic Parsed-Value Classifier Implementation

Status: Drafted for review.

## Purpose

Plan the implementation that turns reviewed raw value shapes into explicit
`parsed_value` results or explicit non-parsed statuses.

This is the next required gate before any frame math, punish calculation,
damage/scaling calculation, combo damage calculation, or answer-runtime use of
normalized current-fact records.

## Current State

The value-shape disposition artifact currently has:

- `247` total review item groups;
- `208` `parse_rule_required_before_schema` groups;
- `16` `source_specific_enum_required` groups;
- `6` `schema_supports_raw_only` groups;
- `17` `out_of_scope_first_normalized_export` groups;
- `0` `blocked_pending_source_review` groups.

The `224` schema-design blockers are the `208` parse-rule groups plus the
`16` enum groups. They are not unresolved source-review blockers anymore, but
they are not safe calculation inputs until deterministic parsing or enum
classification is implemented and reviewed.

The parser/classifier implementation must also consume the reviewed
SuperCombo system mechanics source summary:

```text
docs/system-mechanics/20260523-supercombo-system-mechanics-parser-inputs.md
```

That source summary records frame, scaling, gauge, cancel, guard, juggle,
movement, and image-evidence semantics from the SuperCombo system pages. It is
required because shape names alone do not define whether values such as `X(Y)`,
`X(n)Y`, `X,Y`, `X*Y`, `KD`, Drive units, scaling notes, or cancel tokens are
safe for calculation.

## Scope

Included:

- Implement a deterministic parser/classifier for approved raw value shapes.
- Classify every reviewed disposition group as one of:
  - parsed numeric/structured value;
  - enum token set;
  - raw-preserved non-calculation text;
  - review-required/unparsed;
  - out-of-scope first normalized export.
- Add parser fixtures and tests for official and SuperCombo examples.
- Add a validator that compares parser coverage against:
  - `data/value-shape-dispositions/20260521T025403Z-value-shape-review-item-disposition-summary.json`
  - `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-and-enum-policy.json`
  - `contracts/current-facts/*.schema.json`
- Update validator/test evidence audit.

Excluded:

- No normalized export generation.
- No frame/punish/damage/combo calculation tool.
- No retrieval DB changes.
- No answer behavior changes.
- No official authority promotion.
- No SuperCombo numeric authority promotion.
- No live source acquisition.
- No LLM interpretation of raw values as authority.

## Calculation Safety Rule

Until this classifier is implemented and reviewed:

- exact current-fact lookup may continue to return raw official values from
  existing deterministic sources;
- arithmetic calculation must not consume unparsed raw values;
- raw strings and prose must not be silently treated as numbers;
- SuperCombo values remain enrichment/cross-reference/candidate only;
- LLMs may receive raw text only as quoted context, not as a reason to
  calculate or infer frame/damage facts.

After implementation, a calculation tool may consume only records where:

- `value_shape.classifier_status == "parsed"`;
- `parsed_value.kind` and `unit` match the calculation domain;
- `source_name/source_role/authority_status` allow that use;
- parser tests cover the source expression class.

Everything else must remain raw-preserved, review-required, or out-of-scope.

## Required Parser Domains

The implementation must cover the approved policy counts:

| Semantic family | Required parse-rule groups |
| --- | ---: |
| `advantage` | 50 |
| `damage` | 18 |
| `gauge` | 44 |
| `metadata` | 21 |
| `mobility` | 7 |
| `projectile` | 3 |
| `scaling` | 1 |
| `throw` | 1 |
| `timing` | 63 |

And enum groups:

| Semantic family | Required enum groups |
| --- | ---: |
| `attribute` | 1 |
| `cancel` | 6 |
| `defense` | 9 |

The implementation may initially keep some records `review_required` if and
only if the output artifact records why they are not calculation-safe and a
later ExecPlan owns the missing semantics.

## Text And Prose Handling

Text values are not second-class. They must be handled deliberately:

- if the text affects calculation, it must receive a deterministic enum,
  modifier, condition, or parser rule before calculation use;
- if the text is descriptive only, it must be `raw_preserved` and excluded
  from calculation;
- if the text might affect calculation but the meaning is not fully reviewed,
  it must be `review_required`;
- LLM-facing data may include `raw_value`, `display_label_ja`,
  `source_label`, `source_header_path`, `classifier_status`, and a concise
  policy note, but must not ask the LLM to invent numeric semantics.

## Update And Drift Handling

Future game/source updates must use the existing acquisition drift policy:

- numeric changes are allowed only if the source structure and parser shape
  remain compatible;
- new notes/special expressions must be raw-preserved first, then classified
  through value-shape inventory and parser policy updates;
- structural drift, column drift, row/cell mapping drift, missing expected
  tables, extra unexpected tables, or new unclassified expressions must hard
  fail or become explicit human review items;
- no silent skip, partial success hiding, or validator weakening to fit new
  output.

## Proposed Files / Interfaces

Likely implementation files:

- `src/sf6_knowledge_coach/parsed_value_classifier.py`
- `tests/test_parsed_value_classifier.py`
- `tests/validation/validate_parsed_value_classifier.py`
- `data/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.json`
- `docs/value-shape-policies/20260521T025403Z-parsed-value-classifier-coverage.md`
- updates to `data/validator-audits/20260523-validator-test-fact-source-audit.json`
- updates to `docs/validator-audits/20260523-validator-test-fact-source-audit.md`
- updates to this ExecPlan

Do not write normalized current-fact exports in this unit.

## Acceptance Criteria

- Parser/classifier output validates against current-fact schemas.
- Every parse-rule and enum disposition group is covered by a parser/enum
  policy decision.
- Parser/classifier policy is checked against
  `docs/system-mechanics/20260523-supercombo-system-mechanics-parser-inputs.md`.
- Every unsupported calculation-relevant value remains `review_required`, not
  guessed.
- Raw-only prose remains explicit and excluded from calculation.
- SuperCombo is never promoted to numeric authority.
- Validator audit is updated for the new validator.
- No retrieval, answer, or calculation tool consumes the output yet.

## Validation Commands

Run from repository root:

```bash
git diff --check
git diff --cached --check
uv lock --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
for script in tests/validation/validate_*.py; do PYTHONPATH=src uv run --locked python "$script"; done
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Created branch
  `plan/deterministic-parsed-value-classifier-implementation`.
- [x] (2026-05-23 JST) Confirmed current disposition and parser/enum policy
  counts from local artifacts.
- [x] (2026-05-23 JST) Drafted this planning ExecPlan.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Treat the 224 parser/enum groups as calculation blockers until
  deterministic classifier output is implemented and reviewed.
  Rationale: These values include timing, advantage, damage, gauge, metadata,
  mobility, projectile, scaling, throw, attribute, cancel, and defense
  semantics. Using them in arithmetic before parsing would violate PLAN
  numeric rules.
  Date/Author: 2026-05-23 / Codex

- Decision: Do not add calculation tools in the same PR as parser/classifier.
  Rationale: Calculators need their own domain contracts after parsed values
  exist.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- Some source expressions may remain review-required after first classifier
  implementation; those must block affected calculations.
- Parser tests can overfit if they are written from generated output instead
  of reviewed source examples and policy artifacts.
- Future source updates may add expressions that require new inventory and
  parser policy review.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan parser/classifier | Defined calculation-safe parser boundary | This ExecPlan | reviewer check | Pending | None | Implementation not started | Must not overclaim parse semantics |
| Preserve calculation safety | Block arithmetic on raw/unparsed values | This ExecPlan | reviewer check | Pending | None | Calculation tools not implemented | Future tools must enforce parsed-only inputs |
| Preserve update safety | Reused drift policy for future updates | This ExecPlan | reviewer check | Pending | None | Drift automation not implemented | New source expressions must hard fail or review |
