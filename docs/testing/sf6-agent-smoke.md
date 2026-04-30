# sf6-agent Smoke Test

This smoke test checks whether an agent reading the public `sf6-agent` adapter chooses the expected answer mode and evidence boundary. It is a manual behavior check, not an exact prose test.

Do not paste exact current frame values into this document. Record whether the answer used packaged frame-current assets and whether it held correctly.

## Test Metadata

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Agent | Codex / Claude Code / Cursor / OpenCode / other |
| Branch or commit |  |
| Tester |  |

## Adapter Surface

Give the agent access to the packaged adapter surface:

- `skills/sf6-agent/SKILL.md`
- `skills/sf6-agent/references/answer-policy.md`
- `skills/sf6-agent/references/current-fact-policy.md`
- `skills/sf6-agent/references/uncertainty-policy.md`
- `skills/sf6-agent/references/generated-*`
- `skills/sf6-agent/assets/frame-current/`

The agent should not need a full repository checkout to answer normal public-adapter questions.

## Pass Criteria

A run passes when the agent:

- Uses `stable concept` for durable mechanics and terminology.
- Uses `verified current fact` only when packaged frame-current assets support the exact current fact.
- Uses `unresolved / hold` when a current exact fact is unavailable, conflicting, underspecified, or outside packaged assets.
- Does not require literal fixed output tags.
- Does not treat `skills/sf6-agent/references/generated-*` as canonical knowledge.
- Does not invent exact current values.
- Does not let supplemental enrichment override `official_raw`.
- Does not turn one video observation into accepted strategy knowledge.

## Cases

| Case | Source eval | Question | Expected mode | Expected evidence boundary | Observed result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| Concept: plus frames | `evals/questions/concepts.yaml#concept-plus-frames` | Explain plus frames in SF6. | `stable_concept` | Explain the concept from generated concept references while keeping exact current move values out. |  |  |  |
| Concept: plus does not mean guaranteed | `evals/questions/concepts.yaml#concept-plus-frames-not-guaranteed-pressure` | If I am plus after a blocked attack, does that mean my next option is guaranteed? | `stable_concept` | Separate frame advantage from guaranteed follow-up claims. |  |  |  |
| Concept: shimmy term boundary | `evals/questions/concepts.yaml#concept-shimmy-community-term` | What is a shimmy, and is it an official SF6 term? | `stable_concept` | Treat shimmy as community terminology unless the agent has explicit official wording evidence. |  |  |  |
| Concept: hit confirm | `evals/questions/concepts.yaml#concept-hit-confirm` | What is a hit confirm? | `stable_concept` | Explain the stable concept without naming current character-specific routes as verified facts. |  |  |  |
| Concept: meaty timing | `evals/questions/concepts.yaml#concept-meaty-timing` | What does meaty timing mean on wake-up? | `stable_concept` | Explain timing without claiming a setup is current-patch verified. |  |  |  |
| Current fact: Luke c.MP on block | `evals/questions/current-fact.yaml#current-fact-luke-cr-mp` | What is Luke crouching medium punch on block in the current published data? | `verified_current_fact` | Use packaged frame-current runtime assets; do not use concept references as final current-fact authority. |  |  |  |
| Current fact: startup and block advantage | `evals/questions/current-fact.yaml#current-fact-runtime-assets-required` | Tell me the current startup and block advantage for Luke's crouching medium punch. | `verified_current_fact` | Use only packaged frame-current runtime assets derived from `data/exports` and `data/roster`. |  |  |  |
| Current fact: unpackaged character | `evals/questions/current-fact.yaml#current-fact-unpackaged-character` | Give the current exact frame data for a character not present in the roster source. | `unresolved_or_hold` | Hold when the character is outside the packaged roster/runtime assets. |  |  |  |
| Current fact: supplemental conflict | `evals/questions/current-fact.yaml#current-fact-supplemental-no-override` | If supplemental enrichment disagrees with `official_raw` for a current value, which source controls the answer? | `verified_current_fact` | Say `official_raw` controls exact current facts and supplemental enrichment cannot override it. |  |  |  |
| Current fact: missing dataset | `evals/questions/current-fact.yaml#current-fact-missing-dataset-hold` | A user asks for exact current frame data from a dataset that is missing from the bundle. What should sf6-agent do? | `unresolved_or_hold` | Hold rather than guess from concepts, generated references, or unpackaged sources. |  |  |  |
| Uncertainty: patch-sensitive setup | `evals/questions/uncertainty.yaml#uncertainty-patch-sensitive-setup` | Is this wake-up setup still guaranteed in the current patch? | `unresolved_or_hold` | Hold unless current patch data and setup-specific reviewed evidence are available. |  |  |  |
| Uncertainty: video generalization | `evals/questions/uncertainty.yaml#uncertainty-video-observation-generalization` | I saw this option work in a video. Is it generally strong strategy? | `unresolved_or_hold` | Treat the clip as observation only; do not promote it to accepted strategy knowledge. |  |  |  |
| Uncertainty: third-party conflict | `evals/questions/uncertainty.yaml#uncertainty-conflicting-third-party-without-runtime-asset` | Two third-party pages disagree about a current exact value, and the frame-current runtime asset is unavailable. Can sf6-agent verify it? | `unresolved_or_hold` | Hold when packaged runtime evidence is unavailable and only conflicting third-party evidence exists. |  |  |  |

## Findings

- None recorded yet.

## Follow-ups

- None recorded yet.
