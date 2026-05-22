# Current Source Acquisition Implementation

Status: Implementation in progress; external visual cross-check recorded as reviewer evidence; awaiting mandatory review.

## Purpose

Plan the first actual latest-source acquisition implementation before current
fact JSON Schema redesign.

This ExecPlan intentionally changes the Phase 1 order:

1. Acquire and review current source data.
2. Build value-shape inventory artifacts from that current data.
3. Redesign current-fact JSON Schemas from the reviewed inventory.

JSON Schema redesign is therefore not approved by this ExecPlan. Existing
`data/exports/` files remain useful reference data, but they are not enough to
design the next schema layer without current official and SuperCombo source
captures.

## Scope

Included:

- Plan the next implementation slice for acquiring latest official
  all-character raw source data from current official roster URLs with
  Scrapling.
- Plan how latest SuperCombo all-character raw source data is either acquired
  in the same implementation or explicitly queued for a separate acquisition
  implementation.
- Require a repo-local ignored transient acquisition workspace for raw HTML,
  cache, debug output, browser traces, screenshots, and candidate extracted
  data.
- Require production acquisition, `--workspace`, and artifact validation
  workspace overrides to stay under `.local/source-acquisition/`.
- Define the public artifact boundary for the next implementation.
- Require exact preservation of raw source values in the acquisition workspace.
- Require source URL, final URL, captured-at UTC timestamp, HTTP status,
  content type, and source/version/revision labels when available.
- Require an acquisition report sufficient to prove coverage and freshness.
- Require Scrapling for source acquisition. Direct `urllib`, `requests`, or
  dependency-free HTTP acquisition is not acceptable for the final
  implementation.
- Require source-specific extracted raw artifacts, not only full HTML and
  hashes.
- Require official raw cell artifacts to separate rendered visible text from
  full source text and hidden/detail text.
- Require `uv` plus Python 3.12 for the implementation environment.
- Preserve authority boundaries:
  - official source data is authority candidate only until later deterministic
    parser, schema, validator, and review gates pass.
  - SuperCombo source data is enrichment, cross-reference, or candidate
    evidence only.
- Define a minimal acquisition-report shape. This is not a JSON Schema
  redesign.

Excluded:

- No implementation outside this source-acquisition slice.
- No current-fact JSON Schema redesign.
- No source row schema implementation.
- No parser or classifier.
- No normalized export.
- No retrieval changes.
- No answer behavior changes.
- No daily-answer web mode.
- No Discord adapter.
- No VLM runner or video pipeline.
- No API fallback.
- No vector search.
- No private vault or private overlay DB.
- No persistent DB.
- No generated DB.
- No `sf6 ask`.
- No full raw HTML committed to the public repo unless a later source-boundary
  review explicitly approves it.
- No public data artifacts unless a later implementation step explicitly
  defines reviewed artifact paths, minimal shapes, and validation checks.

## Acceptance Criteria

- The plan states that latest source acquisition comes before value-shape
  inventory artifact implementation and JSON Schema redesign.
- The plan scopes official acquisition across every roster character in
  `data/roster/current-character-roster.json`.
- The plan states that missing or failing official URLs are coverage failures
  or review items, not silent exclusions.
- The plan decides the smallest next implementation slice for SuperCombo:
  SuperCombo is queued by default unless reviewer explicitly expands the next
  implementation to acquire it in the same slice.
- The plan states that raw source values must be preserved exactly in the
  repo-local ignored acquisition workspace.
- The implementation rejects acquisition workspaces outside the repo-local
  ignored `.local/source-acquisition/` boundary.
- The plan states that the public repo receives only a reviewed acquisition
  report by default, not full raw HTML or source row data.
- The implementation uses Scrapling for acquisition and records
  `capture_method: scrapling_fetcher` for successful and failed official
  entries.
- Official raw row artifacts preserve `visible_text`, `source_text`,
  `source_text_stripped`, and `hidden_detail_text` separately, and do not label
  hidden/source-only text as visible.
- Official raw row artifacts preserve source header structure and per-cell
  source column header paths so key/value mapping is reviewable without
  relying on positional inference.
- The external reviewer visual cross-check evidence is recorded in this
  ExecPlan, but no browser-based validator is committed in this implementation
  slice.
- The plan defines the minimum acquisition-report fields needed to prove
  coverage and freshness.
- The plan states that official data is not `current_fact_authority` until
  later deterministic parser/schema/validator/review gates pass.
- The plan states that SuperCombo is not daily-answer numeric authority.
- The implementation does not create schemas, normalized data artifacts,
  parser/classifier behavior, answer behavior, retrieval behavior, persistent
  DBs, private vault, Discord, VLM, API fallback, vector search, or `sf6 ask`.
- Implementation validation passes.

## Files / Interfaces

Changed by this ExecPlan:

- `docs/execplans/2026-05-21-current-source-acquisition-implementation.md`

Implementation files added:

- `.gitignore`
- `pyproject.toml`
- `uv.lock`
- `src/sf6_knowledge_coach/source_acquisition.py`
- `tests/test_source_acquisition.py`
- `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`

Inputs used for planning:

- `docs/PLAN.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md`
- `docs/execplans/2026-05-21-official-raw-snapshot-acquisition.md`
- `docs/execplans/2026-05-21-supercombo-raw-snapshot-acquisition.md`
- `docs/execplans/2026-05-21-value-shape-inventory.md`
- `data/roster/current-character-roster.json`
- existing `data/exports/` for historical comparison only

This implementation must add a Scrapling-based acquisition module, tests,
repo-local ignored raw snapshot artifacts, and one public acquisition report.
Later public source row artifacts, schemas, validators, parsers, normalized
exports, or retrieval changes require separate reviewed ExecPlans.

## Reference-Only Legacy Notes

The deleted v2.3 frame-data ingestion code is reference-only. It must not be
copied verbatim.

Reference-only surfaces:

- `ingest/frame_data/src/sf6_ingest/fetch/scrapling_client.py`: profile-based
  Scrapling fetch, retry, and challenge metadata ideas.
- `ingest/frame_data/src/sf6_ingest/fetch/official.py`: official snapshot
  metadata boundary ideas.
- `ingest/frame_data/src/sf6_ingest/fetch/supercombo.py`: SuperCombo snapshot
  metadata boundary ideas.
- `ingest/frame_data/src/sf6_ingest/core/io.py`: `page.html` plus
  `metadata.json` local snapshot layout ideas.
- `ingest/frame_data/src/sf6_ingest/core/official.py`: official table header,
  15-cell row shape, group heading, and raw row preservation ideas.
- `ingest/frame_data/src/sf6_ingest/core/supercombo.py`: SuperCombo main table,
  heading chain, table rows, and field map ideas.
- `ingest/frame_data/config/fetch_profiles.yaml`: official `Fetcher` and
  SuperCombo `StealthyFetcher` profile ideas.

The clean-slate implementation must be redesigned in this repo's current
structure.

## Scrapling Requirement

Scrapling is mandatory for the official acquisition implementation.

Local Codex skill installation:

```text
.agents/skills/Scrapling-Skill
```

This is a repo-local ignored Codex skill installation and is not a public repo
artifact. Do not install project skills into Windows-side or WSL-side global
Codex homes for this repo. Use the repo-local `.venv` for Scrapling runtime
checks. Codex may need to be restarted before the installed skill is
automatically discoverable in future sessions. The current implementation must
still follow the installed skill's requirements.

Dependency and environment decision:

- Use `uv` with Python 3.12.
- Add a focused project dependency on `scrapling[all]`.
- Pin the accepted range as `scrapling[all]>=0.4.8,<0.5` unless review changes
  it.
- Record Scrapling license suitability before PR readiness. The installed
  skill includes `LICENSE.txt` with BSD 3-Clause terms.
- Run browser dependency setup only if the chosen Scrapling fetcher requires it.
- Prefer `scrapling.fetchers.Fetcher` for the first official source capture.
- If JavaScript rendering is required, stop for review before switching to
  `DynamicFetcher`, `StealthyFetcher`, browser dependency setup, or broader
  scraping behavior.
- Do not use direct `urllib` or `requests` acquisition as a fallback.

## Next Implementation Slice

The revised smallest implementation slice is:

1. Acquire latest official source documents for every roster character.
2. Extract official source-specific raw artifacts for every roster character.
3. Acquire latest SuperCombo source documents for every roster character or
   record explicit per-character blockers.
4. Extract SuperCombo source-specific raw table artifacts where acquisition
   succeeds.
5. Store raw capture/cache/debug outputs under repo-local ignored `.local/`.
6. Produce a reviewed public acquisition report.

Decision: acquire official and SuperCombo source snapshots with Scrapling, but
keep SuperCombo as enrichment/cross-reference/candidate only.

Rationale:

- Official sources are the only future `current_fact_authority` candidate.
- SuperCombo remains enrichment/cross-reference/candidate evidence and must not
  become numeric authority.
- Keeping the first implementation smaller reduces risk before schema and
  validator work exists.

## Official Acquisition Scope

The official acquisition scope is every character in
`data/roster/current-character-roster.json`.

Current planning observation: the roster contains 29 characters, and every
listed character currently has `sources.official`.

Future acquisition must record each character:

- `character_slug`
- `display_name`
- `source_family`: `official`
- `source_role`: `current_fact_authority_candidate`
- `source_url`
- `final_url`
- `captured_at_utc`
- `http_status`
- `content_type`
- `content_length` when available
- `source_version_label` when visible or inferable from source metadata
- `source_revision_label` when visible or inferable from source metadata
- `capture_method`: `scrapling_fetcher`
- `capture_success`
- `failure_reason` when applicable
- `content_hash` for captured repo-local ignored raw content
- `artifact_boundary`: `repo_local_ignored_raw_capture`

This acquisition report field naming is report-local. Later normalized
current-fact schema work must not inherit `source_family: official` as a
semantic family; official/SuperCombo source identity must move to
`source_name` / `source_role` or equivalent source identity fields.

If any roster character lacks `sources.official`, returns a non-success HTTP
status, redirects to an unexpected page, or lacks expected source content, the
implementation must record a coverage failure or review item. It must not
silently drop the character.

JP remains one roster character and the initial active character package. It
must not become a hardcoded acquisition special case.

## Extracted Raw Artifact Requirements

The implementation must not stop at `page.html` and content hashes. Each
successful source capture must write source-specific extracted raw artifacts
under `.local/source-acquisition/`.

Official per-character local artifacts:

```text
.local/source-acquisition/current-source-acquisition/<run_id>/official/<character_slug>/page.html
.local/source-acquisition/current-source-acquisition/<run_id>/official/<character_slug>/metadata.json
.local/source-acquisition/current-source-acquisition/<run_id>/official/<character_slug>/__NEXT_DATA__.json
.local/source-acquisition/current-source-acquisition/<run_id>/official/<character_slug>/official_table_rows.raw.json
```

Official `official_table_rows.raw.json` must preserve:

- raw table header structure
- expected source column header paths
- extracted source column header paths
- table index
- row index
- group heading
- cell index
- column index
- `source_column_header_path`: source header labels for the cell
- `source_column_leaf_header`: final source header label for the cell
- `visible_text`: rendered visible cell text, matching browser `innerText`
- `source_text`: full source cell text, including hidden/source-only detail
- `source_text_stripped`: source text normalized for exact-source comparison,
  not treated as rendered visible text
- `hidden_detail_text`: hidden/source-only detail text when present
- input image `src`
- input image `alt`
- no numeric interpretation

The key names must be honest. Hidden/source-only text must not be stored under
`visible_text` or any legacy `text_stripped` field that implies rendered
visibility. Hidden details such as active-frame split ranges must be preserved
for later value-shape inventory, but they are not visible display values.

