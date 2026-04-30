# Hermes SF6 Pack

This pack is optional maintainer harness guidance for Hermes.

Hermes is not a canonical knowledge surface, not canonical memory, and not required for public distribution. Canonical maintainer procedures live in [workflows](../../workflows/). Public agent behavior lives in the single `sf6-agent` adapter.

## Contents

- `hermes.example.json`: example harness configuration shape.

## Rules

- Do not commit Hermes memory state.
- Do not commit cron state.
- Do not commit secrets.
- Do not commit user session state.
- Keep generated or local Hermes runtime files outside this pack.

## Usage

Install or build the `sf6-agent` adapter using the canonical distribution docs under [docs/distribution/agents](../../docs/distribution/agents/). Use this pack only to point Hermes at the adapter and at [workflows](../../workflows/) for maintainer tasks.
