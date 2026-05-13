# Video Analysis Learning Report 20260513 First Smoke Batch

Executed learning report: this is not the template and not a historical smoke
report. Historical smoke reports are not rewritten by #137.

## Report Metadata

| Field | Value |
|---|---|
| Report id | `video-analysis-learning-report-20260513-first-smoke-batch` |
| Date | 2026-05-13 |
| Related issue | #137 |
| Report type | `sanitized_video_analysis_learning_report` |
| Maintainer-local only status | yes |
| Template/executed status | `executed_learning_report` |
| Source reference type | `existing_repo_source` |
| Source reference | five `knowledge/sources/videos/*.md` source artifacts listed below |
| Non-fetching/source policy | `non_fetching_reference: true; no external fetch in this report` |

## Smoke Scope Before Execution

This #137 smoke used only the five maintainer-selected sample candidates. It
did not search for alternate videos, scrape video platforms, run live Hermes,
run `video_analyze`, or add any CI requirement for video analysis.

After the initial Draft PR, `yt-dlp` became available in the maintainer-local
environment. This update used it only for bounded, representative local review
of the five selected samples. The review was not archival, did not require
cookies, credentials, browser profiles, or authenticated state, and did not
produce canonical video observations.

Maintainer-provided sample descriptions, including player rank/status and
coaching context, are sample-selection notes only. They are not accepted
current facts and do not override `official_raw`.

## Reviewed Existing Surfaces

Existing surfaces were audited before sample handling:

- `docs/architecture/sf6-video-analysis-learning-loop.md`
- `docs/testing/smoke-runs/video-analysis-learning-report-template.md`
- `tests/fixtures/video-observation-taxonomy/`
- `workflows/ingest-video.md`
- `workflows/media-scratch-cache-policy.md`
- `docs/architecture/sf6-video-analysis-protocol.md`
- `docs/architecture/external-frame-atlas-policy.md`
- `knowledge/sources/videos/`
- `knowledge/evidence/video-observations/`
- existing `docs/testing/smoke-runs/*video*`
- `evals/questions/video-observation.yaml`
- `tests/validation/validate-video-artifacts.ps1`
- `tests/validation/validate-video-observation-taxonomy-fixtures.ps1`
- `tests/validation/validate-video-learning-report-template.ps1`
- `tests/validation/run-all.ps1`

Audit summary:

- Existing repo artifacts already cover one vertical short and one JP
  combo/training-mode-like source with observed damage labels.
- The #135 fixtures cover baseline gameplay-only, commentary-only,
  livestream/webcam overlay, vertical short, subtitle overlay, clip
  compilation, training mode, and unknown/mixed cases.
- The #136 template is suitable for this report, including tool availability,
  unsafe inferences, not-inferred notes, and cleanup status.
- `workflows/ingest-video.md` remains useful for raw footage to structured
  observation artifacts, but the reviewed samples confirm that commentary,
  overlay-heavy, vertical, subtitle-heavy, and edited formats need the separate
  metadata/report layer before timestamped observation segments.

## Sample Selection Rationale

The selected batch complements existing artifacts by covering five intended
formats rather than repeating the prior JP combo and ACQUA Shorts observations.
All rows below are based on bounded representative local review, not full-video
analysis and not final accuracy evaluation.

