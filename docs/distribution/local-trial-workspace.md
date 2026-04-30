# Local Trial Workspace

`local/` is the personal trial workspace.

Use it for trying the distributed skills from this repository.

Use the tracked skeleton files under `local/` as the workspace entry surface.

To wire local discovery, run:

```powershell
pwsh -File ../scripts/dev/bootstrap-local-trial-workspace.ps1
```

This creates an ignored local discovery adapter under `local/.agents/skills/` without introducing a tracked repo-root mirror.
