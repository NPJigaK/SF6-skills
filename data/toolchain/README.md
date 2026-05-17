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

Hermes maintainer profile expectations may also include repo-managed skill
selection policy for `sf6ingest`. That policy narrows expected built-in skill
use for repo-local maintainer work, but it is not installed skill state, local
skill configuration, or an exported Hermes profile.

`hermes-maintainer-skill-allowlist.json` is the machine-readable allowlist
policy for the private `sf6ingest` profile. It separates built-in default
skills, built-in conditional skills, external APM-managed skills, deferred
candidates, and forbidden categories. It is policy data only; it is not local
Hermes profile state, an installed skill list, or public `sf6-agent`
distribution metadata.
