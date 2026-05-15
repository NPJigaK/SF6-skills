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
| Terminal state | visual-atlas-acquisition USABILITY_SMOKE_HOLD |

This report defines the gated maintainer-local acquisition path for external
visual move references. It does not perform JP move visual-reference matching,
does not create a move-recognition runtime, does not fetch a full atlas, and
does not add binary assets to the repository.

After maintainer approval for a tiny SF6Frames repo-local smoke, this report
uses the existing Scrapling-aligned fetch path to inspect one JP visual
reference candidate. The fetched file was not a usable move visual; it was an
error placeholder WebP. That makes the acquisition path concrete, but leaves
#179 blocked for actual visual matching until a usable visual reference is
available.

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

No new dependency is added in this PR. A maintainer-local, repo-external
temporary Python environment installed the optional fetch runtime for this
smoke only. CI is unaffected and must not perform live external visual-asset
fetches.

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

Existing source evaluation status for SF6Frames is `hold_terms_or_permission`
for broad binary acquisition or redistribution. The maintainer approved a
single repo-local usability smoke for this PR. That approval does not permit
committing binaries, raw HTML, direct binary URLs, cache paths, or public
runtime behavior.

## JP Visual Reference Acquisition Attempt

Tiny scope selected from #175/#176/#177:

- Stribog family: `jp_034_236mp_stribog`, `jp_035_236hp_stribog`;
- OD Triglav family: `jp_030_22pp_triglav_od_weak`,
  `jp_031_22pp_triglav_od_medium`, `jp_032_22pp_triglav_od_heavy`;
- SA3/CA family: `jp_055_sa3_236236k`, `jp_056_ca_236236k`.

| attempt_id | source | character | move/action candidate | candidate move id(s) | source page or source descriptor | acquisition method | asset kind expected | acquired locally? | file type observed | committed binary? | cleanup status | result | reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `jp-atlas-sf6frames-001` | SF6Frames | JP | M Stribog visual reference usability smoke | `jp_034_236mp_stribog` | `sf6frames:jp_specials:M Stribog:data-animation-src` | Scrapling `fetch_with_profile` using static `Fetcher`; no auth/cookies; repo-external temp only | WebP hitbox/hurtbox animation with frame numbers | yes | WebP container, but image content was an internal-server-error placeholder, not a move visual | no | temp binary and extracted frame deleted | hold | Maintainer-approved smoke proved the static Scrapling path can resolve a file, but the resolved file is not usable for visual matching. |
| `jp-atlas-sf6frames-002` | SF6Frames | JP | OD Triglav visual reference candidate | `jp_030_22pp_triglav_od_weak`; `jp_031_22pp_triglav_od_medium`; `jp_032_22pp_triglav_od_heavy` | `source_id=sf6frames` in source evaluation matrix | pre-fetch gate using existing source evaluation and Scrapling setup review | hitbox-overlay animation or frame-numbered visual reference if permission later allows | no | not observed | no | no scratch created | hold | Same hold: source evaluation recommends `hold_terms_or_permission` and #178 must not bypass that to acquire binaries. |
| `jp-atlas-sf6frames-003` | SF6Frames | JP | SA3/CA visual reference candidate | `jp_055_sa3_236236k`; `jp_056_ca_236236k` | `source_id=sf6frames` in source evaluation matrix | pre-fetch gate using existing source evaluation and Scrapling setup review | hitbox-overlay animation or frame-numbered visual reference if source coverage exists | no | not observed | no | no scratch created | hold | Same hold plus possible source coverage uncertainty for cinematic/super references. |

No GIF, image, WebP, frame, screenshot, contact sheet, raw HTML, raw JSON dump,
or direct binary URL was committed.

## Visual Reference Usability Smoke

| Field | Result |
|---|---|
| visual_reference_source | SF6Frames, maintainer-approved repo-local usability smoke |
| source provenance boundary | External visual reference candidate; approval covers this repo-local smoke only. It does not authorize redistribution, committed binary storage, public runtime behavior, or current-fact authority. |
| character | JP |
| move/action candidate family | Stribog family |
| candidate move id | `jp_034_236mp_stribog` |
| source descriptor | `sf6frames:jp_specials:M Stribog:data-animation-src` |
| acquisition tool | Scrapling via `ingest/frame_data`-style `fetch_with_profile` static `Fetcher` |
| no-auth/no-cookie boundary | yes |
| file type observed | WebP container |
| downloaded bytes | 3156 |
| resolution | 350 x 280 |
| duration/frame count | no duration or `nb_frames` reported by `ffprobe`; `ffmpeg` extracted one frame |
| transparency / overlay / hitbox overlay status | not usable; the observed frame was an internal-server-error placeholder, not a hitbox/hurtbox overlay |
| frame numbers visible? | no |
| clean animation visible? | no |
| can be sampled frame-by-frame? | no; only a single placeholder frame was available |
| can be cropped or normalized? | technically yes as an image, but not useful because the content is not a move visual |
| can be compared to raw-video frame windows later? | no |
| observed preprocessing needs | Source-specific asset resolution or browser/session-compatible acquisition is required before normal image preprocessing matters. Resizing, cropping, alpha/background handling, frame extraction, frame-index normalization, playback-speed normalization, and overlay separation cannot make this placeholder usable. |
| usability result | `not_usable` |
| reason | Scrapling static fetch reached a WebP response, but the visual content is an error placeholder rather than the expected SF6Frames move animation. |
| cleanup status | repo-external temp binary and extracted frame deleted |
| binary committed? | no |
| authority boundary | Visual reference smoke only; not current-fact authority, not exact move identity proof, not an `official_raw` override |

The page fetch itself succeeded with Scrapling and exposed the `M Stribog`
`data-animation-src` descriptor. The failure is the practical visual-reference
usability of the resolved asset through the current static fetch path.

