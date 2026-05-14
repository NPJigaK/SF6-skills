---
id: sf6-review-hameko-2023-combo-scaling
title: Hameko 2023 Combo Scaling Article Pilot Review
claim_kind: unresolved
source_kind: community
source_role: japanese_article_ingest_pilot_review
evidence_basis:
  - "Source summary recorded in knowledge/sources/articles/hameko-2023-combo-scaling.md."
  - "Candidate claims recorded in knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md."
  - "Stable concept boundary recorded in knowledge/curated/mechanics/combo-scaling.md."
  - "System-mechanics current-fact candidates recorded in knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md."
verification_state: partially_verified
confidence: 0.35
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
  - label: "System-mechanics current-fact candidates: Hameko 2023 combo scaling"
    path: "knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md"
    accessed_at: "2026-05-14"
review_after: "2026-08-01"
summary: "Review note for #160 source E2E on a Japanese combo-scaling article; stable concept is accepted in curated knowledge while exact system-mechanics categories remain review-only."
---

# Hameko 2023 Combo Scaling Article Pilot Review

This review note tracks a Japanese article ingest pilot. It is canonical review tracking, but it is not accepted curated knowledge and must not feed generated knowledge references.

## Review Status

- Source metadata artifact created: yes.
- Candidate claims artifact created: yes.
- Stable curated concept already represented: yes, in `knowledge/curated/mechanics/combo-scaling.md`.
- New curated promotion performed in #160: no.
- Current-fact/system-mechanics route created: yes, with review-only source-claimed values.
- Generated references changed: no.
- Exact scaling values stored in curated/generated surfaces: no.
- Source-claimed exact values stored as review-only current-fact candidates: yes.
- Current verification required: yes.

## Held Claims

The article is useful as a Japanese source for decomposing combo-scaling knowledge into stable concepts, route/system explanations, and review-only numeric or exception claims.

The following categories stay unresolved:

- Concrete scaling percentages.
- Weak-attack scaling, system-action scaling, and super-art minimum-damage guarantee details.
- Character-specific and move-specific exceptions.
- Control-scheme-related damage modifiers.
- Any current-patch statement that depends on live game behavior or current official material.

## Review Notes

- Stable concept candidates may later support a curated mechanics page, but this PR does not create one.
- Numeric and exception claims may need a dedicated system-mechanics fact workflow because they are not ordinary move-frame facts.
- Future review should decide whether combo-scaling facts belong in a mechanics-specific contract, a reproducible observation workflow, or a current-system data surface.
- The article should not be used as final public answer evidence until relevant claims are reviewed and promoted into an appropriate canonical surface.

## 2026-05-14 Source E2E Review

This section records #160 one-source E2E execution for
`article-live-japanese-01`.

| Field | Result |
|---|---|
| Source URL | `https://note.com/hameko/n/n933d2911d655` |
| Access method | Public no-cookie article access. |
| Fresh content review occurred? | yes, bounded category-level article review. |
| Raw article body committed? | no. |
| Raw HTML committed? | no. |
| Article images committed? | no. |
| Long excerpts copied? | no. |
| Credentials/cookies/browser profile used? | no. |
| Public adapter behavior changed? | no. |

The source E2E review confirmed that the existing artifact split is the right
terminal routing for this article:

- Stable concept: accepted through existing
  `knowledge/curated/mechanics/combo-scaling.md`. No curated text change was
  needed in this PR.
- Strategy/concept explanation: partially represented by the existing curated
  stable concept page; source-specific examples remain review-only.
- Numeric and current-system categories: routed to
  `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md`.
- Character-, move-, and control-scheme-specific exception categories: routed to
  the same current-fact/system-mechanics candidate artifact.
- Rejected unsafe: none found. No rejection was fabricated for coverage.

## Article Structure And Claim Extraction Map

This map records the article structure observed during #160 bounded review. It
does not preserve the full article body, raw HTML, images, or long excerpts.
Rows with `source_claimed_value_recorded: yes` point to review-only entries in
`knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md`.

