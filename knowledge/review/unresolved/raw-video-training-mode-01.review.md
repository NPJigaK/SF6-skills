---
id: sf6-review-raw-video-training-mode-01
title: Raw Local Training-Mode Video Review
claim_kind: observation
source_kind: reproducible_observation
source_role: raw_local_training_mode_review
evidence_basis:
  - "Sanitized local source descriptor recorded in knowledge/sources/videos/raw-video-training-mode-01.md."
  - "Timestamped observations recorded in knowledge/evidence/video-observations/raw-video-training-mode-01.observations.md."
  - "Analysis calibration report recorded in docs/testing/video-analysis-calibration/raw-video-training-mode-01-20260514.md."
  - "Temporary frames and contact sheet were created only in repo-external scratch."
  - "No raw media, private path, frames, screenshots, contact sheet, transcript, or raw tool output was committed."
verification_state: partially_verified
confidence: 0.46
volatility: patch_sensitive
patch_sensitivity: high
review_status: needs_review
source_refs:
  - label: "Source metadata: raw-video-training-mode-01"
    path: "knowledge/sources/videos/raw-video-training-mode-01.md"
    accessed_at: "2026-05-14"
  - label: "Video observations: raw-video-training-mode-01"
    path: "knowledge/evidence/video-observations/raw-video-training-mode-01.observations.md"
    accessed_at: "2026-05-14"
review_after: "2026-08-14"
summary: "Review note for #170 source E2E on a maintainer-local raw SF6 training-mode video; source-derived observations are sanitized and the analysis-calibration result is held as partial calibration evidence."
---

# Raw Local Training-Mode Video Review

This review note tracks #170 one-source E2E execution for a maintainer-local raw
training-mode video. It is canonical review tracking, but it is not accepted
curated knowledge and must not feed generated knowledge references.

## Review Status

- Sanitized local source descriptor created: yes.
- Timestamped raw-local observation artifact created: yes.
- Analysis calibration report created: yes.
- Candidate claims artifact created: no; the source did not support a
  reviewable claim beyond sanitized observation/report-only routing.
- Raw local video accessible through out-of-band mapping: yes.
- Private local path recorded in repo: no.
- Raw video stored in repo: no.
- Raw frames or screenshots stored in repo: no.
- Contact sheet stored in repo: no.
- Full captions or transcript stored in repo: no.
- Raw tool output or logs stored in repo: no.
- Scratch/cache policy followed: yes.
- Curated promotion performed: no.
- Generated references changed: no.
- Exact current values accepted: no.
- Current verification required before using visual labels as facts: yes.
- Analysis-calibration terminal state: PARTIAL.

## Content Execution Record

| Field | Result |
|---|---|
| Source sample ID | `raw-video-training-mode-01` |
| Source family | maintainer-local raw video |
| Private path recorded? | no |
| Access method | maintainer-provided out-of-band mapping; path not committed or recorded |
| Metadata inspection | `ffprobe` metadata inspection |
| Media summary | MP4-family container, HEVC video, 1920x1080, about 37.93 seconds, 60 fps nominal, 2272 reported video frames, AAC stereo audio stream present |
| Content execution depth | metadata inspection plus temporary frame/contact-sheet visual review |
| Direct video playback reviewed? | no |
| Temporary frame/contact sheet reviewed? | yes |
| Direct audio reviewed? | no |
| Captions/transcript reviewed? | no |
| Raw media or derivatives committed? | no |
| Scratch cleanup | completed before commit |

## Calibration Result

The analysis-calibration terminal state is **PARTIAL**.

Character, control-mode, training/combo-trial context, and final visible damage
were interpreted correctly after targeted UI crops. Exact move naming,
frame-level action/contact timing, hit-by-hit scaling attribution, and input
history alignment remain unresolved because the first-pass contact sheet and
sampled frames do not provide enough reliable evidence without a stronger OCR,
move-recognition, or frame-by-frame analysis method.

## Source-Derived Knowledge Units

The output of this source E2E is not a video summary and not a combo proof. The
source was analyzed for observation units, then routed through the source-unit
promotion decision gate.

