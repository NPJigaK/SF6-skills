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

## [2026-05-27] query | Chun-Li Classic vs Modern frame-data comparison
- Question:
  - Chun-Liのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- Created:
  - `wiki/questions/chun-li-modern-vs-classic-frame-data-moves-and-inputs.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Answer summary:
  - Classic has 78 official frame-data items and Modern has 72.
  - Exact official move-name matching gives 71 shared names, 7 Classic-only
    names, and 1 Modern-only name.
  - The `しゃがみ強K（元伝暗殺蹴）` / `元伝暗殺蹴` naming difference is called
    out explicitly instead of silently normalizing it.
  - Of 71 shared move names, 68 have different input displays and 3 movement
    rows have identical input displays.
  - Damage differs on 15 shared move-name items; other captured frame/gauge/cancel
    fields match for shared move-name items.
- Open questions:
  - Should future comparison pages normalize move identity across name variants,
    or keep exact official move-name matching as the default?

## [2026-05-27] ingest | Capcom official Zangief frame data
- Raw source:
  - `raw/official/frame-data/2026-05-27/zangief/manifest.json`
  - `raw/official/frame-data/2026-05-27/zangief/classic/`
  - `raw/official/frame-data/2026-05-27/zangief/modern/`
- Derived outputs:
  - `wiki/outputs/data/frame-data/zangief/classic.csv`
  - `wiki/outputs/data/frame-data/zangief/modern.csv`
  - `wiki/outputs/data/frame-data/zangief/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/zangief/modern.field-meanings.json`
- Created:
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/entities/zangief.md`
  - `wiki/reviews/2026-05-27-official-zangief-frame-data-capture-review.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/capcom.md`
  - `wiki/entities/street-fighter-6.md`
- Validation:
  - Capture command succeeded for `https://www.streetfighter.com/6/ja-jp/character/zangief/frame`.
  - Extract command reproduced 72 Classic rows and 66 Modern rows from raw DOM.
  - Full validation confirmed `page.html` table hashes, raw DOM, derived CSV,
    field-meanings JSON, overlay metadata, and screenshot coverage for all rows.
  - Metadata reports zero visible Cookiebot and navigation overlays after cleanup.
  - LLM visual check confirmed the screenshots include the table width and page
    footer for both Classic and Modern captures.
  - Zangief-specific command-grab and one/two-circle input tokens are retained
    in `input_token_json`.
- Status:
  - Pending human review before marking the Zangief capture accepted.
- Open questions:
  - Should a Zangief Classic/Modern comparison question be filed after human
    review?
  - Which character should be used next to stress-test unusual frame-data table
    formats?

## [2026-05-27] human-review | Accept official Zangief frame-data capture
- Updated:
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/entities/zangief.md`
  - `wiki/reviews/2026-05-27-official-zangief-frame-data-capture-review.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
- Decision:
  - Accepted.
- Reviewer checks:
  - Full validation passed for Classic 72 rows and Modern 66 rows.
  - `page.html` table hashes match `table.dom.json`.
  - Saved CSV rows match raw-DOM-regenerated rows.
  - Field meanings are regenerated from DOM and match saved JSON.
  - Screenshots show the official Zangief page, selected tabs, full table width,
    table bottom, character select, and footer.
  - Zangief-specific inputs such as `key-circle`, `key-circle key-circle`,
    command grabs, Modern SP/AUTO shortcuts, and parenthesized normal-command
    alternatives are retained.
- Cleanup:
  - Aligned the review index table's review type labels with review page
    frontmatter by using `capture_validation`.

## [2026-05-27] query | Zangief Classic vs Modern frame-data comparison
- Question:
  - Zangiefのモダンとクラシックで、フレームデータ上の技数や入力はどう違いますか？
- Created:
  - `wiki/questions/zangief-modern-vs-classic-frame-data-moves-and-inputs.md`
- Updated:
  - `wiki/index.md`
  - `wiki/log.md`
