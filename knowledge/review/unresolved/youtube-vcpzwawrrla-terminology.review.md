---
id: sf6-review-youtube-vcpzwawrrla-terminology
title: YouTube VCPzwAwRrLA Commentary Terminology Review
claim_kind: unresolved
source_kind: community
source_role: commentary_only_terminology_review
evidence_basis:
  - "Source metadata recorded in knowledge/sources/videos/youtube-vcpzwawrrla.md."
  - "Sanitized observations recorded in knowledge/evidence/video-observations/youtube-vcpzwawrrla-terminology.observations.md."
  - "Candidate claims recorded in knowledge/evidence/claims/youtube-vcpzwawrrla-terminology.claims.md."
  - "Temporary captions were reviewed in repo-external scratch and were not committed."
verification_state: partially_verified
confidence: 0.48
volatility: stable
patch_sensitivity: medium
review_status: needs_review
source_refs:
  - label: "Source metadata: YouTube VCPzwAwRrLA"
    path: "knowledge/sources/videos/youtube-vcpzwawrrla.md"
    accessed_at: "2026-05-14"
  - label: "Video observations: YouTube VCPzwAwRrLA terminology"
    path: "knowledge/evidence/video-observations/youtube-vcpzwawrrla-terminology.observations.md"
    accessed_at: "2026-05-14"
  - label: "Candidate claims: YouTube VCPzwAwRrLA terminology"
    path: "knowledge/evidence/claims/youtube-vcpzwawrrla-terminology.claims.md"
    accessed_at: "2026-05-14"
review_after: "2026-08-14"
summary: "Review note for #168 source E2E on a commentary-only terminology video; source-derived terminology candidates are captured as review-only knowledge."
---

# YouTube VCPzwAwRrLA Commentary Terminology Review

This review note tracks #168 one-source E2E execution for a commentary-only
terminology source. It is canonical review tracking, but it is not accepted
curated knowledge and must not feed generated knowledge references.

## Review Status

- Source metadata artifact created: yes.
- Timestamped observation artifact created: yes.
- Candidate terminology claims artifact created: yes.
- Actual content review occurred: yes, via temporary Japanese caption review in
  repo-external scratch.
- Raw video stored in repo: no.
- Raw audio stored in repo: no.
- Raw frames or screenshots stored in repo: no.
- Full captions or transcript stored in repo: no.
- Scratch/cache policy followed: yes.
- Curated promotion performed: no.
- Generated references changed: no.
- Exact current-system values accepted: no.
- Current verification required before public use: yes for setup-, frame-, or
  move-specific claims.

## Source-Derived Knowledge Units

The output of this source E2E is not a video summary. The source was analyzed
for terminology and concept knowledge units, then routed into review-only repo
surfaces. Review-only terminology candidates are still repo knowledge, but they
are not accepted public-answer authority until reviewed and promoted.

