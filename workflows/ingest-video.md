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

## Pre-Analysis Repo Context Loading

Before any source-unit video analysis or calibration run, perform a repo-context
loading pass. This applies before raw-local calibration, damage/scaling
interpretation, move/action identification, frame/timing analysis, and
commentary or terminology extraction.

Load only reviewed repository artifacts that are relevant to the source and
analysis question. Select candidates by sample ID, source URL or video ID,
character, topic, previous issue/PR links, and explicit parent-issue follow-up
maps.

Relevant context can include:

- same-sample source metadata, video observations, review notes, and prior
  calibration reports;
- accepted curated glossary pages for stable terminology used in the source;
- source-derived system-mechanics candidates for damage, scaling, timing, or
  route interpretation;
- current-fact boundary workflows when exact current facts may be implicated;
- external visual atlas manifests, when a later approved issue creates them;
- current-fact authority surfaces when the task touches exact values.

For damage or scaling calibration, explicitly load these combo-scaling context
artifacts before analysis:

- `knowledge/curated/mechanics/combo-scaling.md`
- `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md`
- `knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md`

Record the loaded context in each calibration report or review note under a
`Loaded Repo Context` section. For each loaded artifact, list:

- artifact path;
- why it was loaded;
- whether it is accepted curated knowledge, review-only candidate evidence,
  source metadata, observation, or calibration report;
- what it can guide;
- what it cannot authorize.

Loaded repo knowledge may guide analysis, prompts, oracle comparison, and
failure classification. It does not automatically become public answer
authority. In particular:

- curated glossary pages can support stable terminology only;
- review-only mechanics candidates can guide analysis but are not accepted
  current facts;
- observations and raw-video reports are calibration evidence only;
- external visual atlas references are visual references only;
- Hermes memory, local skills, session history, Curator output, logs, and local
  state are non-canonical;
- exact current facts must route to the repo's current-fact authority surfaces;
- video observations, external visual references, and Hermes memory must not
  override packaged `official_raw`.

If relevant repo context exists but was not loaded, record that as a workflow
failure. If no relevant context exists, record that explicitly. Do not silently
proceed as if the repository had no prior knowledge.

When loaded context is insufficient, create or reference a follow-up issue. Add
validators, policies, or schema changes only when a concrete source execution
exposes a repeated or review-blocking failure.

## Raw Local Video Analysis Calibration

Raw local videos may be used to calibrate analysis accuracy when a sanitized
oracle or answer key is available from combo-trial UI, visible HUD labels, or
maintainer-provided context.

For calibration runs:

1. Keep raw video and visual derivatives in repo-external scratch only.
2. Record a first-pass prediction before using the oracle where feasible.
3. Store the oracle only as sanitized text; do not commit screenshots, frames,
   contact sheets, raw OCR, raw tool output, private paths, or raw media.
4. Compare prediction vs oracle for characters, control mode, context,
   sequence, timing, damage, and any visible UI labels.
5. Record correct, partial, wrong, unknown, and not-available fields with
   failure reasons.
6. Apply a concrete workflow, prompt, report, schema, or tooling improvement
   only when the source execution exposes a failure.
7. Treat character, move, damage, timing, and scaling observations as
   calibration evidence, not accepted current facts or public answer authority.

### Combo-Trial Command Prompt Normalization

When a training-mode or combo-trial UI exposes command-list prompts, create a
sanitized command-prompt oracle before attempting move order, frame alignment,
or damage attribution.

For command-prompt normalization:

1. Load relevant repo context first, including same-sample calibration reports,
   source descriptors, observations, review notes, and character move metadata.
2. Use repo-external scratch only for crops, frame samples, OCR attempts, and
   manual visual inspection. Do not commit raw visuals, raw OCR, raw tool output,
   private paths, or raw media.
3. Record row order, sanitized input tokens, source-local context labels,
   confidence, and ambiguity.
4. Normalize visible direction and button icons conservatively. Use `unknown`
   when the prompt is occluded or uncertain.
5. Map prompt rows to candidate move IDs with the character move registry and
   packaged frame-current metadata when available.
6. Map system-action prompts to system-action registry candidates when present.
7. Keep all candidate mappings review-only. Prompt rows do not establish
   accepted route validity, exact execution timing, or current-fact authority.
8. Route frame/input/action alignment to later calibration work before using the
   prompt oracle for hit, damage, or scaling attribution.

### Frame Stepping And Input-History Alignment

When a command-prompt oracle exists and the next task is timing or attribution,
perform bounded frame/input alignment before assigning hits, damage, or scaling
to moves.

For frame/input alignment:

1. Load relevant repo context first, including the same-sample source
   descriptor, observations, review notes, prior calibration reports, and the
   command-prompt oracle.
