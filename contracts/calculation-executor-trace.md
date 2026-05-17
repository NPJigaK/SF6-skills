# Calculation Executor Trace Contract

This contract defines how repo-local calculation tools, scripts, skills, or
agents may produce auditable SF6 calculation traces.

Calculation executors are not SF6 authority. They may run arithmetic and emit
trace output, but they must not supply input facts, formulas, rounding rules,
current patch facts, system mechanics, or public answer authority.

The repo does not own accepted SF6 formulas or rounding rules. If SF6-specific
calculation is needed, the reusable knowledge should be an operator instruction
for a trusted external CAS or symbolic math backend, not repo formula
authority.

## Executor Boundary

Calculation executors may:

- run arithmetic against explicitly supplied inputs;
- run arithmetic against explicitly supplied non-authoritative calculation
  instructions;
- emit ordered calculation steps that a reviewer can audit;
- check hypothetical or review-only arithmetic consistency while preserving
  draft or hold status;
- support future damage-hidden eval experiments only as non-authoritative trace
  generation.

Calculation executors must not:

- become source of truth for damage, frame values, scaling, timing, oki, punish
  windows, resources, rounding, or current-system behavior;
- fill missing SF6 formulas from tool memory, third-party skill text, web
  summaries, or embedded examples;
- promote review-only candidates, claim artifacts, video observations, smoke
  reports, or combo fixtures into accepted current facts;
- treat generated concept references as exact current values or formulas;
- override `data/exports/`, `data/roster`, packaged `official_raw`, accepted
  contracts, or accepted workflows;
- write generated references, frame-current assets, or public adapter behavior
  unless a separate reviewed issue explicitly allows it.

Third-party or wild math skills are allowed only as executor implementations or
operator instructions after dependency review. Their output is a calculation
trace candidate, not authority.

## Trace Fields

A calculation trace should include enough structured information to reproduce
and audit the computation. A later JSON schema may narrow these fields when the
repo begins storing trace artifacts.

Minimum fields:

- `trace_id`: stable trace artifact ID.
- `trace_schema_version`: contract version, such as
  `sf6-calculation-trace/v1`.
- `executor_id`: name, version, hash, or invocation identity of the tool,
  script, skill, or agent that produced the trace.
- `executor_role`: one of `calculation_executor`, `trace_generator`, or
  `arithmetic_consistency_checker`.
- `executor_authority_status`: must state that the executor is not SF6
  authority, formula authority, rounding authority, or current-fact authority.
- `calculation_intent`: why the calculation was run, such as
  `hypothetical_arithmetic_check`, `external_backend_instruction_check`,
  `damage_hidden_eval_candidate_check`, `frame_window_arithmetic`,
  `punish_window_arithmetic`, or `oki_timing_arithmetic`.
- `question_scope`: short natural-language scope of the calculation.
- `input_values`: all numeric or symbolic inputs used by the executor.
- `input_authority_refs`: source refs for every non-hypothetical input.
- `input_status`: one of `accepted`, `review_only`, `hypothetical`, `mixed`, or
  `hold`.
- `calculation_instruction_ref`: reviewed maintainer instruction, skill, or
  handoff reference used to tell a trusted external backend what to compute.
- `calculation_instruction_status`: one of `external_backend_candidate`,
  `review_only`, `hypothetical`, `not_applicable`, or `hold`.
- `rounding_instruction_ref`: non-authoritative rounding instruction reference
  when rounding affects output.
- `rounding_instruction_status`: one of `external_backend_candidate`,
  `review_only`, `hypothetical`, `not_applicable`, or `hold`.
- `operation_steps`: ordered computation steps.
- `output_values`: computed outputs, explicitly labeled as trace outputs rather
  than authority.
- `status`: result status from the list below.
- `public_answer_allowed`: whether this trace may support a public answer.
- `generated_reference_allowed`: whether this trace may feed generated
  references. Default is `false` unless a later reviewed workflow allows it.
- `accepted_current_fact_authority`: must be `false` for executor traces.
- `uncertainty_or_hold_reasons`: required when any input, calculation
  instruction, rounding instruction, route mapping, or timing assumption is
  missing.
- `created_by`: human, agent, script, or skill that created the trace.
- `created_at`: timestamp.
- `repo_revision`: repository commit or revision used for the calculation, when
  committed.
- `limitations`: human-readable boundary notes.

Each `operation_steps` entry should include:

- `step_id`
- `operation_kind`
- `inputs_used`
- `output`
- `rounding_applied`
- `policy_ref`
- `notes`

## Status Semantics

Use one of these values for `status`:

- `not_run`: no calculation was executed.
- `trace_generated`: arithmetic ran and a trace exists, but the result is not an
  accepted current fact.
- `hypothetical_arithmetic_only`: values were user-provided, hypothetical, or
  review-only; the executor checked arithmetic consistency only.
- `blocked_missing_input_authority`: an input is absent from `data/exports/`,
  `data/roster`, packaged `official_raw`, or another accepted authority
  surface.
- `blocked_missing_calculation_instruction`: calculation instruction, scaling
  guidance, timing guidance, or exception handling is missing or held.
- `blocked_missing_rounding_instruction`: rounding, floor, ceiling,
  truncation, minimum guarantee, or tie behavior matters but no reviewed
  instruction exists.
- `blocked_ambiguous_route`: combo route, action mapping, hit mapping, timing,
  or move identity is unresolved.
- `blocked_public_answer_boundary`: a calculation may exist for maintainer
  review but cannot support public answer behavior.
- `invalid_input`: inputs are contradictory, malformed, or unsupported by this
  contract.
- `executor_error`: the tool failed or produced non-auditable output.
- `out_of_scope`: the request asks the executor to decide authority, scrape
  facts, infer SF6 formulas, or answer beyond arithmetic execution.

## Public Answer Rules

Executor traces must not support public current-fact answers in v2.6.
`public_answer_allowed` remains `false` for traces from the repo-local
compatibility helper.

Use hold or unresolved behavior when any required input, calculation
instruction, rounding instruction, route mapping, or timing assumption is
missing.

For hypothetical questions, the adapter may compute arithmetic consistency only
if it states that the values are hypothetical or review-only and not accepted
current SF6 truth.

For exact current move facts, public answers remain grounded in packaged
frame-current authority derived from `data/exports/` and `data/roster`. For
route-level formulas, combo damage, meaty or oki timing, punish windows,
resource/damage calculations, or rounding questions, hold unless a later
architecture decision reopens this boundary.

## Non-Authority Inputs

These sources may help route review work but must not become calculator
authority by themselves:

- generated concept references;
- review-only claim artifacts;
- current-fact candidates;
- video observations;
- combo-damage fixtures;
- smoke reports;
- Hermes memory, sessions, local skills, or raw transcripts;
- third-party or wild calculation skills.

## Future Validation

This docs-only contract does not create stored trace artifacts or a trace JSON
schema. A later PR may add:

- `contracts/calculation-trace.schema.json`;
- `tests/validation/validate-calculation-traces.ps1`;
- validators that reject `accepted_current_fact_authority: true`;
- validators requiring external-backend instruction refs for selected trace
  use cases;
- validators blocking `public_answer_allowed: true` for hypothetical, blocked,
  invalid, or executor-error traces.
