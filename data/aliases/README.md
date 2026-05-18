# Query Normalization Aliases

`data/aliases/` is canonical query-normalization support for mapping user wording to structured lookup inputs.

This directory is not exact current-fact authority. Exact current facts remain grounded in `data/exports/` and `data/roster/`, and runtime frame-current facts are generated under `runtime/frame-current/`.

Derived normalization runtime assets are generated under `runtime/normalization/`. That target must stay separate from frame-current runtime assets; do not mix normalization assets into frame-current runtime assets.

Normalization aliases can help map user language to fields such as character slugs, move inputs, and lookup field keys. They do not prove move data, frame values, damage, patch metadata, matchup judgments, or strategy claims.

This surface currently contains minimal fixtures for validation. It does not attempt full roster move alias coverage.
