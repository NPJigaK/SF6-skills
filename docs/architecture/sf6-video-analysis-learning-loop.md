# SF6 Video Analysis Learning Loop

## Purpose

v2.4 is not greenfield video-analysis design. The repository already has video
observation contracts, workflows, media scratch/cache policy, source artifacts,
observation artifacts, smoke reports, evals, and validators.

Existing repo video surfaces must be audited before new taxonomy, report,
fixture, validator, or pipeline work. Existing surfaces are not automatically
correct, but they are the starting point for safe integration and reviewable
change.

This document defines how the v2.4 video-analysis learning loop integrates with
existing surfaces. It records what should be preserved, extended, generalized,
or considered for future supersession.

Video observations remain observation and review input only. No exact current
facts are inferred from video alone. Packaged `official_raw` remains current-fact
authority.

Raw video, frames, screenshots, contact sheets, browser cache, full transcripts,
GIFs, and image dumps are not committed by default. Learning reports are
sanitized repo artifacts, not raw transcripts and not canonical Hermes/video
output.

## Existing surfaces audit

### `contracts/video-observation.schema.json`

Current role: machine-readable schema for a video observation object with
`schema_version`, `clip_metadata`, `actor_bindings`, `segments`, and optional
`derived_events`.

Strengths:

- Keeps observation structure separate from accepted strategy knowledge.
- Requires stable clip metadata, actor bindings, segment timelines, confidence,
  and evidence references.
- Defines a normalized 60 fps timeline and constrained segment tracks.
- Allows extra segment properties, which gives room for observation details
  without changing the root contract.

Gaps or uncertainty:

- It does not model video type, layout, audio, overlay obstruction, analysis
  capability, or failure categories.
- It has no explicit source-level metadata relationship; source artifacts carry
  that separately.
- Some historical "contract-shaped" payloads are not strict schema instances.
  For example, one uses non-enum actor refs and time fields instead of the
  required frame fields. This should be treated as historical evidence of shape
  pressure, not silently rewritten in #134.
- The schema's root is strict while `segments` are permissive. That may be
  enough for observation details but not enough for a stable taxonomy contract.

v2.4 treatment: preserve. Do not replace it in v2.4. Use #135 fixtures to test
a separate metadata classification layer before deciding whether a later schema
extension is warranted.

Follow-up mapping: #135 should test fixture-only mapping and decide whether a
schema extension is needed. #136 should avoid making learning reports pretend to
be strict observation schema instances. Later scoped issues may propose a schema
extension if fixtures prove stable fields.

### `contracts/video-observation.md`

Current role: human-readable contract for observation artifacts, timeline
normalization, actor bindings, tracks, segment kinds, evidence references,
derived events, and knowledge boundaries.

Strengths:

- Clearly separates observation artifacts from accepted knowledge.
- Documents clip-relative half-open frame intervals, 60 fps normalization,
  confidence values, and segment identity.
- Provides track and kind vocabulary for actor-local, interaction, global phase,
  key-display, and transcript observations.
- States that observations may support review but must not encode exact
  current frame-data values, canonical move IDs, or accepted strategy
  conclusions.

Gaps or uncertainty:

- It does not include video-format taxonomy, layout obstruction, audio mixture,
  or analysis capability ratings.
- Existing segment kinds are optimized for gameplay event observations, not for
  livestream frames, vertical shorts, commentary-only sources, or compilations.
- It does not describe sanitized learning reports as a separate repo artifact.

v2.4 treatment: preserve and extend by reference. The contract remains the
observation contract; v2.4 taxonomy should sit beside it until fixtures prove
which fields deserve contract status.

Follow-up mapping: #135 maps taxonomy to existing fields or a sidecar layer.
#136 defines sanitized report shape without duplicating this contract. #141 may
later identify needed segment kinds for move-recognition evaluation.

### `workflows/ingest-video.md`

Current role: maintainer workflow for turning raw SF6 footage into structured
observation artifacts that follow the video observation contract.

Strengths:

- Preserves raw footage to observation separation.
- Defines useful canonical steps: normalize time base, establish
  `clip_metadata`, bind stable actors, emit sparse segments, attach evidence,
  use confidence, and stop at the observation layer.
- Records that current frame data, matchup judgment, and claim review are
  outside direct ingest.
- Ends with a practical ingest report summary.

Gaps or uncertainty:

