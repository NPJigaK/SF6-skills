# Calculation Executor Boundary

Calculation tools are executors only.

They must not:

- become SF6 authority;
- become formula authority;
- become rounding authority;
- become current-fact authority;
- override `data/exports`, `data/roster`, or packaged `official_raw`;
- promote review-only claims, current-fact candidates, video observations,
  combo fixtures, smoke reports, or Hermes output;
- feed generated references by default;
- change public `sf6-agent` behavior.

Use `packages/calculation-executor/sf6_calculation_executor.py` for deterministic
arithmetic traces and keep `accepted_current_fact_authority: false`.
