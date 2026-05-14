# Knowledge Ingest E2E Tranche 1 Available Inputs 20260514

## Report Metadata

| Field | Value |
|---|---|
| Report id | `knowledge-ingest-e2e-tranche-1-available-inputs-20260514` |
| Date | 2026-05-14 |
| Timezone | Asia/Tokyo |
| Related issues | #155, #158 |
| Branch | `v2.5/e2e-ingest-tranche-1` |
| Tranche | Tranche 1 available-input execution |
| Report type | `knowledge_ingest_e2e_execution_ledger` |
| Execution policy | execution-first validation for provided rows only |
| HOLD policy | `HOLD_INPUT_UNAVAILABLE` rows are listed but not processed or counted as proof |

## Scope

This tranche executed only the #158 rows marked ready in the input completion
update:

- A3 `article-live-japanese-01`
- D1 `video-link-gameplay-only-01`
- D2 `video-link-gameplay-commentary-01`
- D3 `video-link-livestream-overlay-01`
- D4 `video-link-vertical-short-01`
- D6 `video-link-clip-compilation-01`
- D6b `video-link-clip-compilation-02`
- D7 `video-link-training-mode-01`
- D8 `video-link-commentary-only-01`
- D9 `video-link-unknown-mixed-01`
- E7 `raw-video-training-mode-01`

This tranche did not implement #153 or #156. It did not create a matrix-only
PR, run Hermes, change public `sf6-agent` behavior, change `official_raw`,
implement move recognition, or implement move-frequency analytics.

## Input Completion Summary

| Input group | Tranche 1 status | Notes |
|---|---|---|
| Article URL live-fetch inputs | partial | A3 executed; A1/A2 remain HOLD. |
| Article URL with maintainer context inputs | HOLD | B1/B2/B3 remain unavailable and unprocessed. |
| Local article/note inputs | HOLD | C1/C2/C3 remain unavailable and unprocessed. |
| YouTube/video link inputs | partial | D1-D4, D6, D6b, D7-D9 executed; D5 remains HOLD. |
| Raw local video inputs | partial | E7 executed; E1-E6/E8/E9 remain HOLD. |

Maintainer confirmation from #158: the provided article/video URLs are open
public sources with an acceptable basis for bounded maintainer-local review.
This report does not make independent legal conclusions and does not authorize
committing raw media, raw article bodies, transcripts, frames, screenshots,
contact sheets, raw tool output, logs, cache, credentials, cookies, browser
state, or local state.

## Execution Depth Summary

This PR is partial Tranche 1 execution. It does not prove all-pattern
knowledge ingest E2E. Each row is classified by the deepest execution actually
performed in this PR or inherited from already-merged artifacts.

