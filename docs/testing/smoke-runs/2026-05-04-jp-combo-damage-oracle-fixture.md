# JP Combo Damage Oracle Fixture Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-04 |
| Issue | #72 |
| Source | これ一本で全てわかるJPコンボ講座【りゅうせい・スト６】 |
| Source URL | `https://www.youtube.com/watch?v=nyFNgnzjV3M` |
| Video ID | `nyFNgnzjV3M` |
| Selected scope | `00:08-00:57` basic light combo chapter |
| Scratch root | repo-external `${XDG_CACHE_HOME:-$HOME/.cache}/sf6-skills/media-ingest/` |
| Raw media stored in repo | no |
| Full transcript stored in repo | no |

## Tooling

| Tool / Capability | Result | Notes |
|---|---|---|
| YouTube metadata inspection | pass | `yt-dlp` via `uvx` wrote metadata only to repo-external scratch. |
| Section download | pass | The selected section was temporarily downloaded outside the repo. |
| Frame/contact-sheet inspection | pass | Sparse frames, stills, crops, and contact sheets were generated outside the repo. |
| Japanese auto-caption inspection | partial | Captions were useful for chapter/context, but noisy for exact route notation. Full captions are not stored in repo. |
| Oracle fixture creation | partial | One high-confidence enabled case and two review-needed disabled candidates were recorded. |

## Observed Fixture Cases

| Case | Timestamp | Combo notation | Observed damage | Fixture status | Confidence | Notes |
|---|---:|---|---:|---|---|---|
| `jp-basic-light-stribog-001` | `00:23` | `しゃがみ小P > 立ち小P > 弱ストリボーグ` | 1240 | enabled seed | high | Overlay and combo damage label are clear. |
| `jp-basic-light-rush-extension-1482` | `00:45` | `小P > 小Pキャンセル > しゃがみ中P or 引き中Pタゲコン > 中ストリボーグ` | 1482 | review-needed disabled candidate | low/medium | Route-to-damage mapping is ambiguous. |
| `jp-basic-light-rush-extension-1527` | `00:56` | `小P > 小Pキャンセル > しゃがみ中P or 引き中Pタゲコン > 中ストリボーグ` | 1527 | review-needed disabled candidate | medium | Likely higher-damage branch, but still needs route normalization review. |

## Boundaries

- This run builds an eval oracle fixture, not curated knowledge.
- Observed damage is not current-system authority.
- The fixture must not feed generated references.
- Damage-hidden calculation evals are out of scope for this run.
- End-to-end video analysis is out of scope for this run.
- Raw video, frames, screenshots, contact sheets, and full captions/transcript are not stored in repo.

## Repo Boundary And Cleanup

- Repo-local media/state scan: no hits after excluding `.git` and `skills/sf6-agent/assets/frame-current/`.
- Scratch cleanup: done.
- Generated references: unchanged.
- Frame-current assets: unchanged.

## Findings

- The high-confidence baseline route is suitable as a first oracle seed.
- The rush-extension alternatives should remain disabled until combo notation and branch mapping are manually reviewed.
- A future combo notation contract is needed before broader damage calculation tests.
- A future fixture validator should check `evals/fixtures/combo-damage/*.yaml` once the shape is accepted.
