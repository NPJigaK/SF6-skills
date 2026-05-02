# Media Scratch Cache Policy

This workflow defines how maintainers should handle temporary images, screenshots, videos, browser artifacts, and vision artifacts during image-aware or video ingest.

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
- full transcripts
- large excerpts
- browser cache artifacts
- session, memory, cron, or profile state
- credentials, tokens, or local `.env` files

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

Do not use repo-local paths such as `tmp/`, `.cache/`, `downloads/`, or `assets/raw/` for media ingest scratch files.

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
     -o -iname "*.mp4" -o -iname "*.mov" -o -iname "*.mkv" \) \
  -not -path "./.git/*" \
  -not -path "./skills/sf6-agent/assets/frame-current/*" \
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