- It is focused on footage where gameplay, actors, and timestamped segments are
  available.
- It does not classify source format before observation.
- It does not guide commentary-only, livestream layout, webcam overlay,
  subtitle overlay, vertical short, clip compilation, replay speed uncertainty,
  or unknown/mixed handling.
- It does not define how a failed or limited observation becomes a taxonomy,
  fixture, validator, or policy candidate.

v2.4 treatment: preserve as canonical for raw footage to structured observation
artifacts. Extend it later only where taxonomy/report experience proves stable
needs. Consider a future replacement only if multiple v2.4 smokes show that
classification-first workflows cannot be represented as an extension.

Follow-up mapping: #136 should reference its ingest report concepts. #137
should use it for maintainer-local observation. #135 should add taxonomy
fixtures without changing this workflow unless needed. Later scoped issues may
generalize or split the workflow.

### `workflows/media-scratch-cache-policy.md`

Current role: repo boundary and maintainer procedure for temporary media,
screenshots, videos, browser artifacts, and vision artifacts.

Strengths:

- Explicitly forbids raw media, screenshots, downloaded clips, full
  transcripts, browser cache, credentials, and local state by default.
- Defines repo-external scratch roots and per-run directories.
- Requires cleanup or short retention notes outside the repo.
- Provides verification commands to catch repo-local media or private state.

Gaps or uncertainty:

- It is a general media-ingest policy and does not yet name v2.4
  video-learning smoke categories.
- It does not explicitly enumerate frame-atlas cache categories from the
  external frame-atlas policy.
- Binary exclusion validation is not yet its own media-policy validator.
- Retention notes are present but could be more structured for learning-loop
  smoke reports.

v2.4 treatment: preserve. #140 should extend this policy rather than create a
duplicate scratch/cache policy.

Follow-up mapping: #140 owns policy extension and binary exclusion validation.
#137 should record cleanup/retention status in the first learning smoke. #138
and #139 should align any frame-atlas cache language with this policy.

### `docs/architecture/video-observation-v2.2-plan.md`

Current role: historical v2.2 planning document for video source artifacts,
observation artifacts, review artifacts, validation prerequisites, and raw
media boundaries.

Strengths:

- Establishes artifact destinations:
  `knowledge/sources/videos/`, `knowledge/evidence/video-observations/`, and
  `knowledge/review/`.
- States that video observations are observation-only until reviewed and
  promoted.
- Preserves the `official_raw` boundary and identifies observed damage labels
  and training UI observations as review context, not authority.
- Anticipates schema-aware validators, source/segment integrity, raw-media
  boundaries, and conflict handling.

Gaps or uncertainty:

- It is planning-only and predates v2.4 learning-loop needs.
- It does not classify source formats or describe sanitized learning reports.
- Its future wrapper sequence is broader than #134 and partly superseded by
  later v2.3/v2.4 issue sequencing.

v2.4 treatment: preserve as historical planning and build on it. Do not rewrite
it in #134.

Follow-up mapping: #135 and #136 should use its artifact destination model.
#140 should use its validator prerequisite notes. #141 should inherit the
review-only move-recognition boundary.

### `docs/architecture/sf6-video-analysis-protocol.md`

Current role: v2.3 SF6-specific protocol for Codex-to-Hermes video-analysis
delegation and `video_analyze` boundaries.

Strengths:

- Keeps Hermes and `video_analyze` as optional maintainer-local draft-input
  tools, not sources of truth.
- Defines source-fps, effective-fps, and 60F game-native caution.
- Separates direct observation from exact current-fact inference.
- Requires `official_raw` checks for current facts and forbids video-derived
  exact frame values.

Gaps or uncertainty:

- It gives a future observation draft shape but does not define v2.4 taxonomy,
  learning reports, fixtures, or validators.
- It does not classify the many source formats listed in #133/#134.
- It does not define a report-to-fixture/policy/validator loop.

v2.4 treatment: preserve and integrate. The learning loop should treat this
protocol as the guardrail for maintainer-local Hermes/video draft input.

Follow-up mapping: #136 should reuse its sanitized reporting boundary. #137
should use its `video_analyze` unavailable/hold behavior. #141 should use its
source-fps and exact-current-fact boundaries.

### `docs/architecture/external-frame-atlas-policy.md`

