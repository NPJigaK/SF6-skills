# Output Contract

This skill emits observation-first SF6 video analysis output. `segments` are the truth surface. `derived_events` are optional projections.

## Root Shape

- `schema_version`
- `clip_metadata`
- `actor_bindings`
- `segments`
- `derived_events` (optional)

## Time Base and IDs

- The canonical timeline is normalized to 60fps.
- Segment and evidence ranges use clip-relative 0-based half-open intervals: `[start_frame, end_frame)`.
- `segment_id` and `evidence_id` are document-wide unique strings.
- Segment `confidence` and `binding_confidence` use numeric `[0, 1]`.
- Document-wide ID uniqueness is a semantic invariant for runtime outputs and is not fully enforced by this shell-only validator.

## Clip Metadata

- `clip_id`
- `source_fps` (`null` allowed when unknown)
- `normalized_fps = 60`
- `total_frames`
- optional `source_duration_sec`

## Actor Bindings

- `actor_ref`: `actor_a | actor_b`
- `slot_id`: `p1 | p2 | unknown`
- `character_slug`: resolved current-roster slug or `null`
- `appearance_hint`: string or `null`
- `binding_confidence`: numeric `[0, 1]`
- `binding_basis[]`: `hud_slot_ui | persistent_tracking | character_visual | key_display_overlay | transcript_or_audio | user_hint | manual_annotation | unknown`
- The `actor_bindings` array must include exactly one `actor_a` binding and exactly one `actor_b` binding.

## Tracks and Kinds

### `actor_a_local` / `actor_b_local`

- `jump`
- `forward_dash`
- `back_dash`
- `attack_commit_candidate`
- `throw_attempt`
- `projectile_emit_candidate`
- `blockstun_candidate`
- `hitstun_candidate`
- `knockdown_state`
- `wakeup_rise`

### `interaction`

- `contact_candidate`
- `hit_connect_candidate`
- `block_connect_candidate`
- `throw_connect_candidate`
- `projectile_presence`
- `side_switch_candidate`

### `global_phase`

- `round_intro`
- `fight_active`
- `super_freeze`
- `ko_overlay`
- `pause_or_cut`

### `key_display`

- `input_sequence_window`
- metadata: `actor_ref`, optional `overlay_lane`, optional `observed_input_text`

### `transcript`

- `utterance_span`
- metadata: `speaker_ref`, `speaker_role`, optional `actor_ref`, `text`, optional `language`, optional `source_subtype`

## Evidence

- `source_type`: `video | key_display | transcript`
- `frame_range` uses the normalized 60fps interval convention.
- `roi_hint` uses one of these shapes:
  - `{ "kind": "full_frame" }`
  - `{ "kind": "named_roi", "name": "key_display_left" }`
  - `{ "kind": "xywh_box", "x": 120, "y": 640, "width": 400, "height": 140 }`

## Derived Events

- `derived_events` is optional.
- Every derived event must carry `source_segment_ids`.
- Derived events are never the truth surface.
