param(
  [string]$RepoRoot = (Join-Path $PSScriptRoot '..\..')
)

Set-StrictMode -Version Latest

$repoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$skillRoot = Join-Path $repoRoot 'skills\video-analysis-core'

function Normalize-Content {
  param(
    [Parameter(Mandatory = $true)]
    [string] $Content
  )

  return ($Content -replace "`r`n", "`n").TrimEnd("`r", "`n")
}

$requiredFiles = @(
  'skills/video-analysis-core/SKILL.md',
  'skills/video-analysis-core/references/output-contract.md',
  'skills/video-analysis-core/assets/video-analysis-v0.schema.json',
  'skills/video-analysis-core/agents/openai.yaml'
)

$missingFiles = $requiredFiles | Where-Object {
  -not (Test-Path -LiteralPath (Join-Path $repoRoot $_) -PathType Leaf)
}

if (@($missingFiles).Count -gt 0) {
  throw "Missing video-analysis-core public files: $($missingFiles -join ', ')"
}

foreach ($relativePath in @(
  'SKILL.md'
  'references\output-contract.md'
  'agents\openai.yaml'
)) {
  $fullPath = Join-Path $skillRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
    throw "Missing video-analysis-core public skill file: $relativePath"
  }
}

$expectedSkillContent = @'
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
'@

$expectedOutputContractContent = @'
# Output Contract

This skill emits observation-first SF6 video analysis output. `segments` are the truth surface. `derived_events` are optional projections.

## Root Shape

- `schema_version`
- `clip_metadata`
- `actor_bindings`
- `segments`
- `derived_events` (optional)

## Time Base and IDs

- The canonical timeline is normalized to 60fps.
- Segment and evidence ranges use clip-relative 0-based half-open intervals: `[start_frame, end_frame)`.
- `segment_id` and `evidence_id` are document-wide unique strings.
- Segment `confidence` and `binding_confidence` use numeric `[0, 1]`.
- Document-wide ID uniqueness is a semantic invariant for runtime outputs and is not fully enforced by this shell-only validator.

## Clip Metadata

- `clip_id`
- `source_fps` (`null` allowed when unknown)
- `normalized_fps = 60`
- `total_frames`
- optional `source_duration_sec`

## Actor Bindings

- `actor_ref`: `actor_a | actor_b`
- `slot_id`: `p1 | p2 | unknown`
- `character_slug`: resolved current-roster slug or `null`
- `appearance_hint`: string or `null`
- `binding_confidence`: numeric `[0, 1]`
- `binding_basis[]`: `hud_slot_ui | persistent_tracking | character_visual | key_display_overlay | transcript_or_audio | user_hint | manual_annotation | unknown`
- The `actor_bindings` array must include exactly one `actor_a` binding and exactly one `actor_b` binding.

## Tracks and Kinds

### `actor_a_local` / `actor_b_local`

- `jump`
- `forward_dash`
- `back_dash`
- `attack_commit_candidate`
- `throw_attempt`
- `projectile_emit_candidate`
- `blockstun_candidate`
- `hitstun_candidate`
- `knockdown_state`
- `wakeup_rise`

### `interaction`

- `contact_candidate`
- `hit_connect_candidate`
- `block_connect_candidate`
- `throw_connect_candidate`
- `projectile_presence`
- `side_switch_candidate`

### `global_phase`

- `round_intro`
- `fight_active`
- `super_freeze`
- `ko_overlay`
- `pause_or_cut`

### `key_display`

- `input_sequence_window`
- metadata: `actor_ref`, optional `overlay_lane`, optional `observed_input_text`

### `transcript`

- `utterance_span`
- metadata: `speaker_ref`, `speaker_role`, optional `actor_ref`, `text`, optional `language`, optional `source_subtype`

## Evidence

- `source_type`: `video | key_display | transcript`
- `frame_range` uses the normalized 60fps interval convention.
- `roi_hint` uses one of these shapes:
  - `{ "kind": "full_frame" }`
  - `{ "kind": "named_roi", "name": "key_display_left" }`
  - `{ "kind": "xywh_box", "x": 120, "y": 640, "width": 400, "height": 140 }`

## Derived Events

- `derived_events` is optional.
- Every derived event must carry `source_segment_ids`.
- Derived events are never the truth surface.
'@

$expectedOpenAiYamlContent = @'
interface:
  display_name: "SF6 Video Analysis Core"
  short_description: "Normalize raw SF6 video to 60fps and emit the canonical observation-first segment timeline."
  default_prompt: "Use $video-analysis-core to turn raw SF6 video into the canonical segment timeline defined by `references/output-contract.md` and `assets/video-analysis-v0.schema.json`."
'@

$actualSkillContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'SKILL.md') -Raw)
$actualOutputContractContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'references\output-contract.md') -Raw)
$actualOpenAiYamlContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'agents\openai.yaml') -Raw)

if ($actualSkillContent -ne (Normalize-Content $expectedSkillContent)) {
  throw 'Public video-analysis-core SKILL.md must match the exact public-shell contract'
}

if ($actualOutputContractContent -ne (Normalize-Content $expectedOutputContractContent)) {
  throw 'Public video-analysis-core output contract must match the exact published contract'
}

if ($actualOpenAiYamlContent -ne (Normalize-Content $expectedOpenAiYamlContent)) {
  throw 'Public video-analysis-core agents/openai.yaml must match the exact agent contract'
}

$schemaPath = Join-Path $skillRoot 'assets\video-analysis-v0.schema.json'
$schema = Get-Content -LiteralPath $schemaPath -Raw | ConvertFrom-Json

$requiredRoot = @('schema_version', 'clip_metadata', 'actor_bindings', 'segments')
foreach ($field in $requiredRoot) {
  if ($schema.required -notcontains $field) {
    throw "Schema missing required root field: $field"
  }
}

$segmentDef = $schema.'$defs'.segment
$requiredSegment = @('segment_id', 'track', 'kind', 'start_frame', 'end_frame', 'confidence', 'evidence_refs')
foreach ($field in $requiredSegment) {
  if ($segmentDef.required -notcontains $field) {
    throw "Schema missing required segment field: $field"
  }
}

$trackEnum = @('actor_a_local', 'actor_b_local', 'interaction', 'global_phase', 'key_display', 'transcript')
foreach ($track in $trackEnum) {
  if ($segmentDef.properties.track.enum -notcontains $track) {
    throw "Schema missing track enum: $track"
  }
}

$actorBindingsDef = $schema.properties.actor_bindings
if ($actorBindingsDef.minItems -ne 2 -or $actorBindingsDef.maxItems -ne 2) {
  throw 'Schema actor_bindings must require exactly two bindings'
}

foreach ($actorRef in @('actor_a', 'actor_b')) {
  $coverage = @($actorBindingsDef.allOf | Where-Object {
    $_.contains.properties.actor_ref.const -eq $actorRef -and
    $_.minContains -eq 1 -and
    $_.maxContains -eq 1
  })

  if ($coverage.Count -ne 1) {
    throw "Schema actor_bindings must require exactly one $actorRef binding"
  }
}

Write-Host 'video-analysis-core public shell OK'
