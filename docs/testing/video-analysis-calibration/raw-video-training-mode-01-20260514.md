# Raw Local Video Analysis Calibration: raw-video-training-mode-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #170 |
| Parent issues | #155, #158 |
| Date | 2026-05-14 |
| Source sample id | `raw-video-training-mode-01` |
| Source family | maintainer-local raw video |
| Local source path committed? | no |
| Raw media committed? | no |
| Private path committed? | no |
| Terminal state | analysis-calibration PARTIAL + sanitized observation/report only + review-only hold |

## Source Access And Scratch Handling

| Field | Result |
|---|---|
| Local mapping available? | yes, through maintainer-provided out-of-band mapping only |
| Media metadata inspected? | yes, with `ffprobe` |
| Media metadata summary | MP4-family container, HEVC video, 1920x1080, about 37.93 seconds, 60 fps nominal, 2272 reported video frames, AAC stereo audio stream present |
| Scratch method | repo-external temporary frames, UI crops, and contact sheets |
| Scratch cleanup status | cleaned before commit |
| Private paths recorded? | no |
| Raw OCR output committed? | no OCR tool output was committed |
| Raw frames/contact sheets committed? | no |

The report stores only sanitized text. Temporary visual derivatives were used as
working material and deleted before commit.

## Analysis Targets

| Target | Attempted? | Notes |
|---|---:|---|
| Characters | yes | HUD labels and character visuals were inspected. |
| Control mode | yes | HUD control icons were inspected. |
| Combo/trial context | yes | Combo-trial UI, command list, success/complete states, and training HUD were inspected. |
| Move/action sequence | partial | Visible command prompts were inspected, but no canonical move names were accepted. |
| Hit sequence | partial | Hit and sequence phases were estimated from sampled frames. |
| Frame/timing | partial | Coarse frame ranges were recorded; exact frame timing was not inferred. |
| Damage/scaling | partial | Visible damage labels were inspected as calibration labels only. |
| Oracle comparison | yes | Prediction was compared against visible HUD/command-list/damage UI and maintainer-provided source context. |

## First-Pass Analysis

The first pass used sparse frame/contact-sheet inspection before targeted UI
crops. It intentionally separated visual prediction from the later answer-key
read.

| Field | Prediction | Confidence | Basis | Frame/timestamp evidence | Limitations |
|---|---|---:|---|---|---|
| Source context | Training/combo-trial style clip. | 0.85 | Visible command list, success state, training HUD. | 00:00-00:38. | Does not identify exact trial catalog entry without oracle. |
| Player character | JP. | 0.82 | HUD label and character visual. | 00:00 onward. | Visual label only; not roster authority. |
| Opponent/dummy character | Ryu. | 0.82 | HUD label and character visual. | 00:00 onward. | Visual label only; not roster authority. |
| Control mode | Likely Classic for both sides. | 0.62 | `C` icon visible in HUD after targeted inspection, not obvious in first contact-sheet pass. | 00:00 crop. | UI icon interpretation is source-local. |
| Combo/trial label | Advanced 5 / `上級 5`. | 0.78 | Left command-list UI. | 00:00 crop. | Treat as combo-trial oracle text, not current fact. |
| Move/action sequence | JP performs a guided special-heavy sequence with projectile/portal-like effects and a cinematic end segment. | 0.35 | Contact sheet and sampled frames. | Approx. 00:04-00:34. | Exact move names, cancel points, and route validity are not reliable from sparse frames. |
| Hit sequence | Multi-hit sequence with launch/airborne and cinematic phases. | 0.45 | Hit sparks, dummy airborne states, UI counters. | Approx. 00:06-00:34. | Exact hit timing and hitstop boundaries are unresolved. |
| Damage/scaling | Final visible combo damage appears high and likely above 5000. | 0.45 | Top damage UI in later frames. | Approx. 00:28-00:34. | First pass could not reliably read all intermediate values. |

## Oracle / Answer Key

The oracle is sanitized text from visible combo-trial/training UI plus
maintainer-provided source context. It is a calibration oracle only, not
current-fact authority.