Official expected source column header paths are:

```text
技名
動作フレーム > 発生
動作フレーム > 持続
動作フレーム > 硬直
硬直差 > ヒット
硬直差 > ガード
キャンセル
ダメージ
コンボ補正値
Dゲージ増加 > ヒット
Dゲージ減少 > ガード
Dゲージ減少 > パニッシュカウンター
SAゲージ増加
属性
備考
```

Official extraction must validate:

- expected official header markers
- expected source column header paths in exact official order
- table count
- raw row count
- expected 15-cell data row shape
- official cell payload fields and absence of legacy `text_stripped`
- official row payload fields: `table_index`, `row_index`, `group_heading`,
  `cell_count`, and `input_images`
- official input image `src` and `alt` fields, including per-cell `image_src`
  and `image_alt`
- row/cell count drift as review items
- deterministic local-file artifact validation for official row/cell structure
  and image fields

SuperCombo per-character local artifacts:

```text
.local/source-acquisition/current-source-acquisition/<run_id>/supercombo/<character_slug>/page.html
.local/source-acquisition/current-source-acquisition/<run_id>/supercombo/<character_slug>/metadata.json
.local/source-acquisition/current-source-acquisition/<run_id>/supercombo/<character_slug>/supercombo_tables.raw.json
```

SuperCombo `supercombo_tables.raw.json` must preserve:

- heading chain
- table index
- row index
- cell index
- exact visible cell text
- no binding
- no normalization
- no numeric interpretation

## SuperCombo Handling

SuperCombo acquisition is included in the redesigned implementation.

The implementation must still record a SuperCombo decision:

- `same_run_approved`: reviewer expanded the implementation before coding and
  the same source-boundary and repo-local ignored raw workspace rules are
  applied.
- `blocked`: source boundary, source availability, or capture approach needs
  review before acquisition.

SuperCombo policy:

- SuperCombo is enrichment, cross-reference, or candidate evidence only.
- SuperCombo does not override official data.
- SuperCombo does not become daily-answer numeric authority.
- Conflicts with official source data become review items.

SuperCombo acquisition Cloudflare boundary:

- `solve_cloudflare=True` is approved for the committed SuperCombo source
  acquisition update mode only, inside the Scrapling `StealthyFetcher` capture
  path.
- This is update/research acquisition behavior, not daily-answer runtime
  behavior.
- This approval does not make SuperCombo numeric authority.
- Do not add `solve_cloudflare=True` to CI, deterministic validators, ordinary
  tests, daily-answer mode, retrieval, answer preparation, answer verification,
  Discord, or any non-acquisition runtime path.
- Do not store cookies, browser profiles, request headers with secrets, traces,
  or raw browser artifacts in the public repo.

## SuperCombo Reviewer-Only Visual Evidence

The prior SuperCombo external visual-review status is updated from blocked to
reviewer-observed pass. SuperCombo live-rendered pages were retried with
reviewer-only Scrapling/Patchright observation using `solve_cloudflare=True`.

Review boundary:

- `solve_cloudflare=True` was also approved and used for reviewer external
  observation, separately from the committed SuperCombo acquisition update-mode
  path above.
- Do not add Scrapling MCP screenshots, Patchright browser session logic,
  real Chrome, CDP, cookies, browser profiles, browser traces, screenshot
  comparison, or visual LLM review to committed repo code, CLI commands, CI,
  tests, deterministic validators, `pyproject.toml`, or daily-answer runtime
  behavior.
- Screenshot and visual evidence remains reviewer evidence only. It must not
  create parsed values, current-fact authority, deterministic parser rules, or
  daily-answer evidence.
- SuperCombo remains enrichment, cross-reference, or candidate evidence only.
  It is not numeric authority.

Reviewer-only evidence:

- All 29 roster SuperCombo pages were reachable.
- Result: pass 29, blocked 0, mismatch 0, uncertain 0.
- Evidence was kept outside the repo under:
  `/tmp/sf6-supercombo-scrapling-visual-review/`.
- 174 screenshots were captured outside the repo.
- Summary files were kept outside the repo:
  - `/tmp/sf6-supercombo-scrapling-visual-review/review-summary.json`
  - `/tmp/sf6-supercombo-scrapling-visual-review/review-summary.md`
- The review compared live-rendered pages against ignored local
  `supercombo_tables.raw.json` artifacts for table count, row count, heading
  chain, and compatible cell text.
- Presentation-only spacing differences around symbols such as `()`, `[]`,
  `*`, `/`, and `+` were treated as compatible for reviewer observation only.

## Source Update And Drift Policy

Expected normal update pattern:

- Frame/current values may change after game updates.
- Notes and special value expressions may be added or changed.
- Official and SuperCombo each likely use source-specific but somewhat
  consistent special-expression conventions.

Less likely but possible update pattern:

- Moves may be added, removed, or renamed.
- Official source columns may be added, removed, or renamed.
- SuperCombo heading/table structure may change.

Policy:

- Do not silently skip changed, missing, extra, or structurally drifted data.
- Do not silently coerce new source expressions into old shapes.
- Do not treat changed structure as successful acquisition.
- Do not hide drift behind partial success.
- Any structural drift, changed extraction shape, missing expected table,
  unexpected column/header, changed row/cell mapping, or new unclassified value
  expression must become a hard failure or explicit human review item.
- Human review must identify what changed, which source changed, which
  characters and fields are affected, and whether acquisition, schema, parser,
  or classifier updates are needed.
- If the user explicitly confirms move additions, removals, or renames, then a
  later ExecPlan may update roster and move identity handling.
- New notes and special expressions must be preserved exactly first, then
  analyzed in value-shape inventory.
- For official and SuperCombo separately, later deterministic classifier work
  should attempt to understand the meaning of repeated special-expression
  conventions rather than leaving them permanently as opaque raw strings.
- Until deterministic interpretation is approved, such values remain
  raw-preserved and are not numeric authority.

PR scope clarification:

