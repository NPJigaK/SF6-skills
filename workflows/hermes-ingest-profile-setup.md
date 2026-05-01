# Hermes Ingest Profile Setup

This workflow documents how maintainers should set up and verify a dedicated Hermes profile for SF6 Knowledge Agent Kit article ingest and review assistance.

Hermes is an optional maintainer harness. It is not required for article ingest, and Hermes memory is not canonical SF6 knowledge.

## Profile Roles

Use separate Hermes profiles for separate maintainer tasks:

- `sf6smoke`: smoke tests for Hermes harness behavior.
- `sf6ingest`: article ingest and review workflow assistance.

The ingest profile should help draft source summaries, candidate claims, and review notes while following `workflows/ingest-article.md`.

Final source, claim, and review outputs must be committed as repo artifacts under `knowledge/`. A Hermes profile, session, memory entry, or chat transcript is not a source of truth.

## Profile Isolation

Hermes profile state is profile-scoped. Config, provider authentication, sessions, memory, cron state, managed skills, and `.env` files can differ between profiles.

Profile isolation is not a filesystem sandbox. Run Hermes from a deliberate working directory, keep `HERMES_HOME` outside this repository, and verify repository cleanliness after each run.

## Provider Authentication

Runtime/provider authentication is profile-scoped. A new or cloned ingest profile may discover repo skills but still fail non-interactive execution until that profile has completed its own provider authentication.

For a new `sf6ingest` profile:

1. Create or select a Hermes profile whose home directory is outside this repo.
2. Configure provider authentication interactively for that profile.
3. Run `hermes doctor` with the ingest profile selected.
4. Run a small non-interactive command with the ingest profile before using it for article ingest.

Do not copy credentials into this repository. Do not paste tokens, API keys, device codes, `.env` contents, or account-specific auth output into issue comments, PR bodies, smoke reports, or workflow docs.

## Recommended Setup Shape

Use repo-external profile state:

```bash
export HERMES_HOME="$HOME/.hermes/profiles/sf6ingest"
```

Configure Hermes so it can discover the repo's public adapter skills without turning Hermes state into repo state. When using external skill discovery, prefer the repo `skills/` directory:

```yaml
skills:
  external_dirs:
    - /absolute/path/to/SF6-skills/skills
```

Do not configure `workflows/` as a skill directory. Workflows are canonical maintainer procedures, not public adapter skills.

## Verification

Before using `sf6ingest` for article ingest:

```bash
test -n "$HERMES_HOME"
case "$HERMES_HOME" in
  /absolute/path/to/SF6-skills/*) echo "HERMES_HOME is inside the repo; stop" ;;
  *) echo "HERMES_HOME is outside the repo" ;;
esac

hermes doctor
hermes chat -Q --max-turns 1 -q "Reply with one sentence confirming this profile can run non-interactively."
```

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
