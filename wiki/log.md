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

## [2026-05-26] lint | Initial wiki health check
- Checked:
  - broken wikilinks
  - pages missing from `wiki/index.md`
  - missing frontmatter
  - duplicate pages
  - contradictions
  - stale claims
  - uncited claims
  - missing concepts
  - data gaps
- Created:
  - `wiki/reviews/2026-05-26-health-check.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Findings:
  - No broken wikilinks, missing index entries, or missing frontmatter were
    found.
  - Open knowledge gaps remain around official Capcom terminology sources,
    malformed notation-table capture quality, and community-source confidence
    policy.

## [2026-05-26] ingest | Capcom official JP frame data
- Raw source:
  - `raw/official/frame-data/2026-05-26/jp/manifest.json`
  - `raw/official/frame-data/2026-05-26/jp/classic/`
  - `raw/official/frame-data/2026-05-26/jp/modern/`
- Derived outputs:
  - `wiki/outputs/data/frame-data/jp/classic.csv`
  - `wiki/outputs/data/frame-data/jp/modern.csv`
  - `wiki/outputs/data/frame-data/jp/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/jp/modern.field-meanings.json`
- Tooling:
  - Added `pyproject.toml` and `uv.lock` for Scrapling-based capture tooling.
  - Added `tools/capture_capcom_frame_data.py`.
  - Added `tools/extract_capcom_frame_data.py`.
  - Fixed capture URL handling so `--source-url` is derived from
    `--character-slug` unless explicitly provided, and explicit URLs must match
    the slug.
- Created:
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/jp.md`
  - `wiki/reviews/2026-05-26-official-jp-frame-data-capture-review.md`
- Updated:
  - `README.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Review:
  - Human review accepted the raw snapshot and derived outputs for wiki ingest.
  - Classic data row count is 69; Modern data row count is 65.
  - `*.field-meanings.json` stores table-header help text separately from row
    CSVs.
- Notes:
  - Raw official captures remain dated snapshots under `raw/official/`.
  - Stable derived CSV paths under `wiki/outputs/data/` are intended to make
    future update diffs easier to review.
- Open questions:
  - Should the next official capture cover all characters, or one additional
    character first to validate the pipeline?
  - Should a normalized command notation be generated later from raw input
    tokens?
  - Which official update-history source should be ingested to explain future
    frame-data changes?

## [2026-05-26] query | JP Modern vs Classic frame-data counts and inputs
- Question:
  - JPのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- Read:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/jp.md`
  - `wiki/outputs/data/frame-data/jp/classic.csv`
  - `wiki/outputs/data/frame-data/jp/modern.csv`
- Created:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Answer summary:
  - Classic has 69 official derived frame-data rows and Modern has 65.
  - Modern has no unique move-name rows compared with Classic; Classic-only
    rows are standing LK, crouching MP, crouching HK, and Heavy Stribog.
  - Of 65 shared move names, 62 have different raw input displays and 3
    movement/system rows have identical raw input displays.
- Open questions:
  - Should future comparisons normalize `input_raw_display` into conventional
    command notation, or continue comparing raw DOM-token displays only?

## [2026-05-26] query-review | Improve JP Modern vs Classic answer
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Notes:
  - Reworked the answer to start with a user-facing conclusion instead of a CSV
    implementation detail.
  - Added the practical interpretation that shared move-name rows have the same
    captured frame/gauge/cancel fields except for 16 damage differences.
  - Added a damage-difference table and clarified that `input_raw_display`
    remains raw DOM-token output, not normalized command notation.

## [2026-05-26] query-review | Japanese wording for JP Modern vs Classic answer
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Converted user-facing section headings and explanatory prose to Japanese.
  - Kept technical field names such as `move_name`, `input_raw_display`, and
    token names unchanged where they identify stored data fields.

## [2026-05-26] query-review | Display command notation for JP comparison
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Replaced raw DOM tokens such as `key-d` and `icon_punch_l` in user-facing
    examples with readable command notation such as ↓, ↘, →, 弱P, and 強K.
  - Left raw token field names in the limitations section to clarify the stored
    evidence format.

## [2026-05-26] query-review | Prefer official column wording
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Replaced internal comparison field names in user-facing prose with official
    table wording such as 技名 and 入力表示.
  - Kept storage field names only where the page explicitly discusses stored
    evidence fields.

## [2026-05-26] query-review | Remove workflow notes from JP answer
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Removed the `File-back` workflow section from the durable answer page.
  - Shortened the caveats so user-facing prose does not expose unnecessary
    storage-field details.

