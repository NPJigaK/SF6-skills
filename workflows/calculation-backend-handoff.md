# Calculation Backend Handoff Workflow

この workflow は、SF6 固有に見える計算要求を、repo-owned formula や
rounding authority にせず、review 済み maintainer handoff instruction として
選定 backend へ渡すための手順です。

v2.6 の初期既定 backend は SymPy です。SymPy と pinned K-Dense SymPy Agent
Skill は executor / operator instruction dependency であり、SF6 公式値、
式、丸め規則、current facts、public answer behavior を提供しません。

## When To Use

Use this workflow when a maintainer needs arithmetic, symbolic checking, or
trace preparation for one of these requests:

- review-only arithmetic consistency checks;
- hypothetical symbolic examples;
- frame-window, punish-window, or oki timing arithmetic where all inputs and
  instructions are explicitly supplied;
- damage-hidden eval experiments that must stay non-authoritative.

Do not use this workflow to define accepted SF6 formulas, rounding rules,
current system mechanics, or public answer behavior.

## Handoff Flow

```text
maintainer request
  -> calculation backend handoff artifact
  -> selected backend/operator instruction
  -> calculation trace candidate
  -> hold/review boundary
```

The handoff artifact is pre-execution context. It tells the selected backend
what it may compute and when it must hold. The handoff is not calculation
truth.

## Required Boundary

Every handoff must state:

- `authority_status: operator_instruction_only`
- `public_answer_allowed: false`
- `generated_reference_allowed: false`
- `accepted_current_fact_authority: false`

Every handoff must include forbidden-use text equivalent to:

- `not_formula_authority`
- `not_rounding_authority`
- `not_current_fact_authority`
- `not_public_answer_behavior`
- `must_not_feed_generated_references`

## Handoff Template

```json
{
  "handoff_id": "example-hold-missing-instruction",
  "handoff_schema_version": "sf6-calculation-backend-handoff/v1",
  "tracking_issue": "#273",
  "backend_ref": "SymPy",
  "backend_role": "maintainer_local_symbolic_backend",
  "selected_dependency_ref": "tools/agent-skills/apm.lock.yaml#scientific-skills/sympy",
  "authority_status": "operator_instruction_only",
  "public_answer_allowed": false,
  "generated_reference_allowed": false,
  "accepted_current_fact_authority": false,
  "request_scope": "Review-only maintainer calculation handoff.",
  "calculation_intent": "external_backend_instruction_check",
  "input_values": {},
  "input_reference_refs": [],
  "input_status": "hold",
  "calculation_instruction": null,
  "calculation_instruction_status": "hold",
  "rounding_instruction": null,
  "rounding_instruction_status": "hold",
  "expected_trace_contract_ref": "contracts/calculation-executor-trace.md",
  "blocked_status_if_missing": [
    "blocked_missing_calculation_instruction",
    "blocked_missing_rounding_instruction"
  ],
  "uncertainty_or_hold_reasons": [
    "No reviewed calculation instruction is available.",
    "No reviewed rounding instruction is available."
  ],
  "forbidden_uses": [
    "not_formula_authority",
    "not_rounding_authority",
    "not_current_fact_authority",
    "not_public_answer_behavior",
    "must_not_feed_generated_references"
  ],
  "created_by": "maintainer",
  "created_at": "2026-05-18T00:00:00Z"
}
```

## Hold Rules

Use hold / blocked behavior when:

- the calculation instruction is missing or ambiguous;
- rounding, floor, ceiling, truncation, minimum guarantee, or tie behavior
  matters but no reviewed rounding instruction exists;
- route mapping, action mapping, hit mapping, timing, or move identity is
  unresolved;
- the request asks the backend to infer official SF6 formula or current truth;
- the request would support a public current-fact answer.

The matching calculation trace should use the statuses from
`contracts/calculation-executor-trace.md`, such as
`blocked_missing_calculation_instruction`,
`blocked_missing_rounding_instruction`, `blocked_ambiguous_route`, or
`blocked_public_answer_boundary`.

## Safe Examples

Safe handoff examples use only:

- empty hold cases;
- abstract symbols such as `x`, `y`, and `z`;
- generic arithmetic that is not labeled as SF6 current truth;
- review-only instructions that explicitly preserve hold behavior.

Do not include real combo damage numbers, scaling percentages, minimum
guarantee values, route-level formulas, current patch exceptions, or
character/move-specific formula examples.

## Artifact Locations

- schema: `contracts/calculation-backend-handoff.schema.json`
- safe fixtures: `tests/fixtures/calculation-backend-handoff/`
- semantic validator: `tests/validation/validate-calculation-backend-handoff.ps1`
- downstream trace contract: `contracts/calculation-executor-trace.md`

## Not Committed

Do not commit Hermes memory, sessions, local skills, raw transcripts, Curator
output, checkpoints, logs, caches, credentials, provider output, `.env`, or
`auth.json` as part of a handoff.
