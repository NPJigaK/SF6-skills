# Maintainer Agent Toolchain Policy Data

`data/toolchain/` is canonical maintainer-toolchain policy data.

It is not SF6 gameplay knowledge. It is not exact current-fact authority.
Exact current facts remain grounded in `data/exports/` and `data/roster/`.

This directory must not contain local installed versions, local configs,
credentials, sessions, caches, logs, tokens, or secrets. It must not be used to
require Codex CLI or Hermes CLI for public `sf6-agent` users.

The policy files in this directory record reviewed expectations and
required/planned maintainer capabilities, not local machine state.

Hermes maintainer profile expectations may include required model and
reasoning-effort policy for repo-local maintainer workflows. Those expectations
are not exported Hermes profile config and are not evidence that a local
machine currently matches the policy.
