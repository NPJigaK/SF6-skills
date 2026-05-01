# Answer Policy

This policy defines adapter behavior for the public `sf6-agent` skill. Canonical SF6 knowledge lives in `knowledge/curated`; generated reference files in this package are derived summaries for runtime use.

## Mode Selection

- Use `stable concept` for durable mechanics, timing ideas, glossary terms, and concept explanations that do not require an exact current row.
- Use `verified current fact` only when an exact current value is found in packaged frame-current assets.
- Use `strategy / matchup knowledge` when the answer is practical guidance based on concepts plus stated assumptions.
- Use `observation` when the answer is limited to what can be seen in provided footage.
- Use `unresolved / hold` when the necessary evidence is missing, ambiguous, stale, outside the package, or would require maintainer review.

## Concept Answers

Concept answers should:

- Start with a direct definition.
- Explain the practical reason the concept matters.
- Separate stable principles from character-specific or patch-sensitive facts.
- State when an exact current value must be checked in frame-current assets.
- Communicate answer mode and evidence boundaries without requiring any fixed label format.

## Strategy And Matchup Answers

Strategy answers may combine stable concepts with assumptions about character, range, resource, round state, and player intent. They should state those assumptions and avoid presenting matchup advice as a verified exact current fact.

## Japanese Questions

When the user asks in Japanese, answer in Japanese unless the user asks otherwise.

Use natural Japanese wording for answer modes and evidence boundaries. Communicate whether the answer is a stable concept, verified current fact, strategy or matchup knowledge, observation, or unresolved/held without requiring any fixed label format.

For stable concepts, explain the concept without giving exact current frame values. For exact current facts, use packaged frame-current assets only.

Japanese terms and shorthand such as `しゃがみ中P`, `屈中P`, `2MP`, `ガード硬直差`, `確反`, `起き攻め`, and `シミー` may require normalization before exact current fact lookup. If the adapter cannot confidently resolve the Japanese term to a packaged character, move, and field, use `unresolved / hold`.

## Generated References

Files named `generated-*` are derived runtime references. Treat their generated marker and source path list as provenance, but do not treat them as the canonical authoring location.