| knowledge_unit_id | extracted observation or knowledge | terminal route | reason |
|---|---|---|---|
| `ku-raw-training-context` | Training/combo-trial style UI with command list and input history visible. | sanitized observation/report only | Useful to prove raw-local video ingest and observation handling; not a stable concept needing curated promotion. |
| `ku-raw-training-actors` | JP and Ryu labels/characters are visible in the sample. | review-only hold | Visual labels are source-local and must not become roster/current-fact authority. |
| `ku-raw-training-sequence` | A guided player-side sequence with hit effects, airborne/cinematic phases, and success/completion context is visible. | sanitized observation/report only | No exact route, move recognition, damage authority, or combo validity is accepted. |
| `ku-raw-training-current-fact-like-labels` | Training UI combo/damage labels are visible in sampled frames. | review-only hold | Values are current-fact-like visual labels and require a separate authority/reproduction path before use. |
| `ku-raw-training-analysis-method` | Contact-sheet-only review was insufficient for exact move/timing/damage interpretation; targeted UI crops improved oracle extraction. | analysis-method knowledge | Captured in calibration report and workflow note. |

## Promotion Decision

No unit was promoted to curated knowledge.

Reasons:

- The source is a single maintainer-local raw clip, not a stable terminology or
  strategy source.
- The useful result is sanitized evidence that the repo can process raw-local
  training-mode video without leaking private path or raw media, plus
  calibration evidence about what the current analysis method can and cannot
  infer.
- The visible sequence is source-local and does not safely establish an
  accepted combo route, exact damage, current-system mechanic, or public answer
  behavior.
- Observed UI labels and visible character labels are review input only.
- Any future claim about route validity, damage, move identity, or system
  mechanics must use a separate current-fact/reproducible verification path.

## Terminal Decisions

| Candidate | Decision | Reason |
|---|---|---|
| Raw local source descriptor | metadata/source descriptor created | Needed to identify the sanitized sample and private-path boundary. |
| Raw local visual observations | sanitized report / observation artifact created | Bounded visual review occurred through repo-external temporary derivatives. |
| Analysis calibration | PARTIAL | Prediction/oracle comparison exists; character/control/context/final damage are correct or partial, while exact move/timing/scaling remain unresolved. |
| Candidate claim artifact | not created | No source-derived claim was safe or useful beyond observation/report-only routing. |
| Curated knowledge | not promoted | Single raw local clip cannot establish stable knowledge without separate review. |
| Current-fact-like labels | review-only hold | Training UI damage/combo labels and visible action details do not override canonical current-fact authority surfaces. |
| Rejected unsafe | none | No unsupported unsafe claim was created; no rejection was fabricated for coverage. |

## Workflow Findings

- `workflows/ingest-video.md` needed a narrow raw-local analysis calibration
  note so future runs separate prediction, oracle, comparison, failure analysis,
  and improvement.
- `workflows/review-claims.md` and `workflows/media-scratch-cache-policy.md`
  were sufficient for this raw-local video source-unit execution.
- The existing video source and observation validators accepted a sanitized
  local sample descriptor with no private path.
- No schema, policy, or validator change was needed.

## 2026-05-14 Combo-Scaling Context Follow-Up

#174 loaded the #160 / PR #171 SF6 combo-scaling system-mechanics candidates
extracted from the Hameko article and compared them against the sanitized #173
damage/scaling oracle.

Report:
`docs/testing/video-analysis-calibration/raw-video-training-mode-01-combo-scaling-context-20260514.md`.

Result: the Hameko-sourced SF6 combo-scaling candidates are useful analysis
context, but insufficient to complete scaling attribution without command/move
normalization, frame/action alignment, and hit-by-hit damage mapping. The
visible #173 labels remain calibration observations only; values extracted from
the Hameko article remain review-only, unverified system-mechanics candidates.

Terminal state remains review-only calibration evidence. #175, #176, and #177
remain required before damage/scaling attribution can be evaluated.

## 2026-05-14 Command Prompt Normalization Follow-Up

#175 created a sanitized command-prompt oracle for the visible JP `上級 5`
combo-trial UI and mapped prompt rows to canonical move candidates where the
visible input tokens matched existing JP move metadata.

Report:
`docs/testing/video-analysis-calibration/raw-video-training-mode-01-command-prompt-normalization-20260514.md`.

