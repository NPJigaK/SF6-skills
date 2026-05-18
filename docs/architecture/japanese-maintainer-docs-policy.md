# Japanese Maintainer Documentation Policy

SF6 Knowledge Agent Kit is maintained primarily for Japanese-speaking maintainers while preserving English-compatible repository structure.

This policy clarifies how maintainer-facing docs can use Japanese prose without creating duplicate canonical sources of truth.

## 日本語要約

このrepoでは、メンテナー向けの説明文やworkflow本文は日本語を正本として書いてよいです。

ただし、metadata key、artifact ID、schema enum、filename、validator contract、command名などは英語互換を保ちます。

`AGENTS.md` や workflow のようにagentが実際に読む入口では、必須ルールを `.ja.*` companion に逃がさず、entrypoint本体に書きます。

`knowledge/curated/` は英語版と日本語版で二重正本化しません。

## Core Principle

Maintainer-facing prose may be Japanese-first when it improves repository operation.

Do not make English the automatic canonical prose language and Japanese the automatic companion language. Use the language that best supports the canonical surface and its maintainers.

Do not create duplicate canonical English/Japanese source-of-truth pages.

## Japanese Canonical Prose

Japanese prose may be canonical for:

- maintainer workflows
- source summaries
- review notes
- curated explanations
- image and video observation notes
- maintainer notes for Japanese sources

These artifacts remain canonical because of their paths, metadata, source references, review status, and validation, not because they are written in English.

## English-compatible Structure

Keep these English-compatible and stable:

- metadata keys
- artifact IDs
- schema enum values
- filenames and path slugs
- generated markers
- validator contracts
- package interfaces
- command names and script names

Japanese prose must not require Japanese-only metadata keys, schema enum values, filenames, or validator contracts.

## Required Entrypoints

Required repo behavior must live in the canonical entrypoints that agents actually read.

Do not move required rules only into `.ja.*` companion files.

Examples:

- `AGENTS.md` must contain required repo guidance directly.

Localized companions may explain or summarize these entrypoints for humans, but they are not enough for required agent behavior unless a later architecture decision changes discovery behavior.

## Knowledge Pages

Do not duplicate `knowledge/curated/` pages only to create separate English and Japanese canonical versions.

A curated page may be written in Japanese when that is the natural operating language. Its canonical status comes from its repository path, metadata, source references, review status, and validation.

If an English explanation is useful later, prefer a concise maintainer note, generated distribution surface, or localized public doc rather than a second canonical curated page.

## Localized Companion Files

`.ja.*` files may be used for human-facing localized documentation when useful, especially:

- architecture explanations
- distribution docs
- testing docs
- quickstart docs
- human-facing summaries

When a `.ja.*` file is added for maintainer-facing docs, it should state whether it is:

- canonical
- localized companion
- summary

If it is a localized companion, it should identify the source file it follows.

Example front matter shape:

```yaml
---
language: ja
localization_role: localized_companion
localized_from: docs/architecture/example.md
sync_policy: meaning_equivalent
review_after: "2026-08-01"
---
```

This policy does not require adding front matter to every localized doc immediately. It defines the expected direction when localized companions are introduced.

## Maintainer-critical English Docs

Maintainer-critical docs should not remain English-only when that blocks Japanese-speaking maintainers from understanding repository operation.

For each maintainer-critical doc, choose one of these approaches:

1. Write the canonical prose in Japanese while keeping paths, metadata, commands, and schema terms English-compatible.
2. Keep the canonical prose in English and add a `.ja.*` human-readable companion with a clear localization role.
3. Add an inline Japanese summary when a full companion would be too heavy.

This does not mean every file needs a strict 1:1 translation. Fast-changing workflows should prefer Japanese-first canonical prose or an inline Japanese summary unless a sync policy exists.

## Workflows

Frequently changing maintainer workflows should avoid strict English/Japanese translation pairs unless a sync policy exists.

A workflow may be Japanese-first canonical text instead of maintaining separate English and Japanese versions.

This is especially appropriate for workflows primarily used by Japanese-speaking maintainers, such as Japanese article ingest, video observation, review, and media scratch/cache handling.

## Distribution

Localized public docs such as `README.ja.md` or agent-specific quickstarts may be considered later.

Do not create `sf6-agent-ja` only for language localization unless a later architecture decision shows that a separate adapter is necessary and can be validated without duplicate source-of-truth drift.

## Relationship To Language Policy

This policy refines `docs/architecture/language-policy.md` for maintainer documentation.

The repository remains Japanese-first in operation and English-compatible in structure.
