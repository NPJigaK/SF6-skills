# Knowledge

`knowledge/` is canonical for curated SF6 knowledge.

- `sources/`: source metadata, access/capture information, short necessary excerpts, and summaries.
- `evidence/claims/`: atomic candidate claims and reviewed claim records.
- `evidence/video-observations/`: observation artifacts that follow the video observation contract.
- `review/`: holding area for unresolved, contested, patch-sensitive, or migration-review material.
- `curated/`: accepted knowledge with v2 evidence metadata.

Do not store exact current move values here. Exact current facts belong in `data/exports/` and generated frame-current runtime assets.

The intended flow is source metadata to evidence or claims, then review, then curated knowledge. Full copyrighted articles, videos, screenshots, audio, and transcripts are not stored by default.

`data/knowledge-lineage.json` is a generated observability report for the
source -> evidence -> review -> curated flow. It is not gameplay authority or
normal public answer authority. Refresh and validate it with:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-knowledge-lineage-report.ps1 -Update
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-knowledge-lineage-report.ps1
```

`data/knowledge-integrity.json` is a generated observability report for
dangling knowledge references, duplicate artifact IDs, `review_after` state,
and generated-reference contamination. It is not gameplay authority or normal
public answer authority. Refresh and validate it with:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-knowledge-integrity-report.ps1 -Update
pwsh -NoProfile -ExecutionPolicy Bypass -File tests/validation/validate-knowledge-integrity-report.ps1
```