- Answer summary:
  - Classic has 72 official frame-data items and Modern has 66.
  - Exact official move-name matching gives 65 shared names, 7 Classic-only
    names, and 1 Modern-only name.
  - The `しゃがみ強K（ビッグスタンプ）` / `ビッグスタンプ` naming difference is
    called out explicitly instead of silently normalizing it.
  - Of 65 shared move names, 62 have different input displays and 3 movement
    rows have identical input displays.
  - Damage differs on 18 shared move-name items; other captured frame/gauge/cancel
    fields match for shared move-name items.
  - One/two-circle inputs are rendered in the answer as readable command
    notation while the raw source keeps the original input tokens.
- Open questions:
  - Should future comparison pages normalize move identity across name variants,
    or keep exact official move-name matching as the default?

## [2026-05-27] lint | post-Zangief wiki health check
- Read:
  - `AGENTS.md`
  - `wiki/index.md`
  - recent `wiki/log.md` entries
  - official frame-data source pages
  - accepted character entity pages
  - filed Classic/Modern comparison question pages
- Created:
  - `wiki/reviews/2026-05-27-health-check.md`
- Updated:
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/entities/jp.md`
  - `wiki/entities/ryu.md`
  - `wiki/entities/chun-li.md`
  - `wiki/entities/zangief.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Checks:
  - Non-template wiki pages have no broken wikilinks.
  - Content pages have frontmatter.
  - Existing non-template wiki pages were registered in `wiki/index.md`.
  - Question pages do not contain operational file-back sections or changed-file
    summaries.
  - Accepted JP, Ryu, Chun-Li, and Zangief frame-data outputs passed validation
    against raw snapshots.
- Cleanup:
  - Removed stale source open questions about filing comparison pages that now
    exist.
  - Removed stale wording implying accepted captures were still waiting for
    human review.
- Open questions:
  - Should command-input normalization become a formal wiki concept?
  - Should move-name identity normalization be introduced before more
    Classic/Modern comparison pages are created?

## [2026-05-27] human-review | Accept post-Zangief wiki health check
- Reviewed:
  - `wiki/reviews/2026-05-27-health-check.md`
  - source-page stale open question cleanup
  - accepted character entity cleanup
- Updated:
  - `wiki/reviews/2026-05-27-health-check.md`
  - `wiki/log.md`
- Decision:
  - Accepted the health check while keeping `status: open`.
  - Accepted keeping JP, Ryu, Chun-Li, and Zangief validation results in the
    health check.
  - Accepted deletion of stale source-page questions about whether already-filed
    comparison pages should be created.
  - Accepted cleanup of accepted character entity wording.
- Design decisions:
  - Command notation remains a display-only transform for now.
  - Classic/Modern move comparison defaults to exact official move-name matching.
  - Likely corresponding name variants, such as `しゃがみ強K（ビッグスタンプ）` and
    `ビッグスタンプ`, should be annotated rather than silently normalized.
- Notes:
  - Older open questions in `wiki/log.md` remain unchanged because the log is
    append-only.

## [2026-05-27] concept-update | Frame-data comparison policy
- Read:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/reviews/2026-05-27-health-check.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/fighting-game-notation.md`
- Updated:
  - `wiki/concepts/frame-data.md`
  - `wiki/concepts/fighting-game-notation.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Decisions recorded:
  - Classic/Modern frame-data comparisons default to exact official move-name
    matching.
  - Likely corresponding move-name variants are annotated rather than silently
    normalized.
  - Command notation in reader-facing answers remains a display-only transform
    for now; raw input tokens remain source-preserving data.
- Open questions:
  - When, if ever, should display-only command notation become a formal wiki
    notation schema?


## [2026-05-30] ingest | Official frame-data coverage for remaining roster
- Read:
  - `AGENTS.md`
  - `wiki/index.md`
  - recent entries in `wiki/log.md`
  - existing official frame-data source, entity, review, and concept pages
  - official Capcom frame-data pages via `tools/capture_capcom_frame_data.py`
