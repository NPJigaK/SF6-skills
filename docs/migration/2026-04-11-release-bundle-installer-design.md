# Release Bundle Installer Design

## Goal

Make this repository usable like major public skill repos such as `superpowers`: developers keep using the source monorepo, while end users install a released skill library instead of cloning the repo and wiring it manually.

Phase 1 standardizes on:

- canonical source in `skills/`
- a GitHub Release bundle containing only the distributable skill library
- one shared installer implementation
- agent-specific `INSTALL.md` entrypoints for `Codex`, `OpenCode`, `Claude`, and `Cursor`
- prompt-first UX where users can paste a short install request into their agent and let the agent perform the install

## Context

The current repo structure is already close to the desired source layout:

- `skills/` is the canonical public surface
- `maintainer-skills/` contains repo-only workflows
- `packages/` and `shared/` hold common infrastructure
- `.agents/skills/` is a repo-local dogfooding mirror

What is still weak is the install story:

- `Codex` currently documents clone + junction
- `OpenCode` currently documents direct git URL usage
- `Claude` and `Cursor` have only thin placeholders

This means the repo is structurally a source monorepo, but operationally it still asks users to consume the source repo directly. That is the gap this design closes.

## Design Principles

1. `skills/` remains the only canonical distributable source.
2. End users should not need to treat the whole repo as their working skill directory.
3. The visible UX should be agent-native and prompt-first.
4. The implementation should be centrally maintained, not reimplemented four times.
5. Phase 1 should support major agent tools without overcommitting to a marketplace format that may change.

## Options Considered

### Option 1: Keep Git Clone As The Install Primitive

Users clone the repo and wire `skills/` into their agent.

Pros:

- almost no new implementation
- developers and users share the same artifact

Cons:

- source repo remains the install unit
- does not match the UX of public installable skill repos
- exposes unrelated maintainer and data surfaces to end users

Verdict:

- rejected

### Option 2: Release Bundle Plus Universal Installer

Publish a release artifact that contains only the distributable skill library, then have one shared installer place it in the correct location for each agent.

Pros:

- clean separation between source monorepo and installed artifact
- one implementation path for all agents
- easy to document
- easy to evolve into per-skill or marketplace distribution later

Cons:

- requires release packaging work
- requires initial agent-target mapping

Verdict:

- recommended

### Option 3: Full Marketplace / Per-Skill Packaging From Day One

Treat each skill as a separately installable package or marketplace unit.

Pros:

- strongest long-term modularity
- closest to mature ecosystem end-state

Cons:

- too much operational overhead for current repo size
- forces four agent-specific distribution solutions too early

Verdict:

- defer to a later phase

## Recommended Design

Phase 1 uses a hybrid model:

- **user-facing UX:** agent-specific `INSTALL.md` entrypoints with copy-paste prompts
- **delivery artifact:** GitHub Release bundle named `sf6-skills-bundle.zip`
- **shared implementation:** one installer implementation under `packages/skill-installers/`

This follows the public-repo pattern of `superpowers`:

- each agent gets a clear front door
- the actual install logic stays centralized
- the source repo remains a development artifact, not the end-user install unit

## Release Artifact

### Bundle Name

- `sf6-skills-bundle.zip`

### Bundle Contents

The bundle contains only the distributable public skill library:

```text
sf6-skills/
  skills/
    kb-sf6-core/
    kb-sf6-frame-current/
```

It does not contain:

- `maintainer-skills/`
- `.agents/`
- `data/`
- `ingest/`
- `tests/`
- `scripts/`
- `docs/`

### Why The Bundle Contains Only `skills/`

This keeps the install unit aligned with the canonical public surface. It also ensures users consume the same skill tree across all supported agents.

## Installer Model

### Public UX

Each major agent gets an `INSTALL.md` that users can reference or paste into the agent. The instruction style should be:

- short
- explicit
- agent-native
- centered on “fetch and follow these install instructions”

