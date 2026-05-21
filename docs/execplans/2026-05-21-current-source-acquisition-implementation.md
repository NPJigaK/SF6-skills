# Current Source Acquisition Implementation Planning

Status: Draft; planning-only ExecPlan.

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
  all-character raw source data from current official roster URLs.
- Plan how latest SuperCombo all-character raw source data is either acquired
  in the same implementation or explicitly queued for a separate acquisition
  implementation.
- Require a Git-outside transient acquisition workspace for raw HTML, cache,
  debug output, browser traces, screenshots, and candidate extracted data.
- Define the public artifact boundary for the next implementation.
- Require exact preservation of raw source values in the acquisition workspace.
- Require source URL, final URL, captured-at UTC timestamp, HTTP status,
  content type, and source/version/revision labels when available.
- Require an acquisition report sufficient to prove coverage and freshness.
- Preserve authority boundaries:
  - official source data is authority candidate only until later deterministic
    parser, schema, validator, and review gates pass.
  - SuperCombo source data is enrichment, cross-reference, or candidate
    evidence only.
- Define a minimal acquisition-report shape. This is not a JSON Schema
  redesign.

Excluded:

- No implementation in this planning step.
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
  Git-outside acquisition workspace.
- The plan states that the public repo receives only a reviewed acquisition
  report by default, not full raw HTML or source row data.
- The plan defines the minimum acquisition-report fields needed to prove
  coverage and freshness.
- The plan states that official data is not `current_fact_authority` until
  later deterministic parser/schema/validator/review gates pass.
- The plan states that SuperCombo is not daily-answer numeric authority.
- The plan does not create implementation files, schemas, validators, data
  artifacts, runtime behavior, or retrieval behavior.
- Planning validation passes.

## Files / Interfaces

Changed by this planning step:

- `docs/execplans/2026-05-21-current-source-acquisition-implementation.md`

Inputs used for planning:

- `docs/PLAN.md`
- `docs/execplans/2026-05-20-phase1-roadmap.md`
- `docs/execplans/2026-05-21-current-fact-acquisition-inventory.md`
- `docs/execplans/2026-05-21-official-raw-snapshot-acquisition.md`
- `docs/execplans/2026-05-21-supercombo-raw-snapshot-acquisition.md`
- `docs/execplans/2026-05-21-value-shape-inventory.md`
- `data/roster/current-character-roster.json`
- existing `data/exports/` for historical comparison only

Future implementation files are not created here. A later implementation may
introduce a small acquisition tool and tests only after this plan is reviewed.
The preferred future implementation remains dependency-free unless direct HTTP
capture proves insufficient and a separate decision approves an acquisition
dependency.

## Next Implementation Slice

The smallest next implementation slice should be:

1. Acquire latest official source documents for every roster character.
2. Store raw capture/cache/debug outputs outside the Git repo.
3. Produce a reviewed public acquisition report.
4. Record whether SuperCombo acquisition is:
   - accepted into the same implementation after reviewer approval, or
   - queued as the next acquisition implementation.

Default decision: acquire official sources first and queue SuperCombo unless
the reviewer explicitly expands the next implementation scope before coding.

Rationale:

- Official sources are the only future `current_fact_authority` candidate.
- SuperCombo remains enrichment/cross-reference/candidate evidence and can be
  acquired separately without blocking official source freshness review.
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
- `capture_method`
- `capture_success`
- `failure_reason` when applicable
- `content_hash` for captured Git-outside raw content
- `artifact_boundary`: `git_outside_raw_capture`

If any roster character lacks `sources.official`, returns a non-success HTTP
status, redirects to an unexpected page, or lacks expected source content, the
implementation must record a coverage failure or review item. It must not
silently drop the character.

JP remains one roster character and the initial active character package. It
must not become a hardcoded acquisition special case.

## SuperCombo Handling

SuperCombo acquisition is not required in the smallest next implementation
unless the reviewer explicitly expands scope.

The next implementation must still record a SuperCombo decision:

- `queued`: SuperCombo acquisition is deferred to a later implementation using
  the approved SuperCombo acquisition plan.
- `same_run_approved`: reviewer expanded the implementation before coding and
  the same source-boundary and Git-outside rules are applied.
- `blocked`: source boundary, source availability, or capture approach needs
  review before acquisition.

SuperCombo policy:

- SuperCombo is enrichment, cross-reference, or candidate evidence only.
- SuperCombo does not override official data.
- SuperCombo does not become daily-answer numeric authority.
- Conflicts with official source data become review items.

## Git-Outside Acquisition Workspace

Future acquisition must write raw source captures and intermediate files
outside the public repo.

Allowed Git-outside contents:

- Raw HTML or equivalent source documents.
- HTTP response headers with secrets removed.
- Fetch cache.
- Debug logs.
- Browser traces or screenshots if needed.
- Candidate extracted tables or rows before review.
- Coverage diagnostics.

Rules:

- Do not commit Git-outside paths.
- Do not commit cookies, credentials, auth headers, or browser profile data.
- Do not commit local absolute paths.
- Do not store private user data.
- Do not use Git-outside transient files as daily-answer authority.
- Do not commit full raw HTML unless source-boundary review explicitly
  approves public redistribution.

