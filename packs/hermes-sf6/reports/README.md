# Hermes Report Guidance

This directory is repo-local orchestration support for future Hermes report guidance.

Files here are not public answer behavior. This directory does not replace skills/sf6-agent. Public SF6 answer behavior remains in the single `skills/sf6-agent/` adapter.

Hermes report guidance must follow canonical workflows and canonical contracts. Reusable output must be committed as repo artifacts, not stored in Hermes state.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, secrets, and chat transcripts are non-canonical.

Reports produced by Hermes-assisted workflows must be committed as repo artifacts in the canonical destination for that workflow. This directory does not define operational prompt bodies. Operational prompt bodies belong to later work after answer contracts and evidence gate policy.
