# Hermes Profile Guidance

This directory is repo-local orchestration support for future Hermes profile guidance.

Files here are not public answer behavior. This directory does not replace skills/sf6-agent. Public SF6 answer behavior remains in the single `skills/sf6-agent/` adapter.

Hermes profile guidance must follow canonical workflows and canonical contracts. Reusable output must be committed as repo artifacts, not stored in Hermes state.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, secrets, and chat transcripts are non-canonical.

Profile files in this issue are markdown guidance only, not executable profile config. Do not add `.json` profile config unless a Hermes profile schema is explicitly defined.
