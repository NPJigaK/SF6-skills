# Ingest Video Workflow

Use this workflow to turn raw SF6 footage into a structured observation artifact. Video ingest records what can be observed; it does not create accepted strategy knowledge by itself.

The output contract is `contracts/video-observation.md` and the machine-readable schema is `contracts/video-observation.schema.json`.

## Boundaries

- Keep video observation artifacts separate from `knowledge/curated/`.
- Treat `segments` as the observation truth surface.
- Treat `derived_events` as optional projections that point back to segment IDs.
- Do not make match verdicts, combo verdicts, coaching conclusions, or exact move facts part of the observation artifact.
- Do not store full copyrighted video, audio, or transcript text by default.
- Do not emit canonical move taxonomy, move IDs, or exact frame-data values from visual inference alone.

If the task needs accepted strategy knowledge, create candidate claims and run `workflows/review-claims.md` after the observation artifact exists.

## Inputs

Record:

- Raw clip reference or local path.
- Optional transcript, captions, audio notes, or key-display source.
- Optional hints such as player side, character, crop, key-display presence, or known timestamp range.
- Capture or accessed timestamp.
- Any known edits, cuts, slowdowns, overlays, or frame-rate conversions.

## Observation Flow

1. Normalize the working timeline to 60 fps.
2. Establish `clip_metadata` with `clip_id`, `source_fps` when known, `normalized_fps = 60`, and `total_frames`.
3. Bind stable actors as `actor_a` and `actor_b`. Do not rely only on current screen side because side switches can occur.
4. Use `character_slug = null` when character identity is unresolved.
5. Emit sparse `segments` across actor, interaction, global, key-display, and transcript tracks.
6. Attach clip-relative evidence references to each segment.
7. Use 0-based half-open frame intervals: `[start_frame, end_frame)`.
8. Assign confidence values in `[0, 1]`.
9. Emit `derived_events` only when each event lists the source segment IDs it came from.
10. Stop at the observation layer when a conclusion requires current frame data, matchup judgment, or claim review.

## Track Guidance

Use these tracks from the video observation contract:

- `actor_a_local`
- `actor_b_local`
- `interaction`
- `global_phase`
- `key_display`
- `transcript`

Common segment kinds include:

- Actor-local: `jump`, `forward_dash`, `back_dash`, `attack_commit_candidate`, `throw_attempt`, `projectile_emit_candidate`, `blockstun_candidate`, `hitstun_candidate`, `knockdown_state`, `wakeup_rise`
- Interaction: `contact_candidate`, `hit_connect_candidate`, `block_connect_candidate`, `throw_connect_candidate`, `projectile_presence`, `side_switch_candidate`
- Global phase: `round_intro`, `fight_active`, `super_freeze`, `ko_overlay`, `pause_or_cut`
- Key display: `input_sequence_window`
- Transcript: `utterance_span`

Use candidate kinds when the observation is visual and not confirmed by another source.

## Output Shape

Observation artifacts use this root shape:

```json
{
  "schema_version": "2.0.0",
  "clip_metadata": {
    "clip_id": "clip-short-id",
    "source_fps": 59.94,
    "normalized_fps": 60,
    "total_frames": 1800
  },
  "actor_bindings": [
    {
      "actor_ref": "actor_a",
      "character_slug": null,
      "binding_confidence": 0.4,
      "binding_basis": [
        "hud_slot_ui"
      ]
    },
    {
      "actor_ref": "actor_b",
      "character_slug": "ryu",
      "binding_confidence": 0.8,
      "binding_basis": [
        "character_visual"
      ]
    }
  ],
  "segments": [
    {
      "segment_id": "seg-0001",
      "track": "interaction",
      "kind": "contact_candidate",
      "start_frame": 420,
      "end_frame": 426,
      "confidence": 0.7,
      "evidence_refs": [
        "ev-0001"
      ]
    }
  ],
  "derived_events": [
    {
      "event_id": "event-0001",
      "kind": "pressure_sequence_candidate",
      "source_segment_ids": [
        "seg-0001"
      ]
    }
  ]
}
```

## Separation From Accepted Knowledge

Video observations may support later claims, but the observation JSON is not accepted strategy knowledge by default.

When a video suggests a reusable claim:

1. Keep the full observation artifact in a review or observation holding location outside `knowledge/curated/`.
2. Create a separate candidate claim that cites the observation artifact as `source_kind = reproducible_observation`.
3. Set `review_status = needs_review`.
4. Run `workflows/review-claims.md`.

Do not copy the full timeline into a curated knowledge page. Curated pages may reference reviewed claim IDs or concise evidence summaries after review.

## Ingest Report

End video ingest with:

- Clip metadata summary.
- Actor bindings and unresolved identities.
- Segment counts by track.
- Derived event count.
- Low-confidence or conflicting observations.
- Candidate claims created for later review.
