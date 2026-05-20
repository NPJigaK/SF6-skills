# ExecPlan Template

Status: Draft

## Purpose

State the concrete outcome this ExecPlan will deliver.

## Scope

Included:

- List the work that is explicitly in scope.

Excluded:

- List adjacent work that must not be implemented here.

## Acceptance Criteria

- Describe observable completion criteria.

## Files / Interfaces

- List files, commands, schemas, data surfaces, and public interfaces touched.

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

- [ ] Draft ExecPlan.
- [ ] Implement scoped changes.
- [ ] Run validation.
- [ ] Complete review table.

## Decision Log

- Decision:
  Rationale:
  Date/Author:

## Deviations

- None.

## Risks

- List remaining risks and mitigations.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
