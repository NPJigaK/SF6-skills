# Language Policy

SF6 Knowledge Agent Kit is Japanese-first in operation and English-compatible in structure.

## Japanese-first Operation

Japanese prose is allowed and encouraged for:

- user-facing guidance
- source summaries
- review notes
- curated explanations
- maintainer notes for Japanese sources

When users ask in Japanese, `sf6-agent` should answer in Japanese unless they ask otherwise.

## English-compatible Structure

Keep these English-compatible and stable:

- metadata keys
- artifact IDs
- schema enum values
- filenames and path slugs
- generated markers
- validator contracts
- package and installer interfaces

## Canonical Knowledge

Do not duplicate canonical knowledge pages only to create separate English and Japanese versions.

A curated page may use Japanese prose when that is the most natural operating language. The page remains canonical because of its artifact path, metadata, source references, review status, and validation, not because of English prose.

## Localized Files

`.ja.*` files may be used for human-facing localized documentation when they improve usability.

Examples that may be appropriate:

- `README.ja.md`
- `docs/distribution/agents/codex.ja.md`

Avoid `.ja.*` files for canonical knowledge pages or core workflows unless an architecture decision defines how canonical and localized variants stay synchronized.

## Public Adapter

Keep `skills/sf6-agent/` as the single public adapter for now.

Do not create `sf6-agent-ja` unless a later architecture decision shows that a separate Japanese adapter is necessary and can be validated without duplicate source-of-truth drift.

## Source Ingest

Japanese source ingest should summarize and review in Japanese by default when useful.

The repo may store Japanese summaries, Japanese review notes, and Japanese claim explanations. It must not store full copyrighted articles, transcripts, or large excerpts by default.

## Current Facts

Language policy does not change current-fact authority.

Exact current facts remain grounded in `data/exports/`, `data/roster/`, and derived frame-current runtime assets.
