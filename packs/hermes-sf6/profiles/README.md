# Hermes Profile Guidance

This directory is repo-local orchestration support for future Hermes profile guidance.

Files here are not public answer behavior. This directory does not replace skills/sf6-agent. Public SF6 answer behavior remains in the single `skills/sf6-agent/` adapter.

Hermes profile guidance must follow canonical workflows and canonical contracts. Reusable output must be committed as repo artifacts, not stored in Hermes state.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, secrets, and chat transcripts are non-canonical.

Profile files in this issue are markdown guidance only, not executable profile config. Do not add `.json` profile config unless a Hermes profile schema is explicitly defined.

## Maintainer Profile Expectations

Repo-local Hermes maintainer profiles should follow
`data/toolchain/maintainer-agent-toolchain.json` and
`docs/architecture/hermes-maintainer-profile-policy.md`.

For SF6 maintainer work, profiles are expected to use `gpt-5.5` / `codex 5.5`
with `xhigh` / extra-high reasoning where the provider and Hermes CLI expose
that setting. If a profile listing does not show reasoning effort, verify it
manually outside the repo and do not commit the observed local profile state or
command output.

Hermes CLI version freshness is primarily managed through the root `flake.nix`,
the reviewed `flake.lock` pin, and Renovate Nix flake PRs.
Fallback checks such as `hermes --version`, `hermes doctor`, and
`hermes profile list` are local review signals only. The repo records policy
and command expectations, not local installed versions or profile snapshots.
