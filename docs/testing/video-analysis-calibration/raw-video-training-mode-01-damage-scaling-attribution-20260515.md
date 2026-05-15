# Raw Video Damage/Scaling Attribution: raw-video-training-mode-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #177 |
| Parent issues | #155 / #158 / #170 |
| Related source mechanics work | #160 / PR #171 |
| Related raw-video calibration | #170 / PR #173 |
| Related combo-scaling context comparison | #174 / PR #182 |
| Related command-prompt normalization | #175 / PR #184 |
| Related frame/input alignment | #176 / PR #185 |
| Related context-loading workflow | #180 / PR #181 |
| Date | 2026-05-15 |
| Source sample id | `raw-video-training-mode-01` |
| Raw media used? | no; this pass used existing sanitized #173/#174/#175/#176 artifacts |
| Raw media committed? | no |
| Raw OCR committed? | no |
| Terminal state | damage/scaling attribution PARTIAL; review-only attribution evidence; no accepted current fact |

## Loaded Repo Context

This report follows the #180 pre-analysis repo context loading requirement. Loaded context is repository evidence only; Hermes memory, session history, local skills, Curator output, logs, and local state are non-canonical.

| Artifact | Artifact type | Why loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `knowledge/curated/mechanics/combo-scaling.md` | accepted curated knowledge | Stable concept boundary for combo scaling terminology. | General distinction between stable concept prose and exact current values. | Exact current damage/scaling values, route validity, or hit-by-hit attribution. |
| `knowledge/review/current-fact-candidates/hameko-2023-combo-scaling-system-mechanics.md` | review-only system-mechanics candidate | Source-derived SF6 combo-scaling candidate mechanics extracted from Hameko article evidence. | Hypotheses about progression, counting units, multi-hit handling, followups, Super Art floors, and modifiers. | Current system authority or official values. |
| `knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md` | claim artifact | Claim-level provenance for the source-derived combo-scaling candidates. | Which mechanics candidates came from which source-derived claims. | Verification of current patch facts. |
| `knowledge/review/unresolved/hameko-2023-combo-scaling.review.md` | review note | Current review status for the Hameko-sourced candidate mechanics. | Why the candidates remain review-only and unverified. | Acceptance of the candidates as final authority. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-20260514.md` | calibration report | Original raw-video oracle and first-pass analysis. | Visible labels, source-local context, and unresolved analysis gaps. | Current damage/scaling facts or exact move order. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-combo-scaling-context-20260514.md` | calibration report | #174 comparison between visible labels and source-derived combo-scaling candidates. | Which labels were useful, insufficient, or unknown before frame/input alignment. | Hit-by-hit attribution or current authority. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-command-prompt-normalization-20260514.md` | calibration report | #175 sanitized command prompt oracle and review-only JP move/system-action candidates. | Candidate action labels and prompt row ids. | Accepted move order, route validity, or official move execution. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-frame-input-alignment-20260515.md` | calibration report | #176 approximate frame/input/action/hit/damage-label windows. | Bounded windows for attribution attempts. | Exact frame data, exact hit timing, or final action execution. |
| `knowledge/evidence/video-observations/raw-video-training-mode-01.observations.md` | observation artifact | Source-local visible observations from the raw video. | Calibration evidence and source-local labels. | Public current facts. |
| `knowledge/review/unresolved/raw-video-training-mode-01.review.md` | review note | Current residual routing for the raw-video calibration sequence. | Which follow-up issues remain open and which gaps have been resolved. | Acceptance of gameplay facts. |
| `knowledge/sources/videos/raw-video-training-mode-01.md` | source metadata | Sanitized source descriptor and raw-local boundary. | Sample identity and source handling constraints. | Private local path, raw media contents, or current fact authority. |
| `ingest/frame_data/config/registry/jp.moves.yaml` | move registry candidate context | Candidate ids for JP prompt rows from #175. | Review-only candidate labels for prompt rows. | Official current route validity or exact move execution. |
| `skills/sf6-agent/assets/frame-current/` | generated current-fact adapter asset context | Candidate label context already used by #175; not edited here. | Cross-checking names/ids as candidate context. | Canonical authorship for new knowledge; generated surfaces are derived. |

