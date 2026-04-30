# Video Observation Contract

Video observations are observation artifacts, not accepted strategy knowledge by default.

The contract separates:

- clip metadata
- stable actor bindings
- timeline segments
- evidence references
- optional derived events that point back to source segment IDs

Observations can feed claim review, but they do not become canonical knowledge until reviewed.

## Root Shape

- `schema_version`
- `clip_metadata`
- `actor_bindings`
- `segments`
- `derived_events` (optional)

The machine-readable schema is `contracts/video-observation.schema.json`.

## Time Base And IDs

- Normalize the working timeline to 60 fps.
- Use clip-relative 0-based half-open intervals: `[start_frame, end_frame)`.
- Keep `segment_id`, evidence IDs, and `event_id` values document-wide unique.
- Use numeric confidence values in `[0, 1]`.
- Ensure `start_frame < end_frame` and `end_frame <= clip_metadata.total_frames`.

## Clip Metadata

Required fields:

- `clip_id`
- `normalized_fps = 60`
- `total_frames`

Optional fields:

- `source_fps`

## Actor Bindings

Each observation should bind exactly one `actor_a` and one `actor_b`.

Actor bindings include:

- `actor_ref`: `actor_a` or `actor_b`
- `character_slug`: current-roster character slug or `null`
- `binding_confidence`: numeric `[0, 1]`
- `binding_basis`: evidence labels such as `hud_slot_ui`, `persistent_tracking`, `character_visual`, `key_display_overlay`, `transcript_or_audio`, `user_hint`, `manual_annotation`, or `unknown`

Use stable actors rather than current screen side. Side switches are represented as interaction segments.

## Tracks And Segment Kinds

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
- Include `actor_ref` when the input lane can be bound to an actor.
- Include `observed_input_text` only when it is visible or transcribed.

### `transcript`

- `utterance_span`
- Include `speaker_ref`, `speaker_role`, optional `actor_ref`, `text`, optional `language`, and optional `source_subtype` when available.

## Evidence References

Each segment must include at least one `evidence_refs` item. Evidence references are clip-relative and should identify the video, key-display, transcript, or annotation basis for the segment.

Region hints may use:

- full frame
- named region, such as `key_display_left`
- pixel box with `x`, `y`, `width`, and `height`

Do not require saved frame or crop files in canonical output.

## Derived Events

`derived_events` are optional.

Every derived event must include:

- `event_id`
- `kind`
- `source_segment_ids`

Derived events are never the truth surface. If an event cannot point back to source segment IDs, do not emit it.

## Knowledge Boundary

Video observations may support claim review, but the observation artifact stays separate from accepted knowledge.

Do not encode:

- accepted strategy conclusions
- match verdicts
- combo verdicts
- canonical move IDs
- exact current frame-data values

To promote a reusable conclusion, create a separate claim with `source_kind = reproducible_observation` and review it through `workflows/review-claims.md`.
