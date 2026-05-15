# External Visual Atlas Acquisition: Move-Analysis Calibration

## Report Metadata

| Field | Value |
|---|---|
| Issue | #178 |
| Parent issues | #155 / #158 |
| Related raw-video calibration | #170 / PR #173 |
| Related command-prompt normalization | #175 / PR #184 |
| Related frame/input alignment | #176 / PR #185 |
| Related damage/scaling attribution | #177 / PR #189 |
| Related downstream matching | #179 |
| Date | 2026-05-15 |
| Scope | JP-small-scope |
| Terminal state | visual-atlas-acquisition PATH_DEFINED; first JP external binary acquisition held for source permission/terms review |

This report defines the gated maintainer-local acquisition path for external
visual move references. It does not perform JP move visual-reference matching,
does not create a move-recognition runtime, does not fetch a full atlas, and
does not add binary assets to the repository.

## Loaded Repo Context

This report follows the #180 pre-analysis repo context loading requirement.

| Artifact | Artifact type | Why loaded | Can guide | Cannot authorize |
|---|---|---|---|---|
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-command-prompt-normalization-20260514.md` | calibration report | Provides JP prompt rows and candidate move/system-action ids from #175. | JP visual-reference scope selection. | Accepted move order, exact execution, or current facts. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-frame-input-alignment-20260515.md` | calibration report | Provides ambiguous action windows from #176. | Which segments need visual reference support. | Exact frame data or route validity. |
| `docs/testing/video-analysis-calibration/raw-video-training-mode-01-damage-scaling-attribution-20260515.md` | calibration report | Provides #177 partial/unknown attribution and remaining action-identity gaps. | Which visual references would help #179. | Damage/scaling authority or hit-by-hit current facts. |
| `knowledge/review/unresolved/raw-video-training-mode-01.review.md` | review note | Provides current resolved/open follow-up routing. | #178/#179/#183 dependency boundary. | Accepted gameplay knowledge. |
| `ingest/frame_data/config/registry/jp.moves.yaml` | move registry | Provides JP move ids and input-token families. | Candidate move ids for the tiny acquisition scope. | Proof that a visual reference is current or that a video action is the move. |
| `docs/architecture/external-frame-atlas-policy.md` | policy | Defines external visual atlas source roles, cache/storage boundaries, and authority limits. | Acquisition safety gates and metadata-only representation. | Permission to fetch, cache, redistribute, or treat visuals as authority. |
| `workflows/media-scratch-cache-policy.md` | workflow/policy | Defines repo-external scratch and forbidden media/cache paths. | Scratch/cache location and cleanup discipline. | Permission to commit binaries or local cache. |
| `workflows/ingest-video.md` | workflow | Provides video-calibration sequencing and #180 context-loading gate. | Where to add a narrow acquisition step for future video calibration. | Current facts or public runtime behavior. |
| `data/external-frame-atlas/evaluation/README.md` | source evaluation docs | Explains existing metadata-only evaluation matrix. | Why existing atlas records do not authorize acquisition. | Direct asset retrieval or binary storage. |
| `data/external-frame-atlas/evaluation/source-evaluation-matrix.json` | metadata-only source evaluation | Provides source status for SF6Frames and Ultimate Frame Data. | Source selection and HOLD conditions. | Fetch permission, stable asset URLs, current facts, or redistribution rights. |
| `contracts/external-frame-atlas-source.schema.json` | manifest schema | Defines metadata-only external atlas source manifest shape. | Future manifest field selection when acquisition is approved. | Binary storage approval. |
| `tests/fixtures/external-frame-atlas/sf6frames-hitbox-overlay-candidate.json` | metadata-only fixture | Existing SF6Frames candidate fixture. | Example of metadata-only visual reference shape. | Direct SF6Frames asset availability or current authority. |
| `tests/fixtures/external-frame-atlas/ultimate-frame-data-hitbox-image-candidate.json` | metadata-only fixture | Existing UFD candidate fixture. | Example of metadata-only UFD shape. | Permission or move mapping for #178. |
| `ingest/frame_data/README.md` | ingestion docs | Describes existing fetch discipline and raw snapshot boundary. | How to align acquisition style with frame-data ingest. | Permission to write external atlas raw snapshots into repo. |
| `ingest/frame_data/pyproject.toml` | package config | Shows optional `fetch` extra with `scrapling[fetchers]`. | Dependency boundary and optional install expectations. | CI live external fetch or new dependency requirement. |
| `ingest/frame_data/src/sf6_ingest/fetch/scrapling_client.py` | fetch helper | Shows existing Scrapling wrapper, fetch profile, metadata, and challenge detection shape. | Future acquisition helper style. | Direct reuse of `data/raw` snapshot behavior for external binary assets. |
| `ingest/frame_data/config/fetch_profiles.yaml` | fetch config | Shows existing Fetcher/StealthyFetcher profiles, timeouts, retry, and challenge markers. | Future no-auth/no-cookie fetch profile design. | Bypassing source access boundaries or CI live fetch. |

