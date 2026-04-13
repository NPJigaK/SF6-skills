---
name: video-analysis-core
description: Use when a task needs observation-first SF6 video analysis from raw video, producing a canonical multi-track sparse segment timeline normalized to 60fps. Optional key-display and transcript inputs may enrich the output. Do not use this skill for exact current-fact lookup, patch audits, or verdict-heavy combo or match evaluation.
---

Analyze raw SF6 video by normalizing the working timeline to 60fps and emitting the canonical segment structure defined in `references/output-contract.md` and `assets/video-analysis-v0.schema.json`.

## Purpose

- Turn raw SF6 video into a reusable observation surface.
- Emit canonical `segments` as the truth surface.
- Keep `derived_events` optional and secondary.

## Required Inputs

- Raw video clip
- Optional transcript source
- Optional hints such as actor slot, character, crop, or key-display presence

## Workflow

1. Normalize the working timeline to 60fps and establish `clip_metadata`.
2. Bind stable actors as `actor_a` and `actor_b` when possible without relying on current screen side.
3. Emit canonical segments across `actor_a_local`, `actor_b_local`, `interaction`, `global_phase`, and optional `key_display` or `transcript` tracks.
4. Attach lightweight clip-relative `evidence_refs` instead of saved artifact paths.
5. Emit `derived_events` only when they can point back to canonical `source_segment_ids`.
6. Stop at the observation layer if the request needs exact move facts, current-fact lookup, or verdict-heavy interpretation.

## Output Rules

- Use the root shape from `assets/video-analysis-v0.schema.json`.
- Keep all times on the normalized 60fps axis.
- Use 0-based half-open intervals `[start_frame, end_frame)`.
- Treat `segments` as the truth surface.
- Use `character_slug = null` when actor resolution is unresolved.
- Keep `key_display` and `transcript` as shared modality tracks, not actor-specific track names.

## Constraints

- Do not depend on another skill directory.
- Do not require saved frame or crop paths in canonical output.
- Do not emit move taxonomy or `move_id` as canonical segment data.
- Do not make commentary verdicts, combo verdicts, or match verdicts part of this skill's canonical output.

## References

- Read `references/output-contract.md` for the canonical output contract and per-track vocabulary.
- Use `assets/video-analysis-v0.schema.json` as the machine-readable root schema.
