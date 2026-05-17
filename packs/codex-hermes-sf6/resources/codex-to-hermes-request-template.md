# Codex-To-Hermes Request Template

This is a fill-in template only. Canonical delegation procedure lives in
`workflows/codex-to-hermes-delegation.md`, with boundary policy in
`docs/architecture/codex-hermes-bridge-policy.md`.

Hermes output is draft input only. For Hermes-first analysis, it is the
primary draft input.

```yaml
analysis_mode: hermes_primary
task_id:
tracking_issue:
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

## Minimal Field Notes

- `target_issue`: issue controlling scope and acceptance.
- `target_scope_summary`: one short scope / non-goal / acceptance restatement.
- `source_material`: repo refs or source refs; not automatically canonical.
- `forbidden_outputs`: include local state, raw transcript, secrets, exact
  current facts, and public answer behavior unless explicitly in scope.
- `authority_boundaries`: current-fact, article/video, visual-asset,
  calculation, and public-adapter boundaries that apply.
- `validators_to_run`: checks Codex must run before commit.

Use this fallback shape only when Hermes-first analysis cannot be used:

```yaml
analysis_mode: codex_fallback
hermes_delegation:
  attempted: false
  reason:
debt: hermes_first_analysis_not_validated_for_this_workflow
```

Fallback rules, provider Codex boundaries, and post-delegation checks are
defined by `workflows/codex-to-hermes-delegation.md`.
