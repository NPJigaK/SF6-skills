# Data Surface Retirement Inventory

Status: Drafted for review.

## Purpose

Inventory legacy and public `data/` surfaces, classify what can be retained,
migrated, archived, or deleted by later ExecPlans, and define the repo-local
ignored storage boundary for reviewer-only visual evidence.

This is a planning-only ExecPlan. It does not delete files, change runtime
behavior, change schemas, change parser/classifier behavior, change retrieval
or answer behavior, run live acquisition, or alter authority status.

JSON Schema redesign remains blocked by the existing SuperCombo mapping and
value-shape disposition gates.

## Scope

Included:

- Inspect actual repository references for known `data/` surfaces.
- Classify each target surface as one of:
  - `retain_current_runtime`
  - `retain_current_review_artifact`
  - `migrate_later`
  - `delete_candidate`
  - `archive_candidate`
  - `blocked_pending_reference_review`
- Separate `data/exports/*/official_raw.json` from old CSV,
  manual-review, derived, and SuperCombo enrichment sidecars.
- Identify deletion/archive candidates for later exact-path ExecPlans.
- Record reviewer evidence storage rules under `.local/reviewer-evidence/`.

Excluded:

- No file deletion.
- No runtime/schema/parser/classifier/retrieval/answer behavior changes.
- No live official or SuperCombo acquisition.
- No `solve_cloudflare=True`.
- No stash application.
- No reviewer screenshots or evidence capture in this step.

## Acceptance Criteria

- All requested data surfaces are classified.
- `data/exports/*/official_raw.json` is not classified as delete-ready while
  `src/sf6_knowledge_coach/current_facts.py` depends on it.
- New value-shape and field-mapping artifacts are retained.
- `data/raw/` is flagged as high-priority review because checked-in raw source
  pages can carry source-boundary and privacy risk.
- `data/exports.zip` is classified separately as ignored local archive debt.
- Old CSV/manual-review/derived/SuperCombo enrichment sidecars under
  `data/exports/` are identified separately from `official_raw.json`.
- Any deletion requires a later deletion ExecPlan with an exact path list and
  validation commands.
- Reviewer visual evidence storage is constrained to repo-local ignored
  `.local/reviewer-evidence/`.
- Planning validation passes.

## Files / Interfaces

Created in this planning step:

- `docs/execplans/2026-05-23-data-surface-retirement-inventory.md`

Inspected data surfaces:

- `data/aliases/`
- `data/roster/`
- `data/exports/`
- `data/exports.zip`
- `data/raw/`
- `data/external-frame-atlas/`
- `data/toolchain/`
- `data/value-shape-inventories/`
- `data/field-mappings/`
- `data/knowledge-integrity.json`
- `data/knowledge-lineage.json`
- `data/repository-surfaces.json`

No implementation files are changed by this ExecPlan.

## Reference Findings

Repository reference checks found:

- `data/aliases/ja-query-fixtures.json` is used through
  `src/sf6_knowledge_coach/paths.py`, `aliases.py`, `cli.py`, and
  `answering.py`, and is required by `tests/validation/validate_clean_slate.py`.
- `data/roster/current-character-roster.json` is used by
  `src/sf6_knowledge_coach/source_acquisition.py`, source-acquisition tests,
  and acquisition planning/report surfaces.
- `data/exports/*/official_raw.json` is used by
  `src/sf6_knowledge_coach/current_facts.py` for current lookup and by tests.
- `data/exports/` also contains old sidecars not used by current runtime:
  `official_raw.csv`, `official_raw_manual_review.*`, `derived_metrics.*`,
  `derived_metrics_manual_review.*`, `supercombo_enrichment.*`,
  `supercombo_enrichment_manual_review.*`, `snapshot_manifest.json`, and
  `_index/manual-review-debt.json`.
- `data/raw/` contains checked-in source pages and metadata:
  58 official raw files and 58 SuperCombo raw files, about 28 MB total.
- `data/exports.zip` exists locally, is ignored by `.gitignore` via `*.zip`,
  and is not tracked by Git.