Current role: policy for external visual frame/hitbox atlas sources, metadata
manifests, repo-external cache, forbidden binary storage, and future
move-recognition/move-frequency use cases.

Strengths:

- States that external visual atlas sources are visual reference inputs only.
- Preserves `official_raw` authority and forbids numeric frame-data ingestion
  through visual atlas policy.
- Defines metadata-only source evaluation and manifest expectations.
- Defines repo-external cache policy and future use cases for candidate move
  identification, hit/block/whiff labeling, and move frequency aggregation.

Gaps or uncertainty:

- It is intentionally broad and future-facing.
- It does not define the v2.4 video source-format taxonomy or learning report
  template.
- It needs #138/#139 to turn policy into evaluation matrix and manifest
  schema/fixtures.

v2.4 treatment: preserve and reference. Do not duplicate it in the v2.4
learning loop. Use it when video taxonomy or learning reports identify a need
for visual reference support.

Follow-up mapping: #138 owns source evaluation matrix. #139 owns manifest
schema and metadata-only fixtures. #141 owns move-recognition and
move-frequency evaluation planning. #140 should align binary cache validation.

### `knowledge/sources/videos/`

Current role: source metadata records for video sources.

Strengths:

- Existing records capture source URL, title, author/publisher, dates,
  copyright policy, review status, review-after date, extracted scope, media
  handling, and reviewer notes.
- They explicitly state that source records are not final public answer
  evidence.
- They record that raw video, frames, screenshots, contact sheets, browser
  cache, session state, and full captions/transcripts are not stored.

Gaps or uncertainty:

- The records do not include v2.4 taxonomy, layout, audio, capability, or
  gap/failure metadata.
- Source roles are source-specific and may need controlled vocabulary
  normalization later.
- They are good examples of boundaries, but not a complete source metadata
  schema.

v2.4 treatment: preserve historical records. Future taxonomy metadata should
not be retrofitted into these records in #134.

Follow-up mapping: #135 may create metadata-only taxonomy fixtures that point
to source records. #136 should reference source metadata in learning reports.
#137 should select samples with enough source metadata to exercise the loop.

### `knowledge/evidence/video-observations/`

Current role: review-only video observation artifacts.

Strengths:

- Existing records separate visible observations from speaker/commentary
  claims.
- They include source references, timestamped tables, confidence, notes,
  contract-shaped payloads, and boundary notes.
- They explicitly forbid generated-reference promotion, accepted current facts,
  raw media, frames, screenshots, contact sheets, and full captions.

Gaps or uncertainty:

- The payloads are coarse and partly illustrative. They should not be treated
  as strict validator fixtures without cleanup in a scoped issue.
- One payload uses non-contract tracks such as `chapter` and
  `combo_observation`, time strings, and actor refs outside the schema enum.
- They do not have source-format taxonomy, layout fields, audio fields,
  capability ratings, or standardized gap/failure categories.

v2.4 treatment: preserve and leave untouched. Use them as historical audit
evidence, not as current strict schema exemplars.

Follow-up mapping: #135 should add separate taxonomy fixtures or sidecar
classification examples. #136 should generalize learning report output without
rewriting observations. Later scoped issues may normalize observation payloads.

### `docs/testing/smoke-runs/*video*` and related video smoke reports

Current role: sanitized maintainer smoke reports for video observation and
video-derived combo fixture work.

Strengths:

- Reports record date, issue, source, selected scope, scratch root, tooling,
  observations, boundaries, cleanup, and findings.
- They show the repo-external media workflow in practice.
- They consistently state that observed damage labels and observations are not
  current-system authority.

Gaps or uncertainty:

- They are historical reports, not a reusable v2.4 learning report template.
- Report shapes differ across video-observation, combo-fixture, and Hermes
  bridge smoke reports.
- They do not classify unknown/mixed source formats or capability ratings.

v2.4 treatment: preserve historical reports. #136 should generalize their
useful fields into a sanitized learning report template and identify any fields
that should be deprecated or optional.

Follow-up mapping: #136 owns report template and validator. #137 owns the first
v2.4 maintainer-local learning smoke. #140 should preserve cleanup reporting.

### `evals/questions/video-observation.yaml`

Current role: answer-quality eval surface for observation-mode video questions.

Strengths:

- Encodes that video questions should use observation mode.
- Requires evidence-boundary behavior that avoids accepted strategy knowledge
  without review.
