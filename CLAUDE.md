# gtheme — Claude Notes

gtheme is a lightweight Ghostty theme switcher with a community marketplace. Pure bash CLI, GitHub Pages web app, GitHub Actions submission pipeline. No server, no package manager.

## Sub-file index

Detailed notes are split by area — load these when working in the relevant directory:

- `bin/CLAUDE.md` — CLI architecture, auto-update, key decisions
- `themes/CLAUDE.md` — bundled themes, vibes, sync process
- `docs/CLAUDE.md` — marketplace site, color schema, preview modal
- `registry/CLAUDE.md` — index.json schema, community submission
- `.github/CLAUDE.md` — GitHub Action, issue template, PR flow

## Critical developer workflows

**Releasing a new version** — bump both files, then push:
```bash
echo "0.2.0" > VERSION
# also update VERSION="0.1.0" → VERSION="0.2.0" inside bin/gtheme
git add VERSION bin/gtheme && git commit -m "Release v0.2.0" && git push
```

**After editing a bundled theme** — repo and local Ghostty themes are separate files, must sync manually:
```bash
cp themes/<name>.conf ~/.config/ghostty/themes/
# reload Ghostty: cmd + shift + ,
```

**Developer mode** — `~/.local/bin/gtheme` is a symlink to `bin/gtheme` in this repo. Auto-update detects symlinks and skips, so edits apply immediately.

**Execute permission** — always run `git update-index --chmod=+x bin/gtheme` before committing bin/gtheme, or use the alias: `git add . && git update-index --chmod=+x bin/gtheme && git commit`.

## Repo structure

```
bin/gtheme          — CLI (pure bash)
themes/             — bundled themes (copied to ~/.config/ghostty/themes/ on install)
registry/themes/    — community theme .conf files
registry/index.json — community theme metadata (drives the marketplace)
docs/index.html     — GitHub Pages marketplace (reads index.json from raw GitHub)
install.sh          — one-liner curl installer
VERSION             — current version string (fetched by auto-update)
```
