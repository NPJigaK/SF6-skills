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
    "confidence": 0.7,
    "volatility": "stable",
    "patch_sensitivity": "low",
    "review_status": "needs_review",
    "source_refs": [
      {
        "label": "Hameko: SF6 combo scaling article",
        "path": "knowledge/sources/articles/hameko-2023-combo-scaling.md",
        "accessed_at": "2026-05-14"
      }
    ],
    "review_after": "2026-08-01"
  },
  "notes": "Accepted as stable concept only through knowledge/curated/mechanics/combo-scaling.md. Exact scaling sequence, counting rules, exception rules, character/move/control-scheme details, and current-system numeric claims remain excluded from curated knowledge and routed to review-only system-mechanics candidates. This embedded claim stays review-only because claim artifacts must not contain accepted review_status values."
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
        "accessed_at": "2026-05-14"
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
      "The source includes concrete numeric scaling examples; #160 records source-claimed values only as review-only current-fact candidates."
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
        "accessed_at": "2026-05-14"
      }
    ],
    "review_after": "2026-08-01"
  },
  "notes": "Do not promote exact percentages from this article. Source-claimed values are review-only in knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md until a current-system authority path verifies them."
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
        "accessed_at": "2026-05-14"
      }
    ],
    "review_after": "2026-08-01"
  },
  "notes": "Keep exception claims in review. They should not become matchup, combo, or current-system advice without current verification."
}
```

## 2026-05-14 Granular Claim Extraction

The table below splits the article into reviewable claim candidates. It preserves
the source's structure without storing the full article body or long excerpts.
Exact values are recorded only in the review-only current-fact candidate
artifact named in the terminal decision.

Artifact-level `review_status` remains `needs_review` because this file also
contains current-system, exception, and source-claimed mechanics candidates that
remain held. Individual terminal decisions are recorded per claim row.

| Claim ID | claim_kind | Statement | Scope | Evidence metadata | Volatility | Patch sensitivity | Review status | Terminal decision | Target repo surface | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `claim-hameko-combo-scaling-concept-001` | `stable_concept` | Combo damage is adjusted by combo context rather than every hit dealing independent full damage. | General combo-scaling concept. | Hameko article, bounded fresh review on 2026-05-14. | stable | low | needs_review | accepted stable concept | `knowledge/curated/mechanics/combo-scaling.md` | No new curated text needed; claim artifact remains review-only by contract. |
| `claim-hameko-combo-scaling-route-reading-002` | `strategy_or_matchup` | Combo damage interpretation should consider starter, route, system actions, and special-case rules rather than hit count alone. | Strategy/concept explanation for reading combo routes. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | medium | needs_review | accepted only at stable concept level; examples held | curated page plus current-fact candidate | Concrete examples route to current-fact candidates. |
| `claim-hameko-combo-scaling-global-progression-003` | `current_fact` | The article describes a global combo-scaling progression and floor. | Numeric system mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` | See `cf-hameko-global-progression` and `model-hameko-global-sequence`. |
| `claim-hameko-combo-scaling-counting-unit-004` | `current_fact` | The article describes scaling-unit progression by move kind / technique category rather than simple hit count. | Combo-scaling counting rule. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `model-hameko-counting-unit`. |
| `claim-hameko-combo-scaling-hit-vs-type-005` | `current_fact` | The article distinguishes hit count from move/type count when explaining when the floor is reached. | Combo-scaling counting semantics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | Records the `10種類目` vs hit-count distinction as review-only knowledge. |
| `claim-hameko-combo-scaling-multihit-operation-006` | `current_fact` | The article says a single operation that produces multiple hits is often treated as one move for scaling progression. | Multi-hit move counting rule. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `model-hameko-multihit-single-operation`. |
| `claim-hameko-combo-scaling-followup-input-007` | `current_fact` | The article says follow-up attacks caused by additional input may be treated as separate moves and advance scaling. | Follow-up / rekka-like counting rule. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | Source-confirmed examples include Luke OD Rising Upper -> Slam Dunk and Jamie rekka-style sequence. |
| `claim-hameko-combo-scaling-weak-starter-008` | `current_fact` | The article describes a weak-attack starter category that changes follow-up damage. | Starter-related numeric mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-weak-starter`. |
| `claim-hameko-combo-scaling-first-hit-only-009` | `current_fact` | The article groups Drive Impact, cancelable crouching medium kick, and anti-air invincible attacks as first-hit-only scaling cases. | Starter and move-category mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-first-hit-only-starters`. |
| `claim-hameko-combo-scaling-self-move-modifier-010` | `current_fact` | The article describes throw and throw-SA examples where the move itself receives an additional modifier when used in a combo. | Move-specific exception mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-self-move-throw-adders`. |
| `claim-hameko-combo-scaling-multistage-route-011` | `current_fact` | The article describes specific route examples where a move or follow-up advances scaling by more than one step. | Route and move-specific mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-multistage-route-progression`. |
| `claim-hameko-combo-scaling-rush-modifier-012` | `current_fact` | The article describes a Drive Rush / Parry Rush modifier category that applies during combo routes. | System-action mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-rush-modifier`. |
| `claim-hameko-combo-scaling-impact-guard-013` | `current_fact` | The article describes a wall-splat combo modifier after Drive Impact is guarded near the corner. | Drive Impact guard mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-impact-guard`. |
| `claim-hameko-combo-scaling-just-parry-014` | `current_fact` | The article describes a Just Parry follow-up damage modifier category. | Just Parry mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-just-parry`. |
| `claim-hameko-combo-scaling-super-art-015` | `current_fact` | The article describes Super Art minimum guarantees and a separate super-cancel modifier. | Super Art mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-sa-minimum-and-super-cancel`. |
| `claim-hameko-combo-scaling-modern-016` | `current_fact` | The article describes a Modern-control special-button modifier and how it interacts with other modifiers. | Control-scheme mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-modern-special-button`. |
| `claim-hameko-combo-scaling-jamie-017` | `current_fact` | The article describes Jamie drink-level damage modifiers as character-specific combo-scaling context. | Character-specific mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-jamie-drink-modifier`. |
| `claim-hameko-combo-scaling-kimberly-018` | `current_fact` | The article describes Kimberly damage modifiers and examples as character-specific combo-scaling context. | Character-specific mechanics. | Hameko article, bounded fresh review on 2026-05-14. | patch_sensitive | high | needs_review | current-fact/system-mechanics route | current-fact candidate | See `cf-hameko-kimberly-damage-modifier`. |

