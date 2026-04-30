# OpenCode Install

OpenCode installs the public SF6 adapter as one skill named `sf6-agent`.

## Install

Download `packages/skill-installers/install-sf6-agent.ps1` from the release branch or repository, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-sf6-agent.ps1 -Agent opencode
```

The installer downloads `sf6-agent-bundle.zip` from the latest GitHub Release, expands it into a private checkout, and links the OpenCode discovery target:

```text
$HOME/.config/opencode/skills/sf6-agent
```

## Install From A Local Bundle

```powershell
powershell -ExecutionPolicy Bypass -File .\install-sf6-agent.ps1 -Agent opencode -Source .\.dist\sf6-agent-bundle.zip
```

Use `-TargetRoot <path>` for fixture or portable installs. With `-TargetRoot`, the discovery link is `<path>/sf6-agent` and the private checkout is `<path>/_install-root/opencode`.

## Notes

- The installed skill is the single adapter `sf6-agent`; do not install legacy `kb-*` skills directly.
- Canonical release bundle details live in [release-bundle.md](../release-bundle.md).