| Row | Depth classification | Terminal-state proof boundary |
|---|---|---|
| A3 | `fresh_content_execution_performed`; `existing_claim_review_reuse` | Fresh bounded article content review was performed without storing the article body. Existing source/claim/review artifacts remain the terminal path, with numeric and exception claims held as `needs_review`. This does not create new accepted curated knowledge. |
| D1 | `metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from #137, not newly performed here. |
| D2 | `metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from #137, not newly performed here. |
| D3 | `metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from #137, not newly performed here. |
| D4 | `metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from #137, not newly performed here. |
| D6 | `metadata_access_only`; `existing_artifact_reuse` | Existing source and observation artifacts are reused; no new content review occurred here. |
| D6b | `metadata_access_only`; `metadata_only_source_artifact_created`; `content_execution_not_performed`; `terminal_state_not_proven` | Proves metadata-only source artifact creation only. It does not prove clipped video-content review or matchup/counterplay claims. |
| D7 | `metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from #137, not newly performed here. |
| D8 | `metadata_access_only`; `metadata_only_source_artifact_created`; `content_execution_not_performed`; `terminal_state_not_proven` | No-download title/description/chapter-outline review confirmed this is a terminology/commentary source, but definition-level content review would require video, caption, transcript, or audio access. That content execution is HOLD. |
| D9 | `metadata_access_only`; `metadata_only_source_artifact_created`; `content_execution_not_performed`; `terminal_state_not_proven` | Proves metadata-only source artifact creation only. It does not prove unknown/mixed content classification, frame-advantage routing, or current-fact review. |
| E7 | `raw_local_bounded_review_performed` | Actual raw-local bounded review was performed through `ffprobe` and scratch-only contact-sheet inspection; raw media and private paths were not committed. |

## Execution Methods

| Method | Used for | Result | Repo boundary |
|---|---|---|---|
| Bounded no-cookie article content review | A3 | HTTP 200 HTML access succeeded; article content was reviewed only at paraphrased category level and existing source/claim/review artifacts were rechecked. | No full article body, raw HTML, raw article images, or long verbatim excerpt stored. |
| `yt-dlp --skip-download` metadata access | D1-D4, D6, D6b, D7-D9 | All ready video-link rows returned title, duration, channel, and canonical URL metadata without downloading media. | No video, subtitles, thumbnails, info JSON, or transcript files were written to the repo. |
| Existing bounded review reuse | D1-D4, D7 | Existing #137 source artifacts and `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md` were reused. No new video-content review was performed for these rows in this PR. | Existing review-only boundaries preserved. |
| Existing source/observation artifact reuse | D6 | Existing metadata-only source and review-only observation artifacts were reused. No new video-content review was performed for this row in this PR. | Existing review-only boundaries preserved. |
| New metadata-only video source artifacts | D6b, D8, D9 | Three missing source artifacts were added. | Metadata-only; no raw media or transcript. |
| D8 no-download description/chapter-outline review | D8 | The title, description, and chapter outline were reviewed from no-download metadata. Definition-level content review was not performed because it would require transcript/caption/video/audio access outside this fix's safe boundary. | No captions, transcript, video, audio, frames, screenshots, or contact sheets were downloaded or committed. |
| `ffprobe` raw local video check | E7 | Maintainer-local file was available and probed outside the repo. | Private absolute path is not recorded in repo artifacts. |
| Scratch-only contact sheet review | E7 | A temporary contact sheet confirmed training/combo-trial visual context. | Scratch directory was deleted before commit; no images committed. |

## Execution Depth And Proof Scope

| Row | Execution depth | Proof scope |
|---|---|---|
| A3 | `fresh_content_execution_performed`; `existing_claim_review_reuse` | Proves bounded article content review plus the existing source/claim/review artifact path ending in `needs_review`. It does not prove a new accepted curated promotion. |
| D1 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D2 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D3 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D4 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D6 | `live_metadata_access_only`; `existing_artifact_reuse`; `bounded_content_review_not_performed` | Reuses existing source and review-only observation artifacts. No new video-content review occurred in this PR. |
| D6b | `live_metadata_access_only`; `metadata_only_source_artifact_created`; `bounded_content_review_not_performed` | Proves metadata-only source artifact creation. It does not prove clipped video-content review or matchup/counterplay validity. |
| D7 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D8 | `live_metadata_access_only`; `metadata_only_source_artifact_created`; `bounded_content_review_not_performed`; `content_execution_not_performed`; `terminal_state_not_proven` | Proves metadata-only source artifact creation and no-download source-outline review. Definition-level terminology content review remains HOLD because this PR did not download or commit video, captions, transcripts, audio, or frames. |
| D9 | `live_metadata_access_only`; `metadata_only_source_artifact_created`; `bounded_content_review_not_performed` | Proves metadata-only source artifact creation. It does not prove unknown/mixed video-content classification, exact frame-advantage routing, or current-fact review. |
| E7 | `raw_local_bounded_review_performed` | Proves actual bounded raw-local review of the provided local sample through `ffprobe` and scratch-only contact sheet review; raw media and private path were not committed. |

## Fresh Content Execution Notes

### A3 Article Content Review

The A3 article was accessed through public no-cookie HTML and reviewed only at a
bounded, paraphrased category level. The raw HTML and article body were not
stored in the repo.

The fresh review confirmed that the existing artifacts still model the source
correctly:

- `knowledge/sources/articles/hameko-2023-combo-scaling.md` records the source
  as a Japanese community article about combo-scaling mechanics.
- `knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md` separates a
  stable concept candidate from patch-sensitive numeric, system-action,
  character-specific, move-specific, and control-scheme exception categories.
- `knowledge/review/unresolved/hameko-2023-combo-scaling.review.md` keeps those
  numeric and exception categories in `needs_review`.
- `knowledge/curated/mechanics/combo-scaling.md` already contains a reviewed
  stable concept page, but this PR did not create or newly accept curated
  knowledge.

No exact scaling percentages, move-specific values, character-specific current
exceptions, or current-system formulas were copied into this ledger.

### D8 Commentary Content Attempt

D8 was reviewed only through no-download title, description, and chapter-outline
metadata. That material was enough to classify the source as a Japanese
fighting-game terminology/commentary source, but not enough to review the actual
definitions.

Definition-level content review would require video, audio, captions, or
transcript access. This fix does not download or commit those materials, so D8
content execution remains HOLD and does not count as terminology knowledge
proof.

### E7 Raw-Local Video Observation Summary

E7 used the maintainer-provided local raw video sample outside the repository.
The repo records only the sanitized sample id `raw-video-training-mode-01`.

Safe observations from the bounded review:

- The sample is a local Street Fighter 6 training/combo-trial style recording.
- The visible context is consistent with JP combo-trial practice rather than a
  public match, article, or accepted knowledge source.
- It is useful as raw-local-video handling proof and sanitized observation/report
  proof.

What was not inferred:

- no exact current facts
- no exact frame data
- no move recognition
- no combo validity conclusion
- no accepted strategy or coaching conclusion
- no public `sf6-agent` behavior readiness

## Executed Rows

| Row | Sample ID | Input family | Workflow used | Execution attempted? | Terminal status | Terminal state | Artifacts created or reused | Why terminal state is correct |
|---|---|---|---|---:|---|---|---|---|
| A3 | `article-live-japanese-01` | Article URL live fetch/extraction | `workflows/ingest-article.md`, `workflows/review-claims.md` | yes | PASS | unresolved / needs_review with fresh bounded content review | Reused `knowledge/sources/articles/hameko-2023-combo-scaling.md`, `knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md`, and `knowledge/review/unresolved/hameko-2023-combo-scaling.review.md`; this ledger and review note add 2026-05-14 content execution evidence. | Fresh bounded article review confirmed the existing split between stable concept, current-fact-like numeric categories, and review-only exceptions. No new curated acceptance occurred and concrete scaling values remain unaccepted. |
| D1 | `video-link-gameplay-only-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-paa8pnlequa.md` and `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md`. | No-download metadata access succeeded. Content-review proof comes from the existing #137 bounded review, not from new content review in this PR. |
| D2 | `video-link-gameplay-commentary-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-6vmm2sdtoak.md` and the #137 report. | Commentary and coaching boundaries are supported by existing #137 review; no new transcript or content review was created in this PR. |
| D3 | `video-link-livestream-overlay-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-ztqbhcrtsnc.md` and the #137 report. | Overlay/webcam/layout boundaries are supported by existing #137 review; no new content review occurred in this PR. |
| D4 | `video-link-vertical-short-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-shorts-aylextw2jic.md` and the #137 report. | Short-form crop/subtitle limitations are supported by existing #137 review; no new content review occurred in this PR. |
| D6 | `video-link-clip-compilation-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | sanitized report only via existing artifact reuse | Reused `knowledge/sources/videos/youtube-nyfngnzjv3m.md` and existing review-only observation artifact `knowledge/evidence/video-observations/youtube-nyfngnzjv3m-jp-combos.observations.md`. | Existing source and observation artifacts remain review-only and keep observed damage labels out of current-fact authority. No new video-content review occurred in this PR. |
| D6b | `video-link-clip-compilation-02` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | metadata-only source artifact only | Added `knowledge/sources/videos/youtube-pfxq7gifuqa.md`; no bounded content review was performed. | This proves metadata-only source artifact creation. Matchup/counterplay conclusions remain future claim-review holds and are not content-review proof. |
| D7 | `video-link-training-mode-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-hwradk0bero.md` and the #137 report. | Training-mode/coaching boundaries are supported by existing #137 review; no new content review occurred in this PR. |
| D8 | `video-link-commentary-only-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS for metadata; HOLD for content execution | metadata-only source artifact only / content execution HOLD | Added `knowledge/sources/videos/youtube-vcpzwawrrla.md`; title, description, and chapter outline were reviewed without downloading media or transcripts. | This proves metadata-only source artifact creation and source-outline classification. It does not prove terminology definition review because transcript/caption/video/audio content was not accessed. |
| D9 | `video-link-unknown-mixed-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | metadata-only source artifact only | Added `knowledge/sources/videos/youtube-ryxbclscdsw.md`; no bounded content review was performed. | This proves metadata-only source artifact creation. Unknown/mixed content classification and exact frame-advantage/current-fact routing remain unproven until future bounded content review. |
| E7 | `raw-video-training-mode-01` | Raw local video | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | sanitized report only | This ledger only. No source URL or private local path artifact was created. | The maintainer-local file was available, basic video metadata was probed, and a scratch-only contact sheet confirmed training/combo-trial context. The private path, raw media, frames, and contact sheet were not committed. |

