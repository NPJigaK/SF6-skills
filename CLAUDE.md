# LLM Wiki Agent Instructions

## Core Model

This repository is a Karpathy-style LLM-maintained knowledge base.

The human curates sources, asks questions, reviews important changes, and
decides direction. The LLM writes and maintains the wiki.

Follow [ROADMAP.md](ROADMAP.md) for the domain-independent implementation plan.
Do not introduce domain-specific architecture until the base raw/wiki/schema
pattern is implemented and reviewed.

## Layers

- `raw/`: immutable source material. Never edit files in `raw/`.
- `wiki/`: LLM-generated and LLM-maintained Markdown wiki.
- `wiki/index.md`: content-oriented catalog and first navigation surface.
- `wiki/log.md`: chronological append-only activity log.
- `AGENTS.md` / `CLAUDE.md`: schema and workflow instructions for LLM agents.

## Page Types

- `wiki/sources/`: one summary page per raw source.
- `wiki/concepts/`: concepts and reusable ideas.
- `wiki/entities/`: people, companies, projects, tools, papers, datasets, and other entities.
- `wiki/syntheses/`: higher-level analysis across multiple pages or sources.
- `wiki/questions/`: useful answered questions filed back from chat.
- `wiki/outputs/`: durable reports, slide decks, charts, canvases, and other outputs.
- `wiki/reviews/`: lint results, contradictions, stale claims, and review notes.
- `wiki/templates/`: reusable page templates.

## Non-Negotiable Rules

1. Never modify files in `raw/`.
2. Prefer updating existing wiki pages over creating duplicates.
3. Every important claim must be traceable to a raw source or wiki source page.
4. Mark uncertainty explicitly.
5. Record contradictions and stale claims instead of hiding them.
6. Update `wiki/index.md` after every meaningful ingest, new page, or major page update.
7. Append to `wiki/log.md` after every ingest, query, output, lint pass, or schema change.
8. Useful query results must be filed back into `wiki/questions/`, `wiki/syntheses/`, or `wiki/outputs/`.
9. Report changed files and unresolved questions at the end of each task.
10. Keep the base pattern domain-independent until a later explicit domain design step.

## Ingest Workflow

When asked to ingest a source:

1. Read this file.
2. Read `wiki/index.md`.
3. Read recent entries in `wiki/log.md`.
4. Read the requested raw source.
5. Do not edit `raw/`.
6. Create or update one page in `wiki/sources/`.
7. Update relevant concept, entity, or synthesis pages.
8. Create new pages only when they are useful and not duplicates.
9. Add backlinks and source references.
10. Flag contradictions, stale claims, and uncertainty.
11. Update `wiki/index.md`.
12. Append to `wiki/log.md`.
13. Report changed files and open questions.

## Query Workflow

When asked to answer a question:

1. Read `wiki/index.md` first.
2. Search the wiki only if the index is insufficient.
3. Read relevant source, concept, entity, synthesis, question, and output pages.
4. Answer with citations to wiki pages or source pages.
5. State uncertainty and missing evidence clearly.
6. If the answer is durable, save it to `wiki/questions/`, `wiki/syntheses/`, or `wiki/outputs/`.
7. Update `wiki/index.md` if a page is created or materially changed.
8. Append to `wiki/log.md`.
9. Report changed files and unresolved questions.

## Output Workflow

When asked to create a durable output:

1. Read `wiki/index.md`.
2. Read relevant wiki and source pages.
3. Create the requested output under `wiki/outputs/`.
4. Cite relevant wiki/source pages.
5. Keep the output readable as plain Markdown where possible.
6. Update `wiki/index.md`.
7. Append to `wiki/log.md`.
8. Report changed files.

## Lint / Health Check Workflow

When asked to run a wiki health check:

1. Read this file.
2. Read `wiki/index.md`.
3. Read recent entries in `wiki/log.md`.
4. Check for broken wikilinks, orphan pages, duplicate pages, missing index
   entries, missing frontmatter, missing backlinks, contradictions, stale claims,
   uncited important claims, weak summaries, missing concept/entity pages, data
   gaps, and suggested next sources/questions.
5. Repair safe structural issues.
6. Do not invent facts.
7. For uncertain factual issues, create a review note in `wiki/reviews/`.
8. Update `wiki/index.md`.
9. Append to `wiki/log.md`.
10. Report changed files and items requiring human review.

## Git And Tooling

- Use Git diff as the review surface for LLM-maintained wiki changes.
- Use `rg` for local text search.
- Use simple file-based CLI tools only when they exist.
- Do not depend on Obsidian CLI, Obsidian APIs, vector databases, graph databases,
  hosted RAG systems, or MCP-first architecture in the base implementation.

