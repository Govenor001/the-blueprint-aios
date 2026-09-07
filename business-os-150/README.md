# Business OS — Curated 150 Skills

This ZIP contains a **ready-to-run installer and exact manifest** for the 150-skill Business OS we designed.

I am deliberately not repackaging the upstream GitHub source files into a new paid/distributable copy. Instead, the installer pulls the current skill packages directly from the upstream repository, so you get each skill's maintained `SKILL.md` plus its references/scripts/assets.

## Windows / PowerShell

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install-business-os.ps1
```

## Claude Code

The installer targets Claude Code and places the skills in the Agent Skills-compatible project location.

## Contents

- `skills-manifest.json` — exact 150 skills and their upstream paths
- `install-business-os.ps1` — Windows installer
- `install-business-os.sh` — macOS/Linux installer
- `README.md` — setup notes

## Source

Primary source: https://github.com/borghei/Claude-Skills

The upstream project currently advertises hundreds of skills across business growth, C-level, marketing, finance, product, project management, engineering and other domains. Its license is MIT + Commons Clause, which permits internal business use but restricts selling/repackaging the software.

This package is intended for personal/internal business use. Verify legal, financial, compliance and other high-stakes outputs independently.
