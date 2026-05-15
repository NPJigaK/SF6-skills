---
id: video-observation-youtube-paa8pnlequa-gameplay-only
title: YouTube PaA8PNLeQUA Gameplay-Only Video Observation
source_kind: reproducible_observation
source_role: gameplay_only_video_link_observation
review_status: needs_review
review_after: "2026-08-16"
---

# YouTube PaA8PNLeQUA Gameplay-Only Video Observation

This artifact records sanitized observations from one gameplay-only YouTube
video source. It is an observation artifact, not accepted strategy knowledge,
and it must not feed generated references without later review.

## Source

- Source metadata: `knowledge/sources/videos/youtube-paa8pnlequa.md`
- Source URL: `https://www.youtube.com/watch?v=PaA8PNLeQUA`
- Accessed: 2026-05-16
- Observation method: no-cookie YouTube metadata access, temporary
  repo-external video download, ffprobe metadata inspection, sparse frame
  sampling, and contact-sheet visual review in repo-external scratch.
- Reviewed duration: approximately 8:14.
- Raw media stored in repo: no.
- Full transcript stored in repo: no.

## Timestamped Observations

| Time | Observation kind | Visible observation | Speaker/commentary claim | Confidence | Notes |
|---|---|---|---|---|---|
| 00:00-00:30 | visual gameplay | Match footage begins with standard SF6 HUD and two visible fighters. The title and sampled HUD context identify the matchup source-locally as JP vs C.Viper. | None observed; no captions/subtitles were available. | high | Actor labels are source-local review input only; no player rank or current fact is accepted. |
| 00:30-02:30 | visual gameplay | Gameplay continues with JP-style purple projectile/portal effects and C.Viper-style ground and aerial movement pressure candidates. | None observed; no captions/subtitles were available. | medium | Candidate move/action impressions are broad visual observations, not exact move identity. |
| 02:30-04:30 | visual gameplay | The sampled windows show multiple interaction phases, including high-effect hit/block candidates and cinematic/super-like visual flashes. | None observed; no captions/subtitles were available. | medium | Effects obscure exact action source and timing; do not infer exact hit or route facts. |
| 04:30-06:30 | visual gameplay | Later rounds or continued match segments show neutral resets, knockdown/pressure candidates, and normal HUD-only gameplay presentation. | None observed; no captions/subtitles were available. | medium | The source remains gameplay-only; sparse sampling is insufficient for move-frequency counting. |
| 06:30-07:45 | visual gameplay | Late-match samples include additional purple effect pressure, close-range contact candidates, and grounded movement from both fighters. | None observed; no captions/subtitles were available. | medium | Useful as sanitized gameplay observation only, not strategy or matchup authority. |
| 07:45-08:14 | end card / channel overlay | The source transitions toward KO/end-card or channel call-to-action presentation. | None observed; no captions/subtitles were available. | high | End-card content is not SF6 gameplay evidence. |

## Contract-Shaped Observation Payload

This payload follows the shape of `contracts/video-observation.schema.json` at a
coarse gameplay-only source E2E level. Segment text is paraphrased; no raw
media, frames, screenshots, contact sheets, captions, or transcript are stored.

```json
{
  "schema_version": "2.0.0",
  "clip_metadata": {
    "clip_id": "youtube-paa8pnlequa-gameplay-only-e2e",
    "source_fps": 60,
    "normalized_fps": 60,
    "total_frames": 29639
  },
  "actor_bindings": [
    {
      "actor_ref": "actor_a",
      "character_slug": "jp",
      "binding_confidence": 0.78,
      "binding_basis": [
        "source title",
        "visible character silhouette",
        "HUD/source-local context"
      ]
    },
    {
      "actor_ref": "actor_b",
      "character_slug": "c_viper",
      "binding_confidence": 0.72,
      "binding_basis": [
        "source title",
        "visible character silhouette",
        "HUD/source-local context"
      ]
    }
  ],
  "segments": [
    {
      "segment_id": "seg-gameplay-0001",
      "track": "global_phase",
      "kind": "fight_active",
      "start_frame": 0,
      "end_frame": 27900,
      "confidence": 0.82,
      "summary": "Gameplay-only replay footage with standard SF6 HUD and no caption/commentary track available.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-paa8pnlequa.md"
      ]
    },
    {
      "segment_id": "seg-gameplay-0002",
      "track": "actor_a_local",
      "kind": "projectile_emit_candidate",
      "start_frame": 1800,
      "end_frame": 9000,
      "confidence": 0.48,
      "summary": "Sparse samples show purple projectile/portal-style effects near actor_a across early match windows.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-paa8pnlequa.md"
      ]
    },
    {
      "segment_id": "seg-gameplay-0003",
      "track": "interaction",
      "kind": "contact_candidate",
      "start_frame": 4500,
      "end_frame": 16200,
      "confidence": 0.46,
      "summary": "Sparse samples show repeated close-range and projectile-contact candidates, but exact action source is unresolved.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-paa8pnlequa.md"
      ]
    },
    {
      "segment_id": "seg-gameplay-0004",
      "track": "global_phase",
      "kind": "super_freeze",
      "start_frame": 9000,
      "end_frame": 24000,
      "confidence": 0.4,
      "summary": "High-effect cinematic or super-like visual flashes appear in sampled windows; exact super/action identity is not accepted.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-paa8pnlequa.md"
      ]
    },
    {
      "segment_id": "seg-gameplay-0005",
      "track": "global_phase",
      "kind": "ko_overlay",
      "start_frame": 28800,
      "end_frame": 29639,
      "confidence": 0.7,
      "summary": "End-card or KO/channel overlay region appears near the end and is not gameplay evidence for move analysis.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-paa8pnlequa.md"
      ]
    }
  ],
  "derived_events": [
    {
      "event_id": "event-gameplay-0001",
      "kind": "gameplay_only_video_link_e2e_sanitized_observation",
      "source_segment_ids": [
        "seg-gameplay-0001",
        "seg-gameplay-0002",
        "seg-gameplay-0003",
        "seg-gameplay-0004",
        "seg-gameplay-0005"
      ]
    }
  ]
}
```

## Boundary Notes

- These are review-only observations.
- The source is useful for gameplay-only video-link E2E validation, not
  accepted strategy knowledge.
- Actor labels, candidate effects, and candidate contacts are not accepted
  current facts.
- Source-local title/HUD context and sparse visual samples are not accepted current facts.
- Exact move identity, exact frame timing, hit/block outcome, route validity,
  matchup claims, damage/scaling facts, and move-frequency statistics remain
  unresolved.
- No raw media, frames, screenshots, contact sheets, full captions, or full
  transcript are stored in the repository.
