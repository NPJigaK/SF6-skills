# Calculation Executor Boundary Pointer

This pointer is repo-local maintainer support only. It does not define public
`sf6-agent` answer behavior and does not define SF6 formula authority.

Canonical calculation boundaries live in:

- `contracts/calculation-executor-trace.md`
- `contracts/calculation-trace.schema.json`
- `contracts/calculation-backend-handoff.schema.json`
- `workflows/calculation-backend-handoff.md`
- `packages/calculation-executor/README.md`
- `tests/validation/validate-calculation-executor.ps1`
- `tests/validation/validate-calculation-backend-handoff.ps1`

Use this pack note only to remember the boundary:

- calculation executors are trace generators only;
- executor output is not SF6 authority, formula authority, rounding authority,
  or current-fact authority;
- exact SF6 values, formulas, and rounding rules are not repo authority;
- backend instructions and traces must stay review-only or hold unless a
  separate accepted authority path exists;
- do not use calculation output to change public `sf6-agent` behavior.

Command examples and executable behavior belong to the package README, tests,
and validators, not to this pack.
