# Raw Video Damage/Scaling Context Calibration: raw-video-training-mode-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #174 |
| Parent issues | #155, #158, #170 |
| Related source-derived mechanics work | #160 / PR #171 |
| Related raw-video calibration | #170 / PR #173 |
| Related workflow fix | #180 / PR #181 |
| Date | 2026-05-14 |
| Source sample id | `raw-video-training-mode-01` |
| Raw media used? | no |
| Raw media committed? | no |
| Terminal state | analysis-calibration PARTIAL + source-derived SF6 combo-scaling candidates used + review-only comparison evidence |

This follow-up uses the sanitized #173 oracle only. It does not reopen the raw
video, rerun frame extraction, perform command-list normalization, infer
canonical move names, or create accepted current-fact authority.

## Loaded Repo Context

This section implements the #180 `Pre-Analysis Repo Context Loading` gate for a
damage/scaling calibration follow-up.

| Artifact path | Artifact type | Why it was loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `knowledge/curated/mechanics/combo-scaling.md` | accepted curated knowledge | Provides the stable concept boundary for combo scaling. | General reasoning that damage labels must be read through combo context, route, starter, and system-action boundaries. | Exact scaling percentages, exact route formulas, character/move exceptions, or public current-system answers. |
| `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` | review-only system-mechanics candidate | Contains SF6 combo-scaling calculation model candidates extracted from the Hameko article. | Hypothesis generation for possible scaling sequence, counting-unit, multi-hit, follow-up, starter, Super Art, Modern, and exception interpretations. | Accepted current facts, generated references, official damage/scaling authority, or final route validation. |
| `knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md` | claim artifact | Splits the Hameko article evidence into reviewable stable-concept and current-system candidate rows. | Identifying which Hameko-sourced candidates are stable concept, current-fact-like, or exception categories. | Promotion of source-claimed values or examples into accepted gameplay facts. |
| `knowledge/review/unresolved/hameko-2023-combo-scaling.review.md` | review note | Records terminal routing from #160 and the authority boundary for the source-derived SF6 combo-scaling candidates. | Explaining why the candidates can be used as review-only analysis context. | Current-system verification or runtime answer authority. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-20260514.md` | calibration report | Provides the sanitized #173 oracle and known residual gaps. | Damage/scaling label comparison, source context, and follow-up routing. | Official damage values, hit-by-hit scaling attribution, canonical move order, or exact timing. |
| `knowledge/evidence/video-observations/raw-video-training-mode-01.observations.md` | observation artifact | Provides sanitized source-local observations from the raw-local clip. | Source-local character/context/sequence observations and caution boundaries. | Accepted roster facts, accepted combo route, current frame data, or current damage authority. |
| `knowledge/review/unresolved/raw-video-training-mode-01.review.md` | review note | Provides #170 terminal decisions and residual issue map. | Review-only routing and open gaps for #175, #176, #177, #178, and #179. | Accepted gameplay knowledge or current-system facts. |

The domain model is SF6 combo-scaling system mechanics. The Hameko article is
treated as source evidence for review-only candidates, not as final authority.

Hameko-sourced SF6 combo-scaling candidates can guide hypothesis generation.
They cannot authorize current facts. The raw-video oracle can support calibration comparison. It cannot
authorize official damage or scaling facts. Hermes memory, session history,
local skills, Curator output, logs, and local state are non-canonical; this
report relies on reviewed repository artifacts.

## Input Oracle From #173

The input oracle is copied only from sanitized values already recorded in #173.
No raw video, frames, screenshots, OCR output, private paths, or raw tool output
were used in this follow-up.

| Oracle field | Sanitized #173 value |
|---|---|
| Source context | Maintainer-local SF6 training/combo-trial recording. |
| Visible player character | JP. |
| Visible dummy/opponent character | Ryu. |
| Visible control mode | `C` icon visible for both sides, treated as source-local Classic-control UI evidence. |
| Visible trial label | `上級 5` in the command-list UI. |
| Visible command-prompt status | Command prompt structure was observed, but canonical move names and canonical move order were not extracted. |
| Hit-by-hit oracle | unavailable. |
| Exact frame oracle | unavailable beyond approximate sampled frame/timestamp ranges. |
| Visible damage labels | `800`, `2220`, `3622`, `4522`, final `5622`. |
| Visible percentage / modifier labels | `100%`, `70%`, `17%`, `50%`. |

## SF6 Combo-Scaling Candidates Considered From The Hameko Source

