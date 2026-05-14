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
- Current-fact/system-mechanics route created: yes.
- Generated references changed: no.
- Exact scaling values stored: no.
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
