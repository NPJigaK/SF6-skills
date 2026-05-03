---
id: video-observation-youtube-shorts-sycyvw6h8wi
title: YouTube Shorts syCYVW6h8WI Video Observation Pilot
source_kind: reproducible_observation
source_role: video_observation_pilot
review_status: needs_review
review_after: "2026-08-03"
---

# YouTube Shorts syCYVW6h8WI Video Observation Pilot

This artifact records timestamped observations from one short SF6 video source. It is an observation artifact, not accepted strategy knowledge, and it must not feed generated references without later review.

## Source

- Source metadata: `knowledge/sources/videos/youtube-shorts-sycyvw6h8wi.md`
- Source URL: `https://www.youtube.com/shorts/syCYVW6h8WI`
- Accessed: 2026-05-03
- Observation method: repo-external temporary video download, sparse frame sampling, contact-sheet inspection, and Japanese auto-caption inspection.
- Raw media stored in repo: no.
- Full transcript stored in repo: no.

## Timestamped Observations

| Time | Observation kind | Visible observation | Speaker/commentary claim | Confidence | Notes |
|---|---|---|---|---|---|
| 00:00-00:05 | visual + commentary | The Short opens with ACQUA branding, a face-cam layout, and Japanese overlay text about using an SF6 specification to escape from the corner more easily. | Speaker introduces the topic as something many players may not know. | medium | Title/overlay are visible; the exact gameplay claim is not verified here. |
| 00:05-00:15 | visual + commentary | Gameplay appears in the upper portion. One character moves from a corner/near-corner escape situation into a jump/back-jump sequence. | Speaker describes escaping from the screen edge and then holding back jump. | medium | Character identities and exact move names are unresolved due to resolution and layout. |
| 00:15-00:24 | commentary | The sampled frames show both characters returning toward a grounded interaction after jump movement. | Speaker claims there are landing frames where guarding is possible, and discusses throw timing at landing. | low | This is a speaker claim about game behavior, not accepted current fact. |
| 00:24-00:34 | visual + commentary | The clip shows a grounded interaction after jump movement; overlay text refers to holding up and losing to strikes. | Speaker says holding up/back jump can lose to strikes. | medium | This supports a review-only observation about the video explanation, not setup validity. |
| 00:34-00:42 | visual + commentary | A sequence appears to show a character guarding in close range after a back-jump-related setup; the overlay/commentary emphasize guard behavior. | Speaker says the character is back-jumping but guarding, and contrasts throw escape with guarding strikes. | medium | Visual support is partial; current mechanics and input timing require verification. |
| 00:42-00:56 | commentary | The visible gameplay stays in the same close-range demonstration context. | Speaker explains that landing has a small window where only guard is possible, and that holding back jump can become guard if the opponent strikes during that window. | low | This is potentially current-system knowledge and must remain review-only. |
| 00:57-01:09 | commentary | The final portion returns to summary-style face-cam/gameplay presentation. | Speaker says the technique is strong but not universal, can lose to meaty throw or later attacks, and treats the behavior as a specification rather than a bug. | medium | Useful as source-local explanation. Do not promote without review and current verification. |

## Contract-Shaped Observation Payload

This payload follows the shape of `contracts/video-observation.schema.json` at a coarse pilot level. Segment text is paraphrased; no full transcript is stored.

```json
{
  "schema_version": "2.0.0",
  "clip_metadata": {
    "clip_id": "youtube-shorts-sycyvw6h8wi",
    "source_fps": 30,
    "normalized_fps": 60,
    "total_frames": 4145
  },
  "actor_bindings": [
    {
      "actor_ref": "actor_a",
      "character_slug": null,
      "binding_confidence": 0.25,
      "binding_basis": [
        "character_visual",
        "unknown"
      ]
    },
    {
      "actor_ref": "actor_b",
      "character_slug": null,
      "binding_confidence": 0.25,
      "binding_basis": [
        "character_visual",
        "unknown"
      ]
    }
  ],
  "segments": [
    {
      "segment_id": "seg-0001",
      "track": "global_phase",
      "kind": "fight_active",
      "start_frame": 0,
      "end_frame": 4145,
      "confidence": 0.7,
      "evidence_refs": [
        "ev-video-sample"
      ],
      "summary": "Shorts layout with SF6 gameplay, face cam, and Japanese explanatory overlays."
    },
    {
      "segment_id": "seg-0002",
      "track": "transcript",
      "kind": "utterance_span",
      "start_frame": 6,
      "end_frame": 300,
      "confidence": 0.7,
      "evidence_refs": [
        "ev-auto-caption"
      ],
      "language": "ja",
      "text_summary": "Speaker introduces a specification-based corner escape topic."
    },
    {
      "segment_id": "seg-0003",
      "track": "interaction",
      "kind": "side_switch_candidate",
      "start_frame": 300,
      "end_frame": 900,
      "confidence": 0.45,
      "evidence_refs": [
        "ev-frame-sample"
      ],
      "summary": "Gameplay appears to demonstrate jump/back-jump movement around a corner or near-corner escape context."
    },
    {
      "segment_id": "seg-0004",
      "track": "transcript",
      "kind": "utterance_span",
      "start_frame": 900,
      "end_frame": 1440,
      "confidence": 0.65,
      "evidence_refs": [
        "ev-auto-caption"
      ],
      "language": "ja",
      "text_summary": "Speaker discusses landing guard behavior and throw timing."
    },
    {
      "segment_id": "seg-0005",
      "track": "interaction",
      "kind": "block_connect_candidate",
      "start_frame": 2040,
      "end_frame": 2520,
      "confidence": 0.4,
      "evidence_refs": [
        "ev-frame-sample",
        "ev-auto-caption"
      ],
      "summary": "A close-range sequence is presented as a back-jump-related guard example."
    },
    {
      "segment_id": "seg-0006",
      "track": "transcript",
      "kind": "utterance_span",
      "start_frame": 2520,
      "end_frame": 3360,
      "confidence": 0.65,
      "evidence_refs": [
        "ev-auto-caption"
      ],
      "language": "ja",
      "text_summary": "Speaker explains a small landing window where guard can occur and frames the behavior as a game specification."
    },
    {
      "segment_id": "seg-0007",
      "track": "transcript",
      "kind": "utterance_span",
      "start_frame": 3420,
      "end_frame": 4145,
      "confidence": 0.65,
      "evidence_refs": [
        "ev-auto-caption"
      ],
      "language": "ja",
      "text_summary": "Speaker gives limitations: the technique is strong but not universal and can still lose to throws or later attacks."
    }
  ],
  "derived_events": [
    {
      "event_id": "event-0001",
      "kind": "corner_escape_technique_explanation_candidate",
      "source_segment_ids": [
        "seg-0002",
        "seg-0003",
        "seg-0004",
        "seg-0005",
        "seg-0006",
        "seg-0007"
      ]
    }
  ]
}
```

## Boundary Notes

- Observed gameplay and caption summaries are review-only observations.
- Speaker claims about landing frames, throw timing, strike interaction, or specification status are not accepted current facts.
- Character identities, exact actions, input timing, setup reliability, and current patch applicability remain unresolved.
- No raw media, frames, screenshots, contact sheets, or full captions are stored in the repository.
