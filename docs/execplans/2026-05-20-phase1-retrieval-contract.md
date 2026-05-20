# Phase 1 Retrieval Contract

Status: Paused; implementation is not stage-ready pending Phase 1 roadmap prerequisites.

## Purpose

Plan the smallest Phase 1 implementation slice that moves the clean-slate
scaffold toward the retrieval contract in `docs/PLAN.md` without broad runtime
work.

This ExecPlan records the small attempted implementation slice for an in-memory
SQLite retrieval boundary. Review found that retrieval should pause until
current-fact acquisition inventory, value semantics, and schema redesign are
planned and approved. It does not implement private vault, Discord, VLM, web,
API, or vector-search behavior.

## Scope

Included in the next implementation slice:

- Add an in-memory SQLite retrieval database built from public repo data at
  command runtime.
- Add an FTS5 prose/search table for searchable public text snippets.
- Add structured numeric/current-fact tables sourced only from
  `data/exports/*/official_raw.json`.
- Add alias dictionary tables sourced only from `data/aliases/`.
- Add metadata/evidence-boundary fields that can filter search and lookup
  results.
- Keep numeric/current-fact answers deterministic and grounded in structured
  tables.
- Keep JP as the initial active character while preserving
  character-agnostic schema and query paths.
- Add tests for retrieval DB construction, current-fact lookup, FTS search,
  alias loading, metadata filters, and answer verification boundaries.

Excluded from the next implementation slice:

- Do not create a persistent SQLite file in the repository.
- Do not write generated DB files in daily answer mode.
- Do not implement private vault, private overlay DB, personal profiles,
  personal logs, or private knowledge.
- Do not implement Discord, VLM, video pipeline, web daily-answer mode, or API
  fallback.
- Do not add vector search or embeddings.
- Do not add external package dependencies.
- Do not create broad knowledge authoring, review workflow, or generated public
  DB publishing behavior.
- Do not restore deleted legacy runtime, validators, packages, workflows, or
  schemas.

## Acceptance Criteria

- A retrieval module can build an in-memory SQLite database from public repo
  data without writing files.
- SQLite FTS5 is used for a first prose/search surface.
- The FTS surface is explicitly non-authoritative for frame, damage, scaling,
  punish, combo damage, patch delta, and current move facts.
- Structured current-fact lookup uses tables populated from
  `data/exports/*/official_raw.json` only.
- CSV sidecars, `*_manual_review.*`, `supercombo_enrichment.*`, and
  `derived_metrics.*` are not numeric-answer authority in this slice.
- Alias loading reads `data/aliases/` and preserves English-compatible metadata
  keys.
- Metadata/evidence filters are represented as queryable columns, at minimum:
  `source_role`, `evidence_basis`, `review_status`, `patch_sensitivity`,
  `character_slug`, and `data_source`.
- Numeric/current-fact answer preparation cannot use FTS text or model memory
  as definitive evidence.
- Daily answer commands remain read-only for the public repository.
- Answer logs remain Git-outside only; this slice does not change log writing.
- Tests prove that JP current facts still work without hardcoding JP as a
  global assumption.

## Files / Interfaces

Implementation files:

- `src/sf6_knowledge_coach/retrieval.py`
- `src/sf6_knowledge_coach/current_facts.py`
- `src/sf6_knowledge_coach/answering.py`
- `src/sf6_knowledge_coach/cli.py`
- `tests/test_retrieval.py`
- `tests/test_cli.py`
- `tests/validation/validate_clean_slate.py`
- `README.md`
- `docs/execplans/2026-05-20-phase1-retrieval-contract.md`

Planned command behavior:

```text
sf6 search <query> [--character <slug>] [--limit <n>]
sf6 current lookup --character <slug> --move <input> [--field <field>]
sf6 answer prepare <query> [--log]
sf6 answer verify <query>
```

The existing command names remain stable. Implementation may change their
internal data source from raw JSON iteration to the retrieval DB API.

No new `sf6 ask` command is included in this slice.

## Retrieval Contract

The next implementation should create a small retrieval boundary with these
conceptual tables.

```text
current_moves
  character_slug
  move_id
  move_name
  input
  field/value columns from official_raw.json
  data_source = data/exports official_raw
  source_role = current_fact_authority
  evidence_basis = official
  review_status = reviewed
  patch_sensitivity = high

search_documents
  doc_id
  title
  body
  character_slug nullable
  source_role
  evidence_basis
  review_status
  patch_sensitivity
  data_source

search_documents_fts
  FTS5 index over title/body

aliases
  alias
  normalized_key
  normalized_value
  source_path
```

The first FTS corpus may be intentionally narrow: generated public text
snippets derived from current move metadata and safe public README-style
descriptions. It must not be treated as authority for numeric answers.

