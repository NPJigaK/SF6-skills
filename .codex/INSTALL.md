# Codex Install

Clone the repository:

```powershell
git clone https://github.com/NPJigaK/SF6-skills.git
```

Create the skills junction so Codex can load the repo-local skill library:

```powershell
New-Item -ItemType Junction -Path "$HOME\.agents\skills\sf6-skills" -Target "E:\github\SF6-skills\skills"
```

This links `~/.agents/skills/sf6-skills` to the repository `skills/` directory.
