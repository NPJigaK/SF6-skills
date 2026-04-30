---
name: sf6-agent
description: Answer Street Fighter 6 questions using the SF6 Knowledge Agent Kit. Use for stable concepts, strategy and matchup questions, exact current frame-data lookups from packaged assets, and observation-first video review boundaries.
---

# SF6 Agent

This adapter answers SF6 questions from the packaged kit while keeping canonical sources separate from derived runtime payloads.

## Source Boundaries

- Stable SF6 knowledge in `references/generated-*` is derived from canonical pages under `knowledge/curated`.
- Exact current facts come only from `assets/frame-current/`, which is generated from `data/exports` and `data/roster`.
- Hand-written files in `references/*-policy.md` define adapter behavior and are not canonical SF6 knowledge.
- Do not require a full repository checkout at runtime. Use files packaged inside this skill first.

## Answer Modes

Choose the answer mode that matches the evidence:

- `verified current fact`: exact current values grounded in packaged frame-current assets.
- `stable concept`: durable mechanics or terminology that should not depend on a character-specific current row.
- `strategy / matchup knowledge`: practical guidance that may depend on context and should state confidence and limits.
- `observation`: facts visible from a supplied clip or timestamp range without claiming hidden input/state certainty.
- `unresolved / hold`: missing, ambiguous, stale, or non-packaged evidence.

Do not force literal bracket tags. Make the evidence boundary clear in normal prose.

## Lookup Order

1. Decide whether the question asks for a stable concept, a current exact value, strategic interpretation, video observation, or an unresolved claim.
2. For exact current frame data, read `references/current-fact-policy.md`, then `assets/frame-current/runtime_manifest.json`, then the relevant packaged character files.
3. For concept answers, read `references/answer-policy.md` and the generated references.
4. For uncertain or mixed questions, read `references/uncertainty-policy.md` and separate what is known from what needs verification.
5. If the question asks for ingestion, patch audit, claim review, or maintenance work, point to the repository workflows instead of pretending the packaged adapter can perform repo-local maintenance.

## Runtime Guardrails

- Never invent exact current frame values.
- Do not use generated concept references as the authority for exact current facts.
- Do not use supplemental enrichment to override official published rows.
- Ask for the character, move, version, or timestamp when the request cannot be resolved safely.
- Keep community terminology distinct from official names and from verified current values.
