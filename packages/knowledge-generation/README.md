# knowledge-generation

Package classification: `active_repo_local`.

Repo-local generated knowledge runtime builder.

`build-sf6-agent-knowledge.ps1` reads `knowledge/curated/` and builds generated
knowledge runtime payloads. The current checked output path is still under the
deferred public adapter, but the package classification is active repo-local
because the generator is retained for private maintainer runtime generation and
future `runtime/generated-knowledge/` migration.

This package is not public skill distribution tooling. Do not add public adapter
behavior here.
