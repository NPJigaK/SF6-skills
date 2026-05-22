# Retire Legacy Alias Fixture

Status: Implementation complete; review pending.

## Purpose

Retire the old `data/aliases/` fixture as legacy app data. Keep only the
current lightweight fallback resolver until a new alias dictionary is designed.

## Scope

Change only PLAN/README wording, the alias fallback, tests, and clean-slate
validation. Do not add new alias data, retrieval behavior, schema/parser work,
or authority changes.

## Changes

- `docs/PLAN.md`: future alias dictionary remains planned, but no longer points
  at retired `data/aliases/`.
- `README.md`: removes stale retained-alias-surface wording.
- `src/sf6_knowledge_coach/aliases.py`: removes legacy JSON fixture loading and
  keeps fixture-free fallback resolution.
- `src/sf6_knowledge_coach/paths.py`: removes the now-unused alias fixture path.
- `tests/test_cli.py`: tests the JP block-advantage smoke path without alias
  fixture data.
- `tests/validation/validate_clean_slate.py`: stops requiring
  `data/aliases/ja-query-fixtures.json`.

## Validation

```bash
git diff --check
git diff --cached --check
PYTHONPATH=src uv run --locked python -m unittest tests.test_cli
PYTHONPATH=src uv run --locked python -m unittest discover -s tests
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
PYTHONPATH=src uv run --locked python -m sf6_knowledge_coach.cli answer prepare "JPの5LPはガードで何F？"
git status --short --branch
```

## Decision

Do not restore `data/aliases/`. The old fixture is data debt; future alias
coverage needs a clean-slate ExecPlan.

## Risks

- Japanese query normalization remains intentionally narrow until that future
  alias design lands.

PLAN deviations: none.