- Created raw snapshots:
  - `raw/official/frame-data/2026-05-30/luke/`
  - `raw/official/frame-data/2026-05-30/jamie/`
  - `raw/official/frame-data/2026-05-30/guile/`
  - `raw/official/frame-data/2026-05-30/kimberly/`
  - `raw/official/frame-data/2026-05-30/juri/`
  - `raw/official/frame-data/2026-05-30/ken/`
  - `raw/official/frame-data/2026-05-30/blanka/`
  - `raw/official/frame-data/2026-05-30/dhalsim/`
  - `raw/official/frame-data/2026-05-30/ehonda/`
  - `raw/official/frame-data/2026-05-30/deejay/`
  - `raw/official/frame-data/2026-05-30/manon/`
  - `raw/official/frame-data/2026-05-30/marisa/`
  - `raw/official/frame-data/2026-05-30/lily/`
  - `raw/official/frame-data/2026-05-30/cammy/`
  - `raw/official/frame-data/2026-05-30/rashid/`
  - `raw/official/frame-data/2026-05-30/aki/`
  - `raw/official/frame-data/2026-05-30/ed/`
  - `raw/official/frame-data/2026-05-30/gouki_akuma/`
  - `raw/official/frame-data/2026-05-30/vega_mbison/`
  - `raw/official/frame-data/2026-05-30/terry/`
  - `raw/official/frame-data/2026-05-30/mai/`
  - `raw/official/frame-data/2026-05-30/elena/`
  - `raw/official/frame-data/2026-05-30/sagat/`
  - `raw/official/frame-data/2026-05-30/cviper/`
  - `raw/official/frame-data/2026-05-30/alex/`
  - `raw/official/frame-data/2026-05-30/ingrid/`
- Created wiki pages:
  - `wiki/sources/capcom-official-luke-frame-data.md`
  - `wiki/sources/capcom-official-jamie-frame-data.md`
  - `wiki/sources/capcom-official-guile-frame-data.md`
  - `wiki/sources/capcom-official-kimberly-frame-data.md`
  - `wiki/sources/capcom-official-juri-frame-data.md`
  - `wiki/sources/capcom-official-ken-frame-data.md`
  - `wiki/sources/capcom-official-blanka-frame-data.md`
  - `wiki/sources/capcom-official-dhalsim-frame-data.md`
  - `wiki/sources/capcom-official-e-honda-frame-data.md`
  - `wiki/sources/capcom-official-dee-jay-frame-data.md`
  - `wiki/sources/capcom-official-manon-frame-data.md`
  - `wiki/sources/capcom-official-marisa-frame-data.md`
  - `wiki/sources/capcom-official-lily-frame-data.md`
  - `wiki/sources/capcom-official-cammy-frame-data.md`
  - `wiki/sources/capcom-official-rashid-frame-data.md`
  - `wiki/sources/capcom-official-aki-frame-data.md`
  - `wiki/sources/capcom-official-ed-frame-data.md`
  - `wiki/sources/capcom-official-gouki-akuma-frame-data.md`
  - `wiki/sources/capcom-official-vega-m-bison-frame-data.md`
  - `wiki/sources/capcom-official-terry-frame-data.md`
  - `wiki/sources/capcom-official-mai-frame-data.md`
  - `wiki/sources/capcom-official-elena-frame-data.md`
  - `wiki/sources/capcom-official-sagat-frame-data.md`
  - `wiki/sources/capcom-official-c-viper-frame-data.md`
  - `wiki/sources/capcom-official-alex-frame-data.md`
  - `wiki/sources/capcom-official-ingrid-frame-data.md`
  - `wiki/entities/luke.md`
  - `wiki/entities/jamie.md`
  - `wiki/entities/guile.md`
  - `wiki/entities/kimberly.md`
  - `wiki/entities/juri.md`
  - `wiki/entities/ken.md`
  - `wiki/entities/blanka.md`
  - `wiki/entities/dhalsim.md`
  - `wiki/entities/e-honda.md`
  - `wiki/entities/dee-jay.md`
  - `wiki/entities/manon.md`
  - `wiki/entities/marisa.md`
  - `wiki/entities/lily.md`
  - `wiki/entities/cammy.md`
  - `wiki/entities/rashid.md`
  - `wiki/entities/aki.md`
  - `wiki/entities/ed.md`
  - `wiki/entities/gouki-akuma.md`
  - `wiki/entities/vega-m-bison.md`
  - `wiki/entities/terry.md`
  - `wiki/entities/mai.md`
  - `wiki/entities/elena.md`
  - `wiki/entities/sagat.md`
  - `wiki/entities/c-viper.md`
  - `wiki/entities/alex.md`
  - `wiki/entities/ingrid.md`
  - `wiki/reviews/2026-05-30-official-frame-data-roster-capture-review.md`
  - `wiki/outputs/reports/2026-05-30-official-frame-data-coverage.md`
