# Packages

Shared executable infrastructure for repo-local generation, validation,
compatibility helpers, and deferred distribution.

Use `packages/` only after a second real consumer exists, or when a reviewed
architecture decision classifies the package as a transition surface.

Keep skill-specific logic inside its skill directory until shared demand is real.

Package classifications are defined in
`docs/architecture/package-surface-classification.md`.

| Package | Package classification | Current boundary |
|---|---|---|
| `calculation-executor/` | `active_repo_local` | Deterministic arithmetic trace compatibility helper. Not a custom SF6 math engine. |
| `knowledge-generation/` | `active_repo_local` | Builds generated knowledge runtime payloads from `knowledge/curated/`. |
| `skill-packaging/` | `shared_infra` | Runtime asset builders plus deferred release bundle builder. Keep entrypoint boundaries separate. |
| `skill-installers/` | `deferred_distribution` | Deferred public adapter installer tooling kept only for interim legacy-distribution coverage. |
| `skill-validator/` | `legacy` | Historical placeholder. Current validation authority is `tests/validation/`. |

- `calculation-executor/`: deterministic repo-local arithmetic trace
  compatibility helper used by validation fixtures and Codex/Hermes maintainer
  playbook calls. It is not a custom SF6 math engine.
