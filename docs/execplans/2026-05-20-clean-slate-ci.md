# Clean-Slate CI Restoration

Status: Remote verification complete; draft PR open and not merged.

## Purpose

Plan the minimal CI surface for the clean-slate SF6 Knowledge Coach scaffold
after commit `5a2ccb709b65a7e37ec6915e0c382eb49ee63e6d`.

This ExecPlan defines and records the small implementation slice that restores
CI without bringing back legacy workflows, legacy validators, or old runtime
behavior.

Remote verification was completed for draft PR #298 on commit
`07be2d391fb78db58c34c29c865ecdc433fd79e6`: the push CI run and the
pull_request CI run both passed.

## Scope

Included:

- Add one new workflow:
  `.github/workflows/ci.yml`.
- Update the clean-slate validator so it
  allows exactly `.github/workflows/ci.yml` while continuing to reject legacy
  `.github` content.
- Run on Python 3.12.
- Validate only the current clean-slate scaffold.
- Run the standard-library unit test suite:
  `PYTHONPATH=src python -m unittest discover -s tests`.
- Run the clean-slate validator:
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`.
- Run the current-fact CLI smoke:
  `PYTHONPATH=src python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"`.
- Include a whitespace check equivalent to `git diff --check`.
- Preserve privacy/log boundary expectations:
  answer logs must not be written inside the Git repository.
- Keep jobs free of application-level network access.

Excluded:

- Do not restore legacy `.github` workflows.
- Do not restore legacy validators.
- Do not allow any `.github` content except `.github/workflows/ci.yml`.
- Do not add runtime features.
- Do not add Discord, VLM, private vault, private overlay DB, video pipeline,
  web mode, or API runtime.
- Do not add package dependencies or dependency installation steps.
- Do not upload answer logs, local artifacts, private data, or generated
  runtime state as CI artifacts.
- Do not add matrix expansion beyond Python 3.12 in this slice.

## Acceptance Criteria

- The implementation adds exactly one minimal workflow:
  `.github/workflows/ci.yml`.
- The implementation updates `tests/validation/validate_clean_slate.py`
  so `.github/workflows/ci.yml` is permitted, while any other `.github` file or
  directory remains a validation failure.
- The workflow uses Python 3.12.
- The workflow checks out the repository and runs only the approved local
  validation commands for the current scaffold.
- The workflow does not install third-party Python dependencies.
- The workflow does not call external SF6 data sources, web search, APIs,
  Discord, VLM runners, or private vault locations.
- The workflow does not set `SF6_COACH_LOG_DIR` to a repository-internal path
  except inside tests that assert such paths are rejected before writes.
- CI fails if the unit tests, clean-slate validator, current-fact CLI smoke, or
  whitespace check fails.
- CI remains scoped to the clean-slate scaffold and does not recreate removed
  legacy behavior.

## Files / Interfaces

Planning and progress record:

- `docs/execplans/2026-05-20-clean-slate-ci.md`

Implementation changes:

- `.github/workflows/ci.yml`
- `tests/validation/validate_clean_slate.py`

CI command interface:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
if [ -n "${GITHUB_BASE_REF:-}" ]; then
  git diff --check "origin/${GITHUB_BASE_REF}...HEAD"
else
  git diff-tree --check --no-commit-id --root -r HEAD
fi
```

Local pre-finalization validation may continue to use:

```bash
git diff --check
git diff --cached --check
```

The CI whitespace check is PR-range-oriented when running for a pull request.
It should use `git diff --check "origin/${GITHUB_BASE_REF}...HEAD"` after a
checkout with enough history to resolve the base branch. For push or manual
runs without `GITHUB_BASE_REF`, it falls back to the HEAD commit/tree check
`git diff-tree --check --no-commit-id --root -r HEAD`. The implementation step
must verify both command paths where practical before treating the workflow as
complete.

## Validation Commands

Run from the repository root for this planning-only step:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Implementation validation must run from the repository root:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
PYTHONPATH=src python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
git diff --check
git diff --cached --check
if [ -n "${GITHUB_BASE_REF:-}" ]; then
  git diff --check "origin/${GITHUB_BASE_REF}...HEAD"
else
  git diff-tree --check --no-commit-id --root -r HEAD
fi
git status --short --branch
```

