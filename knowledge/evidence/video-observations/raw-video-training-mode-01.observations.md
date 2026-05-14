---
id: video-observation-raw-video-training-mode-01
title: Raw Local Training-Mode Video Observation
source_kind: reproducible_observation
source_role: raw_local_training_mode_observation
review_status: needs_review
review_after: "2026-08-14"
---

# Raw Local Training-Mode Video Observation

This artifact records sanitized observations from `raw-video-training-mode-01`.
It is an observation artifact, not accepted strategy knowledge, and it must not
feed generated references without later review.

## Source

- Source metadata: `knowledge/sources/videos/raw-video-training-mode-01.md`
- Source URL: `local-sample://raw-video-training-mode-01`
- Accessed: 2026-05-14
- Source type: maintainer-local raw video.
- Private local path recorded in repo: no.
- Observation method: `ffprobe` metadata inspection plus repo-external
  temporary frame and contact-sheet review.
- Media metadata summary: MP4-family container, HEVC video, 1920x1080, about
  37.93 seconds, 60 fps nominal, 2272 reported video frames, AAC stereo audio
  stream present but not reviewed.
- Raw media stored in repo: no.
- Full transcript stored in repo: no.

## Timestamped Observations

| Time | Observation kind | Visible observation | Speaker/commentary claim | Confidence | Notes |
|---|---|---|---|---|---|
| 00:00-00:04 | raw-local training UI | Training/combo-trial style UI is visible. HUD labels show JP on the player side and Ryu on the dummy side. A command list is visible on the left, and input history is visible on the right. | none | high | Character labels are visual source-local observations, not accepted roster/current facts. |
| 00:04-00:10 | combo-trial attempt | The player-side JP model begins a guided sequence against the Ryu dummy. Hit sparks and training UI counters appear during the attempt. | none | medium | Observed action sequence is not converted into canonical move IDs or exact route validity. |
| 00:10-00:20 | combo-trial sequence | The video shows a continued sequence with repeated hits, launch/airborne states, and training UI damage/combo labels. | none | medium | Observed damage and combo counters are visible labels only and are not current-system authority. |
| 00:20-00:31 | cinematic/super-like segment | The sequence includes a high-visual-effects cinematic segment with JP prominently shown and the Ryu dummy affected by the sequence. | none | medium | Do not infer exact super-art identity, frame data, damage authority, or move properties from this visual review. |
| 00:31-00:36 | completion/knockdown context | The Ryu dummy appears knocked down after the sequence. The command-list UI remains visible and a success state is visible in the run. | none | medium | Useful as raw-local combo-trial completion context, not accepted combo route evidence. |
| 00:36-00:38 | post-attempt UI | The clip ends near a retry/menu style overlay after the attempt. | none | high | Confirms this is a bounded local recording rather than a long gameplay match. |

## Contract-Shaped Observation Payload

This payload follows the shape of `contracts/video-observation.schema.json` at a
coarse raw-local-review level. Segment text is paraphrased; no raw video,
frames, screenshots, contact sheet, audio, or transcript is stored.