- Forbids current frame-data verdicts and unreviewed accepted strategy claims.

Gaps or uncertainty:

- It has only one case.
- It does not cover taxonomy classification, source layouts, audio states,
  capability ratings, or unknown/mixed handling.
- It is an answer-quality surface, not a video-learning fixture surface.

v2.4 treatment: preserve. Do not extend in #134.

Follow-up mapping: #135 may add taxonomy fixtures elsewhere. Later scoped eval
issues may expand answer-quality coverage after the taxonomy and report shape
are stable.

### Existing video validators

Current role: `tests/validation/validate-video-artifacts.ps1` validates video
source artifacts and observation artifacts. Related validators also check
Codex-Hermes delegation fixtures, eval files, current-fact boundaries, and
distribution boundaries.

Strengths:

- Validates required front matter and review-only status.
- Checks source/observation sections and required boundary text.
- Requires observation files to reference existing video source artifacts.
- Rejects text that claims raw video, screenshots, frames, downloaded videos,
  or full transcripts are stored in repo.
- Existing Codex-Hermes fixture validation already covers unavailable
  `video_analyze`, forbidden video-derived current facts, external atlas binary
  import rejection, observed damage label boundaries, and move-frequency
  review-only behavior.

Gaps or uncertainty:

- `validate-video-artifacts.ps1` does not validate embedded JSON against
  `contracts/video-observation.schema.json`.
- It does not validate video taxonomy, layout/audio/capability metadata,
  learning report shape, binary exclusion across all repo paths, or frame-atlas
  cache categories.
- It validates required text rather than a structured report contract.

v2.4 treatment: preserve. Do not add validators in #134 unless the existing
suite requires it for the new documentation. Future validator work belongs in
#135, #136, and #140.

Follow-up mapping: #135 owns taxonomy fixture/validator decisions. #136 owns
learning report validator. #140 owns media binary exclusion validation. Later
issues may add strict schema validation for observation payloads.

## Existing schema relationship

v2.4 taxonomy should remain a separate metadata classification layer first. #135
should provide metadata-only fixtures that map to existing observation fields
where possible. Do not silently replace `contracts/video-observation.schema.json`.

The decision for #135 is:

1. Do not replace the schema.
2. Do not immediately extend the schema for every taxonomy/layout/audio field.
3. Add fixture-only mapping to prove which fields are stable.
4. Consider a future schema extension only after the fixture set shows a small,
   durable field group that belongs in the canonical observation contract.

The existing schema relationship by field is:

- `clip_metadata`: remains the place for `clip_id`, source fps when known,
  normalized fps, and total frame count. Video type, layout, audio, and
  capability ratings should not be forced into `clip_metadata` unless a later
  schema extension defines a stable metadata object.
- `source_fps`: useful for capability ratings and timing uncertainty. Unknown,
  variable, edited, slowed, or compiled sources should lower timing capability
  rather than produce exact frame conclusions.
- `normalized_fps`: remains fixed at 60 for the working timeline. This is an
  observation aid and not exact current-fact authority.
- `total_frames`: useful when a strict clip timeline exists. Some learning
  reports may not have a stable total frame count; those should remain reports
  or taxonomy fixtures, not strict observation payloads.
- `actor_bindings`: useful when stable actors can be identified. Commentary-only
  videos, unclear layouts, compilations, or multi-match sources may have
  unresolved or non-applicable actor bindings. That is a reason for
  `limited`, `not_safe`, or `unknown` capability, not a reason to invent
  bindings.
- `segments`: remain the observation truth surface for timestamped visible,
  key-display, transcript, actor, interaction, and global-phase observations.
  Taxonomy, layout, audio, and capability data may map to segments only when
  they are directly observed at a time range.
- `derived_events`: remain optional projections that point back to source
  segment IDs. They must not become the taxonomy authority and must not encode
  accepted conclusions.

Existing segment tracks map as follows:

- `actor_a_local` and `actor_b_local`: candidate actor actions when stable
  actors are visible.
- `interaction`: contact, hit/block/whiff candidates, projectile presence, and
  side-switch candidates.
- `global_phase`: round state, fight active state, pause/cut, super freeze, KO,
  and possible future observable layout interruption markers if scoped.
- `key_display`: visible input display windows when an input lane can be
  observed and optionally bound to an actor.
- `transcript`: utterance spans, subtitle/caption summaries, and commentary
  claims when paraphrased and bounded.

