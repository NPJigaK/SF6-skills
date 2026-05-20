# Phase 1 Retrieval Contract

Status: Draft; planning-only, not implemented.

## Purpose

Plan the smallest Phase 1 implementation slice that moves the clean-slate
scaffold toward the retrieval contract in `docs/PLAN.md` without broad runtime
work.

This ExecPlan does not implement database, CLI, private vault, Discord, VLM,
web, API, or vector-search behavior. It defines the next implementation slice
only.

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

Expected implementation files:

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
- [ ] Review and approve the next implementation prompt before code changes.

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

## Deviations

- None.

## Unresolved Decisions

- Whether a later slice should create a persisted generated public SQLite DB,
  and if so whether it belongs in Git, GitHub release artifacts, or a Git-outside
  local cache.
- Whether future reviewed prose knowledge should live under a new `knowledge/`
  surface or another public source path after the clean-slate deletion.
- How much metadata filtering should be exposed through CLI flags versus kept
  internal to answer preparation.
- Whether alias normalization should remain query-substring based or become a
  table-driven tokenization pass.

## Risks

- In-memory DB construction may become slow as public data grows. This is
  acceptable for the next slice but should be measured before broader use.
- FTS5 availability must be verified in CI, even though it works locally.
- Current `data/aliases/` seed coverage is small, so query normalization will
  remain limited.
- Search result ranking will be minimal in this slice.
- The slice does not yet provide complete Phase 1 public knowledge retrieval;
  it only establishes the retrieval contract boundary.

## Completion Review Table

| PLAN item | Planned implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SQLite + FTS prose/search | Add in-memory SQLite FTS5 search over narrow public text snippets. | Future `src/sf6_knowledge_coach/retrieval.py`; `src/sf6_knowledge_coach/cli.py`; tests | Future `sf6 search` smoke and unittest | Pending | None | Not implemented in this planning step | FTS ranking and corpus are intentionally small |
| Structured numeric tables | Populate structured current-fact tables only from `official_raw.json`. | Future `retrieval.py`; `current_facts.py`; tests | Future current lookup and answer prepare smoke | Pending | None | Not implemented in this planning step | Must not accidentally use sidecars/manual review |
| Alias dictionary | Load aliases from `data/aliases/` into queryable table/context resolution path. | Future `retrieval.py`; `aliases.py`; tests | Future context/search tests | Pending | None | Not implemented in this planning step | Alias coverage remains limited |
| Evidence filters | Add filter columns for source role, evidence basis, review status, patch sensitivity, character, and data source. | Future `retrieval.py`; tests | Future metadata filter tests | Pending | None | Not implemented in this planning step | CLI exposure remains undecided |
| Deterministic numeric answers | Keep numeric answers grounded in structured current-fact lookup, never FTS or model memory. | Future `answering.py`; `current_facts.py`; tests | Future answer verify smoke | Pending | None | Not implemented in this planning step | Boundary must remain covered by tests |
| Public/private boundary | Keep daily mode read-only for repo data and keep answer logs Git-outside only. | Future tests only unless code needs boundary wiring | Unit tests and clean-slate validator | Pending | None | Private vault not implemented | Later private overlay needs separate ExecPlan |