Authority boundary: the SF6 combo-scaling candidates extracted from Hameko article evidence can guide attribution hypotheses, but they cannot authorize current facts. The #173/#176 visible labels are calibration evidence only. The #175 command rows are candidate action labels only. Exact current facts must not be inferred from raw video alone.

## Input Data From Prior Calibration

| Input | Source | Summary | Boundary |
|---|---|---|---|
| Visible damage/combo labels | #173/#176 | `800`, `1400`, `1800`, `2220`, `2628`, `2754`, `2964`, `3236`, `3486`, `3622`, `4122`, `4322`, `4422`, `4522`, final `5622` where visible in prior reports. | Source-local calibration labels only. |
| Percentage/modifier labels | #173/#176 | `100%`, `80%`, `70%`, `51%`, `42%`, `34%`, `25%`, `17%`, `50%`. | Not accepted scaling facts. |
| Command prompt rows | #175 | 12 sanitized prompt rows from JP combo-trial UI. | Prompt oracle, not accepted execution order. |
| Candidate move/action ids | #175 | OD Veehat family, `jp_005_5hp`, `jp_009_2mp`, Veehat setup followup, `jp_015_j_mp`, `jp_068_parry_drive_rush`, `jp_035_236hp_stribog`, OD Triglav family, `jp_034_236mp_stribog`, SA3/CA family. | Review-only candidate ids. |
| Frame/input windows | #176 | Approximate 60 SF6 game-frame windows for prompt rows, input-history clusters, action phases, hit candidates, and damage-label changes. | Bounded alignment windows, not exact frame data. |
| Input-history clusters | #176 | Early command, portal followup, drive transition, mid-sequence scroll, super trail. | Coarse support only. |
| Action/hit/damage windows | #176 | `damage-change-001` through `damage-change-005`, plus early hold, super start, and completion phases. | Attribution starting points only. |

## Attribution Method

Attribution used existing sanitized artifacts only. Raw video was not reopened for this pass.

1. Use a 60 SF6 game-frame timeline for system analysis.
2. Keep source capture cadence separate as observation uncertainty; #176 records source metadata near 59.95 fps for this sample.
3. Use #175 prompt rows as candidate action labels.
4. Use #176 frame/timestamp windows to associate visible damage/scaling labels with candidate action/hit windows.
5. Use SF6 combo-scaling candidates extracted from Hameko article evidence as review-only hypothesis context.
6. Require overlap between damage-label windows and candidate prompt/action windows before making a partial attribution.
7. Mark unknowns rather than forcing mappings where prompt, hit, move, or frame evidence is insufficient.
8. Preserve authority boundaries: no accepted current damage/scaling facts, no exact route validation, no exact frame data.

Classification meanings:

| Classification | Meaning |
|---|---|
| `attributed` | A bounded review-only mapping has strong prompt/action/hit-window support. No row reaches this level in this pass. |
| `partial` | A useful candidate mapping exists, but exact hit/action identity or frame evidence is incomplete. |
| `unknown` | The label is visible but cannot be tied to a candidate hit/action with enough support. |
| `contradicted` | The visible label conflicts with loaded model candidates strongly enough to record a contradiction. None were proven. |
| `not_applicable` | The label is outside damage/scaling attribution scope. |
| `not_available` | The label was requested but not present in the loaded sanitized artifacts. |

## Damage/Scaling Attribution Table

