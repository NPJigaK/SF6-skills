# Root README Redesign

## Goal

Rewrite the repository-root `README.md` so it matches the current repository design, reads closer to the `superpowers` onboarding style, and still preserves the SF6-specific trust model for current-fact answers.

## Confirmed Repo Facts

- `skills/` is the canonical public source for distributable skills.
- `maintainer-skills/` is the repository-only workflow surface for maintainers.
- The current public skills are:
  - `skills/kb-sf6-core`
  - `skills/kb-sf6-frame-current`
  - `skills/video-analysis-core`
- The current maintainer skills are:
  - `maintainer-skills/sync-knowledge`
  - `maintainer-skills/update-frame-data`
- The root repo currently exposes install front doors for:
  - Codex via `.codex/INSTALL.md`
  - Claude via `.claude-plugin/INSTALL.md`
  - Cursor via `.cursor-plugin/INSTALL.md`
  - OpenCode via `.opencode/INSTALL.md`
- The root repo does not currently expose a Gemini-specific install front door.
- Current roster canonical source is `shared/roster/current-character-roster.json`.
- Current-fact answers for current roster characters must start from `data/exports/<character_slug>/snapshot_manifest.json` and use only datasets whose `publication_state` is `available`.
- `official_raw` is canonical, `derived_metrics` is official-only computed output, and `supercombo_enrichment` is supplemental only.
- `data/raw/...`, `data/normalized/...`, and `*_manual_review.*` are not the final evidence surface for normal current-fact answers.
- The existing root `README.md` already contains some correct facts, but it reads more like a compact repo contract than an install-and-use onboarding document.
- The embedded `superpowers` project uses a stronger onboarding-first README shape:
  - what it is
  - how it works
  - installation
  - verify installation
  - basic workflow / usage
  - what's inside
  - contributing
  - updating

## Audience

Primary audience:

- new contributors entering the repository for the first time

Secondary audiences:

- users who want to install and use the distributed public skills
- maintainers working on current-fact publication or repo structure

## Problem

The current root `README.md` is structurally accurate, but it under-serves the repository's actual entry needs:

1. it does not give a strong install-and-use onboarding path
2. it does not explain skill selection and first-use behavior in the style users now expect from `superpowers`
3. it does not clearly separate public-skill onboarding from maintainer-only workflows
4. it does not foreground the current-fact trust model in a way that is easy to understand without reading deeper docs

That leaves the repo in an awkward middle state:

- too sparse to work as an onboarding README
- too high-level to replace the deeper architecture docs

## Options Considered

### Option A: Superpowers-near clone

- mirror the `superpowers` README structure and tone very closely
- strong onboarding feel
- but risks under-explaining the SF6-specific current-fact policy and canonical-source rules

### Option B: Hybrid onboarding plus trust-model README

- keep the `superpowers` section order and onboarding posture in the front half
- insert SF6-specific `Current fact policy` and a more concrete `What's inside` section in the middle
- preserve easy install/use flow without hiding the repo's most important source-of-truth rules

### Option C: Repo-contract-first README

- focus the README on repository structure, source boundaries, and publication semantics
- high precision
- but weak onboarding, weaker first-use flow, and less alignment with the `superpowers` model the user explicitly wants to emulate

## Decision

Adopt Option B.

The new root README should:

- feel like a `superpowers`-style onboarding README in the front half
- stay accurate to the current repository layout and install surfaces
- give readers a fast path to first use
- still explain the SF6 current-fact trust model clearly enough to prevent misuse

## Narrative Strategy

The README should tell this story in order:

1. what this repository is
2. how the skill-driven usage model works
3. how to install it on supported agents
4. how to confirm that installation worked
5. how to use the public skills first
6. how current-fact trust and published exports work
7. what each major top-level surface is for
8. how contributors should work in the repo
9. how installed users and contributors update

This keeps the front half focused on install and first use, then moves into trust model and repository structure.

## Target README Structure

The target section order is:

1. `SF6 Skills`
2. `How it works`
3. `Installation`
4. `Verify installation`
5. `Basic usage`
6. `Current fact policy`
7. `What's inside`
8. `Contributing`
9. `Updating`

## Section Design

### `SF6 Skills`

Purpose:

- define the repo in one short opening block

Content:

- concept-first SF6 knowledge for agent workflows
- published current-fact surfaces for current roster characters
- install front doors for supported agent environments

Tone:

- English-first overall
- do not force awkward Japanese translations for established terms

### `How it works`

Purpose:

- explain the usage model before install details

Content:

- the repo distributes SF6 knowledge as agent-readable skills
- the agent can usually choose a matching skill automatically
- users can also mention a skill by name explicitly
- concept explanation and current-fact lookup are intentionally separated
- current facts are grounded in published exports rather than raw or audit surfaces

