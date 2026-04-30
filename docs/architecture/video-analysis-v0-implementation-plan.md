# Video Analysis V0 Implementation Plan

**Goal:** Add the first standalone public video-analysis skill as an observation-first SF6 video foundation that normalizes raw video to 60fps and emits the canonical segment schema defined in the approved design.

**Architecture:** Implement a self-contained public skill at `skills/video-analysis-core/` with its own prompt, human-readable output contract, and machine-readable JSON Schema. Protect the new public shell with a dedicated validator, update repo guidance so the skill is discoverable, and sync the generated `.agents/skills/` dogfood mirror without introducing any cross-skill dependency.

**Tech Stack:** Markdown, JSON Schema, YAML, PowerShell validators and sync scripts

---

## Planned File Map

Create:

- `E:/github/SF6-skills/skills/video-analysis-core/SKILL.md`
  - Public skill entrypoint for observation-first SF6 video analysis.
- `E:/github/SF6-skills/skills/video-analysis-core/references/output-contract.md`
  - Self-contained contract for the canonical output shape, tracks, kinds, actor bindings, and evidence model.
- `E:/github/SF6-skills/skills/video-analysis-core/assets/video-analysis-v0.schema.json`
  - Machine-readable JSON Schema for the canonical output document.
- `E:/github/SF6-skills/skills/video-analysis-core/agents/openai.yaml`
  - OpenAI-facing skill metadata.
- `E:/github/SF6-skills/tests/integration/validate-video-analysis-core-location.ps1`
  - Public-shell validator for the new skill.

Modify:

- `E:/github/SF6-skills/docs/architecture/video-analysis-v0-design.md`
  - Lock the remaining executable schema conventions before the public shell is written.
- `E:/github/SF6-skills/docs/testing/README.md`
  - Add the new validator command to the local verification set.
- `E:/github/SF6-skills/tests/packaging/validate-doc-links.ps1`
  - Require the new skill to be registered in repo guidance.
- `E:/github/SF6-skills/AGENTS.md`
  - Register the public video-analysis skill and its observation-only boundary.
- `E:/github/SF6-skills/docs/architecture/README.md`
  - Add the new design and implementation plan as architecture entrypoints.

Generated:

- `E:/github/SF6-skills/.agents/skills/video-analysis-core/**`
  - Repo-local dogfood mirror generated from `skills/video-analysis-core/`.

## Assumption Locked By This Plan

This plan uses `skills/video-analysis-core/` as the public skill directory name. If maintainers want a different slug, rename every path in this plan consistently before execution begins.

### Task 1: Add the Public Skill Shell and Output Contract

**Files:**
- Create: `E:/github/SF6-skills/tests/integration/validate-video-analysis-core-location.ps1`
- Create: `E:/github/SF6-skills/skills/video-analysis-core/SKILL.md`
- Create: `E:/github/SF6-skills/skills/video-analysis-core/references/output-contract.md`
- Create: `E:/github/SF6-skills/skills/video-analysis-core/assets/video-analysis-v0.schema.json`
- Create: `E:/github/SF6-skills/skills/video-analysis-core/agents/openai.yaml`
- Modify: `E:/github/SF6-skills/docs/architecture/video-analysis-v0-design.md`
- Modify: `E:/github/SF6-skills/docs/testing/README.md`
- Test: `E:/github/SF6-skills/tests/integration/validate-video-analysis-core-location.ps1`

- [ ] **Step 1: Write the failing validator for the new public skill shell**

```powershell
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
```

- [ ] **Step 2: Run the validator to verify the new shell is still missing**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/validate-video-analysis-core-location.ps1
```

Expected: FAIL with `Missing video-analysis-core public files`.

- [ ] **Step 3: Tighten the design doc so the remaining schema details are executable**

Ensure `E:/github/SF6-skills/docs/architecture/video-analysis-v0-design.md` contains these exact points without duplicating existing sections:

```md
### Canonical Segment Record

- `segment_id` is a document-wide unique string.
- `confidence` is always present and uses a numeric `[0, 1]` scale.

### Evidence Rules