| attribution_id | visible_label | combo_damage_label | percentage_or_modifier_label | approx_frame_range | approx_timestamp_range | candidate_prompt_row | candidate_move_or_action | candidate_hit_or_phase | related_combo_scaling_candidate | attribution_status | confidence | reason | authority_boundary | needed_next_evidence |
|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|
| attr-001 | `800 (100%)` | `800` | `100%` | 240-270 | 00:04.00-00:04.50 | `cmd-raw-jp-adv5-002` with setup from `001` | `jp_005_5hp` candidate after OD Veehat setup | first clear contact/damage change candidate | global progression first/second 100%; counting-unit rule | partial | 0.54 | Label appears in the first clear damage-change window near the row 2 HP candidate, but row 1 setup and exact contact frame are not isolated. | Review-only calibration evidence; not accepted damage or move fact. | Denser contact-frame confirmation and visual matching. |
| attr-002 | `600 (100%)` | `1400` | `100%` | 1110-1130 | 00:18.50-00:18.83 | `cmd-raw-jp-adv5-011` with possible earlier-row spillover | `jp_034_236mp_stribog` candidate / late juggle continuation | start of late pre-super damage ramp | global progression 100%; counting-unit/multi-hit handling | partial | 0.35 | #176 places this label in the row 11 window, but rows 8-10 may still contribute and the hit source is not isolated. | Review-only; not hit-by-hit current authority. | Hit/source isolation and input-history/action confirmation. |
| attr-003 | `400 (80%)` | `1800` | `80%` | 1135-1155 | 00:18.92-00:19.25 | `cmd-raw-jp-adv5-011` with possible earlier-row spillover | `jp_034_236mp_stribog` candidate / late juggle continuation | late pre-super hit candidate | global progression 80%; counting-unit rule | partial | 0.34 | Percentage aligns with a source-derived global-progression candidate, but the move/hit unit is not proven. | Review-only hypothesis support only. | Move/hit unit mapping and denser frame sampling. |
| attr-004 | `420 (70%)` | `2220` | `70%` | 1155-1170 | 00:19.25-00:19.50 | `cmd-raw-jp-adv5-011` with possible earlier-row spillover | `jp_034_236mp_stribog` candidate / late juggle continuation | late pre-super hit candidate | global progression 70%; counting-unit rule | partial | 0.38 | Label is a useful 70% anchor near the row 11 window, but exact hit source and counting unit remain unresolved. | Review-only calibration evidence. | Hit/action source isolation before #177-style result can become stronger. |
| attr-005 | `408 (51%)` | `2628` | `51%` | 1200-1230 | 00:20.00-00:20.50 | `cmd-raw-jp-adv5-010` / `011` transition | OD Triglav family or `jp_034_236mp_stribog` continuation | mid-to-late juggle hit candidate | rush/modifier, multi-stage exception, character/move exception candidates | unknown | 0.20 | `51%` is not directly explained by the loaded global sequence and may reflect stacked modifiers, exception categories, or UI semantics. | No contradiction or current fact accepted. | Move/hit unit mapping, modifier source, and visual reference matching. |
| attr-006 | `126 (42%)` | `2754` | `42%` | 1245-1275 | 00:20.75-00:21.25 | `cmd-raw-jp-adv5-010` / `011` transition | OD Triglav family or `jp_034_236mp_stribog` continuation | mid-to-late juggle hit candidate | multi-hit handling, multi-stage exception, stacked modifier candidates | unknown | 0.18 | `42%` is visible but not explained by the loaded simple progression; label source and hit unit are not isolated. | Review-only unresolved label. | Hit-by-hit source isolation and math fixture coverage for stacked modifiers. |
| attr-007 | `210 (42%)` | `2964` | `42%` | 1275-1305 | 00:21.25-00:21.75 | `cmd-raw-jp-adv5-010` / `011` transition | OD Triglav family or `jp_034_236mp_stribog` continuation | mid-to-late juggle hit candidate | multi-hit handling, multi-stage exception, stacked modifier candidates | unknown | 0.18 | Same percentage as attr-006 but different damage value; candidate hit/source is not isolated. | Review-only unresolved label. | Move identity and hit/event segmentation. |
| attr-008 | `272 (34%)` | `3236` | `34%` | 1320-1350 | 00:22.00-00:22.50 | `cmd-raw-jp-adv5-010` / `011` transition | OD Triglav family or `jp_034_236mp_stribog` continuation | mid-to-late juggle hit candidate | multi-hit handling, multi-stage exception, stacked modifier candidates | unknown | 0.18 | `34%` is not a direct loaded global-progression value and remains ambiguous. | Review-only unresolved label. | Better hit-event segmentation and source-derived modifier reasoning. |
| attr-009 | `125 (25%)` | `3486` | `25%` | 1365-1395 | 00:22.75-00:23.25 | `cmd-raw-jp-adv5-010` / `011` / transition to `012` | late juggle into super-start transition | pre-super transition hit candidate | multi-stage progression exception, stacked modifier, Super Art transition candidates | unknown | 0.17 | Label may be late juggle or transition-related; the source window does not isolate action source. | No accepted system conclusion. | Visual/action phase confirmation and #183 reasoning fixtures for unsupported percentages. |
| attr-010 | `136 (17%)` | `3622` | `17%` | 1395-1440 | 00:23.25-00:24.00 | transition into `cmd-raw-jp-adv5-012` | late juggle or start of SA3/CA family window | unresolved transition hit candidate | multi-stage exception, stacked modifier, character/move exception, super transition candidates | unknown | 0.16 | #174 already flagged `17%` as not explained by the simple global progression; #176 narrows it to the pre-super/super-start transition but not to a specific hit/action. | Review-only unresolved label; no contradiction proven. | Exact transition hit source, visual reference matching, and math reasoning fixtures. |
| attr-011 | `500 (50%)` | `4122` | `50%` | 1530-1560 | 00:25.50-00:26.00 | `cmd-raw-jp-adv5-012` | SA3/CA family (`jp_055_sa3_236236k` / `jp_056_ca_236236k`) | super/cinematic damage candidate | Super Art minimum guarantee, super-cancel, counting-unit candidates | partial | 0.45 | Label is inside the row 12 cinematic window and is plausibly related to the Super Art candidate family, but SA3 vs CA and exact hit source remain unresolved. | Review-only; not SA current damage/scaling authority. | SA3/CA disambiguation and hit segmentation. |
| attr-012 | `100 (50%)` | `4322` | `50%` | 1590-1620 | 00:26.50-00:27.00 | `cmd-raw-jp-adv5-012` | SA3/CA family | super/cinematic small-hit candidate | Super Art minimum guarantee / super multi-hit candidates | partial | 0.38 | Label is in the super/cinematic window but specific hit index is not isolated. | Review-only; not hit-by-hit current fact. | Super hit segmentation and damage-label stepping. |
| attr-013 | `100 (50%)` | `4422` | `50%` | 1635-1665 | 00:27.25-00:27.75 | `cmd-raw-jp-adv5-012` | SA3/CA family | super/cinematic small-hit candidate | Super Art minimum guarantee / super multi-hit candidates | partial | 0.38 | Label appears as another small 50% hit in the super/cinematic sequence; exact hit index remains unknown. | Review-only; not route authority. | Denser frame stepping through super sequence. |
| attr-014 | `100 (50%)` | `4522` | `50%` | 1680-1740 | 00:28.00-00:29.00 | `cmd-raw-jp-adv5-012` | SA3/CA family | super/cinematic small-hit candidate | Super Art minimum guarantee / super multi-hit candidates | partial | 0.34 | `4522` is present in prior sanitized reports, but #176 did not isolate this exact label in a separate sampled window; it remains associated with row 12 only at coarse level. | Review-only coarse attribution. | Denser frame stepping and super hit segmentation. |
| attr-015 | `1000 (50%)` | final `5622` | `50%` | 1800-1920 | 00:30.00-00:32.00 | `cmd-raw-jp-adv5-012` | SA3/CA family | final super/cinematic damage candidate | Super Art minimum guarantee / super-cancel candidates | partial | 0.50 | Final large label is inside the row 12 super/cinematic window and is the strongest row 12 attribution candidate, but exact SA3/CA identity and current value authority remain unresolved. | Review-only calibration evidence; not accepted current damage. | SA3/CA disambiguation and official/current authority path. |

