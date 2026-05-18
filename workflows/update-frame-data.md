# Update Frame Data Workflow

Use this workflow when a maintainer refreshes current-roster frame data after an official balance patch, battle change list update, frame-page change, or roster-source change.

This is a repository maintainer procedure. It is not a public answer policy and it does not replace the exact current-fact authority in `data/exports/` and `data/roster/`.

## Authority And Scope

- Current roster source: `data/roster/current-character-roster.json`
- Published exact current-fact source: `data/exports/<character_slug>/`
- Primary derived runtime asset target: `runtime/frame-current/`
- Compatibility copy while the public adapter remains: `skills/sf6-agent/assets/frame-current/`
- Runtime asset contract: `contracts/frame-current-runtime-assets.md`
- Ingestion implementation: `ingest/frame_data/`

Do not use raw snapshots, normalized intermediates, CSV sidecars, or manual-review outputs as final public-answer evidence.

## Patch Metadata Rules

Patch names, patch dates, update labels, and battle-change wording are current facts. Verify them from official CAPCOM pages before using them in reports, commit messages, pull request titles, or user-facing summaries.

Prefer official sources in this order:

1. CAPCOM update or information page for the patch.
2. CAPCOM battle change list page with an explicit update label.
3. CAPCOM frame pages that visibly show the update label.

Search snippets and third-party summaries may help find an official page, but they are not final evidence for patch metadata.

Use exact absolute labels such as `2026.03.17 update` when verified. If no official label or date can be verified, continue only with neutral wording and mark the patch metadata as unverified.

## Execution Flow

1. Record the official patch source URL, access time, and exact patch label or note that metadata is unverified.
2. Check the worktree state with `git status --short --branch`.
3. Read `data/roster/current-character-roster.json` and preserve its character order for all update and reporting steps.
4. From `ingest/frame_data/`, run ingest for every roster character.
5. Use `--source all` when the roster entry has `sources.supercombo_data`; otherwise use `--source official` for that character only.
6. Read `data/exports/<character_slug>/snapshot_manifest.json` for every roster character.
7. Record each dataset state separately from the manifest, including `publication_state`, `published_run_id`, `published_snapshot_ids`, `published_record_count`, and `withheld_review_count`.
8. Rebuild frame-current runtime assets so the primary target is `runtime/frame-current/` and the legacy adapter compatibility copy is refreshed.
9. Dry-run raw snapshot pruning for every roster character.
10. Confirm pruning keeps the minimum raw snapshots needed to reproduce the current published exports.
11. Apply pruning only after the dry-run output has been reviewed.
12. Validate that every checked-in raw snapshot directory is referenced by the current published manifests.

## Commands

Run from `ingest/frame_data/`:

```powershell
$roster = Get-Content -Raw ..\..\data\roster\current-character-roster.json | ConvertFrom-Json

foreach ($character in $roster.characters) {
  $sourceMode = if ($null -ne $character.sources.supercombo_data) { 'all' } else { 'official' }
  python -m sf6_ingest.cli run --character $character.character_slug --source $sourceMode
}

foreach ($characterSlug in $roster.characters.character_slug) {
  python -m sf6_ingest.cli prune --character $characterSlug --dry-run --verbose
}

foreach ($characterSlug in $roster.characters.character_slug) {
  python -m sf6_ingest.cli prune --character $characterSlug --apply --verbose
}
```

Run from the repo root:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1
```

The builder output must satisfy these v2 values:

- primary `asset_root = runtime/frame-current`
- compatibility `asset_root = skills/sf6-agent/assets/frame-current`
- `source_root = data/exports`
- `roster_source = data/roster/current-character-roster.json`

## Verification

Before reporting the refresh as complete, run the validation commands that match the v2 surfaces:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-roster-source.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-raw-snapshot-minimality.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-frame-current-assets.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-current-fact-boundaries.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-v2-surfaces.ps1
```

Read the full output and confirm every command exits with code `0`.

Raw snapshot minimality is a strict data hygiene check. Unreferenced checked-in
raw snapshots are removable residue unless a reviewed retention-exception
artifact is explicitly introduced. Missing referenced raw snapshots break
reproducibility and must be fixed before reporting the refresh as complete.
ADR-0005 records this boundary:
`docs/architecture/decisions/0005-raw-snapshot-retention.md`. Broader raw-cache
or raw-history storage stays repo-external unless a later reviewed artifact
contract is introduced.

## Reporting

Report in roster order from `data/roster/current-character-roster.json`.

For each character, include:

- `character_slug`
- each dataset `publication_state`
- changed `published_run_id`
- changed `published_snapshot_ids`
- any nonzero `withheld_review_count`
- any configured supplemental source that could not publish

Separate official-published updates from supplemental enrichment updates. Do not collapse the roster into a single success statement if one character or dataset retained old published output, became unavailable, or produced manual-review rows.

## Commit And Pull Request Wording

Use verified official patch metadata only when it was confirmed from an official source.

Examples:

- `Update current-roster frame data for 2026.03.17 update`
- `Refresh current-roster frame data from official battle change list`

If patch metadata is unverified, use neutral wording:

- `Update current-roster frame data`

Never use a patch label or date that came only from a search snippet, old local note, or third-party summary.
