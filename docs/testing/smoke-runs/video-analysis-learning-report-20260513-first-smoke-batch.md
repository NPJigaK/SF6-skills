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

Direct video-content review was held because `yt-dlp` was not available in the
maintainer-local command environment, and no replacement live browser,
Hermes-video, or `video_analyze` path was used. The smoke still records the
sample set, source artifacts, tool gap, intended taxonomy coverage, and
follow-up shape so later #137 review can proceed without inventing
observations.

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
- `workflows/ingest-video.md` remains useful when video content can be
  reviewed, but commentary-only, overlay-heavy, subtitle-heavy, and
  unavailable-tool cases need the separate metadata/report layer first.

## Sample Selection Rationale

The selected batch complements existing artifacts by covering five intended
formats rather than repeating the prior JP combo and ACQUA Shorts observations.
Because direct video-content review was held, the selected format/category
values below are maintainer-provided intended coverage and taxonomy planning
signals, not verified visual observations.

| Sample id | Source artifact | Intended format/category | Complements existing artifacts | `workflows/ingest-video.md` relationship | Review status | Key gap/follow-up |
|---|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | `knowledge/sources/videos/youtube-paa8pnlequa.md` | `gameplay_only` | Adds normal match footage coverage beyond Shorts and combo-training sources. | Expected to map cleanly if gameplay/HUD are visible, but not verified. | held/unavailable | Tool availability; future baseline gameplay smoke. |
| `yt-sample-commentary-01` | `knowledge/sources/videos/youtube-6vmm2sdtoak.md` | commentary / coaching review | Tests source-local commentary separation. | May not map cleanly if gameplay is absent or intermittent. | held/unavailable | Commentary-only handling; source-local claims. |
| `yt-sample-overlay-01` | `knowledge/sources/videos/youtube-ztqbhcrtsnc.md` | livestream-layout-webcam-overlay | Tests overlay obstruction and HUD visibility. | Needs taxonomy/layout metadata before any timestamped segments. | held/unavailable | Overlay obstruction and HUD visibility classification. |
| `yt-sample-vertical-01` | `knowledge/sources/videos/youtube-shorts-aylextw2jic.md` | vertical short | Adds a second vertical short distinct from the existing ACQUA pilot. | Likely partial mapping; crop/subtitles may limit segment utility. | held/unavailable | Vertical crop, subtitles, and low-resolution handling. |
| `yt-sample-subtitle-edited-01` | `knowledge/sources/videos/youtube-hwradk0bero.md` | subtitle-heavy or edited clip | Tests edited/subtitle-heavy coaching-style source. | Needs metadata classification first; cuts may limit timing segments. | held/unavailable | Subtitle obstruction, edited timing, and coaching-claim boundaries. |

## Raw Media And Local State Status

| Item | Committed? | Notes |
|---|---|---|
| raw video | no | No sample media was downloaded or committed. |
| downloaded clips | no | No clip files were created. |
| frames | no | No frames were extracted. |
| screenshots | no | No screenshots were created. |
| GIFs | no | No GIFs were created. |
| contact sheets | no | No contact sheets were created. |
| image dumps | no | No image dumps were created. |
| browser cache | no | Browser review was not used. |
| captions | no | Caption files were not requested or stored. |
| full transcripts | no | Transcript files were not requested or stored. |
| raw Hermes output | no | Hermes was not used for this smoke. |
| raw `video_analyze` output | no | `video_analyze` was not used or tested. |
| raw yt-dlp output | no | `yt-dlp` was unavailable and no output was committed. |
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
| Manual review used | yes | Existing repo surfaces, maintainer sample notes, source artifact shape, and report boundaries were reviewed manually. Direct video content was not reviewed. |
| Maintainer-local Hermes used | no | Hermes availability was not used for video review; no Hermes prompt or raw output was committed. |
| `video_analyze` used | no | Not tested and not required. |
| Vision analysis used | no | No local frames or screenshots were available because `yt-dlp` was unavailable. |
| yt-dlp | unavailable | The `yt-dlp` command was not available; no installation was attempted. |
| External asset fetch | no | No external visual asset scrape, download, or cache was performed. |
| Tool limitations | direct video-content review held | The smoke records source metadata and intended taxonomy coverage only. |
| Unavailable tools | `yt-dlp`; verified `video_analyze` path not used | Missing `yt-dlp` caused sample-content review to hold. |
| Hold reasons | safe video-content review unavailable | Do not fabricate observations or promote maintainer notes into facts. |

## yt-dlp / Scratch Handling

The policy-defined scratch/cache root from
`workflows/media-scratch-cache-policy.md` was used only to create an empty
per-run directory for the smoke. No repo-local scratch, download, cache, `.dist`,
frame-current, normalization, `data/normalized`, or `data/exports` path was
used for media.

`yt-dlp`, if available, would have been used only for maintainer-local review
of the five maintainer-selected sample URLs. It was unavailable, so no
download occurred. No yt-dlp logs, metadata JSON, thumbnails,
subtitles/captions, cache, or raw output were committed.