No row is classified as fully `attributed` because the available sanitized evidence still does not isolate exact hit source, exact move execution, and exact frame event. No contradiction is proven.

## Candidate Hit/Action Sequence

| sequence_step | prompt_row | candidate move/action family | approximate frame window | nearby damage/scaling labels | confidence | ambiguity | Later reasoning use |
|---|---|---|---|---|---:|---|---|
| seq-001 | `cmd-raw-jp-adv5-001` | OD Veehat setup family | 195-240 | none isolated | 0.30 | setup row, variant unresolved | Context for first HP hit; not a damage source by itself. |
| seq-002 | `cmd-raw-jp-adv5-002` | `jp_005_5hp` candidate | 240-270 | `800 (100%)`, combo `800` | 0.54 | row 1 setup may contribute to state | Partial first damage attribution candidate. |
| seq-003 | `cmd-raw-jp-adv5-003` | `jp_009_2mp` candidate | 270-315 | damage remains around `800` | 0.25 | no isolated new label | Low-confidence sequence support only. |
| seq-004 | `cmd-raw-jp-adv5-004` | Veehat-set followup candidate | 315-375 | none isolated | 0.22 | setup-dependent row | Needs visual/action alignment. |
| seq-005 | `cmd-raw-jp-adv5-005` | `jp_015_j_mp` candidate | 375-435 | none isolated | 0.20 | jump context and hit source not isolated | Needs #179 visual matching. |
| seq-006 | `cmd-raw-jp-adv5-006` | `jp_068_parry_drive_rush` candidate | 420-510 | no direct label isolated | 0.30 | system action, timing unresolved | Modifier/context hypothesis only. |
| seq-007 | `cmd-raw-jp-adv5-007` | `jp_005_5hp` candidate | 450-510 | no new stable label | 0.24 | overlaps drive transition | Sequence support only. |
| seq-008 | `cmd-raw-jp-adv5-008` | `jp_035_236hp_stribog` candidate | 510-630 | no stable new label | 0.22 | visual effects and prior setup obscure source | Needs visual/action segmentation. |
| seq-009 | `cmd-raw-jp-adv5-009` | `jp_005_5hp` candidate | 570-660 | no stable new label | 0.20 | overlap with Stribog/Triglav effects | Needs #179 visual matching. |
| seq-010 | `cmd-raw-jp-adv5-010` | OD Triglav family | 630-900 | later ramp may be downstream | 0.24 | OD variant and hit source unresolved | Candidate context for late juggle labels. |
| seq-011 | `cmd-raw-jp-adv5-011` | `jp_034_236mp_stribog` candidate | 900-1170 | `600 (100%)`, `400 (80%)`, `420 (70%)`, combo `1400`/`1800`/`2220` | 0.38 | prior-row spillover likely | Partial late pre-super attribution candidate. |
| seq-012 | `cmd-raw-jp-adv5-012` | SA3/CA family | 1425-1935 | `500 (50%)`, repeated `100 (50%)`, final `1000 (50%)`, combo `5622` | 0.50 | SA3 vs CA unresolved, cinematic hides hit segmentation | Partial super/cinematic attribution candidate. |

