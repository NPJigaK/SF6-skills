# Raw Video Command Prompt Normalization: raw-video-training-mode-01

## Report Metadata

| Field | Value |
|---|---|
| Issue | #175 |
| Parent issues | #155, #158, #170 |
| Related raw-video calibration | #170 / PR #173 |
| Related combo-scaling context follow-up | #174 / PR #182 |
| Related workflow fix | #180 / PR #181 |
| Date | 2026-05-14 |
| Source sample id | `raw-video-training-mode-01` |
| Raw media used? | yes, via maintainer-provided out-of-band local mapping only |
| Raw media committed? | no |
| Raw OCR committed? | no |
| Terminal state | command-prompt normalization PARTIAL + sanitized command prompt oracle + review-only move candidates |

This follow-up uses the raw-local source only to inspect the visible command-list
UI. It does not perform frame stepping, input-history/action alignment,
hit-by-hit damage/scaling attribution, external visual atlas acquisition, JP
move visual-reference matching, generated reference updates, or public runtime
behavior changes.

## Loaded Repo Context

This section implements the #180 `Pre-Analysis Repo Context Loading` gate before
command prompt normalization.

| Artifact path | Artifact type | Why it was loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-20260514.md` | calibration report | Provides the #173 first-pass oracle, visible source context, and prior command-prompt limitation. | Which UI regions and fields were already inspected; known residual gaps. | Canonical move names, exact move order, current route validity, or frame-accurate action timing. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-combo-scaling-context-20260514.md` | calibration report | Provides #174 damage/scaling comparison and explains why move/action mapping is required. | Why command prompt normalization is a prerequisite for later damage/scaling attribution. | Hit-by-hit scaling, accepted current damage facts, or final combo calculation. |
| `knowledge/evidence/video-observations/raw-video-training-mode-01.observations.md` | observation artifact | Provides sanitized source-local observations for the raw-local clip. | Character/context boundaries and source-local observation discipline. | Accepted roster facts, accepted combo route, exact move identity, current frame data, or damage authority. |
| `knowledge/review/unresolved/raw-video-training-mode-01.review.md` | review note | Provides review-only terminal decisions and follow-up routing for #170/#174. | Review boundary, promotion decision, and remaining execution gaps. | Accepted gameplay knowledge or public answer authority. |
| `knowledge/sources/videos/raw-video-training-mode-01.md` | sanitized source descriptor | Provides the local sample ID and private-path/media boundary. | Source identity, access boundary, and scratch policy. | Private path, raw media retention, exact move facts, or current-system authority. |
| `ingest/frame_data/config/registry/jp.moves.yaml` | move registry / binding metadata | Provides JP move IDs, groups, and icon-token patterns for candidate matching. | Mapping sanitized input-token rows to candidate move IDs. | Proof that the raw-video prompt row is that move, route validity, or public current-fact authority. |
| `skills/sf6-agent/assets/frame-current/published/jp/official_raw.json` | derived frame-current runtime asset from `data/exports/jp/official_raw.json` | Provides packaged JP move names and inputs for cross-checking candidate labels. | Candidate move names for already-visible input patterns. | Visual prompt interpretation, exact route correctness, or a new current-fact claim from the video. |
| `skills/sf6-agent/assets/frame-current/published/jp/supercombo_enrichment.json` | derived third-party enrichment asset | Provides alternate English move-name labels for JP move candidates. | Cross-labeling candidate move families such as Stribog, Departure, Triglav, and Interdiction. | Official/current authority or accepted route validation. |

Existing repo metadata can guide candidate matching. Raw-video prompt rows remain
calibration evidence only. Accepted authority is not created here. Hermes memory,
session history, local skills, Curator output, logs, and local state are
non-canonical.

## Source Access And Scratch Handling

| Field | Result |
|---|---|
| Raw local mapping used? | yes, through maintainer-provided out-of-band mapping only |
| Private path recorded? | no |
| Temporary targeted crops created? | yes, in repo-external scratch only |
| OCR attempted? | no |
| Manual visual inspection used? | yes, from temporary targeted command-list crops |
| Scratch cleanup status | completed before commit |
| Raw media committed? | no |
| Frames/screenshots/contact sheets committed? | no |
| Raw OCR/tool output committed? | no |

The report stores only sanitized text. No raw visual derivative is committed.

## Sanitized Command Prompt Oracle

Rows are recorded from the visible left-side combo-trial command-list UI. Button
icon descriptions are sanitized summaries from manual crop inspection; they are
not raw OCR output and not official input authority.

