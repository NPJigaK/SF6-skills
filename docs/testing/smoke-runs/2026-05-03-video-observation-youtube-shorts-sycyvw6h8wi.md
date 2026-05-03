# Video Observation Pilot: YouTube Shorts syCYVW6h8WI

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-03 |
| Issue | #52 |
| Source | YouTube Shorts `syCYVW6h8WI` |
| Canonical URL | `https://www.youtube.com/shorts/syCYVW6h8WI` |
| Title | `【スト6】仕様を利用したテクニック！端から逃げやすくなる！` |
| Channel | ACQUA |
| Published/uploaded | 2026-04-29 |
| Duration | 69 seconds |
| Repo commit before changes | `126cc60` |
| Scratch root | `${XDG_CACHE_HOME:-$HOME/.cache}/sf6-skills/media-ingest` |
| Run directory | `20260503-youtube-shorts-sycyvw6h8wi` |

## Method

- Followed `workflows/ingest-video.md`.
- Followed `workflows/media-scratch-cache-policy.md`.
- Used repo-external scratch for temporary metadata, a low-resolution video copy, sparse sampled frames, a contact sheet, and Japanese auto-caption inspection.
- Used `yt-dlp` as a temporary repo-external tool downloaded into the scratch directory.
- Used `ffprobe` for duration/fps metadata and `ffmpeg` for sparse frame sampling.
- Used maintainer visual inspection of sampled frames and caption paraphrases for timestamped observations.
- Did not store raw video, raw frames, screenshots, contact sheet, browser cache, session state, or full captions/transcript in the repository.

## Tooling Check

| Tool / Capability | Result | Notes |
|---|---|---|
| YouTube metadata extraction | Pass | Title, channel, duration, upload date, and caption availability were collected into scratch. |
| Japanese auto-caption availability | Pass | Japanese auto-generated captions were available; full transcript was not stored in repo. |
| Temporary video access | Pass | 360x640 MP4, 30 fps, 69.077 seconds; stored only in scratch. |
| Frame sampling | Pass | Sparse frames and one contact sheet were generated only in scratch. |
| Hermes-native browser check | Partial | `sf6ingest` doctor shows browser/vision available, but this pilot used direct scratch-based observation for the video workflow. |

## Timestamped Observation Summary

| Time | Visible observation | Speaker/commentary claim | Confidence | Notes |
|---|---|---|---|---|
| 00:00-00:05 | ACQUA-branded Shorts layout with Japanese overlay about using an SF6 specification to escape the corner more easily. | Speaker introduces the topic as something many players may not know. | medium | Metadata and overlay support the topic only. |
| 00:05-00:15 | Gameplay appears to show a corner/near-corner escape into jump/back-jump movement. | Speaker describes escaping from the screen edge and then holding back jump. | medium | Character identities and exact moves unresolved. |
| 00:15-00:24 | Grounded/landing interaction is shown after jump movement. | Speaker discusses a landing window where guarding is possible and throw timing at landing. | low | This is not accepted current-system proof. |
| 00:24-00:34 | Gameplay and overlay frame the situation as holding up/back jump and being vulnerable to strikes. | Speaker says holding up/back jump can lose to strikes. | medium | Review-only. |
| 00:34-00:42 | Close-range sequence is presented as a back-jump-related guard example. | Speaker says the character is back-jumping but guarding and contrasts throw escape with guarding strikes. | medium | Visual support is partial. |
| 00:42-00:56 | Same demonstration context continues. | Speaker explains a small landing guard-only window and holding back jump becoming guard against strikes during that window. | low | Potential current mechanic; needs verification. |
| 00:57-01:09 | Final summary-style segment. | Speaker says the technique is strong but not universal, can still lose to throws or later attacks, and treats the behavior as specification. | medium | Useful as source-local explanation only. |

## Artifacts Created

- `knowledge/sources/videos/youtube-shorts-sycyvw6h8wi.md`
- `knowledge/evidence/video-observations/youtube-shorts-sycyvw6h8wi.observations.md`
- `knowledge/review/unresolved/youtube-shorts-sycyvw6h8wi.review.md`

No `knowledge/evidence/claims/*.claims.md` artifact was created because this first pilot only needed source metadata, observations, and review holding.

## Boundaries

- Raw video stored in repo: no.
- Raw frames or screenshots stored in repo: no.
- Full transcript stored in repo: no.
- Curated promotion: no.
- Generated references updated: no.
- Frame-current assets updated: no.
- Video-derived observations remain `observation / needs_review`.
- Speaker claims about landing behavior, throw timing, strike interaction, and specification status are not accepted current facts.

## Cleanup

- Scratch cleanup was performed after artifact drafting and validation.
- Retained scratch cache as canonical evidence: no.
- Repo-local media/state scan result: no unexpected media/state files after cleanup.

## Findings

- The existing `workflows/ingest-video.md` and `contracts/video-observation.schema.json` were sufficient for a first coarse video observation artifact.
- A dedicated validator for `knowledge/evidence/video-observations/*.observations.md` is still missing.
- A dedicated validator for `knowledge/sources/videos/*.md` is still missing.
- Short vertical videos can be observed safely as review-only evidence, but low resolution, overlays, and auto-caption quality limit confidence.

## Follow-ups

- Add an executable validator for video observation artifacts.
- Consider a video source artifact validator once more video sources exist.
- Review whether the observed technique should become a candidate claim only after independent gameplay/current-patch verification.