This section should introduce the trust model lightly, then hand off deeper detail to `Current fact policy`.

### `Installation`

Purpose:

- provide a short install entry for each currently supported root install surface

Supported agent sections:

- `Codex`
- `Claude`
- `Cursor`
- `OpenCode`

Rules:

- include the short install prompt directly in the root README
- link each section to its agent-specific `INSTALL.md`
- do not present Gemini as supported in the root README unless the repo gains a root Gemini front door

### `Verify installation`

Purpose:

- give a simple success check after install

Content:

- start a new session in the chosen agent
- ask an SF6 task that should match one of the public skills
- confirm that the agent either selects the matching skill or responds correctly when a skill is named explicitly

### `Basic usage`

Purpose:

- show the first successful public-skill interactions

Rules:

- focus only on public skills
- do not include maintainer-only workflows here

Usage model to describe:

- the agent can choose a matching skill automatically
- the user can also mention a skill by name

Examples to include:

- one natural-language example for `kb-sf6-core`
- one natural-language example for `kb-sf6-frame-current`

Recommended emphasis:

- put the concept-first example first
- mention current-fact lookup second

### `Current fact policy`

Purpose:

- explain the repo's trust model at medium depth

Content to state explicitly:

- current fact for current roster characters is grounded in published exports only
- lookup starts from `data/exports/<character_slug>/snapshot_manifest.json`
- only datasets with `publication_state = available` are valid for normal current-fact answers
- current roster canonical source is `shared/roster/current-character-roster.json`
- `official_raw` is canonical
- `derived_metrics` is official-only computed output
- `supercombo_enrichment` is supplemental only
- `data/raw/...`, `data/normalized/...`, and `*_manual_review.*` are not the final evidence surface for normal current-fact answers
- packaged runtime assets under `skills/kb-sf6-frame-current/assets/published/...` are generated from repo-level canonical published data under `data/exports/...`

Writing rule:

- this section should be clearer than a one-line summary
- but it should stop short of reproducing the full ingestion contract

Link out to:

- `ingest/frame_data/README.md`
- `docs/architecture/repo-structure-contract.md`

### `What's inside`

Purpose:

- explain the top-level surfaces more concretely than `superpowers` needs to

Surfaces to include:

- `skills/`
- `maintainer-skills/`
- `shared/`
- `data/exports/`
- `ingest/`
- `local/`

Each item should explain responsibility, not just name the directory.

### `Contributing`

Purpose:

- move repo-contribution guidance into the back half of the README

Content:

- contributors should work from the repository checkout, not only from installed discovery links
- new public skills belong under `skills/`
- maintainer-only workflows belong under `maintainer-skills/`
- ingestion and publication code belongs under `ingest/frame_data/`
- readers should consult the structure contract before changing repo surfaces

This is the correct place for clone-for-contribution guidance.

### `Updating`

Purpose:

- give a short answer for both installed users and contributors

Content:

- installed users update by following the current install/update flow for their agent
- contributors update by pulling the repository and using the repo directly
- if behavior differs by agent, follow the linked agent-specific install docs

## Writing Guidelines

- Keep the README English-first overall.
- Use short Japanese only when it clarifies repo-specific nuance better than forced English would.
- Prefer a concise onboarding tone over exhaustive contract prose.
- Preserve important exact paths and identifiers verbatim.
- Avoid duplicating full architecture-doc wording when a summary plus a link is sufficient.

## Non-Goals

- do not add Gemini support wording to the root README before the root repo actually exposes that install surface
- do not turn `Basic usage` into maintainer workflow documentation
- do not replace deeper architecture or ingestion docs with a giant README
- do not weaken the current-fact policy into vague wording
- do not rewrite repository structure rules in a way that conflicts with the existing structure contract

## Risks And Mitigations

### Risk: the README becomes too onboarding-heavy and hides the trust model

Mitigation:

- keep `Current fact policy` as a distinct medium-depth section
- state the exact canonical paths that govern current-fact lookup

### Risk: the README becomes too contract-heavy and loses the `superpowers` feel

Mitigation:

- keep install, verification, and basic usage in the front half
- use short sections and direct examples

### Risk: maintainer workflows leak into public first-use guidance

Mitigation:

- keep `sync-knowledge` and `update-frame-data` out of `Basic usage`
- mention them only in `What's inside` or `Contributing`

### Risk: the root README claims support broader than the repo actually exposes

Mitigation:

- limit `Installation` to Codex, Claude, Cursor, and OpenCode
- add Gemini only after a root Gemini install front door exists