- `source_type` uses the stable vocabulary `video | key_display | transcript`.
- `roi_hint` uses one of these shapes:
  - `{ "kind": "full_frame" }`
  - `{ "kind": "named_roi", "name": "key_display_left" }`
  - `{ "kind": "xywh_box", "x": 120, "y": 640, "width": 400, "height": 140 }`

### Key Display

- `observed_input_text` may be carried as optional segment metadata for observed input notation.

## Open Schema Details

- `actor_bindings` must contain exactly one `actor_a` binding and exactly one `actor_b` binding.
- `segment_id` and `evidence_id` are document-wide unique strings.
- Segment `confidence` and `binding_confidence` both use numeric `[0, 1]`.
- `evidence_refs.source_type` uses `video | key_display | transcript`.
- `roi_hint` is a discriminated object using `full_frame`, `named_roi`, or `xywh_box`.
- `key_display` segments may carry optional `observed_input_text`.
- JSON Schema enforces actor-binding coverage, while document-wide ID uniqueness remains a semantic invariant for future concrete-output validation.
```

- [ ] **Step 4: Create the public skill entrypoint, output contract reference, and OpenAI metadata**

Create `E:/github/SF6-skills/skills/video-analysis-core/SKILL.md`:

```md
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
```

Create `E:/github/SF6-skills/skills/video-analysis-core/references/output-contract.md`:

```md
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
```

Create `E:/github/SF6-skills/skills/video-analysis-core/agents/openai.yaml`:

```yaml
interface:
  display_name: "SF6 Video Analysis Core"
  short_description: "Normalize raw SF6 video to 60fps and emit the canonical observation-first segment timeline."
  default_prompt: "Use $video-analysis-core to turn raw SF6 video into the canonical segment timeline defined by `references/output-contract.md` and `assets/video-analysis-v0.schema.json`."