Result: ordered prompt rows were extracted as sanitized text, and candidate JP
move IDs were produced for many rows. Several prompts remain review-only holds:
OD Veehat/Departure variant, Veehat-set follow-up behavior, OD Triglav variant,
and SA3/CA distinction. The Drive Parry `66` row is mapped to review-only
system-action candidate `jp_068_parry_drive_rush`, with exact execution and
timing held for #176.

Terminal state remains review-only calibration evidence. The command-prompt
oracle can support #176 and #177, but it does not establish accepted move order,
route validity, current frame facts, or damage/scaling authority.

## 2026-05-15 Frame/Input Alignment Follow-Up

#176 created a bounded frame/input alignment calibration using the #175
sanitized command-prompt oracle.

Report:
`docs/testing/video-analysis-calibration/raw-video-training-mode-01-frame-input-alignment-20260515.md`.

Result: command prompt rows, input-history clusters, action phases,
hit-event candidates, and damage-label changes were aligned to approximate
frame/timestamp windows where the sampled evidence supported it. The result is
PARTIAL: rows 1-2 and the super/cinematic row have useful coarse windows, but
the mid-sequence rows remain partial or ambiguous because input-history
scrolling, visual effects, and cinematic occlusion prevent exact row-to-action
mapping.

Terminal state remains review-only calibration evidence. #176 does not accept
exact current frame facts, route validity, move execution timing, or
damage/scaling authority. It provided the bounded windows used by #177 for
review-only damage/scaling attribution.

## 2026-05-15 Damage/Scaling Attribution Follow-Up

#177 added
`docs/testing/video-analysis-calibration/raw-video-training-mode-01-damage-scaling-attribution-20260515.md`.

Result: damage/scaling attribution PARTIAL. The pass used #175 command rows and
#176 frame/input/damage-label windows to cover every loaded visible label as
partial or unknown. Early `800 (100%)` is partially associated with the row 2
HP candidate after OD Veehat setup; `600/400/420` labels are partially
associated with the row 11 late juggle window; `408/126/210/272/125/136`
remain unknown in the row 10/11 to row 12 transition; `500/100/1000 (50%)`
labels are partially associated with the row 12 SA3/CA family window.

No accepted current damage, scaling, route, move-order, or frame facts were
created. #178/#179 remain relevant for visual/action identity, and #183 remains
relevant for math reasoning fixtures and insufficient-evidence cases.

## 2026-05-15 External Visual Atlas Acquisition Follow-Up

#178 added
`docs/testing/video-analysis-calibration/external-visual-atlas-acquisition-20260515.md`.

Terminal state: visual-atlas-acquisition
USABILITY_SMOKE_PARTIAL_NEEDS_PREPROCESSING. The PR defines a gated
Scrapling-aligned acquisition path and selects a tiny JP scope covering
Stribog, OD Triglav, and SA3/CA candidate families. After maintainer approval
for a tiny SF6Frames repo-local smoke, #178 used Scrapling to fetch the JP
specials page and inspect M Stribog visual reference descriptors.

Result: the first direct descriptor was reachable but produced an
internal-server-error placeholder. The second iteration followed the page's
encoded animation descriptor path and acquired an actual M Stribog animated
WebP in repo-external scratch. It was classified as `needs_preprocessing`: #179
must re-acquire it repo-externally, extract frames, normalize crop/scale and
source-frame indexing, and account for hitbox/hurtbox overlays, frame numbers,
stage background, and watermark before matching. No GIF, image, WebP, frame,
screenshot, raw HTML, raw tool output, direct binary URL, local cache path, or
private path was committed; the repo-external temp binaries and sampled frames
were deleted.

#178 is complete as a usable/preprocessable acquisition smoke. #179 is
partially unblocked, but actual visual matching still requires repo-external
re-acquisition and preprocessing. External visuals remain review support only
and are not current-fact authority.

## 2026-05-15 Visual Reference Matching Follow-Up

#179 added
`docs/testing/video-analysis-calibration/raw-video-training-mode-01-visual-reference-matching-20260515.md`.

Result: visual-reference matching PARTIAL. The pass re-acquired the SF6Frames
M Stribog animated WebP through the #178 encoded-descriptor path, extracted
representative frames in repo-external scratch with Pillow, then inspected the
row 11 and row 8 raw-video target windows repo-externally before comparing
actual reference samples against actual raw-video samples.

