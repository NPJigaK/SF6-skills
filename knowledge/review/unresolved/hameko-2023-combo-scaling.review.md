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

## 2026-05-14 Tranche 1 Fresh Content Review

As part of #158 Tranche 1, the article URL was accessed through public
no-cookie HTML and reviewed at a bounded, paraphrased category level. The raw
HTML, full article body, article images, and long verbatim excerpts were not
stored in the repository.

The fresh review confirmed the existing routing:

- The source is suitable for explaining the stable concept that combo damage is
  adjusted by combo context rather than every hit being treated as independent
  full damage.
- The source also discusses numeric scaling rules, system-action modifiers,
  super-art guarantee behavior, Modern-control modifiers, and character-specific
  exception categories.
- Those numeric and exception categories remain patch-sensitive
  current-system candidates and are not accepted into curated knowledge here.
- `knowledge/curated/mechanics/combo-scaling.md` already holds the accepted
  stable concept boundary; this Tranche 1 review did not create new curated
  knowledge.

Review decision for this tranche: keep the candidate claims in `needs_review`
unless and until a dedicated current-system or mechanics-fact workflow verifies
the numeric and exception details. No exact values from the article were copied
into the review note.

## Workflow Findings

- The source and candidate-claim locations work for a Japanese article with mixed concept and numeric/system content.
- `knowledge/review/unresolved/` can hold a review-only note using the existing knowledge-page metadata model.
- There is no dedicated validator yet for `knowledge/sources/` source artifacts or `knowledge/evidence/claims/` claim artifacts.
- System-mechanics numeric facts may need a future workflow distinct from frame-current runtime assets.
