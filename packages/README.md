# Packages

Shared executable infrastructure for packaging, validation, and installers.

Use `packages/` only after a second real consumer exists.

Keep skill-specific logic inside its skill directory until shared demand is real.

- `calculation-executor/`: deterministic repo-local arithmetic trace
  compatibility helper used by validation fixtures and Codex/Hermes maintainer
  playbook calls. It is not a custom SF6 math engine.
