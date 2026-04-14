# skill-installers

Shared installer scripts for Codex, OpenCode, Claude, and Cursor live here.

`resolve-install-target.ps1` keeps the agent-specific discovery targets stable.
`install-sf6-skills.ps1` downloads `sf6-skills-bundle.zip`, expands it into a private source checkout, and links the discovery target to that checkout.

When `TargetRoot` is supplied, the private checkout lives under `<TargetRoot>/_install-root/<Agent>`.
Otherwise it lives under `$HOME/.sf6-skills/<Agent>`.