This sequence is review-only. It can be used by later reasoning as a structured starting point, but it is not accepted move order, route validity, or frame data.

## Relation To SF6 Combo-Scaling Candidates

The loaded source-derived SF6 combo-scaling candidates helped classify the labels without overclaiming:

- `100%`, `80%`, and `70%` are useful anchors because they match values present in the source-derived global progression candidate.
- The candidate model made clear that hit count alone is unsafe; attribution needs move-kind/counting-unit evidence.
- Multi-hit and additional-input handling remain important because several labels occur in dense visual-effect windows and setup-dependent rows.
- Drive Rush/Parry Drive Rush context is relevant as a possible modifier context, but no label is strong enough to verify a rush modifier.
- `17%` remains interesting and unresolved. It is not explained by the simple loaded global sequence and may require stacked modifier, exception, UI semantic, or hit-source analysis.
- The `50%` labels remain potentially relevant to Super Art or minimum-guarantee behavior because they occur inside the row 12 super/cinematic window, but this does not prove SA minimum behavior or exact current values.
- No visible label proves a contradiction with the source-derived candidate model because the missing hit/move unit mapping prevents a strict test.

## What Improved Since #174

#174 could compare visible labels to source-derived combo-scaling candidates only abstractly. It correctly found that `100%`, `70%`, `17%`, and `50%` were useful or unresolved, but it lacked move/hit/frame structure.

#175 added sanitized command prompt rows and review-only move/system-action candidates. #176 added approximate frame/input/action/hit/damage-label windows on the 60 SF6 game-frame timeline.

#177 uses those two additional layers to narrow attribution:

- early `800 (100%)` now has a partial association with row 2 HP after row 1 OD Veehat setup;
- late `600/400/420` labels now have a partial association with the row 11 late juggle window;
- `408/126/210/272/125/136` are narrowed to the row 10/11 to row 12 transition but remain unknown;
- `500/100/1000 (50%)` labels now have partial association with row 12 SA3/CA family window.

The remaining uncertainty is narrower and more actionable for #178/#179 visual matching and #183 reasoning fixtures.

## What Still Cannot Be Claimed

- Current official damage values.
- Current official scaling percentages.
- Exact hit-by-hit route.
- Exact frame events, startup, active, recovery, hitstop, or hit advantage.
- Exact execution for ambiguous rows.
- Exact SA3 vs CA distinction.
- Exact OD Veehat or OD Triglav variant.
- Verification of Hameko-sourced candidate values as current SF6 facts.
- Public answer authority from this raw video.

