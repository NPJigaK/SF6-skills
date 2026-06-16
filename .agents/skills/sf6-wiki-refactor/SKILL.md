---
name: sf6-wiki-refactor
description: Use when the SF6 LLM Wiki needs restructuring, recompilation, merge/split/rename/deprecate of wiki pages, hub page creation, index redesign, orphan integration, duplicate concept cleanup, synthesis rewrite, or directory reorganization. This skill edits wiki/ only and never edits raw/.
---

# SF6 Wiki Refactor

## Role

You refactor the `wiki/` layer as LLM-maintained compiled knowledge.

Karpathy-style rule:

- `raw/` is source of truth and must not be rewritten.
- `wiki/` is compiled knowledge owned and maintained by the LLM.
- If the current wiki topology is weak, stale, duplicated, hard to navigate, or hard to query, improve it.

Do not preserve the existing wiki structure by default.
Preserve evidence and provenance; refactor the compiled wiki.

## Required reads

1. `AGENTS.md`
2. `wiki/index.md`
3. recent `wiki/log.md`
4. relevant source pages in `wiki/sources/`
5. relevant concept/entity/synthesis/question/output/review pages
6. relevant raw manifest / validation / derived output only when facts or numeric values are involved

## Refactor triggers

Use this skill when any of the following is true:

- duplicate or overlapping concepts exist
- orphan pages should be connected or merged
- a concept needs a hub page
- an output or question should become a synthesis
- a synthesis is stale or contradicted by newer sources
- page names or directories no longer match how the wiki is used
- source families need clearer grouping
- index.md has become too dense to be a navigation surface
- repeated queries require the same multi-hop reasoning
- lint finds missing backlinks, stale claims, or missing concept/entity pages
- ingest touches multiple related pages and reveals a better topology
- durable outputs or question pages contain reusable knowledge that should be promoted into core wiki pages

## Good topology heuristics

Prefer a wiki that is:

- easier for future LLM queries to navigate
- less duplicated
- more source-grounded
- clearer about official vs community vs derived evidence
- clearer about active / deprecated / review-needed pages
- better connected through backlinks
- better represented in `wiki/index.md`
- organized by reuse pattern, not only ingestion order

Common SF6 hubs may include, when supported by existing content:

- `frame-data`
- `battle-change`
- `terms`
- `drive-system`
- `battle-system`
- `characters`
- `combo-damage`
- `source-provenance`
- `review-queue`

Do not create hubs just because this list exists.
Create or update a hub only when it improves navigation, grounding, repeated query quality, or synthesis reuse.

## Allowed wiki refactors

You may:

- merge duplicate concept/entity pages
- split overloaded pages
- rename pages for clearer slugs
- create hub pages
- create or update synthesis pages
- deprecate stale pages using `status: deprecated`
- mark contradicted pages using `status: contradicted` or `review-needed`
- move reusable question/output content into syntheses when it is durable reasoning
- update backlinks
- update aliases / tags / related frontmatter
- update `wiki/index.md`
- append to `wiki/log.md`
- create review notes for uncertain factual issues

## Hard boundaries

Never:

- edit `raw/`
- silently delete evidence
- silently delete review history
- turn inference into source fact
- hide contradictions
- overwrite official evidence with community evidence
- treat validation-failed derived output as authoritative
- make large wiki topology changes without updating index/log
- use model memory to fill missing facts
- use subagent prose as evidence

## Refactor workflow

1. Diagnose the current topology.
2. Produce a short refactor plan before editing:
   - pages to merge
   - pages to split
   - pages to rename
   - new hub/synthesis pages
   - pages to deprecate
   - backlinks/index updates
   - review notes needed
3. Apply safe wiki-only refactors.
4. For uncertain factual conflicts, create or update `wiki/reviews/` instead of resolving silently.
5. Update all affected backlinks.
6. Update `wiki/index.md`.
7. Append to `wiki/log.md`.
8. Report:
   - changed files
   - moved/merged/split pages
   - deprecated pages
   - evidence gaps
   - human-review items
   - open questions

## Review note frontmatter

When creating a refactor plan review note, use:

```yaml
---
type: review
review_type: refactor_plan
status: open
created: YYYY-MM-DD
updated: YYYY-MM-DD
severity: P2
confidence: medium
related: []
sources: []
---
```

Use `severity: P1` if the refactor plan involves evidence conflicts, source authority, validation failure, or value changes.

## Anti-goals

- Do not preserve the current directory structure just because it exists.
- Do not create a new page when an existing page should be upgraded.
- Do not leave question answers stranded if they should become synthesis.
- Do not hide contradictions.
- Do not silently delete evidence.
- Do not perform raw capture or raw update in this skill.
