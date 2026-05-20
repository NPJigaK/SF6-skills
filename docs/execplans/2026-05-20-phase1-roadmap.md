# Phase 1 Roadmap

Status: Finalized as planning roadmap; retrieval implementation remains paused.

## Purpose

Break Phase 1 into separately reviewable units so each unit can be approved
before implementation. The current unstaged retrieval implementation is paused
and must not be staged until prerequisite current-fact acquisition inventory,
value semantics, and schema decisions are completed or explicitly accepted.

This roadmap is a governance artifact. It does not implement fetching, schema,
runtime, validator, private vault, Discord, VLM, web daily-answer mode, API
fallback, vector search, persistent DB, or `sf6 ask` behavior.

## Global Constraints

- Official values may become `current_fact_authority` after deterministic
  parsing and validation.
- SuperCombo starts as enrichment, cross-reference, or candidate evidence only.
- Raw source values must be preserved exactly.
- Manual review, prose, FTS, and LLM memory are not numeric authority.
- Daily answer mode remains read-only for public repo data.
- No generated DB files are written to the repo unless a later ExecPlan
  explicitly approves that surface.
- Do not add private vault, Discord, VLM, web daily-answer mode, API fallback,
  vector search, persistent DB, or `sf6 ask` in these units unless a later
  ExecPlan changes the contract.
- Each unit needs a mandatory review before the next unit begins.

## Task Units

### 1. Current-Fact Acquisition Inventory Planning

Purpose: Define how the project will inventory official and SuperCombo
current-fact sources before changing schemas or retrieval.

Inputs:

- `docs/PLAN.md`
- Existing `data/exports/`
- Existing `data/aliases/`
- Current clean-slate CLI/tests

Outputs/artifacts:

- ExecPlan for source inventory
- Source list and per-source acquisition questions
- Field inventory template

Authority/evidence rules:

- This unit does not promote any new data to authority.
- It records source roles only.

Explicit exclusions:

- No fetching implementation.
- No schema implementation.
- No runtime answer behavior changes.

Validation commands:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Approval gate:

- Reviewer approves source list, artifact boundaries, and inventory template.

### 2. Official All-Character Raw Snapshot Acquisition

Purpose: Acquire or refresh official all-character raw snapshots with exact raw
values preserved.

Inputs:

- Approved acquisition inventory plan
- Official source URLs or source descriptors
- Existing `data/exports/` for comparison

Outputs/artifacts:

- Official raw snapshot artifacts
- Acquisition metadata including fetch time, source URL, extractor, and source
  version when available
- Raw row manifest

Authority/evidence rules:

- Official raw rows may become current-fact authority only after schema and
  validator gates.
- Raw values are preserved exactly and are not rewritten by the acquisition
  step.

Explicit exclusions:

- No SuperCombo acquisition.
- No parsed value semantics.
- No answer behavior change.

Validation commands:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Approval gate:

- Reviewer approves raw snapshot placement, manifest shape, and no-loss raw
  preservation.

### 3. SuperCombo All-Character Raw Snapshot Acquisition

Purpose: Acquire or inventory SuperCombo all-character raw snapshots as
cross-reference/enrichment evidence without making them numeric authority.

Inputs:

- Approved acquisition inventory plan
- SuperCombo source URLs or source descriptors
- Chosen acquisition approach, including Scrapling if selected

Outputs/artifacts:

- SuperCombo raw snapshot artifacts
- Acquisition metadata
- Raw row manifest

Authority/evidence rules:

- SuperCombo values are enrichment, cross-reference, or candidate evidence.
- They are not daily-answer numeric authority in this unit.

Explicit exclusions:

- No promotion policy.
- No answer behavior change.
- No official/SuperCombo reconciliation logic.

Validation commands:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Approval gate:

- Reviewer approves source role separation and raw preservation.

### 4. Value-Shape Inventory Across All Fields

Purpose: Build a complete inventory of observed value representations across all
characters, fields, and approved raw sources.

Inputs:

- Official raw snapshots
- SuperCombo raw snapshots
- Field inventory template

Outputs/artifacts:

- Value-shape inventory
- Per-field observed shape counts
- Examples for scalar, signed frame, parenthesized, plus-separated, multihit,
  conditional, missing/blank, nonnumeric note, raw-only, and unparsed values

Authority/evidence rules:

- Inventory classifies observed shapes; it does not calculate official totals.
- LLM interpretation is not an authority source.

Explicit exclusions:

- No parsed value implementation.
- No normalized export.
- No retrieval changes.

Validation commands:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Approval gate:

