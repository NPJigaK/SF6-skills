# SF6 Calculation Executor

Package classification: `active_repo_local`.

This package contains a repo-owned deterministic arithmetic trace compatibility
helper for maintainer workflows.

The executor exists to reduce LLM arithmetic errors. It is not SF6 authority,
formula authority, rounding authority, current-fact authority, or public answer
behavior.

SymPy is the initial default maintainer-local symbolic math backend dependency
for calculation execution. It is pinned package-locally in `pyproject.toml` and
`uv.lock` so dependency updates are reviewable.

Use it only with explicit JSON inputs and the non-authority boundaries from
`contracts/calculation-executor-trace.md`. Do not extend it into a custom SF6
math engine. If SF6-specific calculation is needed, prefer a reviewed external
CAS / symbolic math backend and keep this package as a thin trace helper unless
a later architecture decision retires it.

## Run

```bash
python packages/calculation-executor/sf6_calculation_executor.py \
  --input tests/fixtures/calculation-executor/hypothetical-addition.json \
  --pretty
```

The script reads a JSON request and writes a calculation trace JSON object to
stdout.

## First-tranche scope

Supported operations are generic arithmetic only:

- `add`
- `subtract`
- `multiply`
- `divide`
- `sum`
- `min`
- `max`
- `difference`
- `compare`
- `percent_of`

The executor does not implement SF6 combo damage formulas, scaling tables,
minimum guarantees, frame advantage interpretation, punish-window logic,
meaty/oki timing, resource formulas, or SF6 rounding rules.

The SymPy dependency is not SF6 combo damage formula authority. It also does
not add scaling tables, minimum guarantees, frame interpretation, punish logic,
oki timing, resource formulas, SF6 rounding rules, current-system exceptions,
or public answer behavior.

## Authority boundary

The executor must not look up or infer current facts. It does not read
`data/exports/`, `data/roster/`, generated frame-current assets, generated
references, web pages, Hermes state, or local skill memory.

Trace output always keeps `accepted_current_fact_authority: false`.
