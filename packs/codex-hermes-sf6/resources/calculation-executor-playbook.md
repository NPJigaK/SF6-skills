# Calculation Executor Playbook

This playbook is repo-local maintainer support only. It does not define public
`sf6-agent` answer behavior.

Use the deterministic executor when Hermes, Codex, or provider Codex needs to
avoid LLM arithmetic errors while preserving SF6 authority boundaries.

## Command

```bash
python packages/calculation-executor/sf6_calculation_executor.py \
  --input tests/fixtures/calculation-executor/hypothetical-addition.json \
  --pretty
```

## Required boundary

- The executor is a calculation executor and trace generator only.
- The executor output is not SF6 authority, formula authority, or current-fact
  authority.
- Hermes may request arithmetic, but provider Codex should run the repo-owned
  script rather than doing arithmetic in natural language.
- Codex must audit the trace against `contracts/calculation-executor-trace.md`
  and `contracts/calculation-trace.schema.json`.
- Missing input provenance, formula instruction, rounding instruction, route,
  or timing context must produce blocked or hold behavior.
- Do not use the executor to discover SF6 facts, infer formulas, scrape data, or
  make public answers.

## First-tranche use

Use the executor for generic arithmetic and hypothetical consistency checks
only. Do not encode combo damage, scaling tables, minimum guarantees, frame
advantage interpretation, punish-window logic, or meaty/oki timing rules until
a later reviewed backend-instruction policy exists.
