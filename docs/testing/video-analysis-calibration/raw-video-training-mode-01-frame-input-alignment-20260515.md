# Raw Video Frame/Input Alignment: raw-video-training-mode-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #176 |
| Parent issues | #155, #158, #170 |
| Related raw-video calibration | #170 / PR #173 |
| Related combo-scaling context follow-up | #174 / PR #182 |
| Related command prompt normalization | #175 / PR #184 |
| Related workflow fix | #180 / PR #181 |
| Date | 2026-05-15 |
| Source sample id | `raw-video-training-mode-01` |
| Raw media used? | yes, via maintainer-provided out-of-band local mapping only |
| Raw media committed? | no |
| Raw OCR committed? | no |
| Terminal state | frame/input alignment PARTIAL + review-only calibration evidence |

This follow-up uses the #175 sanitized command-prompt oracle as the primary
alignment target. It attempts bounded frame stepping, input-history alignment,
action-phase alignment, hit-event candidate alignment, and damage-label timing.
It does not create exact frame data, accepted move order, route validation,
hit-by-hit damage/scaling attribution, generated references, or public
`sf6-agent` behavior.

## Loaded Repo Context

This section implements the #180 `Pre-Analysis Repo Context Loading` gate before
frame/input alignment.

| Artifact path | Artifact type | Why it was loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-20260514.md` | calibration report | Provides the #173 first-pass prediction, sanitized oracle, metadata, and unresolved timing/damage gaps. | Source context, prior visible labels, and known failure modes. | Exact move order, frame-accurate timing, current damage authority, or route validity. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-combo-scaling-context-20260514.md` | calibration report | Provides the #174 comparison between visible labels and source-derived SF6 combo-scaling candidates. | Which damage/scaling fields need later hit/action attribution. | Accepted current facts, hit-by-hit scaling, or final combo calculation. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-command-prompt-normalization-20260514.md` | calibration report | Provides the #175 sanitized command-prompt rows and review-only JP move/system-action candidates. | Primary alignment targets and candidate row labels. | Accepted move identity, exact action execution, route validity, or timing authority. |
| `knowledge/evidence/video-observations/raw-video-training-mode-01.observations.md` | observation artifact | Provides sanitized source-local video observations. | Character/context boundaries and visible UI observation discipline. | Accepted gameplay facts or current-system authority. |
| `knowledge/review/unresolved/raw-video-training-mode-01.review.md` | review note | Provides current review-only terminal decisions and follow-up routing. | Scope, authority boundaries, and remaining issue map. | Accepted knowledge or public answer authority. |
| `knowledge/sources/videos/raw-video-training-mode-01.md` | sanitized source descriptor | Provides sample identity and local-source boundary. | Source identity, scratch policy, and private-path boundary. | Private path, raw media retention, or gameplay fact authority. |
| `ingest/frame_data/config/registry/jp.moves.yaml` | move registry / binding metadata | Used only to keep #175 candidate IDs visible during alignment. | Candidate labels for prompt-row references. | Proof that the observed action occurred at a specific frame. |
| `skills/sf6-agent/assets/frame-current/published/jp/official_raw.json` | derived frame-current runtime asset | Used only to cross-check #175 candidate labels. | Candidate label context for JP prompt rows. | New current-fact claims from this raw video. |

#175 prompt rows are calibration oracle input, not accepted move order. #173 and
#174 damage/scaling labels are calibration oracle input, not current
damage/scaling authority. Exact current facts must not be inferred from this
video. Hermes memory, session history, local skills, Curator output, logs, and
local state are non-canonical.

## Source Access And Scratch Handling

| Field | Result |
|---|---|
| Raw local mapping used? | yes, through maintainer-provided out-of-band mapping only |
| Private path recorded? | no |
| Frame stepping method | nominal 60 fps timeline with targeted 4 fps action/input sheets and 2 fps damage-label sheets in repo-external scratch |
| Sampling density | 0.25 second action/input samples; 0.5 second damage-label samples |
| Targeted crop method | full-frame sheets plus right-side input-history crop and top damage-label crop |
| OCR attempted? | no |
| Manual inspection used? | yes |
| Scratch cleanup status | completed before commit |
| Raw media committed? | no |
| Frames/screenshots/contact sheets committed? | no |
| Raw OCR/tool output committed? | no |

