# JP Combo Notation Contract Review Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-04 |
| Issue | #80 |
| Fixture | `evals/fixtures/combo-damage/jp-ryusei-nyfngnzjv3m.yaml` |
| Contract | `contracts/combo-notation.md` |
| Source video | `https://www.youtube.com/watch?v=nyFNgnzjV3M` |
| Raw media inspected | no new media inspection |
| Generated references changed | no |
| Frame-current assets changed | no |

## Review Method

This run re-reviewed existing disabled combo damage fixture candidates against `contracts/combo-notation.md`.

No new source video was inspected. No raw video, frames, screenshots, contact sheets, browser cache, or transcript files were created or stored.

## Contract Verdicts

| Case | Previous status | Verdict | Reason |
|---|---|---|---|
| `jp-basic-light-stribog-001` | enabled | keep enabled | Exact starter and route order remain clear enough for the current fixture layer. |
| `jp-basic-light-rush-extension-1482` | disabled | keep disabled | Alternative branches and unresolved normalized notation block enabled status. |
| `jp-basic-light-rush-extension-1527` | disabled | keep disabled | Higher-damage branch is plausible but still inferred. |
| `jp-mid-rush-triglav-1824` | disabled | keep disabled | Generic `medium_normal` starter is not precise enough. |
| `jp-mid-rush-od-triglav-3260` | disabled | keep disabled | Generic starter plus inherited OD follow-up context blocks enabled status. |
| `jp-mid-corner-carry-rush-fhk-2763` | disabled | keep disabled | Generic starter, corner-carry context, and delayed `Drive Rush 6HK` timing remain unresolved. |
| `jp-mid-position-carry-1484` | disabled | keep disabled | Route overlay is incomplete and position/carry context is unresolved. |

## Boundaries

- Observed damage remains eval oracle material only.
- No case was promoted to curated knowledge.
- No disabled case was enabled.
- No damage calculator was added.
- No damage-hidden eval runner was added.
- No generated references were updated.

## Findings

- The existing enabled seed remains acceptable under the current fixture-layer notation contract.
- The disabled candidates are blocked by notation specificity, not damage label visibility.
- The next enabling work requires exact starter/branch/timing review or a future damage calculation input contract.

## Verification

- `tests/validation/validate-combo-damage-fixtures.ps1`: pass.
- `tests/validation/validate-ingest-artifacts.ps1`: pass.
- `tests/validation/validate-doc-links.ps1`: pass.
- `tests/validation/run-all.ps1`: pass.
- `git diff --check`: pass.
- Generated output status check: clean.
- Repo-local media/state scan: no hits.
- Changed-file sensitive-material scan: no hits.
