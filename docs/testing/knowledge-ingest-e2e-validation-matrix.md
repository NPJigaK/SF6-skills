# Knowledge Ingest E2E Validation Matrix

## Purpose

This matrix supports #155. It defines the finite set of declared article and
video ingest patterns that later child issues must execute and mark `PASS`,
`HOLD`, or `FAIL`.

This document is not a smoke report, implementation, source ingest, claim
review, or proof that the workflows already work. It is the auditable matrix
that makes later validation complete rather than representative.

#153 remains a separate docs-only entrypoint guide. It should reflect proven
status after the validation track has scoped and executed the relevant rows.

Success means correct terminal-state routing, not universal accepted knowledge.
Some inputs should become accepted curated knowledge after review; other inputs
should route to current-fact authority, review-only hold, rejected unsafe,
sanitized report only, or metadata-only source artifacts.

## Definitions

| Term | Definition |
|---|---|
| Input family | The starting form of material: article URL live fetch, article URL with maintainer-provided context, local article or maintainer note, YouTube/video link, or raw local video file. |
| Source type | The article/source role used for routing: official or current-fact-like, maintained third party, community strategy, maintainer note, or unknown/ambiguous. |
| Video format family | The video layout/taxonomy family from the v2.4 fixtures: gameplay-only, gameplay with commentary, livestream layout with webcam/overlay, vertical short, subtitle overlay, clip compilation, training mode, commentary-only, or unknown/mixed. |
| Intended workflow | The existing workflow surface that owns the path, such as `workflows/ingest-article.md`, `workflows/ingest-video.md`, `workflows/review-claims.md`, or `workflows/media-scratch-cache-policy.md`. |
| Expected artifact | The repo artifact that a later child issue may create when safe, such as source metadata, claim candidates, review notes, sanitized observation/report artifacts, or accepted curated knowledge after review. |
| Terminal state | The final reviewed state for a row: accepted curated knowledge, current-fact authority route, review-only hold, rejected unsafe, unresolved or `needs_review`, sanitized report only, or metadata-only source artifact only. |
| Forbidden artifact | Material that must not be committed, including raw media, full transcripts, full article bodies, raw Hermes output, local state, credentials, browser cache, generated frames, screenshots, contact sheets, external binaries, or public runtime changes. |
| `PASS` | The later child issue executes the row, creates only expected artifacts, records the expected terminal state, preserves all forbidden boundaries, and passes required validators. |
| `HOLD` | The later child issue cannot safely execute or complete the row and records an explicit reason, such as permission uncertainty, unavailable maintainer sample, unsafe local-state risk, or source ambiguity. |
| `FAIL` | The later child issue attempts the row and violates a required boundary, cannot produce the expected terminal state, silently skips the row, creates forbidden artifacts, or fails required validators. |

## Shared Safety Boundaries

- `official_raw` remains current-fact authority.
- Exact current facts must not bypass `data/exports/`, `data/roster/`, or the
  approved current-fact authority workflow.
- Video observations are review input only.
- Article ingest creates source metadata, claim candidates, and review notes.
  It does not create accepted knowledge automatically.
- `workflows/review-claims.md` is the repository decision step.
- Hermes output remains draft input.
- Raw media, raw transcripts, raw Hermes output, local state, credentials,
  cookies, browser cache, and external binaries are not committed.
- Public `sf6-agent` behavior is unchanged unless a later issue explicitly
  scopes that change.
- External visual atlas references remain visual references only and do not
  override `official_raw`.
- A row must never be silently skipped. If it cannot be executed safely, it
  must be marked `HOLD` or `FAIL` with the reason.

## Matrix Row Schema

Each validation row uses this shape.

| Field | Required meaning |
|---|---|
| `row_id` | Stable row identifier used by child PRs and the final audit. |
| `parent_issue` | Always `#155`. |
| `input_family` | The declared input family being validated. |
| `source_type_or_format` | Article source role or video format family. |
| `intended_workflow` | Existing workflow(s) that own the row. |
| `required_input` | The sample/input that a later child issue must supply or explicitly hold. |
| `expected_artifacts` | Repo artifacts that are allowed if the row passes. |
| `expected_terminal_state` | Terminal state that the row is meant to prove. |
| `forbidden_artifacts` | Artifacts or behavior that must not appear. |
| `required_validators` | Validators and scans required before the row can pass. |
| `pass_criteria` | Concrete evidence required to mark `PASS`. |
| `hold_criteria` | Safe reasons to mark `HOLD`. |
| `fail_criteria` | Boundary violations or missing evidence that mark `FAIL`. |
| `downstream_child` | Later #155 child issue responsible for executing the row. |