Cleanup status: the empty per-run scratch directory was deleted before commit.
Retained repo-external cache reason: none. Retained local cache is not
canonical evidence.

## Source And Reference Policy

Direct sample URLs are stored only in metadata-only source artifacts under
`knowledge/sources/videos/`. This executed report uses repo source paths and
does not include direct video URLs.

| Sample id | Source ref | Non-fetching reference status | Source freshness limitation |
|---|---|---|---|
| `yt-sample-gameplay-only-01` | `knowledge/sources/videos/youtube-paa8pnlequa.md` | true | Maintainer-provided context only; video content not reviewed. |
| `yt-sample-commentary-01` | `knowledge/sources/videos/youtube-6vmm2sdtoak.md` | true | Maintainer-provided context only; video content not reviewed. |
| `yt-sample-overlay-01` | `knowledge/sources/videos/youtube-ztqbhcrtsnc.md` | true | Maintainer-provided context only; video content not reviewed. |
| `yt-sample-vertical-01` | `knowledge/sources/videos/youtube-shorts-aylextw2jic.md` | true | Maintainer-provided context only; video content not reviewed. |
| `yt-sample-subtitle-edited-01` | `knowledge/sources/videos/youtube-hwradk0bero.md` | true | Maintainer-provided context only; video content not reviewed. |

Copyright/storage boundary: raw media and full transcripts are excluded from
repo artifacts. Current-fact authority boundary: exact current facts require
current-fact authority; `official_raw` remains authority.

## Video Taxonomy Classification

The rows below are intended taxonomy classifications from maintainer-selected
sample notes and existing #135 fixture coverage. They are not verified visual
observations.

| Sample id | video_type | unknown_or_mixed handling | taxonomy_update_needed | Related taxonomy fixture | Relationship to observation schema |
|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | `[gameplay_only]` | Not used unless future review shows mixed layout. | false | `gameplay-only` | Metadata layer; do not replace `contracts/video-observation.schema.json`. |
| `yt-sample-commentary-01` | `[commentary_only, coaching_review]` | May become `unknown_or_mixed` if gameplay and commentary are mixed unpredictably. | false | `commentary-only` | Metadata layer; commentary claims map to transcript segments only when paraphrased and time-bound. |
| `yt-sample-overlay-01` | `[livestream_layout, webcam_overlay, gameplay_with_commentary]` | Use `unknown_or_mixed` if overlay or edits prevent safe classification. | false | `livestream-layout-webcam-overlay` | Metadata layer before timestamped observations. |
| `yt-sample-vertical-01` | `[vertical_short, social_short]` | Use `unknown_or_mixed` if crop/subtitles obscure source context. | false | `vertical-short` | Fixture-only mapping before any segment work. |
| `yt-sample-subtitle-edited-01` | `[subtitle_overlay, gameplay_with_commentary, coaching_review, clip_compilation]` | Candidate `unknown_or_mixed` if edited clips or subtitles make the source unsafe to classify. | false | `subtitle-overlay`, `clip-compilation` | Metadata layer before timing-sensitive observation. |

## Visual Layout

Because video-content review was unavailable, layout fields are recorded as
unknown or unverified expected values. Future review must replace these with
direct observations before creating observation artifacts.

| Sample id | gameplay visibility | HUD visibility | input display visibility | damage label visibility | subtitles | webcam / wipe overlay | overlay obstruction | vertical crop | multi-match compilation | replay speed uncertainty | compression / resolution limitation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | unknown, expected full | unknown | unknown | unknown | unknown | unknown, expected none | unknown | unknown, expected none | unknown | unknown | unknown |
| `yt-sample-commentary-01` | unknown, possibly none/intermittent | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown | unknown |
| `yt-sample-overlay-01` | unknown, expected partial | unknown | unknown | unknown | unknown | unknown, expected present | unknown, expected minor or major | unknown | unknown | unknown | unknown |
| `yt-sample-vertical-01` | unknown, expected partial | unknown, expected cropped | unknown | unknown | unknown, expected possible | unknown | unknown | unknown, expected major | unknown | unknown | unknown |
| `yt-sample-subtitle-edited-01` | unknown, expected intermittent or partial | unknown | unknown | unknown | unknown, expected present | unknown | unknown, expected possible | unknown | unknown, expected possible | unknown | unknown |

## Audio And Commentary Context

| Sample id | audio type | commentary claims are source-local | commentary visible/evidence boundary | transcript status | no raw transcript confirmation |
|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | unknown, expected game_audio_only | true | No commentary claim recorded. | none requested | yes |
| `yt-sample-commentary-01` | unknown, expected commentary_only or gameplay_plus_commentary | true | Any future coaching claims remain source-local review input. | none requested | yes |
| `yt-sample-overlay-01` | unknown, expected gameplay_plus_commentary or mixed_voice_chat | true | Any playstyle claims remain source-local review input. | none requested | yes |
| `yt-sample-vertical-01` | unknown | true | Any technique claims remain source-local review input. | none requested | yes |
| `yt-sample-subtitle-edited-01` | unknown, expected gameplay_plus_commentary | true | Any ground-game coaching claims remain source-local review input. | none requested | yes |