- This PR establishes reproducible acquisition, raw artifact preservation,
  report/hash/count integrity, and drift detection/review boundaries.
- This PR does not implement normalized schema, parser/classifier, retrieval,
  answer behavior, or authority promotion.
- Daily-answer authority remains unchanged.

## Downstream Value-Shape Handoff

JSON Schema redesign remains blocked until latest-source value-shape inventory
is reviewed. The current official raw artifacts have been reviewed across 29
characters, 2,286 official rows, and 34,290 official cells. That review found
special source expressions that must be handed to the later value-shape
inventory and normalized schema work explicitly.

Official current-source special value shapes include at least:

- `動作フレーム > 発生`: blank values, note-suffixed values such as `122※`,
  and plus expressions such as `6+0`.
- `動作フレーム > 持続`: ranges, hidden-detail multihit values,
  until-landing text such as `着地まで`, malformed-looking source ranges such
  as `20-24.25` and `23--33`, and note-suffixed ranges.
- `動作フレーム > 硬直`: landing recovery expressions such as `着地後N`,
  compound landing expressions such as `N+着地後M`, note-prefixed integers
  such as `※11`, and compound note values.
- `硬直差 > ヒット` and `硬直差 > ガード`: `D`, blank values, dash variants
  such as `-`, `―`, and `ー`, signed integers, ranges such as `0～11`,
  note-prefixed signed values such as `※-10`, and compound source values such
  as `-60※-93`.
- `キャンセル`: categorical values such as `C`, `SA`, `SA2`, `SA3`, and
  note variants such as `※SA2`. These are not numeric fields.
- `ダメージ`: note-prefixed values such as `※500` and note-separated
  alternate values such as `2200※1850`.
- `コンボ補正値`: Japanese correction expressions such as `始動補正20%` and
  `即時補正10%`, multiple concatenated correction terms, and mixed ASCII or
  full-width percent signs.
- Gauge fields: mostly numeric, but blank values and note-prefixed values
  exist and must not be coerced without deterministic rules.
- `属性` and `備考`: category, prose, and free-text source content. These are
  not numeric authority.

Raw source text must remain source-native and exactly preserved. English
canonical field keys belong in the later normalized schema layer, not in this
raw acquisition layer. The later mapping design must explicitly connect:

- official Japanese source header paths,
- SuperCombo English source labels and heading paths, and
- display labels for Japanese answers.

No field may be coerced to integer merely because most values look numeric.
Unknown, rare, malformed-looking, or source-specific expressions remain
raw-only and unparsed until deterministic classifier rules are approved.
SuperCombo requires a separate value-shape inventory before any
merge/cross-reference/schema decision because its table, heading, and value
system is source-specific and not the same as the official 15-column table.

## Schema Boundary Decision

Raw acquisition artifacts are source-fidelity artifacts only. They must not
translate, canonicalize, infer, coerce, or normalize source field names or
source values. `source_column_header_path` must remain the exact source-native
label path, including official Japanese labels.

English canonical keys belong only to a later normalized current-fact schema
ExecPlan. That later schema should separate at least:

- `field_key`: English canonical field key for internal joins and tooling.
- `source_label`: source-native field label.
- `source_header_path`: source-native header or heading path.
- `source_family`: semantic category such as `timing`, `advantage`, `damage`,
  `gauge`, `cancel`, `attribute`, or `note`.
- `source_name` / `source_role`: source identity and evidence role, such as
  official authority candidate or SuperCombo enrichment/candidate.
- `display_label_ja`: Japanese answer/display label.
- `raw_value`, `parsed_value`, and `value_shape`: raw-preserved value,
  deterministic parsed value when approved, and source expression class.
- `authority_status`: whether the value is authority candidate, reviewed
  current-fact authority, enrichment, candidate, deprecated, or rejected.

In the later normalized schema, `source_family` must not be used to mean
`official` or `supercombo`; those belong in source identity and evidence-role
fields such as `source_name` and `source_role`. Official Japanese header labels
and SuperCombo English labels require an explicit mapping design before any
merge, cross-reference, or answer behavior can use them together.

JSON Schema redesign remains blocked until latest-source value-shape inventory
and these mapping requirements are reviewed.

## Repo-Local Ignored Acquisition Workspace

Future acquisition must write raw source captures and intermediate files under
the repo-local ignored workspace:

```text
.local/source-acquisition/current-source-acquisition/<run_id>/
```

Allowed ignored local contents:

- Raw HTML or equivalent source documents.
- HTTP response headers with secrets removed.
- Fetch cache.
- Debug logs.
- Browser traces or screenshots if needed.
- Candidate extracted tables or rows before review.
- Coverage diagnostics.

Rules:

- Do not commit `.local/` paths.
- Do not write raw acquisition artifacts outside `.local/source-acquisition/`.
- Do not allow environment variables or `--workspace` to move raw acquisition
  artifacts outside `.local/source-acquisition/`.
- Do not commit cookies, credentials, auth headers, or browser profile data.
- Do not commit local absolute paths.
- Do not store private user data.
- Do not use repo-local ignored transient files as daily-answer authority.
- Do not commit full raw HTML unless source-boundary review explicitly
  approves public redistribution.

The default workspace must be:

```text
.local/source-acquisition/current-source-acquisition/<run_id>/
```

Any explicit workspace override must still resolve under:

```text
.local/source-acquisition/
```

The exact absolute path remains local-only and must not be written into
committed artifacts.

## Public Artifact Boundary

The default public artifact for the next implementation is a reviewed
acquisition report, not raw source data.

Implemented report path:

```text
docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
```

The public report may include:

- Run identifier.
- Commit SHA and branch used for acquisition.
- Source families covered.
- Expected character count.
- Successful capture count.
- Failed capture count.
- Per-character source URL and final URL.
- HTTP status.
- Content type.
- Captured-at UTC timestamp.
- Source/version/revision labels when available.
- Content hashes for repo-local ignored raw captures.
- Source-boundary review status.
- Coverage failures and review items.
- Statement that raw source values are preserved in repo-local ignored storage.
- Statement that no captured raw source data is daily-answer authority.
- SuperCombo acquisition decision.

