---
id: sf6-review-youtube-nyfngnzjv3m-jp-combos
title: YouTube nyFNgnzjV3M JP Combo Damage Oracle Fixture Review
claim_kind: observation
source_kind: reproducible_observation
source_role: combo_damage_oracle_fixture_review
evidence_basis:
  - "Video source metadata recorded in knowledge/sources/videos/youtube-nyfngnzjv3m.md."
  - "Timestamped observations recorded in knowledge/evidence/video-observations/youtube-nyfngnzjv3m-jp-combos.observations.md."
  - "Combo/damage fixture recorded in evals/fixtures/combo-damage/jp-ryusei-nyfngnzjv3m.yaml."
  - "Repo-external scratch media was used only for temporary observation and was not committed."
verification_state: unverified
confidence: 0.45
volatility: patch_sensitive
patch_sensitivity: high
review_status: needs_review
source_refs:
  - label: "Source metadata: YouTube nyFNgnzjV3M"
    path: "knowledge/sources/videos/youtube-nyfngnzjv3m.md"
    accessed_at: "2026-05-04"
  - label: "Video observations: YouTube nyFNgnzjV3M JP combos"
    path: "knowledge/evidence/video-observations/youtube-nyfngnzjv3m-jp-combos.observations.md"
    accessed_at: "2026-05-04"
review_after: "2026-08-04"
summary: "Review holding note for JP combo/damage oracle fixture candidates extracted from limited sections of Ryusei's JP combo guide video."
---

# YouTube nyFNgnzjV3M JP Combo Damage Oracle Fixture Review

This review note tracks JP combo/damage oracle fixture candidates. It is canonical review tracking, but it is not accepted curated knowledge and must not feed generated knowledge references.

## Review Status

- Video source metadata artifact created: yes.
- Timestamped video observation artifact created: yes.
- Combo/damage oracle fixture created: yes.
- Candidate claims artifact created: no; the fixture is eval/test material, not a public answer claim.
- Raw video stored in repo: no.
- Raw frames or screenshots stored in repo: no.
- Full transcript stored in repo: no.
- Scratch/cache policy followed: yes.
- Curated promotion performed: no.
- Generated references changed: no.
- Exact current-system values accepted: no.
- Current verification required before public use: yes.

## Held Observations

The selected source sections appear to demonstrate JP basic light-start routes, jab-rush extension routes, and mid-attack cancel-rush routes. The baseline light-start route has high confidence as an oracle seed because the visible overlay and damage label are clear.

The rush-extension variants remain less certain because the overlay presents alternative route branches and the observed damage labels must be mapped to the exact route variant before they can be used as enabled damage-hidden calculation cases.

The mid-attack expansion adds several coverage candidates with visible damage labels, including cancel-rush, OD Triglav follow-up, and corner-carry route shapes. These remain disabled because the visible overlays use generic starters such as `中攻撃`, inherit route context from prior overlays, or require timing notation such as delayed forward-heavy-kick input.

The following categories stay unresolved:

- Exact normalization from Japanese combo notation to a future machine-readable combo notation contract.
- Whether ambiguous rush-extension cases map to crouching medium punch or back-medium-punch target-combo variants.
- Whether generic starters such as `中攻撃` can be represented safely in damage-hidden calculation inputs.
- Whether OD Triglav follow-up and delayed forward-heavy-kick timing need dedicated notation fields.
- Whether drive-rush state, hit count, spacing, counter state, training settings, or patch state affects the observed damage.
- Whether observed damage values reproduce in-game under the same conditions.
- Whether a future damage calculation engine has sufficient current-system data to compute the oracle values.

## Review Notes

- Observed damage is an eval oracle label only.
- Observed damage is not accepted current-system authority.
- Do not use the fixture to answer public questions about JP combo damage unless a later calculation workflow and current-system authority path define that behavior.
- Do not promote the fixture into `knowledge/curated/`.
- `tests/validation/validate-combo-damage-fixtures.ps1` now checks the fixture boundary and enabled/disabled case fields.

## Workflow Findings

- `workflows/ingest-video.md` and `workflows/media-scratch-cache-policy.md` were enough for source metadata, observation, review, and cleanup boundaries.
- The fixture introduces a new eval support surface under `evals/fixtures/combo-damage/`.
- A future issue should define a combo notation contract before damage-hidden calculation evals depend on ambiguous notation.
- The coverage expansion confirms that route notation, not observed damage visibility, is the main blocker for enabling more damage-hidden eval cases.
