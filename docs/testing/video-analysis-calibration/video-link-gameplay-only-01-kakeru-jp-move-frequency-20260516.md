# Kakeru JP Move-Frequency Calibration: video-link-gameplay-only-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #195 |
| Related source E2E | #161 / PR #194 |
| Parent issues | #155 / #158 |
| Date | 2026-05-16 |
| Source sample id | `video-link-gameplay-only-01` |
| Source URL | `https://www.youtube.com/watch?v=PaA8PNLeQUA` |
| Actor focus | Kakeru's JP / source-local actor A |
| Raw media used? | yes, repo-external scratch only |
| Raw media committed? | no |
| Frames/contact sheets committed? | no |
| Terminal state | move-frequency calibration PARTIAL |

## Loaded Repo Context

| Artifact | Type | Why loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `AGENTS.md` | repo guidance | Defines canonical surfaces, current-fact rules, and generated-surface boundaries. | Artifact placement, raw-media boundaries, and authority limits. | Source-specific move counts. |
| GitHub issues #195 / #161 / #155 / #158 | issue scope | Defines the active follow-up, completed source E2E row, and parent tracking context. | Scope, non-goals, and parent routing. | Closing parent tracking issues or implementing other source units. |
| `docs/testing/video-analysis-calibration/video-link-gameplay-only-01-20260516.md` | source E2E report | Prior #161 report for this source. | Source access method, gameplay-only boundary, and move-frequency gap. | Move-frequency results or exact move identity. |
| `knowledge/sources/videos/youtube-paa8pnlequa.md` | source metadata | Source identity and prior media-handling notes. | Source URL, title, duration, and review-only boundary. | Accepted player rank, strategy, or move facts. |
| `knowledge/evidence/video-observations/youtube-paa8pnlequa-gameplay-only.observations.md` | observation artifact | Sanitized source-local actor and gameplay observations. | Actor focus and broad source observations. | Exact move counts, frame data, or current facts. |
| `knowledge/review/unresolved/youtube-paa8pnlequa-gameplay-only.review.md` | review note | Prior terminal routing and move-frequency follow-up. | Held-observation boundary and #195 route. | Curated knowledge promotion. |
| `docs/testing/video-analysis-calibration/external-visual-atlas-acquisition-20260515.md` | calibration report | External visual reference acquisition usability precedent. | Repo-external visual handling and preprocessing boundary. | Move-frequency authority for this gameplay source. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-visual-reference-matching-20260515.md` | calibration report | Prior actual visual-to-visual comparison and generalization boundary. | How to separate partial visual support from exact move identity. | All-character/all-move recognition readiness. |
| `evals/questions/sf6-system-mechanics-math-reasoning.yaml` | eval fixture | Reasoning boundary for insufficient evidence and overgeneralization. | Safe answer behavior for partial visual evidence. | Current-fact values or exact move attribution. |
| `workflows/ingest-video.md` | workflow | Canonical video-ingest and visual calibration procedure. | Source review, repo-external scratch use, and review-only classification. | Public adapter behavior or exact facts. |
| `workflows/media-scratch-cache-policy.md` | workflow | Raw-media and scratch/cache policy. | What may be created locally and what must not be committed. | Permission to commit media or local paths. |
| `workflows/review-claims.md` | workflow | Claim and review terminal-routing procedure. | Whether to create claims or keep review-only evidence. | Automatic current-fact or curated promotion. |
| `ingest/frame_data/config/registry/jp.moves.yaml` | move registry | JP move family and candidate ID context. | Candidate bucket naming and known move-family inventory. | Exact current move usage counts from video. |
| `docs/architecture/sf6-move-recognition-evaluation-plan.md` | architecture note | Evaluation risks for move recognition. | Need for ambiguity handling and false-positive/false-negative evaluation. | A production move-recognition runtime. |
| `tests/fixtures/codex-hermes-delegation/move-frequency-review-only.json` | fixture | Existing review-only move-frequency delegation shape. | Evidence-strength wording and non-final count framing. | Accepted public analytics results. |

## Source Access And Scratch Handling

The source was re-accessed with public no-cookie tooling and reviewed in
repo-external scratch only.

| Field | Result |
|---|---|
| Metadata access | yes, public no-cookie `yt-dlp` metadata access |
| Temporary media review | yes, repo-external scratch only |
| Authentication/cookies/browser profile | not used |
| Source duration observed | approximately 8:14 |
| Reviewed cadence | 1 fps coarse full-timeline pass plus 2 fps dense per-minute contact-sheet pass |
| Visual derivatives created? | yes, temporary contact sheets outside the repo only |
| Captions/transcripts used? | no |
| Raw media or derivatives committed? | no |
| Scratch cleanup | completed before commit |

The temporary review confirmed a 60 fps, 1280x720 gameplay source. The review
used visual samples only. It did not use captions, transcripts, model training,
external visual atlas expansion, or generated references.

## Move-Frequency Analysis Strategy

This calibration tries to answer the practical downstream question: how many
times did Kakeru's JP use each move in this match?

The result is not an exact full-match move count. The inspected evidence is
sufficient for sampled-window family/candidate ranges, but not for exact move
identity or exhaustive event counting.

Counting categories used in this pass:

| Category | Meaning in this report |
|---|---|
| exact move count | A count where the exact move identity is supported by the visible action. No exact move counts were produced in this pass. |
| candidate move count | A count where the visible evidence suggests a move or small family, but exact identity remains review-only. |
| family-level count | A count range for a broad JP move family or visual pattern. |
| unknown/ambiguous action | JP action or pressure window visible in sampled evidence but not safely classifiable. |
| not-counted / out-of-scope | Opponent-only actions, intros/outros, channel end-card material, and repeated samples of one persistent effect. |

Sampling and de-duplication:

- A 1 fps coarse pass covered the full source timeline.
- A 2 fps dense pass covered the gameplay windows by minute.
- Contiguous samples showing the same persistent effect were treated as one
  candidate episode when the boundary was visually clear.
- Ranges are used where start/end boundaries were unclear.
- Fast normals, rapid drive actions, and short projectile startup frames are
  under-sampled by this method.

False-positive and false-negative risks are part of the result, not a separate
afterthought. Any count row with substantial ambiguity remains candidate,
family-level, or unknown.

## Candidate Move Taxonomy

The taxonomy is intentionally narrow and actor-focused. It uses JP move-family
context from the registry, but it does not claim exact move IDs from visual
similarity alone.

| Bucket | Candidate registry context | What counted here | Boundary |
|---|---|---|---|
| Stribog-like horizontal projectile/slash family | `jp_033_236lp_stribog` through `jp_036_236pp_stribog_od` | Horizontal or forward purple/black/white JP-side projectile/slash pressure. | Family-level only; exact strength and OD status unresolved. |
| Triglav / vertical spike / ground-burst family | `jp_027_22lp_triglav` through `jp_032_22pp_triglav_od_heavy` | Vertical spike or ground-burst effects around the opponent. | Family-level only; source and strength often ambiguous. |
| Vih / Departure / portal setup family | `jp_037_214lp_vihat` through `jp_044_214hp_vihat_cheni` | Persistent portal-like delayed effects, overhead or side setup pressure. | Family-level only; persistence can inflate counts. |
| Torbalan / ghost-like forward projectile candidate | `jp_047_236lk_torbalan` through `jp_050_236kk_torbalan_od` | Forward ghost-like or dark projectile candidates. | Candidate only; visual overlap with other purple effects is high. |
| Amnesia / counter-bomb candidate | `jp_045_22k_amnesia`, `jp_046_22kk_amnesia_od` | Counter/bomb-like ambiguous defensive moments. | Not safely counted in this pass. |
| Super/cinematic JP candidate | `jp_053_sa1_236236p` through `jp_056_ca_236236k` | JP-centered cinematic or high-freeze purple/black sequences. | Candidate only; exact super identity unresolved. |
| Normal / poke / close-strike candidate | JP normals in the current roster/registry context. | Close-contact strike or poke snapshots. | Not safely bounded by sampled contact sheets. |
| Movement / drive-system action candidate | JP drive/system-action registry context. | Dash, drive, or movement-like windows. | Actor attribution and exact action remain ambiguous. |
| Unknown / ambiguous JP action | not applicable | JP action visible but not classifiable. | Explicit ambiguity bucket. |

## Move-Frequency Table

The `observed_count` column records sampled-window episode ranges, not exact
full-match move totals.

| Bucket or move | Count type | Observed count | Confidence | Evidence basis | False-positive risk | False-negative risk | Notes |
|---|---|---:|---:|---|---|---|---|
| Stribog-like horizontal projectile/slash family | family-level | 12-18 sampled episodes | 0.42 | Repeated JP-side horizontal purple/black/white projectile or slash pressure in the 1 fps and 2 fps visual passes. | medium | high | Useful pressure-family signal, but exact strength, OD status, and move ID are unresolved. |
| Triglav / vertical spike / ground-burst family | family-level | 8-14 sampled episodes | 0.38 | Vertical spike or ground-burst effects around C. Viper in sampled gameplay windows. | medium-high | high | Some windows may be hit sparks, opponent effects, or portal follow-up effects. |
| Vih / Departure / portal setup family | family-level | 10-16 sampled episodes | 0.35 | Persistent purple portal-like delayed effects and overhead/side setup pressure. | high | high | One setup can persist across several samples, so episode boundaries are approximate. |
| Torbalan / ghost-like forward projectile candidate | candidate/family-level | 3-6 sampled episodes | 0.30 | Dark or ghost-like forward-moving effects from JP-side pressure. | high | high | Kept as candidate context because Stribog/portal/super effects can look similar in compressed samples. |
| Super/cinematic JP candidate | candidate | 3-4 sampled episodes | 0.45 | JP-centered high-effect or cinematic/super-like sequences in sampled gameplay. | medium | medium | Exact SA/CA identity is not inferred. |
| Normal / poke / close-strike candidate | candidate | not safely bounded; more than 25 sampled close-contact windows | 0.20 | Frequent close-contact snapshots and strike-like poses. | high | very high | Sparse visual sampling cannot produce exact normal counts. |
| Movement / drive-system action candidate | candidate | not safely bounded; more than 15 sampled movement/drive-like windows | 0.22 | Dash, movement, and drive-like visual cues in neutral and pressure windows. | high | high | Actor attribution and exact action category are often unclear. |
| Unknown / ambiguous JP action | unknown | more than 30 sampled windows | 0.25 | JP action or pressure is visible, but move family is not safely classifiable. | not applicable | not applicable | Preserved as an ambiguity bucket instead of forcing exact counts. |

No row in this table is an accepted current fact or official move-frequency
result. The table is review-only calibration evidence for what a future
move-frequency workflow would need to handle.

## Ambiguous / Unknown Actions

The largest ambiguity sources were:

- close-contact strings where normals, throws, drive actions, and hit sparks
  occur between 0.5 second samples;
- persistent purple portal/effect states that can span multiple sampled frames
  and risk double-counting;
- C. Viper effects, movement, and impact sparks overlapping JP effects;
- cinematic and KO moments where camera/effect changes hide the initiating
  action;
- neutral movement where dash, drive rush, jump, and spacing changes are not
  safely attributable from sparse contact sheets alone;
- source compression and replay-channel presentation, which reduce fine-grained
  visual confidence.

These windows are intentionally kept out of exact counts.

## False Positive / False Negative Analysis

False-positive risks:

- Stribog-like, Torbalan-like, and portal-like purple effects can visually
  overlap in compressed sampled frames.
- Vertical bursts may be Triglav, delayed portal effects, hit sparks, or
  opponent interaction effects.
- Persistent effects can be counted more than once if the episode boundary is
  not visible.
- Super/cinematic candidates may include KO, counter-hit, or channel-overlay
  moments rather than a clean super-start action.
- Movement and drive-system cues can belong to either actor when the players
  cross or effects obscure spacing.

False-negative risks:

- 1 fps and 2 fps sampling can miss fast normals, short startup frames, and
  quick drive-system actions.
- Single effects that begin and end between samples are absent from the sampled
  evidence.
- Close-range pressure can include several moves inside one sampled interval.
- Some JP projectiles and portals may be visually hidden by C. Viper effects,
  hit sparks, or camera changes.
- End-of-round and cinematic pauses can hide the initiating action.

The sampled ranges should therefore be read as calibration estimates for
review workflow design, not as a complete statistical output.

## Generalization Boundary

This PR does not prove all-character or all-move recognition, full-match
move-frequency analytics readiness, or automatic move counting. It proves only
that one Kakeru JP gameplay-only source can be reviewed with repo-external
video evidence and routed to a cautious sampled-window family/candidate
frequency table.

Generalizing beyond this source requires later scoped validation covering:

- broader character and move coverage;
- denser sampling or full-timeline review;
- candidate generation and ranking;
- negative controls and false-positive / false-negative measurement;
- repeatability across match videos, stages, overlays, compression levels, and
  camera/effect states;
- aggregation rules for persistent effects and multi-hit/multi-sample actions;
- review of whether any future automation should remain review-only or can
  safely feed public answer behavior.

## Reusable Move-Frequency Calibration Method

1. Load source, review, workflow, eval, and move-registry context before media
   work.
2. Select one actor and one source sample.
3. Re-access media only in repo-external scratch with no cookies, credentials,
   browser profile, or committed media.
4. Define candidate buckets before counting, including an explicit
   unknown/ambiguous bucket.
5. Inspect actual video evidence; do not count from source title or prior text
   summaries alone.
6. Separate exact, candidate, family-level, unknown, and not-counted events.
7. Use ranges when sampled evidence cannot define event boundaries.
8. Record false-positive and false-negative risks beside the counts.
9. Preserve current-fact boundaries: visual evidence does not override
   `official_raw` or prove exact move identity.
10. Delete raw media and all visual derivatives before commit.

### Next-Agent One-Shot Checklist

- [ ] Confirm active issue and parent routing.
- [ ] Load prior source report, source metadata, observations, and review note.
- [ ] Load media policy, video-ingest workflow, and relevant eval fixtures.
- [ ] Define actor focus and candidate buckets.
- [ ] Inspect actual video in repo-external scratch only.
- [ ] Record whether sampling is sparse, dense, or full-timeline.
- [ ] Count only what the visual evidence supports.
- [ ] Keep exact/candidate/family/unknown counts separate.
- [ ] Record FP/FN risks and ambiguity buckets.
- [ ] Commit only sanitized report/review artifacts.
- [ ] Run validators and raw/local-state scan.

## Terminal State

`move-frequency calibration PARTIAL`

Reason:

- Actual video evidence was inspected in repo-external scratch.
- A sampled-window move-family/candidate table was produced.
- Exact full-match move counts are not supported by the sampling method.
- Exact move identities, exact inputs, exact frame timing, current facts, and
  public answer behavior were not changed.
- Raw media and all visual derivatives remain outside the repo.

## Cleanup And Validation

| Check | Result |
|---|---|
| Raw media acquired? | yes, repo-external scratch only |
| Temporary contact sheets created? | yes, repo-external scratch only |
| Raw media committed? | no |
| Frames/screenshots/crops/contact sheets committed? | no |
| Captions/subtitles/transcripts committed? | no |
| Raw tool output committed? | no |
| Private paths committed? | no |
| Scratch cleanup | completed before commit |
| `validate-no-video-binary-assets.ps1` | PASS: `No video binary assets OK` |
| `validate-video-artifacts.ps1` | PASS: `Video artifacts OK` |
| `run-all.ps1` | PASS: `V2 validation suite OK` |
| `git diff --check` | PASS |
| `git diff --check origin/main...HEAD` | PASS |
| Raw/local-state scan | PASS: no prohibited changed-file matches |
| Generated-surface residual diff check | PASS after restoring validator-generated manifest churn |
