# Raw Video Visual Reference Matching: raw-video-training-mode-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #179 |
| Parent issues | #155 / #158 / #170 |
| Related command-prompt normalization | #175 / PR #184 |
| Related frame/input alignment | #176 / PR #185 |
| Related damage/scaling attribution | #177 / PR #189 |
| Related visual-atlas acquisition | #178 / PR #191 |
| Related context-loading workflow | #180 / PR #181 |
| Date | 2026-05-15 |
| Source sample id | `raw-video-training-mode-01` |
| Visual source | SF6Frames |
| Visual reference candidate | M Stribog / `jp_034_236mp_stribog` |
| Raw media used? | no; this pass used existing sanitized #175/#176/#177 raw-video artifacts |
| External visual binary used? | yes, repo-external scratch only |
| External visual binary committed? | no |
| Raw video/frame/image committed? | no |
| Terminal state | visual-reference matching PARTIAL; M Stribog reference re-acquired and preprocessed; row 11 and row 8 classified; no accepted current fact |

This report performs the first review-only JP visual-reference matching
calibration for `raw-video-training-mode-01`. It reuses the #178 SF6Frames
encoded-descriptor acquisition path for M Stribog, preprocesses the animated
WebP in repo-external scratch, and compares the resulting visual phases against
the sanitized raw-video candidate windows from #175/#176/#177.

This is not final move recognition, not current-fact authority, not route
validation, and not public `sf6-agent` behavior.

## Loaded Repo Context

This section implements the #180 pre-analysis repo context loading requirement.

| Artifact | Artifact type | Why loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `docs/testing/video-analysis-calibration/external-visual-atlas-acquisition-20260515.md` | calibration report | Provides the #178 SF6Frames encoded-descriptor path and M Stribog usability smoke. | Re-acquisition method, expected preprocessing needs, and source/binary boundaries. | Visual matching result, exact move identity, current facts, or binary storage. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-command-prompt-normalization-20260514.md` | calibration report | Provides sanitized command rows and JP move candidates. | Row 8 and row 11 target selection. | Accepted move order, execution timing, or route validity. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-frame-input-alignment-20260515.md` | calibration report | Provides approximate frame/timestamp windows and visual phase summaries. | Raw-video target windows and broad phase descriptors. | Exact frame events, pixel evidence, or current frame data. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-damage-scaling-attribution-20260515.md` | calibration report | Provides which labels remain partial/unknown and why action identity matters. | Whether visual matching could reduce #177 uncertainty. | Damage/scaling authority or exact hit attribution. |
| `knowledge/review/unresolved/raw-video-training-mode-01.review.md` | review note | Provides current resolved/open follow-up routing. | #179/#183 boundary and no-accepted-fact status. | Accepted gameplay knowledge. |
| `knowledge/sources/videos/raw-video-training-mode-01.md` | sanitized source descriptor | Provides source identity and raw-local boundary. | Sample identity and no-private-path handling. | Raw media access path or current fact authority. |
| `knowledge/evidence/video-observations/raw-video-training-mode-01.observations.md` | observation artifact | Provides source-local observations for the raw video. | General visual context and authority boundary. | Exact move identity or current facts. |
| `ingest/frame_data/config/registry/jp.moves.yaml` | move registry | Provides JP move ids and input-token candidates. | Candidate IDs for M/H Stribog rows. | Proof that raw-video action is the move. |
| `docs/architecture/external-frame-atlas-policy.md` | policy | Defines external visual atlas source roles and authority limits. | Source-role and storage boundary. | Permission to commit binaries or use visuals as authority. |
| `workflows/ingest-video.md` | workflow | Provides video calibration sequencing and #178 acquisition workflow. | Where to add visual matching calibration method. | Current facts or public runtime behavior. |
| `workflows/media-scratch-cache-policy.md` | policy | Defines repo-external scratch and forbidden media/cache artifacts. | Scratch and cleanup handling. | Permission to commit media. |
| `data/external-frame-atlas/evaluation/source-evaluation-matrix.json` | metadata-only source evaluation | Provides SF6Frames source status and forbidden uses. | Why this is maintainer-local review-only support. | Redistribution, binary storage, or current-fact authority. |
| `ingest/frame_data/src/sf6_ingest/fetch/scrapling_client.py` | fetch helper | Shows existing Scrapling `fetch_with_profile` wrapper and metadata shape. | Re-acquisition discipline. | New repo cache behavior or CI live fetch. |
| `ingest/frame_data/config/fetch_profiles.yaml` | fetch config | Shows configured Fetcher/StealthyFetcher profile pattern. | No-auth/no-cookie acquisition style. | Bypassing source boundaries. |

