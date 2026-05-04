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

## Combo Notation Contract Review

The fixture candidates were re-reviewed against `contracts/combo-notation.md` on 2026-05-04.

| Case | Contract verdict | Reason |
|---|---|---|
| `jp-basic-light-stribog-001` | keep enabled | Exact starter and route order are visible enough for the current fixture layer. The `>` separator is acceptable as observed hit/action order under the contract. |
| `jp-basic-light-rush-extension-1482` | keep disabled | The overlay lists alternative branches and normalized notation is unresolved. Branch notation is allowed only for disabled candidates. |
| `jp-basic-light-rush-extension-1527` | keep disabled | The route is likely a crouching-medium-punch branch, but the branch mapping is still inferred rather than reviewed as exact. |
| `jp-mid-rush-triglav-1824` | keep disabled | `medium_normal` represents generic `中攻撃`. Generic starters are not precise enough for enabled damage-hidden eval. |
| `jp-mid-rush-od-triglav-3260` | keep disabled | The route has generic starter context and inherited OD Triglav follow-up context. The full route-to-damage mapping is not reviewed. |
| `jp-mid-corner-carry-rush-fhk-2763` | keep disabled | The route has generic starter context, corner-carry context, and delayed `Drive Rush 6HK` timing not yet representable as calculator input. |
| `jp-mid-position-carry-1484` | keep disabled | The inspected frame has a visible damage label, but the route overlay is incomplete and position/carry context remains unresolved. |

No additional disabled cases were enabled in this review. The next enabling step requires exact starter or branch review, not more video candidates.

## Exact Starter And Branch Mapping Re-Review

The existing disabled candidates were re-inspected on 2026-05-04 with temporary repo-external media. The review focused only on the existing candidate sections and did not add new video sources or new coverage chapters.

| Case | Re-review result | Reason |
|---|---|---|
| `jp-basic-light-rush-extension-1482` | keep disabled | Damage label and branch overlay are clear, but visible evidence does not uniquely map `1482` to either `しゃがみ中P` or `引き中Pタゲコン`. |
| `jp-basic-light-rush-extension-1527` | keep disabled | The crouching-medium-punch branch remains plausible from commentary/context, but the branch-to-damage mapping is still inferred. |
| `jp-mid-rush-triglav-1824` | keep disabled | Mid-attack route and damage context remain clear, but `中攻撃` was not resolved to an exact starter token. |
| `jp-mid-rush-od-triglav-3260` | keep disabled | OD follow-up context was clarified as `OD Triglav > Triglav`, but the route still inherits generic starter context. |
| `jp-mid-corner-carry-rush-fhk-2763` | keep disabled | Delayed `Drive Rush 6HK` wording was confirmed, but generic starter, corner-carry context, and timing semantics remain unresolved. |
| `jp-mid-position-carry-1484` | keep disabled | A complete route overlay was still not visible for the `1484` damage label. |

No case was newly enabled. The next practical step is either a more targeted manual branch/starter review with stronger evidence, or a separate combo damage calculation input/output contract that can describe unresolved requirements explicitly.

## Review Notes

- Observed damage is an eval oracle label only.
- Observed damage is not accepted current-system authority.
- Do not use the fixture to answer public questions about JP combo damage unless a later calculation workflow and current-system authority path define that behavior.
- Do not promote the fixture into `knowledge/curated/`.
- `tests/validation/validate-combo-damage-fixtures.ps1` now checks the fixture boundary and enabled/disabled case fields.
- `contracts/combo-notation.md` now explains why generic starters, inherited route context, unresolved branches, and timing ambiguity keep candidates disabled.

## Workflow Findings

- `workflows/ingest-video.md` and `workflows/media-scratch-cache-policy.md` were enough for source metadata, observation, review, and cleanup boundaries.
- The fixture introduces a new eval support surface under `evals/fixtures/combo-damage/`.
- `contracts/combo-notation.md` now defines the notation review boundary before damage-hidden calculation evals depend on ambiguous notation.
- The coverage expansion confirms that route notation, not observed damage visibility, is the main blocker for enabling more damage-hidden eval cases.
- The exact starter/branch re-review confirms that observed damage labels alone are still insufficient for enabling additional damage-hidden eval cases.
