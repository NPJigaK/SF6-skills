# Knowledge Ingest Entrypoints

## Purpose

This is a start-here guide for maintainers, Codex, and Hermes-assisted
workflows that turn video and article sources into reviewable repository
knowledge candidates.

This guide does not implement ingest, run new validation, fetch sources, run
Hermes, or create source, claim, observation, or curated knowledge artifacts.
It connects existing workflows and records which entrypoint paths are confirmed
by smoke reports versus designed but not yet fully end-to-end validated.

Use this guide to choose the correct first workflow and the correct terminal
state for an input. Knowledge promotion means reaching the correct repository
terminal state, not blindly accepting every input into `knowledge/curated/`.

Terminal states include:

- source metadata
- observation artifact
- claim candidate
- review note
- accepted curated knowledge
- current-fact authority route
- review-only hold
- rejected unsafe item
- sanitized report only

Relevant smoke reports for current proof status:

- `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md`
- `docs/testing/smoke-runs/2026-05-01-hermes-assisted-mizen-article-ingest.md`
- `docs/testing/smoke-runs/hermes-knowledge-promotion-smoke-20260513.md`

## Shared Promotion Rule

Ingest is evidence gathering. Review is the repository decision.

Article and video ingest may create source metadata, observation artifacts,
claim candidates, review notes, and sanitized reports. They do not automatically
create accepted curated knowledge.

Accepted curated knowledge requires claim review through
`workflows/review-claims.md`. Exact current facts route to current-fact
authority surfaces instead of curated prose. `official_raw` remains current-fact
authority, with current data grounded in `data/exports/`, `data/roster/`, and
generated frame-current assets.

Raw media, raw transcripts, raw Hermes output, browser/cache state, local
Hermes state, credentials, external binaries, GIFs, images, frames,
screenshots, contact sheets, captions, and full article bodies are not
committed by default.

When the correct terminal state is uncertain, hold the candidate rather than
promoting it.

## Entrypoint: Raw Local Video

Raw local video is maintainer-local working material. It may be used to support
observation drafting, but raw media stays outside the repository by default.

Use:

- `workflows/media-scratch-cache-policy.md` for repo-external scratch/cache
  handling, cleanup, and leakage checks.
- `workflows/ingest-video.md` for structured observation artifacts.
- `workflows/review-claims.md` before promoting any reusable claim.

Repo artifacts from this entrypoint should be sanitized observations, reports,
source metadata, or claim candidates. Video observations are review input only.
Accepted knowledge is not automatic.

Do not infer exact current facts, exact frame data, exact startup/active/recovery,
exact hit/block advantage, matchup verdicts, or coaching conclusions from video
alone. `official_raw` remains current-fact authority.

Status:

- Workflow exists.
- Full raw-local-video to observation to claim review to
  accepted/hold/rejected terminal state is not yet fully end-to-end validated.

## Entrypoint: YouTube Or Video Link

A YouTube or video link may become a metadata-only source reference when that
fits existing source conventions. The link can support bounded maintainer-local
review, sanitized learning reports, or later metadata-only video source
artifacts.

Raw video, downloaded clips, frames, screenshots, captions, transcripts,
contact sheets, logs, tool output, browser cache, and media cache must not be
committed. Use `workflows/media-scratch-cache-policy.md` for any temporary
media handling.

Use:

- `workflows/ingest-video.md` when the goal is a structured observation
  artifact.
- `workflows/review-claims.md` before any accepted knowledge promotion.
- `docs/testing/smoke-runs/video-analysis-learning-report-20260513-first-smoke-batch.md`
  as the confirmed bounded learning-report example.

Video observations remain review input only. Direct accepted knowledge
promotion requires separate claim review.

Status:

- YouTube link to metadata source references plus sanitized video learning
  report is confirmed by #137 / PR #145.
- The confirmed path covers bounded representative review, metadata source
  references, no raw media commit, and sanitized reporting.
- It does not confirm accepted curated knowledge generation, move recognition,
  move-frequency analytics, or final observation runtime.

## Entrypoint: Article URL

An article URL may become source metadata. Article ingest creates source
metadata, extracted claim candidates, and review notes. It does not
automatically create accepted knowledge.

Use:

- `workflows/ingest-article.md` for source metadata and claim extraction.
- `workflows/review-claims.md` before curated promotion.
- `docs/testing/smoke-runs/2026-05-01-hermes-assisted-mizen-article-ingest.md`
  as the partially confirmed article-ingest smoke example.