```json
{
  "schema_version": "2.0.0",
  "clip_metadata": {
    "clip_id": "raw-video-training-mode-01",
    "source_fps": 60,
    "normalized_fps": 60,
    "total_frames": 2272
  },
  "actor_bindings": [
    {
      "actor_ref": "actor_a",
      "character_slug": "jp",
      "binding_confidence": 0.82,
      "binding_basis": [
        "visible HUD label",
        "character visual",
        "training UI"
      ]
    },
    {
      "actor_ref": "actor_b",
      "character_slug": "ryu",
      "binding_confidence": 0.82,
      "binding_basis": [
        "visible HUD label",
        "character visual",
        "training UI"
      ]
    }
  ],
  "segments": [
    {
      "segment_id": "seg-raw-training-0001",
      "track": "global_phase",
      "kind": "training_mode_combo_trial_context",
      "start_frame": 0,
      "end_frame": 240,
      "confidence": 0.88,
      "summary": "Training/combo-trial style UI with command list and input history is visible.",
      "evidence_refs": [
        "knowledge/sources/videos/raw-video-training-mode-01.md"
      ]
    },
    {
      "segment_id": "seg-raw-training-0002",
      "track": "interaction",
      "kind": "contact_sequence_candidate",
      "start_frame": 240,
      "end_frame": 720,
      "confidence": 0.65,
      "summary": "Player-side JP begins a guided sequence against a Ryu dummy with hit effects and combo UI counters.",
      "evidence_refs": [
        "knowledge/sources/videos/raw-video-training-mode-01.md"
      ]
    },
    {
      "segment_id": "seg-raw-training-0003",
      "track": "interaction",
      "kind": "airborne_sequence_candidate",
      "start_frame": 720,
      "end_frame": 1200,
      "confidence": 0.62,
      "summary": "The sequence continues with launch or airborne states and visible training UI labels.",
      "evidence_refs": [
        "knowledge/sources/videos/raw-video-training-mode-01.md"
      ]
    },
    {
      "segment_id": "seg-raw-training-0004",
      "track": "global_phase",
      "kind": "cinematic_sequence_candidate",
      "start_frame": 1200,
      "end_frame": 1860,
      "confidence": 0.58,
      "summary": "A high-visual-effects cinematic segment appears during the sequence.",
      "evidence_refs": [
        "knowledge/sources/videos/raw-video-training-mode-01.md"
      ]
    },
    {
      "segment_id": "seg-raw-training-0005",
      "track": "global_phase",
      "kind": "trial_completion_context",
      "start_frame": 1860,
      "end_frame": 2272,
      "confidence": 0.72,
      "summary": "The sequence resolves into knockdown/completion context and a post-attempt UI state.",
      "evidence_refs": [
        "knowledge/sources/videos/raw-video-training-mode-01.md"
      ]
    }
  ],
  "derived_events": [
    {
      "event_id": "event-raw-training-0001",
      "kind": "raw_local_training_mode_report_only",
      "source_segment_ids": [
        "seg-raw-training-0001",
        "seg-raw-training-0002",
        "seg-raw-training-0003",
        "seg-raw-training-0004",
        "seg-raw-training-0005"
      ]
    }
  ]
}
```

## Source-Derived Observation Units

| knowledge_unit_id | extracted observation or knowledge | knowledge type | repo surface | terminal state | authority boundary |
|---|---|---|---|---|---|
| `ku-raw-training-context` | The sample is a maintainer-local training/combo-trial style recording with command-list and input-history UI visible. | raw-local training-mode observation | this observation artifact | sanitized observation/report only | Not public answer evidence; no private path or raw media committed. |
| `ku-raw-training-actors` | JP and Ryu labels/characters are visible in the local recording. | source-local visual observation | this observation artifact | review-only hold | Visual labels are not accepted roster/current facts. |
| `ku-raw-training-sequence` | The clip shows a guided player-side sequence with hit effects, airborne/cinematic phases, and a completion/success context. | source-local visual sequence observation | this observation artifact | sanitized observation/report only | No canonical move IDs, route validity, or combo optimization claim inferred. |
| `ku-raw-training-current-fact-like-labels` | Training UI damage/combo labels are visible in sampled frames. | current-fact-like visual label observation | this observation artifact plus review note | review-only hold | Observed labels must not be treated as current damage, scaling, frame, or route authority. |

## Boundary Notes

- These are review-only observations.
- The raw-local video was reviewed through temporary frame/contact-sheet
  derivatives outside the repository.
- Raw media stored in repo: no.
- Raw frames or screenshots stored in repo: no.
- Contact sheet stored in repo: no.
- Full transcript stored in repo: no.
- Private local path stored in repo: no.
- The extracted observations are not accepted current facts.
- Training UI labels, visible character labels, observed damage labels, and
  command-list text must not feed generated references or public answers as
  authority.
- Exact frame data, exact startup/active/recovery, exact hit/block advantage,
  exact combo route validity, official move properties, and current-system
  damage authority are not inferred from this source.