## Held Rows

| Row | Sample ID | Terminal status | Reason |
|---|---|---|---|
| A1 | `article-live-official-currentfact-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| A2 | `article-live-community-strategy-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| B1 | `article-context-maintained-third-party-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| B2 | `article-context-community-strategy-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| B3 | `article-context-unknown-ambiguous-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| C1 | `local-note-maintainer-note-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| C2 | `local-note-currentfact-like-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| C3 | `local-note-ambiguous-unsupported-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe real input available. |
| D5 | `video-link-subtitle-overlay-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no dedicated subtitle-overlay sample available. |
| E1 | `raw-video-gameplay-only-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |
| E2 | `raw-video-gameplay-commentary-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |
| E3 | `raw-video-livestream-overlay-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |
| E4 | `raw-video-vertical-short-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |
| E5 | `raw-video-subtitle-overlay-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |
| E6 | `raw-video-clip-compilation-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |
| E8 | `raw-video-commentary-only-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |
| E9 | `raw-video-unknown-mixed-01` | HOLD | `HOLD_INPUT_UNAVAILABLE`; no safe raw local sample available. |

Held rows were not executed and must not be counted as proof for #155 or #158.

## Forbidden Artifact Check

| Row group | Raw media committed? | Transcript/captions committed? | Raw article body committed? | Local state/cache committed? | Notes |
|---|---:|---:|---:|---:|---|
| A3 | no | no | no | no | Live fetch was bounded to metadata/verification; existing artifacts store only summaries and review candidates. |
| D1-D4, D6, D6b, D7-D9 | no | no | n/a | no | Video execution used no-download metadata access; no subtitles, thumbnails, info JSON, logs, or cache artifacts were committed. |
| E7 | no | no | n/a | no | Raw local video stayed outside the repo; temporary scratch contact sheet was deleted before commit. |
| HOLD rows | no | no | no | no | HOLD rows were not processed. |

