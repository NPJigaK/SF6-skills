# Query Normalization Aliases

`data/aliases/` is canonical query-normalization support for mapping user wording to structured lookup inputs.

This directory is not exact current-fact authority. Exact current facts remain grounded in `data/exports/` and `data/roster/`, and runtime frame-current facts remain under `skills/sf6-agent/assets/frame-current/`.

Future derived normalization runtime assets may be generated under `skills/sf6-agent/assets/normalization/`. That target must stay separate from `skills/sf6-agent/assets/frame-current/`; do not mix normalization assets into frame-current runtime assets.

Normalization aliases can help map user language to fields such as character slugs, move inputs, and lookup field keys. They do not prove move data, frame values, damage, patch metadata, matchup judgments, or strategy claims.

This surface currently contains minimal fixtures for validation. It does not attempt full roster move alias coverage.