2. Use repo-external scratch only for frame sequences, crops, contact sheets,
   OCR attempts, and manual visual inspection. Do not commit raw visuals, raw
   OCR, raw tool output, private paths, or raw media.
3. Normalize SF6 system analysis to a 60 game-frame timeline, while separately
   recording source capture fps/cadence, total frames, timestamp-to-game-frame
   conversion, sampling interval, and uncertainty.
   Source capture fps/cadence does not replace the SF6 game-frame basis.
   Sources with 30 fps capture, VFR, dropped frames, or duplicated frames require
   larger uncertainty, and exact frame claims require sufficient capture
   evidence.
4. Align command-prompt rows to approximate frame/timestamp ranges only when
   input-history changes, visible action phases, hit-event candidates, or UI
   label changes support the window.
5. Record right-side input-history clusters as sanitized observations and note
   scrolling, overwrite, crop, or occlusion limits.
6. Record action phases, hit-event candidates, and damage-label changes as
   separate review-only alignment rows.
7. Keep candidate move mappings review-only. Do not infer exact startup,
   active, recovery, hitstop, hit advantage, route validity, or current damage
   facts from video alignment.
8. Route hit/damage/scaling attribution to later calibration work when exact
   action-to-label mapping is still unresolved.

### Damage And Scaling Attribution Calibration

Run damage/scaling attribution only after a command-prompt oracle and bounded
frame/input windows exist.

For damage/scaling attribution:

1. Load relevant repo context first, including source-derived system-mechanics
   candidates, prior calibration reports, command-prompt oracle, frame/input
   alignment report, source observations, and review notes.
2. Use repo-external scratch only if further inspection is needed. Do not
   commit raw video, frames, screenshots, contact sheets, OCR output, private
   paths, raw tool output, or local state.
3. Normalize SF6 system analysis to the 60 game-frame timeline while separately
   recording source capture cadence and uncertainty.
4. Map visible damage, combo, and scaling labels to candidate prompt rows,
   action windows, hit-event candidates, and damage-label windows only where
   evidence supports the mapping.
5. Compare labels against source-derived mechanics candidates as hypothesis
   context, not as current-fact authority.
6. Classify each label as `attributed`, `partial`, `unknown`, `contradicted`,
   `not_applicable`, or `not_available`; record confidence, reason, authority
   boundary, and missing evidence.
7. Keep all attribution evidence review-only unless a separate current-fact
   authority path verifies it.
8. Do not infer official damage/scaling facts, exact route validity, or exact
   hit-by-hit current facts from video alone.
9. Route unresolved visual-action identity to visual-reference work and
   unresolved arithmetic or authority-boundary reasoning to evaluation fixtures
   or follow-up issues.

### External Visual Atlas Acquisition For Calibration

Use external visual atlas acquisition only as calibration support when prior
video-analysis reports show unresolved move/action identity and a later matching
task needs visual references.

For external visual atlas acquisition:

1. Load relevant repo context first, including same-sample calibration reports,
   source review notes, character move registry, external-frame-atlas source
   evaluation records, media scratch/cache policy, and the existing
   `ingest/frame_data` Scrapling fetch setup.
2. Select a tiny scope: one source, one character, and one to three
   move/action candidate families.
3. Check source evaluation status before any network or binary work. If terms,
   robots, permission, rate limits, or asset stability are unresolved, record a
   HOLD before acquisition.
4. Align any future acquisition with `ingest/frame_data` discipline: config
   driven, no-auth/no-cookie boundary, challenge detection, metadata-first
   reporting, and repo-external scratch/cache only.
5. Do not require live external fetch in CI or public answer flows.
6. Do not commit GIFs, images, WebPs, frames, screenshots, contact sheets, raw
   HTML, raw tool output, cache paths, credentials, cookies, or private paths.
7. Commit metadata/report only. Existing external visual references remain
   review-only support and cannot authorize exact move identity, current facts,
   or `official_raw` changes.
8. After a permitted acquisition or approved local reference inspection, record
   whether the visual reference is `usable_as_is`, `needs_preprocessing`,
   `not_usable`, or `inconclusive`. Also record preprocessing needs such as
   frame extraction, resizing, cropping, alpha/background handling, playback
   normalization, overlay separation, or frame-index normalization.
9. Verify that the fetched asset is an actual move visual, not an error
   placeholder, unsupported payload, or unrelated source asset. A valid image
   container by itself is not enough.
10. Path definition alone is not matching readiness. If no permitted visual
   reference was inspected, or if the inspected visual is `not_usable`, route
   the later matching task as blocked until usability is established.
11. Route visual comparison and usefulness evaluation to a later matching task
   only after the visual-reference input and usability boundary are recorded.

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
