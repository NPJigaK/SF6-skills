# Hermes Profile Guidance

This directory is repo-local orchestration support for future Hermes profile guidance.
It is a thin pointer surface only.

Files here are not public answer behavior. This directory does not define public answer behavior. The former public adapter was removed after runtime relocation.

Hermes profile guidance must follow canonical workflows and canonical contracts. Reusable output must be committed as repo artifacts, not stored in Hermes state. This directory is not canonical procedure authority.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, secrets, and chat transcripts are non-canonical.

Profile files in this issue are markdown guidance only, not executable profile config. Do not add `.json` profile config unless a Hermes profile schema is explicitly defined.

## Maintainer Profile Expectations

Repo-local Hermes maintainer profiles should follow
`data/toolchain/maintainer-agent-toolchain.json` and
`docs/architecture/hermes-maintainer-profile-policy.md`.

Those canonical toolchain surfaces define the `gpt-5.5` / `codex 5.5` and
`xhigh` / extra-high expectations for SF6 maintainer work. Local checks such
as `hermes --version`, `hermes doctor`, and `hermes profile list` are local
review signals only, not CI requirements. Do not commit the observed local
profile state or command output.

Validator anchor: local review signals only.

Hermes CLI version freshness is primarily managed through the root `flake.nix`,
the reviewed `flake.lock` pin, and Renovate Nix flake PRs. The repo records
policy and command expectations, not local installed versions or profile
snapshots.

Profile skill selection should also follow the repo-managed policy in
`data/toolchain/maintainer-agent-toolchain.json`. The policy records expected
allowlisted, conditional, and forbidden skill categories for `sf6ingest`; it is
not a local Hermes skill export and does not commit enabled or disabled skill
state.