The report stores only sanitized observations and approximate frame/timestamp
ranges. It does not commit raw visual derivatives.

## Frame Indexing Method

| Field | Value |
|---|---|
| Source fps | about 59.95 fps from media metadata; nominal display cadence treated as 60 fps |
| Normalized fps | 60 |
| Reported total video frames | 2272 |
| Reported duration | about 37.93 seconds |
| Timestamp conversion | `approx_frame = round(timestamp_seconds * 60)` |
| Frame interval convention | approximate closed ranges for human-readable calibration tables, not exact half-open observation segments |
| Sampling tolerance | about +/-15 frames for 4 fps action/input sheets; about +/-30 frames for 2 fps damage-label sheets; larger during cinematic occlusion |
| VFR / encoding ambiguity | MP4-family container with nominal 60 fps; this report does not prove constant frame-perfect capture cadence |
| Exactness boundary | no startup, active, recovery, hitstop, hit advantage, cancel window, or route-validity frame data is claimed |

Frame ranges were chosen from sampled visual changes, input-history updates, and
visible damage-label changes. They are calibration windows for later analysis,
not current frame-data authority.

## Alignment Targets

| target_id | target_type | source | alignment goal | expected downstream use | authority boundary |
|---|---|---|---|---|---|
| `cmd-raw-jp-adv5-001` through `cmd-raw-jp-adv5-012` | command_prompt_row | #175 command-prompt oracle | Estimate when each prompt row appears to correspond to action/input windows. | Structured input for #177 attribution. | Review-only prompt oracle; not accepted move order. |
| `ih-early-command-cluster` | input_history_change | right-side input history crop | Bound the first visible command cluster and later scroll/update windows. | Confirm whether row candidates have nearby input-history support. | Sanitized observation only; raw input images not committed. |
| `phase-portal-setup` | action_phase | sampled frames | Bound early purple portal/setup phase. | Helps distinguish setup rows from direct strikes. | Visual phase candidate only. |
| `phase-drive-transition` | action_phase | sampled frames | Bound Drive Parry / Drive Rush style transition. | Supports row 6 timing review. | Review-only; not current system-action proof. |
| `phase-super-cinematic` | action_phase | sampled frames | Bound super/cinematic phase and final damage labels. | Gives #177 a coarse final sequence window. | No exact SA3/CA authority. |
| `damage-label-change-*` | damage_label_change | top damage-label crop | Bound visible damage/combo label changes. | #177 can use these as review-only label timing inputs. | Source-local labels only; no current damage authority. |

## Command Prompt Row Alignment