Suggested local workspace pattern for a later implementation:

```text
<git-outside-cache-root>/sf6-knowledge-coach/current-source-acquisition/<run_id>/
```

The exact path remains configurable and must not be written into committed
artifacts.

## Public Artifact Boundary

The default public artifact for the next implementation is a reviewed
acquisition report, not raw source data.

Preferred future report path:

```text
docs/acquisition-reports/<run_id>-current-source-acquisition.md
```

This path is planned for the future implementation. It is not created by this
planning-only step.

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
- Content hashes for Git-outside raw captures.
- Source-boundary review status.
- Coverage failures and review items.
- Statement that raw source values are preserved Git-outside.
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
      artifact_boundary: git_outside_raw_capture
  review_items:
    - string
```

If the future implementation cannot prove coverage and freshness with this
shape, it must update this ExecPlan's Decision Log or create a follow-up
ExecPlan before broadening artifacts.

## Source Boundary Review

Before any full raw HTML or equivalent source document is committed, a later
implementation must record explicit review of:

- Source terms.
- License.
- Robots policy.
- Attribution requirements.
- Source-specific redistribution limits.

Privacy checks and hashes are required but not sufficient to approve public raw
HTML. The default is to keep full raw source documents Git-outside.

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

## Implementation Guardrails For The Next Step

The future implementation must:

- Stay in update/acquisition mode, not daily-answer mode.
- Use current roster URLs from `data/roster/current-character-roster.json`.
- Keep public repo writes limited to the approved report and ExecPlan updates.
- Keep raw source documents Git-outside.
- Avoid dependencies unless direct HTTP capture fails and reviewer approves a
  focused dependency decision.
- Stop and record a blocker if source content requires browser execution,
  login, cookies, or broad scraping behavior not covered by this plan.
- Preserve the paused retrieval runtime stash outside this work.

The future implementation must not:

- Modify answer behavior.
- Modify retrieval behavior.
- Promote data to authority.
- Create normalized exports.
- Create persistent databases.
- Add API fallback or web daily-answer behavior.
- Apply unrelated paused runtime changes.

## Validation Commands

Planning validation:

```bash
git diff --check
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git status --short --branch
```

Future implementation validation should include at minimum:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python tests/validation/validate_clean_slate.py
git diff --check
git diff --cached --check
git status --short --branch
```

If future implementation adds an acquisition report, it must also run a
focused acquisition-report guard before review. This guard is planned here but
not implemented by this planning-only ExecPlan.

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
  capture or an explicit failure/review item.
- Expected roster count and observed report entry count.
- Source-boundary status recorded in the report.
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
- [ ] Mandatory review completed.

## Decision Log

- 2026-05-21: Current-fact JSON Schema redesign is deferred until actual
  current source acquisition and reviewed value-shape inventory artifacts
  exist.
- 2026-05-21: The smallest next implementation slice is official all-character
  latest source acquisition plus an explicit SuperCombo queue/same-run/block
  decision.
- 2026-05-21: Full raw HTML and equivalent source documents remain Git-outside
  by default. Public commit requires source-boundary review.
- 2026-05-21: Public output for the next implementation defaults to an
  acquisition report, not raw source rows or normalized data.
- 2026-05-21: Official captures are authority candidates only. SuperCombo
  remains enrichment/cross-reference/candidate evidence only.

## Deviations

- None.

## Risks

- Official pages may redirect, change layout, require JavaScript, or expose
  source/version labels inconsistently.
- SuperCombo page structure and revision metadata may require a separate
  acquisition implementation.
- Direct HTTP capture may not be sufficient; a browser or scraping dependency
  may need a later explicit approval.
- A report-only public artifact proves coverage and freshness but does not make
  raw values reviewable from the repo by itself.
- Source-boundary review may prohibit committing full raw source documents.
- Existing `data/exports/` remains historical/current local authority until
  later approved replacement; this unit does not update daily-answer authority.
- `stash@{0}` contains paused retrieval runtime work and must remain unrelated
  unless explicitly resumed.

## Completion Review Table

| PLAN item | Implementation content | Changed files | Validation command | Result | Deviation | Incomplete | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Plan first latest-source acquisition implementation | Drafted implementation plan for official acquisition and SuperCombo queue decision | `docs/execplans/2026-05-21-current-source-acquisition-implementation.md` | `git diff --check` | Pass | None | Mandatory review pending | Report-only artifact may not expose raw values |
| Preserve authority boundaries | Official as authority candidate only; SuperCombo as enrichment/candidate only | Same | `PYTHONPATH=src python tests/validation/validate_clean_slate.py` | Pass | None | Mandatory review pending | Later parser/schema gates still required |
| Avoid premature schema redesign | JSON Schema redesign explicitly deferred | Same | Review | Pass | None | Mandatory review pending | Requires discipline in later prompts |
| Keep planning-only scope | No runtime/schema/data implementation | Same | `git status --short --branch` | Pass | None | Mandatory review pending | Future implementation must stay scoped |
