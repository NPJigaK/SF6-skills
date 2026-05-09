# Hermes Pack

Hermes is the primary repo-local orchestration harness when a configured maintainer profile is available.

Hermes is not a public answer adapter, not a public install target, and not canonical memory.

## Use

Use `packs/hermes-sf6/` when a maintainer wants Hermes to orchestrate repo-local workflows around this repository. Normal public agent installs should use the Codex, Claude, Cursor, or OpenCode docs in this directory.

When Hermes is unavailable, Codex, humans, or other agents may still follow the same canonical workflows as fallback executors.

The pack points back to [workflows](../../../workflows/) for canonical maintainer procedures. It must not ship or imply:

- memory state
- cron state
- secrets
- user session state

## Adapter

Hermes should consume the same single adapter as every other surface: `sf6-agent`. The adapter is bundled by `packages/skill-packaging/build-release-bundle.ps1` into `.dist/sf6-agent-bundle.zip`.

Hermes does not replace `skills/sf6-agent/` and does not define public answer behavior.

## Config Guidance

Start from `packs/hermes-sf6/hermes.example.json`, copy it outside the repository if Hermes requires local edits, and keep local state outside version control.
