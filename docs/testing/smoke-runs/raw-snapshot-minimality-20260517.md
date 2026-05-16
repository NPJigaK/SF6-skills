# Raw Snapshot Minimality Report 20260517

## Metadata

| Field | Value |
|---|---|
| analysis_mode | `hermes_primary` |
| target_issue | `#203` |
| date | `2026-05-17` |
| timezone | `Asia/Tokyo` |
| report_type | `raw_snapshot_minimality_handoff` |
| raw_transcript_committed | no |
| hermes_local_state_committed | no |
| public_adapter_behavior_changed | no |
| current_facts_changed | no |
| generated_or_runtime_assets_changed | no |

## Check Method

The raw snapshot keep set is derived from
`data/exports/<character_slug>/snapshot_manifest.json`.

For every dataset with `publication_state = available`:

- `official_raw` references `data/raw/official/<character_slug>/<snapshot_id>/`
- `derived_metrics` references `data/raw/official/<character_slug>/<snapshot_id>/`
- `supercombo_enrichment` references `data/raw/supercombo/<character_slug>/<snapshot_id>/`

The reference check compares those manifest-derived paths with Git-tracked
snapshot directories under `data/raw/official/` and `data/raw/supercombo/`.

## Pre-Cleanup Result

Hermes primary analysis reported:

| Metric | Value |
|---|---:|
| tracked raw snapshot directories | 62 |
| manifest-referenced raw snapshot directories | 58 |
| unreferenced tracked raw snapshot directories | 4 |
| missing referenced raw snapshot directories | 0 |

The four Issue `#203` candidates remained unreferenced:

- `data/raw/supercombo/jp/20260310T023617Z-3b8fa28a`
- `data/raw/supercombo/luke/20260412T151204Z-d96c657b`
- `data/raw/supercombo/ryu/20260412T204407Z-384b6831`
- `data/raw/supercombo/sagat/20260412T214225Z-af77c139`

## Policy Decision

Checked-in raw snapshots are reproducibility input only, not public-answer
evidence. The durable checked-in raw surface should contain the minimum raw
snapshots needed to reproduce current published exports.

Unreferenced checked-in raw snapshots are removable residue unless a reviewed
retention-exception artifact explicitly allows them. No retention exception is
being introduced for the four unreferenced SuperCombo snapshots above.

The validator added with this report is CI-failing rather than warning-only:

- missing referenced snapshots break reproducibility of published exports
- unreferenced snapshots violate the documented minimal checked-in raw surface
- the four known unreferenced snapshots are removed with the same change, so a
  strict baseline is available

## Boundary Audit

| Boundary | Status | Notes |
|---|---|---|
| Target issue scope | pass | Work is limited to raw snapshot minimality for issue `#203`. |
| Current facts | pass | No `data/exports/`, `data/roster/`, move facts, or gameplay facts changed. |
| Public adapter behavior | pass | No `skills/sf6-agent/` behavior changed. |
| Generated/runtime assets | pass | No generated references, frame-current assets, normalization assets, or `.dist` outputs changed. |
| Raw Hermes transcript/state | pass | Not committed. |
| Raw data fetch | pass | No new raw data was fetched. |

## Committed Artifact Decision

This change removes only the four unreferenced tracked SuperCombo raw snapshot
directories listed above. The current published manifests already reference
newer SuperCombo snapshots for those characters, and the removed directories do
not contribute to the current manifest-derived keep set.
