---
id: claims-youtube-vcpzwawrrla-terminology
title: "Candidate terminology claims from YouTube VCPzwAwRrLA"
source_kind: community
source_role: commentary_only_terminology_claims
verification_state: partially_verified
confidence: 0.45
volatility: stable
patch_sensitivity: medium
review_status: needs_review
review_after: "2026-08-14"
source_refs:
  - label: "Source metadata: YouTube VCPzwAwRrLA"
    path: "knowledge/sources/videos/youtube-vcpzwawrrla.md"
    url: "https://www.youtube.com/watch?v=VCPzwAwRrLA"
    accessed_at: "2026-05-14"
  - label: "Video observation: YouTube VCPzwAwRrLA terminology"
    path: "knowledge/evidence/video-observations/youtube-vcpzwawrrla-terminology.observations.md"
    accessed_at: "2026-05-14"
---

# Candidate Claims

These claims are extracted for review only. They are not accepted curated knowledge and must not feed generated references until reviewed and promoted through the normal process.

The source was analyzed for terminology and concept knowledge units, not for a
video summary. Temporary caption review happened outside the repository; the raw
captions and transcript-like text are not stored here.

## Caption-Level Review Boundary

- Claims are derived from temporary auto-generated caption-level content review.
- Direct audio reviewed? no.
- Direct video reviewed? no.
- Claim wording is paraphrased; exact source wording is not preserved.
- Official terminology authority is not claimed.
- Automatic captions can misrecognize Japanese terms, omit speaker nuance, or
  segment commentary imperfectly.
- Any term requiring exact definition wording, official terminology authority,
  move-specific current behavior, or exact setup validity remains `needs_review`.

## Source-Derived Terminology Units

| knowledge_unit_id | source-derived knowledge | claim_kind | target surface | review_status | terminal decision | notes |
|---|---|---|---|---|---|---|
| `term-vcpzwawrrla-meaty-001` | `重ね` is explained as timing an attack or special move against a waking opponent so it overlaps the opponent's wake-up. | `stable_concept` | `knowledge/curated/glossary/meaty.md` | needs_review | accepted curated glossary entry; embedded claim remains review-only | Exact meaty setups, timing, and guaranteed followups remain separate current or matchup claims. |
| `term-vcpzwawrrla-crossup-002` | `めくり` is explained through a jump attack that hits or threatens from behind/crossing side, causing guard-direction ambiguity or reversal. | `stable_concept` | `knowledge/curated/glossary/cross-up.md` | needs_review | accepted curated glossary entry; embedded claim remains review-only | Do not infer which current jump attacks cross up. |
| `term-vcpzwawrrla-sukashi-003` | `すかし` is explained as withholding the expected jump attack and landing into another option such as low or throw pressure. | `strategy_or_matchup` | review note | needs_review | review-only terminology candidate | Option coverage is context-dependent and source-local. |
| `term-vcpzwawrrla-line-004` | `ライン` is explained as screen-position pressure: advancing pushes the opponent toward the corner, retreating lowers the line. | `strategy_or_matchup` | review note | needs_review | review-only concept candidate | No exact spacing rule or matchup claim is accepted. |
| `term-vcpzwawrrla-grapple-005` | `グラップ` is used as community wording for throw escape / throw tech, including delayed throw-tech context. | `stable_concept` | review note / future glossary candidate | needs_review | review-only terminology candidate | Not treated as official terminology authority. |
| `term-vcpzwawrrla-shimmy-006` | `シミー` is explained as baiting an opponent's throw-tech / grapple response, making it whiff, and punishing it. | `stable_concept` | existing curated glossary boundary plus review note | needs_review | corroborates existing stable concept; no new curated promotion | Existing `knowledge/curated/glossary/shimmy.md` remains unchanged. |
| `term-vcpzwawrrla-abare-007` | `暴れ` is explained as attacking from disadvantage or an expected-block situation to interrupt pressure. | `strategy_or_matchup` | review note | needs_review | review-only terminology candidate | Any exact advantage examples remain current-fact-like and are not accepted here. |
| `term-vcpzwawrrla-katame-008` | `固め` is explained as using attacks or pressure strings to make the defender hard to move. | `strategy_or_matchup` | review note | needs_review | review-only concept candidate | SF6-specific pressure strength and plus-state claims remain held. |
| `term-vcpzwawrrla-cancel-009` | `キャンセル` is explained as cutting off the later recovery of one action into another action, commonly normal into special. | `stable_concept` | `knowledge/curated/glossary/cancel.md` | needs_review | accepted curated glossary entry; embedded claim remains review-only | Move-specific cancelability is a current-system fact. |
| `term-vcpzwawrrla-lethal-010` | `リーサル` is explained as an option or combo that can finish the opponent from the current life total. | `stable_concept` | `knowledge/curated/glossary/lethal.md` | needs_review | accepted curated glossary entry; embedded claim remains review-only | Exact kill thresholds are route-, resource-, character-, and patch-sensitive. |