Examples of the user-visible pattern:

- Codex: “Fetch and follow the instructions from `<raw INSTALL.md URL>`”
- OpenCode: “Fetch and follow the instructions from `<raw INSTALL.md URL>`”
- Claude: same pattern, adapted to Claude’s install workflow
- Cursor: same pattern, adapted to Cursor’s install workflow

The end user should not need to understand the packaging internals.

### Internal Installer Contract

The shared installer implementation is responsible for:

1. locating or downloading the requested release bundle
2. extracting only the bundled `skills/` tree
3. placing the extracted skill library into the agent-specific target path
4. replacing any previous install for the same library atomically enough for practical use
5. leaving unrelated installed skills untouched

### Agent Target Model

Phase 1 assumes one installed library name:

- `sf6-skills`

The shared installer should support these targets:

- `codex`
- `opencode`
- `claude`
- `cursor`

The interface should be explicit rather than auto-detected by default. A good minimum contract is:

```text
install-sf6-skills.ps1 -Agent <codex|opencode|claude|cursor> [-Version <release-tag>] [-Source <release-url-or-local-zip>]
```

This keeps automation and debugging simple while allowing future wrappers to hide the flags from end users.

## Agent-Specific Entry Surfaces

### Codex

Keep `.codex/INSTALL.md`, but change its role:

- no clone + junction guidance for end users
- instead describe how the agent should invoke the shared installer against the latest release bundle

### OpenCode

Keep `.opencode/INSTALL.md`, but change it away from direct git URL consumption.

It should route to the same shared installer flow as Codex.

### Claude

Keep `.claude-plugin/` as the Claude-facing surface.

Phase 1 should add a Claude install entrypoint that still resolves to the shared installer logic rather than inventing a separate packaging format.

### Cursor

Keep `.cursor-plugin/` as the Cursor-facing surface.

Phase 1 should move it from docs-only placeholder to an actual install entrypoint that routes to the same bundle/install contract.

## Developer Experience

Developers continue to use the source monorepo directly:

- edit canonical skills in `skills/`
- generate packaged runtime assets in-repo
- refresh `.agents/skills/` for repo-local dogfooding
- build release bundles from the source repo

This keeps authoring and distribution concerns separate without adding a second source of truth.

## Proposed File Additions

### Packaging

- `packages/skill-packaging/build-release-bundle.ps1`
- `tests/packaging/validate-release-bundle.ps1`

### Installers

- `packages/skill-installers/install-sf6-skills.ps1`
- `packages/skill-installers/resolve-install-target.ps1`
- `tests/install/validate-installer-contract.ps1`

### Agent Entry Surfaces

- update `.codex/INSTALL.md`
- update `.opencode/INSTALL.md`
- add/extend Claude install surface under `.claude-plugin/`
- add/extend Cursor install surface under `.cursor-plugin/`

### Release Docs

- `docs/distribution/release-bundle.md`

## Validation Requirements

Phase 1 should verify at least these things:

1. the release bundle contains `skills/` and only distributable skill content
2. the installer can target all four supported agent types
3. the installer does not require the whole repo checkout
4. the installed output preserves the `skills/` tree shape
5. agent entry docs point to the same install contract rather than diverging implementations

## Non-Goals For Phase 1

- per-skill install selection
- marketplace publication automation
- signed release workflow
- semantic version management beyond manual release tags
- uninstall / upgrade UX beyond replace-in-place behavior

## Phase 2 Candidates

- skill-level install selection
- generated install snippets for each release
- marketplace-native packaging where stable and worth the maintenance cost
- release manifest with checksums and metadata

## Recommendation

Proceed with:

- one shared release bundle
- one shared installer implementation
- four agent-specific install front doors
- prompt-first install UX

This is the best fit for the repository’s current maturity and matches the best-practice direction of major public skill repos without forcing premature marketplace complexity.