- Reviewer approves that inventory coverage is sufficient to design schemas.

### 5. Current-Fact JSON Schema Redesign

Purpose: Redesign current-fact schemas using the actual source and value-shape
inventory.

Inputs:

- Value-shape inventory
- Source snapshot manifests
- PLAN authority rules

Outputs/artifacts:

- JSON Schemas for `source_snapshot`, `source_row`, `current_fact_record`,
  `parsed_value`, and `value_shape_inventory`
- Fixtures for each discovered shape class
- Validator plan

Authority/evidence rules:

- `source_role`, `evidence_basis`, `review_status`, `patch_sensitivity`, and
  raw/parsed boundaries are explicit schema fields.
- `raw_value` is preserved even when `parsed_value` exists.

Explicit exclusions:

- No parser implementation.
- No generated DB.
- No retrieval changes.

Validation commands:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Approval gate:

- Reviewer approves schema boundaries and fixture coverage before parser work.

### 6. Deterministic Parsed-Value Classifier

Purpose: Implement deterministic classification for approved raw value shapes.

Inputs:

- Approved JSON Schemas
- Value-shape fixtures
- Official/SuperCombo raw snapshot examples

Outputs/artifacts:

- Parser/classifier implementation
- Tests for scalar, signed frame, parenthesized, plus-separated, multihit,
  conditional, missing/blank, nonnumeric note, raw-only, and unparsed values
- Validator coverage for parser output

Authority/evidence rules:

- Parser may classify values and produce safe numeric scalars only for approved
  shapes.
- Parser must not infer totals from expressions unless the approved schema and
  tests explicitly allow it.

Explicit exclusions:

- No LLM arithmetic.
- No SuperCombo promotion.
- No answer prose expansion.

Validation commands:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git diff --check
git status --short --branch
```

Approval gate:

- Reviewer approves parser boundaries and rejects any unapproved calculation.

### 7. Normalized Current-Fact Export Design

Purpose: Design normalized current-fact artifacts built from approved raw
snapshots and parsed values.

Inputs:

- Approved schemas
- Approved parser/classifier
- Raw snapshots

Outputs/artifacts:

- Normalized export ExecPlan
- Artifact placement decision
- Validator requirements

Authority/evidence rules:

- Normalized official current facts can become current-fact authority only when
  generated from approved official raw snapshots and parser outputs.
- SuperCombo remains separate unless later promoted by explicit policy.

Explicit exclusions:

- No generated DB unless separately approved.
- No private overlay.
- No answer runtime changes.

Validation commands:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Approval gate:

- Reviewer approves artifact location, generated markers, and authority status.

### 8. Retrieval DB Resume/Fix

Purpose: Resume retrieval only after current-fact schema/value prerequisites are
accepted, including the known FTS operator bug.

Inputs:

- Approved schemas or explicit acceptance to proceed without them
- Normalized current-fact design or approved raw-source boundary
- Paused retrieval implementation

Outputs/artifacts:

- Safe in-memory retrieval implementation
- Fixed literal FTS query handling for terms such as `OR`, `AND`, and `NOT`
- Retrieval tests for metadata filters and current-fact boundaries

Authority/evidence rules:

- FTS remains discovery-only.
- Numeric/current-fact answers use structured authority tables, not FTS.

Explicit exclusions:

- No persistent DB.
- No vector search.
- No broad answer behavior rewrite.

Validation commands:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
PYTHONPATH=src python -m sf6_knowledge_coach.cli search "JP 5LP"
PYTHONPATH=src python -m sf6_knowledge_coach.cli search "OR"
PYTHONPATH=src python -m sf6_knowledge_coach.cli search "AND"
PYTHONPATH=src python -m sf6_knowledge_coach.cli search "NOT"
git diff --check
git status --short --branch
```

Approval gate:

- Reviewer confirms retrieval is stage-ready and still non-authoritative for
  numeric facts.

### 9. Answer Behavior And Answer Verify Boundaries

Purpose: Define and implement answer preparation/verification behavior for
scalar, expression, raw-only, candidate, and unavailable values.

Inputs:

- Approved parser/classifier
- Approved authority policy
- Retrieval/current-fact implementation

Outputs/artifacts:

- Answer behavior tests
- Verification rules for source role, raw/parsed value kind, and uncertainty
- User-facing hold/uncertainty language for raw-only or candidate values

Authority/evidence rules:

- Deterministic official parsed values may answer directly when approved.
- Raw-only expressions must preserve raw value and include uncertainty or
  parsing limitation.
- SuperCombo candidates must not be stated as definitive daily-answer facts.