- `data/value-shape-inventories/` is used by
  `src/sf6_knowledge_coach/value_shape_inventory.py`,
  `src/sf6_knowledge_coach/supercombo_field_mapping.py`, and ExecPlans.
- `data/field-mappings/` is used by
  `src/sf6_knowledge_coach/supercombo_field_mapping.py` and ExecPlans.
- `data/external-frame-atlas/`, `data/toolchain/`,
  `data/knowledge-integrity.json`, `data/knowledge-lineage.json`, and
  `data/repository-surfaces.json` have no current runtime references found by
  repository search, but they are policy/metadata surfaces and need reference
  review before deletion.

Approximate sizes:

| Surface | Size / count observed |
| --- | ---: |
| `data/raw/` | 28 MB, 116 tracked files |
| `data/exports/` | 8.2 MB, 378 tracked files |
| `data/value-shape-inventories/` | 1.7 MB |
| `data/exports.zip` | 1.2 MB, ignored local file |
| `data/field-mappings/` | 396 KB |
| `data/toolchain/` | 24 KB |
| `data/external-frame-atlas/` | 20 KB |
| `data/roster/` | 12 KB |
| `data/aliases/` | 8 KB |

## Inventory Classification

| Surface | Classification | Rationale | Later action |
| --- | --- | --- | --- |
| `data/aliases/` | `retain_current_runtime` | Query normalization seed used by current CLI/answering path and clean-slate validation. | Retain until replacement alias store is implemented and validated. |
| `data/roster/` | `retain_current_runtime` | Source acquisition and planning use `current-character-roster.json` for all-character coverage and source URLs. | Retain; refresh only through a dedicated roster/source ExecPlan. |
| `data/exports/*/official_raw.json` | `retain_current_runtime` | `current_facts.py` loads these files for current lookup authority. | Not delete-ready. Replacement requires a runtime/data migration ExecPlan. |
| `data/exports/README.md` | `retain_current_runtime` | Documents current export authority boundaries. | Retain while `data/exports/` remains active. |
| `data/exports/*/official_raw.csv` | `delete_candidate` | Duplicate sidecar for JSON authority data; no current runtime reference found. | Later exact-path deletion ExecPlan after reviewer confirms CSV is not needed for review. |
| `data/exports/*/official_raw_manual_review.*` | `delete_candidate` | Manual-review sidecars are non-authority and not used by current runtime. | Later exact-path deletion ExecPlan or migration into reviewed disposition artifacts if needed. |
| `data/exports/*/derived_metrics.*` | `delete_candidate` | Derived legacy outputs are not current numeric authority in the clean-slate runtime. | Later exact-path deletion ExecPlan after confirming no evaluator depends on them. |
| `data/exports/*/derived_metrics_manual_review.*` | `delete_candidate` | Legacy manual-review sidecars, non-authority. | Later exact-path deletion ExecPlan or archive decision. |
| `data/exports/*/supercombo_enrichment.*` | `delete_candidate` | Legacy enrichment sidecars are superseded in direction by latest acquisition, value-shape, and field-mapping artifacts; not numeric authority. | Later exact-path deletion ExecPlan after confirming no mapping/disposition task needs them. |
| `data/exports/*/supercombo_enrichment_manual_review.*` | `delete_candidate` | Legacy manual-review sidecars, non-authority. | Later exact-path deletion ExecPlan or archive decision. |
| `data/exports/*/snapshot_manifest.json` | `migrate_later` | Provenance sidecars may contain useful migration/reference metadata but are not current runtime lookup inputs. | Review before deleting; migrate only needed provenance into current acquisition reports/artifacts. |
| `data/exports/_index/manual-review-debt.json` | `migrate_later` | Observability index for old manual-review debt, not current runtime authority. | Review against current review-item disposition work before deletion. |
| `data/exports.zip` | `archive_candidate` | Ignored local archive/duplicate debt; not tracked and not referenced by current code. | Later local cleanup step may remove it; no Git deletion artifact exists. |
| `data/raw/` | `delete_candidate` | High-priority review: checked-in raw source pages are large source documents and can carry source-boundary/privacy risk; current acquisition uses ignored `.local/source-acquisition/` instead. | Later exact-path deletion ExecPlan should remove or archive after confirming no current validator/report requires these checked-in pages. |
| `data/external-frame-atlas/` | `archive_candidate` | Metadata-only external source evaluation; no current runtime reference found. | Review whether to keep as policy docs or move to docs-only archive before deletion. |
| `data/toolchain/` | `archive_candidate` | Maintainer/Hermes policy data, not SF6 gameplay runtime data; no current runtime reference found. | Review whether policy belongs in `AGENTS.md`/docs or can be archived. |
| `data/value-shape-inventories/` | `retain_current_review_artifact` | Required input for mapping/classifier/schema planning and validation. | Retain; do not delete new inventory artifacts. |
| `data/field-mappings/` | `retain_current_review_artifact` | Required SuperCombo 403 mapping summary artifact. | Retain; do not delete new mapping artifacts. |
| `data/knowledge-integrity.json` | `blocked_pending_reference_review` | Legacy knowledge integrity metadata has no current runtime reference found, but may encode governance history. | Review with PLAN/AGENTS governance before archive/delete classification. |
| `data/knowledge-lineage.json` | `blocked_pending_reference_review` | Legacy lineage metadata has no current runtime reference found, but may encode governance history. | Review with PLAN/AGENTS governance before archive/delete classification. |
| `data/repository-surfaces.json` | `blocked_pending_reference_review` | Surface registry may overlap with this inventory but no current runtime reference found. | Compare against this ExecPlan before deciding migration or deletion. |

