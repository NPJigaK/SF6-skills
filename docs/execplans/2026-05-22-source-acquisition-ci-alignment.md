# Source Acquisition CI Alignment

Status: Draft; planning-only, not implemented.

## Purpose

Plan a focused CI update after PR #305 so GitHub Actions validates the new
source-acquisition dependency and public report checks without running live web
acquisition.

PR #305 established reproducible current-source acquisition for official and
SuperCombo sources, but the existing CI still runs the older clean-slate
validation surface. This ExecPlan defines the smallest CI alignment slice that
checks the lockfile, verifies Scrapling can be imported, and validates the
committed public acquisition report while preserving the public/private and
authority boundaries from `docs/PLAN.md`.

## Scope

Included:

- Update the clean-slate CI workflow to install and use `uv`.
- Keep Python 3.12 as the only CI Python target.
- Run `uv lock --check` in CI.
- Run a Scrapling import check in CI:

  ```bash
  python -c "from scrapling.fetchers import Fetcher, StealthyFetcher; print(Fetcher.__name__, StealthyFetcher.__name__)"
  ```

- Run existing unit tests through the locked project environment.
- Run the clean-slate validator through the locked project environment.
- Run the current-fact CLI smoke through the locked project environment.
- Run public acquisition report validation:

  ```bash
  python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
  ```

- Keep the existing PR-range whitespace check behavior.
- Distinguish dependency/import validation from live acquisition.
- Keep CI free of source scraping, anti-bot bypass, browser screenshots,
  private/local artifact uploads, and data authority promotion.

Excluded:

- Do not run live official acquisition in CI.
- Do not run live SuperCombo acquisition in CI.
- Do not use `solve_cloudflare=True` in CI.
- Do not run browser/Patchright/Playwright/Scrapling visual observation in CI.
- Do not run `.local` artifact validation in CI, because the required raw
  artifacts are intentionally ignored and not committed.
- Do not generate `.local` source artifacts in CI.
- Do not upload CI artifacts.
- Do not commit `.local/`, `.venv/`, `.agents/`, screenshots, raw HTML, raw
  rows, cookies, browser profiles, traces, or debug dumps.
- Do not modify runtime, schema, parser, retrieval, answer behavior,
  authority status, Discord, VLM, API fallback, vector search, private vault,
  persistent DB, or `sf6 ask`.
- Do not broaden CI beyond source-acquisition dependency/report alignment.

## Acceptance Criteria

- CI installs or enables `uv` in a minimal, reviewed way.
- CI uses Python 3.12 only.
- CI runs `uv lock --check`.
- CI verifies both `Fetcher` and `StealthyFetcher` can be imported from
  Scrapling.
- CI runs unit tests, clean-slate validation, current-fact CLI smoke, public
  acquisition report validation, and whitespace checks.
- CI does not run live web acquisition or source scraping.
- CI does not use `solve_cloudflare=True`.
- CI does not require ignored `.local` artifacts.
- CI does not create, upload, or commit raw HTML, raw rows, screenshots,
  cookies, browser profiles, traces, debug dumps, answer logs, training logs,
  or private user data.
- CI does not promote official data to `current_fact_authority`.
- CI does not promote SuperCombo beyond enrichment, cross-reference, or
  candidate evidence.
- Daily-answer authority remains unchanged.
- No schema, parser, retrieval, or answer behavior changes are introduced.

## Files / Interfaces

Planning file:

- `docs/execplans/2026-05-22-source-acquisition-ci-alignment.md`

Expected implementation file:

- `.github/workflows/ci.yml`

No runtime, schema, parser, retrieval, answer, validator, or data artifact file
changes are planned. If implementation discovers that another file is required,
the implementer must update the Decision Log and stop for review before
editing it.

Planned CI command surface:

```bash
uv lock --check
PYTHONPATH=src uv run --locked python -c "from scrapling.fetchers import Fetcher, StealthyFetcher; print(Fetcher.__name__, StealthyFetcher.__name__)"
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
```

The existing whitespace check should remain PR-range-oriented for pull
requests, with the current HEAD fallback for push or manual runs:

```bash
if [ -n "${GITHUB_BASE_REF:-}" ]; then
  git fetch --no-tags origin "+refs/heads/${GITHUB_BASE_REF}:refs/remotes/origin/${GITHUB_BASE_REF}"
  git diff --check "origin/${GITHUB_BASE_REF}...HEAD"
else
  git diff-tree --check --no-commit-id --root -r HEAD
fi
```

## CI Artifact Boundary

`validate-artifacts` is intentionally excluded from CI for this slice.