## 2026-05-14 Source E2E Decisions

#160 performed a fresh bounded review of the article through public no-cookie
access. Raw HTML, full article text, article images, long excerpts, and private
state were not stored.

| Claim | Source E2E terminal decision | Repo surface |
|---|---|---|
| `claim-hameko-combo-scaling-concept-001` | Accepted stable concept already represented. No curated-page text change needed. | `knowledge/curated/mechanics/combo-scaling.md` |
| `claim-hameko-combo-scaling-factors-002` | Split decision: the stable reading concept is already represented in curated knowledge; source-specific examples and exact rule details remain review-only. | `knowledge/curated/mechanics/combo-scaling.md`; `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` |
| `claim-hameko-combo-scaling-percentages-003` and granular current-fact rows | Current-fact/system-mechanics route. Keep as `needs_review`; do not accept exact values from this article. | `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` |
| `claim-hameko-combo-scaling-exceptions-004` and granular exception rows | Current-fact/system-mechanics route. Keep as `needs_review`; do not accept character-, move-, or control-scheme-specific exception details from this article. | `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` |

No unsupported claim was rejected in this source-unit run. The source produced
accepted stable concept routing and review-only current-fact/system-mechanics
routing, but it did not produce a safe rejected-unsafe terminal state.

## Pilot Notes

- Candidate claim count: 4 legacy broad claims plus 18 source-derived granular
  extraction rows.
- Claims newly promoted to curated knowledge in this PR: 0.
- Existing curated stable concept knowledge reaffirmed in this PR: yes.
- Current-fact/system-mechanics route created in this PR: yes, with unverified
  source-claimed values recorded only in review-only candidate rows.
- Generated references updated in this PR: no.
- Exact scaling values stored in curated/generated surfaces in this PR: no.
- Workflow friction: current exact system-mechanics values still do not have an
  accepted authority data surface; they are held in review-only current-fact
  candidates until that authority path exists.