Remote verification:

- Draft PR: `https://github.com/NPJigaK/SF6-skills/pull/298`
- Commit: `07be2d391fb78db58c34c29c865ecdc433fd79e6`
- Push CI run: `https://github.com/NPJigaK/SF6-skills/actions/runs/26156989969`
- Pull request CI run: `https://github.com/NPJigaK/SF6-skills/actions/runs/26157030962`

## Progress

- [x] (2026-05-20 JST) Verified baseline branch and repository state before
  drafting.
- [x] (2026-05-20 JST) Reviewed `AGENTS.md`, `docs/PLAN.md`, and the existing
  clean-slate scaffold ExecPlan.
- [x] (2026-05-20 JST) Drafted the minimal CI restoration ExecPlan.
- [x] (2026-05-20 JST) Ran planning-step validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [x] (2026-05-20 JST) Corrected the ExecPlan after review: future CI
  implementation must update `tests/validation/validate_clean_slate.py` to
  allow only `.github/workflows/ci.yml`, and the whitespace check is now
  PR-range-oriented with a HEAD fallback.
- [x] (2026-05-20 JST) Ran post-correction planning validation:
  `git diff --check`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`, and
  `git status --short --branch`.
- [x] (2026-05-20 JST) Implemented `.github/workflows/ci.yml` with Python
  3.12, unittest, clean-slate validator, current-fact CLI smoke, and whitespace
  check.
- [x] (2026-05-20 JST) Updated `tests/validation/validate_clean_slate.py` to
  permit only `.github/workflows/ci.yml` under `.github`.
- [x] (2026-05-20 JST) Ran implementation validation:
  `PYTHONPATH=src python -m unittest discover -s tests`,
  `PYTHONPATH=src python tests/validation/validate_clean_slate.py`,
  current-fact CLI smoke, `git diff --check`, `git diff --cached --check`, and
  `git status --short --branch`.
- [x] (2026-05-20 JST) Updated mandatory review table for the implemented
  scope.
- [x] (2026-05-20 JST) Mandatory review completed with no actionable findings.
- [x] (2026-05-20 JST) Pushed branch
  `redesign/sf6-knowledge-coach-clean-slate` and opened draft PR #298.
- [x] (2026-05-20 JST) Observed GitHub Actions push CI run pass for commit
  `07be2d391fb78db58c34c29c865ecdc433fd79e6`.
- [x] (2026-05-20 JST) Observed GitHub Actions pull_request CI run pass for
  commit `07be2d391fb78db58c34c29c865ecdc433fd79e6`.
- [x] (2026-05-20 JST) Confirmed the PR-range whitespace behavior through the
  passing pull_request CI run.

## Decision Log

- Decision: Restore CI through a new clean-slate workflow instead of recovering
  legacy `.github` content.
  Rationale: The maintainer confirmed this repository is being rebuilt as a new
  app and legacy implementation should not be restored by default.
  Date/Author: 2026-05-20 / Codex

- Decision: Use Python 3.12 as the only CI Python target for this slice.
  Rationale: The prompt requires Python 3.12 validation and the scaffold is
  standard-library-only, so a matrix would add noise without increasing current
  coverage.
  Date/Author: 2026-05-20 / Codex

- Decision: Avoid `pip install` in the initial CI workflow.
  Rationale: The current package and tests use only the Python standard
  library, so dependency bootstrapping is unnecessary and would create extra
  network dependency.
  Date/Author: 2026-05-20 / Codex

- Decision: Keep `git diff --check` as local validation and use
  `git diff-tree --check --no-commit-id --root -r HEAD` only as the non-PR CI
  fallback.
  Rationale: `git diff --check` is useful before finalizing local changes, but
  a clean CI checkout normally has no working-tree diff. The commit-tree check
  is still useful for push or manual runs where no pull-request base branch is
  available.
  Date/Author: 2026-05-20 / Codex

- Decision: Use a PR-range whitespace check when pull-request base context is
  available, with a HEAD commit/tree fallback for push or manual runs.
  Rationale: The earlier HEAD-only plan was too narrow for multi-commit pull
  requests. `git diff --check "origin/${GITHUB_BASE_REF}...HEAD"` checks the PR
  range, while the HEAD fallback keeps non-PR runs deterministic.
  Date/Author: 2026-05-20 / Codex

- Decision: Include a minimal clean-slate validator update in the CI
  implementation slice.
  Rationale: The current validator rejects `.github` as a legacy directory.
  Adding `.github/workflows/ci.yml` without updating the validator would make
  the planned CI fail immediately. The validator must allow only the new
  clean-slate CI file and continue rejecting restored legacy `.github` content.
  Date/Author: 2026-05-20 / Codex

- Decision: Allow only GitHub Actions platform bootstrap network use.
  Rationale: `actions/checkout` and `actions/setup-python` are the minimal
  platform mechanisms for hosted CI. The validation commands themselves must
  not use web access, APIs, package registries, Discord, VLM, private vaults, or
  external SF6 data sources.
  Date/Author: 2026-05-20 / Codex

- Decision: Use an explicit `git fetch` for the pull-request whitespace check.
  Rationale: Even with `actions/checkout` configured with `fetch-depth: 0`, the
  workflow should make `origin/${GITHUB_BASE_REF}` unambiguous before running
  the PR-range check.
  Date/Author: 2026-05-20 / Codex

- Decision: Keep PR #298 draft and unmerged after remote CI verification.
  Rationale: The requested step was remote verification only. Marking ready or
  merging should be a separate maintainer decision.
  Date/Author: 2026-05-20 / Codex

## Deviations

- None.

## Risks

- The PR-range whitespace check was observed passing for commit
  `07be2d391fb78db58c34c29c865ecdc433fd79e6` in PR #298. Future workflow
  changes should keep enough checkout history to resolve
  `origin/${GITHUB_BASE_REF}`.
- The push/manual fallback remains HEAD commit/tree-oriented and does not check
  a whole branch range. This is intentional for non-PR runs.
- The validator update is intentionally narrow. It allows exactly
  `.github/workflows/ci.yml`; any other restored `.github` content should still
  fail validation.
- GitHub-hosted CI inherently depends on GitHub Actions infrastructure and
  action download/cache behavior. This is platform bootstrap network use, not
  application runtime network access.
- Future dependency additions will require a separate ExecPlan for package
  installation, lock strategy, and CI cache policy.
- The scaffold currently has no private vault, overlay DB, Discord, VLM, video
  pipeline, web mode, or API runtime by design; CI must not imply those are
  implemented.
- PR #298 remains draft and unmerged by design.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ExecPlan governance | Created and updated a scoped CI restoration plan; implementation stayed within the approved file set. Mandatory review completed with no actionable findings. | `docs/execplans/2026-05-20-clean-slate-ci.md` | `git diff --check`; `git status --short --branch`; review of PR #298 | Pass | None | PR remains draft and unmerged | None known |
| Minimal validation surface | Added Python 3.12 CI running unittest, clean-slate validator, current-fact CLI smoke, and PR-range-oriented whitespace check with HEAD fallback. Push and pull_request CI runs passed for commit `07be2d391fb78db58c34c29c865ecdc433fd79e6`. | `.github/workflows/ci.yml`; `tests/validation/validate_clean_slate.py` | `PYTHONPATH=src python -m unittest discover -s tests`; `PYTHONPATH=src python tests/validation/validate_clean_slate.py`; current-fact CLI smoke; GitHub Actions push run; GitHub Actions pull_request run | Pass | None | None for current commit | Future workflow changes must preserve checkout behavior |
| Privacy/log boundary | CI does not set a repo-internal `SF6_COACH_LOG_DIR` and does not upload artifacts. Existing tests continue to cover repo-internal log rejection. | `.github/workflows/ci.yml` | `PYTHONPATH=src python -m unittest discover -s tests`; clean-slate validator | Pass | None | No additional CI artifact guard beyond absence of upload steps | Future CI additions must preserve this boundary |
| No legacy restore | Validator now allows only `.github/workflows/ci.yml` under `.github` and keeps all other legacy surfaces rejected. No legacy workflow or validator content was restored. | `.github/workflows/ci.yml`; `tests/validation/validate_clean_slate.py` | `PYTHONPATH=src python tests/validation/validate_clean_slate.py`; review of diff | Pass | None | None known | Accidental future `.github` additions should be caught by validator |
