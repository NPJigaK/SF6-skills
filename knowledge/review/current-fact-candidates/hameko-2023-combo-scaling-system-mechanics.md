---
id: current-fact-candidate-hameko-2023-combo-scaling-system-mechanics
title: Hameko 2023 Combo Scaling System-Mechanics Candidates
claim_kind: current_fact
source_kind: community
source_role: japanese_article_system_mechanics_candidate
evidence_basis:
  - "Bounded source E2E review of the Hameko 2023 combo-scaling article on 2026-05-14."
  - "Candidate claims recorded in knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md."
  - "Stable concept boundary recorded in knowledge/curated/mechanics/combo-scaling.md."
verification_state: unverified
confidence: 0.25
volatility: patch_sensitive
patch_sensitivity: high
review_status: needs_review
source_refs:
  - label: "Source metadata: Hameko 2023 combo scaling"
    path: "knowledge/sources/articles/hameko-2023-combo-scaling.md"
    accessed_at: "2026-05-14"
  - label: "Candidate claims: Hameko 2023 combo scaling"
    path: "knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md"
    accessed_at: "2026-05-14"
  - label: "Review note: Hameko 2023 combo scaling"
    path: "knowledge/review/unresolved/hameko-2023-combo-scaling.review.md"
    accessed_at: "2026-05-14"
review_after: "2026-08-14"
summary: "Review-only route for combo-scaling exact system-mechanics categories encountered during #160 source E2E."
---

# Hameko 2023 Combo Scaling System-Mechanics Candidates

This artifact is a review-only current-fact candidate. It is not final public
answer evidence, must not feed generated knowledge references, is not accepted
curated knowledge, and must be resolved into the current-fact data surfaces or
kept on hold.

## Source E2E Context

#160 fetched and reviewed the Hameko combo-scaling article through public
no-cookie access. The raw article body, raw HTML, article images, and long
verbatim excerpts were not stored in the repository.

The source supports the stable concept that combo damage is adjusted by combo
context. That stable concept is handled by
`knowledge/curated/mechanics/combo-scaling.md`.

The source also discusses exact system-mechanics categories that are not safe to
accept from a community article alone. #160 records those source-claimed values
only as review-only candidates so a future reviewer can verify or reject them.

## Candidate Categories

These categories require current-fact or system-mechanics review before public
use:

- global combo-scaling progression and route-level calculation behavior
- starter-related scaling and system-action-related modifiers
- super-art minimum-damage guarantee behavior
- Modern-control modifier behavior
- character-specific damage or scaling exceptions
- move-specific or route-specific exception behavior
- current-patch behavior that depends on live game data or current official
  material

## Source-Claimed System Mechanics Candidates

These values are source-claimed and unverified. They are recorded so future
review has concrete targets; they are not accepted current facts and must not be
used in curated knowledge, generated references, or public answers.

