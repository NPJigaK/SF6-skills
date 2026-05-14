---
id: claims-hameko-2023-combo-scaling
title: "Candidate claims from Hameko 2023 combo scaling article"
source_kind: community
source_role: japanese_article_ingest_pilot_claims
verification_state: partially_verified
confidence: 0.45
volatility: patch_sensitive
patch_sensitivity: high
review_status: needs_review
review_after: "2026-08-01"
source_refs:
  - label: "Source metadata: Hameko 2023 combo scaling"
    path: "knowledge/sources/articles/hameko-2023-combo-scaling.md"
    url: "https://note.com/hameko/n/n933d2911d655"
    accessed_at: "2026-05-14"
---

# Candidate Claims

These claims are extracted for review only. They are not accepted curated knowledge and must not feed generated references until reviewed and promoted through the normal process.

## Claim 1

```json
{
  "id": "claim-hameko-combo-scaling-concept-001",
  "claim_kind": "stable_concept",
  "statement": "Combo scaling is a system that adjusts damage during a combo rather than treating every hit as independent full damage.",
  "scope": "General SF6 system concept.",
  "evidence": {
    "source_kind": "community",
    "source_role": "japanese_article_supporting_context",
    "evidence_basis": [
      "Source summary from Hameko's 2023 combo scaling article."
    ],
    "verification_state": "partially_verified",
    "confidence": 0.45,
    "volatility": "stable",
    "patch_sensitivity": "medium",
    "review_status": "needs_review",
    "source_refs": [
      {
        "label": "Hameko: SF6 combo scaling article",
        "path": "knowledge/sources/articles/hameko-2023-combo-scaling.md",
        "accessed_at": "2026-05-01"
      }
    ],
    "review_after": "2026-08-01"
  },
  "notes": "Candidate stable concept only. Do not include concrete scaling percentages unless separately verified and routed through an appropriate current/system-fact process."
}
```

## Claim 2

```json
{
  "id": "claim-hameko-combo-scaling-factors-002",
  "claim_kind": "strategy_or_matchup",
  "statement": "SF6 combo damage can depend on more than hit count; starter type, route choice, system actions, and special-case rules may affect damage outcomes.",
  "scope": "General strategy/system explanation for reading combo damage behavior.",
  "evidence": {
    "source_kind": "community",
    "source_role": "japanese_article_supporting_context",
    "evidence_basis": [
      "Source summary from Hameko's 2023 combo scaling article."
    ],
    "verification_state": "partially_verified",
    "confidence": 0.4,
    "volatility": "patch_sensitive",
    "patch_sensitivity": "high",
    "review_status": "needs_review",
    "source_refs": [
      {
        "label": "Hameko: SF6 combo scaling article",
        "path": "knowledge/sources/articles/hameko-2023-combo-scaling.md",
        "accessed_at": "2026-05-01"
      }
    ],
    "review_after": "2026-08-01"
  },
  "notes": "Keep this as a review candidate. It may become stable concept wording later, but examples and exact rules remain patch-sensitive."
}
```

## Claim 3

```json
{
  "id": "claim-hameko-combo-scaling-percentages-003",
  "claim_kind": "current_fact",
  "statement": "Specific combo-scaling percentages and system-action modifiers described by the article require current verification before public use.",
  "scope": "Numeric SF6 system mechanics.",
  "evidence": {
    "source_kind": "community",
    "source_role": "japanese_article_supporting_context",
    "evidence_basis": [
      "The source includes concrete numeric scaling examples, but this pilot intentionally does not store or accept those values."
    ],
    "verification_state": "unverified",
    "confidence": 0.25,
    "volatility": "patch_sensitive",
    "patch_sensitivity": "high",
    "review_status": "needs_review",
    "source_refs": [
      {
        "label": "Hameko: SF6 combo scaling article",
        "path": "knowledge/sources/articles/hameko-2023-combo-scaling.md",
        "accessed_at": "2026-05-01"
      }
    ],
    "review_after": "2026-08-01"
  },
  "notes": "Do not promote exact percentages from this article. Future work may need a dedicated system-mechanics numeric-fact workflow separate from frame-current assets."
}
```

## Claim 4

```json
{
  "id": "claim-hameko-combo-scaling-exceptions-004",
  "claim_kind": "current_fact",
  "statement": "Character-specific, move-specific, and control-scheme-specific combo-scaling exceptions described by the article require current verification before public use.",
  "scope": "Patch-sensitive SF6 exception handling.",
  "evidence": {
    "source_kind": "community",
    "source_role": "japanese_article_supporting_context",
    "evidence_basis": [
      "The source discusses specific exception categories, but this pilot treats them as review-only."
    ],
    "verification_state": "unverified",
    "confidence": 0.25,
    "volatility": "patch_sensitive",
    "patch_sensitivity": "high",
    "review_status": "needs_review",
    "source_refs": [
      {
        "label": "Hameko: SF6 combo scaling article",
        "path": "knowledge/sources/articles/hameko-2023-combo-scaling.md",
        "accessed_at": "2026-05-01"
      }
    ],
    "review_after": "2026-08-01"
  },
  "notes": "Keep exception claims in review. They should not become matchup, combo, or current-system advice without current verification."
}
```

## 2026-05-14 Source E2E Decisions

#160 performed a fresh bounded review of the article through public no-cookie
access. Raw HTML, full article text, article images, long excerpts, and private
state were not stored.

| Claim | Source E2E terminal decision | Repo surface |
|---|---|---|
| `claim-hameko-combo-scaling-concept-001` | Accepted stable concept already represented. No curated-page text change needed. | `knowledge/curated/mechanics/combo-scaling.md` |
| `claim-hameko-combo-scaling-factors-002` | Split decision: the stable reading concept is already represented in curated knowledge; source-specific examples and exact rule details remain review-only. | `knowledge/curated/mechanics/combo-scaling.md`; `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` |
| `claim-hameko-combo-scaling-percentages-003` | Current-fact/system-mechanics route. Keep as `needs_review`; do not accept exact values from this article. | `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` |
| `claim-hameko-combo-scaling-exceptions-004` | Current-fact/system-mechanics route. Keep as `needs_review`; do not accept character-, move-, or control-scheme-specific exception details from this article. | `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` |

No unsupported claim was rejected in this source-unit run. The source produced
accepted stable concept routing and review-only current-fact/system-mechanics
routing, but it did not produce a safe rejected-unsafe terminal state.

## Pilot Notes

- Candidate claim count: 2 concept/strategy candidates and 2 current-system candidates.
- Claims newly promoted to curated knowledge in this PR: 0.
- Existing curated stable concept knowledge reaffirmed in this PR: yes.
- Current-fact/system-mechanics route created in this PR: yes.
- Generated references updated in this PR: no.
- Exact scaling values stored in this PR: no.
- Workflow friction: current exact system-mechanics values still do not have an
  accepted authority data surface; they are held in review-only current-fact
  candidates until that authority path exists.