| prompt_row_id | visible_order | sanitized_prompt_text | input_icon_summary | button_strength_or_label | context_note | visible_confidence | source_basis | raw_visual_committed | notes |
|---|---:|---|---|---|---|---:|---|---|---|
| `cmd-raw-jp-adv5-001` | 1 | `214 + PP` | down, down-back, back, plus two punch icons | two punch icons / OD-like input | none visible | 0.86 | targeted command-list crop, early clip | no | Specific OD portal position or strength is not visible from the prompt row alone. |
| `cmd-raw-jp-adv5-002` | 2 | `HP` | heavy punch icon | `強` | none visible | 0.88 | targeted command-list crop | no | No direction icon is visible. |
| `cmd-raw-jp-adv5-003` | 3 | `2MP` | down plus medium punch icon | `中` | none visible | 0.85 | targeted command-list crop | no | Treated as crouching medium punch candidate. |
| `cmd-raw-jp-adv5-004` | 4 | `214 + MP` | down, down-back, back, plus medium punch icon | `中` | `ヴィーハト設置中に` | 0.82 | targeted command-list crop | no | Prompt explicitly depends on an existing Veehat/Departure setup state. |
| `cmd-raw-jp-adv5-005` | 5 | `j.MP` | medium punch icon while jumping | `中` | `ジャンプ中に` | 0.80 | targeted command-list crop | no | Jump context is visible; exact air-action timing is out of scope. |
| `cmd-raw-jp-adv5-006` | 6 | `66` | forward, forward | none | `ドライブパリィ中に` | 0.84 | targeted command-list crop | no | Treated as Drive Rush style system-action prompt, not a JP move. |
| `cmd-raw-jp-adv5-007` | 7 | `HP` | heavy punch icon | `強` | none visible | 0.84 | targeted command-list crop | no | Same sanitized token pattern as row 2. |
| `cmd-raw-jp-adv5-008` | 8 | `236HP` | down, down-forward, forward, plus heavy punch icon | `強` | none visible | 0.86 | targeted command-list crop | no | Candidate special input is visible; hit timing is not inferred. |
| `cmd-raw-jp-adv5-009` | 9 | `HP` | heavy punch icon | `強` | none visible | 0.82 | targeted command-list crop | no | Same sanitized token pattern as rows 2 and 7. |
| `cmd-raw-jp-adv5-010` | 10 | `22PP` | down, down, plus two punch icons | two punch icons / OD-like input | none visible | 0.84 | targeted command-list crop | no | Prompt does not distinguish which OD Triglav position is intended. |
| `cmd-raw-jp-adv5-011` | 11 | `236MP` | down, down-forward, forward, plus medium punch icon | `中` | none visible | 0.80 | targeted command-list crop | no | Button icon is read as medium punch; later visual-reference work may re-check the icon taxonomy. |
| `cmd-raw-jp-adv5-012` | 12 | `236236K` | down, down-forward, forward, down, down-forward, forward, plus kick icon | kick icon, super-art-like input | none visible | 0.78 | targeted command-list crop | no | Prompt cannot distinguish SA3 from CA without additional state/context. |

The success overlay echoes a completed prompt near the bottom of the UI, but it
is not counted as an additional command-list row because the main list already
contains the visible ordered prompt rows.

## Canonical Move Candidate Mapping

Candidate mapping uses visible input tokens plus JP move registry/frame-current
metadata. These are candidates only. They do not prove exact move identity,
route validity, or current-system authority for the raw video.