#178 did not store the visual reference in repo. This pass re-acquired it
repo-externally. #178 proved M Stribog is preprocessable, not directly
match-ready. Visual references are review support only. Visual similarity does
not authorize official move identity. `official_raw` remains current-fact
authority. Hermes/session memory is non-canonical.

## Visual Reference Re-Acquisition

| Field | Result |
|---|---|
| Source | SF6Frames |
| Character | JP |
| Move candidate | M Stribog |
| Candidate id | `jp_034_236mp_stribog` |
| Acquisition method | encoded animation descriptor path recorded by #178 |
| Scrapling alignment | `ingest/frame_data`-style `fetch_with_profile` static `Fetcher` |
| No-auth/no-cookie boundary | yes |
| Page fetch result | public JP specials page fetched; no challenge marker detected |
| Asset fetch result | encoded descriptor fetched; no challenge marker detected |
| File type observed | animated WebP |
| Bytes observed | 1,604,726 |
| Resolution | 750 x 573 |
| Frame count | 53 frames observed with Pillow |
| Overlay / frame number / watermark status | hitbox/hurtbox overlay visible; source frame numbers visible; stage background and SF6Frames watermark visible |
| Cleanup status | repo-external animated WebP and sampled inspection frames deleted before commit |
| Binary committed? | no |
| Direct binary URL committed? | no |
| Private path committed? | no |

The direct `data-animation-src` path from #178 remains recorded as a failure
case because it produced an error placeholder. This pass used the page's
encoded animation descriptor path, which yielded an actual M Stribog visual.

## Preprocessing Performed

| Field | Result |
|---|---|
| Frame extraction tool | Pillow `ImageSequence` in repo-external scratch |
| Frames available | 53 source animation frames |
| Frames sampled for review | 6 representative frames: opening, windup, projectile emergence, active projectile extension, sustained extension, final/recovery-like frame |
| Frame sampling strategy | broad phase sampling rather than frame-perfect alignment |
| Crop / resize / scale normalization | a temporary resized inspection sheet was created outside repo for human review; no committed derivative |
| Overlay handling | hitbox/hurtbox overlays were not removed; they were treated as source-reference context |
| Frame number handling | source frame numbers were preserved for inspection; they were not mapped to exact raw-video frames |
| Stage background / watermark handling | background and watermark were noted as comparison limitations, not removed |
| Source frame index handling | source frame numbers were used as approximate phase anchors only |
| Relation to 60 SF6 game-frame timeline | raw-video windows remain on #176's projected 60-game-frame timeline; SF6Frames animation frames were not treated as exact game-frame timing |
| What was not normalized | no pixel-level template matching, no geometry registration, no overlay separation, no clean/no-hitbox reconstruction, no raw-video crop extraction |
| Why not normalized further | #179 is a calibration pass; raw-video frames were not reopened and external binaries/derivatives cannot be committed |

The useful reference features from the sampled frames are:

- JP stands and rotates into a cane/projectile release posture.
- A horizontal purple/black/white projectile-like slash extends from JP toward
  the opponent side.
- The projectile effect occupies a broad horizontal band and persists through
  the middle and late sampled frames.
- Hitbox/hurtbox overlays and frame numbers make the source useful for
  phase-level review, but weaker for direct raw-video pixel matching.

## Raw-Video Matching Targets

This pass used the #175/#176/#177 sanitized raw-video reports instead of
reopening raw media. The targets are therefore review-only window descriptors,
not raw image evidence.

| target_id | prompt_row_id | candidate_move_id | approximate frame/timestamp window | raw-video evidence source | Why selected | Authority boundary |
|---|---|---|---|---|---|---|
| `vismatch-target-row-011` | `cmd-raw-jp-adv5-011` | `jp_034_236mp_stribog` | 900-1170 / 00:15.00-00:19.50 | #175 command row; #176 command prompt row alignment; #177 sequence step 011 | Exact candidate id matches the M Stribog visual reference and #177 had partial late-juggle attribution near this window. | Sanitized window only; not exact execution or accepted move identity. |
| `vismatch-target-row-008` | `cmd-raw-jp-adv5-008` | `jp_035_236hp_stribog` | 510-630 / 00:08.50-00:10.50 | #175 command row; #176 command prompt row alignment; #177 sequence step 008 | Same Stribog family, but different strength. Useful as same-family caution. | M reference cannot prove H Stribog, exact strength, or hit timing. |

