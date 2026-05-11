# SF6 Video Analysis Protocol

## Purpose

This document defines the SF6-specific video-analysis protocol for
Codex-to-Hermes delegation in v2.3. It is planning and policy documentation
only.

Hermes `video_analyze` may be considered only as a provider, model, credential,
toolset, and maintainer-environment dependent video observation capability. It
is not a source of truth.

Codex remains the repo implementation entrypoint. Hermes video output remains
observation draft input until converted into reviewed repo artifacts through
issue scope, validators, PR review, and merge.

Exact current facts remain grounded in `data/exports/`, `data/roster/`, and
packaged frame-current `official_raw`. Video observations must not replace
those authority surfaces.

This protocol does not run live Hermes, run live video analysis, scrape or
download sources, or store video, GIF, image, frame, screenshot, contact sheet,
browser cache, or transcript assets.

## When Codex May Delegate SF6 Video Analysis

Codex may ask Hermes to analyze SF6 video material only when all of these are
true:

- the target issue explicitly allows video observation or video-analysis
  planning
- the source material is explicitly provided or referenced
- the requested output is an observation draft or review input
- tool availability and limitations will be recorded
- validators or review paths for the resulting repo artifact are known
- the request does not ask for exact current-fact conclusions from video alone

Codex must not delegate video analysis when the request would:

- infer exact frame data from video alone
- override packaged frame-current `official_raw`
- store raw video, frames, screenshots, GIFs, contact sheets, browser cache, or
  full transcripts in the repo
- rely on stale PR #83 or old issue #82 as active source material
- require live Hermes execution in CI
- bypass issue scope, validators, or review

## `video_analyze` Capability Boundary

`video_analyze` may be used only when it is official-source verified and
available in the maintainer environment.

Availability depends on provider, model, credentials, enabled toolsets, local
configuration, and source media compatibility. Exact toolset and invocation
details must remain aligned with
`docs/architecture/hermes-cli-capability-reference.md`.

If `video_analyze` is unavailable or unverified, Codex must use a documented
fallback:

- manual review
- frame sampling
- vision analysis
- hold

Missing `video_analyze` support is not a blocker by itself and must not lead to
fabricated observations, inferred frame data, or invented current facts.

## SF6 Video Observation Protocol

Future video observation drafts should include these fields or equivalent
reviewable concepts:

- source reference
- segment reference
- timestamp or time range
- source video fps, effective fps, or unknown fps
- game-native fps assumption, usually 60fps / 60F when applicable
- frame-window notes
- observed event
- visible UI, input, overlay, or damage-label notes
- uncertainty
- directly observed
- not inferred
- tool used or tool unavailable
- tool limitations
- review status
- `official_raw` check requirement

The observation artifact should make it easy for a reviewer to see the
difference between what the video appears to show and what the repo is allowed
to treat as knowledge.

## 60F And Source-Fps Boundary

SF6 gameplay uses game-native 60fps assumptions, but source videos may not be
true 60fps.

YouTube, stream, replay, or captured footage may be:

- 30fps
- variable fps
- edited
- slowed or sped up
- interpolated
- dropped-frame
- compressed
- desynced from audio, input, or overlay timing

Do not infer exact frame counts when source fps, effective fps, dropped frames,
edits, or playback speed are uncertain.

If exact frame-window inference is unsafe, mark the observation as hold or
uncertain. A 60F frame-window is an observation aid, not exact current-fact
authority.

When the game-native 60fps assumption and source-video fps differ, the
observation must record that mismatch and avoid exact frame-derived
conclusions unless a separate accepted authority path supports them.

## Direct Observation Vs Inference

Direct observation may include:

- visible character action
- visible UI, input, or overlay
- hit spark, guard spark, or whiff candidate
- visible damage label
- round, timer, life, or score state
- camera or replay context

Do not infer final authority for:

- exact startup
- exact active frames
- exact recovery
- exact hit advantage
- exact block advantage
- exact damage formula
- exact frame-current fact
- route verdict
- matchup verdict
- coaching conclusion as final authority