- Updated:
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/capcom.md`
  - `wiki/sources/capcom-official-jp-frame-data.md`
  - `wiki/sources/capcom-official-ryu-frame-data.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/sources/capcom-official-zangief-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- Derived outputs:
  - Added Classic and Modern CSV plus field-meaning JSON outputs under
    `wiki/outputs/data/frame-data/<data-slug>/` for 26 new character data slugs.
- Validation:
  - `tools/validate_capcom_frame_data.py` passed for all 26 new 2026-05-30
    captures.
  - Existing accepted JP, Ryu, Chun-Li, and Zangief captures were also
    revalidated against their raw snapshots.
  - Total coverage is now 30 character data slugs with Classic and Modern
    derived outputs.
- Notes:
  - The official frame-data table slugs are `gouki_akuma` and `vega_mbison`,
    not the shorter character navigation slugs `gouki` and `vega`.
  - An empty generated `raw/official/frame-data/2026-05-30/gouki/manifest.json`
    from the failed short-slug attempt was removed before filing the ingest.
- Open questions:
  - Should the 26 new captures be human-reviewed individually or accepted as a
    batch after representative screenshot review?
  - Should JP, Ryu, Chun-Li, and Zangief be recaptured under a 2026-05-30 date
    label for a single-date full-roster snapshot?

## [2026-05-30] 質問 | 春麗の立ち中Pのフレームデータ
- 質問:
  - 春麗の立ち中Pは、発生・ヒット時・ガード時・キャンセル可否・ダメージを教えて。
- 参照:
  - `wiki/index.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/outputs/data/frame-data/chunli/classic.csv`
  - `wiki/outputs/data/frame-data/chunli/modern.csv`
- 作成:
  - `wiki/questions/chun-li-standing-medium-p-frame-data.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - 春麗の`立ち中P（頸穿刀）`はクラシックとモダンで同じ値:
    発生5F、ヒット時+6F、ガード時+1F、キャンセル`C`、ダメージ600。
- 未解決事項:
  - この質問ではなし。

## [2026-05-30] 質問レビュー | 春麗の立ち中P回答の修正
- レビュー指摘:
  - 発生、硬直差、キャンセル、ダメージだけでなく、持続と硬直も含める。
  - `C`は必殺技、ドライブインパクト、ドライブラッシュ、SAでキャンセル可能という意味だと説明する。
  - ガード時`+1`は、ガードされた時に春麗側が有利という意味だと説明する。
- 更新:
  - `wiki/questions/chun-li-standing-medium-p-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 修正後の回答要約:
  - `立ち中P（頸穿刀）`: 発生5F、持続5-8F、硬直10F、ヒット時+6F、
    ガード時+1F、キャンセル`C`、ダメージ600。
- 未解決事項:
  - なし。

## [2026-05-30] 質問 | 春麗の立ち中Pからしゃがみ中Pへのリンク可否
- 質問:
  - 春麗の立ち中Pが通常ヒットしたあと、発生6Fのしゃがみ中Pは理論上つながる？理由もフレームで説明して。
- 参照:
  - `wiki/index.md`
  - `wiki/sources/capcom-official-chun-li-frame-data.md`
  - `wiki/outputs/data/frame-data/chunli/classic.csv`
  - `wiki/outputs/data/frame-data/chunli/modern.csv`
  - `wiki/outputs/data/frame-data/chunli/classic.field-meanings.json`
  - `wiki/outputs/data/frame-data/chunli/modern.field-meanings.json`
  - `wiki/questions/chun-li-standing-medium-p-frame-data.md`