OD Triglav and SA3/CA were not attempted because #178 only proved M Stribog
usability, and this PR must not become a broad atlas matching pass.

## Visual Matching Method

The method was intentionally conservative:

1. Use the SF6Frames M Stribog animation as visual reference only.
2. Extract representative source frames in repo-external scratch.
3. Identify broad visual phases: startup posture, projectile emergence,
   horizontal projectile extension, and late dissipation.
4. Compare those broad phases against sanitized #176 raw-video window
   descriptors, not against committed raw frames.
5. Account for source mismatch:
   - SF6Frames is frame-numbered, hitbox/hurtbox overlay reference footage.
   - The raw video is a combo-trial recording with effects, opponent state,
     hitstop, UI, and possible route/camera differences.
6. Classify target windows as `helped`, `partial`, `inconclusive`, `failed`, or
   `not_applicable`.
7. Preserve authority boundaries: no official move identity, no current fact,
   no exact frame data, no damage/scaling authority.

## Matching Result

| match_id | raw_video_target | candidate_move_id | visual_reference | reference_frames_or_phase | raw_video_window | matching_features | mismatching_features | result | confidence | reason | authority_boundary | needed_next_evidence |
|---|---|---|---|---|---|---|---|---|---:|---|---|---|
| `vismatch-001` | row 11 late Stribog candidate | `jp_034_236mp_stribog` | SF6Frames M Stribog animated WebP | sampled startup/projectile/recovery-like phases across 53 source frames | 900-1170 / 00:15.00-00:19.50 | Reference shows JP producing a horizontal purple/black/white projectile-like strike; #176 describes row 11 as projectile/juggle continuation and #177 associates late pre-super labels with row 11. Exact candidate id matches the reference. | No raw-video frames were reopened; #176 window is broad and may include row 10 spillover or prior effects. Overlay/reference footage differs from combo-trial footage. | partial | 0.46 | The visual reference helps confirm that the row 11 candidate family is visually plausible, but it does not prove exact execution, hit source, or current move identity. | Review-only visual support; not accepted move identity or frame data. | Repo-external raw-video frame crop review for row 11, plus H/OD references if adjacent effects remain ambiguous. |
| `vismatch-002` | row 8 same-family Stribog candidate | `jp_035_236hp_stribog` | SF6Frames M Stribog animated WebP | same sampled M Stribog phases | 510-630 / 00:08.50-00:10.50 | Reference's horizontal projectile/slash phase is compatible with #176's row 8 "purple projectile/strike effect window." Same Stribog family supports family-level plausibility. | Reference is M Stribog while row 8 candidate is H Stribog; strength-specific timing/spacing/visual extent may differ. Window overlaps later HP and OD Triglav candidates. | partial | 0.32 | The reference helps at family level only. It cannot distinguish `236HP` from `236MP` or prove row 8 execution. | Review-only same-family support; no exact strength or route authority. | H Stribog reference, repo-external raw row 8 crops, and adjacent OD Triglav reference if row 8-10 effects overlap. |

No target reached `helped` with high confidence because this pass did not
reopen raw-video frames. The useful improvement is narrower: M Stribog now has
a preprocessable visual reference and can be compared against row windows
without guessing what the move visually looks like.

## What The Visual Reference Helped With

- It provided an actual M Stribog visual reference instead of only a command
  token.
- It confirmed that M Stribog has a distinctive horizontal purple/black/white
  projectile-like visual phase.
- It made row 11's `jp_034_236mp_stribog` candidate more plausible at the
  broad visual-phase level.
- It helped separate Stribog-like horizontal projectile/slash phases from
  vertical spike or cinematic-super categories as a future matching heuristic.
- It reduced #177 uncertainty slightly for the late pre-super Stribog-family
  window, but did not resolve hit/damage/scaling attribution.

## What It Could Not Solve

- It did not identify OD Triglav or SA3/CA.
- It did not prove H Stribog for row 8 because the reference is M Stribog.
- It did not isolate exact hit timing or contact frames.
- It did not validate exact route order.
- It did not distinguish row 10 spillover from row 11 action in the late juggle
  window.
- It did not turn visible damage/scaling labels into accepted facts.
- It did not create a clean no-overlay visual reference.
- It did not update generated references, public runtime behavior, or
  `official_raw`.

## Failure Analysis

