# Answer Smoke Run Template

This file is a template, not an executed smoke report.

It does not represent live Hermes execution. It does not represent live web research.
It is for recording future contract-level or fixture-level answer smoke runs
after the fixture set and validators are selected.

## Fixture Set

- Fixture directory:
- Fixture revision or PR:
- Covered modes:
- Japanese normalization fixture:

## Validators Run

- `tests/validation/validate-answer-smoke-fixtures.ps1`:
- `tests/validation/run-all.ps1`:
- `git diff --check`:
- `git diff --check origin/main...HEAD`:

## Warnings

- Windows PowerShell git visibility warnings:
- Generated-surface warnings:
- Authority-boundary warnings:

## Unresolved Items

- TBD

## Generated-Surface Status

Record whether these surfaces had residual unintended diff after validation:

- `skills/sf6-agent/references/`:
- `.dist`:
- `skills/sf6-agent/assets/frame-current/`:
- `runtime/normalization/`:
- `skills/sf6-agent/assets/normalization/`:

## Intentionally Not Done

- No live Hermes execution.
- No live web research.
- No operational answer prompt body changes.
- No public `sf6-agent` behavior changes.
