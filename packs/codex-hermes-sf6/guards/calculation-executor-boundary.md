# Calculation Executor Boundary

This guard is a repo-local reminder only. Canonical authority remains in
`AGENTS.md`, `workflows/`, `docs/architecture/`, `contracts/`,
`tests/validation/`, and reviewed repo artifacts.

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

Use the canonical calculation contracts, backend handoff workflow, package
README, and validators for executable behavior.