Taxonomy, layout, audio, and capability data should usually remain separate
metadata for #135/#136:

- A source may be `vertical_short` for the whole run while only some segments
  have visible gameplay.
- A livestream layout may have webcam overlay and subtitles at different times.
- Commentary-only audio may create a reviewable transcript claim without a
  gameplay segment.
- Capability ratings describe what analysis is safe, not what happened at a
  frame interval.

Future replacement should be proposed only if repeated fixtures show that the
existing segment model cannot represent reviewable observations even with a
sidecar classification layer. Current evidence supports extension or sidecar
metadata, not replacement.

## Existing workflow relationship

`workflows/ingest-video.md` remains useful and canonical for raw footage to
structured observation artifacts when the input supports clip-level observation.

Steps that remain useful:

- Record raw clip reference or local path without committing raw media.
- Record optional transcript, captions, audio notes, key-display source, and
  hints.
- Record known edits, cuts, slowdowns, overlays, or frame-rate conversions.
- Normalize the working timeline to 60 fps where a strict clip timeline exists.
- Establish `clip_metadata`.
- Bind stable actors or mark character identity unresolved.
- Emit sparse segments across actor, interaction, global, key-display, and
  transcript tracks.
- Attach evidence references and confidence.
- Emit derived events only when they point back to segments.
- Stop at observation when current facts, matchup judgment, or claim review are
  required.

Where v2.4 taxonomy/report fields fit:

- Before observation: classify source type, layout, audio, and expected
  capability. This decides whether to proceed, hold, or produce a gap report.
- During observation: record layout and obstruction only as segments when they
  are time-bound observations.
- After observation: produce a sanitized learning report with taxonomy match or
  taxonomy gap, capability ratings, failure categories, fixture candidates, and
  policy/validator candidates.

Where the workflow may be too narrow:

- Livestream layouts may include player cams, sponsor overlays, chat, score
  bugs, scene cuts, and multiple gameplay regions.
- Vertical shorts may crop HUD, compress action, and overlay subtitles or face
  cam over important regions.
- Subtitle overlays may cover input/HUD or damage labels.
- Commentary-only videos may have no visible gameplay segment but still create
  reviewable source-local claims.
- Clip compilations may destroy timing continuity and combine different
  matches, patches, or contexts.
- Unknown/mixed videos may need classification as `unknown_or_mixed` rather
  than forced actor bindings and frame timelines.

Extension is enough for #134 and likely for #135/#136. A future replacement
proposal may be needed only if #137 and later learning smokes repeatedly show
that classification-first reports cannot be reconciled with the observation
workflow.

## Existing media scratch/cache policy relationship

`workflows/media-scratch-cache-policy.md` already defines the repo-external
scratch/cache policy for temporary media work.

Existing repo-external scratch/cache policy:

- Use OS/user cache outside the repository.
- Create one per-run directory.
- Use that directory for temporary downloads, extracted frames, screenshots,
  OCR intermediates, browser exports, and other working files.
- Delete scratch files by default after the run.
- If retained briefly, keep outside the repo, record the reason, prefer seven
  days or less, and do not treat retained cache as canonical evidence.

Existing forbidden raw media boundaries:

- Raw article images.
- Screenshots.
- Copied article images.
- Downloaded videos or clips.
- Full transcripts.
- Large excerpts.
- Browser cache artifacts.
- Session, memory, cron, or profile state.
- Credentials, tokens, and local `.env` files.

#140 should extend this existing policy rather than create a duplicate. Needed
extension areas:

- Video-learning smoke report cleanup and retention fields.
- Frame-atlas cache category names and allowed repo-external cache roots.
- Binary exclusion validation for video, image, frame, GIF, contact sheet,
  browser cache, transcript, and local state patterns.
- Temporary local cache categories such as media-ingest, video-learning smoke,
  external-frame-atlas, browser exports, OCR intermediates, and tool outputs.
- Cleanup/retention notes that distinguish deleted scratch, temporary retained
  scratch, and non-canonical local cache.

## Existing artifact relationship

`knowledge/sources/videos/` records represent source-level metadata and
review-input boundaries. They should identify the source URL, title, author or
publisher, publication/access/capture dates, extracted scope, language or topic
notes, media handling, copyright/storage policy, review status, and reviewer
notes. They are not final public answer evidence.