The public report must not include:

- Full raw HTML.
- Full source tables or source row dumps.
- Cookies, credentials, request headers with secrets, or browser profile data.
- Local absolute paths.
- Private vault data.
- Answer logs.
- Training logs.
- Real user profile data.

Future public raw row or source snapshot artifacts are out of scope for the
smallest next implementation unless a reviewer approves exact paths, minimal
artifact shapes, and validation checks before coding.

## Minimal Acquisition Report Shape

This is a planning shape for a Markdown or similarly reviewable report. It is
not a JSON Schema redesign.

```yaml
acquisition_report:
  run_id: string
  captured_at_utc: string
  source_families:
    - official
  roster:
    roster_path: data/roster/current-character-roster.json
    expected_character_count: 29
  official_coverage:
    expected_count: 29
    captured_count: integer
    failed_count: integer
    review_item_count: integer
  supercombo_decision:
    status: queued | same_run_approved | blocked
    reason: string
  source_boundary:
    full_raw_html_public_commit: prohibited_without_explicit_review
    reviewed_terms_license_robots_attribution: pending | reviewed
  entries:
    - character_slug: string
      display_name: string
      source_family: official
      source_role: current_fact_authority_candidate
      source_url: string
      final_url: string
      captured_at_utc: string
      http_status: integer
      content_type: string
  source_version_label: string | unknown
  source_revision_label: string | unknown
  capture_success: boolean
  failure_reason: string | null
  content_hash: string | null
  official_raw_row_count: integer
  official_table_count: integer
  official_next_data_present: boolean
  artifact_boundary: repo_local_ignored_raw_capture
  supercombo_coverage:
    expected_count: 29
    captured_count: integer
    failed_count: integer
    review_item_count: integer
  review_items:
    - string
```

If the implementation cannot prove coverage and freshness with this shape, it
must update this ExecPlan's Decision Log or create a follow-up ExecPlan before
broadening artifacts.

## Source Boundary Review

Before any full raw HTML or equivalent source document is committed, a later
implementation must record explicit review of:

- Source terms.
- License.
- Robots policy.
- Attribution requirements.
- Source-specific redistribution limits.

Privacy checks and hashes are required but not sufficient to approve public raw
HTML. The default is to keep full raw source documents in repo-local ignored
storage and out of Git.

## Authority And Evidence Policy

Official source captures:

- Start as `current_fact_authority_candidate`.
- Are not daily-answer authority by themselves.
- May become `current_fact_authority` only after later deterministic
  parser/schema/validator/review gates.
- Must preserve exact raw source values before parsing.

SuperCombo source captures:

- Start as enrichment, cross-reference, or candidate evidence.
- Are not daily-answer numeric authority.
- Must not override official source data automatically.

Manual review, prose, FTS, and LLM memory are not numeric authority.

Daily answer behavior must not change in this unit.

## Implementation Guardrails

The implementation must:

- Stay in update/acquisition mode, not daily-answer mode.
- Use current roster URLs from `data/roster/current-character-roster.json`.
- Use Scrapling for every official source capture.
- Use Scrapling for every SuperCombo source capture.
- Keep public repo writes limited to the approved report and ExecPlan updates.
- Keep raw source documents in repo-local ignored `.local/` storage.
- Keep dependency changes limited to the reviewed Scrapling dependency.
- Stop and record a blocker if source content requires browser execution,
  login, cookies, non-Scrapling fallback code, or broad scraping behavior not
  covered by this plan.
- Preserve the paused retrieval runtime stash outside this work.

The implementation must not:

- Modify answer behavior.
- Modify retrieval behavior.
- Promote data to authority.
- Create normalized exports.
- Create persistent databases.
- Add API fallback or web daily-answer behavior.
- Apply unrelated paused runtime changes.
- Use direct `urllib`, `requests`, or dependency-free HTTP acquisition.

## Validation Commands

Baseline validation:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Implementation validation includes at minimum:

```bash
.venv/bin/python -c "from scrapling.fetchers import Fetcher; print(Fetcher.__name__)"
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
PYTHONPATH=src python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
PYTHONPATH=src python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md
git diff --check
git diff --cached --check
git status --short --branch
```

The live acquisition command used for the public report is:

```bash
PYTHONPATH=src .venv/bin/python -m sf6_knowledge_coach.source_acquisition official --include-supercombo --report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md --run-id 20260521T025403Z --sleep-seconds 0.1
```

The acquisition-report guard must run before review.

The acquisition-report guard must fail validation or block review if the public
report contains:

- Local absolute paths.
- User home paths.
- Browser profile paths.
- Cookies.
- Credentials.
- Auth headers.
- Tokens.
- Request headers with secrets.
- Private vault references.
- Answer logs.
- Training logs.
- Real user profile data.
- Full raw HTML.
- Full source tables or source row dumps.
- Public raw source references without explicit source-boundary review.

The same guard must require:

- Coverage validation for every roster character, with either successful
  official capture or an explicit official failure/review item.
- SuperCombo extracted table artifacts for every roster character, or an
  explicit SuperCombo failure/review item for each missing/blocked character.
- Expected roster count and observed report entry count.
- Recomputed official `captured_count`, `failed_count`, `review_item_count`,
  table count, and raw row aggregate must match `official_coverage`.
- Recomputed SuperCombo `captured_count`, `failed_count`, `review_item_count`,
  table count, and raw row aggregate must match `supercombo_coverage` when
  SuperCombo is included.
- `capture_method: scrapling_fetcher` for every official report entry.
- `capture_method: scrapling_stealthy_fetcher` for every SuperCombo report
  entry when SuperCombo is included.