| article_topic_id | paraphrased_source_claim | specificity_level | source_claimed_value_recorded | terminal_decision | repo_surface | why |
|---|---|---|---|---|---|---|
| `topic-stable-combo-scaling-concept` | Combo damage is adjusted by combo context; not every hit should be read as independent full damage. | stable_concept | no | accepted stable curated knowledge | `knowledge/curated/mechanics/combo-scaling.md` | Safe concept already exists without exact values. |
| `topic-basic-global-scaling` | The article describes a global progression and floor for combo damage scaling. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` | Exact progression/floor values are patch-sensitive and need authority review. |
| `topic-route-reading-concept` | Starter, route, hit progression, system actions, and exception categories can change how damage should be read. | stable_concept | no | accepted only at stable concept level; examples held | curated page plus current-fact candidate | The broad reading concept is useful, but article examples include exact mechanics. |
| `topic-starter-related-scaling` | Some starter categories apply special scaling when they begin the combo. | conditional_rule | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Starter-specific details are exact current-system mechanics. |
| `topic-weak-attack-starter` | The article gives a weak-attack starter category and follow-up damage behavior. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Source-claimed values need current verification before public use. |
| `topic-first-hit-only-starters` | Drive Impact, cancelable crouching medium kick, and anti-air invincible attacks are discussed as first-hit-only scaling cases. | conditional_rule | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Move category membership and values are patch-sensitive. |
| `topic-route-hit-count-behavior` | The article says some moves or follow-ups advance scaling by more than one step even inside a route. | exception_category | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Route examples are useful for review but not authority. |
| `topic-drive-rush-system-action` | Drive Rush / Parry Rush attacks can add a system-action modifier during combo routes. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Exact multiplier and edge cases need authority review. |
| `topic-drive-impact-guard` | Drive Impact guard wall-splat routes are described as having a distinct guarded-impact modifier. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Guard-hit distinction and floor values are current-system facts. |
| `topic-just-parry` | Just Parry punish follow-ups are described as carrying a large modifier. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Exact modifier and route behavior are current-system facts. |
| `topic-super-art-minimum-guarantee` | Super Art minimum guarantees and super-cancel behavior are described separately from ordinary scaling. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Minimum guarantee values and super-cancel details need authority review. |
| `topic-modern-control-modifier` | Modern special-button use is described as adding a separate modifier while Super Art minimum guarantees still matter. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Control-scheme modifier values are patch-sensitive current facts. |
| `topic-character-specific-exception` | The article treats character-specific damage modifiers as a separate exception category. | exception_category | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Character-specific values must not be accepted from this article alone. |
| `topic-jamie-exception` | Jamie drink level is described as changing damage output by level. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Character-resource values require current authority review. |
| `topic-kimberly-exception` | Kimberly is described as having different damage behavior after Lv3/CA and different baseline damage examples. | exact_numeric | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Character-state values and examples require current authority review. |
| `topic-move-specific-exception` | The article names move-specific examples for throw, follow-up, and special move scaling exceptions. | example | yes | current-fact/system-mechanics route, `needs_review` | current-fact candidate | Move-specific exceptions need current-game verification. |
| `topic-current-version-caveat` | The article is a 2023 source and includes an update-style caveat around exception coverage. | unclear | no | unresolved / needs_review | review note | The source may be stale; missing or changed exceptions must be checked elsewhere. |

## Terminal Decisions

| Candidate | Decision | Reason |
|---|---|---|
| Stable combo-scaling concept | accepted stable curated knowledge | Existing curated page already explains the safe stable concept without exact values. |
| Combo-damage factor explanation | accepted only at stable concept level; examples held | The broad reading concept is safe, but concrete examples and exact rules remain patch-sensitive. |
| Numeric scaling and system-action categories | current-fact/system-mechanics route, `needs_review` | Exact values and formulas require a dedicated current-system authority path or packaged current-fact field. |
| Exception categories | current-fact/system-mechanics route, `needs_review` | Character-, move-, and control-scheme-specific exception details are patch-sensitive and not accepted from this article alone. |

## Workflow Findings

- The source and candidate-claim locations work for a Japanese article with mixed concept and numeric/system content.
- `knowledge/review/unresolved/` can hold a review-only note using the existing knowledge-page metadata model.
- There is no dedicated validator yet for `knowledge/sources/` source artifacts or `knowledge/evidence/claims/` claim artifacts; #160 did not add one because no concrete validator failure was observed.
- `workflows/system-mechanics-fact-workflow.md` is sufficient for this source-unit run. Accepted system-mechanics exact values still need a future authority surface before they can become runtime-answer authority.