| prompt_row_id | sanitized_prompt | candidate_move_name | candidate_move_slug_or_id | source_for_candidate | confidence | match_basis | ambiguity | authority_boundary |
|---|---|---|---|---|---:|---|---|---|
| `cmd-raw-jp-adv5-001` | `214 + PP` | `OD 弱/中/強 ヴィーハト` / `OD Departure` family | `jp_040_214pp_vihat_od_weak`; `jp_041_214pp_vihat_od_medium`; `jp_042_214pp_vihat_od_heavy` | `jp.moves.yaml`; `official_raw.json`; `supercombo_enrichment.json` | 0.72 | input token `214PP` matches OD Veehat/Departure rows. | Prompt row does not show which OD portal position/strength variant is intended. | Review-only candidate; not accepted exact move identity. |
| `cmd-raw-jp-adv5-002` | `HP` | `立ち強P（キンターヴル）` | `jp_005_5hp` | `jp.moves.yaml`; `official_raw.json` | 0.74 | standalone heavy punch prompt with no direction. | Visual prompt cannot prove standing-vs-contextual interpretation beyond no direction shown. | Review-only candidate. |
| `cmd-raw-jp-adv5-003` | `2MP` | `しゃがみ中P（ズミヤー）` | `jp_009_2mp` | `jp.moves.yaml`; `official_raw.json` | 0.78 | down plus medium punch prompt matches crouching medium punch. | Button-icon taxonomy is manual visual interpretation. | Review-only candidate. |
| `cmd-raw-jp-adv5-004` | `214 + MP` while Veehat is set | `ヴィーハト・アクノ` / `Departure: Window` family | `jp_043_214lpmp_vihat_akno` | `jp.moves.yaml`; `official_raw.json`; `supercombo_enrichment.json` | 0.68 | context text says Veehat is set; `214MP` fits the LP/MP follow-up candidate row. | The prompt depends on portal/setup state and does not prove the exact follow-up behavior. | Review-only candidate. |
| `cmd-raw-jp-adv5-005` | `j.MP` | `ジャンプ中P（ローシャッチ）` | `jp_015_j_mp` | `jp.moves.yaml`; `official_raw.json` | 0.70 | jump context plus medium punch prompt. | Manual icon reading; no frame/action alignment. | Review-only candidate. |
| `cmd-raw-jp-adv5-006` | `66` during Drive Parry | Drive Rush / forward dash from parry context | no JP move id; system-action prompt | command-list prompt text; workflow boundary | 0.72 | context text says during Drive Parry and shows forward, forward. | Repo frame-current JP move registry is not the right authority surface for system action prompts. | Calibration prompt only; not an accepted system-action fact. |
| `cmd-raw-jp-adv5-007` | `HP` | `立ち強P（キンターヴル）` | `jp_005_5hp` | `jp.moves.yaml`; `official_raw.json` | 0.72 | standalone heavy punch prompt with no direction. | Same ambiguity as row 2. | Review-only candidate. |
| `cmd-raw-jp-adv5-008` | `236HP` | `強 ストリボーグ` / `Stribog` | `jp_035_236hp_stribog` | `jp.moves.yaml`; `official_raw.json`; `supercombo_enrichment.json` | 0.80 | input token `236HP` matches JP heavy Stribog row. | Does not prove hit/contact timing or whether this action connected. | Review-only candidate. |
| `cmd-raw-jp-adv5-009` | `HP` | `立ち強P（キンターヴル）` | `jp_005_5hp` | `jp.moves.yaml`; `official_raw.json` | 0.70 | standalone heavy punch prompt with no direction. | Same ambiguity as rows 2 and 7. | Review-only candidate. |
| `cmd-raw-jp-adv5-010` | `22PP` | `OD 弱/中/強 トリグラフ` / `OD Triglav` family | `jp_030_22pp_triglav_od_weak`; `jp_031_22pp_triglav_od_medium`; `jp_032_22pp_triglav_od_heavy` | `jp.moves.yaml`; `official_raw.json`; `supercombo_enrichment.json` | 0.74 | input token `22PP` matches OD Triglav family rows. | Prompt does not identify spike position/variant. | Review-only candidate. |
| `cmd-raw-jp-adv5-011` | `236MP` | `中 ストリボーグ` / `Stribog` | `jp_034_236mp_stribog` | `jp.moves.yaml`; `official_raw.json`; `supercombo_enrichment.json` | 0.68 | input token appears to be `236MP`. | Medium punch icon reading should be re-checked during #176/#179 if it becomes attribution-critical. | Review-only candidate. |
| `cmd-raw-jp-adv5-012` | `236236K` | `SA3 ザプリェット` / `CA ザプリェット`; `Interdiction` / `Interdiction (CA)` | `jp_055_sa3_236236k`; `jp_056_ca_236236k` | `jp.moves.yaml`; `official_raw.json`; `supercombo_enrichment.json` | 0.66 | double quarter-circle-forward plus kick prompt matches JP SA3/CA input rows. | Prompt alone does not distinguish SA3 from CA or prove super-art state. | Review-only candidate. |

## Unmapped / Ambiguous Prompts

