# Hermes Knowledge Promotion Smoke 20260513

## Report Metadata

| Field | Value |
|---|---|
| Report id | `hermes-knowledge-promotion-smoke-20260513` |
| Date | 2026-05-13 |
| Timezone | Asia/Tokyo |
| Related issue | #151 |
| Related tracking issue | #133 |
| Report type | `sanitized_hermes_knowledge_promotion_smoke` |
| Maintainer-local only | yes |
| Hermes availability status | available and used for one bounded single-turn smoke |
| Executed status | executed sanitized smoke report |
| Canonical status | sanitized repo artifact only; raw Hermes output is not canonical |

## Smoke Purpose And Scope

This smoke tests whether Hermes-assisted output can be safely classified,
filtered, rejected, held, and distilled into a reviewed repository artifact.

This smoke does not test video analysis, move recognition, move-frequency
analytics, external frame-atlas acquisition, external asset usability, model
training, dataset creation, source ingestion runtime, or public `sf6-agent`
behavior.

Raw Hermes output is non-canonical draft input. Only sanitized, reviewed,
validator-compatible repository artifacts can become repo knowledge inputs.
`official_raw` remains the current-fact authority.

## Source Surfaces Reviewed

The smoke used safe repo-local context only. Codex reviewed the following
surfaces before invoking Hermes and distilled the smoke result against these
repo boundaries:

- `docs/architecture/sf6-video-analysis-learning-loop.md`
- `docs/architecture/sf6-move-recognition-evaluation-plan.md`
- `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md`
- `docs/testing/smoke-runs/video-analysis-learning-report-template.md`
- `tests/fixtures/video-observation-taxonomy/`
- `data/external-frame-atlas/evaluation/README.md`
- `data/external-frame-atlas/evaluation/source-evaluation-matrix.json`
- `contracts/external-frame-atlas-source-evaluation.schema.json`
- `contracts/external-frame-atlas-source.schema.json`
- `tests/fixtures/external-frame-atlas/`
- `workflows/media-scratch-cache-policy.md`
- `tests/validation/validate-no-video-binary-assets.ps1`
- `contracts/video-observation.schema.json`
- `contracts/video-observation.md`
- `workflows/ingest-video.md`
- `docs/architecture/sf6-video-analysis-protocol.md`
- `docs/architecture/external-frame-atlas-policy.md`
- `knowledge/sources/videos/`
- `knowledge/evidence/video-observations/`
- `evals/questions/video-observation.yaml`
- `skills/sf6-agent/assets/frame-current/runtime_manifest.json`
- current-fact authority surfaces under `data/exports/` and `data/roster/`

No external web, video platform, external atlas, or binary asset source was
fetched.

## Hermes Availability And Limitations

| Item | Result |
|---|---|
| Hermes command available | yes |
| Hermes actually used | yes, one bounded single-turn smoke |
| Invocation mode | `hermes chat` quiet single-query mode with repo-local context summarized in the prompt |
| Tool/file/web access requested from Hermes | no |
| Raw local output produced | yes, as draft input only |
| Raw output committed | no |
| Local state committed | no |
| External sources fetched | no |
| Raw media or binary assets used | no |
| CI requirement created | no |
| Public `sf6-agent` requirement created | no |

Limitations:

- Hermes output is draft input only.
- Hermes cannot promote current facts.
- Hermes cannot override `official_raw`.
- Hermes memory, sessions, local skills, Curator output, logs, caches, and
  checkpoints are non-canonical.
- This smoke used a concise repo-context prompt, not a large research campaign
  and not live video analysis.
- Hermes may maintain normal user-level session history outside the repository;
  that local state was not committed, exported, or used as repo evidence.

## Prompt Summary

Hermes was asked to classify future Hermes-assisted SF6 video observation
outputs from v2.4 repository context into sanitized repo artifact candidates,
source metadata candidates, evidence or fixture candidates, validator or policy
candidates, current-fact authority review items, review-only holds, rejected
unsafe items, and out-of-scope items.

The prompt explicitly prohibited current-fact inference, authority promotion
from video observations or external visual references, tool or web access,
external assets, and local state use. The full prompt and raw output transcript
are not included in this report.

## Raw Output And Local State Status