| Oracle field | Sanitized answer key |
|---|---|
| Source context | Raw local SF6 training/combo-trial recording. |
| Maintainer-provided context | JP combo-trial final challenge style recording. |
| Visible trial label | `上級 5` visible in the command-list UI. |
| Visible player character | JP. |
| Visible dummy/opponent character | Ryu. |
| Visible control mode | `C` icon visible for both sides, treated as source-local Classic-control UI evidence. |
| Visible command-prompt structure | Command list shows direction/button-icon prompts with strength labels and context notes such as Veehat-installed, jump, and Drive Parry contexts. |
| Oracle move names | Not available as canonical move names from the visible UI in this run. |
| Oracle move order | Not fully available as canonical move order; available only as sanitized command-prompt structure. |
| Visible damage labels | Sampled UI showed combo damage labels including 800, 2220, 3622, 4522, and final 5622. |
| Visible damage modifiers | Sampled UI showed per-hit percentage labels such as 100%, 70%, 17%, and 50% in the damage UI. |
| Hit count oracle | Partial only; sampled frames show hit-count UI during the sequence, but exact hit-by-hit count was not extracted reliably. |
| Frame/timing oracle | Not available beyond video fps and sampled frame/timestamp ranges. |
| Success/completion oracle | Success/complete UI is visible near the end of the clip. |

The visible command-prompt structure was not converted into canonical move IDs.
The prompt icons are useful for calibration, but they remain source-local UI
labels until a stronger OCR / manual answer-key / move-name mapping exists.

## Prediction Vs Oracle

| Field | Prediction | Oracle | Result | Error type | Notes |
|---|---|---|---|---|---|
| Source context | Training/combo-trial clip. | Training/combo-trial recording. | correct | none | Contact-sheet review was enough. |
| Player character | JP. | JP visible in HUD. | correct | none | Source-local visual label only. |
| Opponent/dummy character | Ryu. | Ryu visible in HUD. | correct | none | Source-local visual label only. |
| Control mode | Likely Classic. | `C` icon visible for both sides. | correct after targeted crop | first-pass visibility | Contact sheet alone was weaker; targeted HUD crop improved confidence. |
| Trial label | Advanced / final challenge style. | `上級 5` visible; maintainer described final JP combo trial style. | partial | label granularity | Visible label is strong; "final challenge" is maintainer context rather than directly inferred from UI alone. |
| Move/action sequence | Broad special-heavy JP sequence with cinematic end. | Command-prompt oracle exists, but canonical move names are unavailable. | partial | move-name ambiguity | Needs OCR/manual command-to-move mapping. |
| Hit sequence | Multi-hit launch/cinematic sequence. | Partial hit-count UI visible; exact hit-by-hit oracle not extracted. | partial | frame/hitstop ambiguity | Needs dense frame stepping and UI extraction. |
| Damage values | Final damage likely >5000. | Final visible combo damage 5622; intermediate sampled values 800, 2220, 3622, 4522. | partial | low first-pass numeric precision | Targeted damage UI crops corrected the final value. |
| Scaling/modifiers | Scaling appears to change across hits. | Sampled labels include 100%, 70%, 17%, and 50%. | partial | attribution ambiguity | No hit-by-hit move-to-modifier mapping. |
| Frame/timing | Coarse phase ranges only. | No exact frame oracle. | not_available | oracle unavailable | Exact startup/contact/recovery not inferred. |
| Input timing | Input history visible but not aligned. | Right-side input history visible. | partial | alignment ambiguity | Needs frame-by-frame input-history parser. |

## Damage And Scaling Analysis

| Timestamp | Observed label | Calibration interpretation |
|---|---|---|
| ~00:08 | `800 (100%)`, combo damage `800` | Early visible damage label; source-local UI oracle only. |
| ~00:20 | `420 (70%)`, combo damage `2220` | Mid-sequence damage label; exact move attribution unresolved. |
| ~00:24 | `136 (17%)`, combo damage `3622` | Low-percentage damage label during high-effects segment; scaling attribution unresolved. |
| ~00:28 | `100 (50%)`, combo damage `4522` | Later cinematic sequence damage label; not accepted damage authority. |
| ~00:32-00:34 | `1000 (50%)`, combo damage `5622` | Final sampled visible combo damage label. |

These values are calibration observations only. They are not accepted current
facts, not generated-answer evidence, and not an authoritative combo-damage
model. They can be used to design a future video-analysis oracle comparison
that checks whether predicted hit/damage/scaling extraction matches visible UI.