## Validator Sets

Rows refer to these validator sets to keep the matrix readable.

| Validator set | Commands or checks |
|---|---|
| `V-BASE` | `tests/validation/validate-no-video-binary-assets.ps1`, `tests/validation/run-all.ps1`, `git diff --check`, `git diff --check origin/main...HEAD`, and raw/local-state scan from `workflows/media-scratch-cache-policy.md`. |
| `V-ARTICLE` | `V-BASE`, plus `tests/validation/validate-knowledge-schema.ps1` and `tests/validation/validate-ingest-artifacts.ps1` when source, claim, or review artifacts are created. |
| `V-VIDEO` | `V-BASE`, plus `tests/validation/validate-video-artifacts.ps1`, `tests/validation/validate-video-observation-taxonomy-fixtures.ps1`, and `tests/validation/validate-video-learning-report-template.ps1` when video observation/report artifacts are created. |
| `V-CURRENT-FACT` | `V-BASE`, plus `tests/validation/validate-current-fact-boundaries.ps1`, `tests/validation/validate-roster-source.ps1`, and frame-current/data-export validation only when the scoped child touches current-fact authority surfaces. |

## Article Validation Matrix

| row_id | parent_issue | input_family | source_type_or_format | intended_workflow | required_input | expected_artifacts | expected_terminal_state | forbidden_artifacts | required_validators | pass_criteria | hold_criteria | fail_criteria | downstream_child |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `A2-LIVE-CURRENT` | #155 | Article URL live fetch/extraction | official or current-fact-like source | `workflows/ingest-article.md`; `workflows/review-claims.md`; current-fact authority workflow | One permitted URL whose content contains exact current-fact-like claims | Source metadata, extracted claim candidate, review note, current-fact route note | current-fact authority route | full article body, long verbatim excerpts, current values in `knowledge/curated/`, raw Hermes output, credentials, browser cache | `V-ARTICLE`; `V-CURRENT-FACT` if authority surfaces are touched | Source is reviewed, exact current facts are routed away from curated knowledge, and no current-fact bypass occurs | Permission, terms, fetch safety, or source freshness is unclear | Exact current fact is accepted into curated knowledge, full text is committed, or validators fail | Child 2 |
| `A2-LIVE-COMMUNITY` | #155 | Article URL live fetch/extraction | community strategy article | `workflows/ingest-article.md`; `workflows/review-claims.md` | One permitted community strategy article URL | Source metadata, claim candidates, review note, accepted or held/rejected decisions | accepted strategy/concept knowledge or review-only hold | full article body, long excerpts, unreviewed curated page, current facts from community source as authority | `V-ARTICLE` | At least one atomic strategy/concept claim is reviewed to accepted or explicitly held/rejected with evidence | Permission or source content cannot be safely reviewed | Claim is promoted without review, source is copied wholesale, or validators fail | Child 2 |
| `A2-LIVE-JA` | #155 | Article URL live fetch/extraction | Japanese source, if feasible | `workflows/ingest-article.md`; `workflows/review-claims.md` | One permitted Japanese source URL or explicit infeasibility note | Source metadata preserving Japanese title, claim candidates, review note | unresolved / `needs_review` or accepted strategy/concept knowledge after review | full article body, long Japanese excerpts, unofficial term promoted as official terminology, current facts bypassing authority | `V-ARTICLE` | Japanese source is summarized without long copying and claims are routed to accepted, held, rejected, or needs_review | No safe Japanese source is available or fetch permission is unclear | Japanese source is treated as authoritative without review, long excerpts are copied, or validators fail | Child 2 |
| `A3-CONTEXT-CURRENT` | #155 | Article URL with maintainer-provided context | official or current-fact-like source | `workflows/ingest-article.md`; `workflows/review-claims.md`; current-fact authority workflow | URL plus maintainer-provided summary/context containing exact current-fact-like claims | Source metadata, claim candidate, review note, current-fact route note | current-fact authority route | pretending context is live extraction, exact values in curated knowledge, raw Hermes output | `V-ARTICLE`; `V-CURRENT-FACT` if authority surfaces are touched | Context is labeled maintainer-provided, current facts route to authority, and no live-fetch claim is made | Maintainer context is insufficient to classify the claim | Context is misrepresented as fetched article text or current facts bypass authority | Child 3 |
| `A3-CONTEXT-THIRD-PARTY` | #155 | Article URL with maintainer-provided context | maintained third-party source | `workflows/ingest-article.md`; `workflows/review-claims.md` | URL plus maintainer-provided summary from a maintained third-party source | Source metadata, claim candidates, review note | accepted stable curated knowledge or unresolved / `needs_review` | full article text, current facts as third-party authority, unreviewed curated page | `V-ARTICLE` | Stable non-current claim is accepted only after review, or insufficient claim remains needs_review | Maintainer context lacks enough detail to review | Third-party claim is treated as current-fact authority or validators fail | Child 3 |
| `A3-CONTEXT-COMMUNITY` | #155 | Article URL with maintainer-provided context | community strategy article | `workflows/ingest-article.md`; `workflows/review-claims.md` | URL plus maintainer-provided strategy summary/context | Source metadata, claim candidates, review note, smallest curated update if accepted | accepted strategy/concept knowledge | full article body, long excerpts, patch-sensitive claim accepted without boundary | `V-ARTICLE` | At least one scoped strategy/concept claim is accepted after review with evidence metadata | Evidence is anecdotal, patch-sensitive, or conflicting | Accepted page lacks review evidence or source boundary | Child 3 |
| `A3-CONTEXT-UNKNOWN` | #155 | Article URL with maintainer-provided context | unknown/ambiguous source | `workflows/ingest-article.md`; `workflows/review-claims.md` | URL plus ambiguous or incomplete maintainer context | Source metadata or review note explaining ambiguity | rejected unsafe or unresolved / `needs_review` | accepted curated knowledge, exact current facts, fabricated source metadata | `V-ARTICLE` | Ambiguity is recorded and the row routes to rejected unsafe or needs_review | Source cannot be located or context is too thin for even metadata | Ambiguous source is accepted as curated knowledge | Child 3 |
| `A4-LOCAL-NOTE` | #155 | Local article or maintainer note | maintainer note source | `workflows/ingest-article.md`; `workflows/review-claims.md` | One maintainer-provided local note safe to summarize | `maintainer_note` source metadata, claim candidates, review note, optional accepted curated update | accepted stable curated knowledge or accepted strategy/concept knowledge | private local paths, private note text copied wholesale, authority without review | `V-ARTICLE` | A safe note produces reviewed claim decision and any accepted item cites the note boundary | Maintainer does not provide a safe note | Private note is treated as authority without review or private paths leak | Child 4 |
| `A4-LOCAL-CURRENT` | #155 | Local article or maintainer note | current-fact-like claim | `workflows/ingest-article.md`; `workflows/review-claims.md`; current-fact authority workflow | Local note containing current-fact-like claim | Source metadata, claim candidate, review note, current-fact route note | current-fact authority route | current values in curated knowledge, generated frame-current changes outside scope, local private state | `V-ARTICLE`; `V-CURRENT-FACT` if authority surfaces are touched | Exact current fact is held for authority workflow and not accepted into curated knowledge | Note lacks enough detail to classify as current-fact-like | Current fact is accepted from local note alone or validators fail | Child 4 |
| `A4-LOCAL-UNSUPPORTED` | #155 | Local article or maintainer note | ambiguous/unsupported claim | `workflows/ingest-article.md`; `workflows/review-claims.md` | Local note with vague, conflicting, or unsupported claim | Review note and rejected/needs_review candidate | rejected unsafe or unresolved / `needs_review` | accepted curated knowledge, raw local note dump, private state | `V-ARTICLE` | Unsupported claim is rejected or left needs_review with reason | Maintainer cannot share enough context safely | Unsupported claim is accepted or raw note material is committed | Child 4 |