## Authority Boundaries Per Row

| Row group | Boundary |
|---|---|
| A3 | Existing claims remain `needs_review`; exact scaling values and character/move/control-scheme exceptions are not accepted into curated knowledge. |
| D1 | Gameplay visibility does not create accepted player-status, matchup, move-recognition, frame-data, or current-system facts. |
| D2/D3/D7 | Commentary, coaching, and playstyle claims remain source-local review input based on existing bounded review reuse. |
| D4 | Vertical/short-form visual context is useful for sanitized reporting only; crop/subtitle limitations reduce observation confidence. |
| D6 | Existing observed damage labels remain review/eval context only, not current-system authority. |
| D6b | Only metadata was reviewed in this PR. Matchup/counterplay conclusions from clipped context require later bounded content review and claim review. |
| D8 | Only title/description/chapter-outline metadata was reviewed in this PR. Terminology definitions require later bounded content review and article-like claim review before curated promotion. |
| D9 | Only metadata was reviewed in this PR. Unknown/mixed content classification, frame-advantage routing, and current-fact review remain unproven until later bounded content review. |
| E7 | Training UI and combo-trial observations are not current facts; no exact move properties or frame data were inferred. |

## Terminal-State Coverage Summary

| Terminal state | Tranche 1 result | Evidence |
|---|---|---|
| accepted stable curated knowledge | not newly proven / existing artifact only | `knowledge/curated/mechanics/combo-scaling.md` already exists, but this PR did not create or newly accept curated knowledge. |
| accepted strategy/concept knowledge | not newly proven / needs_review | A3 fresh content review supports the existing concept/current-fact split, but no new strategy or concept claim was accepted in this PR. |
| current-fact authority route | partial hold only | A3 encountered current-fact-like numeric and exception categories and kept them out of curated knowledge, but this tranche did not update a current-fact authority surface. |
| review-only hold | proven by existing bounded review reuse and actual raw-local review | D2, D3, D4, and D7 reuse #137 bounded review; E7 performed actual bounded raw-local review. D6b/D8/D9 are not counted as content-review proof. |
| rejected unsafe | not proven / HOLD | B3/C3 were unavailable and no executed row produced a rejected unsafe candidate. |
| unresolved / needs_review | proven | A3 performed fresh bounded content review and reused existing source/claim/review artifacts with `needs_review` status. |
| sanitized report only | proven by existing report/artifact reuse and actual E7 review | D1-D4 and D7 reuse the #137 report; D6 reuses existing source/observation artifacts; E7 performed actual bounded raw-local review. D6b/D9 are not counted as video-content report proof. |
| metadata-only source artifact only | proven | D6b, D8, and D9 added metadata-only source artifacts and did not create claim or observation artifacts. |