| prompt_row_id | sanitized_prompt | candidate_move_id_or_family | approx_start_frame | approx_end_frame | approx_timestamp_range | input_history_match | visible_action_phase | hit_event_candidate | damage_label_nearby | confidence | alignment_status | notes |
|---|---|---|---:|---:|---|---|---|---|---|---:|---|---|
| `cmd-raw-jp-adv5-001` | `214 + PP` | `jp_040_214pp_vihat_od_weak`; `jp_041_214pp_vihat_od_medium`; `jp_042_214pp_vihat_od_heavy` | 195 | 240 | 00:03.25-00:04.00 | partial: right-side history shows the first dense direction/punch cluster beginning near 3.25s | purple portal/setup begins | no direct hit isolated | first damage change follows near 4.00s | 0.58 | partial | Window likely covers OD Veehat/Departure setup, but variant and exact execution frame remain unresolved. |
| `cmd-raw-jp-adv5-002` | `HP` | `jp_005_5hp` | 240 | 270 | 00:04.00-00:04.50 | partial: punch input remains near the first cluster | close-range strike/contact window | yes, first clear contact candidate | `800 (100%)` and combo `800` appear by about 4.00-4.50s | 0.60 | partial | This is the strongest early row-to-hit candidate, but the contact sheet cannot prove exact HP contact frame. |
| `cmd-raw-jp-adv5-003` | `2MP` | `jp_009_2mp` | 270 | 315 | 00:04.50-00:05.25 | partial: down/punch-like entries visible but scrolling history is dense | low/grounded follow-up window | ambiguous | damage remains around `800`; no isolated new label change | 0.46 | ambiguous | The command prompt row is clear, but sampled visuals do not isolate crouching medium punch execution. |
| `cmd-raw-jp-adv5-004` | `214 + MP` while Veehat is set | `jp_043_214lpmp_vihat_akno` | 315 | 375 | 00:05.25-00:06.25 | partial: direction/punch cluster appears during portal effects | Veehat/Departure follow-up or portal interaction | yes, launch/portal candidate | damage still mostly held at `800`; no reliable isolated label change | 0.50 | partial | Setup-dependent row; prior portal state and exact follow-up behavior remain held. |
| `cmd-raw-jp-adv5-005` | `j.MP` | `jp_015_j_mp` | 375 | 435 | 00:06.25-00:07.25 | partial: input history changes, but jump-normal input is not isolated | airborne/transition window | ambiguous | no new damage label isolated | 0.42 | ambiguous | Jump context is visible in the prompt oracle, but sampled frames do not prove the air normal timing. |
| `cmd-raw-jp-adv5-006` | `66` during Drive Parry | `jp_068_parry_drive_rush` | 420 | 510 | 00:07.00-00:08.50 | partial: forward/dash-like history cannot be cleanly isolated from surrounding inputs | Drive Parry / Drive Rush style glow transition | no isolated hit; transition into follow-up | `800` persists | 0.52 | partial | Supports a review-only Parry Drive Rush timing window; exact action execution must remain for later frame/input analysis. |
| `cmd-raw-jp-adv5-007` | `HP` | `jp_005_5hp` | 450 | 510 | 00:07.50-00:08.50 | partial | close-range strike after Drive Rush-style transition | yes, possible follow-up contact | `800` persists; no isolated new label | 0.48 | partial | Overlaps row 6 transition; cannot prove exact order from sparse samples alone. |
| `cmd-raw-jp-adv5-008` | `236HP` | `jp_035_236hp_stribog` | 510 | 630 | 00:08.50-00:10.50 | partial: direction/punch cluster visible in the input-history crop | purple projectile/strike effect window | yes, repeated hit/effect candidates | no stable new damage label until later | 0.49 | partial | Candidate special/action window is plausible, but rows 8-10 visually overlap through effects. |
| `cmd-raw-jp-adv5-009` | `HP` | `jp_005_5hp` | 570 | 660 | 00:09.50-00:11.00 | partial | close-range follow-up among purple effect sequence | ambiguous | no isolated label change | 0.38 | ambiguous | The prompt row is preserved, but action phase is not separable from adjacent Stribog/Triglav effects. |
| `cmd-raw-jp-adv5-010` | `22PP` | `jp_030_22pp_triglav_od_weak`; `jp_031_22pp_triglav_od_medium`; `jp_032_22pp_triglav_od_heavy` | 630 | 900 | 00:10.50-00:15.00 | partial: down/down and punch-like clusters appear, but input history scrolls and occludes exact row mapping | repeated spike/portal/juggle effects | yes, multiple candidates | no reliable per-row label; combo remains near `800` in this sampled span | 0.45 | partial | OD Triglav family window is plausible, but variant and hit count are unresolved. |
| `cmd-raw-jp-adv5-011` | `236MP` | `jp_034_236mp_stribog` | 900 | 1170 | 00:15.00-00:19.50 | partial: later input-history clusters are visible but not row-clean | projectile/juggle continuation | yes, multiple candidates | labels transition through `600 (100%)`, `400 (80%)`, `420 (70%)`, combo `1400`, `1800`, `2220` near 18.5-19.5s | 0.43 | partial | This row may cover the late pre-super damage ramp, but hit/action attribution is #177 scope. |
| `cmd-raw-jp-adv5-012` | `236236K` | `jp_055_sa3_236236k`; `jp_056_ca_236236k` | 1425 | 1935 | 00:23.75-00:32.25 | partial: input history shows a settled super-input trail during cinematic, not an isolated activation frame | super/cinematic sequence | yes, multiple cinematic hit candidates | labels include `500 (50%)`, `100 (50%)`, and final `1000 (50%)`, ending at combo `5622` | 0.62 | partial | The cinematic window is clear, but SA3 vs CA and exact activation/hit frames remain unresolved. |

