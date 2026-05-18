# Evidence Gate Contract

This contract defines evidence boundaries for answer orchestration. It is a repo-level policy surface, not an operational Hermes prompt.

## Current Facts

Exact current move facts must be grounded in packaged frame-current authority. The exact current fact runtime surface is `runtime/frame-current/published/*/official_raw.json`, which is derived from `data/exports/` and `data/roster/`.

`derived_metrics` may support calculations only when the route is anchored to `official_raw`. Derived metrics are not an independent source for exact current move facts.

Generated concept references must not be used as exact current frame-value authority. They may support stable concepts, terminology, and strategy context after their source boundary is respected.

## Review And Observation Boundaries

Review claims and video observations must not become final answer authority without review and promotion through the canonical repository workflow.

Video observations are observation-only evidence. They must not be used to infer exact move IDs, exact frame values, matchup verdicts, combo verdicts, or coaching conclusions beyond the observation contract.

Hermes memory, sessions, profile state, browser state, cron state, local managed skills, local config, secrets, and chat transcripts must not be answer evidence.

### Current-Fact Candidate Metadata

Artifacts under `knowledge/review/current-fact-candidates/` are review-only
current-fact candidates. Non-README candidate artifacts must carry
machine-readable metadata marking them as `review_only`, disallowing public
answers, disallowing generated references, and denying accepted current-fact
authority.

Those metadata fields are guardrails only. They do not verify, accept, promote,
or publish current facts, and they do not create a current-fact authority path.

## Hold Behavior

Hold or unresolved mode is required when evidence is missing, ambiguous, stale, unsupported, outside authority, or conflicting across authority boundaries.

When current fact evidence is unavailable, the answer plan must hold rather than fill the gap with generated references, review notes, video observations, Hermes state, or third-party web summaries.
