# New App Scaffold For SF6 Knowledge Coach

Status: Approved by maintainer request in this turn; implemented as the first
clean-slate app slice.

## Purpose

Create the minimal new-app scaffold required to make `docs/PLAN.md` executable
after deleting the legacy implementation. This slice establishes a small
deterministic local CLI and validation baseline without restoring old runtime,
package, workflow, validator, or adapter code.

## Scope

Included:

- Add a Python package for `sf6-knowledge-coach`.
- Add a console command named `sf6`.
- Add deterministic tools for context resolution, current-fact lookup, simple
  search, answer preparation, answer verification, and optional append-only
  Git-outside answer logging.
- Use retained `data/aliases/` for query normalization support.
- Use retained `data/exports/` official raw exports for exact current facts.
- Add minimal standard-library tests and a clean-slate validator.
- Update README to describe the new app state.

Excluded:

- Do not restore legacy `contracts/`, `knowledge/`, `packages/`, `packs/`,
  `runtime/`, `skills/`, `tools/`, `workflows/`, or old validation scripts.
- Do not add Discord, VLM, private vault, private overlay DB, video pipeline, or
  API-backed answer runtime.
- Do not put private user data, logs, or local vault paths in the repository.
- Do not implement broad Phase 1 beyond a deterministic local vertical slice.

## Acceptance Criteria

- `docs/execplans/` exists with a reusable template.
- `PYTHONPATH=src python -m unittest discover -s tests` passes.
- `PYTHONPATH=src python tests/validation/validate_clean_slate.py` passes.
- Numeric/current-fact answers are prepared only from deterministic lookup
  evidence, not prose or model memory.
- The optional answer log writes only outside the Git repository.
- The CLI can resolve a query, look up a current fact, prepare an answer packet,
  and verify the prepared answer packet.

## Files / Interfaces

- `AGENTS.md`
- `docs/PLAN.md`
- broad staged deletion of legacy surfaces:
  - `.github/`
  - `contracts/`
  - `docs/architecture/`
  - `docs/testing/`
  - `evals/`
  - `flake.nix`
  - `flake.lock`
  - `ingest/`
  - `knowledge/`
  - `packages/`
  - `packs/`
  - `runtime/`
  - `skills/`
  - legacy `tests/fixtures/`
  - legacy `tests/validation/` PowerShell validators and manifest
  - `tools/agent-skills/`
  - `workflows/`
- `pyproject.toml`
- `README.md`
- `src/sf6_knowledge_coach/`
- `tests/test_cli.py`
- `tests/validation/validate_clean_slate.py`
- `docs/execplans/TEMPLATE.md`
- `docs/execplans/2026-05-20-new-app-scaffold.md`

Command interface:

```text
sf6 context resolve <query>
sf6 search <query>
sf6 current lookup --character <slug> --move <input> [--field <field>]
sf6 answer prepare <query> [--log]
sf6 answer verify <query>
```

`sf6 search` is intentionally a raw substring search over retained current-fact
records in this scaffold. It does not apply Japanese alias normalization or FTS
ranking yet. Use `sf6 context resolve`, `sf6 current lookup`, or
`sf6 answer prepare` for normalized current-fact flows in this slice.

## Validation Commands

Run from the repository root:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git diff --check
git diff --cached --check
git status --short --branch
```

## Progress

- [x] (2026-05-20 JST) Confirmed broad legacy deletion is intentional for a
  complete new-app rebuild.
- [x] (2026-05-20 JST) Added new-app ExecPlan template and this scaffold plan.
- [x] (2026-05-20 JST) Added minimal deterministic CLI and tests.
- [x] (2026-05-20 JST) Ran validation:
  `PYTHONPATH=src python -m unittest discover -s tests`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and CLI
  answer preparation smoke.
- [x] (2026-05-20 JST) Fixed scaffold review findings: answer logs are rejected
  before any repo-internal directory or file is created; ExecPlan boundary now
  describes the full staged clean-slate replacement; `sf6 search` limitation is
  documented.

## Decision Log

- Decision: Do not restore broad legacy directories.
  Rationale: The maintainer explicitly clarified that this repository is being
  reborn as a completely new app and that the broad deletion is appropriate.
  Date/Author: 2026-05-20 / Maintainer + Codex
- Decision: Use Python standard library only for the first scaffold.
  Rationale: It keeps the new app runnable without dependency bootstrapping
  while the clean-slate package and validation boundaries are still forming.
  Date/Author: 2026-05-20 / Codex
- Decision: Keep exact current-fact lookup grounded in `data/exports/*/official_raw.json`.
  Rationale: `docs/PLAN.md` requires deterministic tools/tables for frame,
  damage, scaling, punish, and current move facts.
  Date/Author: 2026-05-20 / Codex
- Decision: Keep `sf6 search` as raw substring search in this scaffold.
  Rationale: The current slice is only a deterministic local vertical slice.
  Adding normalized FTS/retrieval behavior would broaden Phase 1 beyond the
  approved minimal scaffold.
  Date/Author: 2026-05-20 / Codex

## Deviations

- None.

## Risks

- The CLI is a minimal vertical slice, not a complete Phase 1 runtime.
- Alias coverage is intentionally small and follows the retained seed data.
- `sf6 search` is raw substring search only and does not yet use alias
  normalization, FTS, or ranking.
- There is no CI after deleting `.github/`; a later ExecPlan should add a new
  clean-slate CI workflow.
- Private vault and overlay DB behavior remains unimplemented by design.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Clean-slate replacement boundary | Replaced the legacy repo shape with a new app scaffold while retaining public seed `data/`. | `AGENTS.md`; `docs/PLAN.md`; `README.md`; broad deletion of `.github/`, `contracts/`, `docs/architecture/`, `docs/testing/`, `evals/`, `flake.*`, `ingest/`, `knowledge/`, `packages/`, `packs/`, `runtime/`, `skills/`, legacy `tests/`, `tools/agent-skills/`, and `workflows/` | `git diff --cached --check`; `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | CI not restored | Broad deletion intentionally removes legacy guardrails |
| ExecPlan governance | Added template and this scoped scaffold ExecPlan. | `docs/execplans/TEMPLATE.md`; `docs/execplans/2026-05-20-new-app-scaffold.md` | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | Review pending | Template may need refinement as later phases grow |
| Deterministic local tools | Added context resolution, search, current lookup, answer prepare, and answer verify CLI paths. | `src/sf6_knowledge_coach/*`; `pyproject.toml` | `PYTHONPATH=src python -m unittest discover -s tests` | Pass | None | Private overlay not included | Minimal query parsing only |
| New validation baseline | Added clean-slate validator and unit tests. | `tests/test_cli.py`; `tests/validation/validate_clean_slate.py` | `PYTHONPATH=src python -m unittest discover -s tests`; `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | CI not restored | Local-only validation until new CI exists |
| Answer log privacy boundary | Validate the resolved log path before creating directories or writing `answer-log.jsonl`. | `src/sf6_knowledge_coach/answering.py`; `tests/test_cli.py` | `PYTHONPATH=src python -m unittest discover -s tests` | Pass | None | None | Default external log location still depends on host environment |