- 作成:
  - `wiki/questions/chun-li-standing-medium-p-into-crouching-medium-p-link.md`
- 更新:
  - `wiki/index.md`
  - `wiki/log.md`
- 回答要約:
  - 理論上はつながる。`立ち中P（頸穿刀）`は通常ヒット時`+6F`、
    `しゃがみ中P（丹頂拳）`は発生`6F`なので、`+6F - 6F = 0F`。
    最速なら連続ヒットするが、数値上の余裕はない。
- 未解決事項:
  - 実戦での距離、押し戻し、食らい判定は別途確認が必要。

## [2026-05-31] 取り込み | SuperCombo JP フレームデータの生データ取得
- Raw source:
  - `raw/supercombo/frame-data/2026-05-31/jp/manifest.json`
  - `raw/supercombo/frame-data/2026-05-31/jp/data.raw.wikitext`
  - `raw/supercombo/frame-data/2026-05-31/jp/frame-data.raw.wikitext`
  - `raw/supercombo/frame-data/2026-05-31/jp/cargo/`
  - `raw/supercombo/frame-data/2026-05-31/jp/rendered/`
  - `raw/supercombo/frame-data/2026-05-31/jp/screenshots/`
  - `raw/supercombo/frame-data/2026-05-31/jp/images/files/`
- 追加:
  - `tools/capture_supercombo_frame_data.py`
  - `tools/validate_supercombo_frame_data.py`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/reviews/2026-05-31-supercombo-jp-frame-data-capture-review.md`
- 更新:
  - `wiki/concepts/frame-data.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/entities/jp.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - Scrapling `StealthySession` で SuperCombo から直接取得した。Jina などの第三者 cache/API は使っていない。
  - `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 64 件を抽出した。
  - Cargo API は `SF6_FrameData` 64 行、`SF6_CharacterData` 1 行を返し、raw template 件数と一致した。
  - `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 tab state と、4 section x 5 tab = 20 table comparisons を保存した。
  - 5枚の full-page screenshot は目視確認済み。Character Data、各 tab の table、下部 navigation、footer が写っている。
  - 画像参照 143 件、distinct filename 134 件のうち、MediaWiki `imageinfo` で 123 件を解決し、123 件を download した。
  - `tools/validate_supercombo_frame_data.py` は passed。warning は `11 imageinfo titles are missing`。
  - `python3 -m py_compile tools/capture_supercombo_frame_data.py tools/validate_supercombo_frame_data.py` は成功。
- 注意:
  - `6HPHK` と `236236K` は同じ input を持つ複数 row があるため、SuperCombo raw 内では `moveId` を行識別子として扱う。
  - 公式 data と重なる基本フレーム値では Capcom 公式 data を優先し、SuperCombo は公式にない range、juggle、notes、hitbox image などを後で統合する候補 source として扱う。
- 未解決事項:
  - `imageinfo` で missing になった 11 件の画像参照を、削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。
  - 公式 JP data と SuperCombo `moveId` rows の crosswalk policy をどう定義するか。
  - SuperCombo の HTML 装飾付き frame advantage を、公式 CSV と比較可能な値へ正規化する schema をいつ作るか。

## [2026-05-31] 出力 | SuperCombo JP 派生データと公式 JP 候補照合
- 追加:
  - `tools/extract_supercombo_frame_data.py`
  - `wiki/outputs/data/supercombo/frame-data/jp/frames.csv`
  - `wiki/outputs/data/supercombo/frame-data/jp/frames.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/character.csv`
  - `wiki/outputs/data/supercombo/frame-data/jp/schema.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-official-classic.csv`
  - `wiki/outputs/data/supercombo/frame-data/jp/crosswalk-summary.json`
  - `wiki/outputs/data/supercombo/frame-data/jp/supercombo-unmatched.csv`
  - `wiki/outputs/reports/2026-05-31-supercombo-jp-official-crosswalk.md`
