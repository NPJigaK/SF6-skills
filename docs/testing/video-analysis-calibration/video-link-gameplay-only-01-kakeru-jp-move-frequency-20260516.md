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
full-match move totals. The ranges are derived from repo-external sampled
review plus the representative count ledger below. The ledger is not a full
committed sample dump, and no raw contact sheets or frames are stored in the
repo.

| Bucket or move | Count type | Observed count | Confidence | Evidence basis | Representative ledger refs | False-positive risk | False-negative risk | Notes |
|---|---|---:|---:|---|---|---|---|---|
| Stribog-like horizontal projectile/slash family | family-level | 12-18 sampled episodes | 0.42 | Repeated JP-side horizontal purple/black/white projectile or slash pressure in the 1 fps and 2 fps visual passes. | MF-003, MF-009, MF-012, MF-014, MF-020, MF-022, MF-026, MF-028, MF-031 | medium | high | Useful pressure-family signal, but exact strength, OD status, and move ID are unresolved. |
| Triglav / vertical spike / ground-burst family | family-level | 8-14 sampled episodes | 0.38 | Vertical spike or ground-burst effects around C. Viper in sampled gameplay windows. | MF-004, MF-023, MF-029 | medium-high | high | Some windows may be hit sparks, opponent effects, or portal follow-up effects. |
| Vih / Departure / portal setup family | family-level | 10-16 sampled episodes | 0.35 | Persistent purple portal-like delayed effects and overhead/side setup pressure. | MF-001, MF-002, MF-010, MF-019, MF-021, MF-030 | high | high | One setup can persist across several samples, so episode boundaries are approximate. |
| Torbalan / ghost-like forward projectile candidate | candidate/family-level | 3-6 sampled episodes | 0.30 | Dark or ghost-like forward-moving effects from JP-side pressure. | MF-005 | high | high | Kept as candidate context because Stribog/portal/super effects can look similar in compressed samples. |
| Super/cinematic JP candidate | candidate | 3-4 sampled episodes | 0.45 | JP-centered high-effect or cinematic/super-like sequences in sampled gameplay. | MF-011, MF-015, MF-025, MF-027 | medium | medium | Exact SA/CA identity is not inferred. |
| Normal / poke / close-strike candidate | candidate | not safely bounded; more than 25 sampled close-contact windows | 0.20 | Frequent close-contact snapshots and strike-like poses. | MF-008, MF-018, MF-024 | high | very high | Sparse visual sampling cannot produce exact normal counts. |
| Movement / drive-system action candidate | candidate | not safely bounded; more than 15 sampled movement/drive-like windows | 0.22 | Dash, movement, and drive-like visual cues in neutral and pressure windows. | MF-013 | high | high | Actor attribution and exact action category are often unclear. |
| Unknown / ambiguous JP action | unknown | more than 30 sampled windows | 0.25 | JP action or pressure is visible, but move family is not safely classifiable. | MF-007, MF-016, MF-024, MF-029 | not applicable | not applicable | Preserved as an ambiguity bucket instead of forcing exact counts. |

No row in this table is an accepted current fact or official move-frequency
result. The table is review-only calibration evidence for what a future
move-frequency workflow would need to handle.

## Count Evidence Ledger

This is a representative evidence ledger, not a full committed sample dump. The
full sampled contact sheets and raw frames remain uncommitted. Count ranges in
the table above were derived from repo-external sampled review; this ledger is
sufficient to review why the result is PARTIAL, but it is not sufficient for
exact full-match move counts.