## Video Link Validation Matrix

| row_id | parent_issue | input_family | source_type_or_format | intended_workflow | required_input | expected_artifacts | expected_terminal_state | forbidden_artifacts | required_validators | pass_criteria | hold_criteria | fail_criteria | downstream_child |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `VL-GAMEPLAY-ONLY` | #155 | YouTube/video link | gameplay-only | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md`; `workflows/review-claims.md` | One maintainer-approved video link with gameplay-only format | Metadata-only source reference, sanitized observation/report artifact, optional claim candidate | sanitized report only or accepted strategy/concept knowledge after review | raw video, frames, screenshots, contact sheets, captions, transcripts, logs, caches, exact current facts, `official_raw` override, public runtime behavior | `V-VIDEO` | Link is reviewed safely, report is sanitized, and any claim is reviewed separately | Permission, platform access, or safe sample is unavailable | Raw media or transcript is committed, exact facts are inferred, or validators fail | Child 5 |
| `VL-COMMENTARY` | #155 | YouTube/video link | gameplay with commentary | `workflows/ingest-video.md`; `workflows/review-claims.md` | One maintainer-approved gameplay-with-commentary link | Metadata-only source reference, sanitized report, source-local commentary note | review-only hold or accepted strategy/concept knowledge after review | raw transcript, long utterance copy, commentary as current-system authority, raw video/cache | `V-VIDEO` | Commentary is source-local and any reusable claim is reviewed | Commentary cannot be separated from gameplay safely | Commentary is promoted as current-system authority | Child 5 |
| `VL-LIVESTREAM-OVERLAY` | #155 | YouTube/video link | livestream layout with webcam/overlay | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md` | One maintainer-approved livestream/overlay link | Metadata-only source reference, sanitized layout/obstruction report | sanitized report only or review-only hold | frames, screenshots, contact sheets, raw video, captions, logs, overlay-derived exact facts | `V-VIDEO` | Overlay obstruction is recorded and no exact fact is inferred | No safe sample or overlay prevents useful observation | Overlay-limited observation is promoted to exact fact | Child 5 |
| `VL-VERTICAL-SHORT` | #155 | YouTube/video link | vertical short | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md` | One maintainer-approved vertical short link | Metadata-only source reference, sanitized crop/visibility report | sanitized report only or review-only hold | raw short, frames, screenshots, captions, transcript, public behavior | `V-VIDEO` | Vertical crop limits are documented and source remains metadata-only | Safe access or stable source metadata unavailable | Raw short or generated derivative is committed | Child 5 |
| `VL-SUBTITLE-OVERLAY` | #155 | YouTube/video link | subtitle overlay | `workflows/ingest-video.md`; `workflows/review-claims.md` | One maintainer-approved subtitle-heavy link | Metadata-only source reference, sanitized report, possible claim candidate or hold | unresolved / `needs_review` or review-only hold | raw captions, subtitle files, full transcript, exact current facts from subtitles | `V-VIDEO` | Subtitle obstruction and no-transcript boundary are recorded | Subtitles cannot be reviewed without unsafe transcript handling | Captions/transcripts are committed or subtitle claims are accepted without review | Child 5 |
| `VL-CLIP-COMPILATION` | #155 | YouTube/video link | clip compilation | `workflows/ingest-video.md`; `workflows/review-claims.md` | One maintainer-approved compilation link | Metadata-only source reference, sanitized report with edit/cut notes | review-only hold or rejected unsafe | raw video, extracted clips, frame dumps, exact timing claims across cuts | `V-VIDEO` | Edited/cut limitations route to hold/rejected unless a safe claim is separately reviewed | Compilation source cannot be bounded safely | Edited footage is used for exact timing/current facts | Child 5 |
| `VL-TRAINING-MODE` | #155 | YouTube/video link | training mode | `workflows/ingest-video.md`; `workflows/review-claims.md` | One maintainer-approved training-mode link | Metadata-only source reference, sanitized report, training UI boundary note | review-only hold or current-fact authority route when exact facts appear | training UI labels as current authority, screenshots, raw video, frame facts | `V-VIDEO`; `V-CURRENT-FACT` if exact facts are routed | Training UI observations remain review input and exact facts route to authority | UI is unreadable or source patch context is unknown | Training UI values are accepted as current facts | Child 5 |
| `VL-COMMENTARY-ONLY` | #155 | YouTube/video link | commentary-only | `workflows/ingest-video.md`; `workflows/review-claims.md` | One maintainer-approved commentary-only link | Metadata-only source reference, source-local summary, claim candidate or hold | metadata-only source artifact only or review-only hold | full transcript, long quoted utterances, accepted knowledge without review | `V-VIDEO`; `V-ARTICLE` if claims are created | Commentary-only source is metadata-only unless claims are explicitly reviewed | Cannot safely summarize without transcript-like capture | Transcript is committed or commentary is treated as authority | Child 5 |
| `VL-UNKNOWN-MIXED` | #155 | YouTube/video link | unknown/mixed | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md` | One maintainer-approved unknown/mixed link or explicit unsafe sample note | Metadata-only source reference, sanitized held report | rejected unsafe or review-only hold | raw media, inferred format, fabricated taxonomy, exact facts | `V-VIDEO` | Unknown/mixed status is recorded and not silently coerced | No safe sample is available | Unknown source is marked passed without classification or hold reason | Child 5 |