| Item | Committed? | Notes |
|---|---:|---|
| Raw Hermes output | no | Used only as draft input for this sanitized report. |
| Hermes memory | no | Not exported, inspected as evidence, or committed. |
| Hermes sessions | no | No session export or session file was committed. |
| Hermes local skills | no | No local skill material was committed. |
| Curator output | no | Not used or committed. |
| Logs, caches, checkpoints | no | No repo-local logs, caches, or checkpoints were added. |
| Credentials, cookies, secrets | no | Not printed, requested, recorded, or committed. |
| Raw media | no | No video, audio, GIF, image, or frame asset was used. |
| Transcripts or captions | no | No transcript, caption, subtitle, or full utterance artifact was added. |
| Screenshots, frames, contact sheets | no | No generated visual derivative was added. |
| External assets fetched or stored | no | No external fetch, scrape, download, or cache operation was performed. |

## Promotion Classification

| Category | Examples From The Smoke | Why It Belongs There | Allowed Repo Surface | Promotion Condition | Forbidden Promotion |
|---|---|---|---|---|---|
| `sanitized_repo_artifact_candidate` | Promotion checklist, bounded smoke summary, authority-boundary summary | These describe process and review boundaries rather than new SF6 facts | `docs/testing/smoke-runs/`, `docs/architecture/`, `workflows/` | Must be paraphrased, scoped to an issue, validator-compatible, and reviewed | Raw transcript, raw prompt/output, exact current facts, local state |
| `source_metadata_candidate` | Metadata-only source descriptions, source role labels, access/review notes | Source records can identify where review material came from without storing media | `knowledge/sources/` or approved metadata-only source surfaces | Must include source role, review status, boundary notes, and no copied media/transcript | Source-local claim as current-system authority; raw video, captions, screenshots, or binary assets |
| `evidence_or_fixture_candidate` | Metadata-only taxonomy fixture ideas, future candidate observation fixture ideas, boundary-test fixtures | Fixtures can test schema and validator behavior without becoming accepted gameplay knowledge | `tests/fixtures/`, `knowledge/evidence/` for review-only evidence | Must remain metadata-only, confidence-scored, source-referenced, and review-only | Accepted strategy claim, canonical move ID from visual inference alone, exact frame facts |
| `validator_or_policy_candidate` | Guardrail checks for raw media, local state, authority promotion, external atlas boundaries | Repeated unsafe classes should become machine-checkable or policy-visible | `tests/validation/`, `workflows/`, `contracts/` | Must be implemented in a later scoped PR with focused validation | Broad runtime behavior, scraper/downloader, cache sync, public answer behavior |
| `current_fact_authority_review_required` | Any exact move property, current patch fact, frame data, hit/block advantage, damage/current-system claim | Current facts require authority surfaces, not Hermes summaries, video, or external visual references | `data/exports/`, `data/roster/`, generated frame-current assets through approved generation | Must go through frame-data authority or refresh workflow | Updating current facts from Hermes, video observations, commentary, or external visual atlas alone |
| `review_only_hold` | Video observations, Hermes summaries, external visual reference interpretations, commentary/coaching summaries | These can inform review but lack authority by themselves | Smoke reports, observation holding areas, review notes | Must carry confidence, limitations, `not_inferred`, and follow-up requirements | Generated reference output, accepted curated knowledge, public runtime answer behavior |
| `rejected_unsafe` | Raw Hermes output, raw transcripts, raw media, local state, unsupported current-fact claims, external atlas as authority | These violate source, copyright, privacy, or authority boundaries | none | Must be discarded or held outside repo if local cleanup/review requires it | Any repo artifact promotion |
| `out_of_scope` | Move recognition runtime, move-frequency analytics, external atlas cache sync, external video usability smoke, model/dataset creation | #151 is a smoke report only | none in this PR | Later explicit gated issues only | Implementing them in this PR or treating this smoke as approval |

## Proposed Knowledge-Promotion Candidates

Safe candidates from this smoke are process artifacts, not new SF6 gameplay
facts:

- A promotion checklist for future Hermes-assisted video observation work:
  require issue scope, safe input list, raw-output exclusion, authority
  boundary, confidence/review status, `not_inferred`, validator results, and
  PR review before promotion.
- A future report checklist: record Hermes availability, prompt summary, raw
  output status, local state status, source surfaces reviewed, promotion
  classification, rejected unsafe candidates, hold items, validation, and
  cleanup status.
- A fixture candidate idea: metadata-only candidate move-observation fixtures
  only after a later gated usability smoke proves the shape is useful or
  limited; no raw media, binary assets, or exact current facts.
- A validator/policy follow-up idea: if future reports repeatedly expose the
  same unsafe category, add a scoped validator or policy check rather than
  relying on reviewer memory.
- A current-fact review checklist: route any exact frame data, move property,
  current patch claim, damage/current-system claim, or `official_raw` conflict
  to current-fact authority review.

No new gameplay fact, matchup conclusion, move property, frame value, or public
answer behavior is promoted by this smoke.

## Rejected Unsafe Candidates

