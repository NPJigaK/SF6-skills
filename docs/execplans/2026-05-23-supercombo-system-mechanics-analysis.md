# SuperCombo System Mechanics Analysis

Status: Implementation complete; review pending.

## Purpose

Record evidence from SuperCombo's Street Fighter 6 system pages before
deterministic parser/classifier implementation. The goal is to prevent raw
frame, damage, gauge, cancel, enum, and prose values from being parsed from
shape alone without the source mechanics that define what those values mean.

This ExecPlan answers the current review concern: the remaining disposition
groups are not safe calculation inputs merely because their source review is
complete. They need deterministic parser, enum, and raw-preservation policies
grounded in system-mechanics evidence.

## Scope

Included:

- Capture reviewer evidence for these SuperCombo system pages:
  - Controls
  - HUD
  - Gauges
  - Offense
  - Defense
  - Movement
  - Game Data
  - Glossary
- Analyze page text, sections, tables, and source images that define parsing
  semantics.
- Produce a public summarized source review for parser/schema planning.
- Update the deterministic parsed-value classifier ExecPlan so it depends on
  this source review before implementation.

Excluded:

- No parser/classifier implementation.
- No JSON Schema changes.
- No normalized current-fact export.
- No frame, punish, damage, scaling, or combo calculator.
- No retrieval or answer behavior changes.
- No source page Markdown, raw HTML, screenshots, image dumps, cookies,
  browser profiles, traces, or debug dumps committed to the repo.

## Evidence Boundary

Reviewer evidence is kept under ignored local storage:

```text
.local/reviewer-evidence/supercombo-system-20260523/
```

Evidence collection used Scrapling reviewer tooling because the site is
protected. `solve_cloudflare=True` was used only for reviewer evidence
collection. This remains outside runtime, CLI, CI, validators, retrieval,
answer mode, and numeric authority.

## Public Artifact

Created:

```text
docs/system-mechanics/20260523-supercombo-system-mechanics-parser-inputs.md
```

The artifact contains summarized facts, permanent source revision links, image
observations, parser/schema implications, and calculation-safety gates. It does
not contain raw page dumps or screenshots.

## Findings

- The `224` parser/enum disposition groups are calculation blockers until
  deterministic parser/classifier output exists.
- Text and prose are not ignorable. When a note affects calculation, it must
  become a deterministic condition, enum, modifier, or review-required state.
- Some values are intentionally raw-preserved and excluded from calculation;
  this must be explicit, not a silent fallback.
- Future game updates may change numeric values or special expressions. New
  unclassified expressions must hard fail or become human review items before
  calculation use.

## Acceptance Criteria

- All eight requested system pages are listed with permanent revision links.
- System mechanics affecting parser/schema design are summarized without raw
  source dumps.
- Source images that affect semantics are reviewed as local ignored evidence.
- The disposition groups are mapped to next parser/schema decisions.
- Existing deterministic parsed-value classifier plan explicitly depends on
  this source review.
- No runtime/schema/parser/retrieval/answer behavior changes are introduced.

## Validation Commands

Run from repository root:

```bash
git diff --check
PYTHONPATH=src uv run --locked python tests/validation/validate_clean_slate.py
git status --short --branch
```

## Progress

- [x] (2026-05-23 JST) Preserved unrelated SymPy dependency work in a named
  stash before starting this branch.
- [x] (2026-05-23 JST) Created branch
  `research/supercombo-system-mechanics-analysis`.
- [x] (2026-05-23 JST) Collected all requested SuperCombo system pages through
  Scrapling reviewer evidence.
- [x] (2026-05-23 JST) Reviewed source image evidence under ignored local
  reviewer storage.
- [x] (2026-05-23 JST) Added summarized public source review artifact.
- [x] (2026-05-23 JST) Updated deterministic parsed-value classifier plan to
  depend on this source review.

## Decision Log

- Decision: Treat SuperCombo system pages as planning evidence, not numeric
  authority.
  Rationale: SuperCombo remains enrichment/cross-reference/candidate only in
  this repository. The system pages can define how SuperCombo expressions
  should be interpreted, but they do not promote SuperCombo raw values to
  daily-answer numeric authority.
  Date/Author: 2026-05-23 / Codex

- Decision: Keep screenshots and page captures out of git.
  Rationale: Reviewer evidence may include rendered pages/images and must stay
  under ignored local storage. Public artifacts should contain only summarized
  facts and source links.
  Date/Author: 2026-05-23 / Codex

- Decision: Block calculation use until parser/classifier implementation
  proves the source expression class is parsed.
  Rationale: System pages define context-dependent meanings for values such as
  `X(Y)`, `X(n)Y`, `X,Y`, `X*Y`, `KD`, cancel tokens, scaling notes, and gauge
  units. Treating those as plain numbers would violate the PLAN numeric rules.
  Date/Author: 2026-05-23 / Codex

## Deviations

- None.

## Risks

- The source review is summarized. If later parser implementation needs full
  source context, it must refer to ignored local evidence or re-acquire pages
  through an approved update/research mode.
- SuperCombo source pages may change. Future drift must re-run source review
  before updating parser policies.
- This artifact does not by itself make any calculation possible.

## Completion Review Table

| PLAN item | Implementation | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Evidence before parser | Added source mechanics review | `docs/system-mechanics/20260523-supercombo-system-mechanics-parser-inputs.md` | reviewer check | Pending | None | Parser not implemented | Summary must not be treated as authority fact table |
| Preserve source boundary | Kept captures/screenshots ignored | This ExecPlan | `git status --short --branch` | Pending | None | Local evidence not committed | Later review may need re-acquisition |
| Preserve calculation safety | Updated classifier plan dependency | `docs/execplans/2026-05-23-deterministic-parsed-value-classifier-implementation.md` | reviewer check | Pending | None | Calculators not implemented | Raw/unparsed values remain blocked |