- 更新:
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - `tools/extract_supercombo_frame_data.py` は SuperCombo validation passed の raw snapshot だけを入力にする。
  - `frames.csv` は 64 rows、`character.csv` は 1 row。
  - 公式 JP Classic 69 rows との候補照合は、automatic matched 63、JP 固有名 override matched 4、unmatched 2。
  - SuperCombo 側は 64 rows 中 57 distinct rows が候補照合され、7 rows が公式 Classic frame row にはない補助候補として残った。
  - `python3 -m py_compile tools/extract_supercombo_frame_data.py` は成功。
- 注意:
  - crosswalk は最終マージではなく review 用候補。公式に存在する基本フレーム値は Capcom 公式 data を正とする。
  - `前方ステップ` と `後方ステップ` は公式側 unmatched。SuperCombo では frame row ではなく character data の dash fields に対応する可能性がある。
- 未解決事項:
  - `matched_manual` 4件と多対一対応 rows を人間レビューして、正式 merge policy に昇格するか。
  - SuperCombo unmatched 7 rows を公式 row の補助情報として扱うか、SuperCombo-only rows として保持するか。

## [2026-05-31] 出力 | JP 公式データへの SuperCombo 補助列付与
- 追加:
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/jp/supercombo-only.csv`
  - `wiki/outputs/data/enriched/frame-data/jp/schema.json`
  - `wiki/outputs/data/enriched/frame-data/jp/summary.json`
  - `wiki/outputs/reports/2026-05-31-jp-official-supercombo-enriched-data.md`
- 更新:
  - `wiki/outputs/reports/2026-05-31-supercombo-jp-official-crosswalk.md`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - 公式 JP Classic 69 rows を保持したまま、SuperCombo 補助列を `supercombo_*` prefix で追加した。
  - enriched rows は 69。内訳は enriched 62、enriched review required 5、official only 2。
  - SuperCombo-only rows は 7。suggested handling は supplemental variant 2、supplemental followup 2、taunt 3。
  - 基本値 conflict は damage 1件、startup 1件。
  - `python3 -m py_compile tools/build_official_supercombo_enriched_data.py` は成功。
- 注意:
  - この output は公式 CSV の置換ではない。公式にある基本フレーム値は公式列を正とし、SuperCombo 値は補助列に分離している。
  - `enriched_review_required` の 5 rows は人間レビューが必要。
- 未解決事項:
  - `ヴィーハト・チェーニ` と `SA2 ラヴーシュカ` の conflict をどう扱うか。
  - official only の前方/後方ステップを、SuperCombo character data の dash fields と別枠で結合するか。

## [2026-05-31] レビュー | JP 公式 + SuperCombo 補助行の人間レビュー反映
- 更新:
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/jp/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/jp/schema.json`
  - `wiki/outputs/data/enriched/frame-data/jp/summary.json`
  - `wiki/outputs/reports/2026-05-31-jp-official-supercombo-enriched-data.md`
  - `wiki/outputs/reports/2026-05-31-supercombo-jp-official-crosswalk.md`
  - `wiki/sources/supercombo-jp-frame-data.md`
  - `wiki/log.md`
- 決定:
  - `ヴィーハト・アクノ`、`パリィドライブラッシュ`、`キャンセルドライブラッシュ` は `supplemental_link` として採用。
  - `ヴィーハト・チェーニ` は `non_additive_supplemental_damage`。発火した spike damage は補助情報で、元ヴィーハト damage と合算しない。
  - `SA2 ラヴーシュカ` は startup conflict付き補助情報。公式 startup 29 を正とする。
- 検証:
  - enriched status は `enriched` 62 rows、`enriched_reviewed` 5 rows、`official_only` 2 rows。
  - human review decisions は `supplemental_link` 3、`non_additive_supplemental_damage` 1、`conflict_supplemental_only` 1。
  - `python3 -m py_compile tools/build_official_supercombo_enriched_data.py` は成功。
- 未解決事項:
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。
  - 多対一対応 rows と SuperCombo-only rows の正式 merge policy。

