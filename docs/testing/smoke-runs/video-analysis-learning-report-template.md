# Video Analysis Learning Report Template

TEMPLATE ONLY: this file is not an executed report and is not a historical
smoke report.

Use this template for future maintainer-local v2.4 video-analysis learning
reports after the run is complete and the output has been sanitized. Executed
learning reports should use this naming convention:

`docs/testing/smoke-runs/video-analysis-learning-report-YYYYMMDD-<slug>.md`

Report types:

- Template: this reusable form. It contains placeholders and boundary rules.
- Executed learning report: a sanitized report from a scoped maintainer-local
  video-learning run, named with the convention above.
- Historical smoke report: an existing report created before this template.
  Historical smoke reports are not rewritten by #136.

## Existing Video Smoke Report Audit

#136 audited existing video-related smoke reports before defining this
template. The audit used these existing repo reports as examples:

- `docs/testing/smoke-runs/2026-05-03-video-observation-youtube-shorts-sycyvw6h8wi.md`
- `docs/testing/smoke-runs/2026-05-04-jp-combo-damage-oracle-fixture.md`
- `docs/testing/smoke-runs/2026-05-04-jp-combo-damage-oracle-coverage.md`
- `docs/testing/smoke-runs/hermes-bridge-smoke-gap-report.md`

Preserved fields and conventions:

- date, issue, report type, source or source reference, selected scope, and
  maintainer-local method summary
- tool availability and limitation notes, including unavailable or deferred
  tools
- raw media, transcript, local state, and external asset exclusion confirmation
- observation boundaries, `official_raw` boundary, cleanup status, findings,
  and follow-up candidates

Generalized fields and conventions:

- source details become a non-fetching source-reference policy rather than a
  live retrieval instruction
- tooling tables become a generic tool availability section that can record
  manual review, Hermes, `video_analyze`, vision analysis, and holds without
  requiring any tool to run
- video-specific smoke findings become taxonomy, visual layout, audio context,
  capability, gap/failure, and follow-up candidate fields aligned with
  `tests/fixtures/video-observation-taxonomy/`
- repo boundary checks become a common cleanup and verification section for
  future executed learning reports

Deprecated or not carried forward:

- live source URLs in executed report metadata are not required by this
  template; use repo source records or non-fetching placeholders
- raw command transcripts, raw Hermes output, raw `video_analyze` output,
  full captions, and full transcripts are not report content
- source-local commentary, observed damage labels, training UI labels, and
  video-derived move observations are not accepted current facts
- report shapes that imply canonical Hermes/video output are not carried
  forward

## Report Metadata

| Field | Value |
|---|---|
| Report id | `<video-analysis-learning-report-YYYYMMDD-slug>` |
| Date | `<YYYY-MM-DD>` |
| Related issue | `<issue number>` |
| Report type | `sanitized_video_analysis_learning_report` |
| Maintainer-local only status | `yes` |
| Template/executed status | `executed_learning_report` |
| Source reference type | `existing_repo_source` / `placeholder` / `none` |
| Source reference | `<repo source path, placeholder id, or none>` |
| Non-fetching/source policy | `non_fetching_reference: true; no external fetch in this report` |

## Raw Media And Local State Status

Confirm that none of these are committed in the executed learning report PR:

| Item | Committed? | Notes |
|---|---|---|
| raw video | no | `<confirmation>` |
| frames | no | `<confirmation>` |
| screenshots | no | `<confirmation>` |
| GIFs | no | `<confirmation>` |
| contact sheets | no | `<confirmation>` |
| browser cache | no | `<confirmation>` |
| full transcripts | no | `<confirmation>` |
| raw Hermes output | no | `<confirmation>` |
| raw `video_analyze` output | no | `<confirmation>` |
| local Hermes sessions | no | `<confirmation>` |
| memory | no | `<confirmation>` |
| local skills | no | `<confirmation>` |
| Curator output | no | `<confirmation>` |
| logs | no | `<confirmation>` |
| caches | no | `<confirmation>` |
| credentials | no | `<confirmation>` |
| secrets | no | `<confirmation>` |

## Tool Availability

| Tool / Capability | Value | Notes |
|---|---|---|
| Manual review used | `yes` / `no` / `unknown` | `<notes>` |
| Hermes used | `yes` / `no` / `unknown` | `<notes>` |
| `video_analyze` used | `yes` / `no` | `<notes>` |
| Vision analysis used | `yes` / `no` / `unknown` | `<notes>` |
| External asset fetch | `no` | `<confirmation>` |
| Tool limitations | `<limitations>` | `<notes>` |
| Unavailable tools | `<tools or none>` | `<notes>` |
| Hold reasons | `<reasons or none>` | `<notes>` |

This template does not require live Hermes, live video analysis, or
`video_analyze`.

## Source And Reference Policy

| Field | Value |
|---|---|
| Source ref | `<non-fetching source ref or none>` |
| Existing repo source ref | `<knowledge/sources/videos/<source>.md or none>` |
| Non-fetching reference status | `true` |
| No external fetch confirmation | `yes` |
| Copyright/storage boundary | raw media and full transcripts are excluded from repo artifacts |
| Source freshness limitations | `<limitations or unknown>` |
| Current-fact authority boundary | exact current facts require current-fact authority; `official_raw` remains authority |

## Video Taxonomy Classification

Align this section with `tests/fixtures/video-observation-taxonomy/`.

| Field | Value |
|---|---|
| video_type | `[<taxonomy labels>]` |
| unknown_or_mixed handling | `<why unknown_or_mixed is used or not used>` |
| taxonomy_update_needed | `true` / `false` |
| Related taxonomy fixture | `<fixture id or gap>` |
| Relationship to observation schema | metadata layer; this report does not replace `contracts/video-observation.schema.json` |