| Limitation | Cause | Impact | Follow-up |
|---|---|---|---|
| No raw-video pixel comparison | This pass used existing sanitized #176/#177 windows and did not reopen raw media. | Matching remains phase-level and review-only. | A later pass may use repo-external raw-video crops if maintainer provides the local mapping again. |
| Source overlay mismatch | SF6Frames reference has hitbox/hurtbox overlays, frame numbers, stage grid, and watermark. | Direct pixel matching is unsafe without preprocessing. | #179 method records overlay/watermark handling as required preprocessing. |
| Strength mismatch for row 8 | Reference is M Stribog; row 8 candidate is H Stribog. | Row 8 can only be same-family partial support. | Acquire H Stribog reference if row 8 becomes attribution-critical. |
| Adjacent action overlap | #176 windows for rows 8-11 overlap through purple effects, HP followups, and OD Triglav candidate windows. | Stribog reference cannot alone isolate exact move order. | Add H Stribog and OD Triglav references or denser raw-video frame review. |
| Source frame index mismatch | SF6Frames frame count is not mapped to #176 60-game-frame raw-video windows. | No exact timing claim can be made. | A future matching run must define a time/phase alignment method. |
| Visual evidence boundary | Visual similarity can suggest but not authorize exact current facts. | All results remain review-only. | #183 should include insufficient-visual-evidence reasoning fixtures. |

## Reusable Visual Matching Method

Future Codex/Hermes runs should repeat this method without chat history:

1. Load repo context:
   - prior same-sample video calibration reports;
   - visual-atlas acquisition report;
   - raw-video source descriptor and review note;
   - character move registry;
   - visual atlas policy and scratch policy.
2. Re-acquire the visual reference in repo-external scratch.
3. Preprocess the visual reference outside the repo:
   - extract frames;
   - sample broad phases;
   - record overlay/frame-number/watermark/background constraints;
   - delete binaries and derivatives before commit.
4. Select a tiny raw-video target set from existing command/frame/damage
   reports.
5. Compare broad visual phases, not exact frame identity.
6. Classify each target as `helped`, `partial`, `inconclusive`, `failed`, or
   `not_applicable`.
7. Record confidence, matching features, mismatching features, authority
   boundary, and needed next evidence.
8. Keep visual references review-only and never infer official move identity or
   current facts from visual similarity alone.
9. Route remaining gaps to existing issues or future scoped work.

### Next-Agent One-Shot Checklist

- Load #175/#176/#177/#178 artifacts and review note.
- Re-acquire the selected external visual reference repo-externally.
- Extract/sample frames with a tool that supports the asset type.
- Do not commit WebP/GIF/image/frame/contact sheet/raw HTML/tool output.
- Select one or two raw-video candidate windows from prior sanitized reports.
- Compare broad visual phases and record source mismatch.
- Classify every target.
- Keep all results review-only.
- Update follow-up routing.

## Improvement Applied In This PR

This PR adds this report and a narrow workflow addition:

`workflows/ingest-video.md` -> `Visual Reference Matching Calibration`.

No validator was added. This is one concrete source execution, and existing
validators already enforce the no-binary and video-artifact boundaries.

## Follow-Up Routing

| Follow-up | Status after #179 | Reason |
|---|---|---|
| #183 SF6 system-mechanics math reasoning fixtures | still open | Should cover reasoning where visual evidence is partial and cannot authorize exact move identity, damage/scaling, or current facts. |
| Additional visual references for H Stribog / OD Triglav / SA3/CA | future candidate, no new issue created | Row 8 strength, row 10 OD Triglav, and row 12 SA3/CA remain unresolved, but #179's scoped M Stribog matching is complete. |

## Terminal State

- visual-reference matching: PARTIAL
- M Stribog reference re-acquired: yes, repo-external scratch only
- M Stribog reference preprocessed: yes, representative frames sampled outside repo
- row 11 attempted: yes, `partial`
- row 8 attempted: yes, same-family `partial`
- accepted current fact: no
- curated knowledge: no
- generated references changed: no
- public runtime behavior changed: no
- #179 complete if this review-only matching calibration is accepted

## Cleanup And Validation

| Check | Result |
|---|---|
| Visual reference acquired? | yes, repo-external scratch only |
| Preprocessing outputs created? | yes, repo-external scratch only |
| Scratch cleanup | completed before commit |
| Binaries committed? | no |
| Raw media/frames/screenshots/contact sheets committed? | no |
| Raw HTML/tool output committed? | no |
| Direct binary URL committed? | no |
| Private paths committed? | no |
| Validators run | see PR body |
