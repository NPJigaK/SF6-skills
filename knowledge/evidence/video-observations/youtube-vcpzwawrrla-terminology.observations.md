---
id: video-observation-youtube-vcpzwawrrla-terminology
title: YouTube VCPzwAwRrLA Commentary Terminology Observation
source_kind: reproducible_observation
source_role: commentary_only_terminology_observation
review_status: needs_review
review_after: "2026-08-14"
---

# YouTube VCPzwAwRrLA Commentary Terminology Observation

This artifact records sanitized observations from a commentary-only terminology
video. It is an observation artifact, not accepted strategy knowledge, and it
must not feed generated references without later review.

## Source

- Source metadata: `knowledge/sources/videos/youtube-vcpzwawrrla.md`
- Source URL: `https://www.youtube.com/watch?v=VCPzwAwRrLA`
- Accessed: 2026-05-14
- Observation method: no-cookie YouTube metadata access plus temporary
  auto-generated Japanese caption review in a repo-external scratch/cache
  location.
- Reviewed duration: full source structure by chapter, approximately 20:14.
- Raw media stored in repo: no.
- Full transcript stored in repo: no.

## Timestamped Observations

| Time | Observation kind | Visible observation | Speaker/commentary claim | Confidence | Notes |
|---|---|---|---|---|---|
| 00:46-02:01 | commentary terminology | Commentary chapter introduces `重ね`. | Source explains the term as timing an attack or special move against a waking opponent, and treats a failed overlap as a missed meaty timing. | medium | Review-only terminology candidate; confidence reflects broad topic identification from automatic captions, not exact definition wording. |
| 02:01-03:31 | commentary terminology | Commentary chapter introduces `めくり`. | Source explains the term through a jump attack that crosses or hits behind the opponent so the guard direction is reversed; it also connects the idea to cross-up wording. | medium | Stable glossary candidate, but source-local wording is not copied and exact wording remains needs_review. |
| 03:31-04:49 | commentary terminology | Commentary chapter introduces `すかし`. | Source frames it as withholding the expected jump attack and instead landing into another option such as a low or throw-like threat. | medium | Keep as terminology candidate; exact option coverage is context-dependent. |
| 04:49-06:50 | commentary terminology | Commentary chapter introduces `ライン`. | Source uses line to describe screen-position pressure: advancing the line pushes the opponent toward the corner, while retreating lowers the line. | medium | Strategy concept candidate; no exact screen-position rule is accepted. |
| 06:50-08:44 | commentary terminology | Commentary chapter introduces `グラップ`. | Source uses the term as throw escape / throw-tech wording in SF6 commentary and connects it to delayed throw-tech situations. | medium | Community terminology candidate; not official terminology authority. |
| 08:44-11:20 | commentary terminology | Commentary chapter introduces `シミー`. | Source explains shimmy as baiting an opponent's throw-tech / grapple response, making it whiff, and punishing it. | medium | Existing curated shimmy page was not modified; this row is review input only and caption-derived. |
| 11:20-14:44 | commentary terminology | Commentary chapter introduces `暴れ`. | Source frames the term as pressing an attack from a disadvantage or expected-block situation, such as wake-up or after guarding pressure. | medium | Exact advantage examples are held as current-fact-like and are not recorded as accepted values. |
| 14:44-16:06 | commentary terminology | Commentary chapter introduces `固め`. | Source explains it as using normals, specials, or pressure strings to make the defender hard to move, while noting SF6-specific pressure caveats. | medium | General concept candidate; SF6-specific pressure strength remains review-needed. |
| 16:06-18:01 | commentary terminology | Commentary chapter introduces `キャンセル`. | Source explains cancel as cutting off the later recovery of one action, especially a normal, into another action such as a special. | medium | Stable terminology candidate; move-specific cancelability remains current fact and exact wording remains needs_review. |
| 18:01-20:14 | commentary terminology | Commentary chapter introduces `リーサル`. | Source explains lethal as an option or combo that can finish the opponent from the current life total. | medium | Stable concept candidate; exact route kill thresholds are current or matchup facts. |