## Failure Analysis

The attribution remains PARTIAL because:

- Labels in the mid-to-late juggle sequence are visually dense and not isolated to a single prompt row.
- Input-history clusters support broad ordering but not exact hit-source attribution.
- Damage labels can change during effects/cinematic states where the action source is not visible enough in the sanitized artifacts.
- `17%`, `25%`, `34%`, `42%`, and `51%` are not directly explained by the loaded simple global progression candidate.
- SA3/CA distinction remains unresolved; row 12 is a candidate family, not exact move identity.
- OD variants remain candidate families.
- The analysis used existing sanitized artifacts and did not reopen raw video, so no additional frame-level evidence was introduced.

#178/#179 may help by adding visual references and JP move matching for ambiguous action sources. #183 should cover reasoning classes where labels are visible but hit/move mapping, stacked modifiers, or authority boundaries are insufficient.

## Reusable Damage/Scaling Attribution Method

Future Codex/Hermes runs should be able to repeat this pass without chat history:

1. Load repo context first:
   - source-derived mechanics candidates;
   - prior calibration report;
   - command-prompt oracle;
   - frame/input alignment report;
   - raw-video observation and review notes.
2. Collect visible damage/combo labels and percentage/modifier labels from sanitized reports.
3. Collect command prompt rows and candidate action ids from the command-prompt oracle.
4. Collect frame/timestamp windows, input-history clusters, action phases, hit candidates, and damage-label windows from the alignment report.
5. Use the 60 SF6 game-frame timeline for system analysis and record source capture cadence as observation uncertainty.
6. Compare label windows to prompt/action/hit windows by overlap and sequence order.
7. Compare labels against source-derived combo-scaling candidates only as hypothesis context.
8. Classify each label as `attributed`, `partial`, `unknown`, `contradicted`, `not_applicable`, or `not_available`.
9. Record confidence, reason, authority boundary, and needed next evidence for each label.
10. Route unresolved visual/action identity to visual reference work and unresolved arithmetic/authority reasoning to fixtures.

### Next-Agent One-Shot Checklist

- Load #171/#173/#174/#175/#176 context from repo artifacts.
- Use the 60 SF6 game-frame timeline for attribution.
- Record source capture uncertainty separately.
- Map labels only when prompt/action/hit windows support the mapping.
- Treat source-derived combo-scaling candidates as review-only hypothesis context.
- Never accept current facts from video alone.
- Mark unsupported labels `unknown` or `partial`.
- Update follow-up routing after attribution.
- Do not commit raw media, frames, screenshots, OCR output, tool output, or private paths.

## Improvement Applied In This PR

This PR adds a reusable damage/scaling attribution report for `raw-video-training-mode-01` and a narrow workflow addition under `workflows/ingest-video.md` so later agents do not depend on one-off prompting.

The workflow addition records when to run attribution, what inputs must already exist, how to classify labels, and why results remain review-only unless a separate current-fact authority path verifies them.

No validator was added. This remains a concrete source-calibration workflow improvement rather than a repeated validator-worthy failure.

## Follow-Up Routing

| Follow-up | Status after #177 | Reason |
|---|---|---|
| #178 external visual atlas acquisition | still relevant | Ambiguous mid-route and super/cinematic action sources need visual references. |
| #179 JP move visual-reference matching | still relevant | Candidate prompt rows need visual matching before stronger move/hit attribution. |
| #183 SF6 system-mechanics math reasoning fixtures | still relevant | Labels such as `17%`, `42%`, `51%`, and repeated `50%` need reasoning fixtures that preserve insufficient-evidence boundaries. |

No new follow-up issue is needed.

## Terminal State

- damage/scaling attribution: PARTIAL
- visible labels covered: yes, every loaded label is partial or unknown
- review-only attribution evidence: yes
- accepted current fact: no
- curated knowledge: no
- generated references changed: no
- public runtime behavior changed: no
- #177 complete if this review-only attribution table is accepted

## Cleanup And Validation

| Check | Result |
|---|---|
| Raw media used? | no |
| Scratch cleanup | not applicable; no new scratch artifacts were created |
| Raw media committed? | no |
| Frames/screenshots/contact sheets committed? | no |
| Raw OCR/tool output committed? | no |
| Private paths committed? | no |
| Validators run | see PR body |
