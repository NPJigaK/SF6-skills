# Hermes-native Image Observation Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-03 |
| Timezone | Asia/Tokyo |
| Issue | #48 |
| Source | `≪スト6≫読み合いに勝つコツ「読み合いをシンプルに作る」` |
| Source URL | https://note.com/mizen5/n/n1f61c8308a4d |
| Hermes profile | `sf6ingest` |
| Hermes version | Hermes Agent v0.12.0 (2026.4.30) |
| Scratch root | `${XDG_CACHE_HOME:-$HOME/.cache}/sf6-skills/media-ingest/` |
| Run directory | `20260503-mizen-simple-yomi-hermes-native-vision` |

## Tooling Check

| Capability | Result | Notes |
|---|---|---|
| Provider auth | Pass | `sf6ingest` had OpenAI Codex auth logged in. |
| Browser tool availability | Partial | `hermes doctor` reported browser available, but the browser daemon failed to start during the run. |
| Image discovery | Partial | Hermes discovered article image URLs from static source context rather than a rendered browser page. |
| Vision analysis | Pass | Hermes-native vision successfully analyzed direct image URLs. |
| Repo media/state boundary | Pass | No screenshots, copied images, browser cache, sessions, memory, `.env`, or raw media were stored in the repo. |

## Method

Hermes was run with `HERMES_HOME` set to the repo-external `sf6ingest` profile. The run asked Hermes to use native browser/vision tooling where available, inspect the Mizen article images, and avoid file modifications or repo-local media storage.

Hermes browser rendering did not complete because the browser daemon exited during startup. Hermes still discovered image URLs from the source context and used native vision analysis on direct image URLs.

## Image Observation Results

| Image Group | Hermes-native Method | Result | Confidence | Notes |
|---|---|---|---|---|
| Header image | Direct image URL vision analysis | Pass | medium | Read as a Japanese SF6-style banner about attack technique, winning mind games, and simplifying yomi. |
| Social/Q&A card | Direct image URL vision analysis | Pass | medium | Read as a Japanese Q&A/social-card style image with no obvious SF6 gameplay content. |
| Analogy diagram | Direct image URL vision analysis | Pass | medium | Read as a fire/water/grass type-effectiveness triangle used as an analogy, not SF6 gameplay evidence. |
| SF6 chart 1 | Direct image URL vision analysis | Pass | medium | Read as guard and backdash/jump compared against strike and command throw. |
| SF6 chart 2 | Direct image URL vision analysis | Pass | medium | Read as guard, backdash/jump, and invincible move or Drive Reversal compared against strike, command throw, and wait/observe. |
| SF6 chart 3 | Direct image URL vision analysis | Pass | medium | Read as guard and delayed throw-tech or invincible move compared against throw and shimmy. |
| SF6 chart 4 | Direct image URL vision analysis | Pass | medium | Read as a throw, shimmy, and strike chart against defensive options. |
| SF6 chart 5 | Direct image URL vision analysis | Pass | medium | Read as a narrowed simplified-pair chart with shimmy faded and throw/strike emphasized. |
| SF6 chart 6 | Direct image URL vision analysis | Pass | medium | Read as a narrowed simplified-pair chart with throw faded and shimmy/strike emphasized. |
| Book-cover images | Direct image URL vision analysis | Pass | medium | Read as Japanese esports/pro-gamer book covers and not direct SF6 article claim evidence. |

## Boundaries

- The run did not store article images, screenshots, downloaded media, browser cache, or Hermes session artifacts in the repository.
- The run did not promote image-derived observations to `knowledge/curated/`.
- The run did not update generated references or frame-current assets.
- Observations remain source-local and review-only.
- Hermes memory and session state are not canonical SF6 knowledge.

## Findings

- Hermes-native vision can inspect direct image URLs and extract useful image-level observations for this article.
- Hermes browser availability is not sufficient by itself: the browser daemon failed to start during this run, so rendered-page browser inspection remains a tooling gap.
- Static image discovery plus direct image URL vision was enough to verify Hermes-native vision analysis, but it is not equivalent to full rendered article inspection.
- The media scratch/cache policy was sufficient for this run; the repo-local media/state scan found no repo artifacts.

## Follow-ups

- If rendered-page browser inspection is required, debug the Hermes browser daemon startup separately.
- Keep image-derived claims as `observation` / `needs_review` unless separately reviewed and promoted.