`knowledge/evidence/video-observations/` records represent review-only
timestamped observations. They may include visible observations,
speaker/commentary claim summaries, confidence, notes, source references,
contract-shaped payloads, and boundary notes. They are not accepted strategy
knowledge, not accepted current facts, and must not feed generated references
without later review.

`docs/testing/smoke-runs/*video*` reports represent historical sanitized
maintainer smoke reports. Related combo-damage smoke reports also use video
inputs and record raw-media boundaries. They show working practices but should
not be rewritten into a new template by #134.

`evals/questions/video-observation.yaml` covers an answer-quality case where a
video-derived user question should use observation mode and avoid current
frame-data verdicts or unreviewed accepted strategy claims.

Historical artifacts should be preserved and left untouched in #134. Future
work may generalize their useful shape, deprecate fields in a new template, or
add sidecar fixtures, but this issue does not rewrite historical smoke reports
or existing observation artifacts.

## Learning loop

The v2.4 learning loop is:

1. Maintainer-local observation.
   Use local tools, manual review, Hermes, or video tooling only when scoped.
   Raw media, transcripts, frames, screenshots, contact sheets, browser cache,
   and local state stay outside the repo.
2. Sanitized report.
   Commit only a sanitized repo artifact that records source reference,
   method, limitations, cleanup, capability, taxonomy match or gap, and
   follow-up candidates. Do not include raw transcript or media dumps.
3. Taxonomy classification or taxonomy gap.
   Classify the source with the current taxonomy, or record why
   `unknown_or_mixed` or a new category candidate is needed.
4. Gap/failure note.
   Record observation blockers such as overlay obstruction, crop, low
   resolution, replay speed uncertainty, compilation cuts, or claims not
   visible in gameplay.
5. Fixture candidate.
   Propose metadata-only taxonomy fixtures, report fixtures, eval cases, or
   observation fixtures for a later scoped PR. Do not add them in #134.
6. Validator/policy candidate.
   Record whether a validator, policy extension, or schema extension should be
   considered in #135, #136, #140, #141, or later scoped issues.
7. Reviewed PR.
   Promote only reviewed, scoped, validated artifacts. Hermes/video outputs,
   local cache, and raw transcripts are draft input only until transformed into
   repo artifacts through review.

Observations are review input. Learning reports are sanitized. Hermes/video
outputs are draft input. Raw transcripts and media are not committed. Exact
current facts still require current-fact authority.

## Initial video type taxonomy

The initial taxonomy is a multi-label classification layer. A source may have
more than one label; unknown and mixed formats must be accepted rather than
forced into false categories.

- `gameplay_only`: visible SF6 gameplay without meaningful commentary,
  face-cam, or non-game overlay beyond normal video framing.
- `commentary_only`: speaker, captions, slides, or text discuss SF6 while no
  gameplay evidence is visible enough for observation.
- `gameplay_with_commentary`: gameplay is visible and source-local commentary
  or captions describe it.
- `livestream_layout`: stream layout with score bugs, cameras, chat, scene
  frames, sponsor overlays, multiple panels, or broadcast composition.
- `webcam_overlay`: player or commentator camera overlay covers part of the
  frame.
- `subtitle_overlay`: subtitles, captions, or large text overlays appear over
  gameplay or UI.
- `vertical_short`: vertical aspect, phone-first presentation, or cropped
  short-form layout.
- `clip_compilation`: multiple clips, cuts, matches, or contexts are edited
  together.
- `replay_review`: replay footage or replay UI is used for review or
  explanation.
- `training_mode`: training mode UI, dummy state, damage labels, input display,
  or route demonstrations are visible.
- `tournament_broadcast`: bracket, player names, commentators, broadcast
  overlays, round score, or event layout is part of the source.
- `coaching_review`: source is framed as coaching, analysis, review, or lesson,
  often with pauses, rewinds, telestration, or commentary.
- `social_short`: short-form social media clip with platform-native framing,
  captions, stickers, music, or rapid edits.
- `unknown_or_mixed`: source format is unknown, mixed, too edited, too low
  context, or unsafe to classify precisely.

Mapping to existing fields:

- Taxonomy labels belong in #135 metadata fixtures or #136 report metadata.
- Visible gameplay/commentary can map to `segments` when time-bound.
- Training mode UI, input display, and subtitles may map to `key_display`,
  `transcript`, or `global_phase` segments when directly observed.
