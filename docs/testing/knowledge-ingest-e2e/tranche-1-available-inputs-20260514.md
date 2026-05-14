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

## Execution Methods

| Method | Used for | Result | Repo boundary |
|---|---|---|---|
| Bounded no-cookie article metadata/access check | A3 | HTTP 200 HTML access succeeded; only metadata and existing repo artifacts were used in this report. Fresh full live extraction was not performed. | No full article body or long verbatim excerpt stored. |
| `yt-dlp --skip-download` metadata access | D1-D4, D6, D6b, D7-D9 | All ready video-link rows returned title, duration, channel, and canonical URL metadata without downloading media. | No video, subtitles, thumbnails, info JSON, or transcript files were written to the repo. |
| Existing bounded review reuse | D1-D4, D7 | Existing #137 source artifacts and `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md` were reused. No new video-content review was performed for these rows in this PR. | Existing review-only boundaries preserved. |
| Existing source/observation artifact reuse | D6 | Existing metadata-only source and review-only observation artifacts were reused. No new video-content review was performed for this row in this PR. | Existing review-only boundaries preserved. |
| New metadata-only video source artifacts | D6b, D8, D9 | Three missing source artifacts were added. | Metadata-only; no raw media or transcript. |
| `ffprobe` raw local video check | E7 | Maintainer-local file was available and probed outside the repo. | Private absolute path is not recorded in repo artifacts. |
| Scratch-only contact sheet review | E7 | A temporary contact sheet confirmed training/combo-trial visual context. | Scratch directory was deleted before commit; no images committed. |

## Execution Depth And Proof Scope

| Row | Execution depth | Proof scope |
|---|---|---|
| A3 | `live_metadata_access_only`; `existing_artifact_reuse`; `fresh_live_extraction_not_performed` | Proves only current access plus the existing source/claim/review artifact path ending in `needs_review`. It does not prove full article URL live-fetch/extraction E2E. |
| D1 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D2 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D3 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D4 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D6 | `live_metadata_access_only`; `existing_artifact_reuse`; `bounded_content_review_not_performed` | Reuses existing source and review-only observation artifacts. No new video-content review occurred in this PR. |
| D6b | `live_metadata_access_only`; `metadata_only_source_artifact_created`; `bounded_content_review_not_performed` | Proves metadata-only source artifact creation. It does not prove clipped video-content review or matchup/counterplay validity. |
| D7 | `live_metadata_access_only`; `existing_bounded_review_reuse` | Content-review proof is inherited from the existing #137 bounded review report and source artifact, not newly performed in this PR. |
| D8 | `live_metadata_access_only`; `metadata_only_source_artifact_created`; `bounded_content_review_not_performed` | Proves metadata-only source artifact creation for a commentary/terminology source. It does not prove terminology content review. |
| D9 | `live_metadata_access_only`; `metadata_only_source_artifact_created`; `bounded_content_review_not_performed` | Proves metadata-only source artifact creation. It does not prove unknown/mixed video-content classification, exact frame-advantage routing, or current-fact review. |
| E7 | `raw_local_bounded_review_performed` | Proves actual bounded raw-local review of the provided local sample through `ffprobe` and scratch-only contact sheet review; raw media and private path were not committed. |

## Executed Rows

