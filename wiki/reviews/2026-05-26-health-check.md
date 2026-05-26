---
type: review
review_type: lint
created: 2026-05-26
status: open
---

# Wiki Health Check - 2026-05-26

## Summary

Initial health check after the first source ingest and the first filed-back
query.

The wiki structure is healthy at this scale. No broken wikilinks, missing index
entries, or missing frontmatter were found in the non-template wiki pages.

Several knowledge gaps remain open because they require new sources or human
direction rather than safe automatic repair.

## Structural issues

### Broken links

None found.

### Orphan pages

None found relative to `wiki/index.md`. All non-template wiki pages are listed
in the index.

### Missing index entries

None found.

### Missing frontmatter

None found in non-template content pages.

### Duplicate pages

None found.

## Knowledge issues

### Contradictions

No direct contradictions were found between the currently ingested pages.

### Stale claims

No stale claims were confirmed. The SuperCombo source page's own footer says the
source was last edited on 31 January 2026 at 11:22, and the wiki records that
date in `wiki/index.md` as the source date.

### Uncited claims

No high-impact uncited claims were found in the current wiki pages. Existing
claims point back to `[[sources/supercombo-street-fighter-6-glossary]]` or to
the raw source path recorded in that source page.

## Data gaps

- Official Capcom terminology sources have not yet been ingested. This matters
  for the mapping between community juggle terms and official terms such as
  Combo Count Initial Value, Combo Count Additional Value, and Combo Count Upper
  Limit.
- The raw SuperCombo Web Clipper capture appears to contain a malformed
  numpad-direction table. Because `raw/` is immutable after capture, this should
  be handled by adding a new raw recapture source if higher-fidelity notation
  evidence is needed.
- There is no explicit source confidence policy for community wiki sources yet.
  Current pages use `medium` confidence for the SuperCombo source.

## Missing concepts

- `Forced Knockdown` is currently explained inside the juggle answer and source
  page context, but it does not yet have a dedicated concept page. This is not a
  structural problem yet; create one only if future sources make it reusable.
- A community-to-official terminology mapping may deserve a synthesis page after
  at least one official Capcom source is ingested.

## Suggested next sources

- An official Capcom Battle Change List page that uses Combo Count terminology.
- A higher-fidelity recapture of the SuperCombo notation table, only if the
  current malformed table becomes a practical blocker.

## Suggested next questions

- Which official Capcom source should anchor the first community-to-official
  terminology comparison?
- Should this wiki maintain separate confidence guidance for official,
  community wiki, and user-curated sources?

## Changes made

- Created this review page.
- Added this review page to `wiki/index.md`.
- Appended a health-check entry to `wiki/log.md`.

## Requires human review

- Choose whether the next source should be an official Capcom Battle Change
  List page.
- Decide whether the malformed notation table matters enough to justify a new
  raw recapture source.
- Decide whether to formalize source confidence guidance now or defer until more
  source types are ingested.