The alignment windows are intentionally broad. They provide #177 a structured
starting point, but they do not establish exact route order, frame data, or
damage attribution.

## Input-History Alignment

| input_history_event_id | approx_frame_range | approx_timestamp_range | sanitized observation | possible prompt rows | confidence | notes |
|---|---:|---|---|---|---:|---|
| `ih-idle-before-sequence` | 0-180 | 00:00.00-00:03.00 | Mostly neutral/right-hold history with no dense command cluster. | none | 0.70 | Useful as pre-sequence baseline only. |
| `ih-first-command-cluster` | 195-285 | 00:03.25-00:04.75 | Dense direction plus punch entries appear as the first action begins. | rows 1-2, possibly row 3 | 0.58 | Supports the start of the command sequence but does not isolate row boundaries. |
| `ih-portal-followup-cluster` | 300-390 | 00:05.00-00:06.50 | Direction/punch entries continue during purple portal/setup effects. | rows 3-5 | 0.46 | Input history is readable enough to show activity, not enough to prove exact row mapping. |
| `ih-drive-transition-cluster` | 405-540 | 00:06.75-00:09.00 | Input history continues through a Drive/green-glow transition and close-range follow-up. | rows 5-8 | 0.44 | The `66` row cannot be isolated cleanly from sparse samples. |
| `ih-mid-sequence-scroll` | 600-1170 | 00:10.00-00:19.50 | Repeated direction/punch clusters scroll while effects and hitstun obscure the actors. | rows 8-11 | 0.36 | Right-side history is visible, but exact scrolling overwrite prevents row-level alignment. |
| `ih-super-trail` | 1425-1935 | 00:23.75-00:32.25 | A settled input-history trail is visible through the cinematic, including double-quarter-circle-like and kick-like entries. | row 12 | 0.50 | Supports super input context, not exact activation frame or SA3/CA distinction. |

No raw input-history images or OCR outputs are committed. Input-history entries
are summarized only as sanitized observations.

## Action / Hit / Damage Label Alignment

| alignment_id | approx_frame_range | approx_timestamp_range | observed phase / label | related prompt rows | relation to #174 | status | notes |
|---|---:|---|---|---|---|---|---|
| `damage-change-001` | 240-270 | 00:04.00-00:04.50 | first visible damage label `800 (100%)`, combo `800` | rows 1-2 | Useful anchor for #174 `100%`; insufficient for scaling attribution without exact hit/action mapping. | partial | The first hit/contact candidate is nearby, but exact HP attribution is not proven. |
| `phase-early-hold` | 300-1080 | 00:05.00-00:18.00 | combo label frequently remains around `800` or resets visually while effects continue | rows 3-10 | Shows why #174 could not attribute labels from sparse samples alone. | ambiguous | UI label visibility and effect occlusion make hit count/order unclear. |
| `damage-change-002` | 1110-1170 | 00:18.50-00:19.50 | labels progress through `600 (100%)`, `400 (80%)`, `420 (70%)`, combo `1400`, `1800`, `2220` | row 11 candidate window, possibly earlier row spillover | Useful anchor for #174 `70%`, but exact hit unit is unresolved. | partial | This is a strong #177 target window. |
| `damage-change-003` | 1200-1410 | 00:20.00-00:23.50 | labels progress through `408 (51%)`, `126 (42%)`, `210 (42%)`, `272 (34%)`, `125 (25%)`, `136 (17%)`, combo `2628` to `3622` | rows 10-11 and transition to row 12 | Explains #174 `17%` unknown: multiple candidate modifiers/effects are in play. | partial | Requires move/hit index and possibly input/action alignment before attribution. |
| `phase-super-start` | 1425-1470 | 00:23.75-00:24.50 | super/cinematic visuals begin; damage labels held near `3622` | row 12 | Relevant to SA3/CA and minimum guarantee hypotheses. | partial | Activation frame and exact super type are not accepted. |
| `damage-change-004` | 1530-1665 | 00:25.50-00:27.75 | `500 (50%)`, combo `4122`; then `100 (50%)`, combo `4322`/`4422` | row 12 | Useful for #174 `50%` context, but not sufficient for hit-by-hit attribution. | partial | Cinematic occlusion makes individual hits hard to separate. |
| `damage-change-005` | 1800-1920 | 00:30.00-00:32.00 | `100 (50%)`, then final `1000 (50%)`, combo `5622`; completion follows | row 12 | Confirms final label window but not current damage authority. | partial | Best terminal damage-label window for #177. |
| `phase-complete` | 1920-2010 | 00:32.00-00:33.50 | completion overlay / post-combo return | none | Terminal state marker only. | aligned | Not a move/hit event. |