An observation may identify a candidate event, candidate move, or candidate
interaction, but it must record confidence and what was not inferred.

## SF6-Specific Boundaries

Video observations are observation-only until reviewed and promoted through an
accepted repo path.

They must not become:

- exact move, frame, or current-fact authority from video alone
- exact frame data from video alone
- combo verdict, route verdict, damage verdict, matchup verdict, or coaching
  conclusion as final authority
- public `sf6-agent` behavior
- replacement for packaged frame-current `official_raw`

Observed damage labels are eval or review context only unless accepted by a
separate authority path. Training UI observations are not current-system
authority by default.

Conflicts between video observations and packaged current facts require hold,
review, or a frame-data refresh workflow. They must not silently replace
`official_raw`.

Hermes memory, sessions, local skills, Curator output, browser state, local
media scratch, and private local state are not video evidence.

## Output Shape

Future video observation drafts may use this shape or an equivalent
schema-aligned artifact:

```json
{
  "observation_id": "match1-r1-0123-drive-rush-candidate",
  "source_ref": "match1",
  "segment_ref": "round1",
  "timestamp": "01:23.400-01:24.100",
  "source_video_fps": "unknown",
  "effective_fps": "unknown",
  "game_fps_assumption": 60,
  "frame_window": {
    "kind": "candidate_window",
    "notes": "Source fps is unknown; do not infer exact frame count."
  },
  "candidate_event": "drive-rush-approach-candidate",
  "candidate_move": "unknown",
  "confidence": "medium",
  "directly_observed": [
    "Green visual effect appears before close-range contact",
    "Guard spark candidate appears after the approach"
  ],
  "not_inferred": [
    "exact startup",
    "exact active frames",
    "exact recovery",
    "exact hit advantage",
    "exact block advantage",
    "exact damage",
    "current-system frame fact"
  ],
  "tool_used": "manual_review",
  "tool_limitations": [
    "video_analyze unavailable",
    "source fps unknown"
  ],
  "official_raw_check": {
    "required": true,
    "status": "not_checked"
  },
  "review_status": "needs_review"
}
```

The example intentionally avoids exact frame values as video-derived facts.
`candidate_move` and `candidate_event` are not final authority. Confidence,
`not_inferred`, `official_raw_check`, and `review_status` are required
concepts.

## Relationship To #124 External Frame-Atlas Policy

External visual references, GIFs, frame atlases, hitbox overlays, and
clean/no-hitbox variants are handled by #124.

This protocol does not fetch, download, store, or authorize external visual
assets. Any external visual reference must remain observation or review support
only.

No external atlas, GIF, image, hitbox overlay, clean visual, or video
observation may override packaged `official_raw`.

## Expected Follow-Up Surfaces

Future v2.3 work should connect this protocol to these surfaces:

- #120 should include or reference this protocol through
  `resources/sf6-video-analysis-protocol.md` and
  `guards/video-observation-boundary.md`.
- #115 dry-run fixtures should cover:
  - valid video observation request
  - unavailable `video_analyze` fallback
  - forbidden exact current-fact inference
  - stale PR/video debt rejection
  - observed damage label boundary
- #121 owns the Hermes CLI capability reference.
- #124 owns external frame-atlas and cache policy.

These follow-up surfaces must preserve the same current-fact, raw-media,
external-asset, and public adapter boundaries.

## Non-Goals

This protocol does not implement #124, #120, #115, or #119. It does not add
`packs/codex-hermes-sf6/`, dry-run fixtures, plugin or gateway planning, live
Hermes execution, live video analysis, external scraping, external asset
downloads, raw video storage, frame storage, screenshot storage, GIF storage,
contact sheet storage, browser cache storage, full transcript storage, Hermes
prompts, runtime lookup, answer behavior, public `sf6-agent` behavior,
generated outputs, `.dist` changes, frame-current changes, normalization
changes, historical smoke report rewrites, or stale PR #83 / old issue #82
imports.