## [2026-05-26] query-review | Simplify evidence wording
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Replaced internal derived-output file paths in the evidence section with
    user-facing source wording.
  - Kept the wiki source link as the traceability anchor.

## [2026-05-27] schema | Keep question pages reader-facing
- Updated:
  - `AGENTS.md`
  - `CLAUDE.md`
  - `ROADMAP.md`
  - `wiki/templates/question.md`
  - `wiki/questions/how-juggles-work-internally.md`
  - `wiki/log.md`
- Notes:
  - Removed `Filed-back updates` from the question template and the existing
    juggle question page.
  - Clarified that `wiki/questions/` pages are durable reader-facing answers.
  - Operational file-back details, changed files, and task summaries now belong
    in `wiki/log.md` or the final task report, not in question pages.

## [2026-05-27] query-review | Make JP comparison answer less implementation-facing
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Notes:
  - Removed implementation-facing wording such as CSV, derived data, and row
    counting from the durable answer prose.
  - Reworded the answer around official frame-data items, move names, input
    displays, and the practical Classic/Modern differences a reader asked for.

## [2026-05-27] query-review | Remove bare source footer from JP comparison
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Removed the bare `参照元` wikilink from the answer body because the source
    is already recorded in frontmatter.
  - Kept the evidence section focused on what was checked rather than exposing
    wiki navigation details to the reader.

## [2026-05-27] query-review | Sort JP damage differences by move family
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Reordered the damage-difference table so variants of the same move family,
    such as Stribog and Triglav, stay adjacent.

## [2026-05-27] query-review | Format JP command examples
- Updated:
  - `wiki/questions/jp-modern-vs-classic-frame-data-moves-and-inputs.md`
  - `wiki/log.md`
- Notes:
  - Wrapped command notation examples in inline code for readability.

## [2026-05-27] query-removal | Remove low-quality juggle answer
- Removed:
  - `wiki/questions/how-juggles-work-internally.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Notes:
  - Removed the filed-back juggle question because the current answer quality
    and reader-facing shape no longer match the standard established by later
    question-page tuning.
  - Kept the underlying SuperCombo source and related concept pages intact; this
    is a removal of a weak answer, not a rejection of the source.
- Follow-up:
  - Re-answer the juggle mechanism question later after the relevant official
    Capcom terminology or a stronger source has been ingested.

## [2026-05-27] review-removal | Remove stale initial health check
- Removed:
  - `wiki/reviews/2026-05-26-health-check.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Notes:
  - Removed the initial health check because it described the early wiki state
    around a now-deleted filed-back juggle answer.
  - Kept `wiki/reviews/2026-05-26-official-jp-frame-data-capture-review.md`
    because it records the human acceptance of the official JP frame-data
    capture and remains useful evidence.

## [2026-05-27] ingest | Capcom official Ryu frame data
- Raw source:
  - `raw/official/frame-data/2026-05-27/ryu/manifest.json`
  - `raw/official/frame-data/2026-05-27/ryu/classic/`
  - `raw/official/frame-data/2026-05-27/ryu/modern/`
- Derived outputs:
  - `wiki/outputs/data/frame-data/ryu/classic.csv`
  - `wiki/outputs/data/frame-data/ryu/modern.csv`
  - `wiki/outputs/data/frame-data/ryu/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/ryu/modern.field-meanings.json`
- Created:
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/entities/ryu.md`
  - `wiki/reviews/2026-05-27-official-ryu-frame-data-capture-review.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
- Validation:
  - Capture command succeeded for `https://www.streetfighter.com/6/ja-jp/character/ryu/frame`.
  - Extract command reproduced 75 Classic rows and 69 Modern rows from raw DOM.
  - Metadata reports separate Classic and Modern tab captures with no visible
    Cookiebot or navigation overlays after cleanup.
  - LLM visual check confirmed the screenshots include the table width.
- Status:
  - Pending human review before marking the Ryu capture accepted.
- Open questions:
  - Should a Ryu Classic/Modern comparison question be filed after human review?
  - Which character should stress-test unusual frame-data table formats next?

## [2026-05-27] schema | Simplify official frame-data CSV rows
- Updated:
  - `tools/capture_capcom_frame_data.py`
  - `tools/extract_capcom_frame_data.py`
  - `README.md`
  - `wiki/outputs/data/frame-data/jp/classic.csv`
  - `wiki/outputs/data/frame-data/jp/modern.csv`
  - `wiki/outputs/data/frame-data/ryu/classic.csv`
  - `wiki/outputs/data/frame-data/ryu/modern.csv`
  - `wiki/log.md`
