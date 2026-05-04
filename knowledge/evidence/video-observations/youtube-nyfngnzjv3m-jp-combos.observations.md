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
- Observation method: repo-external temporary section downloads, sparse frame sampling, still-frame/crop inspection, contact-sheet inspection, and YouTube metadata inspection.
- Observed section: `00:08-02:00` from the original video.
- Raw media stored in repo: no.
- Full transcript stored in repo: no.

## Timestamped Observations

| Time | Observation kind | Visible observation | Speaker/commentary claim | Confidence | Notes |
|---|---|---|---|---|---|
| 00:08-00:12 | visual + commentary | The chapter opens with JP gameplay and an overlay reading `JPの基本コンボ(小技始動)`. | Speaker introduces this as a basic JP combo section. | high | Chapter boundary and topic are clear from overlay and captions. |
| 00:12-00:23 | visual + commentary | Overlay shows `しゃがみ小P > 立ち小P > 弱ストリボーグ`. The training UI later shows combo damage `1240`. | Speaker describes the basic route as crouching jab/jab into Stribog; captions are noisy but align with the visible overlay. | high | Use as the first usable oracle fixture case. Damage is an observed video label, not current-system authority. |
| 00:31-00:45 | visual + commentary | Overlay shows `小P > 小Pキャンセル > しゃがみ中P or 引き中Pタゲコン > 中ストリボーグ`. A later training UI frame shows combo damage `1482`. | Speaker says there are routes after using rush from jab. | medium | The route-to-damage mapping is less certain because the overlay lists alternatives. Keep as review-needed fixture candidate. |
| 00:41-00:57 | visual + commentary | The same rush-extension discussion continues. A later training UI frame shows combo damage `1527`. | Speaker says the crouching medium punch route has higher damage, based on auto-caption and visible context. | medium | Likely the higher-damage crouching MP variant, but keep route mapping review-needed until manual verification. |
| 00:57-01:10 | visual + commentary | The mid-attack chapter begins. Overlay shows `中攻撃キャンセルラッシュ > しゃがみ大P > 強ストリボーグ > 中トルバラン > トリグラフ`. The training UI later shows combo damage `1824`. | Embedded explanatory text and commentary frame this as a combo from mid attacks after cancel rush. | medium | Route overlay and damage label are clear, but `中攻撃` is a generic starter rather than an exact move. Keep disabled for damage-hidden eval. |
| 01:10-01:21 | visual + commentary | The same route is discussed with the final Triglav changed to OD Triglav. The training UI shows combo damage `3260`. | Embedded explanatory text says using OD Triglav for the final Triglav gives one more Triglav hit. | medium | Useful OD follow-up coverage, but the full route is partly inherited from the preceding overlay. Keep disabled until notation review. |
| 01:27-01:36 | visual + commentary | Overlay shows `中攻撃キャンセルラッシュ > しゃがみ大P > 強ストリボーグ > 前ステ > ラッシュ前大K(ちょい遅らせ) > トリグラフ`. The training UI shows combo damage `2763`. | Embedded explanatory text describes this as a route to push the opponent toward the corner. | medium | Adds corner-carry coverage. The generic starter and delayed forward-heavy-kick timing need notation review before enabling. |
| 01:37-01:48 | visual + commentary | The route demonstration continues while explanatory text warns that inputting forward heavy kick too early can reduce damage because only one hit connects. | Embedded explanatory text cautions about timing and lower damage when forward heavy kick is too early. | medium | This is explanatory context, not an oracle case. |
| 01:56-02:00 | visual + commentary | A later frame shows combo damage `1484` while on-screen text says this spacing lets crouching medium punch carry to the corner. | Embedded explanatory text discusses carrying to the corner when crouching medium punch hits from this position. | low/medium | Damage is visible, but the route overlay is incomplete in the inspected frame. Keep as disabled position/carry candidate. |

## Branch Mapping Re-Review

Existing disabled fixture candidates were re-inspected on 2026-05-04 using the same repo-external scratch policy. This did not introduce a new source video or broaden the observed source scope.

| Case | Re-inspected evidence | Review result | Notes |
|---|---|---|---|
| `jp-basic-light-rush-extension-1482` | Damage label `1482`, alternative-branch overlay, and visible input history. | keep disabled | The branch cannot be uniquely mapped to `しゃがみ中P` or `引き中Pタゲコン` from visible evidence alone. |
| `jp-basic-light-rush-extension-1527` | Damage label `1527`, commentary/visible context around the higher-damage branch, and visible input history. | keep disabled | The crouching-medium-punch branch remains plausible, but still inferred rather than exact. |
| `jp-mid-rush-triglav-1824` | Mid-attack cancel-rush overlay, damage label context, and visible input history. | keep disabled | `中攻撃` remains generic; exact starter was not safely resolved to `2MP`, `5MP`, or another exact move. |
| `jp-mid-rush-od-triglav-3260` | Magenta explanatory overlay saying OD Triglav adds one more Triglav hit. | keep disabled | OD follow-up context is clearer, but the full route still inherits generic starter context from the previous overlay. |
| `jp-mid-corner-carry-rush-fhk-2763` | Corner-carry overlay with `ラッシュ前大K(ちょい遅らせ)` and damage label `2763`. | keep disabled | Delayed `Drive Rush 6HK` wording is confirmed, but timing semantics and generic starter remain unresolved. |
| `jp-mid-position-carry-1484` | Damage label `1484` and position/carry explanatory text. | keep disabled | The inspected frame still lacks a complete route overlay. |

## Contract-Shaped Observation Payload

This payload follows the shape of `contracts/video-observation.schema.json` at a coarse fixture-build level. Segment text is paraphrased; no full transcript is stored.

```json
{
  "schema_version": "2.0.0",
  "clip_metadata": {
    "clip_id": "youtube-nyfngnzjv3m-jp-combo-coverage",
    "source_fps": 60,
    "normalized_fps": 60,
    "duration_seconds": 112
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
    },
    {
      "segment_id": "seg-0005",
      "track": "combo_observation",
      "kind": "combo_damage_oracle_candidate",
      "start_time": "00:57",
      "end_time": "01:10",
      "confidence": 0.65,
      "summary": "Mid-attack cancel-rush route overlay is visible and associated with observed damage 1824; starter remains generic."
    },
    {
      "segment_id": "seg-0006",
      "track": "combo_observation",
      "kind": "combo_damage_oracle_candidate",
      "start_time": "01:10",
      "end_time": "01:21",
      "confidence": 0.6,
      "summary": "OD Triglav follow-up variant is associated with observed damage 3260; full route inherits context from the previous overlay."
    },
    {
      "segment_id": "seg-0007",
      "track": "combo_observation",
      "kind": "combo_damage_oracle_candidate",
      "start_time": "01:27",
      "end_time": "01:36",
      "confidence": 0.6,
      "summary": "Corner-carry route overlay is visible and associated with observed damage 2763; delayed forward-heavy-kick timing remains notation review-needed."
    },
    {
      "segment_id": "seg-0008",
      "track": "combo_observation",
      "kind": "combo_damage_oracle_candidate",
      "start_time": "01:56",
      "end_time": "02:00",
      "confidence": 0.45,
      "summary": "Position/carry discussion is associated with observed damage 1484, but route overlay is incomplete."
    }
  ],
  "derived_events": [
    {
      "event_id": "event-0001",
      "kind": "jp_combo_damage_oracle_fixture_seed",
      "source_segment_ids": [
        "seg-0002",
        "seg-0003",
        "seg-0004",
        "seg-0005",
        "seg-0006",
        "seg-0007",
        "seg-0008"
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