The Hameko combo-scaling source-derived model candidates from #160 are relevant
as a future reasoning surface, but this PR does not verify the numeric scaling
model against this raw clip.

## Frame And Timing Analysis

| Segment | Approx. time | Approx. normalized frame range | Interpretation | Confidence | Limitation |
|---|---|---:|---|---:|---|
| Setup / command-list context | 00:00-00:04 | 0-240 | Trial UI and actor labels visible. | 0.88 | Exact initial actionable frame unknown. |
| Opening sequence | 00:04-00:10 | 240-600 | JP begins sequence against Ryu dummy; hit effects appear. | 0.65 | Start/contact/recovery frames unresolved. |
| Airborne / mid-combo sequence | 00:10-00:20 | 600-1200 | Launch or airborne states and combo labels visible. | 0.62 | Hitstop and action boundaries unresolved. |
| High-effects / cinematic segment | 00:20-00:31 | 1200-1860 | Cinematic or super-like effects dominate the screen. | 0.58 | Visual occlusion prevents exact move/hit attribution. |
| Completion / post-attempt UI | 00:31-00:38 | 1860-2272 | Completion context, final damage label, and retry/menu state visible. | 0.72 | End-of-combo frame and final actionable state unresolved. |

Frame indexing uses `normalized_fps = 60`. Timing is approximate because the run
uses sparse sampled frames and does not perform full frame-by-frame stepping.
Exact startup, active, recovery, hit/block advantage, hitstop, and route validity
are unsafe to infer from this run.

## Failure Analysis

| Failure / uncertainty | Why it happened | Impact |
|---|---|---|
| Exact move names not extracted | The visible combo-trial UI primarily shows command icons and context labels, not canonical move names. | Cannot compare predicted move order to canonical move oracle. |
| First-pass damage precision was weak | Contact sheet scale was too small for reliable numeric reading. | Targeted damage UI crops were required to read final/intermediate labels. |
| Frame-level timing not established | Sparse frame sampling is insufficient for contact, hitstop, and recovery boundaries. | No frame-accurate action/hit timing claim can be made. |
| Input history not aligned to actions | Right-side input history is visible, but alignment to action/hit frames was not parsed. | Cannot validate input/action timing sequence. |
| Scaling attribution unresolved | Damage percentage labels are visible only at sampled moments and are not mapped to exact moves/hits. | No combo-scaling calculation proof. |
| Control mode needed targeted crop | The `C` HUD icon is visible but small in contact sheets. | Second-pass crop was required for confidence. |

## Improvement Applied In This PR

This PR adds a narrow `Raw Local Video Analysis Calibration` section to
`workflows/ingest-video.md`.

The improvement is driven by this #170 failure mode: the initial observation
artifact proved raw-local boundary handling, but did not require prediction,
oracle extraction, comparison, failure analysis, or a rerun/revised method.

The workflow addition now requires calibration runs to:

- separate first-pass prediction from oracle fields,
- store the oracle only as sanitized text,
- compare prediction vs oracle,
- record correct / partial / wrong / unknown / not-available outcomes,
- document failure causes,
- add improvements only from concrete source-execution failures,
- preserve the boundary that video-derived character, move, damage, timing, and
  scaling observations are calibration evidence only.

No validator change was added because the existing validators already enforce
the important repo boundary: no raw video, frames, transcripts, contact sheets,
private paths, or accepted current facts in review-only video artifacts.

## Second-Pass Or Revised Analysis

Second-pass analysis used targeted UI crops for:

- top HUD/control-mode icons,
- left command-list UI,
- top-center damage/combo-damage labels,
- right-side input history.

Second-pass improvements:

| Field | First pass | Second pass / revised method | Result |
|---|---|---|---|
| Control mode | likely Classic, lower confidence | visible `C` icons identified from HUD crop | confidence improved |
| Trial label | training/combo-trial context | `上級 5` visible from command-list crop | confidence improved |
| Damage | final damage only roughly high | sampled values 800, 2220, 3622, 4522, 5622 visible | numeric oracle improved |
| Command prompt | broad sequence only | command-list prompt structure recorded as sanitized oracle | still not canonical move names |
| Input history | visible but unparsed | cropped right-side input history confirms input stream exists | still not action-aligned |

