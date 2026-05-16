# SF6 Calculation Executor

This package contains a repo-owned deterministic calculation executor for
maintainer workflows.

The executor exists to reduce LLM arithmetic errors. It is not SF6 authority,
formula authority, rounding authority, current-fact authority, or public answer
behavior.

Use it only with explicit JSON inputs and audited authority boundaries from
`contracts/calculation-executor-trace.md`.

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

## Authority boundary

The executor must not look up or infer current facts. It does not read
`data/exports/`, `data/roster/`, generated frame-current assets, generated
references, web pages, Hermes state, or local skill memory.

Trace output always keeps `accepted_current_fact_authority: false`.