- Overall source class should not be forced into current
  `clip_metadata` without a schema extension.

## Visual layout fields

The visual layout fields should be recorded as structured metadata in #135/#136
and mapped to segments only when time-bound.

- `gameplay_visibility`: `full`, `partial`, `intermittent`, `none`, or
  `unknown`.
- `hud_visibility`: `full`, `partial`, `blocked`, `cropped`, `none`, or
  `unknown`.
- `input_display_visibility`: `visible`, `partial`, `blocked`, `not_present`,
  or `unknown`.
- `damage_label_visibility`: `visible`, `partial`, `blocked`, `not_present`,
  or `unknown`.
- `subtitles`: `none`, `present_non_obstructing`, `present_obstructing`, or
  `unknown`.
- `webcam_or_wipe_overlay`: `none`, `present_non_obstructing`,
  `present_obstructing`, or `unknown`.
- `overlay_obstruction`: `none`, `minor`, `major`, `critical`, or `unknown`.
- `vertical_crop`: `none`, `minor`, `major`, `critical`, or `unknown`.
- `multi_match_compilation`: `false`, `true`, or `unknown`.
- `replay_speed_uncertainty`: `none`, `possible`, `likely`, or `unknown`.
- `compression_resolution_limitation`: `none`, `minor`, `major`, `critical`,
  or `unknown`.

These fields should influence analysis capability. For example, blocked input
display should lower input/HUD observation capability, and replay speed
uncertainty should lower timing/frame-window capability.

## Audio/commentary fields

Audio/commentary classification should be separate from transcript segments.
Transcript segments record what was said when paraphrased; audio metadata
records what kind of audio evidence exists.

- `no_audio`: no usable audio track.
- `game_audio_only`: game audio is present without meaningful speech.
- `commentary_only`: speech or narration is present without usable game audio
  or visible gameplay evidence.
- `gameplay_plus_commentary`: game audio and commentary are both present.
- `mixed_voice_chat`: voice chat, stream chat narration, multiple speakers, or
  ambiguous voice sources are mixed.
- `music_ambient`: music or ambient audio dominates or is mixed in a way that
  reduces analysis utility.
- `unknown`: audio was not checked, unavailable, muted, or cannot be
  classified.

Commentary claims are source-local claims. They may be recorded as paraphrased
transcript observations, but they must not become current-system authority
without review.

## Analysis capability rating

Ratings:

- `likely`: the source appears suitable for the dimension, with ordinary review
  caveats.
- `limited`: the source may support partial candidate observation, but gaps,
  overlays, crop, compression, edits, or uncertainty reduce confidence.
- `not_safe`: the source should not be used for that dimension because the
  evidence is too ambiguous or misleading.
- `forbidden`: the dimension is not allowed from video alone or is outside the
  authority boundary.
- `unknown`: the dimension was not checked or cannot be assessed.

Dimensions:

- `candidate_move_identification`: may be `likely`, `limited`, `not_safe`, or
  `unknown` depending on visibility and reference support. It is never final
  move authority without review.
- `hit_block_whiff_candidate_labeling`: may be `likely`, `limited`,
  `not_safe`, or `unknown` when contact, spark, guard, whiff, and context are
  visible enough. It remains candidate labeling.
- `timing_frame_window_observation`: may be `likely` only when source fps,
  effective fps, playback speed, cuts, and timeline are controlled enough for
  observation. It is often `limited` or `not_safe`.
- `matchup_strategy_summary`: may be `likely` or `limited` for source-local
  qualitative summary, but it is not accepted matchup knowledge without review.
- `input_hud_observation`: may be `likely`, `limited`, `not_safe`, or
  `unknown` depending on HUD/input display visibility and obstruction.
- `exact_current_fact`: must be `forbidden` from video alone. Exact current
  facts require packaged current-fact authority such as `official_raw`.

## Gap/failure categories

Gap and failure categories should be recorded in sanitized reports and later
fixtures. Initial categories:

- `overlay_blocks_important_area`
- `subtitles_cover_input_or_hud`
- `vertical_crop_removes_hud`
- `compilation_cuts_destroy_timing`
- `replay_speed_unknown`
- `commentary_claims_not_visible`
- `low_resolution`
- `compression_artifacts`
- `ambiguous_character_or_move`
- `mixed_source_context`
- `unknown_or_mixed_source_format`