| Ledger ID | Timestamp or window | Sample pass | Actor focus | Observed visual bucket | Bucket assignment | Count treatment | Confidence | Included in table row | Dedupe or persistence note | False-positive note | False-negative note | Notes |
|---|---|---|---|---|---|---|---:|---|---|---|---|---|
| MF-001 | 00:20.0-00:21.0 | 2fps_dense | Kakeru JP | Purple overhead/side portal-like setup | Vih / Departure / portal setup family | family_level_episode | 0.36 | Vih / Departure / portal setup family | Treated as one setup episode start. | Could be delayed follow-up or hit spark. | A startup before the window may be missed. | Representative early portal/setup pressure. |
| MF-002 | 00:21.0-00:22.0 | 2fps_dense | Kakeru JP | Same persistent portal/effect state | Vih / Departure / portal setup family | persistent_effect_continuation | 0.30 | Vih / Departure / portal setup family | Continuation, not a separate episode. | Persistence could inflate counts if not deduped. | Additional overlapping action may be hidden. | De-duplication example. |
| MF-003 | 00:23.5-00:24.5 | 2fps_dense | Kakeru JP | Wide horizontal purple/black projectile or slash | Stribog-like horizontal projectile/slash family | family_level_episode | 0.45 | Stribog-like horizontal projectile/slash family | Discrete horizontal pressure episode. | Could overlap with portal follow-up. | Exact startup and strength may be missed. | Representative Stribog-like row support. |
| MF-004 | 00:29.0-00:30.5 | 2fps_dense | Kakeru JP | Vertical burst/spike near opponent | Triglav / vertical spike / ground-burst family | family_level_episode | 0.38 | Triglav / vertical spike / ground-burst family | Treated as one burst episode. | Could be hit spark or delayed portal effect. | Fast preceding setup may be absent. | Representative vertical-spike row support. |
| MF-005 | 00:31.5-00:32.5 | 2fps_dense | Kakeru JP | Dark forward ghost-like projectile/effect | Torbalan / ghost-like forward projectile candidate | candidate_episode | 0.30 | Torbalan / ghost-like forward projectile candidate | Candidate episode, not exact move. | Could be Stribog or portal effect in compression. | Short projectile phases may be missed. | Representative ghost-like candidate. |
| MF-006 | 00:37.0-00:37.5 | 2fps_dense | unclear / overlap | Orange impact and close-range collision | not assigned | not_counted_unclear_actor | 0.18 | not counted | Not counted because actor/source is unclear. | Opponent effect could be mistaken for JP action. | JP action inside impact may be missed. | Not-counted unclear-actor example. |
| MF-007 | 00:41.5-00:42.5 | 2fps_dense | Kakeru JP | Purple projectile/portal overlap | unknown / ambiguous JP action | unknown_episode | 0.26 | Unknown / ambiguous JP action | Not merged into Stribog or portal rows. | Could be either Stribog-like or setup follow-up. | A distinct move may be hidden. | Ambiguous bucket example. |
| MF-008 | 00:53.0-00:54.5 | 2fps_dense | Kakeru JP | Close-contact strike/poke snapshots | Normal / poke / close-strike candidate | candidate_episode | 0.20 | Normal / poke / close-strike candidate | Close-contact windows are not exact-counted. | Hit sparks can obscure actor and move. | Multiple normals can happen between samples. | Shows why exact normal counts are not bounded. |
| MF-009 | 02:00.0-02:05.0 | 2fps_dense | Kakeru JP | Repeated horizontal blue/purple projectile pressure | Stribog-like horizontal projectile/slash family | family_level_episode | 0.43 | Stribog-like horizontal projectile/slash family | Treated as one or two sampled episodes depending on visible separation; contributes to range. | Could include block/hit effects. | Intervening actions between samples may be missed. | Representative mid-video Stribog-like pressure. |
| MF-010 | 02:14.0-02:17.0 | 2fps_dense | Kakeru JP | Portal/follow-up pressure around opponent | Vih / Departure / portal setup family | family_level_episode | 0.34 | Vih / Departure / portal setup family | Setup/follow-up boundary unclear, so contributes to range. | Could overlap with vertical spike or hit spark. | Setup start may occur before sampled window. | Representative portal/setup range support. |
| MF-011 | 02:41.0-02:43.0 | 2fps_dense | Kakeru JP | JP-centered cinematic/high purple effect | Super/cinematic JP candidate | candidate_episode | 0.45 | Super/cinematic JP candidate | Counted as one cinematic candidate. | Could include KO or transition presentation. | Exact super-start frame not sampled. | Candidate only; no exact SA/CA identity. |
| MF-012 | 02:47.0-02:48.5 | 2fps_dense | Kakeru JP | Large purple horizontal slash/projection | Stribog-like horizontal projectile/slash family | family_level_episode | 0.42 | Stribog-like horizontal projectile/slash family | Discrete sampled pressure episode. | Could be super aftermath or portal effect. | Startup and strength unresolved. | Representative horizontal projectile/slash support. |
| MF-013 | 02:59.0-02:59.5 | 2fps_dense | unclear / Kakeru JP candidate | Green movement/drive-like visual | Movement / drive-system action candidate | candidate_episode | 0.22 | Movement / drive-system action candidate | Candidate action only; not exact-counted. | Green effects can belong to either actor. | Brief drive/movement actions are easy to miss. | Shows why drive/system counts are not bounded. |
| MF-014 | 04:09.0-04:10.5 | 2fps_dense | Kakeru JP | Horizontal purple projectile across screen | Stribog-like horizontal projectile/slash family | family_level_episode | 0.44 | Stribog-like horizontal projectile/slash family | Discrete projectile-like episode. | Could include opponent interaction spark. | Exact strength and startup unresolved. | Representative later Stribog-like support. |
| MF-015 | 04:13.5-04:17.5 | 2fps_dense | Kakeru JP | Large cinematic purple sphere / close-up sequence | Super/cinematic JP candidate | candidate_episode | 0.46 | Super/cinematic JP candidate | Treated as one cinematic candidate. | Could include cinematic transition frames. | Exact initiating move not sampled. | Candidate only; no current-fact authority. |
| MF-016 | 04:18.0-04:19.5 | 2fps_dense | Kakeru JP | Close purple hit/black effect overlap | unknown / ambiguous JP action | unknown_episode | 0.25 | Unknown / ambiguous JP action | Not forced into Stribog, portal, or normal rows. | Multiple move families look similar here. | Underlying action may be hidden by hit effects. | Ambiguous action example. |
| MF-017 | 04:24.0-04:24.5 | 2fps_dense | C. Viper / opponent | Green opponent rush/effect | not assigned | not_counted_opponent_only | 0.60 | not counted | Excluded because it is opponent-focused. | If counted, would inflate JP movement/drive row. | JP reaction during this window may be missed. | Opponent-only not-counted example. |
| MF-018 | 04:30.5-04:31.5 | 2fps_dense | Kakeru JP | Close-range strike/poke pressure | Normal / poke / close-strike candidate | candidate_episode | 0.21 | Normal / poke / close-strike candidate | Not exact-counted due to sparse samples. | Hit sparks and body overlap obscure move identity. | Several normals can occur between samples. | Representative normal/poke uncertainty. |
| MF-019 | 04:59.0-04:59.5 | 2fps_dense | Kakeru JP | Purple orb/setup pressure | Vih / Departure / portal setup family | family_level_episode | 0.33 | Vih / Departure / portal setup family | Contributes to setup range. | Could be hit spark or another projectile family. | Setup start and follow-up may be off-sample. | Representative setup support. |
| MF-020 | 06:01.5-06:05.0 | 2fps_dense | Kakeru JP | Blue/purple horizontal projectile pressure | Stribog-like horizontal projectile/slash family | family_level_episode | 0.42 | Stribog-like horizontal projectile/slash family | One or two episodes depending on separation; kept as range support. | Could include block/hit effects. | Fast recovery/follow-up not sampled. | Late-match Stribog-like support. |
| MF-021 | 06:22.0-06:24.0 | 2fps_dense | Kakeru JP | Purple portal/effect pressure near opponent | Vih / Departure / portal setup family | family_level_episode | 0.34 | Vih / Departure / portal setup family | Persistent effect range support. | Could be a spike or hit-effect overlap. | Additional setup action may be hidden. | Late-match setup example. |
| MF-022 | 06:34.0-06:36.0 | 2fps_dense | Kakeru JP | Horizontal purple projectile/slash pressure | Stribog-like horizontal projectile/slash family | family_level_episode | 0.43 | Stribog-like horizontal projectile/slash family | Discrete horizontal pressure episode. | Could be setup follow-up. | Exact move strength unresolved. | Representative late-match Stribog-like support. |
| MF-023 | 06:39.0-06:40.0 | 2fps_dense | Kakeru JP | Vertical purple spike/ground burst | Triglav / vertical spike / ground-burst family | family_level_episode | 0.39 | Triglav / vertical spike / ground-burst family | One spike/burst candidate. | Could be portal follow-up or hit spark. | Setup start may be missed. | Late-match vertical-spike support. |
| MF-024 | 06:42.5-06:44.5 | 2fps_dense | Kakeru JP | Close-contact / burst overlap | unknown / ambiguous JP action | unknown_episode | 0.23 | Normal / poke / close-strike candidate; Unknown / ambiguous JP action | Not exact-counted; used as ambiguity evidence. | Close strike, hit spark, or projectile follow-up can overlap. | Multiple actions may occur between samples. | Shows why normal and unknown buckets remain broad. |
| MF-025 | 06:55.0-06:56.5 | 2fps_dense | Kakeru JP | Bright purple cinematic/explosion-like effect | Super/cinematic JP candidate | candidate_episode | 0.42 | Super/cinematic JP candidate | Candidate only. | Could be high-effect hit sequence rather than super start. | Exact initiating frame may be absent. | Late super/cinematic support. |
| MF-026 | 07:19.5-07:20.5 | 2fps_dense | Kakeru JP | Blue/purple horizontal projectile pressure | Stribog-like horizontal projectile/slash family | family_level_episode | 0.40 | Stribog-like horizontal projectile/slash family | Counted as sampled pressure episode. | Could include hit/block spark. | Startup may be missed. | Final-gameplay Stribog-like support. |
| MF-027 | 07:25.5-07:28.0 | 2fps_dense | Kakeru JP | Cinematic close-up / super-like sequence | Super/cinematic JP candidate | candidate_episode | 0.47 | Super/cinematic JP candidate | Treated as one cinematic candidate. | Exact super identity unresolved. | Earlier input/action not sampled. | Final-gameplay cinematic candidate. |
| MF-028 | 07:31.5-07:32.5 | 2fps_dense | Kakeru JP | Horizontal purple projectile/slash | Stribog-like horizontal projectile/slash family | family_level_episode | 0.42 | Stribog-like horizontal projectile/slash family | Discrete sampled pressure episode. | Could be portal follow-up. | Exact strength unresolved. | Final-gameplay Stribog-like support. |
| MF-029 | 07:36.5-07:39.0 | 2fps_dense | Kakeru JP | Vertical/portal-like purple pressure | Triglav / vertical spike / ground-burst family; unknown / ambiguous JP action | unknown_episode | 0.28 | Triglav / vertical spike / ground-burst family; Unknown / ambiguous JP action | Ambiguous, included as weak range support only. | Could be portal setup, vertical spike, or hit spark. | Underlying move may be off-sample. | Ambiguous vertical/portal example. |
| MF-030 | 07:45.0-07:47.0 | 2fps_dense | Kakeru JP | Portal/setup-like purple pressure with continuation | Vih / Departure / portal setup family | persistent_effect_continuation | 0.31 | Vih / Departure / portal setup family | Continuation risk; contributes to range but not a clean exact count. | Persistent effects can double count. | Setup start may be missed. | Late de-duplication pressure example. |
| MF-031 | 07:51.0-07:53.0 | 2fps_dense | Kakeru JP | Horizontal purple projectile / end-of-round pressure | Stribog-like horizontal projectile/slash family | family_level_episode | 0.39 | Stribog-like horizontal projectile/slash family | Counted only before end-card/KO presentation dominates. | KO and overlay effects can pollute visual signal. | Late action boundary may be cut off. | Final counted projectile-like episode. |
| MF-032 | 07:55.0-07:59.5 | 2fps_dense | not gameplay | Channel end-card / post-match overlay | not assigned | not_counted_endcard | 0.95 | not counted | Excluded from gameplay counts. | Would be a pure false positive if counted. | Not relevant to JP actions. | End-card not-counted example. |

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
