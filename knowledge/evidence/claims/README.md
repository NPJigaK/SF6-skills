# Evidence Claims

`knowledge/evidence/claims/` holds atomic candidate claims and reviewed claim records.

Each claim should use the generic v2 metadata model: `claim_kind`, `source_kind`, `source_role`, `evidence_basis`, `verification_state`, `confidence`, `volatility`, `patch_sensitivity`, `review_status`, `source_refs`, and `review_after`.

Claims are not final public answer evidence until they are accepted through review and promoted into the appropriate canonical surface.

## Machine-readable authority metadata

Each non-README claim artifact must include these front matter fields with
these exact values:

```yaml
authority_status: review_only
authority_role: review_only_evidence_claim_artifact
public_answer_allowed: false
generated_reference_allowed: false
accepted_current_fact_authority: false
```

These fields are artifact-level guardrails only. They do not verify, accept,
promote, reject, or publish any embedded claim. They do not make the claim
artifact public answer authority. Claim artifacts must not feed generated references directly.

Accepted public use requires normal claim review and promotion into an
appropriate canonical surface.
