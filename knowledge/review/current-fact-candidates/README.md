# Current-Fact Candidate Review

This directory holds patch-sensitive exact-current candidates before they are resolved through the current-fact workflow.

Entries here may cite `data/exports/`, `snapshot_manifest.json`, packaged current-fact fields, candidate frame values, or `move_id` values when that evidence is needed for review.

Entries here are not final public answer evidence, must not feed generated knowledge references, are not accepted curated knowledge, and must be resolved into the current-fact data surfaces or kept on hold.

Candidate artifacts here are review-only current-fact claim records, not ordinary knowledge pages. They are governed by the current-fact boundary validator and claim/source contracts rather than the curated knowledge page validator.

System-mechanics current fact candidates also stay here until a dedicated accepted authority path exists.

Examples include combo-scaling numeric values that are not already packaged as move-specific frame-current fields, route-level damage formulas, minimum guarantee values, system action modifiers, and patch-sensitive exception rules.

## Machine-readable authority metadata

Each non-README candidate artifact must include these front matter fields with
these exact values:

```yaml
authority_status: review_only
authority_role: review_only_current_fact_candidate
public_answer_allowed: false
generated_reference_allowed: false
accepted_current_fact_authority: false
```

These fields are guardrails only.
They do not verify, accept, promote, or publish current facts.
Changing them is not a promotion path. Accepted use requires a separate
current-fact authority path and review.

See `workflows/system-mechanics-fact-workflow.md`.
