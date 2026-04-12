---
name: update-frame-data
description: Use when a maintainer asks to refresh the current-roster frame-data after an official balance patch, battle change list update, or frame-page change in this repository. Use for the full maintainer workflow: verify the official patch label/date first, load the canonical roster, run ingest for every character, rebuild published runtime assets, prune backing raw snapshots, verify outputs, and prepare accurate reporting or commit wording without guessing patch metadata.
---

Repository-only workflow for patch-driven frame-data refreshes.

## Scope

- Use this when the user says things like `調整入ったから更新して`, `全キャラのデータ更新して`, `roster 全部更新して`, or `バトル変更リスト対応で更新して`.
- Use this for maintainer operations in this repository only.
- Do not use this for public distribution skills, concept answers, or current-fact lookup answers.
- Do not use this for knowledge curation; that belongs to `maintainer-skills/sync-knowledge/`.

## Hard Rules

- Patch names, patch dates, `update` labels, and battle-change wording are current facts. Treat them like any other current fact.
- Verify patch metadata from `T1` before you write summary prose, user-facing explanations, commit messages, or PR titles.
- Search snippets and third-party articles may help locate an official page, but they are never the final source for patch metadata.
- Use exact absolute dates such as `2026.03.17 update`. Do not rely on relative wording like `latest`, `today`, or `the recent patch`.
- If the official patch label/date cannot be confirmed, continue only with neutral factual wording and mark the patch label/date as `[保留]`. Do not guess.

## T1 Sources For Patch Metadata

Prefer these in order:

1. Official CAPCOM update / information page for the patch
2. Official battle change list page with the explicit update label
3. Official frame pages that visibly show `Battle Change List Updated ...`

If none of the above can be verified directly, patch metadata is not verified.

## Execution Flow

1. Confirm the official patch label/date from `T1`.
2. Read `shared/roster/current-character-roster.json` and treat its character order as the canonical update order.
3. Check the current worktree state with `git status --short`.
4. For each roster character:
   - use `--source all` when `sources.supercombo_data` is configured for that character
   - otherwise use `--source official`
5. Read `data/exports/<character_slug>/snapshot_manifest.json` for every roster character.
6. Record each dataset state separately: `published`, `retained_last_known_good`, `unavailable`, or `not_selected`.
7. Rebuild frame-current runtime assets:
   - `powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1`
8. Sync the dogfood mirror after the build finishes:
   - `powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1`
9. Do not run steps 7 and 8 in parallel. Build must finish before mirror sync starts.
10. Run prune in `--dry-run --verbose` mode for every roster character.
11. Confirm prune keeps the current published exports and only the minimum raw snapshots needed to reproduce them.
12. Apply prune for every roster character.

## Commands

Run from `ingest/frame_data/`:

```powershell
$roster = Get-Content -Raw ..\..\shared\roster\current-character-roster.json | ConvertFrom-Json

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
powershell -ExecutionPolicy Bypass -File packages/skill-packaging/build-frame-current-runtime-assets.ps1
powershell -ExecutionPolicy Bypass -File scripts/dev/sync-dogfood-skills.ps1
```

## Verification

Before claiming success or creating a commit, run:

```powershell
powershell -ExecutionPolicy Bypass -File tests/packaging/validate-frame-current-runtime-assets.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-kb-sf6-frame-current-location.ps1
powershell -ExecutionPolicy Bypass -File tests/integration/validate-frame-current-boundary.ps1
powershell -ExecutionPolicy Bypass -File tests/install/validate-dogfood-mirror.ps1
```

Read the full output and confirm exit code `0` for all four.

## Reporting Rules

- Report every roster character separately.
- Use roster order from `shared/roster/current-character-roster.json`.
- Include exact `published_run_id` and `published_snapshot_ids` when they changed.
- Explicitly call out any dataset that stayed on `retained_last_known_good`.
- Distinguish official-published updates from supplemental enrichment updates.
- Call out characters where `supercombo_enrichment` stayed `not_selected` because no supplemental source is configured.
- If patch metadata is unverified, say that clearly and do not decorate the update with a guessed label.

## Commit Message Rules

- If the official patch label/date is verified from `T1`, use it in the commit subject.
- Prefer the exact official label when available, for example:
  - `2026.03.17 updateのバトル変更リスト対応で全キャラのフレームデータを更新`
  - `Ver.2.300のバトル変更リスト対応で現行rosterのフレームデータを更新`
- If `T1` verification fails, use a neutral factual subject:
  - `現行rosterのフレームデータを更新`
- Never use a patch label/date taken only from stale search snippets or third-party summaries.

## Common Mistakes

- Inferring the patch date from search-engine snippets
- Reusing an older patch label because the frame page changed recently
- Treating commit wording as exempt from source verification
- Running runtime-asset build and dogfood sync in parallel
- Reporting the whole roster as fully updated when one or more characters stayed on last-known-good
- Forgetting that some characters may be official-only and should be run with `--source official`