| Sample id | Source artifact | Format/category after review | Complements existing artifacts | `workflows/ingest-video.md` relationship | Review status | Key gap/follow-up |
|---|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | `knowledge/sources/videos/youtube-paa8pnlequa.md` | `[gameplay_only]` | Adds normal match footage coverage beyond Shorts and combo-training sources. | Maps cleanly for source-to-observation flow if later timestamped segments are needed; no new observation artifact is added here. | partially_reviewed; bounded representative review | Baseline gameplay smoke; timing remains unsafe without purpose-built observation pass. |
| `yt-sample-commentary-01` | `knowledge/sources/videos/youtube-6vmm2sdtoak.md` | `[gameplay_with_commentary, coaching_review, subtitle_overlay, webcam_overlay]` | Tests source-local commentary separation with visible gameplay excerpts and presenter overlays. | Partially maps; taxonomy/report metadata should classify layout and source-local claims before any transcript-like segment. | partially_reviewed; bounded representative review | Expected commentary sample was not pure commentary-only; report should preserve intended-vs-reviewed taxonomy drift. |
| `yt-sample-overlay-01` | `knowledge/sources/videos/youtube-ztqbhcrtsnc.md` | `[livestream_layout, webcam_overlay, gameplay_with_commentary, subtitle_overlay, coaching_review]` | Tests overlay obstruction, side-panel layout, and HUD visibility. | Partially maps; livestream layout needs metadata classification before timestamped segments. | partially_reviewed; bounded representative review | Overlay and subtitle obstruction reduce HUD/input confidence. |
| `yt-sample-vertical-01` | `knowledge/sources/videos/youtube-shorts-aylextw2jic.md` | `[vertical_short, social_short, subtitle_overlay, gameplay_with_commentary, webcam_overlay]` | Adds a second vertical short distinct from the existing ACQUA pilot. | Partial mapping only; vertical crop and split-screen layout limit segment utility. | partially_reviewed; bounded representative review | Vertical crop, subtitle obstruction, and low-resolution handling. |
| `yt-sample-subtitle-edited-01` | `knowledge/sources/videos/youtube-hwradk0bero.md` | `[training_mode, gameplay_with_commentary, coaching_review, subtitle_overlay, webcam_overlay]` | Tests training-mode coaching footage with subtitles and presenter/chat-style layout. | Partially maps; training UI observations must stay review/eval context and not current-system authority. | partially_reviewed; bounded representative review | Subtitle/layout obstruction and source-local coaching boundaries. |

## Raw Media And Local State Status

| Item | Committed? | Notes |
|---|---|---|
| raw video | no | Bounded local media was used only under the policy scratch root and deleted. |
| downloaded clips | no | Temporary review clips were not committed. |
| frames | no | Temporary visual review derivatives were not committed. |
| screenshots | no | No screenshots were committed. |
| GIFs | no | No GIFs were created or committed. |
| contact sheets | no | Temporary contact sheets were generated only under the policy scratch root for local review and deleted. |
| image dumps | no | No image dumps were committed. |
| browser cache | no | Browser review was not used. |
| captions | no | Caption files were not requested or stored. |
| full transcripts | no | Transcript files were not requested or stored. |
| raw Hermes output | no | Hermes was not used for this smoke. |
| raw `video_analyze` output | no | `video_analyze` was not used or tested. |
| raw yt-dlp output | no | Command output and logs were not committed. |
| local Hermes sessions | no | No local Hermes session state was committed. |
| memory | no | No memory files were committed. |
| local skills | no | No local skills were committed. |
| Curator output | no | No Curator output was committed. |
| logs | no | No logs were committed. |
| caches | no | No cache artifacts were committed. |
| credentials | no | No credentials were used or committed. |
| cookies | no | No cookies or authenticated browser state were used. |
| secrets | no | No secrets were used or committed. |

## Tool Availability