## Raw Local Video Validation Matrix

| row_id | parent_issue | input_family | source_type_or_format | intended_workflow | required_input | expected_artifacts | expected_terminal_state | forbidden_artifacts | required_validators | pass_criteria | hold_criteria | fail_criteria | downstream_child |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `RV-GAMEPLAY-ONLY` | #155 | Raw local video file | gameplay-only | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md`; `workflows/review-claims.md` | Maintainer-provided local gameplay-only sample kept outside repo | Sanitized observation/report artifact, optional claim candidate | sanitized report only or accepted strategy/concept knowledge after review | raw local file, local path leak, frames, screenshots, contact sheets, captions, transcripts, logs, caches, exact current facts | `V-VIDEO` | Raw file stays repo-external and sanitized report/claim route is recorded | No safe maintainer sample, media cannot stay repo-external, validator failure, or local path leakage risk | Raw media enters repo, exact facts are inferred, or validators fail | Child 6 |
| `RV-COMMENTARY` | #155 | Raw local video file | gameplay with commentary | `workflows/ingest-video.md`; `workflows/review-claims.md` | Maintainer-provided local gameplay-with-commentary sample outside repo | Sanitized report, source-local commentary note, optional claim candidate | review-only hold or accepted strategy/concept knowledge after review | raw media, transcript, long utterance copy, local paths, commentary as authority | `V-VIDEO` | Commentary remains source-local and any claim is separately reviewed | No safe sample or commentary cannot be separated safely | Transcript/local media leaks or commentary becomes authority | Child 6 |
| `RV-LIVESTREAM-OVERLAY` | #155 | Raw local video file | livestream layout with webcam/overlay | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md` | Maintainer-provided local livestream/overlay sample outside repo | Sanitized report or held report with obstruction notes | sanitized report only or review-only hold | raw local file, frames, screenshots, contact sheets, local state, overlay-derived exact facts | `V-VIDEO` | Overlay/visibility limits are recorded with sanitized evidence only | No safe sample, repo-external scratch unavailable, or local state risk | Local media or generated derivatives are committed | Child 6 |
| `RV-VERTICAL-SHORT` | #155 | Raw local video file | vertical short | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md` | Maintainer-provided local vertical short sample outside repo | Sanitized report or held report | sanitized report only or review-only hold | raw short, local path, frames, screenshots, captions, contact sheets | `V-VIDEO` | Vertical/crop limits are recorded without local path leakage | No safe sample or media cannot remain outside repo | Raw short or visual derivative enters repo | Child 6 |
| `RV-SUBTITLE-OVERLAY` | #155 | Raw local video file | subtitle overlay | `workflows/ingest-video.md`; `workflows/review-claims.md` | Maintainer-provided local subtitle-heavy sample outside repo | Sanitized report, possible claim candidate or hold | unresolved / `needs_review` or review-only hold | subtitle files, transcript, raw media, local paths, exact facts from subtitles | `V-VIDEO` | Subtitle visibility is summarized without committing transcript/captions | No safe sample or transcript would be required | Captions/transcripts are committed or subtitle claims bypass review | Child 6 |
| `RV-CLIP-COMPILATION` | #155 | Raw local video file | clip compilation | `workflows/ingest-video.md`; `workflows/review-claims.md` | Maintainer-provided local compilation sample outside repo | Sanitized report with edit/cut notes | review-only hold or rejected unsafe | extracted clips, raw media, frame dumps, exact timing/current facts across cuts | `V-VIDEO` | Edited/cut uncertainty routes to hold/rejected unless safe claim is reviewed | No safe sample or edits cannot be bounded | Compilation is used for exact timing/current facts | Child 6 |
| `RV-TRAINING-MODE` | #155 | Raw local video file | training mode | `workflows/ingest-video.md`; `workflows/review-claims.md` | Maintainer-provided local training-mode sample outside repo | Sanitized report, training UI boundary note | review-only hold or current-fact authority route when exact facts appear | screenshots, raw media, training UI as current authority, frame-current changes outside scope | `V-VIDEO`; `V-CURRENT-FACT` if exact facts are routed | Training UI remains review input and exact facts route to authority | No safe sample or source patch context unknown | Training UI values are accepted as current facts | Child 6 |
| `RV-COMMENTARY-ONLY` | #155 | Raw local video file | commentary-only | `workflows/ingest-video.md`; `workflows/review-claims.md` | Maintainer-provided local commentary-only sample outside repo | Sanitized source-local report, optional claim candidate or hold | metadata-only source artifact only or review-only hold | raw audio/video, transcript, long utterance copy, local paths | `V-VIDEO`; `V-ARTICLE` if claims are created | Commentary-only material remains source-local unless reviewed claims are created | Safe summary cannot be made without transcript-like capture | Transcript/raw local media is committed | Child 6 |
| `RV-UNKNOWN-MIXED` | #155 | Raw local video file | unknown/mixed | `workflows/ingest-video.md`; `workflows/media-scratch-cache-policy.md` | Maintainer-provided local unknown/mixed sample outside repo or explicit unsafe sample note | Sanitized held report | rejected unsafe or review-only hold | raw media, local path, fabricated taxonomy, exact facts, generated derivatives | `V-VIDEO` | Unknown/mixed row is explicitly held or rejected with reason | No safe sample or local-state risk is too high | Row is marked pass without classification or hold reason | Child 6 |