## Validation Commands

Run from the repository root for this planning-only step:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Future implementation validation should include:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
PYTHONPATH=src python -m sf6_knowledge_coach.cli search "JP 5LP"
PYTHONPATH=src python -m sf6_knowledge_coach.cli current lookup --character jp --move 5LP --field block_adv
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer verify "JPの5LPはガードで何F？"
git diff --check
git diff --cached --check
git status --short --branch
```

## Progress

- [x] (2026-05-20 JST) Verified PR #298 was merged into `main` and `origin/main`
  points to merge commit `214c74e33b7473a00cc3a4b51f1b4b42c8c2e474`.
- [x] (2026-05-20 JST) Verified main branch CI passed for merge commit
  `214c74e33b7473a00cc3a4b51f1b4b42c8c2e474`.
- [x] (2026-05-20 JST) Created branch `plan/phase1-retrieval-contract` from
  current `main`.
- [x] (2026-05-20 JST) Reviewed `AGENTS.md`, `docs/PLAN.md`, current CLI,
  current fact lookup, alias loading, tests, and retained data surfaces.
- [x] (2026-05-20 JST) Confirmed local Python SQLite supports FTS5.
- [x] (2026-05-20 JST) Drafted this planning-only ExecPlan.
- [x] (2026-05-20 JST) Ran planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [x] (2026-05-20 JST) Committed this ExecPlan before implementation with
  message `Plan Phase 1 retrieval contract`.
- [x] (2026-05-20 JST) Added `src/sf6_knowledge_coach/retrieval.py` with
  in-memory SQLite tables for current facts, search documents, FTS5, and
  aliases.
- [x] (2026-05-20 JST) Routed `current lookup`, `search`, and numeric answer
  preparation through the retrieval boundary without adding persistent DB
  files.
- [x] (2026-05-20 JST) Added tests for in-memory DB behavior, FTS discovery,
  metadata filters, alias table loading, character-agnostic current fact
  lookup, and numeric evidence verification.
- [x] (2026-05-20 JST) Ran full implementation validation:
  `PYTHONPATH=src python -m unittest discover -s tests`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`,
  `sf6 search`, `sf6 current lookup`, `sf6 answer prepare`, `sf6 answer
  verify`, `git diff --check`, `git diff --cached --check`, and
  `git status --short --branch`.
- [x] (2026-05-20 JST) Mandatory review found the current unstaged retrieval
  implementation is not stage-ready. The immediate bug is raw FTS operator
  handling for search terms such as `OR`, `AND`, and `NOT`; the larger
  prerequisite is deterministic current-fact acquisition inventory, value
  semantics, and schema redesign.
- [x] (2026-05-20 JST) Paused retrieval implementation. The current unstaged
  retrieval changes must not be staged until prerequisite ExecPlans are
  completed or explicitly accepted.
- [x] (2026-05-20 JST) Created `docs/execplans/2026-05-20-phase1-roadmap.md`
  to break Phase 1 into separately reviewable units.

## Decision Log

- Decision: The next slice uses in-memory SQLite, not a persisted DB file.
  Rationale: This proves the retrieval contract while preserving daily answer
  mode as read-only for the public repository and avoiding generated binary DB
  review churn.
  Date/Author: 2026-05-20 / Codex

- Decision: Use Python standard library `sqlite3` and SQLite FTS5.
  Rationale: The scaffold currently has no external dependencies, and local
  verification showed the available Python SQLite build supports FTS5.
  Date/Author: 2026-05-20 / Codex

- Decision: `data/exports/*/official_raw.json` remains the only numeric/current
  fact authority for this slice.
  Rationale: `docs/PLAN.md` requires deterministic tools/tables for current
  facts, and `AGENTS.md` forbids numeric answers from memory.
  Date/Author: 2026-05-20 / Codex

- Decision: FTS search may find current-fact related text but may not authorize
  numeric answers.
  Rationale: FTS is useful for discovery, but frame, damage, scaling, punish,
  combo damage, patch delta, and current move facts require structured table
  results.
  Date/Author: 2026-05-20 / Codex

- Decision: Do not implement private vault in this slice.
  Rationale: The retrieval contract can advance using public surfaces only;
  private overlay behavior needs a separate boundary-focused ExecPlan.
  Date/Author: 2026-05-20 / Codex

- Decision: Store official rows with missing `input` in `current_moves` with a
  nullable input column rather than dropping them.
  Rationale: Some `official_raw.json` records represent follow-up or automatic
  move states without input notation. They remain official current-fact rows,
  but command lookup by input naturally cannot select them.
  Date/Author: 2026-05-20 / Codex

