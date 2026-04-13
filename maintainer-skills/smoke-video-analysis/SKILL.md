---
name: smoke-video-analysis
description: Use when a maintainer wants to run local real-video smoke checks for `skills/video-analysis-core/` without mixing fixtures or generated outputs into public skills, `.agents/skills/`, or the core repo validator set.
---

Repository-only smoke workflow for real-video validation of `skills/video-analysis-core/`.

## Scope

- Use this only for maintainer operations in this repository.
- Target public skill: `skills/video-analysis-core/`.
- Use case manifests under `references/smoke-cases/` to stage and review local smoke runs.
- Treat this as real-behavior smoke, not as a replacement for repo contract validators under `tests/`.
- Do not turn this workflow into a public distribution unit.

## Canonical Output Boundary

- `skills/video-analysis-core/references/output-contract.md` remains the human-readable canonical output contract.
- `skills/video-analysis-core/assets/video-analysis-v0.schema.json` remains the machine-readable canonical schema.
- Smoke cases may add coarse expectations for review, but they must not redefine the canonical output shape.
- Canonical output must stay observation-first and must not require saved artifact paths.

## Storage Rules

- Keep raw input videos and optional transcript files outside public skill directories.
- Prefer ignored local paths such as `local/smoke-inputs/video-analysis/`.
- Keep generated prompts, JSON outputs, and validation summaries under ignored paths such as `local/smoke-out/video-analysis/`.
- Do not commit raw videos, transcripts, prompt packets, generated outputs, or validation summaries.
- Do not place smoke fixtures or generated artifacts under `skills/`, `.agents/skills/`, or `tests/`.

## Execution Flow

1. Choose a case manifest from `references/smoke-cases/`.
2. Run `scripts/dev/run-video-analysis-smoke.ps1` with the case id, input video path, optional transcript path, and an ignored output directory.
3. Use the generated request packet to run `skills/video-analysis-core/` against the local clip.
4. Save the canonical JSON output under the chosen local output directory.
5. Re-run the smoke script to validate the saved JSON against the canonical schema and the case invariants.

## Review Focus

- Confirm the output stays inside the canonical schema and segment vocabulary.
- Check coarse invariants only: non-empty segments, required tracks for the case, interval sanity, source linkage for any `derived_events`, and no saved-artifact-path requirement in canonical output.
- Use case notes to observe provisional v0 items such as `key_display` kind pressure, actor binding stability, `interaction` boundaries, and transcript/gameplay alignment.
- Do not turn smoke findings into new public contract fields unless the canonical design is intentionally updated.
