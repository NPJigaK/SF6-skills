# Media Scratch Cache Policy

This workflow defines how maintainers should handle temporary images, screenshots, videos, browser artifacts, frame-atlas assets, and vision artifacts during image-aware or video ingest.

Raw media is working material. It is not canonical SF6 knowledge and should not be committed to this repository by default.

## Repo Boundary

The repository should store reviewable knowledge artifacts, not raw media caches.

Allowed repo artifacts include:

- source URLs
- `accessed_at` and `captured_at` metadata
- short source summaries
- image or video observation summaries
- image index or timestamp references
- uncertainty notes
- candidate claims
- review notes

Forbidden repo artifacts by default include:

- raw article images
- screenshots
- copied article image assets
- downloaded videos or clips
- GIFs, WebP files, frame dumps, contact sheets, thumbnails, or generated visual derivatives
- full transcripts
- raw captions or subtitle files
- large excerpts
- browser cache artifacts
- local media cache directories
- external frame-atlas binary assets
- session, memory, cron, or profile state
- credentials, tokens, or local `.env` files

`official_raw` remains the current-fact authority. Local media caches, retained scratch files, external visual atlas assets, and visual review artifacts are not current-fact authority and do not override `official_raw`.

## Scratch Root

Use a repo-external scratch/cache root for temporary media work.

Recommended WSL/Linux/macOS root:

```bash
scratch_root="${XDG_CACHE_HOME:-$HOME/.cache}/sf6-skills/media-ingest"
```

Optional Windows equivalent:

```text
%LOCALAPPDATA%\sf6-skills\media-ingest\
```

Future external frame-atlas cache sync, if approved by a later explicit issue, must also use a repo-external root such as:

```bash
atlas_cache_root="${XDG_CACHE_HOME:-$HOME/.cache}/sf6-skills/external-frame-atlas"
```

Do not use repo-local paths such as `tmp/`, `.cache/`, `downloads/`, or `assets/raw/` for media ingest scratch files.

## External Frame-Atlas Boundary

External frame-atlas assets are visual references only. They are not numeric frame-data ingestion sources, current-fact authority, public answer behavior, or permission to store binaries in the repository.

Future external frame-atlas cache sync or GIF/image video-usability smoke must be:

- a later explicit issue only;
- maintainer-local only;
- repo-external by default;
- disabled from CI;
- excluded from public `sf6-agent` behavior and release bundles;
- sanitized into reports or metadata only;
- unable to override `official_raw`;
- unable to become current-fact authority;
- unable to ingest numeric frame data from external visual sources.

This policy does not authorize #140 to scrape, download, cache, or sync external frame-atlas assets. If a later issue approves acquisition, it should align with existing repo acquisition discipline before adding any new fetch technology, but #140 implements no acquisition.

Recommended future gated sequence, not implemented here:

1. External frame-atlas local cache sync smoke:
   - later explicit issue only;
   - after this binary/cache guard is merged;
   - after permission, terms, robots, and rate-limit review;
   - maintainer-local only;
   - repo-external cache only;
   - CI disabled;
   - no raw binary commit;
   - sanitized report and metadata only.
2. External frame-atlas video usability smoke:
   - later explicit issue only;
   - after local cache sync smoke succeeds or is safely held;
   - tiny sample only;
   - compare hitbox overlay, clean visual, GIF/contact-sheet style review support;
   - evaluate candidate move identification as useful, limited, not_safe, or unsupported;
   - record false-positive risks, overlay/crop/compression failure modes, and source/effective FPS or GIF timing uncertainty;
   - preserve not-inferred fields;
   - no exact startup/active/recovery inference;
   - no exact hit/block advantage inference;
   - no current-fact promotion;
   - no `official_raw` override.

## Forbidden Repo Locations

Repo-tracked binary media, media cache, and external atlas binary artifacts are forbidden by default in:

- `skills/sf6-agent/`
- public release bundle paths
- `.dist`
- `runtime/frame-current/`
- `skills/sf6-agent/assets/frame-current/`
- `runtime/normalization/`
- `skills/sf6-agent/assets/normalization/`
- `data/raw`
- `data/normalized`
- `data/exports`
- `tests/fixtures/` unless metadata-only
- `knowledge/` unless metadata-only source, evidence, or report artifacts
- `docs/testing/smoke-runs/` except sanitized reports
- `tmp/`
- `.cache/`
- `downloads/`
- `assets/raw/`
- `.external-cache/`
- `.external-assets/`
- `.local-media/`
- `.video-cache/`
- `.frame-atlas-cache/`

Maintainer-configured scratch paths are allowed only when they are outside the repository. Ignored local scratch inside the repository requires a later explicit issue, `.gitignore` coverage, and validator coverage.

## Per-run Directory

Create one directory per ingest run:

```bash
run_id="$(date +%Y%m%d)-<source-slug>"
run_dir="$scratch_root/$run_id"
mkdir -p "$run_dir"
```

Example:

```bash
~/.cache/sf6-skills/media-ingest/20260502-mizen-simple-yomi/
```

The run directory may hold temporary downloads, extracted frames, screenshots, OCR intermediates, browser exports, or other working files while the ingest run is active.

## Cleanup And Retention

Default behavior: delete scratch files after the run.

```bash
du -sh "$run_dir"
rm -rf "$run_dir"
test ! -e "$run_dir"
```

If temporary media must be retained briefly:

- keep it outside the repo;
- record the reason in the smoke report or maintainer notes;
- prefer retention of 7 days or less;
- do not treat retained local cache as canonical evidence;
- delete it when the review task is complete.

Retained cache is only a maintainer convenience. Repo artifacts such as source metadata, observations, claims, and review notes are the reviewable record.

## Verification

After media ingest work, verify the repository did not receive raw media or local state:

```bash
git status --porcelain

find . \
  \( -name ".hermes" -o -name ".env" -o -iname "*session*" -o -iname "*memory*" -o -iname "*cron*" \
     -o -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.webp" \
     -o -iname "*.gif" \
     -o -iname "*.mp4" -o -iname "*.mov" -o -iname "*.mkv" -o -iname "*.avi" \
     -o -iname "*.vtt" -o -iname "*.srt" -o -iname "*.ass" \
     -o -iname "*.info.json" \
     -o -iname "*frame*dump*" -o -iname "*contact*sheet*" \) \
  -not -path "./.git/*" \
  | sort
```

Record in the PR or smoke report whether cleanup was completed or whether repo-external cache remains temporarily with a reason.

## Hermes And Browser/Vision State

Hermes, browser, and vision profile state must remain outside the repository.

Hermes memory, browser cache, screenshots, downloaded images, extracted frames, and session state are not canonical SF6 knowledge. If Hermes-native vision is tested, this scratch policy still applies.

Final outputs should be normalized into repository artifacts under the appropriate surfaces, such as:

- `knowledge/sources/`
- `knowledge/evidence/claims/`
- `knowledge/review/`
- `docs/testing/smoke-runs/`
