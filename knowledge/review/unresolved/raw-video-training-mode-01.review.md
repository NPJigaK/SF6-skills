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

#174 loaded the #160 / PR #171 Hameko combo-scaling source-derived mechanics
candidates and compared them against the sanitized #173 damage/scaling oracle.

Report:
`docs/testing/video-analysis-calibration/raw-video-training-mode-01-combo-scaling-context-20260514.md`.

Result: the Hameko candidates are useful analysis context, but insufficient to
complete scaling attribution without command/move normalization, frame/action
alignment, and hit-by-hit damage mapping. The visible #173 labels remain
calibration observations only; Hameko values remain review-only, unverified
system-mechanics candidates.

Terminal state remains review-only calibration evidence. #175, #176, and #177
remain required before damage/scaling attribution can be evaluated.

## Next Review Questions

| Residual gap | Follow-up issue | Notes |
|---|---|---|
| Hameko combo-scaling candidates from #160 / PR #171 were not loaded into this damage/scaling calibration. | #174 | This is a workflow/context-loading failure, not a failure of #171. |
| Combo-trial command prompts were not normalized to canonical move candidates. | #175 | Needed before predicted move order can be compared to an answer key. |
| Coarse frame ranges were not aligned with input history, action phases, hit events, or damage labels. | #176 | Needed for frame-level calibration without claiming current frame data. |
| Visible damage/scaling labels were not attributed hit-by-hit or move-by-move. | #177 | Should use #173 oracle plus #171 model candidates where applicable. |
| External visual atlas acquisition is missing. | #178 | Needed for move/action identification support without committing GIFs/images. |
| JP move/action matching against visual references was not attempted. | #179 | Depends on gated repo-external visual reference acquisition. |
| Source-derived repo knowledge is not automatically loaded before later video analysis. | #180 | Should add a checklist for loading reviewed repo artifacts rather than Hermes local memory. |

Open questions that remain after #173:

- Should a later raw-local gameplay source create claim artifacts when it
  contains a reviewable source-derived concept beyond visual observation?
- Should future raw-local reports distinguish direct playback review from
  contact-sheet review as separate execution-depth fields in a shared template?
- Should the repo define a dedicated sanitized local-source descriptor contract
  if more raw-local samples are added?
