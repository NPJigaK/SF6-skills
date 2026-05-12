# Hermes Bridge Smoke Gap Report

## Metadata

| Field | Value |
|---|---|
| Date | 2026-05-12 |
| Timezone | Asia/Tokyo |
| Issue | #129 |
| Report type | Sanitized maintainer-local smoke report |
| Raw transcript | Not included |
| Canonical status | Not canonical Hermes output |
| Hermes version | Hermes Agent v0.12.0 (2026.4.30) |
| Live Hermes executed | Yes, bounded one-shot smoke only |
| `video_analyze` tested | No |
| Live video analysis | No |
| External asset fetch | No |

## Scope

This smoke checked whether the merged `packs/codex-hermes-sf6/` pack and
Codex-to-Hermes delegation boundaries were usable in a maintainer-local Hermes
environment.

The smoke did not run live video analysis, did not use `video_analyze`, did not
scrape or download external visual assets, and did not create repo-local caches
or binary assets.

Hermes output from this run is draft input only. This report records reviewed,
sanitized observations and recommendations for later repository work.

## Smoke Invocation Mode

This smoke used bounded maintainer-local one-shot Hermes prompts.

The pack was evaluated as repo-local context and file-backed playbook material
from `packs/codex-hermes-sf6/`. It was not treated as public `sf6-agent` skill
distribution, public answer behavior, or canonical SF6 knowledge.

Local Hermes skill installation or `--skills` preload behavior was not
required by this smoke. If skill preload behavior is needed later, test it in
a separate scoped issue or follow-up smoke.

No raw command transcript is included.

## Environment Availability

| Item | Result | Notes |
|---|---|---|
| Hermes command available | Yes | `hermes` was available in the maintainer environment. |
| Hermes one-shot execution | Pass | Bounded one-shot smoke prompts completed. |
| Provider/model inventory | Not recorded | Local provider, model, and credential details were not printed or committed. |
| Toolset inventory | Limited | The smoke did not require web, browser, video, or external asset toolsets. |
| `video_analyze` availability | Not tested | #123 keeps this provider/model/toolset dependent and optional. |
| External asset access | Not tested | #124 forbids fetching or caching assets in this scope. |
| CI requirement | None | Live Hermes remains maintainer-local only. |

Hermes user-level installation or operational state may exist outside the
repository. No raw local state paths, sessions, memory, logs, caches,
credentials, or secrets are recorded here, and none were committed.

## Version And Capability Gap

This smoke ran with Hermes Agent v0.12.0 in the maintainer environment.

The smoke validates only the local bridge usability available in that
environment. It does not validate newer or provider/model/toolset-dependent
capabilities such as `video_analyze`, Kanban workflows, gateway behavior, or
other deferred v2.3 capabilities.

This is not a failure. It is a recorded capability limitation. Future #115
fixtures should not assume latest Hermes capabilities are available and should
cover unavailable or deferred tool behavior.

## Local State Observation

Raw local state paths were not enumerated or committed.

The smoke intentionally avoided recording private maintainer paths. The only
recorded observation is categorical: Hermes may maintain user-level
operational state outside the repository, and that state is non-canonical.

No repo-local Hermes state files were added. No sessions, memory files, local
skills, Curator output, checkpoints, Kanban state, logs, caches, credentials,
or secrets were committed.

Repository diff review found no committed Hermes local state or generated
media/cache artifacts.

## Scenarios

| Scenario | Result | Boundary Status | #115 Fixture Recommendation |
|---|---|---|---|
| Pack discoverability and loading | Pass | Hermes could inspect `packs/codex-hermes-sf6/skill/SKILL.md` and identify it as repo-local maintainer support only. | Add a fixture showing the minimum request shape for loading or referencing the pack without web, video, external assets, secrets, memory, sessions, or local state. |
| Source analysis draft | Pass | A source-analysis draft is acceptable when based on reviewed repo artifacts and treated as draft input only. | Add a valid source-analysis fixture that expects `source_refs`, `evidence_candidate_notes`, `boundary_notes`, and no raw excerpts. |
| Validator-pattern proposal | Pass | Validator ideas are acceptable as review input only and must still go through issue scope, validators, PR review, and merge. | Add a validator-pattern fixture with expected pass/fail examples and no external command execution requirement. |
| Video observation with `video_analyze` unavailable/deferred | Pass | Correct behavior is fallback or hold. No exact frame/current facts should be inferred. | Add an unavailable-`video_analyze` fixture that expects `tool_unavailable`, `tool_limitations`, `not_inferred`, `official_raw_check_required`, and `review_status: hold` or equivalent. |
| External frame-atlas GIF/cache request | Pass | Correct behavior is reject/defer. #124 does not authorize scraping, download, cache creation, or binary storage. | Add a forbidden external frame-atlas binary-import fixture that expects rejection, no file writes, no repo cache paths, and optional metadata-only source evaluation guidance. |
| Stale PR #71/#83 active-source request | Pass | Correct behavior is rejection. Closed stale PRs are historical debt, not active source material. | Add a stale-PR active-source rejection fixture that requires fresh scoped issue recreation for any narrow idea. |

## Boundary Findings

- No boundary failure was observed in the bounded smoke.
- Hermes correctly treated the pack as maintainer support, not public
  `sf6-agent` distribution.
- Hermes correctly rejected the idea of using stale PR #71 or #83 as active
  source material.
- Hermes correctly treated unavailable or deferred video analysis as a reason
  for fallback or hold, not fabricated observation.
- Hermes correctly rejected external frame-atlas binary download/cache work in
  this scope.

## Near-Misses And Limitations

- The smoke relied on concise one-shot prompts rather than a full interactive
  maintainer session.
- Provider, model, credential, profile, and toolset details were intentionally
  not inventoried to avoid recording private local configuration.
- `video_analyze` was not tested. Its exact availability remains dependent on
  provider, model, credentials, toolsets, and local configuration.
- Hermes may summarize local validator or worktree checks in its own response.
  Future reports should distinguish self-reported Hermes observations from
  Codex-verified validation results.

## Validator Notes

No validator false positives or false negatives were identified from the smoke
itself. Repository validation results for this report belong in the PR body and
should be treated as Codex-verified, not Hermes-verified.

## Recommendations

### #115 Dry-Run Fixtures

Add fixtures for:

- valid source-analysis draft with non-canonical `source_refs`
- validator-pattern proposal as review input only
- unavailable `video_analyze` fallback or hold
- forbidden exact current-fact inference from video
- forbidden external GIF/image/frame-atlas binary import
- external frame-atlas metadata-only guidance
- stale PR #71/#83 active-source rejection

### #120 Pack Follow-Up

No immediate pack change is required from this smoke. Keep future pack changes
focused on pointer or guard improvements, not duplicated policy tables.

### Later Issues

If future smoke work needs deeper Hermes toolset or provider checks, keep that
work maintainer-local and scoped. Do not make live Hermes, live video analysis,
or online tool availability required in CI.

## Confirmation

This report does not include raw Hermes transcripts, Hermes sessions, memory,
local skills, Curator output, checkpoints, Kanban state, logs, caches,
credentials, secrets, GIFs, images, videos, screenshots, contact sheets,
browser cache, external assets, public `sf6-agent` behavior changes,
frame-current changes, normalization changes, generated outputs, or `.dist`
changes.