## Terminal-State Coverage Matrix

| Terminal state | Required row(s) | Minimum evidence | Child issue that will prove it |
|---|---|---|---|
| accepted stable curated knowledge | `A3-CONTEXT-THIRD-PARTY` or `A4-LOCAL-NOTE` | Accepted claim has evidence metadata, review decision, no exact current values, and smallest curated update | Child 3 or Child 4 |
| accepted strategy/concept knowledge | `A2-LIVE-COMMUNITY`, `A3-CONTEXT-COMMUNITY`, `VL-GAMEPLAY-ONLY`, or `RV-GAMEPLAY-ONLY` | Accepted claim passed `workflows/review-claims.md` and does not depend on current facts | Child 2, Child 3, Child 5, or Child 6 |
| current-fact authority route | `A2-LIVE-CURRENT`, `A3-CONTEXT-CURRENT`, `A4-LOCAL-CURRENT`, `VL-TRAINING-MODE`, or `RV-TRAINING-MODE` | Exact current-fact-like claim is routed to authority workflow and not accepted into curated knowledge | Child 2, Child 3, Child 4, Child 5, or Child 6 |
| review-only hold | `A3-CONTEXT-UNKNOWN`, `VL-COMMENTARY`, `VL-LIVESTREAM-OVERLAY`, `RV-COMMENTARY`, or `RV-LIVESTREAM-OVERLAY` | Hold reason, confidence/uncertainty, and forbidden promotion are recorded | Child 3, Child 5, or Child 6 |
| rejected unsafe | `A3-CONTEXT-UNKNOWN`, `A4-LOCAL-UNSUPPORTED`, `VL-UNKNOWN-MIXED`, or `RV-UNKNOWN-MIXED` | Rejection reason shows source or observation is unsafe, unsupported, or too ambiguous | Child 3, Child 4, Child 5, or Child 6 |
| unresolved / `needs_review` | `A2-LIVE-JA`, `A3-CONTEXT-UNKNOWN`, `VL-SUBTITLE-OVERLAY`, or `RV-SUBTITLE-OVERLAY` | Claim or observation remains explicitly unresolved with next review condition | Child 2, Child 3, Child 5, or Child 6 |
| sanitized report only | `VL-LIVESTREAM-OVERLAY`, `VL-VERTICAL-SHORT`, `RV-LIVESTREAM-OVERLAY`, or `RV-VERTICAL-SHORT` | Sanitized report records layout/visibility limits and no source/claim/curated artifact is required | Child 5 or Child 6 |
| metadata-only source artifact only | `VL-COMMENTARY-ONLY`, `RV-COMMENTARY-ONLY`, or a held article URL row where only source metadata is safe | Metadata-only source record exists with no accepted claim or raw content | Child 5, Child 6, or Child 2 |

