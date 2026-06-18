---
name: sf6-calculation-grounding
description: "Use for SF6 calculation grounding: exact combo damage, damage/gauge/juggle/distance/timing calculations, source-backed ledgers, fixtures, prediction/postmortem, validation, authority, and rule-promotion decisions. Do not use route text alone to produce deterministic outputs."
---

# SF6 Calculation Grounding

## Role

Manage calculation evidence lifecycle. The job is not to make the calculator guess; the job is to prevent uncertain ledgers from becoming deterministic facts.

Use this skill for calculation grounding across SF6 damage, gauge, juggle, distance, and timing work, especially when exact values, fixtures, prediction/postmortem records, validation status, or rule promotion are involved.

## Required Reads

1. `AGENTS.md`.
2. `wiki/concepts/combo-damage-ledger-protocol.md` for combo damage, damage scaling, or ledger work.
3. Relevant `wiki/sources/` pages.
4. Relevant raw paths, manifests, metadata, validation files, and derived JSON outputs.
5. Relevant `wiki/reviews/`, `wiki/outputs/reports/`, and existing postmortems.
6. Existing tool code, fixture, test, and output contract when tool, schema, fixture, or regression changes are requested.

Use repo-local `$jq-cli` for JSON / JSONL values, row counts, validation status, fixture schema checks, and derived-output spot checks whenever practical.

## Core Rule

The calculator may be deterministic. The ledger often is not.

Never let deterministic arithmetic disguise uncertain ledger construction.

## Work Classification

Classify the task before acting:

- `answer-only`
- `candidate ledger`
- `regression fixture`
- `validated fixture`
- `prediction record`
- `postmortem record`
- `rule promotion`
- `tool contract change`
- `schema / validator change`
- `wiki review / durable report`

State the classification in the working notes or final report when it affects whether an exact value can be produced.

## Allowed Output Matrix

Classification controls what may be produced.

| Classification | Allowed outputs | Forbidden outputs |
|---|---|---|
| `answer-only` | cited explanation, uncertainty, required evidence | new fixture, new rule, deterministic output without ledger |
| `candidate ledger` | candidate ledger, unknowns, review-needed note | exact final value, deterministic calculator output as final |
| `regression fixture` | route-specific fixture with authority, source paths, and limits | general rule promotion |
| `validated fixture` | fixture with accepted validation and reproducible contract | treating fixture as source fact |
| `prediction record` | immutable pre-answer prediction with hash | editing after answer is known |
| `postmortem record` | comparison to prediction, error taxonomy, protocol updates | retroactive prediction changes |
| `rule promotion` | proposed rule with independent evidence and accepted review | route-specific observation as general rule |
| `tool contract change` | tool/schema/test update with fixture coverage | behavior change without tests |
| `schema / validator change` | schema format decision, validator/test update, migration note | calling repo-local descriptors formal JSON Schema |
| `wiki review / durable report` | review note or report with evidence, uncertainty, and next action | hiding unresolved authority or validation gaps |

## Gates

Apply these in order, stopping when a required input is missing:

1. **Version / source gate**: confirm patch, version, source freshness, source authority, and whether the route or value is current-only or historical.
2. **Move resolution gate**: resolve notation to source moves, including target combo follow-up, strength, Modern / Classic, install state, manual / auto activation, and branch conditions.
3. **Non-linear hit gate**: identify delayed projectiles, install follow-ups, portals, bombs, multi-hit moves, juggle, distance, corner, height, and timing-dependent routes.
4. **Hit order proof gate**: require source-backed relative timing, accepted validation, or explicit hit display before treating hit order as deterministic.
5. **Attack-step gate**: separate `hit_index` from `attack_step`; do not assume multi-hit segments share or advance scaling unless source-backed.
6. **Scaling-state gate**: separate starter, immediate, multiplier, minimum, Drive Rush one-time penalty, Super Art minimum, character-specific scaling, and condition multiplier.
7. **Arithmetic gate**: run deterministic calculator only after ledger evidence is sufficient; preserve per-hit floor policy and trace fields.
8. **Validation gate**: compare against accepted training-mode display, video-derived per-hit evidence, validated fixture, or source-backed derived output when available.
9. **Fixture decision gate**: decide whether evidence supports candidate ledger only, regression fixture, or validated fixture.
10. **Rule promotion gate**: do not promote route-specific observations into general rules without independent source or accepted review support.
11. **Wiki feedback gate**: decide whether the outcome should update a review note, durable report, protocol page, concept page, tests, schema, or tool contract.

## Stop Conditions

If any required evidence is missing, do not produce an exact deterministic value.

Return:

- candidate ledger if useful
- unknowns
- required evidence
- recommended review note, validation task, or capture/review follow-up

Stop rather than exact-answer when:

- route text is the only hit-order evidence
- candidate ledger / candidate fixture is the strongest evidence
- validation status is missing, failed, disputed, or human-only and a general rule is being inferred
- delayed projectile, install, portal, bomb, multi-hit, juggle, distance, corner, height, or timing dependency lacks hit order proof
- a community-only numeric source would be elevated to official, lab-verified, or validated-rule authority

