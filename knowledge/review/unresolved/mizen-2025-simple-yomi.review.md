---
id: sf6-review-mizen-2025-simple-yomi
title: Mizen 2025 Simple Yomi Article Pilot Review
claim_kind: unresolved
source_kind: community
source_role: hermes_assisted_japanese_article_ingest_review
evidence_basis:
  - "Source summary recorded in knowledge/sources/articles/mizen-2025-simple-yomi.md."
  - "Candidate claims recorded in knowledge/evidence/claims/mizen-2025-simple-yomi.claims.md."
  - "Hermes-assisted decomposition was manually reviewed into repo artifact form."
  - "No claim was promoted to curated knowledge during the pilot."
verification_state: partially_verified
confidence: 0.4
volatility: patch_sensitive
patch_sensitivity: medium
review_status: needs_review
source_refs:
  - label: "Source metadata: Mizen 2025 simple yomi"
    path: "knowledge/sources/articles/mizen-2025-simple-yomi.md"
    accessed_at: "2026-05-01"
  - label: "Candidate claims: Mizen 2025 simple yomi"
    path: "knowledge/evidence/claims/mizen-2025-simple-yomi.claims.md"
    accessed_at: "2026-05-01"
review_after: "2026-08-01"
summary: "Review holding note for a Hermes-assisted Japanese article ingest pilot about simplifying SF6 decision-making; source and claims remain review-only."
---

# Mizen 2025 Simple Yomi Article Pilot Review

This review note tracks a Hermes-assisted Japanese article ingest pilot. It is canonical review tracking, but it is not accepted curated knowledge and must not feed generated knowledge references.

## Review Status

- Source metadata artifact created: yes.
- Candidate claims artifact created: yes.
- Hermes used as maintainer harness: yes.
- Hermes memory treated as canonical: no.
- Image-aware observation pass performed: yes.
- Article images or screenshots stored in repo: no.
- Curated promotion performed: no.
- Generated references changed: no.
- Exact current values stored: no.
- Current verification required for setup-specific interpretations: yes.

## Held Claims

The article is useful as a Japanese source for strategy framing around simplifying SF6 decision-making. It separates main options from additional options that can disrupt those options, using okizeme examples.

The following categories stay unresolved:

- Character-specific okizeme coverage.
- Move-specific defensive or offensive interactions.
- Setup-specific reliability.
- Timing, spacing, punish, or current-patch interaction claims.
- Image-derived readings of visual matchup or payoff tables.
- Japanese terminology normalization for future curated wording.

## Review Notes

- The high-level framing may later support strategy or concept knowledge after review.
- Accepted wording should avoid implying a universal flowchart or guaranteed answer.
- Claims involving command grabs, invincible reversals, throw, shimmy, backdash, or jump should remain scoped to strategy framing unless independently verified.
- Image-derived observations should remain `observation` / `needs_review` until reviewed against the full source context and any relevant gameplay verification.
- Image-derived Claim 7 is grounded only in the Image 1 through Image 6 observation records in `docs/testing/smoke-runs/2026-05-02-image-aware-japanese-ingest.md`.
- The article should not be used as final public answer evidence until relevant claims are reviewed and promoted into an appropriate canonical surface.

## Workflow Findings

- Hermes helped produce candidate claim categories quickly, especially the split between high-level strategy framing and setup-specific hold conditions.
- Hermes output needed manual path correction because it proposed noncanonical review paths.
- Hermes output correctly identified that memory is not canonical.
- A dedicated ingest profile was created, but profile-scoped Hermes runtime authentication had not been completed there. The actual run used the existing isolated smoke profile with memory and curator disabled.
- Follow-up validation for `knowledge/sources/` source artifacts and `knowledge/evidence/claims/` claim artifacts now exists in `tests/validation/validate-ingest-artifacts.ps1`.
- The image-aware pass confirmed that visual examples can add useful observation context. Six article images were inspected through a repo-external temporary vision-capable path, while Hermes `sf6ingest` had browser available and Hermes vision unavailable in `hermes doctor`; future Hermes-specific image ingest should verify Hermes vision separately before claiming Hermes vision extraction.