## Why #179 Is Still Blocked

The smoke verifies that "SF6Frames asset referenced by the page" is not the same
as "usable visual reference for matching." The current Scrapling static fetch
path produced a valid WebP container, but not a move visual. #179 must not
attempt raw-video matching from this placeholder. It needs either:

- a corrected Scrapling/source-specific acquisition path that resolves the
  actual frame-numbered move visual; or
- a maintainer-approved repo-external local visual reference sample with a
  usable or needs-preprocessing result.

## Metadata-Only Visual Atlas Record

No new JSON manifest was created because the inspected SF6Frames WebP was
`not_usable`. This report records the metadata-only smoke result instead.
Existing metadata-only fixtures still cover the general source shape:

- `tests/fixtures/external-frame-atlas/sf6frames-hitbox-overlay-candidate.json`
- `tests/fixtures/external-frame-atlas/ultimate-frame-data-hitbox-image-candidate.json`

The inspected sample would be represented with these metadata-only fields:

| Field | Planned value / rule |
|---|---|
| `character_slug` | `jp` |
| `candidate_move_id_or_family` | `jp_034_236mp_stribog` |
| `move_family` | Stribog |
| `source_kind` | external visual reference candidate |
| `source_name` | SF6Frames |
| `source_page_descriptor` | `sf6frames:jp_specials:M Stribog:data-animation-src` |
| `visual_reference_kind` | expected hitbox/hurtbox animation |
| `file_type_observed` | WebP container |
| `usability_result` | `not_usable` |
| `preprocessing_required` | source-specific asset resolution; placeholder cannot be fixed by crop/resize/frame extraction |
| `acquired_for_review` | true |
| `local_binary_committed` | false |
| `raw_html_committed` | false |
| `authority_boundary` | visual reference only; not current-fact authority |
| `cleanup_status` | temp binary and extracted frame deleted |
| `next_use` | #179 review-only visual matching |

Current hold reason: the inspected sample is an error placeholder, so #179 needs
a corrected permitted acquisition path or an approved local usable sample before
matching.

## How This Supports #179

#179 can use this report to decide whether it has an allowed visual-reference
input, but this report does not itself provide one.

What #179 can do:

- load the same JP command-prompt rows and frame/action windows;
- use the selected JP move families as the first visual matching scope;
- use this acquisition path to determine whether a permitted repo-external or
  maintainer-approved visual reference exists;
- use the `not_usable` result to HOLD rather than forcing visual matching.

What #179 cannot do from this PR:

- compare raw-video segments against SF6Frames binaries, because none were
  usable;
- treat the fetched placeholder as visual evidence;
- infer official move identity from visual similarity alone;
- treat SF6Frames/UFD visuals as current-fact authority;
- commit GIFs, images, frames, screenshots, contact sheets, raw HTML, raw tool
  output, or private paths.

If source permission/terms are resolved later, the first useful #179 visual
checks are likely:

- Stribog family vs rows 8/11;
- OD Triglav family vs row 10 and mid-route ambiguous labels;
- SA3/CA family vs row 12 cinematic window.

If a future #179 run receives a corrected SF6Frames asset or a permitted local
visual reference, it must first record file type, frame count or still-image
status, resolution, overlay/frame-number visibility, sampling readiness,
preprocessing needs, and cleanup status before attempting visual matching.

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
6. Verify that the fetched asset is a real visual reference, not an error
   placeholder or unsupported payload.
7. Record metadata only in repo:
   - source;
   - character;
   - move candidate;
   - expected asset kind;
   - file type observed if permitted;
   - usability result and preprocessing needs;
   - cleanup/cache status;
   - authority boundary.
8. If the acquired visual is not usable, classify it as `not_usable` and keep
   #179 held until a corrected source path or approved local reference exists.
9. Delete binaries after review unless a later explicit repo-external cache
   retention rule applies.
10. Route visual comparison to #179 only after usability is established or
   explicitly held with reason.
11. Preserve the boundary that visual references are review support only.

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
- Record usability as `usable_as_is`, `needs_preprocessing`, `not_usable`, or
  `inconclusive` before treating #179 as ready for matching.
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

| Follow-up | Status after this PR | Reason |
|---|---|---|
| #179 JP move/action visual-reference matching | open; blocked for actual matching | #178 now includes a Scrapling usability smoke, but the inspected WebP was `not_usable`. Matching requires a corrected permitted visual reference or approved local usable sample. |
| #183 SF6 system-mechanics math reasoning fixtures | still relevant | Visual references do not solve damage/scaling reasoning or authority-boundary fixtures. |

No new follow-up issue is needed.

## Terminal State

- visual-atlas-acquisition: USABILITY_SMOKE_HOLD
- small JP scope selected: yes
- acquisition attempt result: SF6Frames page and M Stribog asset descriptor
  fetched through Scrapling; asset response was a WebP placeholder
- hold reason: inspected WebP was not a usable move visual
- visual-reference usability smoke: run
- usability result: `not_usable`
- metadata/report only: yes
- binary committed: no
- raw HTML committed: no
- current-fact authority: no
- #178 complete? yes for the path/usability boundary; no usable atlas asset was
  produced
- #179 ready? no for actual matching; it can only load the path/scope and must
  HOLD until a corrected usable visual reference exists

## Cleanup And Validation

| Check | Result |
|---|---|
| External binaries acquired? | yes, one maintainer-approved SF6Frames WebP in repo-external temp only |
| Permission-cleared visual reference inspected? | yes |
| Committed binaries? | no |
| Raw HTML committed? | no |
| Scratch cleanup | temp binary and extracted frame deleted |
| Private paths committed? | no |
| Validators run | see PR body |
