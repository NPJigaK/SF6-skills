---
type: review
review_type: health_check
created: 2026-05-27
status: open
sources:
  - "[[sources/supercombo-street-fighter-6-glossary]]"
  - "[[sources/capcom-official-jp-frame-data]]"
  - "[[sources/capcom-official-ryu-frame-data]]"
  - "[[sources/capcom-official-chun-li-frame-data]]"
  - "[[sources/capcom-official-zangief-frame-data]]"
related:
  - "[[concepts/frame-data]]"
  - "[[entities/jp]]"
  - "[[entities/ryu]]"
  - "[[entities/chun-li]]"
  - "[[entities/zangief]]"
tags:
  - review
  - health-check
---

# Wiki Health Check - 2026-05-27

## Summary

This health check reviewed the wiki after the accepted JP, Ryu, Chun-Li, and
Zangief official frame-data captures and the four Classic/Modern comparison
question pages.

No blocking structural issue was found. Safe cleanup was applied to stale open
questions that still asked whether already-filed Classic/Modern comparison
pages should be created.

## Human review decision

Accepted on 2026-05-27.

- Keep `status: open` because follow-up design work remains.
- Keep JP, Ryu, Chun-Li, and Zangief validation results in this health check.
- Accept the cleanup of stale source-page questions about whether already-filed
  comparison pages should be created.
- Accept the cleanup of character entity wording after human review.
- Treat command notation as a display-only transform for now. Raw input tokens
  remain the source-preserving data.
- Use exact official move-name matching as the default comparison rule.
- For pairs such as `しゃがみ強K（ビッグスタンプ）` and `ビッグスタンプ`, annotate
  them as likely corresponding name variants instead of silently normalizing
  them as the same move.

## Structural issues

### Broken links

None found in non-template wiki pages.

Template placeholder links under `wiki/templates/` were intentionally excluded
from the broken-link check because they contain example links such as
`concepts/...`.

### Missing index entries

No existing non-template wiki page was missing from `wiki/index.md` before this
review page was added. This page is now registered in the Reviews section.

### Missing frontmatter

No missing frontmatter found in content pages. `wiki/index.md` and `wiki/log.md`
are treated as special navigation/log files and intentionally do not use page
frontmatter.

### Question-page workflow leakage

No `wiki/questions/` page currently includes workflow-only sections such as
`Filed-back updates`, changed files, task summaries, or implementation notes.

## Data validation

The official frame-data outputs were revalidated against raw snapshots.

| Character | Classic rows | Modern rows | Result |
|---|---:|---:|---|
| JP | 69 | 65 | passed |
| Ryu | 75 | 69 | passed |
| Chun-Li | 78 | 72 | passed |
| Zangief | 72 | 66 | passed |

The validation checks compare saved derived rows and field meanings against
data regenerated from raw HTML / raw DOM snapshots. Screenshots are used as
visual coverage evidence for page state, table width, and overlays, not as the
primary cell-value source.

## Knowledge issues

### Stale open questions

Fixed:

- Removed source-page open questions asking whether the Ryu, Chun-Li, and
  Zangief Classic/Modern comparison pages should be filed, because those pages
  now exist.
- Updated accepted character entity open questions so they no longer imply
  that human review is still pending.
- Updated JP source open questions so they no longer ask whether only one
  additional official character should be tested.

### Contradictions

No direct contradiction was found between accepted source pages, character
entities, index entries, and question pages.

### Stale claims

Chun-Li source wording still implied the capture should not be generalized until
human review accepts it; this was updated because the capture has already been
accepted.

## Suggested next questions

- Should the wiki define a normalized command-input notation for reader-facing
  answers while preserving raw input tokens in source/output data?
- Should Classic/Modern comparison pages keep exact official move-name matching
  as the default, or add a separate normalized identity mapping for likely
  equivalent move-name variants?
- Which official Capcom source should be ingested next to explain update
  history and official terminology?

## Changes made

- Cleaned stale open questions in official frame-data source pages.
- Cleaned stale open questions in accepted character entity pages.
- Added this health-check review page.
- Updated `wiki/index.md`.
- Appended to `wiki/log.md`.

## Open follow-up items

- If display-only command notation becomes repeated enough, consider defining
  it as a formal wiki concept later.
- If move-name variants become common across more characters, consider creating
  an explicit move-identity mapping page. Until then, keep exact official
  move-name matching as the default and annotate likely corresponding variants.