## Analysis Capability

Because direct content review was held, candidate analysis dimensions are
`unknown` or `not_safe`. `exact_current_fact` is always `forbidden`.

| Sample id | candidate_move_identification | hit_block_whiff_candidate_labeling | timing_frame_window_observation | matchup_strategy_summary | input_hud_observation | exact_current_fact |
|---|---|---|---|---|---|---|
| `yt-sample-gameplay-only-01` | unknown | unknown | not_safe | unknown | unknown | forbidden |
| `yt-sample-commentary-01` | not_safe | not_safe | not_safe | unknown | not_safe | forbidden |
| `yt-sample-overlay-01` | unknown | unknown | not_safe | unknown | unknown | forbidden |
| `yt-sample-vertical-01` | unknown | unknown | not_safe | unknown | unknown | forbidden |
| `yt-sample-subtitle-edited-01` | unknown | unknown | not_safe | unknown | unknown | forbidden |

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

- No direct video-content observations were recorded.
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
- `official_raw` not overridden.
- Matchup/coaching conclusion not treated as final authority.
- Commentary claims not treated as current-system authority.
- External visual references were not used and would not override
  `official_raw`.

## Gap / Failure Findings

| Category | Finding |
|---|---|
| `unknown_or_mixed_source_format` | Video content could not be reviewed, so intended taxonomy classifications remain unverified. |
| `mixed_source_context` | Commentary, overlay, vertical, and edited samples may mix gameplay, source-local claims, and layouts; future review should preserve multi-label taxonomy. |
| `commentary_claims_not_visible` | Commentary and coaching claims cannot be evaluated without content review and must remain source-local. |
| `overlay_blocks_important_area` | Overlay sample is the intended future test, but obstruction was not directly observed in this run. |
| `subtitles_cover_input_or_hud` | Subtitle-heavy sample is the intended future test, but obstruction was not directly observed in this run. |
| `vertical_crop_removes_hud` | Vertical short is the intended future test, but crop was not directly observed in this run. |
| `compilation_cuts_destroy_timing` | Subtitle/edited sample may expose this gap, but cuts were not directly observed in this run. |
| `replay_speed_unknown` | Playback speed and source fps are unknown for all samples because content review was held. |
| `low_resolution` | Unknown for all samples. |
| `compression_artifacts` | Unknown for all samples. |
| `ambiguous_character_or_move` | Candidate moves and characters were not observed. |
| Tool availability gap | `yt-dlp` was unavailable, and no substitute live analysis path was used. |

## Follow-Up Candidates

| Candidate | Value | Mapping |
|---|---|---|
| taxonomy update candidate | false | No new taxonomy change is justified without direct sample review. |
| fixture candidate | false | No fixture should be added from unreviewed video content. |
| validator candidate | false | No validator change is needed in #137. |
| policy candidate | false | No #140 policy change is made here; #140 may later document unavailable-tool reporting if desired. |
| later issue candidate | #137 follow-up review, #140 if tool/cache policy wording is needed, #141 only after reviewed observations exist | Do not start #138-#141 in this PR. |
| unsupported/hold | true | Hold direct sample observations until a safe local review tool is available. |

Per-sample follow-up:

- `yt-sample-gameplay-only-01`: rerun as the baseline gameplay-only smoke when
  safe local media review is available.
- `yt-sample-commentary-01`: use to test commentary-only/coaching-source
  boundaries without raw transcripts.
- `yt-sample-overlay-01`: use to test overlay obstruction, HUD visibility, and
  livestream/webcam taxonomy.
- `yt-sample-vertical-01`: use to test vertical crop, subtitle, and
  low-resolution handling.
- `yt-sample-subtitle-edited-01`: use to test subtitle-heavy and edited clip
  timing boundaries.

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
| Scratch cleanup status | done; the empty policy-defined per-run scratch directory was deleted before commit |
| Retained repo-external cache reason | none |
| Git diff/status confirmation | to be recorded in the PR after validation |
| Validator commands | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-artifacts.ps1`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-learning-report-template.ps1`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-observation-taxonomy-fixtures.ps1`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1`; `git diff --check`; `git diff --check origin/main...HEAD` |
| Raw-media/local-state check | to be recorded in the PR after validation |
| No raw media / transcript / local state committed confirmation | no raw media, transcripts, raw tool output, local state, cookies, credentials, secrets, or external binary assets were added |

Final confirmation:

- No raw media committed.
- No transcript committed.
- No local state committed.
- No historical smoke reports were rewritten.
- No existing video observation artifacts were rewritten.
- No generated outputs, `.dist`, frame-current assets, normalization assets,
  `data/normalized`, or `data/exports` were intentionally changed.
