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
  'assets\video-analysis-v0.schema.json'
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
- Interval ordering (`start_frame < end_frame`) and clip-bound checks (`end_frame <= clip_metadata.total_frames`) are semantic invariants for runtime outputs and are not fully enforced by this shell-only validator or schema package.

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
- metadata: `speaker_ref`, `speaker_role`, optional `actor_ref`, `text`, optional `language` (`string | null`), optional `source_subtype`

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

$expectedSchemaContent = @'
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
'@

$actualSkillContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'SKILL.md') -Raw)
$actualOutputContractContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'references\output-contract.md') -Raw)
$actualOpenAiYamlContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'agents\openai.yaml') -Raw)
$actualSchemaContent = Normalize-Content (Get-Content -LiteralPath (Join-Path $skillRoot 'assets\video-analysis-v0.schema.json') -Raw)

if ($actualSkillContent -ne (Normalize-Content $expectedSkillContent)) {
  throw 'Public video-analysis-core SKILL.md must match the exact public-shell contract'
}

if ($actualOutputContractContent -ne (Normalize-Content $expectedOutputContractContent)) {
  throw 'Public video-analysis-core output contract must match the exact published contract'
}

if ($actualOpenAiYamlContent -ne (Normalize-Content $expectedOpenAiYamlContent)) {
  throw 'Public video-analysis-core agents/openai.yaml must match the exact agent contract'
}

if ($actualSchemaContent -ne (Normalize-Content $expectedSchemaContent)) {
  throw 'Public video-analysis-core schema must match the exact published schema contract'
}

Write-Host 'video-analysis-core public shell OK'
