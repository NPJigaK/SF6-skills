# SF6 Skills

SF6 Skills is a repository of concept-first Street Fighter 6 knowledge and published current-fact surfaces for agent workflows. It distributes public skills from `skills/`, keeps current roster facts grounded in published exports, and exposes install front doors for Codex, Claude, Cursor, and OpenCode.

## How it works

After installation, this repo exposes SF6 knowledge as agent-readable skills. The agent can usually choose a matching skill automatically. You can also mention a skill by name explicitly.

Use `kb-sf6-core` for stable concepts and terminology that should not depend on the current patch. Use `kb-sf6-frame-current` when the task needs exact current values for supported current roster characters. Use `video-analysis-core` for observation-first video analysis from raw footage.

Concept explanation and current-fact lookup are intentionally separated. Current facts are grounded in published exports rather than raw or audit surfaces.

## Installation

Installation differs by agent. This root README currently documents Codex, Claude, Cursor, and OpenCode.

### Codex

Ask Codex:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent codex using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the Codex discovery target to that source.
```

Detailed docs: [.codex/INSTALL.md](./.codex/INSTALL.md)

### Claude

Ask Claude:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent claude using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the Claude discovery target to that source.
```

Detailed docs: [.claude-plugin/INSTALL.md](./.claude-plugin/INSTALL.md)

### Cursor

Ask Cursor:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent cursor using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the Cursor discovery target to that source.
```

Detailed docs: [.cursor-plugin/INSTALL.md](./.cursor-plugin/INSTALL.md)

### OpenCode

Ask OpenCode:

```text
Fetch https://raw.githubusercontent.com/NPJigaK/SF6-skills/main/packages/skill-installers/install-sf6-skills.ps1, save it locally, and run it for agent opencode using the latest sf6-skills-bundle.zip release from NPJigaK/SF6-skills. The installer downloads the bundle into a private source checkout and links the OpenCode discovery target to that source.
```

Detailed docs: [.opencode/INSTALL.md](./.opencode/INSTALL.md)

## Verify installation

Start a new session in your agent, then try one concept question and one current-fact question.

Concept check:

```text
Explain what plus frames mean in SF6 and why they matter on offense.
```

Current-fact check:

```text
Use kb-sf6-frame-current to check the current published frame data for Luke's crouching medium punch.
```

If the agent selects the expected public skill automatically or responds correctly when you name the skill directly, installation is working.

## Basic usage

The agent can usually choose a matching skill automatically. You can also mention a skill by name explicitly.

### Concept-first usage with `kb-sf6-core`

```text
Use kb-sf6-core to explain what a shimmy is in SF6 and why it beats throw tech attempts.
```

### Current-fact usage with `kb-sf6-frame-current`

```text
Use kb-sf6-frame-current to check the current published startup and block advantage for Luke's crouching medium punch.
```

## Current fact policy

For current roster characters, current fact is grounded in published exports only.

- Start from `data/exports/<character_slug>/snapshot_manifest.json`.
- Use only datasets whose `publication_state = available`.
- The current roster canonical source is `shared/roster/current-character-roster.json`.
- `official_raw` is canonical.
- `derived_metrics` is official-only computed output.
- `supercombo_enrichment` is supplemental only.
- `data/raw/...`, `data/normalized/...`, and `*_manual_review.*` are not the final evidence surface for normal current-fact answers.
- Packaged runtime assets under `skills/kb-sf6-frame-current/assets/published/...` are generated from repo-level canonical published data under `data/exports/...`.

For more detail, see [ingest/frame_data/README.md](./ingest/frame_data/README.md) and [repo-structure-contract.md](./docs/architecture/repo-structure-contract.md).

## What's inside

- `skills/`
  - canonical public source for distributable skills
- `maintainer-skills/`
  - repository-only workflows for maintainers
- `shared/`
  - shared non-code artifacts such as roster and stable vocabulary
- `data/exports/`
  - repo-level canonical published current-fact surface
- `ingest/`
  - ingestion, normalization, and publishing implementation
- `local/`
  - tracked personal trial workspace for trying distributed skills

## Contributing

Contributors should work from the repository checkout rather than only from installed discovery links.

- New public skills belong under `skills/<skill-name>/`.
- Maintainer-only workflows belong under `maintainer-skills/`.
- Ingestion and publication code belongs under `ingest/frame_data/`.
- Read [repo-structure-contract.md](./docs/architecture/repo-structure-contract.md) before changing repository surfaces.

## Updating

- Installed users should follow the current install or update flow for their agent, using the linked install docs above.
- Contributors should pull the repository directly and work from the repo checkout.
- If an agent-specific flow changes, treat the linked install docs as the source of truth.
