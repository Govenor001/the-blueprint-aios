# Imported skill provenance

This repository does not bundle the third-party Business OS skill source files. A fresh
deployment may import the procedures at install time from the upstream repository below,
then normalize them into the server's private `skill-vault/`.

| Source | Material | Licence stated by upstream | Distribution note |
|---|---|---|---|
| [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills) | Business OS skill procedures named in `business-os-150/skills-manifest.json` | MIT + Commons Clause, as described by the supplied archive README | Not vendored into this repository; review the upstream terms before commercial redistribution |

The supplied `business-os-150-skills (1).zip` contained only the manifest and installer
wrappers. It did not contain the 150 source `SKILL.md` files, so no third-party source
file from that archive is represented as a checked-in platform asset.

The platform-authored procedures in `skill-vault/` are part of this repository and are
covered by the repository's licence.

| [tt-a1i/archify](https://github.com/tt-a1i/archify) | `vendor/archify/` diagram renderer | MIT | Pinned at commit `2ead014aa8ec91f104cd052f1a6ca82de5e26c31`; update checking and browser visual-check are not run on customer servers |
