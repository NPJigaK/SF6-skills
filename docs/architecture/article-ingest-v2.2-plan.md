# Article Ingest v2.2 Plan

## Purpose

This document plans article ingest policy and future wrapper sequencing for
v2.2. It is planning-only documentation.

Article ingest supports future knowledge-growth workflows by turning article
sources into reviewable repo artifacts. Article sources may provide source
metadata, excerpt-safe summaries, candidate claims, and review inputs. They do
not become canonical SF6 knowledge automatically.

Web and article sources do not override packaged frame-current `official_raw`.
Exact current facts remain grounded in `data/exports/`, `data/roster/`, and
derived frame-current runtime assets.

Codex and Hermes analysis output is draft input until converted into reviewed
repository artifacts under issue scope, validators, PR review, and merge.

## Artifact Destinations

Future article ingest work should keep article-related artifacts separated by
role.

### `knowledge/sources/articles/`

Use this destination for source records and article-level review inputs:

- source metadata
- source URL or stable reference
- title, author, publisher, and publication date when available
- access and retrieval notes
- language and topic tags
- summary or excerpt-safe notes only

Do not store full article text by default.

### `knowledge/evidence/claims/`

Use this destination for candidate claim artifacts extracted from article
sources:

- candidate claim text in repo prose
- claim scope
- source references
- confidence and uncertainty
- current-fact sensitivity
- patch sensitivity
- review status

Candidate claims are not final knowledge. They are review inputs.

### `knowledge/review/`

Use this destination for maintainer review and promotion decisions:

- reviewer notes
- promotion decisions
- hold or reject reasons
- validator results
- conflict notes
- follow-up issue references

Review artifacts should make the target repo surface explicit when a claim is
promoted.

## Source Metadata Requirements

Future article source metadata should include:

- source identifier
- source URL or stable reference
- publisher or source name
- author when available
- publication date when available
- retrieval or observed date
- language
- topic
- claim categories
- access notes
- copyright and storage boundary

When publication date is unavailable, record the retrieval or observed date
and mark the source as date-limited. Do not infer publication metadata without
review.

## Candidate Claim Extraction Boundaries

Article ingest should extract candidate claims, not final knowledge.

Candidate claims must be separated from source summaries. A source summary
captures what the article appears to discuss. A candidate claim is a specific
statement proposed for review.

Each candidate claim should mark whether it is:

- stable concept
- strategy or meta
- current-fact sensitive
- patch-sensitive
- unsupported or needs review

Exact current facts require an accepted authority path before promotion.
Article-derived values must not become exact current facts by default.

Web or article claims must not override packaged `official_raw`. If an article
conflicts with packaged current facts, the result is a hold, conflict note, or
frame-data refresh signal, not silent replacement of packaged authority.

Hermes memory, sessions, local skills, Curator output, browser state, and
private local state are not article evidence.

## Review And Promotion Requirements

Candidate claims require review before curated promotion.

Before promotion:

- the target repo surface must be explicit
- the target issue scope must allow the promotion
- source references and uncertainty must be retained
- validators required by the target surface must be listed and run
- current-fact conflicts must be resolved by hold or refresh workflow
- copyright and storage boundaries must be checked

Promotion may target a reviewed repo surface such as curated knowledge,
review notes, workflow documentation, contracts, or validators. The target
surface determines the required checks.

Hermes or Codex analysis output is draft input. It is not canonical evidence
until distilled into reviewed repo artifacts.

## Copyright Boundaries

Do not store full copyrighted article text by default.

Allowed article ingest artifacts should store:

- source metadata
- stable references or URLs
- short summaries
- paraphrased notes
- minimal direct quotes only when necessary for review
- reviewed candidate claims
- review decisions

Future wrappers must not dump article content into repo artifacts. If a direct
quote is necessary, keep it minimal, label it as quoted source text, and keep
it tied to a review purpose.

## Validator Prerequisites Before Wrapper Implementation

Before implementing article ingest wrappers, add or plan validators for:

- article source metadata schema
- article candidate claim schema or validator
- review and promotion artifact validator
- copyright and storage boundary validator
- source path and destination validator
- no-full-article-text scan
- web/current-fact conflict guard
- required source reference and retrieval-date checks
- no local browser/session/cache/secret state scan

Wrapper implementation should wait until these validation boundaries are clear
enough to make generated or assisted article artifacts reviewable.

## Future Wrapper Issue Sequence

Recommended future issue sequence:

1. Add article source metadata contract.
2. Add article candidate claim contract or validator.
3. Add article review artifact template and validator.
4. Add copyright and no-full-article-text boundary scan.
5. Add Hermes/Codex article ingest wrapper guidance.
6. Add article ingest smoke fixture.
7. Add promotion workflow for reviewed claims.

Each issue should state its artifact destinations, validators, non-goals, and
promotion boundaries. Wrapper issues should remain separate from claim
promotion issues unless an issue explicitly allows both.

## Non-Goals For v2.2 Planning

This plan does not implement article ingest wrappers. It does not run live web
research, store full article text, promote unreviewed article claims, change
public `sf6-agent` behavior, change frame-current facts, or add Hermes
operational prompts.
