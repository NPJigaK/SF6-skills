# V2 Architecture

## Product

SF6 Knowledge Agent Kit is a reviewable knowledge and distribution repo for AI agents answering Street Fighter 6 questions.

The repo has one public adapter, `skills/sf6-agent/`, and several canonical source surfaces that feed it.

## Canonical Surfaces

- `knowledge/`: curated concepts, glossary, strategy notes, and reviewable claims.
- `data/exports/`: exact published current-fact exports.
- `data/roster/`: exact current roster source.
- `contracts/`: schemas and structured artifact contracts.
- `workflows/`: maintainer procedures for growing and refreshing the repo.
- `evals/`: answer-quality questions and rubrics.

## Adapter Surface

- `skills/sf6-agent/SKILL.md`: adapter entry behavior.
- `skills/sf6-agent/references/*-policy.md`: hand-written adapter policy.
- `skills/sf6-agent/references/generated-*`: derived curated knowledge payload.
- `skills/sf6-agent/assets/frame-current/`: derived exact current-fact runtime payload.

The adapter can be bundled without requiring a full repo checkout.

## Derived Surface Rules

Generated references and frame-current assets are outputs. They must carry provenance and must point back to canonical source paths.

Generated references come from `knowledge/curated/` only. They must not contain exact current frame values.

Frame-current assets come from `data/exports/` plus `data/roster/` only. They must not include manual-review rows, raw snapshots, normalized intermediate files, or CSV sidecars.

## Evidence Model

V2 uses generic evidence metadata. Canonical artifacts should describe source kind, source role, evidence basis, verification state, confidence, volatility, patch sensitivity, review status, source references, and review timing.

Historical labels and source-tier names may appear only when documenting deprecated v1 behavior. They are not v2 metadata fields.

## Answer Modes

Public answers should communicate the mode and evidence boundary naturally:

- `stable_concept`
- `verified_current_fact`
- `strategy_or_matchup_knowledge`
- `observation`
- `unresolved_or_hold`

Evals check whether the answer mode and boundary behavior are correct. They do not require legacy bracket labels.

## Hermes

Hermes may be used as an optional maintainer harness. It is not canonical memory, and no Hermes memory, cron state, secrets, or user session state should be shipped.