## Caption Review Provenance And Limits

- Caption provenance: auto-generated. `yt-dlp --list-subs` reported no
  uploaded/manual subtitles and available automatic captions for this source.
- Direct audio reviewed? no.
- Direct video reviewed? no.
- Content execution depth: `caption_level_content_review`.
- Timestamped observations are paraphrased from temporary caption-level review
  plus chapter metadata; raw captions and transcript-like text are not
  committed.
- Automatic caption errors may affect Japanese terminology extraction,
  especially source-local wording, speaker nuance, and homophones.
- Confidence values mean confidence in broad chapter/topic identification and
  paraphrased concept extraction, not official definition accuracy or exact
  source wording.
- Terms requiring exact wording, official terminology authority, or
  move/system-specific claims remain `needs_review`.

## Contract-Shaped Observation Payload

This payload follows the shape of `contracts/video-observation.schema.json` at a
coarse commentary-review level. Segment text is paraphrased; no full transcript
or raw captions are stored.

```json
{
  "schema_version": "2.0.0",
  "clip_metadata": {
    "clip_id": "youtube-vcpzwawrrla-terminology-review",
    "source_fps": null,
    "normalized_fps": 60,
    "total_frames": 72840
  },
  "actor_bindings": [
    {
      "actor_ref": "actor_a",
      "character_slug": null,
      "binding_confidence": 0.0,
      "binding_basis": [
        "commentary-only source; no gameplay actor binding accepted"
      ]
    },
    {
      "actor_ref": "actor_b",
      "character_slug": null,
      "binding_confidence": 0.0,
      "binding_basis": [
        "commentary-only source; no gameplay actor binding accepted"
      ]
    }
  ],
  "segments": [
    {
      "segment_id": "seg-terminology-0001",
      "track": "transcript",
      "kind": "term_meaty_source_claim",
      "start_frame": 2760,
      "end_frame": 7260,
      "confidence": 0.62,
      "summary": "Source-derived `重ね` explanation candidate.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-vcpzwawrrla.md"
      ]
    },
    {
      "segment_id": "seg-terminology-0002",
      "track": "transcript",
      "kind": "term_crossup_source_claim",
      "start_frame": 7260,
      "end_frame": 12660,
      "confidence": 0.65,
      "summary": "Source-derived `めくり` explanation candidate.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-vcpzwawrrla.md"
      ]
    },
    {
      "segment_id": "seg-terminology-0003",
      "track": "transcript",
      "kind": "term_shimmy_source_claim",
      "start_frame": 31440,
      "end_frame": 40800,
      "confidence": 0.65,
      "summary": "Source-derived `シミー` explanation candidate.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-vcpzwawrrla.md"
      ]
    },
    {
      "segment_id": "seg-terminology-0004",
      "track": "transcript",
      "kind": "term_cancel_and_lethal_source_claim",
      "start_frame": 57960,
      "end_frame": 72840,
      "confidence": 0.62,
      "summary": "Source-derived `キャンセル` and `リーサル` explanation candidates.",
      "evidence_refs": [
        "knowledge/sources/videos/youtube-vcpzwawrrla.md"
      ]
    }
  ],
  "derived_events": [
    {
      "event_id": "event-terminology-0001",
      "kind": "commentary_only_terminology_extraction_seed",
      "source_segment_ids": [
        "seg-terminology-0001",
        "seg-terminology-0002",
        "seg-terminology-0003",
        "seg-terminology-0004"
      ]
    }
  ]
}
```

## Boundary Notes

- These are review-only observations.
- They are based on caption-level content review, not direct audio/video review.
- The extracted terminology candidates are not accepted current facts.
- Commentary definitions are source-derived review input, not official
  terminology authority.
- Exact frame advantage, guaranteed setup validity, and move-specific
  cancelability are held for separate verification.
- No raw media, frames, screenshots, contact sheets, full captions, or full
  transcript are stored in the repository.
