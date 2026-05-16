# Codex-To-Hermes Request Template

Use this concise template when the target issue allows Hermes delegation.
Hermes output is draft input only. For Hermes-first analysis, it is the
primary draft input.

```yaml
analysis_mode: hermes_primary
target_issue:
target_scope_summary:
codex_app_role:
  - hermes_operator
  - boundary_auditor
  - artifact_converter
  - validator_executor
hermes_role:
  - primary_analyst
  - orchestrator
provider_codex_role:
  - executor
source_material:
requested_artifact_type:
allowed_outputs:
forbidden_outputs:
authority_boundaries:
validators_to_run:
review_checklist:
```

## Field Guidance

- `target_issue`: the GitHub issue controlling scope and acceptance.
- `target_scope_summary`: a short restatement of scope, non-goals, and
  acceptance.
- `analysis_mode`: usually `hermes_primary`; use `codex_fallback` only when
  Hermes is unavailable, unconfigured, explicitly out of scope, or unsafe for
  the material.
- `codex_app_role`: Windows Codex app responsibilities. It operates Hermes,
  audits boundaries, converts artifacts, runs validators, and reports to the
  maintainer.
- `hermes_role`: Hermes responsibilities. Hermes performs primary analysis,
  orchestration, uncertainty integration, and self-improvement review.
- `provider_codex_role`: provider Codex responsibilities when Hermes uses it.
  Provider Codex is an executor, not the final analyst.
- `source_material`: repo artifacts, links, notes, article/video references,
  or other input. Source material is not automatically canonical.
- `requested_artifact_type`: draft note, candidate observation, review
  checklist, validator proposal, or other scoped draft.
- `allowed_outputs`: what Hermes may produce as draft input.
- `forbidden_outputs`: exact current facts, public answer behavior, raw
  article/video dumps, local state, secrets, or out-of-scope artifacts.
- `authority_boundaries`: current-fact, article, video, external visual atlas,
  and public adapter boundaries that apply.
- `validators_to_run`: repo validators Codex must run before commit.
- `review_checklist`: checks Codex must perform before using the draft.

Use this fallback shape only when Hermes-first analysis cannot be used:

```yaml
analysis_mode: codex_fallback
hermes_delegation:
  attempted: false
  reason:
debt: hermes_first_analysis_not_validated_for_this_workflow
```

Reference `workflows/codex-to-hermes-delegation.md` for the canonical
delegation workflow.
