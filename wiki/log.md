# Wiki Log

This is the chronological append-only activity log for the LLM-maintained wiki.

## [2026-05-26] schema | Initialize LLM Wiki scaffold
- Created:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `README.md`
  - `raw/`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/templates/`
- Notes:
  - Initialized the domain-independent raw/wiki/schema structure.
  - No raw sources have been ingested yet.

## [2026-05-26] ingest | Street Fighter 6/Glossary
- Raw source:
  - `raw/articles/2026-05-26-supercombo-street-fighter-6-glossary.md`
- Created:
  - `wiki/sources/supercombo-street-fighter-6-glossary.md`
  - `wiki/concepts/drive-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/juggle-system.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/supercombo-wiki.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Notes:
  - Captured Obsidian Web Clipper output as an exact raw source copy.
  - The raw source checksum matched the original file in Downloads before wiki
    compilation began.
  - The source page footer says it was last edited on 31 January 2026 at 11:22;
    this was noted to avoid confusing source freshness with wiki creation date.
  - Treated SuperCombo Wiki as a community wiki source with medium confidence.
- Open questions:
  - Should SuperCombo Wiki receive a standard source confidence policy?
  - Should the malformed numpad-direction table be recaptured from the source?
  - Which official source should be ingested next for terminology comparison?

## [2026-05-26] query | How juggles work internally
- Question:
  - `ジャグルって内部的にどういう仕組みで発生するんですか？`
- Read:
  - `wiki/index.md`
  - `wiki/concepts/juggle-system.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/sources/supercombo-street-fighter-6-glossary.md`
  - `raw/articles/2026-05-26-supercombo-street-fighter-6-glossary.md`
- Created:
  - `wiki/questions/how-juggles-work-internally.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Notes:
  - Filed the answer back into the wiki because it is likely to be reusable.
  - Answer is limited to the currently ingested SuperCombo Wiki glossary source.
- Open questions:
  - Ingest an official source later to compare official Combo Count terminology
    against community juggle terminology.

## [2026-05-26] query-review | Refine juggle explanation
- Updated:
  - `wiki/questions/how-juggles-work-internally.md`
  - `wiki/log.md`
- Notes:
  - Weakened wording from direct hit/whiff language to whether the hit is
    allowed by the juggle rules.
  - Clarified that spacing, timing, hitboxes, and hurtboxes still matter.
  - Clarified that official terminology sources have not yet been independently
    ingested or cited by this wiki page.
