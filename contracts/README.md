# Contracts

`contracts/` is canonical for schemas and structured artifact contracts.

Contracts distinguish canonical surfaces from derived surfaces and use generic source/evidence metadata.

Some contracts describe Markdown front matter or agent-readable artifacts that are enforced by dedicated validators rather than by a generic JSON Schema runtime. Validators under `tests/validation/` are the executable contract layer for the current repo.

When `source_refs.path` points to a migrated legacy file, `source_revision` identifies the commit where that historical path can be reviewed.