These categories should lead to `limited`, `not_safe`, `forbidden`, or
`unknown` capability ratings where appropriate. They are learning-loop signals,
not automatic failures.

## Follow-up mapping

- #135 taxonomy fixtures / validator:
  - Add metadata-only taxonomy fixtures.
  - Map taxonomy/layout/audio/capability/gap fields to existing observation
    fields where possible.
  - Decide whether validation should remain fixture-only or propose a narrow
    schema extension.
  - Include `unknown_or_mixed` acceptance.
- #136 learning report template / validator:
  - Generalize useful fields from existing smoke reports: source, issue,
    method, tooling, classification, capability, gaps, raw-media boundary,
    cleanup, findings, and follow-up candidates.
  - Preserve sanitized reporting and no raw transcript/media dumps.
  - Deprecate report fields that imply canonical Hermes/video output.
- #137 first maintainer-local learning smoke:
  - Select samples that exercise at least one straightforward gameplay source
    and at least one constrained or mixed source.
  - Prefer samples that can be observed without committing raw media or
    relying on live CI video analysis.
  - Record `video_analyze` unavailable/deferred behavior if applicable.
- #138 external frame-atlas source evaluation matrix:
  - Use this document only when taxonomy/capability gaps indicate visual
    reference support is relevant.
  - Preserve external atlas policy boundaries and do not fetch assets in #138
    unless explicitly scoped.
- #139 external frame-atlas manifest schema:
  - Keep manifests metadata-only by default.
  - Align source roles and cache boundaries with the external frame-atlas
    policy and media scratch/cache policy.
- #140 media scratch/cache policy extension and binary exclusion validator:
  - Extend `workflows/media-scratch-cache-policy.md`.
  - Add binary exclusion validation for raw media, frames, screenshots,
    contact sheets, GIFs, transcripts, browser cache, local state, and
    frame-atlas cache categories.
- #141 move-recognition / move-frequency evaluation plan:
  - Treat move recognition and move frequency as candidate, review-only
    analysis.
  - Use capability ratings and gap categories to define when evaluation is
    possible, limited, or unsafe.
  - Preserve `official_raw` and exact-current-fact boundaries.
- Later scoped issues:
  - Strict schema validation for embedded observation payloads.
  - Possible video observation schema extension after fixture evidence.
  - Possible ingest workflow generalization if classification-first reports
    cannot be represented as an extension.
  - Possible observation artifact normalization, without rewriting historical
    artifacts casually.

## Boundaries

- Do not infer exact current facts from video alone.
- Do not override `official_raw`.
- Do not treat observed damage labels as current-system authority.
- Do not treat training UI observations as current-system authority by default.
- Do not treat external visual atlas sources as current-fact authority.
- Do not treat Hermes memory, sessions, local skills, Curator output, logs,
  caches, or private local state as evidence.
- Do not commit raw video, frames, screenshots, contact sheets, browser cache,
  full transcripts, GIFs, image dumps, or external binary assets by default.
- Do not make live Hermes, live video analysis, online tool availability, or
  `video_analyze` required in CI.
- Do not rewrite historical smoke reports or existing observation artifacts in
  this issue.
- Do not change public `sf6-agent` behavior, frame-current assets,
  normalization assets, generated outputs, or `.dist` in #134.

## Recommendation

#135 should use a separate metadata classification layer with fixture-only
mapping to existing observation fields. It should not replace
`contracts/video-observation.schema.json`. A schema extension can be proposed
later only if fixtures show stable fields that belong in the canonical
observation contract.

#136 should preserve the existing smoke reports' useful practices: sanitized
method summaries, source references, capability/tooling notes, boundary
confirmation, cleanup status, findings, and follow-up candidates. It should
generalize those practices into a learning report template, and deprecate any
shape that implies raw transcript storage, canonical Hermes output, or accepted
video-derived facts.

#137 should select video samples that exercise both useful observation and
failure handling. At least one sample should make unknown/mixed or limited
capability handling realistic, such as a vertical short, overlay-heavy
livestream layout, commentary-only source, or compilation.

#140 should extend `workflows/media-scratch-cache-policy.md` rather than create
a duplicate policy. The extension should add v2.4 video-learning smoke,
frame-atlas cache, binary exclusion validation, temporary cache category, and
cleanup/retention details while preserving the existing repo-external scratch
model.
