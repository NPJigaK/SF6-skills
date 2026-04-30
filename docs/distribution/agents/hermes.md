# Hermes Pack

Hermes is optional maintainer harness guidance, not a public install target and not canonical memory.

## Use

Use `packs/hermes-sf6/` only when a maintainer wants a Hermes harness around this repository. Normal public agent installs should use the Codex, Claude, Cursor, or OpenCode docs in this directory.

The pack points back to [workflows](../../../workflows/) for canonical maintainer procedures. It must not ship or imply:

- memory state
- cron state
- secrets
- user session state

## Adapter

Hermes should consume the same single adapter as every other surface: `sf6-agent`. The adapter is bundled by `packages/skill-packaging/build-release-bundle.ps1` into `.dist/sf6-agent-bundle.zip`.

## Config Guidance

Start from `packs/hermes-sf6/hermes.example.json`, copy it outside the repository if Hermes requires local edits, and keep local state outside version control.