```

- [ ] **Step 5: Create the machine-readable JSON Schema and register the validator in testing docs**

Create `E:/github/SF6-skills/skills/video-analysis-core/assets/video-analysis-v0.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://sf6-skills.local/video-analysis-v0.schema.json",
  "title": "SF6 Video Analysis V0 Output",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "clip_metadata",
    "actor_bindings",
    "segments"
  ],
  "properties": {
    "schema_version": {
      "const": "1.0.0"
    },
    "clip_metadata": {
      "$ref": "#/$defs/clipMetadata"
    },
    "actor_bindings": {
      "type": "array",
      "minItems": 2,
      "maxItems": 2,
      "allOf": [
        {
          "contains": {
            "type": "object",
            "required": [
              "actor_ref"
            ],
            "properties": {
              "actor_ref": {
                "const": "actor_a"
              }
            }
          },
          "minContains": 1,
          "maxContains": 1
        },
        {
          "contains": {
            "type": "object",
            "required": [
              "actor_ref"
            ],
            "properties": {
              "actor_ref": {
                "const": "actor_b"
              }
            }
          },
          "minContains": 1,
          "maxContains": 1
        }
      ],
      "items": {
        "$ref": "#/$defs/actorBinding"
      }
    },
    "segments": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/$defs/segment"
      }
    },
    "derived_events": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/derivedEvent"
      }
    }
  },
  "$defs": {
    "clipMetadata": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "clip_id",
        "source_fps",
        "normalized_fps",
        "total_frames"
      ],
      "properties": {
        "clip_id": {
          "type": "string",
          "minLength": 1
        },
        "source_fps": {
          "type": [
            "number",
            "null"
          ],
          "exclusiveMinimum": 0
        },
        "normalized_fps": {
          "const": 60
        },
        "total_frames": {
          "type": "integer",
          "minimum": 1
        },
        "source_duration_sec": {
          "type": [
            "number",
            "null"
          ],
          "minimum": 0
        }
      }
    },
    "actorBinding": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "actor_ref",
        "slot_id",
        "character_slug",
        "appearance_hint",
        "binding_confidence",
        "binding_basis"
      ],
      "properties": {
        "actor_ref": {
          "enum": [
            "actor_a",
            "actor_b"
          ]
        },
        "slot_id": {
          "enum": [
            "p1",
            "p2",
            "unknown"
          ]
        },
        "character_slug": {
          "type": [
            "string",
            "null"
          ],
          "minLength": 1
        },
        "appearance_hint": {
          "type": [
            "string",
            "null"
          ]
        },
        "binding_confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "binding_basis": {
          "type": "array",
          "minItems": 1,
          "uniqueItems": true,
          "items": {
            "enum": [
              "hud_slot_ui",
              "persistent_tracking",
              "character_visual",
              "key_display_overlay",
              "transcript_or_audio",
              "user_hint",
              "manual_annotation",
              "unknown"
            ]
          }
        }
      }
    },
    "frameRange": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "start_frame",
        "end_frame"
      ],
      "properties": {
        "start_frame": {
          "type": "integer",
          "minimum": 0
        },
        "end_frame": {
          "type": "integer",
          "minimum": 1
        }
      }
    },
    "roiHint": {
      "oneOf": [
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind"
          ],
          "properties": {
            "kind": {
              "const": "full_frame"
            }
          }
        },
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind",
            "name"
          ],
          "properties": {
            "kind": {
              "const": "named_roi"
            },
            "name": {
              "type": "string",
              "minLength": 1
            }
          }
        },
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "kind",
            "x",
            "y",
            "width",
            "height"
          ],
          "properties": {
            "kind": {
              "const": "xywh_box"
            },
            "x": {
              "type": "integer",
              "minimum": 0
            },
            "y": {
              "type": "integer",
              "minimum": 0
            },
            "width": {
              "type": "integer",
              "minimum": 1
            },
            "height": {
              "type": "integer",
              "minimum": 1
            }
          }
        }
      ]
    },
    "evidenceRef": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "evidence_id",
        "source_type",
        "frame_range"
      ],
      "properties": {
        "evidence_id": {
          "type": "string",
          "minLength": 1
        },
        "source_type": {
          "enum": [
            "video",
            "key_display",
            "transcript"
          ]
        },
        "frame_range": {
          "$ref": "#/$defs/frameRange"
        },
        "roi_hint": {
          "$ref": "#/$defs/roiHint"
        },
        "note": {
          "type": "string"
        }
      }
    },
    "segment": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "segment_id",
        "track",
        "kind",
        "start_frame",
        "end_frame",
        "confidence",
        "evidence_refs"
      ],
      "properties": {
        "segment_id": {
          "type": "string",
          "minLength": 1
        },
        "track": {
          "type": "string",
          "enum": [
            "actor_a_local",
            "actor_b_local",
            "interaction",
            "global_phase",
            "key_display",
            "transcript"
          ]
        },
        "kind": {
          "type": "string"
        },
        "family": {
          "type": [
            "string",
            "null"
          ]
        },
        "start_frame": {
          "type": "integer",
          "minimum": 0
        },
        "end_frame": {
          "type": "integer",
          "minimum": 1
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "evidence_refs": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/$defs/evidenceRef"
          }
        },
        "actor_ref": {
          "enum": [
            "actor_a",
            "actor_b",
            "unknown"
          ]
        },
        "screen_side": {
          "enum": [
            "left",
            "right",
            "unknown"
          ]
        },
        "overlay_lane": {
          "enum": [
            "lane_1",
            "lane_2",
            "unknown"
          ]
        },
        "speaker_ref": {
          "type": "string",
          "pattern": "^(speaker_[1-9][0-9]*|unknown)$"
        },
        "speaker_role": {
          "enum": [
            "commentary",
            "actor_voice",
            "system_voice",
            "unknown"
          ]
        },
        "text": {
          "type": "string",
          "minLength": 1
        },
        "language": {
          "type": [
            "string",
            "null"
          ]
        },
        "source_subtype": {
          "enum": [
            "provided_transcript",
            "asr",
            "subtitle_ocr",
            "unknown"
          ]
        },
        "observed_input_text": {
          "type": "string"
        }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "track": {
                "enum": [
                  "actor_a_local",
                  "actor_b_local"
                ]
              }
            },
            "required": [
              "track"
            ]
          },
          "then": {
            "properties": {
              "kind": {
                "enum": [
                  "jump",
                  "forward_dash",
                  "back_dash",
                  "attack_commit_candidate",
                  "throw_attempt",
                  "projectile_emit_candidate",
                  "blockstun_candidate",
                  "hitstun_candidate",
                  "knockdown_state",
                  "wakeup_rise"
                ]
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "track": {
                "const": "interaction"
              }
            },
            "required": [
              "track"
            ]
          },
          "then": {
            "properties": {
              "kind": {
                "enum": [
                  "contact_candidate",
                  "hit_connect_candidate",
                  "block_connect_candidate",
                  "throw_connect_candidate",
                  "projectile_presence",
                  "side_switch_candidate"
                ]
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "track": {
                "const": "global_phase"
              }
            },
            "required": [
              "track"
            ]
          },
          "then": {
            "properties": {
              "kind": {
                "enum": [
                  "round_intro",
                  "fight_active",
                  "super_freeze",
                  "ko_overlay",
                  "pause_or_cut"
                ]
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "track": {
                "const": "key_display"
              }
            },
            "required": [
              "track"
            ]
          },
          "then": {
            "required": [
              "actor_ref"
            ],
            "properties": {
              "kind": {
                "const": "input_sequence_window"
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "track": {
                "const": "transcript"
              }
            },
            "required": [
              "track"
            ]
          },
          "then": {
            "required": [
              "speaker_ref",
              "speaker_role",
              "text"
            ],
            "properties": {
              "kind": {
                "const": "utterance_span"
              }
            }
          }
        }
      ]
    },
    "derivedEvent": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "event_id",
        "kind",
        "frame_index",
        "source_segment_ids"
      ],
      "properties": {
        "event_id": {
          "type": "string",
          "minLength": 1
        },
        "kind": {
          "type": "string",
          "minLength": 1
        },
        "frame_index": {
          "type": "integer",
          "minimum": 0
        },
        "source_segment_ids": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    }
  }
}
```

Keep the JSON Schema responsible for structural invariants, including exact `actor_a` / `actor_b` coverage in `actor_bindings`. Treat document-wide uniqueness for `segment_id`, `evidence_id`, and `event_id` as a semantic runtime invariant that this shell-only plan documents now and defers for future concrete-output validation.

Update `E:/github/SF6-skills/docs/testing/README.md` by adding this command to the core local verification set:

```md
- `powershell -ExecutionPolicy Bypass -File tests/integration/validate-video-analysis-core-location.ps1`
```

- [ ] **Step 6: Run the new validator to verify the public shell now passes**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/validate-video-analysis-core-location.ps1
```