## Visual Layout

| Field | Value |
|---|---|
| gameplay visibility | `full` / `partial` / `intermittent` / `none` / `unknown` |
| HUD visibility | `full` / `partial` / `blocked` / `cropped` / `none` / `unknown` |
| input display visibility | `visible` / `partial` / `blocked` / `not_present` / `unknown` |
| damage label visibility | `visible` / `partial` / `blocked` / `not_present` / `unknown` |
| subtitles | `none` / `present_non_obstructing` / `present_obstructing` / `unknown` |
| webcam / wipe overlay | `none` / `present_non_obstructing` / `present_obstructing` / `unknown` |
| overlay obstruction | `none` / `minor` / `major` / `critical` / `unknown` |
| vertical crop | `none` / `minor` / `major` / `critical` / `unknown` |
| multi-match compilation | `true` / `false` / `unknown` |
| replay speed uncertainty | `none` / `possible` / `likely` / `unknown` |
| compression / resolution limitation | `none` / `minor` / `major` / `critical` / `unknown` |

## Audio And Commentary Context

| Field | Value |
|---|---|
| audio type | `no_audio` / `game_audio_only` / `commentary_only` / `gameplay_plus_commentary` / `mixed_voice_chat` / `music_ambient` / `unknown` |
| commentary claims are source-local | `true` |
| commentary visible/evidence boundary | commentary may be paraphrased as source-local review input only |
| transcript status | `<none, unavailable, paraphrased only, or unknown>` |
| no raw transcript confirmation | `yes` |

## Analysis Capability

| Dimension | Rating | Notes |
|---|---|---|
| candidate_move_identification | `likely` / `limited` / `not_safe` / `unknown` | `<notes>` |
| hit_block_whiff_candidate_labeling | `likely` / `limited` / `not_safe` / `unknown` | `<notes>` |
| timing_frame_window_observation | `likely` / `limited` / `not_safe` / `unknown` | `<notes>` |
| matchup_strategy_summary | `likely` / `limited` / `not_safe` / `unknown` | `<notes>` |
| input_hud_observation | `likely` / `limited` / `not_safe` / `unknown` | `<notes>` |
| exact_current_fact | `forbidden` | exact_current_fact must always be forbidden from video alone |

## Unsafe Inferences

Record `unsafe_inferences` categories aligned with
`tests/fixtures/video-observation-taxonomy/`.

Required baseline categories for executed reports:

- `exact_current_fact_from_video`
- `official_raw_override`

Optional categories when applicable:

- `exact_frame_data_from_video`
- `raw_tool_output_promotion`
- `training_ui_damage_label_as_current_fact`
- `commentary_claim_as_current_fact`
- `external_visual_atlas_as_current_fact`

These are unsafe inferences to reject, hold, or route to reviewed authority
checks. They are not conclusions accepted by the report.

## Observed-Safe Notes

Use paraphrased, safe observations only.

- Observations are review input.
- Observed damage labels are review/eval context only.
- Training UI observations are not current-system authority by default.
- Do not include raw transcript text or raw tool output.

## Not-Inferred Notes

- Exact current facts not inferred.
- Exact startup/active/recovery not inferred.
- Exact hit/block advantage not inferred.
- `official_raw` not overridden.
- Matchup/coaching conclusion not treated as final authority.

## Gap / Failure Findings

Record applicable categories and concise notes:

- `overlay_blocks_important_area`: overlay blocks important area
- `subtitles_cover_input_or_hud`: subtitles cover input/HUD
- `vertical_crop_removes_hud`: vertical crop removes HUD
- `compilation_cuts_destroy_timing`: compilation cuts destroy timing
- `replay_speed_unknown`: replay speed unknown
- `commentary_claims_not_visible`: commentary claims not visible
- `low_resolution`: low resolution
- `compression_artifacts`: compression artifacts
- `ambiguous_character_or_move`: ambiguous character/move
- `mixed_source_context`: mixed source/context
- `unknown_or_mixed_source_format`: unknown/mixed source format

## Follow-Up Candidates

| Candidate | Value | Mapping |
|---|---|---|
| taxonomy update candidate | `true` / `false` | #135 or later scoped taxonomy issue |
| fixture candidate | `true` / `false` | #135 taxonomy fixture shape or later fixture issue |
| validator candidate | `true` / `false` | #136 validator follow-up or later scoped validator issue |
| policy candidate | `true` / `false` | #140 media scratch/cache policy extension |
| later issue candidate | `<issue or none>` | #137, #140, #141, or later scoped issue |
| unsupported/hold | `<reason or none>` | hold when evidence is unsafe or unavailable |

Notes:

- Map first executed learning smoke findings to #137 when relevant.
- Map binary/cache policy gaps to #140.
- Map move-recognition or move-frequency evaluation gaps to #141.

## Authority Boundaries

- Video observations are observation/review input only.
- Hermes/video outputs are draft input.
- External visual atlas sources are not current-fact authority.
- `official_raw` remains current-fact authority.
- Exact current facts require current-fact authority.
- No public `sf6-agent` behavior change.

## Cleanup And Verification

| Field | Value |
|---|---|
| Scratch cleanup status | `<done, not used, retained outside repo, or hold>` |
| Retained repo-external cache reason | `<reason or none>` |
| Git diff/status confirmation | `<confirmation>` |
| Validator commands | `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-video-learning-report-template.ps1`; `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1`; `git diff --check`; `git diff --check origin/main...HEAD` |
| No raw media / transcript / local state committed confirmation | `<confirmation>` |

Final confirmation for executed reports:

- No raw media committed.
- No transcript committed.
- No local state committed.
- Historical smoke reports are not rewritten.