Rationale:

- The raw source artifacts live under ignored `.local/source-acquisition/`.
- Those artifacts include raw HTML and raw row data that must not be committed
  or uploaded.
- Regenerating them in CI would require live official/SuperCombo acquisition
  and, for SuperCombo, anti-bot bypass behavior that is explicitly outside CI.
- The public report can be validated deterministically without exposing or
  regenerating raw artifacts.

Local/reviewer validation remains responsible for artifact integrity checks
when the ignored `.local` artifacts are present:

```bash
PYTHONPATH=src python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
```

## Validation Commands

Run from the repository root for this planning-only step:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Future implementation validation must run from the repository root:

```bash
uv lock --check
PYTHONPATH=src uv run --locked python -c "from scrapling.fetchers import Fetcher, StealthyFetcher; print(Fetcher.__name__, StealthyFetcher.__name__)"
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
git diff --check
git diff --cached --check
git status --short --branch
```

Remote verification after implementation must observe both push and
pull_request CI passing before PR readiness.

## Progress

- [x] (2026-05-22 JST) Started from updated `main` at
  `67bd6a8c5bb2672012be864d94e597600694ef75`.
- [x] (2026-05-22 JST) Created branch
  `plan/source-acquisition-ci-alignment`.
- [x] (2026-05-22 JST) Reviewed `AGENTS.md`, `docs/PLAN.md`, the clean-slate
  CI ExecPlan, current CI workflow, and the current-source acquisition
  ExecPlan.
- [x] (2026-05-22 JST) Drafted this planning-only ExecPlan.
- [x] (2026-05-22 JST) Ran planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [ ] Complete mandatory review.
- [ ] Implement CI alignment in a separate implementation step after approval.

## Decision Log

- Decision: CI should validate the Scrapling dependency through `uv lock
  --check` and a direct Scrapling import check.
  Rationale: PR #305 added a runtime dependency and source-acquisition module,
  but current CI does not prove the dependency can be installed or imported.
  Date/Author: 2026-05-22 / Codex

- Decision: CI should validate the public acquisition report but not the
  ignored `.local` artifact set.
  Rationale: The report is committed and deterministic. The `.local` artifacts
  are intentionally ignored, may include raw source material, and would require
  live acquisition to recreate in CI.
  Date/Author: 2026-05-22 / Codex

- Decision: Do not run live acquisition or `solve_cloudflare=True` in CI.
  Rationale: CI should check dependency/report integrity, not scrape live
  sources, bypass anti-bot pages, or perform reviewer-only browser
  observation.
  Date/Author: 2026-05-22 / Codex

- Decision: Keep this CI slice separate from schema, parser, retrieval, and
  answer behavior.
  Rationale: The current-source acquisition PR deliberately stopped before
  authority promotion and normalized schema design. CI alignment should not
  change that boundary.
  Date/Author: 2026-05-22 / Codex

## Unresolved Decisions

- The implementation must choose the exact `uv` setup mechanism for GitHub
  Actions and record it before editing the workflow. The preferred direction is
  a focused setup action or equivalent minimal bootstrap, but the final action
  reference should be reviewed during implementation.
- Whether to add dependency caching is deferred. The default for this slice is
  no explicit cache unless implementation review shows a clear need.

## Deviations

- None.

## Risks

- CI will still not prove that live official or SuperCombo acquisition works.
  This is intentional; live source acquisition remains a reviewer/update-mode
  activity, not a CI activity.
- CI will not run `validate-artifacts` unless a later ExecPlan introduces a
  safe, non-public, CI-local artifact generation strategy. Current policy keeps
  `.local` artifacts out of CI.
- The exact `uv` setup mechanism is not fixed by this planning step and must
  be selected carefully during implementation.
- Installing dependencies in CI introduces dependency-bootstrap network use.
  This must remain limited to CI environment setup and must not become daily
  answer web access or live source acquisition.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan source-acquisition CI alignment | Drafted this ExecPlan only | `docs/execplans/2026-05-22-source-acquisition-ci-alignment.md` | `git diff --check` | Pass | None | Implementation not started | Exact `uv` setup mechanism deferred |
| Preserve no-live-acquisition boundary | Planned CI report/dependency validation only | `docs/execplans/2026-05-22-source-acquisition-ci-alignment.md` | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | Implementation not started | CI will not prove live acquisition |
| Keep authority unchanged | Planned no schema/parser/retrieval/answer changes | `docs/execplans/2026-05-22-source-acquisition-ci-alignment.md` | Reviewer check | Pending mandatory review | None | Implementation not started | None |
