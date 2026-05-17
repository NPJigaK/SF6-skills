# Manage Maintainer Toolchain

## Purpose

Use this workflow to keep maintainer command-line tooling reproducible and
GitHub-reviewable.

This workflow covers repo-local maintainer tools only. It is not SF6 gameplay
knowledge, not exact current-fact authority, and not a public `sf6-agent`
runtime requirement.

## Canonical Files

- `mise.toml` defines the WSL/Linux maintainer tools used by this repo.
- `mise.lock` pins exact tool versions, URLs, and checksums where the backend
  supports them.
- `ingest/frame_data/pyproject.toml` defines the frame-data ingest Python
  package constraints.
- `ingest/frame_data/uv.lock` pins Python dependency resolution for the ingest
  package.
- `.github/renovate.json` defines dependency update PR behavior.
- `.github/workflows/renovate.yml` runs Renovate on a daily schedule and can
  also be started manually.
- `.github/workflows/v2-validation.yml` verifies locked installation and repo
  validation in CI.
- `flake.nix` declares the Hermes Agent flake input for repo-local maintainer
  workflows. `flake.lock` is the reviewed Hermes Agent input pin.

## Tool Boundary

The repo-level `mise.toml` intentionally manages these tools:

- Python and `uv` for ingest development and Python dependency locking.
- Node only as the package-manager runtime for the official npm backend used
  by Codex CLI.
- PowerShell Core as `powershell-core`, with `pwsh` as the expected command.
- GitHub CLI as `gh`.
- Codex CLI through `npm:@openai/codex`, matching the official npm install
  channel while still allowing mise to pin it.
- `yt-dlp` for maintainer media workflows.
- `ffmpeg` and `ffprobe` through `conda:ffmpeg`, declared explicitly so local
  asdf plugins or aliases cannot change the backend used by the lockfile.
- Git through `conda:git` for repo-local and CI pinning.

Git cannot be fully bootstrapped by this repo because a maintainer needs Git or
another checkout mechanism before `mise.toml` is available.

Hermes CLI is intentionally not declared in `mise.toml`. Hermes is the
repo-local growth engine when a configured maintainer profile is available.
Prefer the repo Nix flake for Hermes CLI pinning and Renovate updates. Keep
Hermes profile state outside the repository and promote only reviewed repo
artifacts into this repository.

## Local Setup

From WSL2 or another Linux environment with this repo already checked out:

```bash
mise install --locked
```

If the shell is not activated, either rely on mise shims or add mise activation
to the shell profile outside the repository.

For Python ingest dependencies:

```bash
cd ingest/frame_data
uv sync
```

## Updating Tools

Use Renovate for normal update PRs. Renovate is configured for mise, Nix
flakes, GitHub Actions, and Python dependency updates. The Renovate workflow is
separate from normal CI and runs once per day at 04:23 JST. It requires a
repository secret named `RENOVATE_TOKEN`; use a PAT or GitHub App token rather
than the default `GITHUB_TOKEN` so Renovate-created PRs can trigger the normal
validation workflows.

When Renovate updates `mise.toml`, it also runs the allowlisted
`.github/renovate-mise-lock.sh` post-upgrade task to regenerate
`mise.lock`. The workflow allows only that exact post-upgrade command.

For a manual tool update:

```bash
mise use <tool>@<version>
mise lock --platform linux-x64
```

For a manual Python dependency update:

```bash
cd ingest/frame_data
uv lock --upgrade
```

For a manual Hermes Agent flake input update in a Nix-capable environment:

```bash
nix flake update hermes-agent
```

Review the resulting manifest and lockfile diffs together. Do not commit local
tool state, credentials, sessions, caches, logs, or profile-specific Hermes
state. Keep machine-specific mise overrides in ignored local config files such
as `mise.local.toml` or `.mise.local.toml`.

## Validation

Before opening a PR that changes maintainer toolchain files, run:

```bash
mise install --locked
cd ingest/frame_data
uv lock --check
```

Before opening any repo PR, also run:

```powershell
pwsh -NoProfile -File tests/validation/run-all.ps1
```

For narrow toolchain docs or policy-only changes, `tests/validation/run-all.ps1 -Lane read-only` is the lighter first pass. Keep the no-argument `all` lane for merge readiness and CI-equivalent validation.