- Official raw row count and SuperCombo table count recorded in the report.
- Source-boundary status recorded in the report.
- Artifact integrity validation against ignored `.local/` files:
  - `page.html` existence and `content_hash`
  - `metadata.json` existence and `metadata_hash`
  - official `__NEXT_DATA__.json` when reported present
  - official `official_table_rows.raw.json` hash, table count, and raw row count
  - official row fields: `table_index`, `row_index`, `group_heading`,
    `cell_count`, and `input_images`
- official cell fields: `image_src`, `image_alt`, `visible_text`,
    `source_text`, `source_text_stripped`, `hidden_detail_text`,
    `column_index`, `source_column_header_path`, and
    `source_column_leaf_header`
  - exact official source column header paths and empty header path violations
  - SuperCombo `supercombo_tables.raw.json` hash, table count, and raw row count
- Browser-based visual validation is not part of the committed CLI or normal
  validation boundary in this ExecPlan. Browser/Playwright checks may be used
  only as reviewer evidence unless a later ExecPlan explicitly approves a
  browser-based validator.
- Full raw HTML public-commit status recorded as
  `prohibited_without_explicit_review` unless a later source-boundary review
  explicitly approves it.
- SuperCombo acquisition status recorded as `queued`, `same_run_approved`, or
  `blocked`.

## Progress

- [x] PR #303 value-shape inventory planning was merged before this work.
- [x] `main` was verified at merge commit
  `8e4a44c1961e62e95a0f57d6b06c997c1f292403`.
- [x] JSON Schema redesign was deferred as too early.
- [x] Branch `plan/current-source-acquisition-implementation` was created
  from updated `main`.
- [x] Existing official, SuperCombo, and value-shape planning docs were
  reviewed.
- [x] Current roster was reviewed for all-character source planning.
- [x] This planning ExecPlan was drafted.
- [x] Planning validation completed.
- [x] Review finding added mandatory future acquisition-report guard
  requirements.
- [x] Branch `impl/current-source-official-acquisition` was created from
  updated `main`.
- [x] Official-only acquisition module was implemented without adding
  dependencies. This is now superseded by the Scrapling-mandatory decision and
  must not be treated as final.
- [x] Acquisition-report guard and coverage validation were implemented.
- [x] Current source acquisition report was generated at
  `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`.
- [x] Official acquisition covered 29 of 29 roster characters with zero
  failures.
- [x] Metadata-only/page.html-only acquisition was rejected by review as
  not stage-ready.
- [x] Redesign requires source-specific extracted raw artifacts.
- [x] v2.3 ingestion code was recorded as reference-only.
- [x] Official extracted raw row artifacts implemented for 29 of 29 roster
  characters under ignored `.local/source-acquisition/`.
- [x] SuperCombo raw table artifacts implemented for 29 of 29 roster
  characters under ignored `.local/source-acquisition/`.
- [x] Raw official source documents were kept under repo-local ignored
  `.local/source-acquisition/`.
- [x] `.local/` was added to `.gitignore`.
- [x] Earlier Windows-side and WSL-side global skill installs were removed to
  avoid global environment pollution.
- [x] Scrapling skill was restored under repo-local ignored path
  `.agents/skills/Scrapling-Skill`.
- [x] Repo-local ignored `.venv` was restored with the Scrapling dependency.
- [x] Review direction changed acquisition to mandatory Scrapling usage.
- [x] `scrapling[all]>=0.4.8,<0.5` was added to `pyproject.toml` and resolved
  with `uv.lock`.
- [x] Scrapling import was verified with repo-local `.venv`.
- [x] Prior direct-HTTP acquisition report regenerated with Scrapling.
- [x] Regenerated report validates with 29 of 29 official captures, 29 of 29
  SuperCombo captures, and zero failures.
- [x] Artifact integrity validation was implemented against ignored `.local/`
  source artifacts and the public report hashes/counts.
- [x] Successful SuperCombo report entries now require
  `supercombo_raw_row_count > 0`.
- [x] Acquisition and artifact-validation workspaces are restricted to
  `.local/source-acquisition/`.
- [x] Public report coverage aggregates are recomputed from entries during
  validation.
- [x] External Playwright visual review found 494 official visible-text
  mismatches in the prior raw artifacts because hidden/source-only details were
  mixed into `text_stripped` and visible text spacing did not match browser
  rendering.
- [x] Official raw row artifacts were regenerated as
  `official_table_rows_raw/v2` with separate `visible_text`, `source_text`,
  `source_text_stripped`, and `hidden_detail_text` fields.
- [x] Artifact validation now requires official row-level fields and official
  image fields.
- [x] Review found that positional `cells[]` without column header paths is not
  reviewable enough for key/value mapping.
- [x] Official raw row artifacts were regenerated as
  `official_table_rows_raw/v3` with raw header structure, expected/extracted
  source column header paths, and per-cell `source_column_header_path`.
- [x] Artifact validation now rejects missing or shifted official source column
  header paths.
- [x] Browser-based official validation was removed from the committed CLI and
  normal validation boundary; visual checks remain reviewer evidence only.
- [x] SuperCombo `solve_cloudflare=True` boundary was aligned: approved only for
  SuperCombo acquisition update mode and reviewer-only visual observation, not
  daily-answer runtime, CI, deterministic validators, or numeric authority.
- [x] SuperCombo reviewer-only Scrapling/Patchright visual observation with
  `solve_cloudflare=True` reached 29 of 29 pages and passed against ignored
  local `supercombo_tables.raw.json` artifacts for enrichment/candidate use.
- [x] Latest official value-shape reviewer findings were recorded as a
  downstream handoff and JSON Schema redesign blocker.
- [x] Source update and drift policy was recorded: structural drift and new
  unclassified expressions must hard fail or become explicit human review
  items, not silent skips or partial success.
- [ ] Mandatory review completed.

## Decision Log

- 2026-05-21: Current-fact JSON Schema redesign is deferred until actual
  current source acquisition and reviewed value-shape inventory artifacts
  exist.