## [2026-05-31] 取り込み | SuperCombo Ryu フレームデータ取得
- 追加:
  - `raw/supercombo/frame-data/2026-05-31/ryu/`
  - `wiki/sources/supercombo-ryu-frame-data.md`
  - `wiki/reviews/2026-05-31-supercombo-ryu-frame-data-capture-review.md`
- 更新:
  - `tools/validate_supercombo_frame_data.py`
  - `wiki/index.md`
  - `wiki/entities/ryu.md`
  - `wiki/entities/supercombo-wiki.md`
  - `wiki/entities/street-fighter-6.md`
  - `wiki/concepts/frame-data.md`
  - `wiki/log.md`
- 検証:
  - Scrapling `StealthySession` で SuperCombo から直接取得した。Jina などの第三者 cache/API は使っていない。
  - `Data?action=raw` から `CharacterData-SF6` 1 件、`FrameData-SF6` 77 件を抽出した。
  - Cargo API は `SF6_FrameData` 77 行、`SF6_CharacterData` 1 行を返し、raw template 件数と一致した。
  - `General`、`Details`、`Meter`、`Properties`、`Notes` の 5 tab state と、4 section x 5 tab = 20 table comparisons を保存した。
  - 5枚の full-page screenshot は目視確認済み。Character Data、各 tab の table、下部 navigation、footer が写っている。
  - 画像参照 173 件、distinct filename 134 件のうち、MediaWiki `imageinfo` で 133 件を解決し、133 件を download した。
  - `uv run python tools/validate_supercombo_frame_data.py --repo-root . --date-label 2026-05-31 --character-slug ryu` は成功。warning は `1 imageinfo titles are missing`。
  - `uv run python -m py_compile tools/capture_supercombo_frame_data.py tools/validate_supercombo_frame_data.py` は成功。
- 注意:
  - Ryu は duplicate input が 10 種類あるため、SuperCombo raw 内では `moveId` を行識別子として扱う。
  - Ryu では `moveType` に `Special` / `Super` の大文字表記があるため、validator で小文字正規化するようにした。
- 未解決事項:
  - missing imageinfo の `File:SF6 Ryu 236p hitbox.png` を、削除済み/未作成ファイルとして扱うか、filename 正規化で再解決できるか。
  - Ryu の Denjin / hold level / duplicate input rows の merge policy。

