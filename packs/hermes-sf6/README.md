# Hermes SF6 Pack

This pack is repo-local orchestration support for Hermes.

Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available. Hermes is not a canonical knowledge surface, not canonical memory, and not required for public distribution. Hermes state is non-canonical. This pack is not public answer behavior and does not replace skills/sf6-agent. Canonical maintainer procedures live in [workflows](../../workflows/). Public agent behavior lives in the single `sf6-agent` adapter.

When Hermes is unavailable, Codex, humans, or other agents may still follow the same canonical workflows as fallback executors.

## Contents

- `hermes.example.json`: example harness configuration shape.
- `prompts/`: boundary guidance for future prompt wrappers.
- `profiles/`: markdown profile guidance only; not executable profile config.
- `guards/`: boundary guidance for future guard checks.
- `reports/`: boundary guidance for future report templates.

## Rules

- Hermes wrappers must follow canonical workflows and canonical contracts.
- Operational prompt bodies belong to later work after answer contracts and evidence gate policy.
- Reusable output must be committed as repo artifacts, not stored in Hermes state.
- Do not commit Hermes memory state.
- Do not commit cron state.
- Do not commit secrets.
- Do not commit user session state.
- Keep generated or local Hermes runtime files outside this pack.

## Usage

Install or build the `sf6-agent` adapter using the canonical distribution docs under [docs/distribution/agents](../../docs/distribution/agents/). Use this pack only to point Hermes at the adapter and at [workflows](../../workflows/) for repo-local orchestration tasks.