Row 11 (`cmd-raw-jp-adv5-011`, `jp_034_236mp_stribog`) is classified as
`partial`: actual row 11 samples include mixed close-range and strike phases,
but the late portion shows purple/black effect pressure that partially overlaps
the M Stribog reference's broad projectile/effect phase. It does not prove
exact execution, hit source, move identity, or current facts. Row 8
(`cmd-raw-jp-adv5-008`, `jp_035_236hp_stribog`) is `inconclusive`: actual row 8
samples show portal/effect carryover and close-range strike/kick phases, but
not the clean horizontal M Stribog projectile phase; the reference is M
Stribog, not H Stribog.

No external WebP, GIF, image, frame, contact sheet, raw HTML, raw tool output,
direct binary URL, private path, generated reference, public runtime behavior,
raw-video frame/crop, or current-fact authority change was committed. External
visuals remain review support only. #183 remains relevant for reasoning
fixtures that prevent overclaiming from partial or inconclusive visual evidence.

Generalization boundary: #179 proves one narrow JP M Stribog visual-reference
matching pipeline slice only. It does not prove full-character, full-move,
match-level move recognition, or move-frequency analytics. Those require later
coverage, repeatability, false-positive/false-negative, and aggregation
validation before they can be claimed.

## Resolved Follow-Up Routing

| Previously mapped gap | Follow-up issue | Resolution |
|---|---|---|
| Hameko-sourced SF6 combo-scaling candidates were not loaded into damage/scaling calibration. | #174 | Resolved in #174 / PR #182: candidates extracted from the Hameko article were loaded and compared against the #173 oracle. Later #175/#176/#177 narrowed attribution, but did not verify current facts. |
| Combo-trial command prompts were visible but not normalized to canonical move candidates. | #175 | Resolved in #175: a sanitized command-prompt oracle and review-only candidate move mappings were created. Later #176/#177 used the rows for bounded alignment and partial attribution, but exact move order remains unaccepted. |
| Coarse frame ranges were not aligned with input history, command-prompt rows, action phases, hit events, or damage labels. | #176 | Resolved in #176 as PARTIAL calibration evidence: approximate frame/timestamp windows were recorded where supported and later used by #177. Exact execution remains unresolved. |
| Visible damage/scaling labels were not mapped to candidate hit/action windows. | #177 | Resolved in #177 as PARTIAL review-only attribution evidence: every loaded visible label is covered as partial or unknown, with no accepted current facts. |
| External visual atlas acquisition path and usability boundary were missing. | #178 | Resolved in #178 as USABILITY_SMOKE_PARTIAL_NEEDS_PREPROCESSING: a Scrapling-aligned path was recorded, a failing direct-descriptor placeholder was preserved as failure evidence, and a second encoded-descriptor iteration acquired an actual M Stribog animated WebP that #179 can re-acquire and preprocess repo-externally. |
| JP move/action matching against visual references was not attempted. | #179 | Resolved in #179 as PARTIAL review-only visual-to-visual matching evidence: M Stribog was re-acquired and preprocessed repo-externally, then compared against repo-external raw-video samples for rows 11 and 8. Row 11 remains partial, row 8 remains inconclusive, and no accepted move identity or current fact was created. |
| Source-derived repo knowledge was not automatically loaded before later video analysis. | #180 | Resolved in #180 / PR #181: `workflows/ingest-video.md` now requires `Loaded Repo Context` before video-analysis calibration, and #174 used that gate. |

## Next Review Questions

| Residual gap | Follow-up issue | Notes |
|---|---|---|
| SF6 system-mechanics math reasoning fixtures are missing. | #183 | Should cover combo-scaling arithmetic, insufficient-evidence detection, and current-fact authority boundaries after #177 has stronger attribution examples. |

Open questions that remain after #173:

- Should a later raw-local gameplay source create claim artifacts when it
  contains a reviewable source-derived concept beyond visual observation?
- Should future raw-local reports distinguish direct playback review from
  contact-sheet review as separate execution-depth fields in a shared template?
- Should the repo define a dedicated sanitized local-source descriptor contract
  if more raw-local samples are added?
