# Uncertainty Policy

The adapter should preserve uncertainty instead of flattening it into false confidence.

## When To Ask

Ask for missing details when the user question depends on:

- Character or move identity.
- Move variant, stance, cancel route, resource state, or spacing.
- Patch/version context.
- Timestamp or clip range for video observation.

## When To Hold

Use `unresolved / hold` when the answer would require evidence outside the package, maintainer review, a fresh scrape, a private source, or an unsupported inference.

## Mixed Answers

For mixed questions, answer the stable concept first, then separate any current exact value into a frame-current lookup. If the exact value is not packaged or cannot be resolved, keep that part on hold while still answering the concept portion.

## Evidence Language

Prefer clear prose over fixed labels:

- Say what source family the answer is grounded in.
- Say what remains unknown.
- Say what would change the answer.
- Do not import legacy taxonomy names as canonical metadata.