| Candidate id | Source artifact | Source-claimed candidate summary | Review status | accepted_use_allowed | Applicability to #173 oracle |
|---|---|---|---|---|---|
| `model-hameko-global-sequence`; `cf-hameko-global-progression` | `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` | Source claims a global scaling sequence and floor. | needs_review / unverified | false | Useful as a hypothesis that visible percentage labels may represent progression, but insufficient without hit/move index. |
| `model-hameko-counting-unit` | same | Source claims scaling is managed by move kind / technique category, not simple hit count. | needs_review / unverified | false | Useful because #173 lacks move-kind mapping; prevents treating labels as a simple hit-count sequence. |
| `model-hameko-multihit-single-operation` | same | Source claims one operation producing multiple hits is often one scaling unit. | needs_review / unverified | false | Useful caution for JP multi-hit/cinematic-looking segments; insufficient without canonical move/action segmentation. |
| `model-hameko-additional-input-followup` | same | Source claims added-input follow-ups may count as separate scaling units. | needs_review / unverified | false | Useful because command prompts and input history are visible, but not normalized or aligned. |
| `model-hameko-heavy-starter-exceptions`; `cf-hameko-weak-starter`; `cf-hameko-first-hit-only-starters` | same | Source claims starter categories can impose special scaling. | needs_review / unverified | false | Mostly insufficient: #173 does not identify the starter move or category. |
| `model-hameko-mid-combo-multistage-exceptions`; `cf-hameko-multistage-route-progression` | same | Source claims some moves/routes advance scaling by more than one step. | needs_review / unverified | false | Useful caution for visible jumps in percentage labels, but cannot be applied without move/hit attribution. |
| `model-hameko-super-art-minimum-guarantee`; `cf-hameko-sa-minimum-and-super-cancel` | same | Source claims Super Art floors and super-cancel modifier behavior. | needs_review / unverified | false | Potentially relevant because #173 includes a high-effects/cinematic segment and `50%` labels, but move identity is unavailable. |
| `model-hameko-modern-control-modifier`; `cf-hameko-modern-special-button` | same | Source claims Modern-control special-button modifiers. | needs_review / unverified | false | Not applicable to the visible #173 Classic UI icon unless later evidence contradicts the control-mode reading. |
| `model-hameko-character-move-exceptions`; `cf-hameko-jamie-drink-modifier`; `cf-hameko-kimberly-damage-modifier` | same | Source records character/move/control-scheme exception categories and examples. | needs_review / unverified | false | Generally not applicable to JP vs Ryu except the broader warning that character/move-specific exceptions may exist. |

## Damage/Scaling Comparison

| Observed label | Timestamp from #173 | Possible related Hameko-sourced candidate(s) | Comparison result | Reason | Required next evidence |
|---|---|---|---|---|---|
| `800 (100%)`, combo damage `800` | ~00:08 | `model-hameko-global-sequence`; `model-hameko-counting-unit` | useful | `100%` is consistent with the idea that early route labels may start at full scaling, but the Hameko-sourced candidate cannot determine whether this is first hit, second hit, or a move-kind unit. | #175 canonical command prompt normalization; #176 hit/frame alignment; #177 hit/action attribution. |
| combo damage `2220`; `420 (70%)` | ~00:20 | `model-hameko-global-sequence`; `cf-hameko-global-progression`; `model-hameko-counting-unit`; `model-hameko-mid-combo-multistage-exceptions` | insufficient | `70%` appears in the source-claimed progression extracted from the Hameko article, but #173 lacks the hit/move index and move category needed to decide whether this is ordinary progression or an exception. | #175, #176, #177. |
| combo damage `3622`; `136 (17%)` | ~00:24 | `model-hameko-heavy-starter-exceptions`; `model-hameko-mid-combo-multistage-exceptions`; `model-hameko-super-art-minimum-guarantee`; `model-hameko-character-move-exceptions` | unknown | `17%` is not directly explained by the loaded source-claimed global progression row. It may reflect stacked modifiers, route-specific exception behavior, move-specific handling, or UI semantics that #173 did not extract. | #175 canonical move/order data; #176 frame/action segmentation; #177 damage/scaling attribution; later system-mechanics verification. |
| combo damage `4522`; `100 (50%)` | ~00:28 | `model-hameko-global-sequence`; `model-hameko-super-art-minimum-guarantee`; `cf-hameko-sa-minimum-and-super-cancel` | insufficient | `50%` is source-claimed in Super Art floor categories extracted from the Hameko article, but #173 does not identify the action as a Super Art, super cancel, or ordinary route step. | #175 move candidate; #176 phase/timing; #177 label-to-hit mapping. |
| final combo damage `5622`; `1000 (50%)` | ~00:32-00:34 | `model-hameko-super-art-minimum-guarantee`; `cf-hameko-sa-minimum-and-super-cancel`; `model-hameko-mid-combo-multistage-exceptions` | insufficient | Final `50%` may be relevant to minimum-guarantee or cinematic/super-like hypotheses, but the raw-video oracle does not include canonical move identity or hit count. | #175 canonical command/move mapping; #176 frame stepping; #177 final-hit attribution. |
| visible percentage labels as a set: `100%`, `70%`, `17%`, `50%` | sampled #173 damage UI | `model-hameko-global-sequence`; `model-hameko-counting-unit`; `model-hameko-multihit-single-operation`; `model-hameko-additional-input-followup` | useful | The loaded candidates clarify that the labels cannot be interpreted as a simple hit-count series. They need move-kind, multi-hit, and follow-up handling before comparison is meaningful. | #175 command normalization, #176 input/history alignment, #177 hit-by-hit attribution. |

