# Video Observation v2.2 Plan

## Purpose

This document plans video observation policy and future wrapper sequencing for
v2.2. It is planning-only documentation.

Video observation supports future knowledge-growth workflows by turning video
sources into reviewable repo artifacts. Video sources may provide source
metadata, segment references, observed events, uncertainty, and review inputs.
They do not become canonical SF6 knowledge automatically.

Video observations are observation-only until reviewed and promoted through an
accepted repo path. They do not override packaged frame-current `official_raw`.
Exact current facts remain grounded in `data/exports/`, `data/roster/`, and
derived frame-current runtime assets.

Codex and Hermes analysis output is draft input until converted into reviewed
repository artifacts under issue scope, validators, PR review, and merge.

## Relationship To Article Ingest Planning

Article ingest and video observation share source, review, and promotion
ideas: source metadata should be separated from candidate knowledge, review
status must be explicit, and promotion requires an in-scope repo artifact plus
validation.

Video observation remains a separate artifact family because video has
different raw media, inference, segment, timestamp, observation, and copyright
boundaries. Article claims and video observations should not be collapsed into
one artifact type. A future promotion issue may connect them through reviewed
claims, but the source families should remain distinct.

## Artifact Destinations

Future video observation work should keep video-related artifacts separated by
role.

### `knowledge/sources/videos/`

Use this destination for video source records and source-level review inputs:

- source metadata
- source URL or stable reference
- title, channel, creator, and publication date when available
- retrieval or observed date
- language and topic tags
- media access notes
- copyright and raw media storage boundary

Do not store raw video, frames, screenshots, contact sheets, browser cache, or
full transcripts by default.

### `knowledge/evidence/video-observations/`

Use this destination for observation artifacts:

- observation artifact metadata
- source reference
- segment reference
- timestamp or time range
- observed event
- uncertainty and confidence
- what was directly observed
- what was not inferred
- review status

Video observation artifacts are review inputs. They are not accepted strategy
knowledge, matchup knowledge, combo verdicts, or current-system authority by
default.

### `knowledge/review/`

Use this destination for maintainer review and promotion decisions:

- reviewer notes
- promotion decisions
- hold or reject reasons
- validator results
- conflict notes
- follow-up issue references

Review artifacts should state whether an observation remains review-only,
supports a candidate claim, or requires a hold or refresh workflow.

## Observation Artifact Requirements

Future observation artifacts should record at least:

- observation identifier
- source identifier or source reference
- segment reference
- timestamp or time range
- observed event
- observation confidence
- uncertainty notes
- inference boundary
- review status
- storage and copyright boundary
- promotion target, if any

When using `contracts/video-observation.schema.json`, keep the segment track
and confidence model aligned with that schema or document why a replacement
schema is needed before wrapper implementation.

## Boundaries

Video observations are observation-only until reviewed and promoted.

They must not silently promote into curated knowledge. A reusable conclusion
needs a separate reviewed claim or another explicit promotion target.

Do not infer exact move, frame, or current-system facts from video alone.
Video observations alone must not become exact current facts.

Do not treat these as final authority without review:

- match verdicts
- combo verdicts
- route verdicts
- damage verdicts
- coaching conclusions
- strategy conclusions

Observed damage labels are not current-system authority. Training UI
observations can be eval or review context only unless accepted by a separate
authority path. If a video observation conflicts with packaged current facts,
the result is a hold, conflict note, review item, or refresh workflow signal,
not silent replacement of `official_raw`.

Hermes memory, sessions, local skills, Curator output, browser state, local
media scratch, and private local state are not video evidence.

## Schema-Aware Validator Prerequisites

Before implementing video observation wrappers, add or plan validators for:

- `contracts/video-observation.schema.json` alignment or replacement
- required observation fields
- source and segment reference integrity
- no raw media, screenshots, contact sheets, browser cache, or full transcript
  storage
- observation-only boundary text
- no exact current facts inferred from video observations
- review and promotion status
- local scratch, cache, media, session, credential, token, and secret state
  not being committed
- conflict handling when observations appear to contradict packaged
  frame-current authority

Wrapper implementation should wait until these validation boundaries are clear
enough to make assisted video observation artifacts reviewable.

## Copyright And Raw Media Boundaries

Do not store raw video, frames, screenshots, contact sheets, browser cache, or
full transcripts by default.

Temporary media inspection must use repo-external scratch space. That scratch
space is not a repo artifact and must be cleaned or excluded from commits.

Allowed video observation artifacts should store:

- source metadata
- stable references or URLs
- segment references
- timestamps or time ranges
- paraphrased observations
- uncertainty and confidence notes
- review notes

Direct transcript quotes should be minimal and only when necessary for review.
Future wrappers must not dump transcripts, captions, frames, screenshots, or
contact sheets into repo artifacts.

## Handling Stale Video And Combo Review Debt

Existing stale video or combo review work, such as PR #83 and Issue #82,
should be treated as reference-only debt until re-reviewed.

Future work may rebase and align that work with this video observation plan, or
it may close the old branch and migrate useful notes into new scoped artifacts.
Either path requires renewed review under current contracts, validators, and
issue scope.

Do not treat old draft PR observations, unresolved branch mapping notes, or
observed damage labels as canonical knowledge without renewed review.

## Future Wrapper Issue Sequence

Recommended future issue sequence:

1. Align or update the video observation schema.
2. Add a schema-aware video observation validator.
3. Add a video source metadata contract or template.
4. Add a video observation artifact template.
5. Add a raw media, transcript, and scratch-state boundary validator.
6. Add Hermes/Codex video observation wrapper guidance.
7. Add a video observation smoke fixture.
8. Add a promotion workflow for reviewed observations.
9. Re-review stale PR #83 and Issue #82 under this planning boundary.

Each issue should state its artifact destinations, validators, non-goals, and
promotion boundaries. Wrapper issues should remain separate from observation
promotion issues unless an issue explicitly allows both.

## Non-Goals For v2.2 Planning

This plan does not implement video observation wrappers or article ingest
wrappers. It does not store raw video, frames, screenshots, contact sheets,
browser cache, or full transcripts. It does not infer exact current facts from
video observations, promote observations directly into curated knowledge,
change public `sf6-agent` behavior, add Hermes operational prompts, change
frame-current facts, modify generated outputs, modify `.dist`, modify
normalization assets, rewrite historical smoke reports, merge or modify PR
#83, or close #94.