## Claim Payloads

The JSON payloads below are review-only claim candidates. Every embedded
`review_status` remains `needs_review`; accepted public-use surfaces are changed
only through the curated glossary files listed in the table above.

For terms promoted to curated glossary entries, the accepted terminal decision
is recorded in the table and the new curated page. The embedded JSON stays
review-only because video-derived claim artifacts must not mark their own
payloads accepted.

```json
[
  {
    "id": "claim-youtube-vcpzwawrrla-meaty-001",
    "claim_kind": "stable_concept",
    "statement": "The source explains `重ね` as timing an attack or special move against a waking opponent so it overlaps wake-up.",
    "scope": "Community fighting-game terminology; no exact setup or current timing claim.",
    "evidence": {
      "source_kind": "community",
      "source_role": "commentary_only_terminology_source",
      "evidence_basis": [
        "Temporary Japanese caption review of YouTube VCPzwAwRrLA on 2026-05-14.",
        "Timestamped sanitized observation recorded in knowledge/evidence/video-observations/youtube-vcpzwawrrla-terminology.observations.md."
      ],
      "verification_state": "partially_verified",
      "confidence": 0.52,
      "volatility": "stable",
      "patch_sensitivity": "medium",
      "review_status": "needs_review",
      "source_refs": [
        {
          "label": "YouTube VCPzwAwRrLA source metadata",
          "path": "knowledge/sources/videos/youtube-vcpzwawrrla.md",
          "accessed_at": "2026-05-14"
        }
      ],
      "review_after": "2026-08-14"
    },
    "notes": "Keep as terminology candidate. Exact meaty setup validity is not accepted."
  },
  {
    "id": "claim-youtube-vcpzwawrrla-crossup-002",
    "claim_kind": "stable_concept",
    "statement": "The source explains `めくり` as a jump-attack situation where the defender's guard direction becomes reversed or ambiguous because the attack comes from the crossing side.",
    "scope": "Community fighting-game terminology; no accepted current move list.",
    "evidence": {
      "source_kind": "community",
      "source_role": "commentary_only_terminology_source",
      "evidence_basis": [
        "Temporary Japanese caption review of YouTube VCPzwAwRrLA on 2026-05-14."
      ],
      "verification_state": "partially_verified",
      "confidence": 0.54,
      "volatility": "stable",
      "patch_sensitivity": "low",
      "review_status": "needs_review",
      "source_refs": [
        {
          "label": "YouTube VCPzwAwRrLA source metadata",
          "path": "knowledge/sources/videos/youtube-vcpzwawrrla.md",
          "accessed_at": "2026-05-14"
        }
      ],
      "review_after": "2026-08-14"
    },
    "notes": "Candidate glossary definition only. Current jump-attack behavior remains separate."
  },
  {
    "id": "claim-youtube-vcpzwawrrla-shimmy-006",
    "claim_kind": "stable_concept",
    "statement": "The source explains `シミー` as baiting an opponent's throw-tech or grapple response, making it whiff, and punishing it.",
    "scope": "Community terminology corroborating the existing shimmy boundary.",
    "evidence": {
      "source_kind": "community",
      "source_role": "commentary_only_terminology_source",
      "evidence_basis": [
        "Temporary Japanese caption review of YouTube VCPzwAwRrLA on 2026-05-14.",
        "Existing curated shimmy page was inspected but not changed."
      ],
      "verification_state": "partially_verified",
      "confidence": 0.56,
      "volatility": "stable",
      "patch_sensitivity": "low",
      "review_status": "needs_review",
      "source_refs": [
        {
          "label": "YouTube VCPzwAwRrLA source metadata",
          "path": "knowledge/sources/videos/youtube-vcpzwawrrla.md",
          "accessed_at": "2026-05-14"
        }
      ],
      "review_after": "2026-08-14"
    },
    "notes": "No curated text changed. This source is review corroboration only."
  },
  {
    "id": "claim-youtube-vcpzwawrrla-cancel-009",
    "claim_kind": "stable_concept",
    "statement": "The source explains `キャンセル` as ending the later recovery of one action into another action, especially normal into special.",
    "scope": "Community terminology; no accepted move-specific cancelability claim.",
    "evidence": {
      "source_kind": "community",
      "source_role": "commentary_only_terminology_source",
      "evidence_basis": [
        "Temporary Japanese caption review of YouTube VCPzwAwRrLA on 2026-05-14."
      ],
      "verification_state": "partially_verified",
      "confidence": 0.52,
      "volatility": "stable",
      "patch_sensitivity": "medium",
      "review_status": "needs_review",
      "source_refs": [
        {
          "label": "YouTube VCPzwAwRrLA source metadata",
          "path": "knowledge/sources/videos/youtube-vcpzwawrrla.md",
          "accessed_at": "2026-05-14"
        }
      ],
      "review_after": "2026-08-14"
    },
    "notes": "Do not infer current cancel routes or move properties from this source alone."
  },
  {
    "id": "claim-youtube-vcpzwawrrla-lethal-010",
    "claim_kind": "stable_concept",
    "statement": "The source explains `リーサル` as an option or combo that can finish the opponent from the current life total.",
    "scope": "Community terminology; no route-specific kill threshold claim.",
    "evidence": {
      "source_kind": "community",
      "source_role": "commentary_only_terminology_source",
      "evidence_basis": [
        "Temporary Japanese caption review of YouTube VCPzwAwRrLA on 2026-05-14."
      ],
      "verification_state": "partially_verified",
      "confidence": 0.52,
      "volatility": "stable",
      "patch_sensitivity": "medium",
      "review_status": "needs_review",
      "source_refs": [
        {
          "label": "YouTube VCPzwAwRrLA source metadata",
          "path": "knowledge/sources/videos/youtube-vcpzwawrrla.md",
          "accessed_at": "2026-05-14"
        }
      ],
      "review_after": "2026-08-14"
    },
    "notes": "Exact lethal routes and damage thresholds need current route/resource verification."
  }
]
```

## Held / Routed Claims

- `暴れ` included source-local examples involving advantage/disadvantage; exact
  advantage values are not recorded here and remain current-fact-like.
- `固め` included SF6-specific commentary about pressure strength; keep that as
  source-local review input, not accepted public guidance.
- `グラップ`, `すかし`, and `ライン` are captured as terminology or concept
  candidates, but they need normalization before curated glossary promotion.
- `重ね`, `めくり`, `キャンセル`, and `リーサル` are promoted only as stable
  glossary boundaries. Their setup-, move-, route-, resource-, and
  current-system details remain held.
- No rejected unsafe claim was found in this source-unit run.
