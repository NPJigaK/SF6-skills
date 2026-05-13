# SF6 Move Recognition Evaluation Plan

## Purpose

This is a planning artifact for future candidate move-recognition and
move-frequency evaluation.

It does not implement recognition, analytics, dataset creation, local cache
sync, external frame-atlas cache sync, video-usability smoke, public runtime
behavior, or public `sf6-agent` behavior.

The plan builds on the v2.4 audit, taxonomy, report, smoke, external atlas
metadata, and binary/cache guard work. It defines how later scoped issues may
evaluate whether SF6 videos can support:

- candidate move identification
- hit/block/whiff candidate labeling
- move-frequency aggregation
- review-only visual-reference-assisted observations

Video observations remain observation and review input only. Exact current
facts remain grounded in current-fact authority surfaces, especially
`official_raw`.

## Inputs Reviewed

This plan is based on the v2.4 sequence and the existing video observation
surfaces. It does not treat the sequence as implementation approval.

- #134 existing video surface audit and learning-loop integration:
  `docs/architecture/sf6-video-analysis-learning-loop.md`
- #135 video taxonomy fixtures:
  `tests/fixtures/video-observation-taxonomy/`
- #136 sanitized learning report template:
  `docs/testing/smoke-runs/video-analysis-learning-report-template.md`
- #137 first maintainer-local video-analysis learning smoke:
  `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md`
- #138 external frame-atlas source evaluation matrix:
  `data/external-frame-atlas/evaluation/source-evaluation-matrix.json`
- #139 external frame-atlas source manifest schema and fixtures:
  `contracts/external-frame-atlas-source.schema.json` and
  `tests/fixtures/external-frame-atlas/`
- #140 media scratch/cache policy and binary exclusion validator:
  `workflows/media-scratch-cache-policy.md` and
  `tests/validation/validate-no-video-binary-assets.ps1`

Related policy and contract surfaces reviewed:

- `contracts/video-observation.schema.json`
- `contracts/video-observation.md`
- `workflows/ingest-video.md`
- `docs/architecture/sf6-video-analysis-protocol.md`
- `docs/architecture/external-frame-atlas-policy.md`
- `knowledge/sources/videos/`
- `knowledge/evidence/video-observations/`
- existing `docs/testing/smoke-runs/*video*`
- `evals/questions/video-observation.yaml`

## Key Findings From v2.4

- Video formats vary widely: gameplay-only, commentary, livestream layout,
  webcam overlay, vertical short, subtitle-heavy, training-mode, edited clip,
  and unknown/mixed forms all need metadata classification before precise
  observation.
- Bounded representative review is useful for layout and taxonomy learning,
  but it is not final accuracy evaluation.
- Overlay, subtitles, vertical crop, compression, edited cuts, unknown replay
  speed, and source/effective FPS uncertainty reduce confidence.
- Commentary and coaching claims remain source-local review input.
- Exact current facts must not be inferred from video.
- `official_raw` remains current-fact authority.
- External frame-atlas sources are visual/reference candidates only.
- External GIF/image usability against real video remains unproven.
- The #140 binary/cache leakage guard now exists before any future local-only
  cache or usability experiment.
- Hermes and `video_analyze` are optional maintainer-local aids. They are not
  required for public users, public `sf6-agent` behavior, or CI.

## Evaluation Stages

Each later evaluation stage must produce reviewable metadata or sanitized
reports only. A stage may stop early with a hold.