Expected: PASS with `video-analysis-core public shell OK`.

- [ ] **Step 7: Commit the public shell and contract**

```bash
git add docs/architecture/video-analysis-v0-design.md docs/testing/README.md tests/integration/validate-video-analysis-core-location.ps1 skills/video-analysis-core
git commit -m "feat: add video-analysis-core public shell"
```

### Task 2: Register the New Skill in Repo Guidance

**Files:**
- Modify: `E:/github/SF6-skills/tests/packaging/validate-doc-links.ps1`
- Modify: `E:/github/SF6-skills/AGENTS.md`
- Modify: `E:/github/SF6-skills/docs/architecture/README.md`
- Test: `E:/github/SF6-skills/tests/packaging/validate-doc-links.ps1`

- [ ] **Step 1: Extend the doc-link validator so it fails until repo guidance mentions the new skill**

Add these checks to `E:/github/SF6-skills/tests/packaging/validate-doc-links.ps1`:

```powershell
  @{ Path = 'AGENTS.md'; MustContain = 'skills/video-analysis-core/' },
  @{ Path = 'docs/architecture/README.md'; MustContain = 'video-analysis-v0-design.md' },
  @{ Path = 'docs/architecture/README.md'; MustContain = 'video-analysis-v0-implementation-plan.md' }
```

