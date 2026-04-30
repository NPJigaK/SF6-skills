# skill-installers

Shared installer scripts for Codex, OpenCode, Claude, and Cursor live here.

`resolve-install-target.ps1` keeps the agent-specific discovery targets stable for the public `sf6-agent` adapter.
`install-sf6-agent.ps1` downloads `sf6-agent-bundle.zip`, expands it into a private source checkout, and links the discovery target to that checkout.

When `TargetRoot` is supplied, the private checkout lives under `<TargetRoot>/_install-root/<Agent>`.
Otherwise it lives under `$HOME/.sf6-agent/<Agent>`.

Default discovery targets:

- Codex: `$HOME/.agents/skills/sf6-agent`
- OpenCode: `$HOME/.config/opencode/skills/sf6-agent`
- Claude: `$HOME/.claude/skills/sf6-agent`
- Cursor: `$HOME/.cursor/skills/sf6-agent`