External visual references remain visual review support only. They cannot
authorize current facts, override `official_raw`, or become public
`sf6-agent` behavior. Hermes/session memory is non-canonical.

## Existing Scrapling Setup Review

The existing `ingest/frame_data` package already has a Scrapling-based fetch
style:

- `ingest/frame_data/pyproject.toml` declares optional `fetch` dependencies:
  `scrapling[fetchers]>=0.4.2`.
- `ingest/frame_data/src/sf6_ingest/fetch/scrapling_client.py` wraps
  Scrapling `Fetcher` and `StealthyFetcher` behind a `FetchProfile`, records
  final URL, status, encoding, title, challenge detection, raw byte count, and
  SHA-256.
- `ingest/frame_data/config/fetch_profiles.yaml` keeps fetcher, timeout, retry,
  wait, and challenge-marker behavior in config rather than ad hoc scripts.
- Existing frame-data fetch writes raw response bytes and metadata into
  `data/raw`, then parses deterministically from those raw bytes.

For external visual atlas acquisition, this style can be reused only with an
important storage change:

- keep the fetch profile / challenge detection / metadata-first discipline;
- do not write external visual atlas raw bytes or raw HTML into `data/raw`;
- write external binary assets only to maintainer-local repo-external scratch or
  cache when an explicit source permission/terms gate allows it;
- commit metadata/report only.

No new dependency is added in this PR. The current shell does not have the
optional fetch runtime installed (`scrapling` and `pydantic` imports were not
available), so this PR does not run a live Scrapling fetch. CI is unaffected and
must not perform live external visual-asset fetches.

## Source Selection

| Candidate source | Selected? | Reason |
|---|---|---|
| SF6Frames | yes, as first path candidate only | Existing evaluation records hitbox-overlay availability, frame-number visibility, JP candidate fixture, and alignment with future Scrapling acquisition. It is still held for permission/terms before binary acquisition. |
| Ultimate Frame Data | no, deferred | Existing evaluation is less complete for permissions/robots and move mapping. It remains a later candidate if SF6Frames is unavailable or insufficient. |
| Maintainer-local captured references | no, deferred | No maintainer-local captured visual reference was provided for this issue. |
| SuperCombo text/reference context | no | Existing matrix treats it as non-visual reference context, not a visual atlas source by default. |

Selected source: SF6Frames, metadata-only path candidate.

Access boundary:

- no authentication;
- no cookies;
- no browser cache;
- no rate-limit bypass;
- no raw HTML dump;
- no direct binary URL storage;
- no legal conclusion beyond maintainer-local source-review basis.

Existing source evaluation status for SF6Frames is `hold_terms_or_permission`.
Therefore this PR holds binary acquisition before fetching or caching a visual
asset.

## JP Visual Reference Acquisition Attempt

Tiny scope selected from #175/#176/#177:

- Stribog family: `jp_034_236mp_stribog`, `jp_035_236hp_stribog`;
- OD Triglav family: `jp_030_22pp_triglav_od_weak`,
  `jp_031_22pp_triglav_od_medium`, `jp_032_22pp_triglav_od_heavy`;
- SA3/CA family: `jp_055_sa3_236236k`, `jp_056_ca_236236k`.