Residual gaps:

- full frame-by-frame stepping is still required for hit/contact timing,
- OCR/manual command-list normalization is required for canonical move order,
- input-history parsing is required for input/action/hit alignment,
- damage/scaling attribution requires hit-by-hit mapping and a verified formula
  surface.

## Follow-Up Issue Map

PR #173 intentionally stops at `analysis-calibration PARTIAL`. The residual gaps
are mapped to executable follow-up issues so they do not remain as vague report
notes.

| Residual gap | Follow-up issue | Expected next execution |
|---|---|---|
| #171 combo-scaling candidates were not loaded into the #170 damage/scaling calibration. | #174 | Compare the #173 visible damage/scaling oracle against Hameko source-derived combo-scaling model candidates. |
| Combo-trial command prompts were visible but not normalized to canonical move candidates. | #175 | Extract sanitized command-list prompt rows and map them to canonical move-name candidates where possible. |
| Coarse frame ranges were not aligned with right-side input history, action phases, hit events, or damage-label changes. | #176 | Run bounded frame stepping and input-history alignment with explicit uncertainty. |
| Visible damage/scaling labels were sampled but not attributed hit-by-hit or move-by-move. | #177 | Map each visible damage/scaling label to hit/action candidates or mark it unknown. |
| Move identification lacks a repo-external visual reference atlas. | #178 | Build a gated Scrapling-aligned external visual atlas acquisition path that commits metadata/report only. |
| JP move/action matching was not attempted against visual references. | #179 | Compare raw-video segments against repo-external JP visual references and record candidate matches. |
| Merged repo knowledge did not automatically affect later video analysis. | #180 | Add a context-loading checklist so source-derived mechanics candidates, prior calibration reports, and other reviewed artifacts are loaded before analysis. |

#171 / PR #171 is not the failure here. The failure is that #170 did not
explicitly load the merged source-derived combo-scaling model before attempting
damage/scaling calibration. That context-loading gap is tracked in #180, and
the concrete damage/scaling follow-up is tracked in #174.

## Terminal State

| State | Result | Reason |
|---|---|---|
| analysis-calibration PASS / PARTIAL / FAIL | PARTIAL | Characters, control mode, context, and several visible damage labels were calibrated; exact move order, frame timing, hit sequence, and scaling attribution remain unresolved. |
| sanitized observation/report only | yes | Raw-local observation artifact and calibration report were created. |
| review-only hold | yes | Current-fact-like labels, visual actor labels, and sequence interpretation remain held. |
| candidate claim | no | No safe claim beyond calibration evidence was created. |
| accepted curated knowledge | no | This source is a single raw local clip, not a stable public knowledge source. |
| current-fact authority | no | No exact current fact was accepted or routed as authority. |

## Authority Boundaries

- Raw video observations are calibration evidence only.
- The sanitized answer key is an analysis oracle only, not public answer
  authority.
- Exact current facts are not inferred from this raw video.
- `official_raw` remains the current-fact authority.
- No public `sf6-agent` behavior changed.
- No generated references changed.
- Combo-trial labels, visible character names, input history, damage values, and
  scaling labels are not accepted gameplay facts in this PR.

## Cleanup And Validation

| Check | Result |
|---|---|
| Scratch cleanup | completed before commit |
| Raw media committed | no |
| Frames/screenshots/contact sheets committed | no |
| Audio committed | no |
| Captions/transcripts committed | no |
| Raw OCR/tool output committed | no |
| Private local path committed | no |
| Credentials/cookies/secrets committed | no |
| `validate-no-video-binary-assets.ps1` | `No video binary assets OK` |
| `validate-video-artifacts.ps1` | `Video artifacts OK` |
| `run-all.ps1` | `V2 validation suite OK` |
| `git diff --check` | PASS, no output |
| `git diff --check origin/main...HEAD` | PASS, no output |
| raw/local-state scan | only existing approved Hermes docs/packs/workflows/test paths appeared |
| generated-surface residual diff check | no unintended residual diffs in generated references, `.dist`, frame-current assets, normalization assets, `data/raw`, `data/normalized`, or `data/exports` |
