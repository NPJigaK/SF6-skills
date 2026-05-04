# JP Combo Branch Mapping Review Smoke Run

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-04 |
| Issue | #82 |
| Fixture | `evals/fixtures/combo-damage/jp-ryusei-nyfngnzjv3m.yaml` |
| Contract | `contracts/combo-notation.md` |
| Source video | `https://www.youtube.com/watch?v=nyFNgnzjV3M` |
| Re-inspected scope | existing fixture candidate sections only, approximately `00:31-02:00` |
| Generated references changed | no |
| Frame-current assets changed | no |

## Review Method

This run re-inspected the existing disabled JP combo damage oracle fixture candidates to see whether exact starter, branch, OD follow-up, or timing context could be resolved enough to enable additional damage-hidden eval cases.

Temporary section media and sparse still frames were generated only in repo-external scratch. No new source video or broad coverage chapter was added.

## Re-Review Verdicts

| Case | Verdict | Reason |
|---|---|---|
| `jp-basic-light-rush-extension-1482` | keep disabled | Damage label and alternative-branch overlay are visible, but branch-to-damage mapping remains unresolved. |
| `jp-basic-light-rush-extension-1527` | keep disabled | Crouching-medium-punch branch remains plausible, but exact branch mapping is still inferred. |
| `jp-mid-rush-triglav-1824` | keep disabled | Generic `中攻撃` starter could not be safely mapped to an exact starter token. |
| `jp-mid-rush-od-triglav-3260` | keep disabled | OD follow-up wording is clearer, so notation was refined to `OD Triglav > Triglav`, but the route still inherits generic starter context. |
| `jp-mid-corner-carry-rush-fhk-2763` | keep disabled | Delayed `Drive Rush 6HK` wording is confirmed, but timing semantics and generic starter remain unresolved. |
| `jp-mid-position-carry-1484` | keep disabled | The damage label remains visible, but a complete route overlay was not available. |

## Boundaries

- Observed damage remains eval oracle material only.
- No case was promoted to curated knowledge.
- No disabled case was enabled.
- No damage calculator was added.
- No damage-hidden eval runner was added.
- No generated references were updated.
- No frame-current assets were updated.
- Raw video, frames, screenshots, contact sheets, browser cache, and full transcript were not stored in the repository.

## Findings

- The main blocker remains notation specificity, not damage label visibility.
- `1482` and `1527` are still not safe enabled cases because the route branch remains unresolved.
- `medium_normal` candidates remain blocked until exact starter review maps them to exact move tokens.
- The OD Triglav candidate can carry a clearer disabled normalized route, but inherited generic starter context still blocks enabled status.

## Repo Boundary And Cleanup

- Repo-external scratch was used for temporary section media and still-frame inspection.
- Scratch cleanup: done.
- Repo-local media/state scan: no hits.

## Verification

- `tests/validation/validate-combo-damage-fixtures.ps1`: pass.
- `tests/validation/validate-video-artifacts.ps1`: pass.
- `tests/validation/validate-doc-links.ps1`: pass.
- `tests/validation/run-all.ps1`: pass.
- `git diff --check`: pass.
- Generated output status check: clean.
- Changed-file sensitive-material scan: no hits.