| Tool / Capability | Value | Notes |
|---|---|---|
| Manual review used | yes | Existing repo surfaces, maintainer sample notes, source artifact shape, report boundaries, and representative local visual review were reviewed manually. |
| Maintainer-local Hermes used | no | Intentionally skipped for this #137 smoke. Hermes is allowed when configured but not required; this run used manual bounded visual review via `yt-dlp`. No Hermes prompt, raw output, session, memory, local skill, log, cache, or state was created or committed. |
| `video_analyze` used | no | Not tested and not required. |
| Vision analysis used | yes | Temporary scratch-only contact sheets were used for layout/obstruction review and deleted; no images were committed. |
| yt-dlp | used | Used only for bounded local review of the five maintainer-selected sample URLs represented by repo source artifacts. |
| External visual atlas / non-sample asset fetch | no | The only external media access was bounded review of the five maintainer-selected samples via `yt-dlp` under the policy scratch root, followed by cleanup. No external atlas assets, alternate videos, scrape, mirror, or non-sample cache were used. |
| Tool limitations | bounded representative review only | Findings are layout/taxonomy learning notes, not full-video observations or final accuracy evaluation. |
| Unavailable tools | none required | Hermes and `video_analyze` were intentionally skipped. |
| Hold reasons | none for sample availability | Exact facts, move recognition, frame windows, and coaching conclusions remain held by authority boundaries. |

## yt-dlp / Scratch Handling

The policy-defined scratch/cache root from
`workflows/media-scratch-cache-policy.md` was used for one per-run directory
outside the repository. No repo-local scratch, download, cache, `.dist`,
frame-current, normalization, `data/normalized`, or `data/exports` path was
used for media.

`yt-dlp` was used only for maintainer-local review of the five
maintainer-selected sample URLs represented by the source artifacts below. The
review used bounded, representative media rather than full-video archival
downloads. No cookies, credentials, browser profiles, authenticated state,
subtitles/captions, thumbnails, info JSON, yt-dlp cache, command logs, or raw
tool output were committed.

Cleanup status: the per-run scratch directory, including temporary media and
temporary contact sheets, was deleted before commit. Retained repo-external
cache reason: none. Retained local cache is not canonical evidence.

## Source And Reference Policy

Direct sample URLs are stored only in metadata-only source artifacts under
`knowledge/sources/videos/`. This executed report uses repo source paths and
does not include direct video URLs.

| Sample id | Source ref | Non-fetching reference status | Source freshness limitation |
|---|---|---|---|
| `yt-sample-gameplay-only-01` | `knowledge/sources/videos/youtube-paa8pnlequa.md` | true | Representative local review only; source metadata is review-only and not current-fact authority. |
| `yt-sample-commentary-01` | `knowledge/sources/videos/youtube-6vmm2sdtoak.md` | true | Representative local review only; commentary/coaching claims remain source-local. |
| `yt-sample-overlay-01` | `knowledge/sources/videos/youtube-ztqbhcrtsnc.md` | true | Representative local review only; playstyle claims remain source-local. |
| `yt-sample-vertical-01` | `knowledge/sources/videos/youtube-shorts-aylextw2jic.md` | true | Representative local review only; technique claims remain source-local. |
| `yt-sample-subtitle-edited-01` | `knowledge/sources/videos/youtube-hwradk0bero.md` | true | Representative local review only; coaching claims remain source-local. |

Copyright/storage boundary: raw media and full transcripts are excluded from
repo artifacts. Current-fact authority boundary: exact current facts require
current-fact authority; `official_raw` remains authority.

## Video Taxonomy Classification

The rows below are metadata-layer classifications from bounded representative
review. They do not replace `contracts/video-observation.schema.json`.