## Validation Authority Matrix

Do not treat all human validation the same.

| Validation type | Exact route answer | Regression fixture | Validated rule |
|---|---:|---:|---:|
| unreviewed human claim | no | no | no |
| human training display, not reviewed | candidate only | candidate only | no |
| accepted route-specific training display / video review | yes, route-specific only | yes | no |
| source-backed derived output | yes, within scope | yes | maybe, if independently supported |
| official source / accepted rule review | yes | yes | yes |

Human-only route validation may support a route-specific regression after review, but must not become a source fact or general rule.

Accepted review means a `wiki/reviews/` note with explicit accepted status or a human-reviewed final decision. Do not infer accepted status from the existence of a review note alone.

## Promotion Policy

Do not confuse:

- candidate ledger
- candidate fixture
- regression fixture
- validated fixture
- working hypothesis
- validated rule

A fixture matching an expected total is not enough to promote a general rule.

A human training-mode observation can support a route-specific regression, but does not automatically become a source fact or validated rule.

A fixture verifies calculator behavior against a documented ledger. It does not by itself prove a gameplay rule. A regression fixture preserves a route-specific known case; a validated fixture may support future comparisons, but rule promotion still requires independent evidence.

Prediction and postmortem records are lifecycle inputs. When they reveal a missing gate or false assumption, update or propose updates to protocol, reviews, tests, schema, or tool contract instead of just reporting the result.

## Prediction / Postmortem Integrity Gate

Prediction records are pre-answer artifacts.

- A prediction record must be written before the answer / validation is known.
- Once used for postmortem, prediction content must not be edited.
- Postmortem records must include `prediction_sha256` or an equivalent immutable reference.
- If a prediction contains an error, do not rewrite the prediction. Explain the error in postmortem.
- Postmortem may update protocol, review notes, tests, schema, or tool contract, but must not alter the original prediction.

## Schema / Contract Format Gate

Before changing schema or validator behavior, classify the schema format:

- `repo_local_contract_descriptor`
- `formal_json_schema`
- `python_validator_contract`
- `test_fixture_contract`

Do not call a repo-local contract descriptor a formal JSON Schema.

If adopting formal JSON Schema, update dependencies, validator command, tests, migration notes, and wiki documentation together.

## Test Gate

When modifying any of the following, run the relevant calculation tests or explicitly report why they could not be run:

- `tools/calculations/**`
- `tests/calculations/**`
- calculation fixtures
- calculation schema / contract descriptors
- generated calculation output

Expected command examples:

- `pytest tests/calculations/combo_damage`
- targeted fixture validation command if available

Do not mark a calculation tool / fixture / schema change as complete without test status.

## Write Scope Policy

Default mode is read / classify / report.

Only write when the user explicitly asks for durable changes or tool/fixture updates.

| Classification | Allowed write targets |
|---|---|
| `answer-only` | none |
| `candidate ledger` | review note or report only |
| `regression fixture` | tests/fixtures + report + log, after evidence check |
| `validated fixture` | tests/fixtures + schema/report/log, after accepted validation |
| `prediction record` | prediction path only, before answer is known |
| `postmortem record` | postmortem/report/review/log |
| `rule promotion` | review note first; tool/schema only after accepted review |
| `tool contract change` | tools/tests/schema/docs/wiki protocol/log |
| `schema / validator change` | schema/validator/tests/migration note/wiki protocol/log |
| `wiki review / durable report` | `wiki/reviews/` or `wiki/outputs/reports/` + index/log |

## Family Protocol Gate

If no family-specific protocol exists for gauge, juggle, distance, timing, or another calculation family, do not invent deterministic rules silently.

Create or propose a review note / protocol stub before implementing deterministic tooling.

## Handoff

- Use `$sf6-durable-output` for reader-facing calculation reports, postmortems, comparisons, or durable review notes.
- Use `$sf6-wiki-refactor` if protocol, concept, index, or wiki topology needs recompile.
- Use `$sf6-wiki-health-check` when detecting calculation evidence drift, schema / contract drift, candidate fixture leakage, or stale claims.
- Use `$sf6-source-ingest` if new raw source material must be compiled before calculation grounding can proceed.
- Update `wiki/index.md` and append to `wiki/log.md` for durable changes.

## Handoff Loop Guard

Do not recursively bounce between skills.

If this skill was invoked from another skill, return a handoff recommendation instead of invoking another skill automatically.

At most one secondary skill handoff should be executed in a single pass unless the user explicitly asks for a full maintenance cycle.

## Tooling Boundary

Do not add route parsers, frame simulators, generic calculators, schema migration scripts, or validators merely because a calculation question is hard. Add or change deterministic tools only when the source-backed formula, input contract, failure mode, fixture coverage, and rollback behavior are clear.

When modifying `tools/calculations/`, also inspect and update relevant tests, fixtures, schema descriptors, reports, and wiki protocol pages.