Explicit exclusions:

- No API fallback.
- No Discord adapter.
- No private personalization.

Validation commands:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer verify "JPの5LPはガードで何F？"
git diff --check
git status --short --branch
```

Approval gate:

- Reviewer approves that answer behavior follows source authority and value
  semantics.

### 10. CI/Validator Expansion

Purpose: Expand CI and validators only after schemas, parser, retrieval, and
answer boundaries have approved tests.

Inputs:

- Approved tests and validators from prior units
- Current `.github/workflows/ci.yml`
- Clean-slate validator

Outputs/artifacts:

- CI/validator ExecPlan
- Updated CI commands
- Validation guard coverage for source snapshots, schemas, parser fixtures, and
  answer boundaries

Authority/evidence rules:

- CI must reject private data, generated DB files not explicitly approved, and
  numeric authority violations.

Explicit exclusions:

- No dependency installation unless separately approved.
- No artifact upload of private or local state.
- No legacy workflow restoration.

Validation commands:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git diff --check
git status --short --branch
```

Approval gate:

- Reviewer approves CI coverage before PR readiness.

## Known Blocked Work

- Current unstaged retrieval implementation is not stage-ready.
- FTS operator bug must wait until retrieval resumes.
- Retrieval DB authority boundaries depend on current-fact schema/value
  semantics.
- Answer verification for expression/raw-only values depends on parsed-value
  classification.
- Inputless official rows need an identifier-based lookup decision.
- Alias tokenization and metadata filter CLI exposure remain unresolved.
- In-memory DB performance must be measured after normalized artifacts and
  retrieval scope are clearer.

## Validation Commands

Run from the repository root for this planning-only step:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-20 JST) Recorded that the current retrieval implementation is
  paused and not stage-ready.
- [x] (2026-05-20 JST) Listed known Phase 1 blocked work from retrieval review
  and current-fact value semantics discussion.
- [x] (2026-05-20 JST) Broke Phase 1 into ten separately reviewable units with
  per-unit approval gates.
- [x] (2026-05-20 JST) Completed planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [x] (2026-05-20 JST) Final roadmap review completed; roadmap is ready to
  stage as docs-only work while paused retrieval implementation remains
  unstaged.

## Decision Log

- Decision: Split Phase 1 into separately reviewed units before continuing
  retrieval implementation.
  Rationale: Current-fact value semantics, source acquisition, and JSON Schema
  boundaries are prerequisites for safe retrieval and answer behavior.
  Date/Author: 2026-05-20 / Codex

- Decision: Treat SuperCombo acquisition separately from official acquisition.
  Rationale: A common acquisition technique such as Scrapling may be practical,
  but source authority differs. Official values may become current-fact
  authority; SuperCombo starts as enrichment/cross-reference/candidate.
  Date/Author: 2026-05-20 / Codex

- Decision: Do not fix the FTS operator bug until retrieval resumes.
  Rationale: The bug is real, but fixing it alone would advance a retrieval
  slice whose current-fact schema and value semantics are not yet approved.
  Date/Author: 2026-05-20 / Codex

## Deviations

- None.

## Risks

- The roadmap may reveal that some current unstaged retrieval work needs to be
  discarded or rewritten after schema decisions.
- All-character acquisition may expose value shapes not listed here.
- SuperCombo source structure may require source-specific extraction policy even
  if acquisition tooling is shared.
- Planning-only validators do not prove future source acquisition or parser
  correctness.

## Completion Review Table

| PLAN item | Planned implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ExecPlan governance | Added a Phase 1 roadmap with separate approval gates before implementation units. | `docs/execplans/2026-05-20-phase1-roadmap.md` | `git diff --check`; clean-slate validator | Pass | None | None for roadmap docs | Roadmap may need adjustment after source inventory |
| Numeric/current-fact safety | Made acquisition inventory, value-shape inventory, schema redesign, and parser classification prerequisites before retrieval/answers. | Roadmap only | Review of roadmap | Pass | None | No implementation in this step | Future parser must avoid unapproved arithmetic |
| Source authority boundary | Separated official authority path from SuperCombo enrichment/candidate path. | Roadmap only | Review of roadmap | Pass | None | No source acquisition yet | Source-specific extraction may be needed |
| Retrieval pause | Recorded that retrieval implementation is paused and the FTS operator bug waits for retrieval resume. | `docs/execplans/2026-05-20-phase1-retrieval-contract.md`; roadmap | Review of docs | Pass | None | Current unstaged code remains not stage-ready | Unstaged code must not be committed accidentally |
