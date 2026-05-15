# Video Link Gameplay-Only Source E2E: video-link-gameplay-only-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #161 |
| Parent issues | #155 / #158 |
| Date | 2026-05-16 |
| Sample ID | `video-link-gameplay-only-01` |
| Source URL | `https://www.youtube.com/watch?v=PaA8PNLeQUA` |
| Input family | YouTube/video link |
| Declared format | gameplay-only |
| Raw media used? | yes, repo-external scratch only |
| Raw media committed? | no |
| Captions/transcripts committed? | no |
| Terminal state | sanitized report + sanitized observation artifact + review-only hold |

## Loaded Repo Context

| Artifact | Type | Why loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `AGENTS.md` | repo guidance | Defines canonical surfaces, current-fact rules, generated-surface boundaries, and GitHub workflow expectations. | Artifact placement and authority boundaries. | Source-specific observation results. |
| `workflows/ingest-video.md` | workflow | Canonical video-ingest procedure and observation shape. | Direct video-link review, observation payload shape, and source/report separation. | Accepted strategy knowledge or exact current facts. |
| `workflows/media-scratch-cache-policy.md` | workflow | Scratch/cache and forbidden artifact policy for media work. | Repo-external scratch, cleanup, and raw-media boundaries. | Permission to commit media, frames, captions, or local paths. |
| `workflows/review-claims.md` | workflow | Terminal routing for claim/review decisions. | Whether to create claims or leave observations held. | Automatic curated promotion from video observations. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-20260514.md` | calibration report | Prior raw-video report with media boundary and terminal-state examples. | How to record sanitized visual observations and held exact facts. | Current-fact authority or #161 observations. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-command-prompt-normalization-20260514.md` | calibration report | Review-only move/prompt boundary example. | Avoiding exact move identity from visual/prompt hints. | #161 source conclusions. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-frame-input-alignment-20260515.md` | calibration report | 60f game-frame and exact-frame boundary example. | Avoiding exact timing claims from sparse samples. | Exact frame facts for #161. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-damage-scaling-attribution-20260515.md` | calibration report | Review-only damage/scaling attribution boundary. | Avoiding damage/scaling authority from video labels. | Current damage/scaling facts for #161. |
| `docs/testing/video-analysis-calibration/external-visual-atlas-acquisition-20260515.md` | calibration report | External visual reference acquisition boundary. | Keeping visual references review-only if ever used later. | Move identity or current-fact authority. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-visual-reference-matching-20260515.md` | calibration report | Visual matching and generalization boundary. | Avoiding all-move or move-frequency overclaiming from one source. | #161 move recognition or analytics readiness. |
| `evals/questions/sf6-system-mechanics-math-reasoning.yaml` | eval fixture | Authority-boundary fixture for insufficient evidence and overgeneralization. | Safe answer behavior for sparse visual evidence. | New source observations or current facts. |
| `knowledge/sources/videos/youtube-paa8pnlequa.md` | source metadata | Existing metadata-only source artifact for this URL. | Source identity and prior review boundary. | Content-level #161 terminal state until this PR. |
| `knowledge/evidence/video-observations/` | observation surface | Existing observation artifact style. | Shape and wording for sanitized observations. | Accepted curated knowledge. |
| `knowledge/review/unresolved/` | review surface | Existing review note style. | Terminal routing and held-observation wording. | Public answer authority. |

## Source Access And Scratch Handling

| Field | Result |
|---|---|
| Metadata access | yes, public no-cookie `yt-dlp` metadata access |
| Video content access | yes, temporary repo-external download |
| Video inspection | yes, sparse visual sampling and contact-sheet review |
| Audio/caption inspection | no caption/subtitle track was available; direct audio was not used for knowledge extraction |
| Authentication/cookies/browser profile | not used |
| Scratch location recorded in repo | no |
| Temporary media cleanup | completed before commit |
| Raw media committed | no |
| Frames/screenshots/contact sheets committed | no |
| Raw tool output committed | no |

## Content Review Method

1. Confirmed the source URL through no-cookie `yt-dlp` metadata access.
2. Downloaded a temporary 720p video/audio merge into repo-external scratch.
3. Used `ffprobe` to confirm a WebM container, 1280x720 video, 60 fps source
   cadence, and approximately 493.981 seconds duration.
4. Checked caption availability with `yt-dlp --list-subs`; no uploaded/manual
   subtitles or automatic captions were available.
5. Created temporary sparse contact sheets outside the repo at 15-second and
   30-second sampling intervals.
6. Manually reviewed sampled frames for format classification, visible actors,
   UI/layout, overlay/caption presence, and safe observation candidates.
7. Deleted all temporary media and visual derivatives before commit.

## Source Metadata Summary

| Field | Observed value |
|---|---|
| Video ID | `PaA8PNLeQUA` |
| Public title | `SF6 KAKERU JP vs KAZUNOKO C.Viper high-level gameplay` |
| Channel | SF6 High Level Replays |
| Uploaded date from metadata | 2026-05-10 |
| Duration | approximately 8:14 |
| Live status | not live |
| Availability | public |
| Age limit | 0 |
| Captions/subtitles | none reported |

## Gameplay-Only Format Confirmation

The source is classified as gameplay-only for this source-unit PR.

Evidence:

- standard SF6 match HUD is visible throughout sampled gameplay windows;
- sampled frames show replay-style JP vs C.Viper gameplay;
- no face-cam, commentary transcript, subtitle overlay, or instructional
  chapter structure was observed in the sampled gameplay windows;
- channel call-to-action/end-card material appears near the end and is separated
  from gameplay evidence;
- no caption/subtitle track was available.

Limitations:

- sparse sampling is enough for source-format confirmation, not for full move
  recognition or move-frequency analytics;
- exact player rank/status in the title remains source-local context;
- no audio transcription was used.

## Sanitized Observation Summary

| Time | Observation | Confidence | Boundary |
|---|---|---|---|
| 00:00-00:30 | Standard HUD gameplay with source-local JP vs C.Viper actor context. | high | Actor identity is review input, not roster/current-fact authority. |
| 00:30-02:30 | JP-style purple effects and C.Viper-style movement/contact candidates appear in sampled windows. | medium | Broad visual features only; no exact move identity. |
| 02:30-04:30 | High-effect and cinematic/super-like moments appear in sampled windows. | medium | Exact action source and timing unresolved. |
| 04:30-06:30 | Continued match gameplay with neutral resets, knockdown/pressure candidates, and normal HUD-only presentation. | medium | No matchup or strategy verdict. |
| 06:30-07:45 | Additional close-range and projectile/effect pressure candidates. | medium | No move-frequency or all-move readiness. |
| 07:45-08:14 | End-card/channel call-to-action region. | high | Not gameplay evidence. |

## Candidate Knowledge Units

No candidate claim artifact was created.

Reason:

- the source is gameplay-only with no captions/subtitles and no reviewed
  commentary claim;
- sparse visual observations support format and source E2E validation, but do
  not support stable curated knowledge;
- exact move, route, damage, frame, matchup, and frequency claims would be
  unsafe from this pass.

## Terminal Routing

| Unit | Terminal state | Reason |
|---|---|---|
| Source metadata | metadata-only source artifact updated | Existing source file now records #161 direct content review and gameplay-only boundary. |
| Gameplay observations | sanitized observation artifact created | Actual video content was reviewed safely through repo-external scratch. |
| Review note | review-only hold | Observations are useful review input but not accepted knowledge. |
| Candidate claims | not created | No safe atomic claim was extracted from gameplay-only sparse review. |
| Curated knowledge | not promoted | Video observations alone are insufficient. |
| Current-fact authority route | not_applicable | No exact current-fact-like value was extracted; exact facts were avoided. |
| Rejected unsafe | none | No candidate claim was extracted, so no rejection was fabricated. |

## Unsafe Inferences Avoided

- No exact move identity was accepted.
- No exact frame timing, startup, recovery, hitstop, or advantage was inferred.
- No exact damage/scaling facts were accepted.
- No player rank/status, matchup verdict, or route validity was accepted.
- No move-frequency analytics or all-character/all-move readiness was inferred.
- No current facts were inferred from video alone.

## Current-Fact Authority Boundary

Video observations are review input only. `official_raw` remains the exact
current-fact authority. This source does not override `official_raw`, frame
data exports, current roster surfaces, or generated frame-current runtime
assets.

## Raw Media / Local State Boundary

- Raw video used: yes, repo-external scratch only.
- Downloaded media committed: no.
- Audio committed: no.
- Captions/subtitles/transcripts committed: no.
- Frames/screenshots/contact sheets committed: no.
- Raw HTML committed: no.
- Raw tool output committed: no.
- Private paths committed: no.
- Credentials/cookies/secrets used or committed: no.

## Failure Analysis

This source E2E did not fail. The limiting factor is source type: gameplay-only
visual footage can validate video-link handling and produce sanitized
observations, but it does not by itself create accepted knowledge.

Remaining limits:

- no caption/commentary track to extract source-local claims;
- sparse samples cannot count moves or establish hit/action sequences;
- visual effects can obscure exact action source;
- title/HUD actor labels remain source-local context;
- any future move recognition or frequency work requires separate scoped
  validation with false-positive and false-negative measurement.

## Reusable Method / Next-Agent Checklist

For gameplay-only YouTube/video-link source-unit rows:

1. Load repo context and same-source metadata first.
2. Use public no-cookie metadata access.
3. Attempt direct content review in repo-external scratch where safe.
4. Check captions/subtitles, but do not commit them.
5. Use sparse visual sampling to classify format and record broad observations.
6. Create source metadata, sanitized observation, review note, and source-unit
   report only when content supports them.
7. Do not create candidate claims from sparse gameplay-only footage unless a
   reviewable atomic claim is actually supported.
8. Delete media, frames, contact sheets, and any visual derivatives before
   commit.
9. Keep exact move/frame/damage/current-fact/matchup/frequency claims out of the
   source-unit terminal state.

## Follow-Up Routing

| Follow-up | Routing |
|---|---|
| #162 gameplay-commentary video link | Still open; should exercise commentary/caption or audio/video claim extraction separately. |
| #155 / #158 parent tracking | Remain open; #161 covers only one gameplay-only video-link row. |
| Future move-recognition or move-frequency work | Not implemented here; would require separate scoped validation and broader coverage. |

## Cleanup And Validation

| Check | Result |
|---|---|
| Raw media used? | yes, repo-external scratch only |
| Scratch cleanup | completed before commit |
| Raw media committed? | no |
| Frames/screenshots/contact sheets committed? | no |
| Captions/transcripts committed? | no |
| Raw tool output committed? | no |
| Private paths committed? | no |
| Validators | pending in PR validation section |
