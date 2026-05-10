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
docs or release sources. If a command is not verified, keep the command field
nullable in the manifest and include a review note.

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
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-agent-toolchain.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-v2-contracts.ps1
```

Before opening a PR, also run the full validation suite:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1
```
