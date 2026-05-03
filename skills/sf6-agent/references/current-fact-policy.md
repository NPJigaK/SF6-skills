# Current Fact Policy

Exact current SF6 facts are answered from packaged frame-current assets only.

## Authority

- Canonical repo sources: `data/exports` and `data/roster`.
- Packaged runtime assets: `assets/frame-current/`.
- Runtime manifest: `assets/frame-current/runtime_manifest.json`.

The packaged assets are generated from repo sources during distribution build. At runtime, the adapter should not need `data/exports` or `data/roster` to answer normal user questions.

## Lookup Rules

1. Resolve a packaged `character_slug` from the user question or clear thread context.
2. Read `assets/frame-current/runtime_manifest.json`.
3. Read `assets/frame-current/published/<character_slug>/snapshot_manifest.json`.
4. Use only datasets whose `publication_state` is `available`.
5. Read `official_raw.json` first for exact current values.
6. Use `derived_metrics.json` only for mechanical calculations anchored to `official_raw`.
7. Use `supercombo_enrichment.json` only as supplemental context and never as an override.

## Hold Conditions

Use `unresolved / hold` when:

- The character is not packaged.
- The move or variant cannot be resolved.
- The requested field is unavailable.
- The answer would require manual-review rows, raw snapshots, normalized working data, scraping, or patch audit work.
- A value appears only in supplemental enrichment and not in the official published rows.

## System-Mechanics Current Facts

Some exact current questions are about system mechanics rather than a single packaged move field.

Examples include route-level combo damage formulas, minimum guarantee values, system action modifiers, and exception rules that are not directly available as packaged frame-current fields.

Answer these only when the requested exact value is available in packaged frame-current assets. If the value is not packaged, use `unresolved / hold`.

Do not infer exact system-mechanics values from generated concept references, article claims, video observations, or review candidates.

## Provenance In Answers

When an answer depends on exact current data, mention the relevant packaged dataset names when useful. Do not expose internal repository paths as if the user must have the repository checkout.
