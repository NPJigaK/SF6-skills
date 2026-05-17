# Check Agent Toolchain Freshness

## Purpose

Use this workflow to manually review maintainer agent toolchain freshness for
Codex CLI and Hermes CLI.

This workflow does not make local tool state canonical. The canonical policy
surface is `data/toolchain/maintainer-agent-toolchain.json`, which records
reviewed expectations and capabilities, not local installed versions.

## Manual Review Steps

1. Read `data/toolchain/README.md`.
2. Read `data/toolchain/maintainer-agent-toolchain.json`.
3. Review the official documentation or release source for each tool.
4. Check whether the local tool can provide the required or planned
   capabilities needed for current maintainer work.
5. Record policy changes only when they are reviewed and useful to future
   maintainers.

Version and update commands should be used only when verified from official
docs, release sources, or the tool's own reviewed CLI help. If a command is not
verified, keep the command field nullable in the manifest and include a review
note.

## Hermes Profile Review

For Hermes maintainer profiles, review the policy in
`docs/architecture/hermes-maintainer-profile-policy.md` and the structured
expectations in `data/toolchain/maintainer-agent-toolchain.json`.

The repo-managed expectation is:

- maintainer profiles are repo-local only
- model: `gpt-5.5`
- accepted model alias: `codex 5.5`
- reasoning: `xhigh` / extra-high where supported
- Hermes CLI version management is primarily through `flake.nix`, `flake.lock`,
  and Renovate Nix flake PRs
- skill selection is profile-specific policy, not committed runtime skill state
- local Hermes commands are fallback observations, not canonical repo data

## Canonical Hermes CLI Freshness Route

Hermes CLI freshness is reviewed through repo-managed pins and dependency PRs,
not by committing local command output.

Primary route:

- Renovate Nix flake PRs update the `hermes-agent` input.
- Review `flake.nix`, `flake.lock`, the Renovate PR diff, and CI output.
- Merge only after the reviewed pin and validation are acceptable.

Manual Nix review, when a maintainer needs to inspect the pin locally:

```bash
nix flake update hermes-agent
nix run .#hermes -- --version
nix flake metadata
```

The command output is local operator evidence only. Do not paste exact version
strings, resolved local store paths, commit-behind counts, or Nix command
transcripts into repo artifacts.

If local Nix is unavailable, do not treat that as proof that the policy is
wrong. Use fallback local Hermes checks only as operator diagnostics:

```bash
hermes --version
hermes doctor
```

If a non-Nix local Hermes installation needs an update, keep that action local:

```bash
hermes update
hermes --version
hermes doctor
```

Fallback output is not the canonical version pin. A PR may summarize that local
freshness was reviewed, but it must not include exact local installed versions,
commit-behind counts, doctor transcripts, local paths, provider diagnostics,
Python/OpenAI SDK versions, update output, logs, caches, credentials, or auth
output.

## Profile Expectation Review

`sf6ingest` profile checks are local review signals. They may help confirm that
a maintainer's machine is aligned with the repo policy, but they are not proof
of canonical repo state.

Profile checks are separate from CLI pinning:

```bash
hermes profile list
hermes profile show sf6ingest
```

Expected profile policy:

- model: `gpt-5.5`
- accepted model alias: `codex 5.5`
- reasoning: `xhigh` / extra-high when the provider and Hermes CLI expose it
- reasoning requirement mode: required when supported

These values are policy expectations from
`data/toolchain/maintainer-agent-toolchain.json`, not copied local profile
state, and not local profile state. If local profile output does not expose
reasoning effort, treat that as a manual local review gap rather than a repo
policy mismatch. Fix local profile state locally, or open a separate policy PR
if the repo expectation itself must change.

Skill selection checks are also local review signals only:

```bash
hermes skills list
hermes skills inspect hermes-agent
```

Do not paste exact local version output, commit-behind counts, local profile
paths, Python/OpenAI SDK versions, profile listings, logs, or auth output into
canonical policy data. Do not paste local skill enablement output, local skill
paths, or exported skill configuration into canonical policy data. A PR body
may summarize that local freshness and skill selection were reviewed, but local
output remains non-canonical.

Safe PR wording:

- OK: "Reviewed Hermes CLI freshness policy; canonical update path remains
  Renovate Nix flake PRs. Local profile output was not committed."
- OK: "The `sf6ingest` model and reasoning expectations remain `gpt-5.5` and
  `xhigh` as repo policy. No local profile dump is included."
- Not OK: exact `hermes --version` output, commit-behind counts, full
  `hermes doctor` output, `hermes profile list` output, profile paths,
  config paths, command transcripts, logs, caches, credentials, tokens, device
  codes, or auth output.

If a PR uses the phrase "not copied local profile state", it must mean exactly
that no local profile state was copied into the repo artifact.
Device codes are auth output and must not be pasted into repo artifacts.

## Boundaries

- Do not store local installed versions in canonical policy data.
- Do not commit local configs, sessions, logs, caches, tokens, credentials, or
  secrets.
- Do not use this workflow to require Codex CLI or Hermes CLI for public
  `sf6-agent` users.
- CI validators must not perform online latest-version checks.
- Future Hermes cron may report freshness, but it must not auto-update tools
  or mutate canonical repo surfaces.

## Validation

After editing toolchain policy data, run:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-agent-toolchain.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-v2-contracts.ps1
```

Before opening a PR, also run the full validation suite:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```

See `docs/architecture/powershell-compatibility-policy.md` for Windows
PowerShell / `powershell.exe` fallback guidance.
