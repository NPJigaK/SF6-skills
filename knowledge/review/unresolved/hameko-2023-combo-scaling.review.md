---
id: sf6-review-hameko-2023-combo-scaling
title: Hameko 2023 Combo Scaling Article Pilot Review
claim_kind: unresolved
source_kind: community
source_role: japanese_article_ingest_pilot_review
evidence_basis:
  - "Source summary recorded in knowledge/sources/articles/hameko-2023-combo-scaling.md."
  - "Candidate claims recorded in knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md."
  - "No claim was promoted to curated knowledge during the pilot."
verification_state: partially_verified
confidence: 0.35
volatility: patch_sensitive
patch_sensitivity: high
review_status: needs_review
source_refs:
  - label: "Source metadata: Hameko 2023 combo scaling"
    path: "knowledge/sources/articles/hameko-2023-combo-scaling.md"
    accessed_at: "2026-05-01"
  - label: "Candidate claims: Hameko 2023 combo scaling"
    path: "knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md"
    accessed_at: "2026-05-01"
review_after: "2026-08-01"
summary: "Review holding note for a Japanese article ingest pilot about combo scaling; source and claims remain review-only."
---

# Hameko 2023 Combo Scaling Article Pilot Review

This review note tracks a Japanese article ingest pilot. It is canonical review tracking, but it is not accepted curated knowledge and must not feed generated knowledge references.

## Review Status

- Source metadata artifact created: yes.
- Candidate claims artifact created: yes.
- Curated promotion performed: no.
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

## Workflow Findings

- The source and candidate-claim locations work for a Japanese article with mixed concept and numeric/system content.
- `knowledge/review/unresolved/` can hold a review-only note using the existing knowledge-page metadata model.
- There is no dedicated validator yet for `knowledge/sources/` source artifacts or `knowledge/evidence/claims/` claim artifacts.
- System-mechanics numeric facts may need a future workflow distinct from frame-current runtime assets.