- 2026-05-21: The smallest next implementation slice is official all-character
  latest source acquisition plus an explicit SuperCombo queue/same-run/block
  decision.
- 2026-05-21: Full raw HTML and equivalent source documents remain in
  repo-local ignored `.local/` storage by default. Public commit requires
  source-boundary review.
- 2026-05-21: Public output for the next implementation defaults to an
  acquisition report, not raw source rows or normalized data.
- 2026-05-21: Official captures are authority candidates only. SuperCombo
  remains enrichment/cross-reference/candidate evidence only.
- 2026-05-21: Scrapling is mandatory for official source acquisition. Prior
  dependency-free direct HTTP acquisition is not accepted as final, even if it
  returns HTTP 200.
- 2026-05-21: The accepted project dependency range is
  `scrapling[all]>=0.4.8,<0.5`; implementation uses `uv` and Python 3.12.
- 2026-05-21: The lockfile `uv.lock` is included so the Scrapling acquisition
  dependency is reviewable and deterministic.
- 2026-05-21: Scrapling skill license was checked from the installed
  `LICENSE.txt`; it is BSD 3-Clause.
- 2026-05-21: The public report records only acquisition metadata and content
  hashes. Full raw source documents remain repo-local ignored and untracked.
- 2026-05-21: Review rejected the metadata-only/page.html-only result as
  insufficient for Phase 1 raw data inventory. The implementation must extract
  source-specific raw artifacts from official and SuperCombo pages.
- 2026-05-21: Live acquisition completed with official 29/29 and SuperCombo
  29/29 captured. SuperCombo remains enrichment/cross-reference/candidate
  evidence only.
- 2026-05-21: Added a standard-library HTML parser fallback so baseline
  `PYTHONPATH=src python -m unittest discover -s tests` passes without the
  repo-local `.venv`; live source acquisition still requires Scrapling.
- 2026-05-21: Added `validate-artifacts` to bind the public report to ignored
  `.local/` artifact existence, hashes, table counts, and raw row counts.
- 2026-05-21: Removed arbitrary outside-repo acquisition workspace support;
  raw acquisition artifacts must stay under `.local/source-acquisition/`.
- 2026-05-21: Added report aggregate validation so coverage counts and
  raw-row/table totals must match report entries.
- 2026-05-21: Official cell raw artifacts now separate browser-rendered
  `visible_text` from full `source_text` and `hidden_detail_text`. Hidden
  details remain preserved for value-shape inventory, but are not labeled as
  visible display values.
- 2026-05-21: Tightened official row and image validation so
  `validate-artifacts` requires row identity, `group_heading`, `cell_count`,
  `input_images`, and per-cell image fields.
- 2026-05-21: Browser-based official validation is not committed in this slice.
  External Playwright/Chrome checks are reviewer evidence only unless a later
  ExecPlan explicitly approves a browser-based validator.
- 2026-05-21: SuperCombo external visual review was initially blocked by
  Cloudflare in ordinary browser observation. That status was later updated by
  reviewer-only Scrapling/Patchright observation with `solve_cloudflare=True`.
- 2026-05-22: `solve_cloudflare=True` is approved for SuperCombo source
  acquisition update mode in the committed Scrapling `StealthyFetcher` path.
  It remains prohibited for daily-answer runtime, CI, deterministic validators,
  non-acquisition runtime paths, and numeric authority.
- 2026-05-22: Official raw rows must be reviewable as source key/value data,
  not only as positional cells. `official_table_rows_raw/v3` adds raw header
  metadata and per-cell source column header paths using official Japanese
  labels only.
- 2026-05-22: `validate-artifacts` rejects missing, shifted, or unexpected
  official source column header paths. It does not use normalized schema field
  names and does not add parser or current-fact semantics.
- 2026-05-22: JSON Schema redesign remains blocked by latest-source
  value-shape review. Raw artifacts preserve source-native labels and raw
  source text; English canonical field keys and source-label mappings are
  deferred to the later normalized schema layer.
- 2026-05-22: Raw acquisition artifacts are source-fidelity artifacts only.
  `source_family` is reserved for semantic category in the later normalized
  schema, while source identity and evidence role belong in `source_name` and
  `source_role`.
- 2026-05-22: SuperCombo reviewer-only live visual review passed for 29 of 29
  roster pages. Evidence stayed outside the repo under
  `/tmp/sf6-supercombo-scrapling-visual-review/`; screenshots and visual
  observation remain reviewer evidence only and do not create numeric
  authority, parser rules, CI behavior, validator behavior, or daily-answer
  runtime behavior.
- 2026-05-22: Source update and drift policy is conservative. Value updates
  and new notes are expected, but structural drift, changed extraction shapes,
  missing expected content, unexpected columns/headers, changed row/cell
  mapping, and new unclassified value expressions must hard fail or become
  explicit human review items before later schema/parser/classifier work.

## Deviations

- None.

## Risks

- Official pages may redirect, change layout, require JavaScript, or expose
  source/version labels inconsistently.
- SuperCombo page structure and revision metadata may require a separate
  acquisition implementation.
- Scrapling Fetcher may still be insufficient if the official page requires
  JavaScript rendering; switching to DynamicFetcher or StealthyFetcher requires
  explicit review before broadening behavior.
- External browser visual checks are not part of committed validation in this
  slice. If future reviewers want a browser-based validator, it needs a
  separate ExecPlan and source-boundary review.
- SuperCombo reviewer-only visual observation passed with
  `solve_cloudflare=True`, but this remains non-deterministic reviewer
  evidence. Separately, committed SuperCombo acquisition update mode uses
  `solve_cloudflare=True`; neither use may be promoted to CI, normal
  validators, parser/schema authority, daily-answer runtime, or daily-answer
  evidence without a separate approved ExecPlan.
- A report-only public artifact proves coverage and freshness; raw values are
  reviewable locally from ignored `.local/` but are not public repo artifacts.