| attempt_id | source | character | move/action candidate | candidate move id(s) | source page or source descriptor | acquisition method | asset kind expected | acquired locally? | file type observed | committed binary? | cleanup status | result | reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `jp-atlas-sf6frames-001` | SF6Frames | JP | Stribog visual reference candidate | `jp_034_236mp_stribog`; `jp_035_236hp_stribog` | `source_id=sf6frames` in `data/external-frame-atlas/evaluation/source-evaluation-matrix.json` | pre-fetch gate using existing source evaluation and Scrapling setup review | hitbox-overlay animation or frame-numbered visual reference if permission later allows | no | not observed | no | no scratch created | hold | SF6Frames is held for permission/terms review; direct asset URL stability was not tested; no live fetch runtime was installed; no binary acquisition was safe in this PR. |
| `jp-atlas-sf6frames-002` | SF6Frames | JP | OD Triglav visual reference candidate | `jp_030_22pp_triglav_od_weak`; `jp_031_22pp_triglav_od_medium`; `jp_032_22pp_triglav_od_heavy` | `source_id=sf6frames` in source evaluation matrix | pre-fetch gate using existing source evaluation and Scrapling setup review | hitbox-overlay animation or frame-numbered visual reference if permission later allows | no | not observed | no | no scratch created | hold | Same hold: source evaluation recommends `hold_terms_or_permission` and #178 must not bypass that to acquire binaries. |
| `jp-atlas-sf6frames-003` | SF6Frames | JP | SA3/CA visual reference candidate | `jp_055_sa3_236236k`; `jp_056_ca_236236k` | `source_id=sf6frames` in source evaluation matrix | pre-fetch gate using existing source evaluation and Scrapling setup review | hitbox-overlay animation or frame-numbered visual reference if source coverage exists | no | not observed | no | no scratch created | hold | Same hold plus possible source coverage uncertainty for cinematic/super references. |

No GIF, image, WebP, frame, screenshot, contact sheet, raw HTML, raw JSON dump,
or direct binary URL was committed.

## Metadata-Only Visual Atlas Record

No new metadata-only manifest was created beyond this report because no binary
or source page acquisition succeeded. Existing metadata-only fixtures already
cover the general source shape:

- `tests/fixtures/external-frame-atlas/sf6frames-hitbox-overlay-candidate.json`
- `tests/fixtures/external-frame-atlas/ultimate-frame-data-hitbox-image-candidate.json`

If a later issue resolves the source permission/terms gate and performs a tiny
repo-external acquisition, #179 can consume metadata fields like:

| Field | Planned value / rule |
|---|---|
| `character_slug` | `jp` |
| `candidate_move_id` | one of the selected Stribog, OD Triglav, or SA3/CA candidates |
| `move_family` | Stribog / OD Triglav / SA3-CA |
| `source_name` | SF6Frames, unless a later source is selected |
| `source_page_descriptor` | source page or character/move descriptor only; no private temp path or direct binary URL unless policy permits |
| `asset_kind` | hitbox overlay / frame-numbered visual reference / unknown |
| `file_type_observed` | `gif`, `webp`, `png_sequence`, `hitbox_image`, or `unknown` after permitted acquisition |
| `acquired_for_review` | true only after permitted repo-external acquisition |
| `local_binary_committed` | false |
| `raw_html_committed` | false |
| `authority_boundary` | visual reference only; not current-fact authority |
| `cleanup_status` | deleted or repo-external cache retained with reason |
| `next_use` | #179 review-only visual matching |

Current hold reason: existing SF6Frames/UFD evaluations do not grant permission
for binary acquisition or redistribution, and #178 does not add a live fetch
runtime or source-specific selector.

## How This Supports #179

#179 can use this report to decide whether it has an allowed visual-reference
input.

What #179 can do:

- load the same JP command-prompt rows and frame/action windows;
- use the selected JP move families as the first visual matching scope;
- use this acquisition path to determine whether a permitted repo-external
  visual reference exists;
- mark #179 HOLD if no permitted visual reference has been acquired.

What #179 cannot do from this PR:

- compare raw-video segments against SF6Frames binaries, because none were
  acquired;
