# Karpathy-Style LLM Wiki Roadmap

Status: draft roadmap
Created: 2026-05-26
Scope: domain-independent LLM Knowledge Base / LLM Wiki design

## Purpose

This roadmap defines a domain-independent implementation plan for a
Karpathy-style LLM Knowledge Base / LLM Wiki.

This document intentionally does not include any domain-specific architecture,
schemas, answer rules, data model, or product behavior. Domain-specific design
comes only after this base pattern is implemented and reviewed.

The target is not a conventional app, database-backed RAG system, or
domain-specific runtime. The target is a plain-file knowledge repository where:

```text
Human curates sources and asks questions.
LLM compiles, writes, links, maintains, lints, searches, and outputs.
Obsidian is the frontend.
Markdown files are the durable memory.
CLI tools are the LLM's hands.
```

Compatibility with any existing implementation is not a goal of this roadmap.
Git history is the rollback mechanism.

## Source Basis

This roadmap is based on the user's "Karpathy式 LLM Knowledge Base / LLM Wiki
設計実装まとめ" and the current public Karpathy `llm-wiki` gist.

Source links:

- [Karpathy llm-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Farzapedia / file collection memory](https://x.com/karpathy/status/2040572272944324650)
- [LLM Knowledge Bases post](https://x.com/karpathy/status/2039805659525644595)
- [Manual incremental compilation reply](https://x.com/karpathy/status/2039812403962253744)
- [Obsidian CLI reply](https://x.com/karpathy/status/2039814066575917263)

## Design Boundary

The first implementation must stay inside the Karpathy-style base pattern:

- generic `raw/`
- generic `wiki/`
- generic schema files
- generic `index.md`
- generic `log.md`
- generic ingest / query / output / lint workflows
- optional small file-based CLI tools
- optional Obsidian viewing workflow

The first implementation must not include:

- domain-specific page types
- domain-specific answer policy
- domain-specific validators
- domain-specific structured databases
- domain-specific runtime behavior
- domain-specific UI
- domain-specific retrieval architecture
- product-specific automation

## Karpathy-Stated Core

### 1. LLM Wiki Is Not Ordinary RAG

Ordinary RAG retrieves chunks from raw documents at query time and reconstructs
answers repeatedly.

The LLM Wiki pattern is different:

- raw sources are added to a curated collection
- the LLM reads new sources
- the LLM compiles the source into a persistent Markdown wiki
- the LLM updates entity pages, concept pages, summaries, contradictions, and
  cross-references
- knowledge accumulates in the wiki instead of being re-derived from scratch on
  every question

The wiki is a persistent, compounding artifact.

### 2. Three Layers

The architecture has three layers:

```text
1. Raw sources
2. The wiki
3. The schema
```

`raw/` is the immutable source of truth. The LLM reads raw files but never
modifies them.

`wiki/` is a directory of LLM-generated Markdown files. The LLM owns this layer:
it creates pages, updates pages, maintains cross-references, and keeps the wiki
consistent.

The schema is a file such as `AGENTS.md` or `CLAUDE.md` that tells the LLM how
the wiki is structured and what workflows to follow.

### 3. Role Split

Human:

- curates sources
- chooses what matters
- asks questions
- reviews important changes
- directs analysis
- checks Git diffs

LLM:

- summarizes sources
- creates pages
- updates pages
- maintains cross-references
- updates `index.md`
- appends `log.md`
- answers questions from the wiki
- files useful answers back into the wiki
- runs health checks
- produces outputs

### 4. Obsidian Is The IDE

Obsidian is the human-facing frontend for browsing the file collection:

- reading pages
- following wikilinks
- inspecting graph view
- viewing outputs
- using optional plugins such as Marp or Dataview

Obsidian is not the knowledge base. The knowledge base is the directory of plain
files.

### 5. Fully Autonomous Ingest Is Not The Starting Point

Early ingest should be source-by-source with the human in the loop.

Batch ingest and more automation may come later, after the schema, page shapes,
and review expectations are stable.

## Implementation Judgments

The following details are not fixed by Karpathy as universal requirements, but
they are practical choices that preserve the pattern.

### 1. Plain Directory Structure

Use a small, obvious directory tree:

```text
llm-wiki/
  AGENTS.md
  CLAUDE.md
  README.md

  raw/
    articles/
    papers/
    repos/
    datasets/
    images/
    assets/
    transcripts/
    notes/

  wiki/
    index.md
    log.md

    sources/
    concepts/
    entities/
    syntheses/
    questions/
    outputs/
      reports/
      slides/
      charts/
      canvases/
    reviews/
    templates/

  tools/
    kb_search.py
    kb_status.py
    kb_lint.py
    kb_render.py
    kb_ingest_status.py

  scripts/
    normalize_web_clip.py
    extract_pdf_notes.py
    download_assets.py
```

The minimum viable version is:

```text
raw/
wiki/
AGENTS.md
CLAUDE.md
README.md
wiki/index.md
wiki/log.md
```

### 2. Use Frontmatter Where Useful

YAML frontmatter is useful for humans, LLMs, and optional Obsidian Dataview
queries. It should stay simple and editable.

### 3. Keep Tools Small

CLI tools should help the LLM operate on the file tree. They should not become
the source of truth.

Start with simple file-based tooling. Do not introduce vector databases, graph
databases, hosted RAG systems, or MCP-first architecture in the base
implementation.

### 4. Use Git As The Safety Rail

The wiki is just files, so Git provides:

- history
- diffs
- branching
- rollback
- review

LLM-maintained wiki changes should be reviewed through Git diff.

## Raw Layer Design

`raw/` stores human-curated source material.

Examples:

```text
raw/articles/
raw/papers/
raw/repos/
raw/datasets/
raw/images/
raw/assets/
raw/transcripts/
raw/notes/
```

Rules:

- LLMs must not edit files in `raw/`.
- Raw filenames should make date, source, and topic reasonably clear.
- Images should be saved locally when they matter.
- Source metadata can live in frontmatter or a sidecar file.
- Wiki pages should link back to raw sources.

Example raw source frontmatter:

```markdown
---
type: raw_source
source_type: article
title: ""
author: ""
original_url: ""
captured_at: YYYY-MM-DD
status: raw
---
```

## Wiki Layer Design

`wiki/` stores LLM-generated, LLM-maintained compiled knowledge.

Recommended directories:

```text
wiki/sources/
wiki/concepts/
wiki/entities/
wiki/syntheses/
wiki/questions/
wiki/outputs/
wiki/reviews/
wiki/templates/
```

Rules:

- Prefer updating existing pages over creating duplicates.
- Every important claim should be traceable to a source.
- Mark uncertainty explicitly.
- Record contradictions and stale claims instead of hiding them.
- Maintain backlinks and cross-references.
- Add useful query results back into the wiki.
- Update `wiki/index.md` after meaningful page changes.
- Append `wiki/log.md` after ingest, query, output, lint, or schema work.

## Schema Layer Design

`AGENTS.md` and `CLAUDE.md` are the agent-facing operating constitution.

They should define:

- core model
- raw/wiki/schema layer boundaries
- page types
- naming conventions
- wikilink conventions
- frontmatter conventions
- ingest workflow
- query workflow
- output workflow
- lint workflow
- index update rules
- log append rules
- citation/source handling
- uncertainty handling
- contradiction handling
- CLI tool usage
- Git diff reporting

Minimum schema rules:

```markdown
# LLM Wiki Agent Instructions

## Core model

This repository is an LLM-maintained knowledge base.

The human curates sources, asks questions, reviews important changes, and
decides direction. The LLM writes and maintains the wiki.

## Layers

- `raw/`: immutable source material. Never edit files in `raw/`.
- `wiki/`: LLM-generated and LLM-maintained Markdown wiki.
- `wiki/index.md`: content-oriented catalog.
- `wiki/log.md`: chronological append-only activity log.

## Non-negotiable rules

1. Never modify `raw/`.
2. Prefer updating existing wiki pages over creating duplicates.
3. Every important claim must be traceable to a source.
4. Mark uncertainty explicitly.
5. Update `wiki/index.md` after every meaningful ingest or new page.
6. Append to `wiki/log.md` after every ingest, query, output, or lint pass.
7. Useful query results should be filed back into the wiki.
8. Report all changed files at the end of each task.
```

## Special Files

### `wiki/index.md`

`index.md` is content-oriented. It catalogs wiki pages with links, one-line
summaries, and optional metadata.

The LLM reads it first when answering questions.

Suggested shape:

```markdown
# Wiki Index

## Sources

| Page | Summary | Date | Source type | Status |
|---|---|---:|---|---|

## Concepts

| Page | Summary | Related |
|---|---|---|

## Entities

| Page | Summary | Type |
|---|---|---|

## Syntheses

| Page | Summary | Updated |
|---|---|---:|

## Questions

| Page | Question | Summary | Updated |
|---|---|---|---:|

## Outputs

| Page | Type | Summary | Updated |
|---|---|---|---:|

## Reviews

| Page | Review type | Summary | Status |
|---|---|---|---|
```

Rules:

- Add new wiki pages to the index.
- Update summaries after major page updates.
- Keep the index useful for navigation.
- Use search tools only when the index is insufficient.

### `wiki/log.md`

`log.md` is chronological and append-only.

Suggested shape:

```markdown
# Wiki Log

## [YYYY-MM-DD] schema | Initialize LLM Wiki
- Created:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Notes:
  - Initialized raw/wiki/schema structure.

## [YYYY-MM-DD] ingest | <Source Title>
- Raw source:
  - `raw/articles/<file>.md`
- Created:
  - `wiki/sources/<source>.md`
- Updated:
  - `wiki/index.md`
- Open questions:
  - ...
```

Rules:

- Append only.
- Do not rewrite old entries except to correct obvious formatting mistakes.
- Log ingest, query, output, lint, and schema updates.
- Use consistent entry prefixes so Unix tools can parse recent activity.

## Page Templates

### Source Summary

```markdown
---
type: source
source_type: article
title: ""
author: ""
raw_path: ""
original_url: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
confidence: high
tags: []
related_concepts: []
related_entities: []
---

# Source: <Title>

## One-line summary

...

## Key takeaways

1. ...
2. ...
3. ...

## Important claims

| Claim | Evidence | Confidence | Notes |
|---|---|---|---|
| ... | ... | high | ... |

## Related concepts

- [[concepts/...]]

## Related entities

- [[entities/...]]

## Contradictions or updates to existing wiki

- ...

## Open questions

- ...

## Source notes

- Raw file: `raw/...`
- Original URL: ...
```

### Concept Page

```markdown
---
type: concept
title: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
confidence: medium
sources: []
related: []
tags: []
---

# <Concept>

## Summary

...

## Definition

...

## Why it matters

...

## Key claims

| Claim | Sources | Confidence |
|---|---|---|
| ... | ... | ... |

## Connections

- [[concepts/...]]
- [[entities/...]]

## Contradictions / caveats

...

## Open questions

...
```

### Entity Page

```markdown
---
type: entity
entity_type: person | company | project | tool | paper | dataset | other
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
sources: []
related: []
tags: []
---

# <Entity>

## Summary

...

## Timeline

| Date | Event | Source |
|---|---|---|
| ... | ... | ... |

## Relevant claims

...

## Related concepts

...

## Open questions

...
```

### Synthesis Page

```markdown
---
type: synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
sources: []
related: []
tags: []
---

# <Synthesis Title>

## Executive summary

...

## Core argument

...

## Evidence

| Point | Supporting sources | Confidence |
|---|---|---|
| ... | ... | ... |

## Comparison

| Dimension | A | B | Notes |
|---|---|---|---|
| ... | ... | ... | ... |

## Implications

...

## Open questions

...

## Pages to update

- [[concepts/...]]
```

### Question Page

```markdown
---
type: question
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
question: ""
sources: []
related: []
---

# Question: <Question>

## Short answer

...

## Evidence

...

## Reasoning

...

## Limits / uncertainty

...
```

### Lint Review

```markdown
---
type: review
review_type: lint
created: YYYY-MM-DD
status: open
---

# Wiki Health Check - YYYY-MM-DD

## Summary

...

## Structural issues

### Broken links

...

### Orphan pages

...

### Missing index entries

...

## Knowledge issues

### Contradictions

...

### Stale claims

...

### Uncited claims

...

## Missing concepts

...

## Suggested new sources

...

## Suggested next questions

...

## Changes made

...

## Requires human review

...
```

## Workflows

### Ingest Workflow

Purpose: integrate one new raw source into the wiki.

Steps:

1. Human adds one source under `raw/`.
2. LLM reads `AGENTS.md` or `CLAUDE.md`.
3. LLM reads `wiki/index.md`.
4. LLM reads recent `wiki/log.md` entries.
5. LLM reads the new raw source.
6. LLM creates a source summary in `wiki/sources/`.
7. LLM finds related concept, entity, and synthesis pages.
8. LLM updates existing pages where appropriate.
9. LLM creates new concept or entity pages only when useful.
10. LLM records contradictions, stale claims, and uncertainty.
11. LLM adds backlinks.
12. LLM updates `wiki/index.md`.
13. LLM appends `wiki/log.md`.
14. LLM reports changed files and open questions.
15. Human reviews the Git diff.

Initial prompt:

```text
Please ingest this source into the LLM Wiki.

Source:
raw/<path>

Follow AGENTS.md exactly.

Requirements:
- Do not edit raw/.
- Read wiki/index.md first.
- Read recent entries in wiki/log.md.
- Create a source summary in wiki/sources/.
- Update related concept/entity/synthesis pages.
- Prefer updating existing pages over creating duplicates.
- Add backlinks.
- Flag contradictions, stale claims, and uncertainty.
- Update wiki/index.md.
- Append to wiki/log.md.
- Report changed files and open questions.
```

Batch policy:

```text
0-20 sources:
  one source at a time with human review

20-100 sources:
  small batches only after patterns stabilize

100+ sources:
  consider stronger search tooling if index.md is no longer enough
```

### Query Workflow

Purpose: answer a question from the compiled wiki and preserve useful results.

Steps:

1. LLM reads `wiki/index.md`.
2. LLM searches the wiki if needed.
3. LLM reads relevant source, concept, entity, and synthesis pages.
4. LLM synthesizes an answer with citations to wiki/source pages.
5. LLM chooses an output form when useful:
   - Markdown report
   - comparison table
   - Marp slide deck
   - matplotlib chart
   - canvas
6. LLM files durable answers back into `wiki/questions/`, `wiki/syntheses/`, or
   `wiki/outputs/`.
7. LLM updates `wiki/index.md`.
8. LLM appends `wiki/log.md`.

Initial prompt:

```text
Please answer this question against the wiki.

Question:
<question>

Workflow:
1. Read wiki/index.md first.
2. Search the wiki if needed.
3. Read relevant source, concept, entity, and synthesis pages.
4. Answer with citations to wiki/source pages.
5. If the answer is useful, file it back into:
   - wiki/questions/ for Q&A
   - wiki/syntheses/ for durable analysis
   - wiki/outputs/ for visual or presentation output
6. Update wiki/index.md and wiki/log.md.
7. Report changed files and unresolved questions.
```

### Output Workflow

Purpose: make useful results durable and viewable.

Output locations:

```text
wiki/outputs/reports/
wiki/outputs/slides/
wiki/outputs/charts/
wiki/outputs/canvases/
```

Initial prompt:

```text
Create a durable output from the wiki.

Topic:
<topic>

Output type:
Markdown report / Marp slide deck / matplotlib chart / comparison table

Output path:
wiki/outputs/<type>/<filename>

Requirements:
- Cite relevant wiki/source pages.
- Make it useful in Obsidian.
- File it back into the wiki.
- Update index.md and log.md.
```

### Lint / Health Check Workflow

Purpose: keep the wiki healthy as it grows.

Checks:

```text
Structural:
  - broken wikilinks
  - orphan pages
  - duplicate pages
  - pages missing from index.md
  - pages with missing frontmatter
  - pages with missing backlinks

Knowledge:
  - contradictions between pages
  - stale claims superseded by newer sources
  - uncited important claims
  - weak summaries
  - concepts mentioned repeatedly but lacking pages
  - entities without pages
  - missing cross-references

Research:
  - data gaps
  - web-searchable missing facts
  - new article candidates
  - further questions to investigate
```

Initial prompt:

```text
Please run a wiki health check.

Workflow:
1. Read AGENTS.md / CLAUDE.md.
2. Read wiki/index.md and recent wiki/log.md entries.
3. Check for:
   - contradictions
   - stale claims
   - orphan pages
   - missing cross-references
   - important concepts without pages
   - missing source citations
   - data gaps
   - broken links
4. Repair safe structural issues.
5. For uncertain factual issues, create a review note instead of guessing.
6. Write findings to wiki/reviews/<date>-health-check.md.
7. Update wiki/index.md and wiki/log.md.
8. Suggest next questions and next sources.
```

## CLI Design

CLI tools are optional helpers for the LLM. They are not the knowledge base.

Initial commands:

```bash
kb search "query"
kb status
kb recent --n 5
kb lint
kb unprocessed
```

Decision status:

| Tool | Status | Basis |
|---|---|---|
| search CLI | recommended | most obvious useful LLM helper |
| status CLI | implementation judgment | useful for maintenance |
| recent CLI | implementation judgment | reads parseable `log.md` |
| lint CLI | implementation judgment | packages health checks |
| render CLI | optional | packages output generation |
| qmd | later option | useful when Markdown search needs grow |
| MCP | deferred | useful only if a chosen tool exposes it cleanly |

Do not start with:

- Obsidian CLI
- vector DB
- graph DB
- hosted RAG
- MCP-first architecture
- fine-tuning

## Obsidian Design

Obsidian is recommended as a viewer and IDE-like frontend.

Recommended settings:

```text
Attachment folder path:
  raw/assets/

Useful core feature:
  Graph view

Useful plugins:
  Web Clipper
  Marp
  Dataview
```

Rules:

- Do not depend on Obsidian for correctness.
- Do not require Obsidian CLI.
- Do not require Obsidian APIs.
- Keep the repository readable with ordinary file tools.

## Git Design

Use Git for:

- version history
- rollback
- branch-based experiments
- collaboration
- review of LLM edits

Suggested operations:

```bash
git status
git diff
git add raw/ wiki/ AGENTS.md CLAUDE.md README.md
git commit -m "Initialize LLM Wiki"
```

After ingest:

```bash
git status
git diff
git add raw/ wiki/
git commit -m "Ingest <source title>"
```

After lint:

```bash
git status
git diff
git add wiki/
git commit -m "Run wiki health check"
```

## Scale Plan

### Small Scale

Use:

- `index.md`
- `log.md`
- source summaries
- `rg`
- simple search CLI

Avoid:

- vector DB
- graph DB
- MCP-first design
- complex RAG pipelines

### Moderate Scale

Consider:

- qmd or another local Markdown search tool
- BM25/vector hybrid search
- stronger frontmatter conventions
- periodic lint
- stronger index conventions

### Larger Scale

Consider:

- dedicated search layer
- page-level metadata discipline
- source confidence tracking
- batch ingest queues
- review workflows
- branch / PR process
- possible vector search
- possible MCP
- possible evaluation set

The core remains unchanged: raw sources are compiled into a persistent wiki.

## Fine-Tuning / Synthetic Data

Fine-tuning and synthetic data are future explorations, not MVP requirements.

Recommended order:

1. Create `raw/` and `wiki/`.
2. Run ingest / query / lint manually.
3. Stabilize `index.md` and `log.md`.
4. Add simple search CLI if needed.
5. Build evaluation questions if useful.
6. Consider synthetic data.
7. Consider fine-tuning only after the wiki has grown.

## Security And Privacy

Even in a generic LLM Wiki, source sensitivity should be explicit.

Optional frontmatter:

```markdown
---
sensitivity: public | internal | private
share_with_cloud_llm: true
contains_personal_data: false
---
```

Rules:

- Label sensitive raw sources.
- Label sensitive wiki pages.
- Do not send sources to cloud LLMs unless allowed.
- Keep local-only material out of public remotes.
- Review screenshots, transcripts, and personal notes carefully.

## Explicit Non-Goals

- Domain-specific architecture in the base layer.
- Complete automation from day one.
- Obsidian CLI dependency.
- Obsidian API dependency.
- App-first design.
- Database-first design.
- Vector DB from day one.
- Graph DB from day one.
- MCP-first design.
- Fine-tuning from day one.
- Humans manually maintaining the wiki as traditional notes.
- Leaving useful answers only in chat history.

## MVP Roadmap

### Phase 0: Pure Pattern Lock

Goal: accept the domain-independent Karpathy-style design before applying it to
any specific domain.

Tasks:

- Review this roadmap.
- Confirm that no domain-specific logic belongs in the base pattern.
- Decide whether this roadmap supersedes any current implementation plan.

Acceptance criteria:

- `raw/`, `wiki/`, and schema are the only architectural layers.
- `index.md` and `log.md` are mandatory.
- Ingest, query, output, and lint are the only workflows.
- CLI tools are optional helpers.
- No domain-specific page types or answer policies are present.

Validation:

```bash
git diff --check
```

### Phase 1: Base Repository Scaffold

Goal: create the plain-file LLM Wiki structure.

Tasks:

- Create `raw/`.
- Create `wiki/`.
- Create `wiki/index.md`.
- Create `wiki/log.md`.
- Create `wiki/templates/`.
- Add generic templates.
- Add `README.md`.

Acceptance criteria:

- The repo is readable without Obsidian.
- The repo is useful in Obsidian.
- No domain-specific files are introduced.
- No app runtime is introduced.

Validation:

```bash
git diff --check
find raw wiki -maxdepth 3 -type f | sort
```

### Phase 2: Schema Files

Goal: make LLM agent behavior explicit.

Tasks:

- Write `AGENTS.md`.
- Write `CLAUDE.md`.
- Define layer boundaries.
- Define page types.
- Define workflows.
- Define index and log rules.
- Define uncertainty and citation rules.
- Define Git diff reporting.

Acceptance criteria:

- Schema files prohibit editing `raw/`.
- Schema files require reading `wiki/index.md` first for queries.
- Schema files require appending `wiki/log.md` after meaningful work.
- Schema files require filing useful answers back into the wiki.

Validation:

```bash
git diff --check
rg "raw/" AGENTS.md CLAUDE.md
rg "wiki/index.md" AGENTS.md CLAUDE.md
rg "wiki/log.md" AGENTS.md CLAUDE.md
```

### Phase 3: First Manual Ingest

Goal: prove single-source compilation.

Tasks:

- Human adds one generic source to `raw/`.
- LLM creates one source summary.
- LLM creates or updates relevant concept/entity/synthesis pages.
- LLM updates index.
- LLM appends log.
- Human reviews diff.

Acceptance criteria:

- Raw source remains unchanged.
- Source summary links to raw source.
- At least one compiled wiki page exists.
- Index and log are updated.

Validation:

```bash
git diff --check
rg "raw/" wiki/sources wiki/index.md wiki/log.md
```

### Phase 4: First Query And File-Back

Goal: prove that questions compound into durable knowledge.

Tasks:

- Ask one question answerable from the wiki.
- LLM answers with citations.
- LLM saves useful answer to `wiki/questions/` or `wiki/syntheses/`.
- LLM updates index and log.

Acceptance criteria:

- The answer cites wiki/source pages.
- The filed-back page is useful outside chat history.
- Index and log are updated.

Validation:

```bash
git diff --check
rg "type: question|type: synthesis" wiki/questions wiki/syntheses
rg "questions/|syntheses/" wiki/index.md wiki/log.md
```

### Phase 5: First Health Check

Goal: prove maintenance workflow.

Tasks:

- Run a wiki health check.
- Repair safe structural issues.
- Write uncertain factual issues to `wiki/reviews/`.
- Suggest next sources and next questions.
- Update index and log.

Acceptance criteria:

- A review page exists.
- Broken links and missing index entries are checked.
- Uncertain claims are not guessed.
- Index and log are updated.

Validation:

```bash
git diff --check
rg "type: review" wiki/reviews
rg "health" wiki/log.md
```

### Phase 6: Small CLI

Goal: add optional file-based helper tools.

Tasks:

- Add simple search.
- Add status.
- Add recent log reader.
- Add basic lint.
- Add unprocessed raw source report.

Acceptance criteria:

- Tools operate on plain files.
- Tools do not become the source of truth.
- Tools do not require Obsidian.
- Tools do not require vector DB or hosted services.

Validation:

```bash
python tools/kb_status.py
python tools/kb_search.py "query"
python tools/kb_lint.py
```

### Phase 7: Scale Review

Goal: decide whether simple files and index are still enough.

Trigger:

- around 100 sources
- hundreds of wiki pages
- repeated search failures
- repeated lint friction

Tasks:

- Review search quality.
- Review index usefulness.
- Review log usefulness.
- Decide whether to add qmd or another local Markdown search layer.
- Record the decision in `wiki/reviews/`.

Acceptance criteria:

- Search escalation is evidence-based.
- New tools preserve raw/wiki/schema boundaries.
- No domain-specific assumptions are added.

## Decision Table

| Item | Decision | Basis |
|---|---:|---|
| `raw/` | required | immutable source layer |
| `wiki/` | required | LLM-generated compiled Markdown wiki |
| `AGENTS.md` | required | Codex schema |
| `CLAUDE.md` | recommended | Claude Code schema |
| `wiki/index.md` | required | content-oriented catalog |
| `wiki/log.md` | required | chronological append-only log |
| Obsidian app | recommended | human IDE frontend |
| Obsidian CLI | rejected | not part of the simple-file core |
| Git | strongly recommended | version history and review |
| search CLI | recommended | LLM helper |
| lint CLI | optional | health check packaged as tool |
| render CLI | optional | output generation packaged as tool |
| qmd | later option | local Markdown search when needed |
| MCP | deferred | only if a chosen tool makes it useful |
| vector DB | deferred | not needed at small scale |
| fine-tuning | future exploration | not MVP |
| full automation | rejected for MVP | early human-in-loop ingest |

## Completion Definition For The Base Pattern

The base pattern is complete when:

- `raw/` exists and is treated as immutable.
- `wiki/` exists and is LLM-maintained.
- `AGENTS.md` exists.
- `CLAUDE.md` exists or is explicitly deferred.
- `wiki/index.md` exists and is maintained.
- `wiki/log.md` exists and is append-only.
- One source has been manually ingested.
- One useful query has been filed back into the wiki.
- One health check has been recorded.
- Optional CLI tools, if present, operate only on plain files.
- No domain-specific architecture has been introduced.