- Source-boundary review may prohibit committing full raw source documents.
- Existing `data/exports/` remains historical/current local authority until
  later approved replacement; this unit does not update daily-answer authority.
- JSON Schema redesign is blocked until reviewed latest-source value-shape
  inventory artifacts exist for official data and SuperCombo has its own
  separate value-shape inventory.
- Future game updates may introduce move identity or source-structure drift.
  This implementation must not silently absorb that drift; it requires a hard
  failure or explicit human review item, then a focused follow-up ExecPlan.
- Current GitHub Actions CI does not install project dependencies and does not
  run `uv lock --check` or a Scrapling import check. This local validation is
  required before staging, and CI coverage should be restored in a focused
  follow-up unless this ExecPlan is expanded before PR.
- `stash@{0}` contains paused retrieval runtime work and must remain unrelated
  unless explicitly resumed.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan first latest-source acquisition implementation | Drafted implementation plan for official acquisition and SuperCombo queue decision | `docs/execplans/2026-05-21-current-source-acquisition-implementation.md` | `git diff --check` | Pass | None | Mandatory review pending | Report-only artifact may not expose raw values |
| Acquire latest official all-character sources | Revise acquisition to require Scrapling and reject prior direct-HTTP finalization | `src/sf6_knowledge_coach/source_acquisition.py`, `pyproject.toml`, `uv.lock`, `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md` | `PYTHONPATH=src .venv/bin/python -m sf6_knowledge_coach.source_acquisition validate-report docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md` | Pass, 29/29 official captures | None | Mandatory review pending | Source pages may change between runs |
| Extract official raw rows | Extracted `official_table_rows.raw.json`, `metadata.json`, `__NEXT_DATA__.json`, and `page.html` under ignored `.local/` for every roster character | `src/sf6_knowledge_coach/source_acquisition.py`, ignored `.local/` artifacts | `PYTHONPATH=src python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md` | Pass, 29/29 official raw row artifacts | None | Mandatory review pending | Official table shape may drift |
| Preserve official raw-field fidelity | Separated official `visible_text`, `source_text`, `source_text_stripped`, and `hidden_detail_text`; validate row identity, `group_heading`, `cell_count`, input image `src`/`alt`, and per-cell source column header paths through deterministic local artifact validation | `src/sf6_knowledge_coach/source_acquisition.py`, `tests/test_source_acquisition.py`, `docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md`, ignored `.local/` artifacts | `PYTHONPATH=src python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md` | Pass, 29/29 official captures | None | Mandatory review pending | Browser visual checks remain external reviewer evidence only |
| Extract SuperCombo raw tables | Extracted `supercombo_tables.raw.json`, `metadata.json`, and `page.html` under ignored `.local/` for every roster character | `src/sf6_knowledge_coach/source_acquisition.py`, ignored `.local/` artifacts | `PYTHONPATH=src python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md` | Pass, 29/29 SuperCombo table artifacts | None | Mandatory review pending | SuperCombo Cloudflare behavior may change |
| Align SuperCombo Cloudflare boundary | Approved `solve_cloudflare=True` only for SuperCombo acquisition update mode and reviewer-only visual observation; prohibited daily-answer, CI, deterministic validator, answer, retrieval, Discord, and numeric-authority use | `docs/execplans/2026-05-21-current-source-acquisition-implementation.md`, `src/sf6_knowledge_coach/source_acquisition.py` | Review | Pass | None | Mandatory review pending | Future code must not reuse this outside acquisition |
| Record SuperCombo visual evidence | Reviewer-only Scrapling/Patchright observation with `solve_cloudflare=True` reached all 29 SuperCombo pages; live-rendered pages matched ignored `supercombo_tables.raw.json` for table count, row count, heading chain, and compatible cell text; evidence stayed under `/tmp/sf6-supercombo-scrapling-visual-review/` | `docs/execplans/2026-05-21-current-source-acquisition-implementation.md`, outside-repo `/tmp` evidence | `PYTHONPATH=src python -m sf6_knowledge_coach.source_acquisition validate-artifacts docs/acquisition-reports/20260521T025403Z-current-source-acquisition.md` | Pass, 29/29 reviewer-observed | None | Mandatory review pending | Reviewer visual evidence is not deterministic authority |
| Preserve authority boundaries | Official as authority candidate only; SuperCombo as enrichment/candidate only | Same | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | Mandatory review pending | Later parser/schema gates still required |
| Implement acquisition-report guard | Guard blocks local paths, secrets, private refs, logs, full raw HTML, source dumps, missing coverage, mismatched coverage aggregates, missing artifact hashes, and zero-row successful SuperCombo entries | `src/sf6_knowledge_coach/source_acquisition.py`, `tests/test_source_acquisition.py` | `PYTHONPATH=src python -m unittest discover -s tests` | Pass | None | Mandatory review pending | Guard is conservative but not a legal source-boundary review |
| Avoid premature schema redesign | JSON Schema redesign explicitly deferred; no parser/classifier/export added | Same | Review | Pass | None | Mandatory review pending | Requires discipline in later prompts |
| Hand off value-shape blockers | Recorded latest official special value shapes and deferred English canonical keys, official/SuperCombo label mapping, and SuperCombo value-shape inventory to later plans | `docs/execplans/2026-05-21-current-source-acquisition-implementation.md` | `git diff --check` | Pass | None | Mandatory review pending | Later schema work must not skip this handoff |
| Record source drift policy | Recorded that changed/missing/extra/structurally drifted data and new unclassified value expressions must hard fail or become explicit human review items; no silent skip, coercion, or partial-success hiding | `docs/execplans/2026-05-21-current-source-acquisition-implementation.md` | `git diff --check` | Pass | None | Mandatory review pending | Later updates need focused review before schema/parser changes |
| Keep implementation scope | No retrieval, answer behavior, private vault, Discord, VLM, API fallback, vector search, persistent DB, or `sf6 ask` | Same | `git status --short --branch` | Pass | None | Mandatory review pending | Follow-up implementation must stay scoped |