| Prompt / area | Status | Reason | Needed evidence |
|---|---|---|---|
| OD Veehat/Departure variant in row 1 | ambiguous | `214PP` maps to multiple OD Veehat/Departure variants in the registry; the command-list row does not expose portal distance/strength selection. | #176 frame/input alignment or maintainer/oracle confirmation. |
| Veehat-set follow-up in row 4 | candidate only | Context text is visible, but the row depends on prior portal state and may require route-specific interpretation. | #176 timing plus #179 visual-reference matching if needed. |
| Drive Parry context row 6 | system-action prompt, not JP move id | JP move registry is not designed for Drive Rush/system-action prompt rows. | Later system-action representation if #176/#177 need it. |
| OD Triglav variant in row 10 | ambiguous | `22PP` maps to multiple OD Triglav variants. | #176 input/action alignment and visible spike position. |
| SA3 vs CA in row 12 | ambiguous | `236236K` maps to both SA3 and CA candidate rows. | Health/resource state and UI context, or official trial answer key. |
| Success-overlay prompt echo | excluded from ordered list | It appears as post-completion UI echo rather than a separate ordered command-list row. | Dense UI-state review only if later issues need it. |

#178/#179 visual references may help confirm action identity, especially where
the prompt row is ambiguous or visually occluded. #176 frame/input alignment is
needed before the candidate list can be used as exact move order in damage or
scaling attribution.

## Prediction / Oracle Impact

Before #175, #173 recorded that the command prompt structure existed but did not
preserve a row-level command oracle. #174 then showed that damage/scaling labels
could not be interpreted without move/action-unit mapping.

After #175, the repo has:

- a sanitized ordered command-prompt oracle for the visible `上級 5` JP
  combo-trial UI;
- candidate move IDs for rows whose input patterns match existing JP
  registry/frame-current metadata;
- explicit held rows for ambiguous OD variants, Drive Rush/system-action
  context, and SA3/CA ambiguity.

The remaining blocker for #176/#177 is not the absence of command-prompt rows;
it is alignment: the rows must still be tied to frame ranges, input-history
changes, hit events, and damage-label changes.

## Failure Analysis

| Failure / uncertainty | Why it remains | Impact |
|---|---|---|
| No accepted canonical move order | Command-list rows are visible, but the row-to-action execution timing is not aligned. | #176 must align prompt rows to frame/input/action segments. |
| OD variant ambiguity | Several JP OD prompts use shared input tokens with variant choice determined by button combination, portal/spike position, or route context. | Candidate mapping can identify a move family but not a single accepted variant. |
| System-action row is outside JP move registry | Drive Rush from Drive Parry context is not a character move row in the JP registry. | Needs separate representation if #176/#177 consume it. |
| Button-icon taxonomy is manually inspected | No raw OCR output or screenshot is committed; icon interpretation is sanitized. | Confidence is bounded and must be rechecked if attribution depends on a row. |
| Prompt rows are not official route authority | Combo-trial UI shows a prompt sequence, but this PR does not verify current route validity or exact hit behavior. | No accepted current facts or public runtime behavior are created. |

## Follow-Up Routing

| Follow-up issue | Routing from #175 |
|---|---|
| #176 | Use the sanitized command-prompt oracle to align prompt rows with frame ranges, input-history changes, action phases, and hit events. |
| #177 | Use #175 prompt candidates plus #176 alignment to attribute visible damage/scaling labels to hit/action candidates. |
| #178 | Build repo-external visual atlas acquisition before relying on visual references for ambiguous move/action identity. |
| #179 | Use visual references to re-check JP move/action candidate matches, especially OD variants and visually occluded segments. |
| #183 | Add SF6 system-mechanics math reasoning fixtures after #177 has stronger hit/action attribution examples. |

## Terminal State

| State | Result | Reason |
|---|---|---|
| command-prompt normalization PASS / PARTIAL / FAIL | PARTIAL | Ordered sanitized prompt rows were created and many rows map to candidate JP move families, but several rows remain ambiguous and none become accepted current facts. |
| sanitized command prompt oracle | yes | Row-level prompt text is preserved without raw visual artifacts. |
| canonical move candidates | partial | Candidate IDs are recorded where input tokens match existing JP metadata; ambiguous rows are held. |
| accepted current fact | no | Prompt rows and candidate mappings are calibration evidence only. |
| curated knowledge | no | This PR adds no stable concept and no curated surface. |
| generated references | no | Public generated references and `sf6-agent` behavior are unchanged. |

#175 is complete if this review-only command prompt oracle is accepted:
sanitized prompt rows were extracted, candidate mappings were produced where
possible, ambiguity was recorded, and #176/#177 now have structured input for
their follow-up work.

## Cleanup And Validation

| Check | Result |
|---|---|
| Raw media used | yes, via out-of-band local mapping only |
| Scratch cleanup | completed before commit |
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
