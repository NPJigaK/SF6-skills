# Video Analysis V0 Design

Status: Implemented (v0)
Date: 2026-04-13

This document records the current agreed and implemented design for the first public video-analysis skill, and serves as a maintained reference for the v0 behavior.

## Verified Repo Constraints

- The repo currently manages concept-first SF6 knowledge plus current roster published frame-data exports. The current roster canonical source is `shared/roster/current-character-roster.json`.
- Repo-level canonical published current-fact data lives under `data/exports/<character_slug>/...`.
- Public distributed `skills/kb-sf6-frame-current` reads generated packaged runtime assets under `skills/kb-sf6-frame-current/assets/published/<character_slug>/...`.
- Public skills must start as independent units under `skills/<skill-name>/`.
- `skills/` is the canonical public source. `.agents/skills/` is an exact top-level mirror for repo-local dogfooding.
- Shared extraction to `packages/` or `shared/` should happen only after a second real consumer exists.
- Public skills must not depend on another skill directory.

## Scope / Non-Goals

### Scope

- Build a public video-analysis skill as an observation-first foundation.
- Accept raw video input and normalize the working timeline to 60fps.
- Return a canonical multi-track sparse segment timeline.
- Support optional `key_display` and optional `transcript` tracks.
- Keep actor identity, screen side, and character resolution separate.
- Keep the design open to short combo clips, longer match videos, and commentary or transcript-aligned analysis.

### Non-Goals

- Do not make `event timeline` the truth surface.
- Do not make move taxonomy, `move_id` resolution, or current-fact lookup part of the canonical output.
- Do not track HUD or resource state as part of the first-cut required surface.
- Do not require saved frame or crop artifact paths in the canonical schema.
- Do not depend on `skills/kb-sf6-frame-current/` or any other skill directory at runtime.
- Do not treat commentary claim verification, combo verdicts, or match evaluation as v0 responsibilities.

## Canonical Output Shape

The canonical top-level shape is:

```text
schema_version
clip_metadata
actor_bindings
segments
derived_events   # optional
```

### Shape Rules

- `schema_version` lives at the root.
- `segments` is the canonical required surface.
- `derived_events` is optional and secondary.
- Time is frame-native on the normalized 60fps timeline.
- `start_frame` and `end_frame` use clip-relative 0-based half-open intervals: `[start_frame, end_frame)`.
- `evidence_refs.frame_range` uses the same interval convention.
- `derived_events.frame_index`, if present, uses the same normalized 60fps axis as a 0-based integer.
- Empty intervals are not allowed.

### Interval Invariants

- `start_frame` and `end_frame` are integers.
- `0 <= start_frame < end_frame <= clip_metadata.total_frames`
- A one-frame interval is represented as `[k, k+1)`.
- Interval ordering (`start_frame < end_frame`) and clip-bound checks (`end_frame <= clip_metadata.total_frames`) are semantic invariants for runtime outputs and are not fully enforced by this schema package.

## Track Model

### Canonical Tracks

- `actor_a_local`
- `actor_b_local`
- `interaction`
- `global_phase`
- optional `key_display`
- optional `transcript`

### Track Semantics

- `actor_a_local` and `actor_b_local` are stable actor-local tracks, not screen-side labels.
- `slot_id = p1 | p2 | unknown` is metadata, not a track name.
- `screen_side = left | right | unknown` is segment-local metadata.
- `character_slug` is optional binding metadata.
- `appearance_hint` is optional binding metadata and may be null or empty when appearance does not help.
- `key_display` is a shared modality track with segment-level `actor_ref`.
- `transcript` is a shared modality track with clip-local speaker identity and optional actor binding.

### Clip Metadata

First-cut `clip_metadata` stays frame-native.

Fields that are always present:

- `clip_id`
- `source_fps`
- `normalized_fps = 60`
- `total_frames`

Field value rules:

- `source_fps` must be present and may be `null` when the source rate cannot be established reliably.
- `normalized_fps` must be present and is fixed at `60`.
- `total_frames` must be present and is counted on the normalized timeline.

Optional provenance or display fields:

- `source_duration_sec`
- source type or ingest notes
- crop-presence or modality-presence flags

Not canonical required:

- `normalized_duration_sec`

`normalized_duration_sec` is derived from `total_frames / 60`.

### Canonical Segment Record

Every canonical segment must carry these common fields:

- `segment_id`
- `track`
- `kind`
- `start_frame`
- `end_frame`
- `confidence`
- `evidence_refs[]`

- `segment_id` is a document-wide unique string.
- `confidence` is always present and uses a numeric `[0, 1]` scale.

Track-specific metadata may add fields such as:

- `family`
- `actor_ref`
- `screen_side`
- `overlay_lane`
- `speaker_ref`
- `speaker_role`
- `text`
- `language`
- `source_subtype`

The common record stays stable across tracks. Track-specific payload should extend it without changing the core segment identity and interval model.

## Per-Track Kind Vocabulary

Canonical `segments[].kind` is defined per track and then treated as a union of those per-track vocabularies.

### Actor-Local Tracks (`actor_a_local`, `actor_b_local`)

First-cut canonical `kind`:

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

Additional notes:

- `family` exists as a derived or secondary classification, not as the canonical kind.
- `jump` stays a single kind in first cut.
- `wakeup_rise` is a short segment kind, not a point event.

### Interaction

First-cut canonical `kind`:

- `contact_candidate`
- `hit_connect_candidate`
- `block_connect_candidate`
- `throw_connect_candidate`
- `projectile_presence`
- `side_switch_candidate`

Additional notes:

- `projectile_presence` belongs to `interaction`, not actor-local tracks.
- `crossup` is not a first-cut canonical segment kind. It can be derived later.
- Short overlaps between `contact_candidate` and outcome-like interaction segments are allowed.

### Global Phase

First-cut canonical `kind`:

- `round_intro`
- `fight_active`
- `super_freeze`
- `ko_overlay`
- `pause_or_cut`

Additional notes:

- `global_phase` is a shared, coarse-grained, and generally non-overlapping phase track.
- These are allowed canonical kinds, not a required full coverage set for every clip.

### Key Display

First-cut canonical `kind`:

- `input_sequence_window`

Additional notes:

- This is a provisional first-cut vocabulary.
- `charge_window` and `button_chord_window` are not canonical first-cut kinds.
- `actor_ref` is segment metadata.
- `overlay_lane` may be added as metadata if simultaneous overlays need disambiguation.
- `observed_input_text` may be carried as optional segment metadata for observed input notation.

### Transcript

First-cut canonical `kind`:

- `utterance_span`

Additional notes:

- Transcript meaning lives mostly in metadata, not in a richer first-cut kind vocabulary.
- `speaker_ref` is a clip-local speaker token such as `speaker_1`, `speaker_2`, or `unknown`.
- `speaker_role` is separate metadata such as `commentary`, `actor_voice`, `system_voice`, or `unknown`.
- `actor_ref` is optional metadata and is separate from `speaker_ref`.
- `text` must be present for transcript segments.
- `language` is optional and may be `null` when unknown.
- `source_subtype` is optional metadata such as `provided_transcript`, `asr`, `subtitle_ocr`, or `unknown`.

## Actor Binding Rules

First-cut canonical fields for each actor binding:

- `actor_ref`
- `slot_id`
- `character_slug`
- `appearance_hint`
- `binding_confidence`
- `binding_basis[]`

### Binding Semantics

- `actor_ref` identifies `actor_a` or `actor_b`.
- `slot_id` is always present and uses `p1 | p2 | unknown`.
- `character_slug` is always present and is a single resolved roster slug or `null`.
- Non-null `character_slug` values must use the current roster slug namespace defined by `shared/roster/current-character-roster.json` and the packaged roster inventory recorded in `skills/kb-sf6-frame-current/assets/runtime_manifest.json`.
- `character_candidates[]` is not part of the first-cut canonical schema.
- Same-character matchups are allowed.
- Appearance does not need to be usable for binding. `appearance_hint` is expected to be present and may be `null` or empty.
- `binding_confidence` is always present and expresses how stable the chosen binding is.
- `binding_basis[]` is always present and records why the binding was made.

### Binding Basis Tags

First-cut stable tag vocabulary:

- `hud_slot_ui`
- `persistent_tracking`
- `character_visual`
- `key_display_overlay`
- `transcript_or_audio`
- `user_hint`
- `manual_annotation`
- `unknown`

`binding_basis[]` is a coarse tag array, not free text and not a debug artifact surface.
If no stronger basis exists, use `unknown`.

## Evidence Model

`segments[].evidence_refs` stays lightweight, clip-relative, and reproducible.

First-cut intended shape:

```text
evidence_refs[]:
  - evidence_id
  - source_type
  - frame_range
  - roi_hint? 
  - note?
```

### Evidence Rules

- `source_type` uses the stable vocabulary `video | key_display | transcript`.
- `frame_range` uses the normalized 60fps 0-based half-open convention.
- `roi_hint` uses one of these shapes:
  - `{ "kind": "full_frame" }`
  - `{ "kind": "named_roi", "name": "key_display_left" }`
  - `{ "kind": "xywh_box", "x": 120, "y": 640, "width": 400, "height": 140 }`
- Evidence points back to the source clip, not to required saved artifacts.
- Saved frame or crop artifact paths are not canonical required fields.
- Future materialization may use optional debug or sidecar outputs, not the canonical schema.

## Derived Events Policy

- `derived_events` is optional.
- `derived_events` is downstream-friendly but not the canonical truth surface.
- Each derived event must carry `source_segment_ids` so the event can be traced back to canonical segments.
- If an interpretation only exists as a derived event and cannot be supported by source segments, it should not be treated as canonical.

## Provisional Items Requiring Real Video Review

These items are intentionally not final and should be confirmed against real sample videos before implementation details are frozen:

- Whether `key_display` needs canonical kind expansion beyond `input_sequence_window`
- How stable `actor_ref` binding is for different key-display overlay layouts
- How cleanly `interaction` boundaries can be segmented in real clips
- How transcript content aligns with gameplay in practice

## Open Schema Details

- `actor_bindings` must contain exactly one `actor_a` binding and exactly one `actor_b` binding.
- `segment_id` and `evidence_id` are document-wide unique strings.
- Segment `confidence` and `binding_confidence` both use numeric `[0, 1]`.
- `evidence_refs.source_type` uses `video | key_display | transcript`.
- `roi_hint` is a discriminated object using `full_frame`, `named_roi`, or `xywh_box`.
- `key_display` segments may carry optional `observed_input_text`.
- JSON Schema enforces actor-binding coverage, while document-wide ID uniqueness and interval invariants (`start_frame < end_frame`, `end_frame <= clip_metadata.total_frames`) remain semantic invariants for future concrete-output validation.