- infer official move identity from visual similarity alone;
- treat SF6Frames/UFD visuals as current-fact authority;
- commit GIFs, images, frames, screenshots, contact sheets, raw HTML, raw tool
  output, or private paths.

If source permission/terms are resolved later, the first useful #179 visual
checks are likely:

- Stribog family vs rows 8/11;
- OD Triglav family vs row 10 and mid-route ambiguous labels;
- SA3/CA family vs row 12 cinematic window.

## Reusable Visual Atlas Acquisition Method

Future Codex/Hermes runs should repeat this method without chat history:

1. Load repo context:
   - same-sample calibration reports;
   - source review note;
   - JP move registry;
   - external-frame-atlas policy;
   - source evaluation matrix;
   - existing metadata-only fixtures;
   - `ingest/frame_data` Scrapling setup.
2. Select a tiny character/move scope from unresolved video-analysis gaps.
3. Inspect the source evaluation status before any network or binary work.
4. If the source is held for permission/terms/robots/rate-limit review, stop
   before binary acquisition and record a HOLD.
5. If acquisition is permitted by a later explicit issue, use the existing
   `ingest/frame_data` fetch discipline:
   - config-driven profile;
   - no-auth/no-cookie boundary;
   - challenge detection;
   - metadata-first recording;
   - repo-external scratch/cache only.
6. Record metadata only in repo:
   - source;
   - character;
   - move candidate;
   - expected asset kind;
   - file type observed if permitted;
   - cleanup/cache status;
   - authority boundary.
7. Delete binaries after review unless a later explicit repo-external cache
   retention rule applies.
8. Route visual comparison to #179.
9. Preserve the boundary that visual references are review support only.

### Next-Agent One-Shot Checklist

- Load prior video-calibration reports and `raw-video-training-mode-01.review.md`.
- Load `docs/architecture/external-frame-atlas-policy.md`.
- Load `data/external-frame-atlas/evaluation/source-evaluation-matrix.json`.
- Load existing metadata-only fixture examples.
- Load `ingest/frame_data` Scrapling setup and fetch profiles.
- Pick one character and one to three move families.
- Check source evaluation status before any fetch.
- Use repo-external scratch/cache only if acquisition is permitted.
- Commit only metadata/report.
- Mark success/partial/hold with a concrete reason.
- Route matching to #179.
- Never treat external visuals as current-fact authority.

## Improvement Applied In This PR

This PR adds:

- this #178 operational report; and
- a narrow `External Visual Atlas Acquisition For Calibration` subsection in
  `workflows/ingest-video.md`.

The existing architecture policy already covers broad source/storage rules.
The new workflow subsection records the source-unit operational sequence so
future video-calibration agents know where this step fits: after command/action
gaps are identified, before #179 visual matching, and without live CI fetch or
binary commits.

No validator was added. Existing external-frame-atlas validators already cover
metadata-only fixtures and source evaluation, and this PR does not add a new
schema or manifest.

## Follow-Up Routing

| Follow-up | Status after #178 | Reason |
|---|---|---|
| #179 JP move/action visual-reference matching | open; binary matching not yet ready | #178 defines the path and selected JP scope, but actual SF6Frames binary acquisition is held until permission/terms review is resolved or an approved local reference is provided. |
| #183 SF6 system-mechanics math reasoning fixtures | still relevant | Visual references do not solve damage/scaling reasoning or authority-boundary fixtures. |

No new follow-up issue is needed.

## Terminal State

- visual-atlas-acquisition: PATH_DEFINED
- small JP scope selected: yes
- acquisition attempt result: held before binary fetch
- hold reason: SF6Frames/UFD source evaluations do not grant permission/terms
  clearance for binary acquisition or redistribution
- metadata/report only: yes
- binary committed: no
- raw HTML committed: no
- current-fact authority: no
- #179 ready? partially: ready to use the path and scope, not ready for actual
  binary visual matching until a permitted external reference is acquired

## Cleanup And Validation

| Check | Result |
|---|---|
| External binaries acquired? | no |
| Committed binaries? | no |
| Raw HTML committed? | no |
| Scratch cleanup | no scratch created |
| Private paths committed? | no |
| Validators run | see PR body |
