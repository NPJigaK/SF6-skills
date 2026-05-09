# Web Research Policy

This policy defines how answer orchestration may use web sources. It is a repo-level policy surface, not an operational Hermes prompt.

## Allowed Uses

Web research may be used for discovery, freshness checks, patch metadata, strategy or meta context, and source ingest support.

Official web sources are required for patch or current metadata when that metadata is used in reports or user-facing summaries.

Web-derived strategy or meta analysis must state freshness, source quality, confidence, and patch-sensitivity boundaries.

## Current Fact Boundary

Web sources must not override packaged frame-current `official_raw`.

Third-party and community web sources are not final authority for exact current facts. They may be used as discovery or supplemental context, but not as the source of truth for exact current move values.

If web sources conflict with packaged current facts, the answer plan must hold the exact value, report the conflict, or route the work to the frame-data refresh workflow. It must not silently replace packaged `official_raw`.

Web research that finds possible stale packaged data is an update signal for the frame-data refresh workflow, not direct permission to change answer authority.