Do not store full copyrighted article text by default. Do not copy long
verbatim excerpts. Use short neutral summaries and claim-level paraphrases.

Exact current facts do not go into curated knowledge when current-fact
authority surfaces cover them. Route exact current values, current roster
facts, and current patch facts through the current-fact authority path.

Status:

- Article URL plus maintainer-provided context to source, claims, and
  unresolved review was partially confirmed by the Hermes-assisted Japanese
  article ingest smoke.
- Live URL fetch or full extraction to source, claims, and review is not fully
  end-to-end validated.

## Entrypoint: Local Article Or Maintainer Note

Local articles, notes, and maintainer research notes may become
`maintainer_note` source metadata or review candidates. They must still follow
source metadata, claim extraction, evidence, volatility, patch sensitivity, and
review boundaries.

Use:

- `workflows/ingest-article.md` for article or note ingest.
- `workflows/review-claims.md` for accepted, hold, rejected, or deprecated
  decisions.

Hermes output remains draft input if used. Hermes memory, sessions, local
skills, Curator output, logs, caches, checkpoints, credentials, cookies, and
local state are not repo evidence.

Current facts still route to current-fact authority surfaces. Local notes are
not authority by themselves.

Status:

- Workflow is defined.
- Broad representative end-to-end coverage is not yet proven.

## Confirmed Vs Not-Yet-Confirmed Matrix

| Entrypoint | Existing workflow | Current proof status | Confirmed | Not yet confirmed |
|---|---|---|---|---|
| Raw local video | `workflows/ingest-video.md` | not fully end-to-end validated | observation workflow shape and boundaries | raw local video to observation to claim review to accepted/hold/rejected terminal state |
| YouTube/video link | `workflows/ingest-video.md`, #137 report | partially confirmed | bounded review, metadata source refs, no raw media commit, sanitized learning report | accepted curated knowledge, move recognition, move frequency |
| Article URL + maintainer context | `workflows/ingest-article.md`, article smoke report | partially confirmed | source/claims/review artifact path with maintainer-provided context | live fetch/full extraction end-to-end |
| Local article/note | `workflows/ingest-article.md` | workflow defined | candidate path and review boundary | broad representative validation |

## End-To-End Proof Suite Needed

A real proof of repository quality requires representative end-to-end
validation, not only documentation.

"All patterns" should be treated as entrypoint families and terminal-state
classes, not every possible source variant. The suite should prove that inputs
reach the correct terminal state:

- accepted curated knowledge
- current-fact authority route
- review-only hold
- rejected unsafe
- sanitized report only

It should not prove that every input becomes accepted knowledge.

Recommended future validation issues:

- Article URL end-to-end knowledge promotion validation
- Local article/note end-to-end knowledge promotion validation
- YouTube/video link end-to-end observation-to-claim validation
- Raw local video end-to-end observation-to-claim validation

Each future validation issue should define:

- representative input count
- allowed sources
- expected repo artifacts
- forbidden artifacts
- terminal states to prove
- validators to run

## Proposed End-To-End Validation Matrix

| Future validation | Representative inputs | Expected terminal states | Must not happen |
|---|---|---|---|
| Article URL E2E | 1 official/current-fact-ish source, 1 community strategy article | source metadata, claims, review note, accepted/hold/rejected decisions | full article copy, unreviewed curated knowledge, current facts bypassing authority |
| Local article/note E2E | 1 maintainer note | `maintainer_note` source, claim candidates, review decision | private note as authority without review |
| YouTube/video link E2E | 1 gameplay or coaching link | video source metadata, sanitized observation/report, claim candidate or hold | raw video commit, transcript commit, accepted move facts from video |
| Raw local video E2E | 1 maintainer-local clip | observation artifact or held report, claim candidate or rejected/hold decision | raw media commit, exact frame facts from video, public behavior change |

## Non-Goals

- No ingest implementation.
- No external fetch.
- No Hermes run.
- No raw media.
- No source artifacts.
- No claim artifacts.
- No observation artifacts.
- No curated pages.
- No validators.
- No public `sf6-agent` behavior change.
- No `official_raw` change.
- No #133 reopen.

## Next-Step Recommendation

After #153, create a separate end-to-end validation tracking issue if the
maintainer wants proof beyond documentation.

Do not start end-to-end validation in #153. Do not treat #153 as proof that all
ingest paths work. This guide records the entrypoints, current proof status,
and the proof suite needed next.
