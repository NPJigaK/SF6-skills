# sf6-agent Smoke Run: Codex CLI

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-01 |
| Agent | Codex CLI 0.128.0-alpha.1 |
| Model | gpt-5.5 |
| Bundle source | `.dist/sf6-agent-bundle.zip` |
| Commit | `1c0a9b77fb0bf66da78c5403b62c0af2ec91df32` |
| Extracted adapter root | `/tmp/sf6-agent-smoke-aNq80u/sf6-agent` |
| Full repo checkout visible | no |

## Method

The release bundle was built with `tests/validation/run-all.ps1`, extracted to a temporary directory, and tested with Codex CLI using the extracted `sf6-agent/` directory as the working root.

The smoke prompt instructed the agent to use only the packaged adapter surface:

- `SKILL.md`
- `references/answer-policy.md`
- `references/current-fact-policy.md`
- `references/uncertainty-policy.md`
- `references/generated-*`
- `assets/frame-current/`

The prompt explicitly denied access to `knowledge/`, `data/exports/`, `data/roster/`, `contracts/`, and `workflows/`. Exact current values were not pasted into this report.

## Results

| Case | Expected mode | Observed mode | Result | Notes |
|---:|---|---|---|---|
| 1 | `stable_concept` | `stable_concept` | Pass | Generated concept references were used for stable concept grounding; no exact frame lookup was needed. |
| 2 | `stable_concept` | `stable_concept` | Pass | The answer boundary separated frame advantage from guaranteed follow-up claims. |
| 3 | `stable_concept` | `stable_concept` | Pass | Shimmy was treated as community terminology, not official wording. |
| 4 | `stable_concept` | `stable_concept` | Pass | Hit confirm was treated as a stable concept; routes and windows were kept as separate current or strategy claims. |
| 5 | `stable_concept` | `stable_concept` | Pass | Meaty timing was treated as a concept; exact wake-up setups were kept behind current verification. |
| 6 | `verified_current_fact` | `verified_current_fact` | Pass | Luke was packaged and the requested block field was present in the official packaged row. Exact value withheld. |
| 7 | `verified_current_fact` | `verified_current_fact` | Pass | Luke's packaged official row contained both requested fields. Exact values withheld. |
| 8 | `unresolved_or_hold` | `unresolved_or_hold` | Pass | A character outside packaged roster/assets could not be verified. |
| 9 | `verified_current_fact` | `verified_current_fact` | Pass | `official_raw` was treated as controlling authority; supplemental enrichment was not allowed to override it. |
| 10 | `unresolved_or_hold` | `unresolved_or_hold` | Pass | A missing dataset was treated as a hold condition; no repo-local maintenance was assumed. |
| 11 | `unresolved_or_hold` | `unresolved_or_hold` | Pass | The setup was treated as underspecified and patch-sensitive. |
| 12 | `unresolved_or_hold` | `unresolved_or_hold` | Pass | A video anecdote alone was not promoted to general strategy knowledge. |
| 13 | `unresolved_or_hold` | `unresolved_or_hold` | Pass | Conflicting third-party current facts without packaged frame-current assets were held. |

## Findings

- Packaged-surface behavior matched the expected modes for all 13 cases.
- Exact current frame answers stayed limited to `assets/frame-current/`, with `official_raw` as controlling source.
- Generated references were used for stable concept grounding only, not canonical exact current data.
- Missing, conflicting, underspecified, or non-packaged current facts were held.

## Follow-ups

- None required for this smoke run.

