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
authority_status: review_only
authority_role: review_only_current_fact_candidate
public_answer_allowed: false
generated_reference_allowed: false
accepted_current_fact_authority: false
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

## Source-Derived Combo Scaling Calculation Model

This section is the source-derived mechanics knowledge extracted from the
article. It is not a summary of the article. It is a structured, review-only
model candidate that future combo-damage reasoning can inspect after authority
verification exists.

| candidate_id | knowledge_type | source_claimed_rule_or_value | condition_or_scope | examples | verification_state | review_status | accepted_use_allowed | generated_reference_allowed | reason_for_hold | future_verification_path |
|---|---|---|---|---|---|---|---|---|---|---|
| `model-hameko-global-sequence` | scaling_sequence | Source claims `100% -> 100% -> 80% -> 70% -> 60% -> 50% -> 40% -> 30% -> 20% -> 10%`, then a `10%` floor. | General combo scaling progression by move kind / technique category. | none recorded for this unit | unverified | needs_review | false | false | Community 2023 source; exact sequence must be verified against current system-mechanics authority. | Compare against official/current system data or a reproducible training-mode damage fixture. |
| `model-hameko-counting-unit` | counting_rule | Source claims scaling is managed by move kind / technique category, not by simple hit count; `10種類目` is not identical to tenth hit. | Applies to interpreting progression indices in combo damage scaling. | Article contrasts technique/type progression with hit count. | unverified | needs_review | false | false | Counting semantics are core system mechanics and must not be accepted from a community article alone. | Define a system-mechanics authority surface or verify with controlled multi-hit route tests. |
| `model-hameko-multihit-single-operation` | counting_rule | Source claims a single operation that produces multiple hits is often treated as one move for scaling progression. | Multi-hit moves produced by one input or one move sequence. | Article treats many single-technique multi-hit attacks as one scaling unit. | unverified | needs_review | false | false | Needs route-level observation or authority data before use in combo optimization. | Verify with controlled routes that isolate one-operation multi-hit moves. |
| `model-hameko-additional-input-followup` | counting_rule | Source claims follow-up attacks caused by additional input may be treated as separate moves and advance scaling. | Follow-up / rekka-like sequences and added-input extensions. | Source examples confirmed in review: Luke OD Rising Upper -> Slam Dunk; Jamie rekka-style Flowing Sway Fist sequence. | unverified | needs_review | false | false | Examples are source-claimed and may be patch- or move-version-sensitive. | Verify named routes against current game data and move metadata. |
| `model-hameko-heavy-starter-exceptions` | exception_category | Source claims some moves apply heavy scaling when used as starter. | Starter-heavy categories such as weak attacks, Drive Impact, cancelable crouching medium kick, and anti-air invincible move examples. | Weak attack starter; Drive Impact; cancelable crouching medium kick; anti-air invincible move examples. | unverified | needs_review | false | false | Starter categories and values are exact current-system mechanics. | Verify starter categories and values through authority data or training-mode fixtures. |
| `model-hameko-mid-combo-multistage-exceptions` | exception_category | Source claims some moves may advance scaling by multiple stages even when used mid-combo. | Mid-combo route progression exceptions. | Source-confirmed examples include Marisa and Jamie/Cammy-style route examples at a category level. | unverified | needs_review | false | false | Named move behavior can change and needs exact move/version verification. | Verify each named route through current data or controlled observation. |
| `model-hameko-super-art-minimum-guarantee` | system_mechanics_category | Source claims Super Arts have minimum damage guarantees and a separate super-cancel modifier category. | Super Art scaling floors and super-cancel route behavior. | Super Art level categories and super-cancel examples. | unverified | needs_review | false | false | Minimum guarantee values are exact system mechanics. | Verify against current system data or controlled damage fixtures. |
| `model-hameko-modern-control-modifier` | control_scheme_modifier | Source claims Modern special-button moves carry a separate modifier and interact with other modifiers and Super Art floors. | Modern-control special-button route behavior. | Source-confirmed Modern special-button category and stacked-modifier example. | unverified | needs_review | false | false | Control-scheme modifiers are current-system facts. | Verify with Modern-control route fixtures. |
| `model-hameko-character-move-exceptions` | exception_category | Source claims some character, move, and control-scheme examples are exception categories rather than stable general rules. | Character-specific, move-specific, and control-scheme-specific exceptions. | Source-confirmed examples include Jamie, Kimberly, Luke, and throw/throw-SA categories. | unverified | needs_review | false | false | Character and move examples are patch-sensitive and source-local until verified. | Split into character/move-specific authority rows or test fixtures before accepted use. |

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