This tranche does not complete #155. It proves only the terminal states
demonstrated above for the provided rows.

## Unresolved Gaps And Residual Tasks

- D5 subtitle-overlay video-link coverage remains HOLD.
- Full article live-fetch/extraction remains only partially proven; A3 performed
  bounded live content review, but did not store a full article extraction or
  create a new accepted curated artifact.
- D6b/D8/D9 bounded video content review remains not proven; these rows prove
  metadata-only source artifact creation only.
- D8 terminology definition review remains HOLD because this PR did not download
  or commit video, captions, transcript, audio, frames, screenshots, or contact
  sheets.
- Unknown/mixed video-content classification remains not proven for D9 unless
  future bounded content review is performed.
- All article URL with maintainer-provided context rows remain HOLD.
- All local article/note rows remain HOLD.
- All raw local video formats except E7 remain HOLD.
- Accepted stable curated knowledge, accepted strategy/concept knowledge,
  rejected unsafe, and a full current-fact authority route remain unproven in
  this tranche.
- No public `sf6-agent` behavior changed.

## Cleanup And Verification

| Check | Result |
|---|---|
| A3 raw article body cleanup | no raw article body was written to repo. |
| Video raw media cleanup | no video media was downloaded for video-link rows. |
| E7 scratch cleanup | temporary contact sheet directory was deleted before commit. |
| Private local paths | not recorded in repo artifacts. |
| Raw `yt-dlp` output | not committed. |
| Hermes output/local state | not used or committed. |
| Credentials/cookies/secrets | not used or committed. |
| `validate-no-video-binary-assets.ps1` | PASS: `No video binary assets OK`. |
| `run-all.ps1` | PASS: `V2 validation suite OK`; PowerShell emitted git-unavailable warnings during derived-output status checks, so a git-visible residual diff check was run. |
| `git diff --check` | PASS: no whitespace errors. |
| `git diff --check origin/main...HEAD` | PASS after commit check; no whitespace errors. |
| Raw/local-state scan | PASS: scan reported expected pre-existing Hermes-named docs, packs, workflows, and validators only; no new raw media, transcript, local state, cache, credential, or external binary artifacts were found. |
| Generated-surface residual diff check | PASS: no residual diffs in `.dist`, generated references, frame-current assets, normalization assets, `data/raw`, `data/normalized`, or `data/exports`. |
