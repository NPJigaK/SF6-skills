---
id: sf6-review-youtube-shorts-sycyvw6h8wi
title: YouTube Shorts syCYVW6h8WI Video Observation Pilot Review
claim_kind: observation
source_kind: reproducible_observation
source_role: video_observation_pilot_review
evidence_basis:
  - "Video source metadata recorded in knowledge/sources/videos/youtube-shorts-sycyvw6h8wi.md."
  - "Timestamped observations recorded in knowledge/evidence/video-observations/youtube-shorts-sycyvw6h8wi.observations.md."
  - "Repo-external scratch media was used only for temporary observation and was not committed."
  - "No claim was promoted to curated knowledge during the pilot."
verification_state: unverified
confidence: 0.35
volatility: patch_sensitive
patch_sensitivity: high
review_status: needs_review
source_refs:
  - label: "Source metadata: YouTube Shorts syCYVW6h8WI"
    path: "knowledge/sources/videos/youtube-shorts-sycyvw6h8wi.md"
    accessed_at: "2026-05-03"
  - label: "Video observations: YouTube Shorts syCYVW6h8WI"
    path: "knowledge/evidence/video-observations/youtube-shorts-sycyvw6h8wi.observations.md"
    accessed_at: "2026-05-03"
review_after: "2026-08-03"
summary: "Review holding note for a first video observation workflow pilot using a short ACQUA YouTube Shorts source about a corner-escape technique."
---

# YouTube Shorts syCYVW6h8WI Video Observation Pilot Review

This review note tracks the first v2 video observation workflow pilot. It is canonical review tracking, but it is not accepted curated knowledge and must not feed generated knowledge references.

## Review Status

- Video source metadata artifact created: yes.
- Timestamped video observation artifact created: yes.
- Candidate claims artifact created: no; observations were sufficient for this first pilot.
- Raw video stored in repo: no.
- Raw frames or screenshots stored in repo: no.
- Full transcript stored in repo: no.
- Scratch/cache policy followed: yes.
- Curated promotion performed: no.
- Generated references changed: no.
- Exact current values stored: no.
- Current verification required for technique reliability: yes.

## Held Observations

The source appears to explain an SF6 corner-escape idea involving jump or back-jump input after leaving the corner and a possible landing guard interaction. This remains a source-local observation.

The following categories stay unresolved:

- Whether the described landing behavior is current across the relevant patch/version.
- Exact landing-frame, throw, guard, strike, or input timing details.
- Character-specific or stage-position-specific reliability.
- Whether the demonstrated sequence works as a reusable defensive option outside the clip context.
- Whether the visual sequence confirms the speaker claim or only illustrates it.
- Japanese terminology normalization for any future curated wording.

## Review Notes

- The video is useful for testing video observation artifact shape and timestamped observation practice.
- Speaker/commentary claims were separated from visible observations.
- Visual observation confidence is limited by vertical Shorts layout, low resolution, face-cam overlay, and sparse frame sampling.
- Any future candidate claim should cite the video observation artifact as `source_kind = reproducible_observation`, set `review_status = needs_review`, and pass review before curated promotion.
- Do not use this video as final public answer evidence.

## Workflow Findings

- `workflows/ingest-video.md` was practical for separating clip metadata, timestamped visual observations, transcript/commentary summaries, and review-only handling.
- `contracts/video-observation.schema.json` was usable as a coarse payload shape inside the Markdown artifact, but there is no executable validator for `knowledge/evidence/video-observations/*.observations.md` yet.
- `knowledge/sources/videos/` has no dedicated source artifact validator yet.
- A future validator should check video observation payload shape, no full transcript/media storage claims, source references, and review-only status.
- The media scratch/cache policy was necessary because the pilot used temporary raw video and frames outside the repo.
