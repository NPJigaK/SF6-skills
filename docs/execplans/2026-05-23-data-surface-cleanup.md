# Data Surface Cleanup

Status: Implemented; awaiting mandatory review.

## Purpose

Clean legacy `data/` surfaces in one focused PR after the data surface
retirement inventory.

This ExecPlan deletes legacy checked-in source/raw/archive surfaces and updates
only the active metadata that would become stale after deletion. It does not
change runtime lookup behavior, schemas, parser/classifier behavior, retrieval
or answer behavior, source acquisition, authority status, or JSON Schema
redesign.

JSON Schema redesign remains blocked by the existing SuperCombo mapping and
value-shape disposition gates.

## Scope

Included:

- Delete checked-in legacy raw source pages under `data/raw/`.
- Delete old `data/exports/` CSV, manual-review, derived, and legacy
  SuperCombo enrichment sidecars.
- Delete legacy data governance/tooling metadata surfaces with no current
  runtime or validator references.
- Remove ignored local `data/exports.zip` if present.
- Update active `data/roster/current-character-roster.json` only to remove the
  stale checked-in `data/raw/` evidence reference.
- Update active `data/exports/README.md` only to describe the retained
  clean-slate export surface after sidecar deletion.

Excluded:

- Do not delete `data/exports/*/official_raw.json`.
- Do not delete `data/exports/*/snapshot_manifest.json`.
- Do not delete `data/exports/_index/manual-review-debt.json`.
- Do not delete `data/exports/README.md`.
- Do not delete `data/aliases/`.
- Do not delete `data/roster/`.
- Do not delete `data/value-shape-inventories/`.
- Do not delete `data/field-mappings/`.
- Do not delete `.local/`, `.agents/`, or `.venv/`.
- Do not alter source acquisition, retrieval, answer behavior, parser,
  classifier, normalized export, or authority status.
- Do not run live official or SuperCombo acquisition.
- Do not use `solve_cloudflare=True`.
- Do not apply `stash@{0}`.

## Acceptance Criteria

- The tracked deletion scope is exactly:
  - all 116 tracked files under `data/raw/`;
  - 319 tracked old export sidecars matching the approved suffix list;
  - 8 tracked legacy governance/tooling metadata files.
- The ignored local `data/exports.zip` file is removed if present, without
  creating a Git deletion entry.
- Retained surfaces remain present:
  - `data/exports/*/official_raw.json`;
  - `data/exports/*/snapshot_manifest.json`;
  - `data/exports/_index/manual-review-debt.json`;
  - `data/exports/README.md`;
  - `data/aliases/`;
  - `data/roster/`;
  - `data/value-shape-inventories/`;
  - `data/field-mappings/`.
- `data/roster/current-character-roster.json` no longer references deleted
  `data/raw/` paths.
- `data/exports/README.md` no longer documents deleted sidecars as current
  layout.
- No runtime/schema/parser/retrieval/answer behavior changes are made.
- Validation passes.

## Files / Interfaces

Changed by this implementation:

- `docs/execplans/2026-05-23-data-surface-cleanup.md`
- `data/roster/current-character-roster.json`
- `data/exports/README.md`

Deleted tracked data surfaces:

- `data/raw/`
- old `data/exports/` sidecars:
  - `data/exports/*/official_raw.csv`
  - `data/exports/*/official_raw_manual_review.*`
  - `data/exports/*/derived_metrics.*`
  - `data/exports/*/derived_metrics_manual_review.*`
  - `data/exports/*/supercombo_enrichment.*`
  - `data/exports/*/supercombo_enrichment_manual_review.*`
- `data/external-frame-atlas/`
- `data/toolchain/`
- `data/knowledge-integrity.json`
- `data/knowledge-lineage.json`
- `data/repository-surfaces.json`

Deleted ignored local artifact:

- `data/exports.zip`, if present.

## Exact Deletion Set Definition

The tracked deletion set is built only from `git ls-files` and these exact
path filters:

```bash
git ls-files data/raw
git ls-files data/exports \
  | rg '/(official_raw\.csv|official_raw_manual_review\.(csv|json)|derived_metrics\.(csv|json)|derived_metrics_manual_review\.(csv|json)|supercombo_enrichment\.(csv|json)|supercombo_enrichment_manual_review\.(csv|json))$'
git ls-files data/external-frame-atlas data/toolchain \
  data/knowledge-integrity.json data/knowledge-lineage.json \
  data/repository-surfaces.json
```

Pre-delete counts:

| Delete group | Count |
| --- | ---: |
| `data/raw/` tracked files | 116 |
| old `data/exports/` sidecars | 319 |
| legacy governance/tooling metadata files | 8 |
| total tracked deletions | 443 |

The implementation must not delete tracked files outside this generated set.

Retain checks:

```bash
git ls-files data/exports \
  | rg '/(official_raw\.json|snapshot_manifest\.json)$|data/exports/README\.md|data/exports/_index/manual-review-debt\.json'
git ls-files data/aliases data/roster data/value-shape-inventories data/field-mappings
```

Pre-delete retained counts:

| Retain group | Count |
| --- | ---: |
| retained `data/exports/` current/provenance files | 60 |
| aliases, roster, value-shape inventories, field mappings | 6 |

## Reference Findings

Repository search found no current runtime/test/validator references to the
tracked delete set, except:

- `data/roster/current-character-roster.json` contains one historical
  `data/raw/.../page.html` source reference. This implementation updates that
  metadata to point at the current acquisition report instead of a checked-in
  raw page.
- `data/exports/README.md` describes old sidecars as part of current layout.
  This implementation updates that README to reflect retained current facts
  and retired sidecars.
- Historical ExecPlans mention these old surfaces. They are not runtime
  blockers and are left as historical records unless validation fails.