| Stage | Purpose | Allowed inputs | Output | Hold conditions | Forbidden promotion |
|---|---|---|---|---|---|
| 1. Taxonomy and layout classification | Decide whether a video segment is even suitable for observation. | Repo source metadata, #135 taxonomy labels, sanitized #137-style report notes. | `video_type`, layout, audio/commentary, and unknown/mixed classification. | Source format is mixed, gameplay not visible, or context cannot be separated. | Do not promote classification into move recognition or current-fact knowledge. |
| 2. Source FPS / visibility / obstruction gating | Record whether timing and visibility are good enough for candidate observation. | Source fps/effective fps notes, HUD/input visibility, overlay/crop/subtitle/compression notes. | Visibility gates and timing uncertainty. | FPS unknown, effective FPS unstable, replay speed uncertain, overlays block the playfield/HUD, or cuts destroy timing. | Do not infer exact frame windows or exact current facts from gated video. |
| 3. Candidate move observation | Record a candidate visible move or interaction without final authority. | Sanitized local review, visible evidence notes, optional reviewed visual-reference metadata. | Candidate move, candidate interaction, and evidence notes with confidence. | Character/move ambiguity, low confidence, occlusion, visual mismatch, or insufficient segment context. | Do not output exact move confirmation without review. |
| 4. Confidence and review status | Make uncertainty explicit before any downstream use. | Candidate observation and reviewer notes. | Confidence, review status, and follow-up. | Confidence is missing, reviewer cannot reproduce the observation, or evidence is source-local only. | Do not treat unreviewed confidence as accepted knowledge. |
| 5. `official_raw` consistency check | Route current-fact implications to authority review. | Candidate observation plus packaged current-fact authority surfaces. | `official_raw_check` with status and notes. | Current-fact implication is unclear, source patch context is unknown, or apparent conflict appears. | Do not replace or override packaged `official_raw`. |
| 6. Metadata-only external atlas reference | Attach visual-reference metadata without storing assets. | #138 matrix, #139 metadata-only fixtures/manifests, source-evaluation status. | External visual reference metadata and permission/cache status. | Permission, terms, robots, rate limit, mapping, or binary-storage status is unclear. | Do not ingest numeric frame data from external visual sources. |
| 7. Local-only experiment | Test a tiny maintainer-local path after policy gates. | Later explicit issue, repo-external cache, sanitized video sample, #140 validator. | Sanitized smoke report and metadata-only feasibility/usability notes. | Cache leaks toward repo/public bundle, source requires auth, validator fails, or permission is unclear. | Do not commit raw media, binaries, descriptors, contact sheets, or local state. |
| 8. Fixture candidate | Convert stable planning shape into metadata-only fixtures. | Reviewed sanitized reports and stable field candidates. | Fixture proposal or metadata-only fixture in a later scoped PR. | Output shape is unstable, exact facts are implied, or binary-derived fields are required. | Do not create production runtime or dataset. |
| 9. Validator/policy update | Add guardrails only after a repeated failure or stable fixture need. | Fixture gaps, smoke reports, policy gaps, false-positive findings. | Narrow validator or policy update in a scoped issue. | Change would overfit one sample, weaken raw-media boundaries, or duplicate existing policy. | Do not use validators to authorize acquisition or recognition runtime. |

## Candidate Observation Output Shape

Future candidate observation records should remain review metadata. This shape
is illustrative, not a schema added by #141.

```json
{
  "observation_id": "candidate-observation-id",
  "source_video_ref": "knowledge/sources/videos/<metadata-only-source>.md",
  "segment_ref": "segment-or-review-window-id",
  "timestamp_or_segment": "bounded-segment-label",
  "source_video_fps": "unknown",
  "effective_fps": "unknown",
  "visibility_gates": {
    "gameplay_visible": "partial",
    "hud_visible": "partial",
    "input_visible": "unknown",
    "overlay_obstruction": "major",
    "compression_limit": "minor"
  },
  "candidate_move": {
    "character_slug": "jp",
    "move_id": null,
    "source_local_name": null,
    "mapping_status": "ambiguous"
  },
  "candidate_move_confidence": "low",
  "candidate_move_evidence": [
    "visible pose or motion cue, paraphrased",
    "visible interaction cue, paraphrased"
  ],
  "result_candidate": "hit_candidate",
  "hit_block_whiff_confidence": "low",
  "external_visual_reference": {
    "manifest_ref": "tests/fixtures/external-frame-atlas/sf6frames-hitbox-overlay-candidate.json",
    "use": "review_support_only",
    "asset_stored": false
  },
  "official_raw_check": {
    "required": true,
    "status": "not_checked",
    "notes": "Current-fact implications require authority review."
  },
  "visible_evidence": [
    "what appears visible in the reviewed segment"
  ],
  "not_inferred": [
    "exact startup",
    "exact active frames",
    "exact recovery",
    "exact hit advantage",
    "exact block advantage",
    "exact current patch fact"
  ],
  "unsafe_inferences_rejected": [
    "exact_current_fact_from_video",
    "official_raw_override",
    "external_visual_atlas_as_current_fact"
  ],
  "review_status": "needs_review",
  "follow_up": [
    "hold for reviewer",
    "fixture candidate if repeated"
  ]
}
```

Required boundaries:

- Candidate move is not final authority.
- Confidence is required.
- `not_inferred` is required.
- `official_raw_check` is required when current facts may be implicated.
- Review status is required.
- Source FPS and effective FPS uncertainty must be explicit.

## Forbidden Outputs

Future evaluation must not output:

- exact move confirmation without review
- exact startup/active/recovery from video
- exact hit/block advantage from video
- exact current patch facts from video
- matchup verdict as final authority
- coaching conclusion as final authority
- commentary claim as current-system authority
- observed damage label as current-system authority
- training UI label as current-system authority
- external visual atlas as current-fact authority
- external visual atlas overriding `official_raw`
- numeric frame-data ingestion from SF6Frames, Ultimate Frame Data, or any
  external visual atlas
- public `sf6-agent` behavior change
- raw media, transcript, local state, cache, or binary promotion
- perceptual hash or visual descriptor match as exact move confirmation

## Official Raw Consistency Gate

`official_raw` remains current-fact authority.

External visual references and video observations can create review prompts,
holds, or frame-data refresh questions. They cannot become automatic
replacements for packaged current-fact data.

Consistency statuses:

- `not_checked`: no current-fact comparison was performed.
- `consistent`: reviewed comparison found no apparent conflict, but this does
  not promote external visuals or video observations to authority.
- `inconsistent`: apparent conflict exists and must route to hold, reviewer
  notes, or the frame-data refresh workflow.
- `inconclusive`: visibility, source context, source freshness, or mapping is
  insufficient.

`inconsistent` and `inconclusive` statuses must not update packaged
`official_raw`. They create review work only.

## External Frame-Atlas Reference Use

SF6Frames and Ultimate Frame Data are visual/reference candidates only.

External visual references are not numeric frame-data ingestion sources.
Metadata-only manifests from #139 describe candidate sources without storing
assets. #140 binary/cache validation must remain a prerequisite before any
cache experiment.

Hitbox overlay and clean/no-hitbox visual variants should be evaluated
separately:

- Hitbox overlay may support human review, spacing explanation, and why a
  candidate interaction might matter.
- Clean/no-hitbox visual references may be better for visual similarity if
  safely available.
- Direct GIF-to-video matching may be unreliable and must be tested before any
  assumption.

GIF/image usability against real video is unproven. It must be evaluated only
by later gated maintainer-local experiments.

## Future Gated Experiments

These are future recommendations only. #141 does not open issues and does not
approve implementation.

### A. External frame-atlas local cache sync smoke

Purpose:

- Test whether a tiny external visual atlas sample can be acquired safely into
  maintainer-local repo-external cache.

Prerequisites:

- #138 merged
- #139 merged
- #140 merged
- source permission, terms, robots, and rate-limit review complete
- explicit maintainer approval
- CI remains no-live-fetch
- public `sf6-agent` unaffected

Scope:

- one source
- one character
- one or two moves
- repo-external cache only
- no raw binary commit
- no public bundle inclusion
- sanitized report/metadata only
- no `official_raw` override

Outputs:

- sanitized smoke report
- metadata-only cache feasibility notes
- no binary repo artifacts

Hold conditions:

- permission unclear
- robots, terms, or rate limits unclear
- source requires auth or cookies
- asset URL unstable
- cache leaks toward repo/public bundle
- validator fails

### B. External frame-atlas video usability smoke

Purpose:

- Test whether cached GIF/image/visual atlas references actually help
  candidate move identification or review against SF6 video samples.

Prerequisites:

- local cache sync smoke succeeded or was safely held with an approved
  alternate local sample
- #140 binary guard still passes
- selected video sample is maintainer-local and sanitized
- no CI live video analysis
- no public `sf6-agent` behavior

Scope:

- tiny sample only
- one source
- one character
- one or two moves
- one or two representative video segments
- compare hitbox overlay, clean/no-hitbox visual if safely available,
  GIF/contact-sheet style review support, and metadata-only reference context
- evaluate candidate move identification as `useful`, `limited`, `not_safe`,
  or `unsupported`

Record:

- false-positive risks
- overlay/crop/compression failure modes
- source FPS / effective FPS uncertainty
- GIF timing uncertainty
- visual mismatch issues
- whether candidate move identification remains review-only
- what was not inferred
- follow-up fixture, validator, or policy candidates

Forbidden:

- exact move confirmation without review
- exact startup/active/recovery inference
- exact hit/block advantage inference
- numeric frame-data ingestion
- `official_raw` override
- public runtime behavior
- raw binary commit
- raw transcript or local state commit

### C. Candidate move-observation fixture pilot

Purpose:

- After a successful usability smoke, add metadata-only fixtures for candidate
  move observations.

Prerequisites:

- external atlas usability smoke has `useful` or `limited` findings
- no raw media required
- observation shape is stable enough for fixture-only validation

Scope:

- metadata-only fixtures
- no implementation runtime
- no public answer behavior