| Row | Sample ID | Input family | Workflow used | Execution attempted? | Terminal status | Terminal state | Artifacts created or reused | Why terminal state is correct |
|---|---|---|---|---:|---|---|---|---|
| A3 | `article-live-japanese-01` | Article URL live fetch/extraction | `workflows/ingest-article.md`, `workflows/review-claims.md` | yes | PASS | unresolved / needs_review | Reused `knowledge/sources/articles/hameko-2023-combo-scaling.md`, `knowledge/evidence/claims/hameko-2023-combo-scaling.claims.md`, and `knowledge/review/unresolved/hameko-2023-combo-scaling.review.md`; this ledger added current access verification. | The source/claim/review path already exists and remains review-only. Live metadata access succeeded, but fresh full live extraction was not performed and concrete scaling values remain unaccepted. |
| D1 | `video-link-gameplay-only-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-paa8pnlequa.md` and `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md`. | No-download metadata access succeeded. Content-review proof comes from the existing #137 bounded review, not from new content review in this PR. |
| D2 | `video-link-gameplay-commentary-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-6vmm2sdtoak.md` and the #137 report. | Commentary and coaching boundaries are supported by existing #137 review; no new transcript or content review was created in this PR. |
| D3 | `video-link-livestream-overlay-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-ztqbhcrtsnc.md` and the #137 report. | Overlay/webcam/layout boundaries are supported by existing #137 review; no new content review occurred in this PR. |
| D4 | `video-link-vertical-short-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-shorts-aylextw2jic.md` and the #137 report. | Short-form crop/subtitle limitations are supported by existing #137 review; no new content review occurred in this PR. |
| D6 | `video-link-clip-compilation-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | sanitized report only via existing artifact reuse | Reused `knowledge/sources/videos/youtube-nyfngnzjv3m.md` and existing review-only observation artifact `knowledge/evidence/video-observations/youtube-nyfngnzjv3m-jp-combos.observations.md`. | Existing source and observation artifacts remain review-only and keep observed damage labels out of current-fact authority. No new video-content review occurred in this PR. |
| D6b | `video-link-clip-compilation-02` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | metadata-only source artifact only | Added `knowledge/sources/videos/youtube-pfxq7gifuqa.md`; no bounded content review was performed. | This proves metadata-only source artifact creation. Matchup/counterplay conclusions remain future claim-review holds and are not content-review proof. |
| D7 | `video-link-training-mode-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | review-only hold / sanitized report only via existing bounded review reuse | Reused `knowledge/sources/videos/youtube-hwradk0bero.md` and the #137 report. | Training-mode/coaching boundaries are supported by existing #137 review; no new content review occurred in this PR. |
| D8 | `video-link-commentary-only-01` | YouTube/video link | `workflows/ingest-video.md`, `workflows/media-scratch-cache-policy.md` | yes | PASS | metadata-only source artifact only | Added `knowledge/sources/videos/youtube-vcpzwawrrla.md`; no bounded content review was performed. | This proves metadata-only source artifact creation for an article-like video source. It does not prove terminology content review. |
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
| D8 | Only metadata was reviewed in this PR. Terminology explanations require later article-like claim review before curated promotion. |
| D9 | Only metadata was reviewed in this PR. Unknown/mixed content classification, frame-advantage routing, and current-fact review remain unproven until later bounded content review. |
| E7 | Training UI and combo-trial observations are not current facts; no exact move properties or frame data were inferred. |

## Terminal-State Coverage Summary

| Terminal state | Tranche 1 result | Evidence |
|---|---|---|
| accepted stable curated knowledge | not proven / HOLD | No input was selected specifically for safe stable curated acceptance. |
| accepted strategy/concept knowledge | not proven / needs_review | A3 has possible concept candidates, but existing review keeps them unaccepted. |
| current-fact authority route | not proven / HOLD | A1/C2 remain unavailable. A3 includes current-fact-like claim categories, but this tranche did not exercise a current-fact authority route. |
| review-only hold | proven by existing bounded review reuse and actual raw-local review | D2, D3, D4, and D7 reuse #137 bounded review; E7 performed actual bounded raw-local review. D6b/D8/D9 are not counted as content-review proof. |
| rejected unsafe | not proven / HOLD | B3/C3 were unavailable and no executed row produced a rejected unsafe candidate. |
| unresolved / needs_review | proven | A3 reused existing source/claim/review artifacts with `needs_review` status. |
| sanitized report only | proven by existing report/artifact reuse and actual E7 review | D1-D4 and D7 reuse the #137 report; D6 reuses existing source/observation artifacts; E7 performed actual bounded raw-local review. D6b/D9 are not counted as video-content report proof. |
| metadata-only source artifact only | proven | D6b, D8, and D9 added metadata-only source artifacts and did not create claim or observation artifacts. |

This tranche does not complete #155. It proves only the terminal states
demonstrated above for the provided rows.

## Unresolved Gaps And Residual Tasks

- D5 subtitle-overlay video-link coverage remains HOLD.
- Full article live-fetch/extraction remains not fully proven; A3 verified
  live metadata/access and reused existing source/claim/review artifacts.
- D6b/D8/D9 bounded video content review remains not proven; these rows prove
  metadata-only source artifact creation only.
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