This section intentionally stops before hit-by-hit damage/scaling attribution.
#177 must decide which labels can be assigned to hit/action candidates and which
remain unknown.

## Prediction Vs Alignment Result

| Field | Previous prediction/oracle | #176 alignment result | Result | Error type | Notes |
|---|---|---|---|---|---|
| command-prompt rows exist | #175 recorded 12 sanitized rows | Rows are usable alignment targets. | correct | none | Row order is now tied to approximate windows where possible. |
| canonical move candidates | #175 produced review-only candidates | Candidate labels helped organize windows, but exact action execution is not proven. | partial | authority boundary | Candidate IDs remain review-only. |
| input-history visibility | #173 saw input history but did not align it | Input history is visible through most of the sequence, but scrolling/occlusion prevents exact row mapping. | partial | visibility / overwrite | Good for broad clusters, weak for exact event frames. |
| damage labels | #173/#174 recorded visible labels | Label-change windows are now bounded approximately. | partial | sampling tolerance | Useful for #177, not damage authority. |
| frame-level timing | #173 held exact timing unresolved | #176 provides coarse 60 fps windows with tolerance. | partial | exactness limitation | No exact startup/contact/hit/recovery frames are claimed. |
| hit-by-hit attribution | unresolved | still unresolved | unknown | out of scope | Routed to #177. |

## Failure Analysis

| Failure / uncertainty | Cause | Impact | Follow-up |
|---|---|---|---|
| Row-to-action boundaries overlap | Purple portal effects, Drive transitions, and juggle phases overlap across prompt rows. | Several rows are partial or ambiguous instead of aligned. | #177 should treat #176 windows as candidate ranges, not exact order. |
| Input-history scroll overwrites earlier entries | The right-side history remains visible, but entries scroll and accumulate during long sequences. | Exact input-to-row matching is weak for rows 8-12. | #176 method can be repeated with denser frame stepping if needed; #177 should not overclaim. |
| Cinematic occlusion | Super/cinematic camera movement obscures actors and labels. | Row 12 is bounded broadly but not hit-by-hit. | #177 may attribute only coarse windows unless stronger evidence exists. |
| Damage label sampling is sparse | Damage crop was sampled at 2 fps, not frame-by-frame. | Label changes are bounded to approximate windows only. | #177 can request denser targeted sampling for specific labels if needed. |
| Command prompt vs execution order is not identical proof | Prompt rows provide a trial answer key, but actual visible execution still requires frame/action support. | Prompt rows cannot become accepted route facts. | Keep review-only routing. |
| No visual atlas matching | #178/#179 are not implemented. | Ambiguous move/action identity remains weak. | Use visual references later if needed. |

## Reusable Frame/Input Alignment Method

This section records the reusable method from #176 so future Codex/Hermes
video-analysis runs can repeat frame/input alignment without relying on chat
history or local memory.

1. Pre-analysis context loading
   - Load same-sample source descriptor, observations, review notes, prior
     calibration reports, and any command-prompt oracle.
   - Load damage/scaling context reports when label attribution is a downstream
     goal.
   - Load character move registry and frame-current metadata only as candidate
     labels, not as proof of video events.
   - Record what each artifact can guide and cannot authorize.

2. Frame stepping / sampling plan
   - Normalize the timeline to 60 fps for reporting.
   - Inspect broad full-frame samples first, then targeted input-history and
     damage-label crops.
   - Use denser sampling only for windows where sparse samples expose a
     concrete ambiguity.
   - Record the sampling interval and tolerance.