## Delete / Archive Candidate Summary

Deletion candidates for later exact-path ExecPlans:

- `data/raw/`
- `data/exports/*/official_raw.csv`
- `data/exports/*/official_raw_manual_review.*`
- `data/exports/*/derived_metrics.*`
- `data/exports/*/derived_metrics_manual_review.*`
- `data/exports/*/supercombo_enrichment.*`
- `data/exports/*/supercombo_enrichment_manual_review.*`

Migration or archive candidates:

- `data/exports/*/snapshot_manifest.json`
- `data/exports/_index/manual-review-debt.json`
- `data/external-frame-atlas/`
- `data/toolchain/`
- `data/exports.zip` ignored local archive debt

Blocked pending reference review:

- `data/knowledge-integrity.json`
- `data/knowledge-lineage.json`
- `data/repository-surfaces.json`

Retain blockers:

- `data/exports/*/official_raw.json` cannot be deleted while
  `current_facts.py` uses it.
- `data/aliases/` cannot be deleted while `aliases.py` and CLI answering use
  it.
- `data/roster/` cannot be deleted while source acquisition coverage uses it.
- `data/value-shape-inventories/` and `data/field-mappings/` cannot be deleted
  while mapping/disposition/schema planning depends on them.

## Reviewer Evidence Storage Boundary

Reviewer visual evidence, including screenshots used for LLM-assisted
comparison of rendered pages against extracted JSON artifacts, must be stored
only under:

```text
.local/reviewer-evidence/
```

Rules:

- `.local/reviewer-evidence/` must remain ignored and must never be committed.
- Do not store reviewer screenshots or temporary visual-review outputs in
  `/tmp`, global Codex paths, user profile directories, browser profile
  directories, or OS-global temp locations unless explicitly approved for
  one-off debugging.
- Evidence must not include cookies, browser profiles, auth/session data,
  request headers, tokens, secrets, full raw HTML dumps, full raw row dumps,
  traces, debug dumps, answer logs, training logs, or private user data.
- Reviewer screenshots may be used only as reviewer-only external observation,
  not as runtime, CI, deterministic validator, daily-answer authority, or
  numeric authority.
- If a later workflow needs reproducible visual evidence, create a dedicated
  ExecPlan for evidence capture, retention period, cleanup rule, and
  privacy/source-boundary guard.

## Later Deletion Requirements

No deletion is approved by this ExecPlan.

Any later deletion ExecPlan must include:

- exact path list;
- whether each path is tracked or ignored local-only;
- reference search results;
- validation commands before and after deletion;
- public/private/source-boundary review for raw source documents;
- explicit confirmation that `official_raw.json`, new value-shape artifacts,
  and new field-mapping artifacts are not deleted unless a replacement plan is
  already approved.

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Confirmed local `main` is updated to
  `90e4d71837efef9460df596aa44c4b456f950ee3`.
- [x] (2026-05-23 JST) Created branch
  `plan/data-surface-retirement-inventory`.
- [x] (2026-05-23 JST) Inspected target `data/` surfaces, sizes, tracked
  files, ignored `data/exports.zip`, and repository references.
- [x] (2026-05-23 JST) Drafted this inventory and classification ExecPlan.
- [x] (2026-05-23 JST) Completed planning validation:
  `git diff --check`,
  `PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py`,
  and `git status --short --branch`.
- [ ] Complete mandatory review.

## Decision Log

- Decision: Keep `data/exports/*/official_raw.json` as
  `retain_current_runtime`.
  Rationale: Current `current_facts.py` lookup uses those files as exact
  current-fact input.
  Date/Author: 2026-05-23 / Codex

- Decision: Treat `data/raw/` as a high-priority deletion candidate, not as a
  retained review artifact.
  Rationale: Current acquisition stores raw source documents under ignored
  `.local/source-acquisition/`; checked-in raw pages are large and create
  source-boundary/privacy review risk.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep new value-shape and field-mapping artifacts.
  Rationale: They are active review inputs for mapping, disposition, and later
  schema planning.
  Date/Author: 2026-05-23 / Codex

- Decision: Standardize reviewer-only visual evidence under
  `.local/reviewer-evidence/`.
  Rationale: Reviewer evidence should stay repo-local and ignored, avoiding
  global temp/profile pollution while remaining outside committed artifacts.
  Date/Author: 2026-05-23 / Codex

## Unresolved Decisions

- Whether to delete or archive `data/raw/` first, and whether any source terms
  or attribution review is needed before removing checked-in raw pages.
- Whether old `data/exports/*/snapshot_manifest.json` provenance should be
  migrated into current acquisition reports before deletion.
- Whether `data/exports/_index/manual-review-debt.json` contains disposition
  information still useful for the 247 review-item workflow.
- Whether `data/external-frame-atlas/` and `data/toolchain/` should remain as
  policy metadata or move to docs/archive.
- Whether `data/knowledge-integrity.json`, `data/knowledge-lineage.json`, and
  `data/repository-surfaces.json` should be migrated, archived, or deleted.

## Deviations

- None.

## Risks

- Deleting `data/exports/*/official_raw.json` would break current lookup and
  tests; this ExecPlan explicitly blocks that.
- Deleting `data/raw/` may remove historical source pages that some reviewer
  still expects; later deletion must review exact path list and references.
- Keeping `data/raw/` too long preserves large source documents in the public
  repo and increases source-boundary review risk.
- Treating ignored `data/exports.zip` as a Git deletion target would be
  incorrect because it is not tracked.
- Reviewer evidence stored outside `.local/reviewer-evidence/` can pollute
  global/user temp locations or leak into unrelated tooling state.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Inventory data surfaces | Classified requested `data/` surfaces and sidecars | `docs/execplans/2026-05-23-data-surface-retirement-inventory.md` | `git diff --check` | Pass | None | Mandatory review pending | Later deletion must use exact paths |
| Preserve runtime blockers | Marked aliases, roster, and `official_raw.json` as retain-current-runtime | ExecPlan only | reviewer check | Pending | None | Runtime replacement not planned here | Accidental deletion would break lookup |
| Identify deletion/archive candidates | Flagged `data/raw/`, old export sidecars, and ignored `data/exports.zip` debt | ExecPlan only | reviewer check | Pending | None | Deletion not implemented | Source-boundary review still needed |
| Reviewer evidence boundary | Defined `.local/reviewer-evidence/` as ignored reviewer-only evidence storage | ExecPlan only | reviewer check | Pending | None | No evidence cleanup implemented | Future workflows need their own ExecPlan |