- [ ] **Step 2: Run the doc-link validator to verify the repo guidance is still missing**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected: FAIL because `AGENTS.md` and `docs/architecture/README.md` do not mention the new skill yet.

- [ ] **Step 3: Update `AGENTS.md` and the architecture index**

Add these lines under `## Knowledge と Skills` in `E:/github/SF6-skills/AGENTS.md`:

```md
- 動画観測の canonical segment timeline は `skills/video-analysis-core/` に寄せる。
- `skills/video-analysis-core/` は raw video を 60fps に正規化した observation-first surface を返す。
- exact current fact や verdict-heavy interpretation はこの skill で断定しない。
```

Update `E:/github/SF6-skills/docs/architecture/README.md` so the primary entrypoints become:

```md
# Architecture Docs

Repository-level architecture notes and dependency-boundary decisions.

Primary entrypoints:

- `repo-structure-contract.md`
- `kb-sf6-frame-current-packaging.md`
- `video-analysis-v0-design.md`
- `video-analysis-v0-implementation-plan.md`
```

- [ ] **Step 4: Run the doc-link validator again**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-doc-links.ps1
```

Expected: PASS with `Docs OK`.

- [ ] **Step 5: Commit the repo guidance updates**

```bash
git add AGENTS.md docs/architecture/README.md tests/packaging/validate-doc-links.ps1
git commit -m "docs: register video-analysis-core guidance"
```

### Task 3: Sync the Dogfood Mirror and Run the Repo Verification Set

**Files:**
- Generated: `E:/github/SF6-skills/.agents/skills/video-analysis-core/**`
- Test: `E:/github/SF6-skills/scripts/dev/sync-dogfood-skills.ps1`
- Test: `E:/github/SF6-skills/tests/integration/validate-public-skill-boundaries.ps1`
- Test: `E:/github/SF6-skills/tests/integration/validate-video-analysis-core-location.ps1`
- Test: `E:/github/SF6-skills/tests/install/validate-dogfood-mirror.ps1`
- Test: `E:/github/SF6-skills/tests/install/validate-distribution-surface.ps1`
- Test: `E:/github/SF6-skills/tests/packaging/validate-layout.ps1`

- [ ] **Step 1: Sync `skills/` into `.agents/skills/`**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

Expected: PASS with `Synced <count> public skills to .agents/skills`, and `.agents/skills/video-analysis-core/` exists afterward.

- [ ] **Step 2: Verify public-skill path boundaries**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/validate-public-skill-boundaries.ps1
```

Expected: PASS with `Public skill boundaries OK`.

- [ ] **Step 3: Re-run the new public-shell validator**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/integration/validate-video-analysis-core-location.ps1
```

Expected: PASS with `video-analysis-core public shell OK`.

- [ ] **Step 4: Verify the dogfood mirror**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1
```

Expected: PASS with `Dogfood mirror OK`.

- [ ] **Step 5: Verify the distribution surface**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/install/validate-distribution-surface.ps1
```

Expected: PASS with `Distribution surface OK`.

- [ ] **Step 6: Verify the repository layout**

Run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-layout.ps1
```

Expected: PASS with `Layout OK`.

- [ ] **Step 7: Commit the generated dogfood mirror**

```bash
git add .agents/skills/video-analysis-core
git commit -m "build: sync video-analysis-core dogfood mirror"
```

## Self-Review Checklist

- Spec coverage:
  - Public skill shell exists and is standalone.
  - Canonical output contract is duplicated inside the skill, not only in repo-level docs.
  - Machine-readable schema exists and matches the agreed top-level shape.
  - Repo guidance mentions the new skill.
- Dogfood mirror is refreshed and verified.
- Placeholder scan:
  - No placeholder markers or implicit "fill in later" text remains in the plan.
  - Every new file has concrete content.
  - Every verification step has an exact command and expected output.
- Type consistency:
  - `segment_id`, `event_id`, `evidence_id`, `actor_ref`, `slot_id`, `speaker_ref`, `speaker_role`, `source_type`, and `roi_hint.kind` use the same names across design doc, output contract, schema, and validator.