These candidate outputs must not be promoted:

- unsupported current-fact claims from Hermes output;
- video-derived exact startup, active, recovery, hit advantage, or block
  advantage;
- external visual atlas references treated as current-fact authority;
- raw Hermes claims without repo evidence;
- commentary or coaching claims treated as current-system authority;
- transcript-like raw outputs or full copied utterances;
- raw media, GIFs, images, frames, screenshots, contact sheets, thumbnails, or
  captions;
- Hermes memory, sessions, local skills, Curator output, logs, caches,
  checkpoints, credentials, cookies, or secrets;
- public `sf6-agent` behavior changes;
- unreviewed move-recognition or move-frequency claims;
- perceptual hash, visual descriptor, or visual similarity output treated as
  exact move confirmation.

## Hold Items

These items require later scoped work and are not approved by this smoke:

- external frame-atlas local cache sync smoke;
- GIF/image video usability smoke;
- candidate move-observation metadata fixtures;
- candidate move-observation validator;
- move-frequency aggregation planning updates;
- deeper Hermes tool availability or `video_analyze` capability checks;
- any validator or policy updates that future reports show are needed.

## Authority Boundary

- `official_raw` remains current-fact authority.
- Hermes output is draft input only.
- Current facts must not be inferred from Hermes summaries alone.
- Source-local claims remain source-local.
- Video observations remain review input.
- External visual atlas references remain visual references only.
- External visual atlas references do not override `official_raw`.
- External visual atlas references are not numeric frame-data ingestion sources.
- Public `sf6-agent` behavior is unchanged.

## What Was Not Inferred

- no exact current facts;
- no exact frame data;
- no exact startup, active, or recovery;
- no exact hit or block advantage;
- no move-recognition accuracy;
- no move-frequency analytics;
- no matchup verdicts;
- no coaching conclusions;
- no external asset usability conclusion;
- no public behavior readiness conclusion;
- no conclusion that Hermes can independently produce correct SF6 knowledge.

## Follow-Up Candidates

Immediate PR follow-up:

- none expected; this PR should remain a single sanitized smoke report unless
  review identifies a report clarity issue.

Tracking issue #133 closure decision input:

- #151 gives one small positive smoke that the Hermes-assisted promotion loop
  can be used in a bounded, sanitized, repo-local way.
- #133 can use this report as evidence that v2.4 produced guardrails and a
  first promotion-loop smoke, not as evidence that move recognition, external
  atlas usefulness, or automatic knowledge growth is complete.

Future gated issue candidates:

- external frame-atlas local cache sync smoke;
- external frame-atlas video usability smoke;
- candidate move-observation metadata fixture pilot;
- candidate move-observation validator;
- move-frequency aggregation planning update;
- optional local-only recognition experiment only if prior stages justify it.

Validator or policy candidates:

- add new checks only after repeated, concrete failure modes appear in future
  reports;
- keep media/cache, local-state, authority, and current-fact boundaries as
  required gates.

Unsupported or hold items:

- any request to promote raw Hermes output, raw video observations, external
  visual atlas artifacts, or source-local commentary into current-fact
  authority remains held or rejected.

Follow-up candidates are recommendations only. They are not automatically
approved work.

## Cleanup And Verification

| Item | Status |
|---|---|
| Local raw output cleanup | Raw Hermes output was not written to a repo file. The local CLI response was used only as draft input for this sanitized report. |
| Local state cleanup | No repo-local Hermes state was created or committed. Normal maintainer-local Hermes session history, if retained by the tool outside the repo, is non-canonical and not used as evidence. |
| Worktree check | PASS; post-validation `git status --short` showed only this new sanitized report before commit. |
| `validate-no-video-binary-assets.ps1` | PASS; `No video binary assets OK`. |
| `run-all.ps1` | PASS; `V2 validation suite OK`. PowerShell preflight emitted git-unavailable warnings for derived-output status checks. |
| `git diff --check` | PASS; no output. |
| `git diff --check origin/main...HEAD` | PASS; no output. |
| Raw/local-state scan | PASS; scan reported expected pre-existing Hermes-named docs, packs, workflows, `workflows/maintainer-agent-session.md`, and this sanitized report. No new raw media, external asset, transcript, binary, cache, credential, or repo-local Hermes state artifact was found. |
| Generated-surface residual diff check | PASS after cleanup; `run-all.ps1` preflight temporarily regenerated frame-current JSON diffs, those scope-excluded generated changes were restored, and a git-visible shell showed no residual diffs in `.dist`, generated references, frame-current assets, normalization assets, `data/raw`, `data/normalized`, or `data/exports`. |