3. Targeted crop plan
   - Use repo-external scratch only for all frame, crop, contact-sheet, and
     visual derivative work.
   - Create separate views for full action, input history, and damage labels
     when the UI layout supports it.
   - Do not commit raw visuals, raw OCR, raw tool output, or private paths.

4. Command prompt row alignment workflow
   - Start from the sanitized command-prompt oracle.
   - Assign each row an approximate timestamp/frame window only when nearby
     input-history changes, action phases, or UI labels support it.
   - Mark rows `partial`, `ambiguous`, `unknown`, or `not_visible` rather than
     forcing an exact execution frame.

5. Input-history alignment workflow
   - Summarize visible input-history clusters as sanitized text.
   - Map clusters to prompt-row groups only when timing and token patterns
     support the connection.
   - Treat scrolling/overwrite as an explicit limitation.

6. Action/hit/damage label alignment workflow
   - Record coarse action phases, hit-event candidates, and damage-label change
     windows separately.
   - Keep label timing review-only until #177 can compare labels against
     action/hit candidates.
   - Do not infer exact damage/scaling facts from the video.

7. Confidence and terminal routing
   - Record confidence per row or phase.
   - Preserve exact-current-fact boundaries.
   - Route hit/damage/scaling attribution to #177 and visual matching to
     #178/#179 when needed.

### Next-Agent One-Shot Checklist

Before closing a future frame/input alignment run, confirm:

- relevant repo context was loaded and recorded;
- the command-prompt oracle was used as the primary target list;
- the frame stepping interval and timestamp-to-frame conversion were recorded;
- input-history, action-phase, hit-event, and damage-label regions were
  inspected separately where possible;
- prompt rows were assigned approximate frame/time windows only when evidence
  supported them;
- ambiguous rows and overlapping action windows were held instead of forced;
- no exact current frame data, route validity, or damage authority was claimed;
- raw media, frames, screenshots, OCR output, tool output, and private paths
  were not committed;
- remaining attribution work was routed to #177.

## Improvement Applied In This PR

#176 adds this report's reusable frame/input alignment method and a narrow
workflow subsection in `workflows/ingest-video.md` so future agents can repeat
the same steps without relying on chat prompting.

The improvement is intentionally procedural. No validator was added because this
is one concrete source execution, not a repeated validator-worthy failure.

## Follow-Up Routing

| Follow-up issue | Routing from #176 |
|---|---|
| #177 | Use #175 command rows and #176 frame/input/damage-label windows to attempt review-only hit/damage/scaling attribution. |
| #178 | Add gated repo-external visual atlas acquisition before relying on visual references. |
| #179 | Use JP visual references to re-check ambiguous action identity and overlapping move windows. |
| #183 | Add SF6 system-mechanics math reasoning fixtures using #174/#176/#177 examples once attribution examples are stronger. |

## Terminal State

| State | Result | Reason |
|---|---|---|
| frame/input alignment PASS / PARTIAL / FAIL | PARTIAL | Approximate windows were recorded for command rows, input-history clusters, action phases, hit candidates, and damage-label changes, but several rows remain ambiguous. |
| command rows aligned | partial | Rows 1-2 and 12 have useful coarse windows; mid-sequence rows overlap and remain partial/ambiguous. |
| input-history alignment | partial | Input clusters are visible, but scrolling/overwrite prevents exact row mapping. |
| action/hit/damage label alignment | partial | Damage-label windows are bounded, but hit-by-hit attribution is still #177 scope. |
| accepted current fact | no | All observations are calibration evidence only. |
| curated knowledge | no | No stable concept or accepted gameplay knowledge is created. |
| generated references | no | Public generated references and `sf6-agent` behavior are unchanged. |

#176 is complete if this review-only calibration report is accepted: bounded
frame/input/damage-label windows exist, uncertainty is recorded, reusable method
is preserved, and #177 has structured input for attribution without any current
fact promotion.

## Cleanup And Validation

| Check | Result |
|---|---|
| Raw media used? | yes, via out-of-band local mapping only |
| Scratch cleanup | completed before commit |
| Raw media committed? | no |
| Frames/screenshots/contact sheets committed? | no |
| Raw OCR/tool output committed? | no |
| Private paths committed? | no |
| Validators run | see PR body |