No contradiction was proven. The comparison found useful guidance and multiple
insufficiencies, but the #173 oracle is too coarse to verify, reject, or
quantitatively apply the source-claimed SF6 combo-scaling candidates.

## What The Source-Derived SF6 Combo-Scaling Candidates Helped With

The source-derived SF6 combo-scaling candidates changed the interpretation task
from "read visible damage labels" to "explain which missing structure is
required before the labels can mean anything."

It helped identify that:

- `100%`, `70%`, `17%`, and `50%` cannot be interpreted as a simple hit-count
  progression.
- The next required evidence is move/action-unit mapping, not just better OCR
  of damage labels.
- Multi-hit single-operation handling and additional-input follow-up handling
  are key unknowns for this JP combo-trial sample.
- `50%` labels should not be assumed to be ordinary global progression or Super
  Art minimum behavior without move identity.
- The `17%` label is a useful review target because it does not map cleanly to
  the loaded global-sequence row and may require stacked-modifier, exception, or
  UI-semantics analysis.

## What It Could Not Solve

The loaded Hameko-sourced SF6 combo-scaling candidates could not solve:

- canonical move order;
- hit-by-hit attribution;
- frame stepping;
- input/action alignment;
- exact scaling-unit index;
- whether a visible percentage belongs to a hit, a move, a minimum guarantee,
  a modifier stack, or another UI category;
- official current-system verification.

The source-claimed values extracted from the Hameko article remain unverified
community-source candidates. Raw-video labels remain source-local calibration
observations. Neither surface authorizes public damage/scaling answers.

## Learning-Loop Finding

#171 SF6 combo-scaling candidate knowledge was successfully loaded in #174. It
guided the comparison and made the missing evidence explicit, but it cannot
complete scaling attribution without the follow-up work in #175, #176, and
#177.

This confirms #180's context-loading gate is necessary. The repo becomes more
capable only when later tasks explicitly load and use reviewed repository
artifacts; merged knowledge does not improve analysis by itself.

## Follow-Up Routing

| Follow-up issue | Routing from #174 |
|---|---|
| #175 | Required to normalize visible command prompts into canonical move/action candidates. |
| #176 | Required to align sampled frames, input history, action phases, hit events, and damage-label changes. |
| #177 | Required to map each visible damage/scaling label to hit/action candidates and compare against #171 SF6 combo-scaling candidates. |
| #178 | Required before external visual references can support future move/action identification. |
| #179 | Required after #178 to compare JP move/action candidates against repo-external visual references. |
| #180 | Completed; this report uses its `Loaded Repo Context` gate. |
| #183 | Required to add SF6 system-mechanics math reasoning fixtures for combo-scaling arithmetic, insufficient-evidence detection, and current-fact authority boundaries. |

#183 was created for the broader SF6 math-reasoning fixture gap. The remaining
execution gaps are covered by #175-#179 and #183.

## Terminal State

| State | Result | Reason |
|---|---|---|
| source-derived SF6 combo-scaling candidates used | yes | #171 candidates extracted from the Hameko article were loaded and compared to #173 oracle labels. |
| analysis-calibration PASS / PARTIAL / FAIL | PARTIAL | The source-derived candidates were useful as analysis context, but scaling attribution remains blocked by missing command/move/hit/timing data. |
| review-only comparison evidence | yes | This report records model applicability without accepting current facts. |
| accepted current fact | no | Neither source-claimed Hameko-article values nor raw-video labels are accepted authority. |
| curated knowledge | no | This PR adds no stable curated concept and changes no generated references. |
| raw-video rerun | no | The existing sanitized #173 oracle was sufficient for #174 comparison. |

#174 is complete if this review-only comparison is accepted: SF6 combo-scaling
candidates extracted from the Hameko article were loaded, applied to the
sanitized raw-video oracle, and found useful but insufficient until
#175/#176/#177 provide the missing structure.

## Cleanup And Validation

| Check | Result |
|---|---|
| Raw media used | no |
| Scratch cleanup | not applicable; no scratch created |
| Raw media committed | no |
| Frames/screenshots/contact sheets committed | no |
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