## Downstream Child Issue Map

| Downstream child | Rows owned | Execution responsibility |
|---|---|---|
| Child 2: Article URL live-fetch E2E validation | `A2-*` | Validate live URL fetch/extraction only where permission, terms, copyright, and tooling are safe. Mark unsafe rows `HOLD` rather than faking extraction. |
| Child 3: Article URL with maintainer-provided context E2E validation | `A3-*` | Validate the safer URL plus maintainer context path without pretending it is live extraction. |
| Child 4: Local article / maintainer note E2E validation | `A4-*` | Validate local note handling while preventing private note text, private paths, or unsupported authority promotion. |
| Child 5: YouTube/video link E2E validation across all declared video format families | `VL-*` | Validate metadata-only source references, sanitized reports, and claim/hold/reject routing for video links. |
| Child 6: Raw local video E2E validation across all declared video format families | `RV-*` | Validate repo-external raw local video handling and sanitized observation/report routing for maintainer-provided samples. |
| Child 7: Cross-path review and promotion audit | all rows | Verify every row has `PASS`, `HOLD`, or `FAIL`, no row was silently skipped, accepted items have review evidence, and validators pass. |

Recommended execution order:

1. Child 2 through Child 4 for article paths.
2. Child 5 for video links.
3. Child 6 for raw local video, because it depends on maintainer-provided
   repo-external samples.