| Sample id | video_type | Intended taxonomy changed? | unknown_or_mixed handling | taxonomy_update_needed | Related taxonomy fixture | Relationship to observation schema |
|---|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | `[gameplay_only]` | no | Not used; reviewed segment is coherent gameplay-only. | false | `gameplay-only` | Metadata layer; later segments may map to observation tracks if needed. |
| `yt-sample-commentary-01` | `[gameplay_with_commentary, coaching_review, subtitle_overlay, webcam_overlay]` | yes | Not used; multi-label classification captures the reviewed mixed layout better than `commentary_only`. | false | `gameplay-with-commentary`, `subtitle-overlay` | Metadata layer; commentary claims should remain source-local and paraphrased only. |
| `yt-sample-overlay-01` | `[livestream_layout, webcam_overlay, gameplay_with_commentary, subtitle_overlay, coaching_review]` | no | Not used; layout is mixed but classifiable with existing labels. | false | `livestream-layout-webcam-overlay`, `subtitle-overlay` | Metadata layer before timestamped observation. |
| `yt-sample-vertical-01` | `[vertical_short, social_short, subtitle_overlay, gameplay_with_commentary, webcam_overlay]` | yes | Not used; existing labels capture vertical split layout, subtitles, and presenter overlay. | false | `vertical-short`, `subtitle-overlay` | Fixture-only mapping before segment work. |
| `yt-sample-subtitle-edited-01` | `[training_mode, gameplay_with_commentary, coaching_review, subtitle_overlay, webcam_overlay]` | yes | Not used in reviewed segment; use `unknown_or_mixed` if later sections introduce mixed source contexts. | false | `training-mode`, `subtitle-overlay` | Metadata layer; training UI observations are review/eval context only. |

## Visual Layout

| Sample id | gameplay visibility | HUD visibility | input display visibility | damage label visibility | subtitles | webcam / wipe overlay | overlay obstruction | vertical crop | multi-match compilation | replay speed uncertainty | compression / resolution limitation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | full | full | not_present | not_present | none | none | none | none | false | unknown | minor |
| `yt-sample-commentary-01` | intermittent | partial | partial | visible | present_obstructing | present_non_obstructing | major | none | false | unknown | minor |
| `yt-sample-overlay-01` | intermittent | partial | partial | not_present | present_obstructing | present_non_obstructing | major | none | false | unknown | minor |
| `yt-sample-vertical-01` | partial | cropped | partial | visible | present_obstructing | present_non_obstructing | major | critical | false | unknown | major |
| `yt-sample-subtitle-edited-01` | partial | partial | visible | visible | present_obstructing | present_non_obstructing | major | none | false | unknown | minor |

Layout notes:

- `yt-sample-gameplay-only-01`: gameplay and HUD appeared visible enough for
  coarse layout classification; no subtitles or webcam overlay were present in
  the representative review.
- `yt-sample-commentary-01`: presenters, large captions, and gameplay/training
  excerpts were mixed; this is not pure commentary-only in the reviewed
  segment.
- `yt-sample-overlay-01`: side-panel/presenter layout and large subtitles could
  obstruct part of the playfield or HUD, especially before gameplay settles.
- `yt-sample-vertical-01`: vertical split layout and subtitles limited HUD and
  input visibility.
- `yt-sample-subtitle-edited-01`: training-mode footage, chat/presenter layout,
  and subtitles make source-local coaching review possible but timing-sensitive
  observation unsafe.

## Audio And Commentary Context

| Sample id | audio type | commentary claims are source-local | commentary visible/evidence boundary | transcript status | no raw transcript confirmation |
|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | game_audio_only | true | No commentary claim was accepted; any player/rank context remains maintainer-provided selection context only. | none requested | yes |
| `yt-sample-commentary-01` | gameplay_plus_commentary | true | Coaching/commentary claims are visible as source-local context only and are not accepted conclusions. | none requested | yes |
| `yt-sample-overlay-01` | gameplay_plus_commentary | true | Playstyle analysis claims are source-local review input only. | none requested | yes |
| `yt-sample-vertical-01` | gameplay_plus_commentary | true | Technique claims are source-local review input only. | none requested | yes |
| `yt-sample-subtitle-edited-01` | gameplay_plus_commentary | true | Ground-game coaching claims are source-local review input only. | none requested | yes |

No raw captions, subtitles, or transcripts were requested, stored, quoted, or
committed.

## Analysis Capability

The ratings below are for bounded representative smoke review only.
`exact_current_fact` is always `forbidden`.

