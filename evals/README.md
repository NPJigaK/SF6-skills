# Evals

`evals/` is canonical for agent-agnostic answer-quality cases and rubrics.

Eval cases check answer mode, grounding, uncertainty, current-fact separation, patch sensitivity, and must-not-include behavior.

Eval score reports are answer-quality / regression observability artifacts,
not SF6 gameplay authority or normal public answer authority. The current
offline contract is `contracts/eval-score-report.schema.json`, with semantic
validation in `tests/validation/validate-eval-score-reports.ps1`.

Validate eval cases and score reports with:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-evals.ps1
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-eval-score-reports.ps1
```