| knowledge_unit_id | extracted knowledge | knowledge type | repo surface | terminal state | authority boundary |
|---|---|---|---|---|---|
| `ku-vcpzwawrrla-meaty` | `重ね` as wake-up-overlap attack timing. | source-derived terminology candidate | claims + observation + review | review-only hold, `needs_review` | Exact setup timing and guaranteed followups are not accepted. |
| `ku-vcpzwawrrla-crossup` | `めくり` as cross-side jump attack / guard-direction reversal concept. | source-derived terminology candidate | claims + observation + review | review-only hold, `needs_review` | Current move-specific cross-up capability is not accepted. |
| `ku-vcpzwawrrla-sukashi` | `すかし` as withholding an expected jump attack and landing into another option. | source-derived terminology candidate | claims + review | review-only hold, `needs_review` | Option coverage and setup validity are context-dependent. |
| `ku-vcpzwawrrla-line` | `ライン` as screen-position pressure and corner-push concept. | source-derived strategy concept candidate | claims + review | review-only hold, `needs_review` | No exact positioning rule is accepted. |
| `ku-vcpzwawrrla-grapple` | `グラップ` as throw escape / throw-tech wording in commentary. | source-derived terminology candidate | claims + review | review-only hold, `needs_review` | Community wording, not official terminology authority. |
| `ku-vcpzwawrrla-shimmy` | `シミー` as baiting throw-tech / grapple and punishing the whiff. | source-derived terminology candidate | claims + existing curated boundary | review-only corroboration; no new curated promotion | Existing shimmy page remains the accepted surface; this source does not alter it. |
| `ku-vcpzwawrrla-abare` | `暴れ` as attacking from disadvantage or expected-block situations. | source-derived terminology / strategy candidate | claims + review | review-only hold, `needs_review` | Source-local frame examples are held. |
| `ku-vcpzwawrrla-katame` | `固め` as pressure strings that make the defender hard to move. | source-derived terminology / strategy candidate | claims + review | review-only hold, `needs_review` | SF6-specific pressure strength claims remain held. |
| `ku-vcpzwawrrla-cancel` | `キャンセル` as ending later recovery into another action. | source-derived terminology candidate | claims + review | review-only hold, `needs_review` | Move-specific cancelability is current-system information. |
| `ku-vcpzwawrrla-lethal` | `リーサル` as an option or combo that can finish the opponent from the current life total. | source-derived terminology candidate | claims + review | review-only hold, `needs_review` | Exact kill thresholds depend on current route, resources, health, and character state. |

## Terminal Decisions

| Candidate | Decision | Reason |
|---|---|---|
| Source metadata | metadata-only source artifact created | Needed to identify the public video and content-review boundary. |
| Commentary observations | sanitized report / observation artifact created | Content was reviewed through temporary captions without committing raw transcript or media. |
| Terminology/concept candidates | review-only hold, `needs_review` | The source is community commentary and should not become accepted glossary or strategy authority without review. |
| Existing shimmy curated page | unchanged | The source corroborates the broad concept, but #168 does not alter accepted curated knowledge. |
| Current-fact-like examples | held | Exact advantage, guaranteed setup validity, move-specific cancelability, and route-specific lethal thresholds require separate verification. |
| Rejected unsafe | none | No unsupported unsafe claim was found; no rejection was fabricated for coverage. |

## Content Execution Record

| Field | Result |
|---|---|
| Source URL | `https://www.youtube.com/watch?v=VCPzwAwRrLA` |
| Access method | Public no-cookie YouTube metadata access plus temporary Japanese caption review. |
| Actual content review occurred? | yes. |
| Raw video/audio committed? | no. |
| Captions/transcript committed? | no. |
| Frames/screenshots/contact sheets committed? | no. |
| Credentials/cookies/browser profile used? | no. |
| Public adapter behavior changed? | no. |
| Curated promotion? | no. |

## Workflow Findings

- `workflows/ingest-video.md`, `workflows/review-claims.md`, and
  `workflows/media-scratch-cache-policy.md` were sufficient for this source
  after treating commentary-only video as an article-like source for claim
  review.
- `tests/validation/validate-ingest-artifacts.ps1` had an article-only source
  reference check for claim artifacts. #168 updates that check so review-only
  claim artifacts may cite either article or video source metadata when the
  source E2E run actually produces video-derived claims.
- No broad speculative validator was added.

## Next Review Questions

- Should `重ね`, `めくり`, `すかし`, `グラップ`, `暴れ`, `固め`, `キャンセル`, and
  `リーサル` get dedicated glossary pages after a second source or maintainer
  review?
- Should the existing `knowledge/curated/glossary/shimmy.md` cite this source
  in a future glossary-focused PR, or should it remain based on the legacy
  reviewed note?
- Does the repo need a dedicated `terminology_candidate` claim kind, or are
  `stable_concept` and `strategy_or_matchup` sufficient for this stage?