- Notes:
  - Removed repeated source-level metadata from per-move CSV rows.
  - `publisher`, `game`, `locale`, `source_url`, character, control scheme,
    raw capture path, and screenshot path remain in raw manifests, raw metadata,
    output paths, and wiki source pages.
  - Kept CSVs focused on row-level frame-data fields to make diffs and manual
    inspection easier.

## [2026-05-27] human-review | Accept official Ryu frame-data capture
- Updated:
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/entities/ryu.md`
  - `wiki/reviews/2026-05-27-official-ryu-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
- Decision:
  - Accepted.
- Reviewer checks:
  - Raw placement matches the JP convention.
  - Classic and Modern screenshots show the intended Ryu official tables without
    visible horizontal cutoff or obstructing overlays.
  - DOM row counts, manifest row counts, and CSV row counts match: Classic 75,
    Modern 69.
  - Field meanings are present: Classic 7 records, Modern 8 records, including
    the Modern SP-button 80% damage note.
  - Ryu source, entity, review, and outputs are reachable from the index.
- Notes:
  - Source and review statuses were moved from `pending_human_review` to active
    or accepted as appropriate.

## [2026-05-27] query | Ryu Modern vs Classic frame-data counts and inputs
- Question:
  - Ryuのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- Read:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/ryu.md`
  - `wiki/outputs/data/frame-data/ryu/classic.csv`
  - `wiki/outputs/data/frame-data/ryu/modern.csv`
- Created:
  - `wiki/questions/ryu-modern-vs-classic-frame-data-moves-and-inputs.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Answer summary:
  - Classic has 75 official frame-data items and Modern has 69.
  - Exact official move-name matching gives 68 shared names, 7 Classic-only
    names, and 1 Modern-only name.
  - The `しゃがみ強K（回転足払い）` / `回転足払い` naming difference is called
    out explicitly instead of silently normalizing it.
  - Of 68 shared move names, 65 have different input displays and 3 movement
    rows have identical input displays.
  - Damage differs on 22 shared move-name items; other captured frame/gauge/cancel
    fields match for shared move-name items.
- Open questions:
  - Should future comparison pages normalize move identity across name variants,
    or keep exact official move-name matching as the default?

## [2026-05-27] ingest | Capcom official Chun-Li frame data
- Raw source:
  - `raw/official/frame-data/2026-05-27/chunli/manifest.json`
  - `raw/official/frame-data/2026-05-27/chunli/classic/`
  - `raw/official/frame-data/2026-05-27/chunli/modern/`
- Derived outputs:
  - `wiki/outputs/data/frame-data/chunli/classic.csv`
  - `wiki/outputs/data/frame-data/chunli/modern.csv`
  - `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json`
- Created:
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/entities/chun-li.md`
  - `wiki/reviews/2026-05-27-official-chun-li-frame-data-capture-review.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
- Validation:
  - Capture command succeeded for `https://www.streetfighter.com/6/ja-jp/character/chunli/frame`.
  - Extract command reproduced 78 Classic rows and 72 Modern rows from raw DOM.
  - Metadata reports separate Classic and Modern tab captures with no visible
    Cookiebot or navigation overlays after cleanup.
  - LLM visual check confirmed the screenshots include the table width.
- Status:
  - Pending human review before marking the Chun-Li capture accepted.
- Open questions:
  - Should a Chun-Li Classic/Modern comparison question be filed after human
    review?
  - Which character should be used next to stress-test unusual frame-data table
    formats?

## [2026-05-27] human-review | Accept official Chun-Li frame-data capture
- Updated:
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/entities/chun-li.md`
  - `wiki/reviews/2026-05-27-official-chun-li-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
- Decision:
  - Accepted.
- Reviewer checks:
  - Raw placement matches the JP and Ryu conventions.
  - Classic and Modern screenshots show the intended Chun-Li official tables
    without visible horizontal cutoff or obstructing overlays.
  - DOM row counts, manifest row counts, and CSV row counts match: Classic 78,
    Modern 72.
  - Field meanings are present: Classic 7 records, Modern 8 records, including
    the Modern SP-button 80% damage note.
  - Chun-Li source, entity, review, and outputs are reachable from the index.
  - Stance-like, branch, charge, and air-action inputs are retained in
    `input_token_json`.
- Cleanup:
  - Restored `[[entities/jp]]` to `wiki/concepts/frame-data.md` frontmatter
    `related` to match the page connections and index.
- Notes:
  - Source and review statuses were moved from `pending_human_review` to active
    or accepted as appropriate.
