# gtheme — Claude Notes

## Shipping a new version

To push an update to all installed users, bump the version in `VERSION` and `bin/gtheme` (the `VERSION=` line near the top), then commit and push. Users on the auto-update path will silently receive the new binary within 24 hours.

```bash
# Example: releasing v0.2.0
echo "0.2.0" > VERSION
# Update VERSION="0.1.0" → VERSION="0.2.0" in bin/gtheme
git add VERSION bin/gtheme
git commit -m "Release v0.2.0"
git push
```

## Repo structure

- `bin/gtheme` — the CLI (pure bash, no dependencies beyond curl)
- `themes/` — bundled default themes (shipped with install.sh)
- `registry/themes/` — community theme files (added via issue review)
- `registry/index.json` — community theme index (name, author, description, font, colors, tags)
- `docs/index.html` — GitHub Pages marketplace site (reads index.json from raw GitHub URL)
- `install.sh` — one-liner installer
- `VERSION` — current version string, fetched by auto-update logic

## Adding a community theme

When someone submits a theme via the GitHub issue form:
1. Copy their `.conf` to `registry/themes/<name>.conf`
2. Add an entry to `registry/index.json` (include `colors.background` and `colors.accent` array for marketplace swatches)
3. Commit and push — the marketplace site updates automatically

## Developer mode

`~/.local/bin/gtheme` on Geoff's machine is a symlink to `bin/gtheme` in this repo. Auto-update skips symlinks, so edits in the repo take effect immediately without any overwrite risk.