### D. Move-frequency aggregation evaluation plan update

Purpose:

- Only after candidate move observation shape is stable, plan whether
  move-frequency aggregation is meaningful.

Scope:

- planning only
- metrics candidates only
- no analytics implementation

## Future Metrics

Future metrics are candidates only:

- precision / recall only if a labeled local dataset exists
- unknown/hold rate
- review acceptance rate
- false-positive category rate
- overlay/crop/subtitle failure categories
- source FPS uncertainty rate
- external visual mismatch rate
- `official_raw` consistency hold rate
- human-review effort / time-to-review
- candidate usefulness rating: `useful`, `limited`, `not_safe`, or
  `unsupported`

#141 does not create a dataset, run evaluation, or define pass/fail
thresholds.

## Review And Promotion Boundary

- Hermes output remains draft input.
- `video_analyze` output, if ever used, remains observation support only.
- Human review is required before promotion.
- External visual references remain review support.
- Sanitized reports and metadata fixtures are repo artifacts.
- Raw media, frames, screenshots, contact sheets, transcripts, local Hermes
  state, Curator output, logs, caches, and credentials are not repo artifacts.

Promotion can only happen through reviewed repository artifacts, authority
checks, validators, and scoped PR review.

## Non-Goals

#141 does not:

- implement move recognition
- implement move-frequency analytics
- build a model
- create a dataset
- download or store videos
- download or store GIFs, images, frames, screenshots, contact sheets, or
  transcripts
- fetch external assets
- run local cache sync
- run external frame-atlas cache sync
- run GIF/image video-usability smoke
- add scraper/downloader code
- change frame-current assets
- change normalization assets
- change generated outputs or `.dist`
- change `ingest/frame_data`
- change public `sf6-agent` behavior
- infer exact current facts
- override `official_raw`
- open new GitHub issues unless explicitly requested by the maintainer

## Recommended Future Issue Sequence

These are gated recommendations only.

| Order | Recommendation | Prerequisite | Allowed output | Forbidden output | Expected decision point |
|---|---|---|---|---|---|
| 1 | External frame-atlas local cache sync smoke | #138, #139, #140, source permission/terms/robots/rate-limit review, maintainer approval | Sanitized smoke report and metadata-only cache feasibility notes | Raw binary commit, public bundle inclusion, CI live fetch, `official_raw` override | Is acquisition safe enough to support a tiny repo-external local cache path? |
| 2 | External frame-atlas video usability smoke | Local cache sync smoke success or safe hold with approved alternate local sample; #140 guard still passes | Sanitized usability report with `useful`, `limited`, `not_safe`, or `unsupported` finding | Exact move confirmation, raw media commit, public runtime behavior, numeric frame-data ingestion | Do external visual references help candidate move review enough to justify fixtures? |
| 3 | Candidate move-observation metadata fixture pilot | Usability smoke has `useful` or `limited` finding and stable field candidates | Metadata-only fixtures | Dataset, runtime, raw media, accepted move facts | Is the candidate observation shape stable enough for validation? |
| 4 | Candidate move-observation validator | Fixture pilot merged and repeated failure modes are known | Validator for metadata-only fixtures | Acquisition approval, recognition runtime, binary storage | Can the repo guard candidate observation boundaries without overfitting? |
| 5 | Move-frequency aggregation planning update | Candidate move observation shape and validator are stable | Updated planning doc with metrics candidates | Analytics implementation, dataset creation, public behavior | Are frequency metrics meaningful enough to evaluate? |
| 6 | Optional local-only recognition experiment | Prior stages justify it and maintainer explicitly approves | Maintainer-local sanitized experiment report | Model training, public runtime, raw binary repo artifacts | Does local recognition warrant a separate implementation proposal? |
| 7 | Public behavior decision | Evidence, validators, authority gates, and review boundaries are accepted | Architecture decision or scoped proposal | Silent public `sf6-agent` behavior change | Should any reviewed capability affect public answer behavior? |

## Acceptance Checklist

- [x] #134 existing surface audit is referenced.
- [x] #137 smoke findings are referenced.
- [x] #138 and #139 external frame-atlas metadata work is referenced.
- [x] #140 binary/cache guard is referenced.
- [x] Evaluation stages are documented.
- [x] Candidate observation output shape is documented.
- [x] Forbidden outputs are documented.
- [x] `official_raw` consistency gate is documented.
- [x] Review-only boundary is documented.
- [x] Future metrics are documented as candidates only.
- [x] Future issue sequence is gated recommendations only.
- [x] No implementation, dataset, or raw media is added by this plan.
