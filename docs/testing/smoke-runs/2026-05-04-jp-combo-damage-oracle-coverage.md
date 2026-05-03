# JP Combo Damage Oracle Fixture Coverage Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-04 |
| Issue | #76 |
| Source | これ一本で全てわかるJPコンボ講座【りゅうせい・スト６】 |
| Source URL | `https://www.youtube.com/watch?v=nyFNgnzjV3M` |
| Video ID | `nyFNgnzjV3M` |
| Selected scope | `00:57-02:00` mid-attack combo chapter expansion |
| Scratch root | repo-external `${XDG_CACHE_HOME:-$HOME/.cache}/sf6-skills/media-ingest/` |
| Raw media stored in repo | no |
| Full transcript stored in repo | no |

## Tooling

| Tool / Capability | Result | Notes |
|---|---|---|
| YouTube metadata inspection | pass | `yt-dlp` via `uvx` confirmed title, channel, duration, and upload date. |
| Section download | pass | `00:57-02:00` was temporarily downloaded outside the repo. |
| Frame/contact-sheet inspection | pass | Sparse frames, still frames, and a contact sheet were generated outside the repo. |
| Caption/transcript inspection | unavailable/partial | `yt-dlp --list-subs` listed automatic caption formats, but the video reported no downloadable subtitles. Full transcript was not stored. |
| Fixture coverage expansion | partial | Four mid-attack coverage candidates were recorded, all disabled for damage-hidden eval because notation still needs review. |

## Observed Fixture Candidates

| Case | Timestamp | Combo notation | Observed damage | Fixture status | Confidence | Notes |
|---|---:|---|---:|---|---|---|
| `jp-mid-rush-triglav-1824` | `01:10` | `中攻撃キャンセルラッシュ > しゃがみ大P > 強ストリボーグ > 中トルバラン > トリグラフ` | 1824 | disabled candidate | medium/high | Overlay and damage label are clear, but the starter is generic `中攻撃`. |
| `jp-mid-rush-od-triglav-3260` | `01:18` | `中攻撃キャンセルラッシュ > しゃがみ大P > 強ストリボーグ > 中トルバラン > ODトリグラフ追撃` | 3260 | disabled candidate | medium/high | OD follow-up variant is visible, but the full route inherits prior overlay context. |
| `jp-mid-corner-carry-rush-fhk-2763` | `01:33` | `中攻撃キャンセルラッシュ > しゃがみ大P > 強ストリボーグ > 前ステ > ラッシュ前大K(ちょい遅らせ) > トリグラフ` | 2763 | disabled candidate | medium/high | Adds corner-carry coverage; delayed forward-heavy-kick timing needs notation review. |
| `jp-mid-position-carry-1484` | `01:56` | `しゃがみ中P始動から端まで運ぶ位置別ルート` | 1484 | disabled candidate | low/high | Damage label is visible, but the inspected frame does not contain a complete route overlay. |

## Boundaries

- This run expands eval oracle fixture coverage, not curated knowledge.
- Observed damage is not current-system authority.
- The fixture must not feed generated references.
- Newly added cases remain `enabled_for_damage_hidden_eval: false`.
- Damage-hidden calculation evals are out of scope for this run.
- End-to-end video analysis is out of scope for this run.
- Raw video, frames, screenshots, contact sheets, and full captions/transcript are not stored in repo.

## Repo Boundary And Cleanup

- Repo-local media/state scan: no hits after excluding `.git` and `skills/sf6-agent/assets/frame-current/`.
- Scratch cleanup: done.
- Generated references: unchanged.
- Frame-current assets: unchanged.

## Findings

- The mid-attack chapter provides useful route-shape coverage, but not enough exact notation confidence to enable new damage-hidden eval cases.
- The main blocker is combo notation specificity: generic `中攻撃`, inherited route context, OD follow-up notation, delayed input timing, and position-specific route mapping.
- The existing fixture validator correctly permits disabled candidates while preserving the boundary around enabled cases.
