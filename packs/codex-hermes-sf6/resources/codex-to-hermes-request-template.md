# Codex-To-Hermes Request Template

Use this concise template when the target issue allows Hermes delegation.
Hermes output is draft input only.

```yaml
target_issue:
scope_summary:
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
- `scope_summary`: a short restatement of scope, non-goals, and acceptance.
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

Reference `workflows/codex-to-hermes-delegation.md` for the canonical
delegation workflow.