4. Child 7 final audit after every row has a recorded terminal state.

## Required Validators

Every child PR must run at least:

- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-no-video-binary-assets.ps1`
- `powershell.exe -NoProfile -ExecutionPolicy Bypass -File tests/validation/run-all.ps1`
- `git diff --check`
- `git diff --check origin/main...HEAD`
- raw/local-state scan based on `workflows/media-scratch-cache-policy.md`

Rows that create article/source/claim/review artifacts should also run relevant
existing validation, including:

- `tests/validation/validate-knowledge-schema.ps1`
- `tests/validation/validate-ingest-artifacts.ps1`

Rows that create video observation or report artifacts should also run relevant
existing validation, including:

- `tests/validation/validate-video-artifacts.ps1`
- `tests/validation/validate-video-observation-taxonomy-fixtures.ps1`
- `tests/validation/validate-video-learning-report-template.ps1`

Rows that route or touch current-fact authority surfaces should also run
relevant current-fact validation, including:

- `tests/validation/validate-current-fact-boundaries.ps1`
- `tests/validation/validate-roster-source.ps1`
- frame-current and generated-surface checks when those surfaces are in scope

If PowerShell reports git-unavailable warnings during generated-surface checks,
the child PR must verify from a git-visible shell that there are no unintended
residual diffs in generated references, `.dist`, frame-current assets,
normalization assets, `data/raw`, `data/normalized`, or `data/exports`.

## Non-Goals

- No article ingest execution in this Child 1 PR.
- No video ingest execution in this Child 1 PR.
- No external fetch.
- No Hermes run.
- No raw media.
- No source artifacts.
- No claim artifacts.
- No video observations.
- No curated knowledge pages.
- No validators.
- No public behavior change.
- No #153 implementation.
- No #133 changes.

## Acceptance Checklist

- [ ] `docs/testing/knowledge-ingest-e2e-validation-matrix.md` exists.
- [ ] Matrix covers all declared video input families.
- [ ] Matrix covers all declared video format families.
- [ ] Matrix covers all declared article input families.
- [ ] Matrix covers all declared article/source role families.
- [ ] Matrix covers all terminal-state families.
- [ ] Every row has `PASS` / `HOLD` / `FAIL` criteria.
- [ ] Every row names expected artifacts and forbidden artifacts.
- [ ] Every row names required validators.
- [ ] Every row maps to a later child issue.
- [ ] The document states that success means correct routing, not universal curated promotion.
- [ ] No ingest execution, external fetch, raw media, source artifact, claim artifact, observation artifact, curated page, validator, or public behavior change is added.