| Sample id | candidate_move_identification | hit_block_whiff_candidate_labeling | timing_frame_window_observation | matchup_strategy_summary | input_hud_observation | exact_current_fact |
|---|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | limited | limited | not_safe | not_safe | limited | forbidden |
| `yt-sample-commentary-01` | limited | limited | not_safe | limited | limited | forbidden |
| `yt-sample-overlay-01` | limited | limited | not_safe | limited | limited | forbidden |
| `yt-sample-vertical-01` | limited | limited | not_safe | limited | limited | forbidden |
| `yt-sample-subtitle-edited-01` | limited | limited | not_safe | limited | limited | forbidden |

## Unsafe Inferences

`unsafe_inferences` baseline categories intentionally avoided for every
sample:

- `exact_current_fact_from_video`
- `official_raw_override`
- `exact_frame_data_from_video`
- `raw_tool_output_promotion`
- `training_ui_damage_label_as_current_fact`
- `commentary_claim_as_current_fact`
- `external_visual_atlas_as_current_fact`

These are unsafe inference categories to reject, hold, or route to reviewed
authority checks. They are not conclusions accepted by this report.

## Observed-Safe Notes

- `yt-sample-gameplay-only-01`: gameplay/HUD appeared visible enough for coarse
  layout classification, but exact move facts and timing windows were not
  inferred.
- `yt-sample-commentary-01`: visible presenter/commentary context and gameplay
  excerpts support multi-label classification; coaching claims remain
  source-local review input.
- `yt-sample-overlay-01`: webcam/side-panel layout and subtitles were present
  and may obstruct the playfield or HUD; playstyle claims remain source-local.
- `yt-sample-vertical-01`: vertical crop, split layout, and subtitles limited
  HUD/input visibility.
- `yt-sample-subtitle-edited-01`: training-mode gameplay and coaching overlays
  were visible; observed training UI labels are review/eval context only.
- Observations are review input.
- Observed damage labels are review/eval context only.
- Training UI observations are not current-system authority by default.
- Maintainer-provided sample descriptions are selection context only.
- Player rank/status claims are not accepted as current facts.

## Not-Inferred Notes

- Exact current facts not inferred.
- Exact startup/active/recovery not inferred.
- Exact hit/block advantage not inferred.
- Exact player rank/status not inferred or accepted.
- Exact patch status not inferred.
- Exact move recognition accuracy not evaluated.
- Move-frequency analytics not evaluated.
- `official_raw` not overridden.
- Matchup/coaching conclusion not treated as final authority.
- Commentary claims not treated as current-system authority.
- External visual references were not used and would not override
  `official_raw`.

## Gap / Failure Findings

| Category | Finding |
|---|---|
| `unknown_or_mixed_source_format` | No sample required `unknown_or_mixed` after bounded review, but intended-vs-reviewed taxonomy drift was visible for commentary and vertical samples. |
| `mixed_source_context` | Commentary, overlay, vertical, and subtitle-heavy samples mixed gameplay, presenter overlays, source-local claims, and edited layouts; multi-label taxonomy is necessary. |
| `commentary_claims_not_visible` | Coaching/commentary claims may be spoken or shown in captions, but this report did not transcribe or accept them as conclusions. |
| `overlay_blocks_important_area` | Presenter, side-panel, chat-like, and subtitle overlays can block or reduce important layout areas in the commentary, overlay, vertical, and subtitle-heavy samples. |
| `subtitles_cover_input_or_hud` | Subtitles were present and sometimes obstructing in four reviewed samples. |
| `vertical_crop_removes_hud` | The vertical short limits HUD and input visibility through crop and split layout. |
| `compilation_cuts_destroy_timing` | Edited/commentary layouts make timing-sensitive observation unsafe without a dedicated timestamped pass. |
| `replay_speed_unknown` | Playback speed and source timing remain unknown for all samples. |
| `low_resolution` | The vertical short is low-resolution for HUD/input reading; other samples were adequate only for coarse layout review. |
| `compression_artifacts` | Compression/resolution limitations reduce confidence for small HUD and input details, especially in the vertical short. |
| `ambiguous_character_or_move` | Candidate moves were not promoted to accepted observations; low resolution, overlays, and edits keep move identification limited. |
| Tool availability gap | `yt-dlp` was available for this rerun, but Hermes and `video_analyze` remain intentionally unused and unnecessary for #137. |