- Decision: Keep alias-backed context resolution in `aliases.py` unchanged and
  add the alias table to the retrieval DB for the next boundary.
  Rationale: The approved slice allowed queryable alias tables, but broader
  tokenization or normalization redesign remains unresolved.
  Date/Author: 2026-05-20 / Codex

- Decision: Pause the current retrieval implementation rather than fix the FTS
  operator bug in isolation.
  Rationale: Review found `sf6 search "OR"`, `sf6 search "AND"`, and
  `sf6 search "NOT"` can traceback because raw user tokens are passed into the
  SQLite FTS5 `MATCH` expression. That bug is real, but current-fact value
  semantics and schema boundaries are a higher-priority prerequisite for making
  retrieval and answer verification safe.
  Date/Author: 2026-05-20 / Codex

- Decision: Retrieval work resumes only after Phase 1 prerequisite ExecPlans
  are completed or explicitly accepted.
  Rationale: Current facts must preserve raw official/SuperCombo values,
  classify observed value shapes, and define JSON Schemas before retrieval can
  safely expose normalized/current-fact answer behavior.
  Date/Author: 2026-05-20 / Codex

## Deviations

- None.

## Unresolved Decisions

- Whether a later slice should create a persisted generated public SQLite DB,
  and if so whether it belongs in Git, GitHub release artifacts, or a Git-outside
  local cache.
- How all-character official and SuperCombo raw snapshots should be acquired
  and inventoried.
- How observed current-fact value shapes should drive JSON Schema redesign.
- Which parsed value classes can safely support deterministic arithmetic and
  which must remain raw-only or manual-review-required.
- How SuperCombo values should be represented as enrichment, cross-reference,
  or candidate evidence without becoming daily-answer numeric authority.
- Whether future reviewed prose knowledge should live under a new `knowledge/`
  surface or another public source path after the clean-slate deletion.
- How much metadata filtering should be exposed through CLI flags versus kept
  internal to answer preparation.
- Whether alias normalization should move from current query-substring behavior
  to a table-driven tokenization pass.

## Risks

- In-memory DB construction may become slow as public data grows. This is
  acceptable for the next slice but should be measured before broader use.
- FTS5 availability must be verified in CI, even though it works locally.
- Current `data/aliases/` seed coverage is small, so query normalization will
  remain limited.
- Search result ranking will be minimal in this slice.
- The slice does not yet provide complete Phase 1 public knowledge retrieval;
  it only establishes the retrieval contract boundary.
- Some official rows have no input notation; they are stored in the structured
  table but cannot be selected through `current lookup --move` until a later
  identifier-based lookup exists.
- The current unstaged retrieval implementation has a known FTS operator bug and
  is not stage-ready.
- Retrieval may need to change after current-fact raw snapshot, value-shape, and
  schema decisions are made.

## Completion Review Table

| PLAN item | Planned implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SQLite + FTS prose/search | Added an attempted in-memory SQLite FTS5 search over narrow public metadata snippets. Review found raw FTS operator handling is unsafe. | `src/sf6_knowledge_coach/retrieval.py`; `src/sf6_knowledge_coach/cli.py`; `tests/test_retrieval.py`; `tests/test_cli.py` | `PYTHONPATH=src python -m sf6_knowledge_coach.cli search "JP 5LP"`; review repro with `OR`/`AND`/`NOT` | Paused | None | Not stage-ready | FTS operator handling must be fixed when retrieval resumes |
| Structured numeric tables | Populated attempted structured current-fact table only from `official_raw.json`. | `retrieval.py`; `current_facts.py`; tests | Current lookup and answer prepare smoke | Paused | None | Needs value semantics/schema prerequisite | Inputless official rows require later identifier lookup |
| Alias dictionary | Loaded aliases from `data/aliases/` into queryable table; existing context resolver remains file-backed. | `retrieval.py`; `tests/test_retrieval.py` | Alias table tests | Paused | None | Table-driven tokenization not implemented | Alias coverage remains limited |
| Evidence filters | Added queryable source role, evidence basis, review status, patch sensitivity, character, and data source columns. | `retrieval.py`; tests | Metadata filter tests | Paused | None | CLI exposure remains minimal | CLI exposure remains undecided |
| Deterministic numeric answers | Kept attempted numeric answers grounded in structured current-fact lookup and added verification guard for source role/data source. | `answering.py`; `current_facts.py`; tests | Answer verify smoke and unittest | Paused | None | Needs current-fact schema/value semantics | Boundary must remain covered by later tests |
| Public/private boundary | Daily mode still reads public data and does not write generated DB files; answer log behavior remains Git-outside only. | `README.md`; tests | Unit tests and clean-slate validator | Pass | None | Private vault not implemented | Later private overlay needs separate ExecPlan |