## [2026-05-31] 出力 | SuperCombo Ryu 派生データと公式 Ryu 補助データ生成
- 追加:
  - `wiki/outputs/data/supercombo/frame-data/ryu/frames.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/frames.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/character.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/schema.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-official-classic.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/supercombo-unmatched.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/supercombo-only.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/schema.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/summary.json`
  - `wiki/outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk.md`
  - `wiki/outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data.md`
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/index.md`
  - `wiki/log.md`
- 検証:
  - SuperCombo Ryu derived `frames.csv` は 77 rows、`character.csv` は 1 row。
  - 公式 Ryu Classic 75 rows との候補照合は matched 61、ambiguous 10、generic name override matched 2、unmatched 2。
  - enriched rows は 75。内訳は `enriched` 60、`enriched_review_required` 13、`official_only` 2。
  - SuperCombo-only rows は 14。suggested handling は `supercombo_only` 10、`supercombo_only_taunt` 4。
  - `uv run python -m py_compile tools/extract_supercombo_frame_data.py tools/build_official_supercombo_enriched_data.py` は成功。
- 注意:
  - Ryu の `enriched_review_required` 13 rows は accepted 扱いにしない。
  - `パリィドライブラッシュ` / `キャンセルドライブラッシュ` は generic name override で紐づけるが、人間レビューは未完了。
- 未解決事項:
  - Ryu の review-required 13 rows を人間レビューする。
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。

## [2026-05-31] レビュー | Ryu 公式 + SuperCombo 補助行の人間レビュー反映
- 更新:
  - `tools/extract_supercombo_frame_data.py`
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-official-classic.csv`
  - `wiki/outputs/data/supercombo/frame-data/ryu/crosswalk-summary.json`
  - `wiki/outputs/data/supercombo/frame-data/ryu/supercombo-unmatched.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/supercombo-only.csv`
  - `wiki/outputs/data/enriched/frame-data/ryu/summary.json`
  - `wiki/outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk.md`
  - `wiki/outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data.md`
  - `wiki/sources/supercombo-ryu-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 決定:
  - `[電刃錬気]波動拳`、`[電刃錬気]OD 波動拳`、`[電刃錬気]波掌撃`、`[電刃錬気]SA1 真空波動拳` は Denjin / charged variant の `move_id` に補助リンクする。
  - `SA2 真波掌撃（Lv2/Lv3）` と `[電刃錬気]SA2 真波掌撃（Lv2/Lv3）` は hold-level variant の `move_id` に補助リンクする。
  - `OD 波掌撃` は active duration conflict 付き補助情報として扱い、公式 active `18-22` を正とする。
  - `パリィドライブラッシュ` と `キャンセルドライブラッシュ` は補助リンクとして採用する。
- 検証:
  - enriched status は `enriched` 60 rows、`enriched_reviewed` 13 rows、`official_only` 2 rows。
  - human review decisions は `supplemental_link` 8、`hold_level_supplemental_link` 4、`conflict_supplemental_only` 1。
  - crosswalk は matched 61、matched_manual 10、ambiguous 2、unmatched 2。
  - SuperCombo-only rows は 6。`6HK~214K` / `6HK~214KK` と taunt 4件のみ。
  - 公式由来列は `wiki/outputs/data/frame-data/ryu/classic.csv` と enriched output で全行一致した。
  - `uv run python -m py_compile tools/extract_supercombo_frame_data.py tools/build_official_supercombo_enriched_data.py` は成功。
- 注意:
  - 公式に存在する damage / startup / active / recovery などの基本数値は公式列を正とし、SuperCombo 値は `supercombo_*` 補助列として保持する。
  - SA2 Lv2 / Lv3 の SuperCombo startup `18~` / `50~` は hold-level 補助情報で、公式 startup 20 / 70 を上書きしない。
- 未解決事項:
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。
  - SuperCombo-only の `6HK~214K` / `6HK~214KK` を公式 row の補助情報として扱うか。

## [2026-06-01] レビュー | Ryu SuperCombo-only 空中竜巻 variant link
- 更新:
  - `tools/build_official_supercombo_enriched_data.py`
  - `wiki/outputs/data/enriched/frame-data/ryu/classic-supercombo.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/schema.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/summary.json`
  - `wiki/outputs/data/enriched/frame-data/ryu/supercombo-only.csv`
  - `wiki/outputs/reports/2026-05-31-ryu-official-supercombo-enriched-data.md`
  - `wiki/outputs/reports/2026-05-31-supercombo-ryu-official-crosswalk.md`
  - `wiki/sources/supercombo-ryu-frame-data.md`
  - `wiki/index.md`
  - `wiki/log.md`
- 決定:
  - `ryu_6hk_214k` は primary official row 41 `空中竜巻旋風脚`、enabled-by row 23 `旋風脚` の conditional variant として扱う。
  - `ryu_6hk_214kk` は primary official row 42 `OD 空中竜巻旋風脚`、enabled-by row 23 `旋風脚` の conditional variant として扱う。
  - row 23 `旋風脚` の damage 800 / startup 16 と、キャンセル後の空中竜巻派生 damage / startup は合算・上書きしない。
- 検証:
  - SuperCombo-only suggested handling は `supplemental_variant_row` 2、`supercombo_only_taunt` 4。
  - `supercombo-only.csv` に `primary_official_row_order`、`enabled_by_official_row_order`、`link_note` などの link fields を追加した。
  - 公式由来列は `wiki/outputs/data/frame-data/ryu/classic.csv` と enriched output で全行一致した。
  - `uv run python -m py_compile tools/build_official_supercombo_enriched_data.py` は成功。
- 未解決事項:
  - 前方/後方ステップを SuperCombo CharacterData dash fields と別リンクするか。
  - conditional variant link を他 character にも使う場合、どこまで汎用 schema 化するか。
