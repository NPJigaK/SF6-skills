# Distribution Docs

This directory is a deferred legacy public distribution surface. ADR-0004 keeps
these docs only as interim `legacy-distribution` lane coverage until the public
`skills/sf6-agent/` adapter is removed after runtime payload relocation.

Current human-readable install docs while the deferred adapter still exists:

- [Codex](./agents/codex.md)
- [Claude](./agents/claude.md)
- [Cursor](./agents/cursor.md)
- [OpenCode](./agents/opencode.md)

Repo-local maintainer orchestration guidance:

- [Hermes](./agents/hermes.md)

Supporting docs:

- [release-bundle.md](./release-bundle.md)

The public distribution surface is the single `sf6-agent` adapter. Agent-specific front-door files are not canonical hand-written surfaces in v2; this directory owns the canonical install instructions while the deferred adapter still exists.

Do not add new public distribution features here unless a later ADR reactivates
public distribution. Policy reference:
`docs/architecture/decisions/0004-retire-deferred-distribution-surfaces.md`.
See
[`../architecture/decisions/0004-retire-deferred-distribution-surfaces.md`](../architecture/decisions/0004-retire-deferred-distribution-surfaces.md).
