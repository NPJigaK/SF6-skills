---
id: video-observation-youtube-nyfngnzjv3m-jp-combos
title: YouTube nyFNgnzjV3M JP Combo Damage Oracle Fixture Observation
source_kind: reproducible_observation
source_role: combo_damage_oracle_observation
review_status: needs_review
review_after: "2026-08-04"
---

# YouTube nyFNgnzjV3M JP Combo Damage Oracle Fixture Observation

This artifact records timestamped observations from a limited section of one Japanese JP combo guide video. It is an observation artifact, not accepted strategy knowledge, and it must not feed generated references without later review.

## Source

- Source metadata: `knowledge/sources/videos/youtube-nyfngnzjv3m.md`
- Source URL: `https://www.youtube.com/watch?v=nyFNgnzjV3M`
- Accessed: 2026-05-04
- Observation method: repo-external temporary section download, sparse frame sampling, still-frame/crop inspection, contact-sheet inspection, and Japanese auto-caption inspection.
- Observed section: `00:08-00:57` from the original video.
- Raw media stored in repo: no.
- Full transcript stored in repo: no.

## Timestamped Observations

| Time | Observation kind | Visible observation | Speaker/commentary claim | Confidence | Notes |
|---|---|---|---|---|---|
| 00:08-00:12 | visual + commentary | The chapter opens with JP gameplay and an overlay reading `JPの基本コンボ(小技始動)`. | Speaker introduces this as a basic JP combo section. | high | Chapter boundary and topic are clear from overlay and captions. |
| 00:12-00:23 | visual + commentary | Overlay shows `しゃがみ小P > 立ち小P > 弱ストリボーグ`. The training UI later shows combo damage `1240`. | Speaker describes the basic route as crouching jab/jab into Stribog; captions are noisy but align with the visible overlay. | high | Use as the first usable oracle fixture case. Damage is an observed video label, not current-system authority. |
| 00:31-00:45 | visual + commentary | Overlay shows `小P > 小Pキャンセル > しゃがみ中P or 引き中Pタゲコン > 中ストリボーグ`. A later training UI frame shows combo damage `1482`. | Speaker says there are routes after using rush from jab. | medium | The route-to-damage mapping is less certain because the overlay lists alternatives. Keep as review-needed fixture candidate. |
| 00:41-00:57 | visual + commentary | The same rush-extension discussion continues. A later training UI frame shows combo damage `1527`. | Speaker says the crouching medium punch route has higher damage, based on auto-caption and visible context. | medium | Likely the higher-damage crouching MP variant, but keep route mapping review-needed until manual verification. |

## Contract-Shaped Observation Payload

This payload follows the shape of `contracts/video-observation.schema.json` at a coarse fixture-build level. Segment text is paraphrased; no full transcript is stored.

```json
{
  "schema_version": "2.0.0",
  "clip_metadata": {
    "clip_id": "youtube-nyfngnzjv3m-jp-basic-light",
    "source_fps": 60,
    "normalized_fps": 60,
    "duration_seconds": 49
  },
  "actor_bindings": [
    {
      "actor_ref": "player_jp",
      "character_slug": "jp",
      "binding_confidence": 0.9,
      "binding_basis": [
        "video title",
        "visible JP mirror-match UI",
        "combo overlay"
      ]
    },
    {
      "actor_ref": "dummy_jp",
      "character_slug": "jp",
      "binding_confidence": 0.8,
      "binding_basis": [
        "training mode UI",
        "visible character model"
      ]
    }
  ],
  "segments": [
    {
      "segment_id": "seg-0001",
      "track": "chapter",
      "kind": "basic_light_combo_intro",
      "start_time": "00:08",
      "end_time": "00:12",
      "confidence": 0.9,
      "summary": "JP basic light-start combo chapter begins."
    },
    {
      "segment_id": "seg-0002",
      "track": "combo_observation",
      "kind": "combo_damage_oracle_candidate",
      "start_time": "00:12",
      "end_time": "00:23",
      "confidence": 0.85,
      "summary": "Visible overlay shows crouching light punch into standing light punch into weak Stribog; training UI shows combo damage 1240."
    },
    {
      "segment_id": "seg-0003",
      "track": "combo_observation",
      "kind": "combo_damage_oracle_candidate",
      "start_time": "00:31",
      "end_time": "00:45",
      "confidence": 0.55,
      "summary": "Visible overlay shows a jab-rush extension with crouching medium punch or back-medium-punch target-combo branch into medium Stribog; one observed damage label is 1482."
    },
    {
      "segment_id": "seg-0004",
      "track": "combo_observation",
      "kind": "combo_damage_oracle_candidate",
      "start_time": "00:41",
      "end_time": "00:57",
      "confidence": 0.55,
      "summary": "A second rush-extension variant is associated with observed damage 1527; route mapping remains review-needed."
    }
  ],
  "derived_events": [
    {
      "event_id": "event-0001",
      "kind": "jp_combo_damage_oracle_fixture_seed",
      "source_segment_ids": [
        "seg-0002",
        "seg-0003",
        "seg-0004"
      ]
    }
  ]
}
```

## Boundary Notes

- These are review-only observations.
- Observed damage values are eval oracle labels, not accepted current facts.
- Speaker claims about route usefulness, relative damage, or current applicability are not accepted current facts.
- Combo notation normalization, input timing, drive-rush state, and route variants remain review-needed before a damage calculator consumes ambiguous cases.
- No raw media, frames, screenshots, contact sheets, or full captions are stored in the repository.
