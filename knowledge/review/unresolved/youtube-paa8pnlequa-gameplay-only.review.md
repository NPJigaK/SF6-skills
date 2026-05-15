---
id: sf6-review-youtube-paa8pnlequa-gameplay-only
title: YouTube PaA8PNLeQUA Gameplay-Only Source E2E Review
claim_kind: observation
source_kind: reproducible_observation
source_role: gameplay_only_video_link_review
evidence_basis:
  - "Video source metadata recorded in knowledge/sources/videos/youtube-paa8pnlequa.md."
  - "Sanitized observations recorded in knowledge/evidence/video-observations/youtube-paa8pnlequa-gameplay-only.observations.md."
  - "Source-unit report recorded in docs/testing/video-analysis-calibration/video-link-gameplay-only-01-20260516.md."
  - "Temporary media and contact sheets were reviewed in repo-external scratch and were not committed."
verification_state: partially_verified
confidence: 0.5
volatility: patch_sensitive
patch_sensitivity: high
review_status: needs_review
source_refs:
  - label: "Source metadata: YouTube PaA8PNLeQUA"
    path: "knowledge/sources/videos/youtube-paa8pnlequa.md"
    accessed_at: "2026-05-16"
  - label: "Video observations: YouTube PaA8PNLeQUA gameplay-only"
    path: "knowledge/evidence/video-observations/youtube-paa8pnlequa-gameplay-only.observations.md"
    accessed_at: "2026-05-16"
review_after: "2026-08-16"
summary: "Review note for #161 source E2E on a gameplay-only YouTube video link; the source reached sanitized report and review-only observation terminal state."
---

# YouTube PaA8PNLeQUA Gameplay-Only Source E2E Review

This review note tracks #161 one-source E2E execution for a gameplay-only
YouTube video link. It is canonical review tracking, but it is not accepted
curated knowledge and must not feed generated knowledge references.

## Review Status

- Video source metadata artifact updated: yes.
- Timestamped observation artifact created: yes.
- Source-unit report created: yes.
- Candidate claims artifact created: no.
- Curated promotion performed: no.
- Raw video stored in repo: no.
- Raw audio stored in repo: no.
- Raw frames or screenshots stored in repo: no.
- Contact sheets stored in repo: no.
- Captions/subtitles/transcript stored in repo: no.
- Scratch/cache policy followed: yes.
- Exact current-system values accepted: no.
- Public `sf6-agent` behavior changed: no.
- Generated references changed: no.

## Terminal Decisions

| Unit | Decision | Reason |
|---|---|---|
| Source metadata | updated metadata-only source artifact | #161 required the existing metadata-only source to record real no-cookie content review and the gameplay-only boundary. |
| Gameplay observations | sanitized observation artifact created | Direct visual content review was possible, and sparse samples support gameplay-only format confirmation. |
| Candidate claims | none created | The source has no commentary/caption-derived stable knowledge unit in this pass, and sparse visual gameplay observations should not become claims by themselves. |
| Curated knowledge | none promoted | Gameplay-only footage does not safely produce accepted strategy knowledge or current facts without separate claim review and authority checks. |
| Current-fact route | not_applicable for this pass | No exact current-fact-like value was extracted; exact move/frame/damage claims were explicitly avoided. |
| Rejected unsafe | none | No unsafe candidate claim was extracted; rejection was not fabricated for coverage. |

## Content Execution Record

| Field | Result |
|---|---|
| Source URL | `https://www.youtube.com/watch?v=PaA8PNLeQUA` |
| Access method | Public no-cookie YouTube metadata access, temporary media download, ffprobe inspection, sparse frame/contact-sheet visual review. |
| Metadata access? | yes. |
| Video download/review? | yes, repo-external scratch only. |
| Audio/caption review? | no caption/subtitle track was available; direct audio was not used for knowledge extraction. |
| Temporary frames/contact sheets? | yes, repo-external scratch only, deleted before commit. |
| Content execution depth | direct visual gameplay review with sparse sampling. |
| Raw video/audio committed? | no. |
| Frames/screenshots/contact sheets committed? | no. |
| Captions/transcript committed? | no. |
| Credentials/cookies/browser profile used? | no. |

## Held Observations

The source is useful as an executed gameplay-only video-link input. It confirms
that a public replay-style YouTube source can become source metadata,
sanitized observations, and a review terminal state without committing raw
media or making public-answer claims.

The visual samples show JP vs C.Viper-style gameplay with standard SF6 HUD,
purple projectile/portal-style effects, close-range contact candidates,
cinematic/high-effect moments, and end-card/channel overlay content. These
observations remain broad and sparse.

The following categories stay unresolved:

- Exact move identity and exact input sequence for any interaction.
- Exact hit/block/whiff outcome and frame timing.
- Exact damage/scaling facts or route validity.
- Player rank, matchup verdict, or strategy conclusion from source title or
  replay footage.
- Move-frequency analytics or all-character/all-move generalization.

## Workflow Findings

- `workflows/ingest-video.md` and `workflows/media-scratch-cache-policy.md`
  were sufficient for this #161 source-unit run.
- No schema, validator, workflow, generated reference, public adapter, or
  exact current-fact data surface change was required.
- The correct terminal state is sanitized source/report/observation plus
  review-only hold, not accepted curated knowledge.

## Move-Frequency Follow-Up

#161 did not perform move-frequency analytics. This source is a good candidate
for future Kakeru JP move-frequency calibration because it is gameplay-only
match footage and the practical downstream query is how many times Kakeru's JP
used each move in the match.

Follow-up issue #195 tracks that calibration explicitly. This review note must
not be interpreted as proving move-count readiness, match-level analytics, or
all-character/all-move recognition.

## Next Review Questions

- Should a later video-link batch compare #161 with #162 to document the
  gameplay-only vs gameplay-with-commentary difference?
- Should the final #158 audit record this row as PASS for the gameplay-only
  YouTube/video-link family with terminal state `sanitized report only` plus
  review-only observation?
- Should future move-recognition or move-frequency work use this source as a
  separate scoped validation case? That would require a new issue and
  false-positive/false-negative evaluation.