## Follow-Up Candidates

| Candidate | Value | Mapping |
|---|---|---|
| taxonomy update candidate | false | Existing #135 labels covered the reviewed samples when used as multi-label metadata. |
| fixture candidate | true | A later scoped fixture may capture intended-vs-reviewed taxonomy drift for commentary/coaching samples. |
| validator candidate | false | No validator change is needed in #137. |
| policy candidate | false | No #140 policy change is made here; #140 may later clarify temporary visual-review derivatives if needed. |
| later issue candidate | #141 only after reviewed observations exist; #140 only for cache-policy wording if maintainers want it | Do not start #138-#141 in this PR. |
| unsupported/hold | false | All five samples were available for bounded representative review; exact facts and timing-sensitive claims remain held by authority boundaries. |

Per-sample follow-up:

- `yt-sample-gameplay-only-01`: useful baseline for a future timestamped
  gameplay-only observation pass, but #137 should not start move recognition.
- `yt-sample-commentary-01`: useful fixture candidate for expected
  commentary-only input that reviews as gameplay-plus-commentary/coaching.
- `yt-sample-overlay-01`: useful for later overlay obstruction and HUD
  visibility evaluation; no frame-atlas work is started here.
- `yt-sample-vertical-01`: useful for vertical crop, subtitle, low-resolution,
  and split-screen limitations.
- `yt-sample-subtitle-edited-01`: useful for training-mode/coaching source
  boundaries and for keeping observed damage/training UI labels non-authority.

## Authority Boundaries

- Video observations are observation/review input only.
- This report is a sanitized learning-loop artifact, not a final accuracy
  evaluation.
- Hermes/video outputs are draft input; no Hermes/video output was used here.
- External visual atlas sources are not current-fact authority.
- `official_raw` remains current-fact authority.
- Exact current facts require current-fact authority.
- Exact startup/active/recovery must not be inferred from video.
- Exact hit/block advantage must not be inferred from video.
- Exact current patch facts must not be inferred from video.
- Player rank/status claims must not be accepted as current facts from video
  or sample descriptions.
- Matchup verdicts and final coaching conclusions are not final authority.
- Commentary claims are source-local review input only.
- Unknown/mixed formats must be recorded as unknown/mixed rather than forced
  into a false category.
- No public `sf6-agent` behavior change.

## Cleanup And Verification

| Field | Value |
|---|---|
| Scratch cleanup status | done; the policy-defined per-run scratch directory and temporary media/review derivatives were deleted before commit |
| Retained repo-external cache reason | none |
| Git diff/status confirmation | PASS; worktree clean after commit; `git diff --check` and `git diff --check origin/main...HEAD` passed |
| Validator commands | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-artifacts.ps1`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-learning-report-template.ps1`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-observation-taxonomy-fixtures.ps1`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1`; `git diff --check`; `git diff --check origin/main...HEAD` |
| Raw-media/local-state check | PASS; scan reported only the pre-existing `./workflows/maintainer-agent-session.md` name-match false positive; no new raw media or local-state artifact was added |
| No raw media / transcript / local state committed confirmation | no raw media, downloaded clips, frames, screenshots, contact sheets, transcripts, raw tool output, local state, cookies, credentials, secrets, or external binary assets were added |

Final confirmation:

- No raw media committed.
- No transcript committed.
- No local state committed.
- No historical smoke reports were rewritten.
- No existing video observation artifacts were rewritten.
- No generated outputs, `.dist`, frame-current assets, normalization assets,
  `data/normalized`, or `data/exports` were intentionally changed.
