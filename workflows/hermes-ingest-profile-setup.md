# Hermes Ingest Profile Setup

This workflow documents how maintainers should set up and verify a dedicated Hermes profile for SF6 Knowledge Agent Kit article ingest and review orchestration.

Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available. It is not required for article ingest when maintainers use Codex, humans, or other agents as fallback executors, and Hermes memory is not canonical SF6 knowledge.

## Profile Roles

Use a single repo-local Hermes maintainer profile for SF6 maintainer tasks:

- `sf6ingest`: source review, artifact drafting, smoke checks, and maintainer
  workflow validation.

The ingest profile should help draft source summaries, candidate claims, and review notes while following `workflows/ingest-article.md`.

Final source, claim, and review outputs must be committed as repo artifacts under `knowledge/`. A Hermes profile, session, memory entry, or chat transcript is not a source of truth.

## Profile Isolation

Hermes profile state is profile-scoped. Config, provider authentication, sessions, memory, cron state, managed skills, and `.env` files can differ between profiles.

Profile isolation is not a filesystem sandbox. Run Hermes from a deliberate working directory, keep `HERMES_HOME` outside this repository, and verify repository cleanliness after each run.

## Provider Authentication

Runtime/provider authentication is profile-scoped. A new or cloned ingest profile may discover repo skills but still fail non-interactive execution until that profile has completed its own provider authentication.

For a new `sf6ingest` profile:

1. Create or select a Hermes profile whose home directory is outside this repo.
2. Configure the profile for `gpt-5.5` / `codex 5.5` with `xhigh` /
   extra-high reasoning where the provider and Hermes CLI expose that setting.
3. Configure provider authentication interactively for that profile.
4. Run `hermes doctor` with the ingest profile selected.
5. Run a small non-interactive command with the ingest profile before using it for article ingest.

Do not copy credentials into this repository. Do not paste tokens, API keys, device codes, `.env` contents, or account-specific auth output into issue comments, PR bodies, smoke reports, or workflow docs.

## Recommended Setup Shape

Use repo-external profile state:

```bash
export HERMES_HOME="$HOME/.hermes/profiles/sf6ingest"
```

Configure `sf6ingest` from the safe config policy in
`docs/architecture/hermes-maintainer-profile-policy.md`. The profile state stays
outside the repo; this repository records expectations, not the machine's
actual `config.yaml`.

Recommended starting posture:

```yaml
terminal:
  backend: docker
  env_passthrough: []
  docker_forward_env: []

approvals:
  mode: smart

skills:
  guard_agent_created: true
  external_dirs: []

security:
  redact_secrets: true
  tirith_fail_open: false
  allow_private_urls: false

compression:
  enabled: true

agent:
  tool_use_enforcement: auto
```

Use `data/toolchain/hermes-maintainer-skill-allowlist.json` as the reviewed
skill selection policy for `sf6ingest`. Normal maintainer work should expose
only the allowlisted built-in default skills. Built-in conditional skills are
for task-scoped needs only; external APM skills are for reviewed dependency
routes such as the SymPy calculation backend. Do not treat local
`hermes skills list` output as canonical repo data.

`terminal.backend: local` is allowed for trusted repo-local work, but it is not
a sandbox. Use Docker for untrusted code, broad source ingest, experimental
refactors, or credential-adjacent tasks.

Built-in Hermes memory and `session_search` may be enabled locally for
`sf6ingest`, but they are non-canonical context only. External Memory Providers
remain disabled by default unless a later reviewed issue adopts one. See
`docs/architecture/hermes-memory-policy.md`.

For substantial Hermes-assisted edits, use a dedicated git worktree or
`hermes -w`, and enable checkpoints as a local rollback safety feature. Run
Curator only through the lifecycle in
`docs/architecture/hermes-curator-worktree-checkpoint-policy.md`: dry-run,
pin important skills, backup, review, restore/rollback if needed, and promote
only summarized lessons through reviewed repo artifacts.

Do not point `skills.external_dirs` at the repo `skills/` directory by default.
`skills/sf6-agent/` is a deferred public adapter surface, not the active private
Hermes maintainer skill package. External skill directories must come from a
reviewed dependency policy such as #231 or a later architecture decision.

When external skill dependencies are installed for local operation, they must
come from the reviewed APM manifest / lockfile route in `tools/agent-skills/`
and appear in the `external_apm_skills` allowlist category. Broad third-party skill bundles,
local managed skills, and ad-hoc external directories are not default
`sf6ingest` profile inputs.

Do not configure `workflows/` as a skill directory. Workflows are canonical
maintainer procedures, not Hermes installed skills.

## Verification

Before using `sf6ingest` for article ingest:

```bash
test -n "$HERMES_HOME"
repo_root="$(git rev-parse --show-toplevel)"
case "$HERMES_HOME" in
  "$repo_root"/*)
    echo "HERMES_HOME is inside the repo; stop"
    exit 1
    ;;
  *) echo "HERMES_HOME is outside the repo" ;;
esac

hermes doctor
hermes --version
hermes profile list
hermes profile show sf6ingest
hermes chat -Q --max-turns 1 -q "Reply with one sentence confirming this profile can run non-interactively."
```

Also verify the safe config posture locally without committing the output:

```bash
hermes config check
hermes config
```

Review the printed local config for the recommended keys above. If a command,
section, or config key differs across Hermes versions, record the mismatch as a
local review note only. Do not paste local profile output into repo artifacts.

Prefer the repo Nix flake and Renovate Nix flake PRs for Hermes CLI version
freshness. Use `hermes --version` output only as a fallback local freshness
signal. If a non-Nix local Hermes install reports `Update available` or a
commit-behind count, update Hermes outside the repo and re-run
`hermes --version` and `hermes doctor`. Do not commit exact version output,
profile listings, local paths, auth output, logs, sessions, or local profile
state.

After any Hermes-assisted ingest run:

```bash
git status --porcelain
find . -maxdepth 3 \( -name ".hermes" -o -name ".env" -o -iname "*session*" -o -iname "*memory*" -o -iname "*cron*" \)
```

The expected repository state is clean except for intentional repo artifacts such as source notes, candidate claims, review notes, or smoke reports.

## Ingest Boundaries

When Hermes assists article ingest:

- `workflows/ingest-article.md` remains the canonical ingest procedure.
- Hermes may draft summaries, claim decomposition, and review notes.
- Maintainer review normalizes outputs before commit.
- Canonical outputs belong under `knowledge/sources/`, `knowledge/evidence/claims/`, and `knowledge/review/`.
- Claims do not become curated knowledge until reviewed and promoted through the repo workflow.
- Do not store full copyrighted articles, transcripts, large excerpts, credentials, or private local state in the repo.