Current runtime blockers remain protected:

- `current_facts.py` loads `data/exports/*/official_raw.json`.
- Source acquisition coverage uses `data/roster/current-character-roster.json`
  source URLs.
- Query resolution uses `data/aliases/`.
- Value-shape inventory and SuperCombo mapping validators use
  `data/value-shape-inventories/` and `data/field-mappings/`.

## Source Boundary And Privacy Notes

Checked-in `data/raw/` contains full `page.html` source documents plus
metadata. Current source acquisition raw artifacts belong under ignored
repo-local storage:

```text
.local/source-acquisition/
```

Reviewer visual evidence belongs under ignored repo-local storage:

```text
.local/reviewer-evidence/
```

The cleanup reduces public source-boundary exposure and keeps only summarized,
reviewable public artifacts. It must not add raw HTML, raw rows, screenshots,
cookies, browser profiles, auth/session data, request headers, tokens, secrets,
traces, debug dumps, answer logs, training logs, or private user data.

## Validation Commands

Run from repository root:

```bash
git diff --check
git diff --cached --check
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_inventory.py
PYTHONPATH=src uv run --locked python tests/validation/validate_supercombo_field_mapping.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
git ls-files data/raw
git status --short --branch
```

Expected:

- `git ls-files data/raw` prints no tracked files.
- Validation commands pass.
- No ignored `.local/`, `.agents/`, `.venv/`, raw screenshots, cookies,
  browser profiles, or raw acquisition artifacts are staged.

## Progress

- [x] (2026-05-23 JST) Confirmed cleanup branch
  `impl/data-surface-cleanup`.
- [x] (2026-05-23 JST) Confirmed tracked delete counts:
  116 `data/raw/` files, 319 old export sidecars, and 8 legacy
  governance/tooling metadata files.
- [x] (2026-05-23 JST) Found stale `data/raw/` reference in
  `data/roster/current-character-roster.json` and added it to focused cleanup
  scope.
- [x] (2026-05-23 JST) Found stale active layout documentation in
  `data/exports/README.md` and added it to focused cleanup scope.
- [x] (2026-05-23 JST) Deleted approved tracked data surfaces:
  116 `data/raw/` files, 319 old export sidecars, and 8 legacy
  governance/tooling metadata files.
- [x] (2026-05-23 JST) Removed ignored local `data/exports.zip`.
- [x] (2026-05-23 JST) Updated `data/roster/current-character-roster.json` to
  replace the old checked-in raw source page evidence path with the current
  acquisition report reference.
- [x] (2026-05-23 JST) Updated `data/exports/README.md` to describe the
  retained clean-slate export surface after sidecar deletion.
- [x] (2026-05-23 JST) Confirmed post-delete retain counts:
  60 retained `data/exports/` current/provenance files and 6 retained aliases,
  roster, value-shape, and field-mapping files.
- [x] (2026-05-23 JST) Completed cleanup validation:
  `git diff --check`,
  `git diff --cached --check`,
  `PYTHONPATH=src uv run --locked python -m unittest discover -s tests`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_value_shape_inventory.py`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_supercombo_field_mapping.py`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"`,
  `PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`,
  and post-delete path count checks.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Delete all checked-in `data/raw/` files.
  Rationale: Full source pages are legacy public raw documents; current raw
  source artifacts are ignored under `.local/source-acquisition/`.
  Date/Author: 2026-05-23 / Codex

- Decision: Delete old export sidecars but retain `official_raw.json`,
  `snapshot_manifest.json`, `manual-review-debt.json`, and `README.md`.
  Rationale: `official_raw.json` is current runtime input, while snapshot and
  manual-review debt files may still be useful provenance/review inputs.
  Date/Author: 2026-05-23 / Codex

- Decision: Delete legacy governance/tooling metadata files with no current
  runtime/test/validator references.
  Rationale: These are pre-clean-slate metadata surfaces and should not remain
  in `data/` unless an active workflow depends on them.
  Date/Author: 2026-05-23 / Codex

- Decision: Update the roster metadata instead of deleting the roster.
  Rationale: The roster remains current acquisition input, but its old checked
  raw evidence path would become stale after `data/raw/` deletion.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- Whether retained `snapshot_manifest.json` files and
  `data/exports/_index/manual-review-debt.json` should be migrated or deleted
  in a later cleanup.
- Whether a validator should permanently assert that checked-in `data/raw/`
  remains absent.
- Whether historical ExecPlans should later be annotated to point at this
  cleanup PR.

## Deviations

- None.

## Risks

- Historical docs still mention deleted legacy surfaces. They are retained as
  historical records unless they create active operational confusion.
- Retained `snapshot_manifest.json` and manual-review debt metadata may still
  be legacy debt; they are intentionally deferred because they are provenance
  and review surfaces rather than raw source pages.
- JSON Schema redesign remains blocked.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Clean legacy raw data | Deleted exact 116-file `data/raw/` tracked deletion set | ExecPlan and deletions | `git ls-files data/raw` | Pass, no tracked files remain | None | Mandatory review pending | Historical docs may mention deleted paths |
| Clean export sidecars | Deleted 319 old sidecars while retaining current JSON/provenance files | ExecPlan and deletions | CLI smoke and unit tests | Pass | None | Mandatory review pending | Snapshot/manual-review debt retained |
| Clean metadata debt | Deleted 8 unreferenced governance/tooling metadata files | ExecPlan and deletions | clean-slate validator | Pass | None | Mandatory review pending | Hidden human workflow could miss them |
| Preserve runtime inputs | Retained official current facts, aliases, roster, value-shape inventories, and field mappings | ExecPlan, roster/README updates | unit tests and focused validators | Pass | None | Mandatory review pending | None |