| candidate_id | category | source_claimed_value_recorded | source_claimed_value | condition_or_scope | verification_state | accepted_use_allowed | reason_for_hold |
|---|---|---|---|---|---|---|---|
| `cf-hameko-global-progression` | global combo-scaling progression | yes | `100 -> 100 -> 80 -> 70 -> 60 -> 50 -> 40 -> 30 -> 20 -> 10`; floor claimed as `10%` | Article's general combo-scaling overview; framed as type/progression based rather than simple hit count. | unverified | false | Community article from 2023; needs current system-mechanics authority or reproducible verification. |
| `cf-hameko-weak-starter` | weak-attack starter category | yes | follow-up after weak starter claimed as `90%`; third hit claimed as normal `80%` | Weak attack used as combo starter, including chain/counter-hit follow-up contexts. | unverified | false | Starter-specific value must be checked against current game data. |
| `cf-hameko-first-hit-only-starters` | first-hit-only starter category | yes | Drive Impact / cancelable crouching medium kick category claimed as `80%` on the next attack and `70%` on the third attack; anti-air invincible super-cancel context includes a claimed `70%` next-hit case and `60%` SA3 example | Article groups Drive Impact, cancelable crouching medium kick, and anti-air invincible attacks as first-hit-only modifier examples. | unverified | false | Move membership, exact values, and super-cancel interaction need current authority review. |
| `cf-hameko-self-move-throw-adders` | self-move modifier / throw and throw-SA examples | yes | throw/SA adders are claimed in example bands of `5%`, `10%`, `15%`, and `20%`; normal throw in combo is claimed as adding `20%` to itself | Throw-like moves and throw Super Arts when inserted into a combo. | unverified | false | Move-specific exception values need current-game verification. |
| `cf-hameko-multistage-route-progression` | route-level multi-step progression | yes | examples include claimed progressions such as `100 -> 100 -> 80 -> 70 -> 50` and `100 -> 90 -> 70` | Specific follow-up and multi-hit route examples cited by the article. | unverified | false | Route examples are source-local and need reproducible validation. |
| `cf-hameko-rush-modifier` | Drive Rush / Parry Rush modifier | yes | rush modifier claimed as `85%`; example combination `80% * 85% = 68%`; modifier claimed as applying once per combo | Combo route uses Drive Rush or Parry Rush during the combo rather than starting from a Parry Rush attack. | unverified | false | System-action multiplier, once-per-combo behavior, and chip-damage interaction need current authority review. |
| `cf-hameko-impact-guard` | Drive Impact guard wall-splat modifier | yes | guarded wall-splat modifier claimed as multiplicative `80%`; example progression `80 -> 80 -> 64 -> 56`; floor claimed as `8%` | Drive Impact is guarded near the corner and causes wall splat into a combo. | unverified | false | Guarded-impact distinction and floor value require current verification. |
| `cf-hameko-just-parry` | Just Parry punish modifier | yes | Just Parry follow-up modifier claimed as `50%`; example progression `50 -> 50 -> 40 -> 35` | Attack lands during opponent recovery after a successful Just Parry. | unverified | false | Exact modifier and route behavior require current verification. |
| `cf-hameko-sa-minimum-and-super-cancel` | Super Art minimum guarantee and super-cancel modifier | yes | minimum guarantee claimed as Lv1 `30%`, Lv2 `40%`, Lv3/CA `50%`; super cancel claimed as adding `10%` to the next Super Art / CA | Super Art scaling floors and Super Art performed via super cancel. | unverified | false | Minimum guarantee and cancel modifier are exact system mechanics. |
| `cf-hameko-modern-special-button` | Modern-control special-button modifier | yes | special-button move modifier claimed as `80%`; an extreme stacked example is claimed as `3%`; Super Art floors claimed to remain at Lv1 `30%`, Lv2 `40%`, Lv3/CA `50%` | Modern control special-button move inputs in combos. | unverified | false | Control-scheme modifier values and floor interactions require current verification. |
| `cf-hameko-jamie-drink-modifier` | Jamie drink-level damage modifier | yes | drink-level modifiers claimed as Lv0 `90%`, Lv1 `95%`, Lv2 `100%`, Lv3 `105%`, Lv4 `110%`; example combined route claimed as `61%` | Jamie damage output by drink level and combo route context. | unverified | false | Character-resource values are current character mechanics, not stable curated knowledge. |
| `cf-hameko-kimberly-damage-modifier` | Kimberly damage modifier examples | yes | Lv3/CA state claimed as `111%`; baseline damage described as about `90%` of other characters, with an example throw comparison `1082` vs `1200` | Kimberly character-state and baseline damage examples. | unverified | false | Character-state and example damage values require current authority review. |

## Terminal State

Terminal state for #160: current-fact/system-mechanics route, `needs_review`.
This route is reviewable because source-claimed values were captured above, but
it remains non-authoritative.

The repo already has `workflows/system-mechanics-fact-workflow.md`, which is
sufficient to route these candidates without accepting them into
`knowledge/curated/`.

Accepted use is blocked until one of these is true:

- a value is available through packaged frame-current data as a move-specific
  field; or
- a later accepted system-mechanics authority surface is defined and populated.

## Review Notes

- Do not use this artifact as final public answer evidence.
- Do not infer exact current system values from the source article alone.
- Do not copy these categories into generated concept references as exact facts.
- The stable teaching concept may stay in curated knowledge, but exact values,
  formulas, and exception rules remain held.
