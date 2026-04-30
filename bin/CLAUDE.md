# CLI Notes — bin/gtheme

Pure bash, `set -euo pipefail`. No dependencies beyond `curl` and `python3` (python3 optional — only used for rich search output, falls back to grep).

## Script structure

```
constants / URLs
helpers:     get_font, brew_cask_name, active_name, font_installed, require_cmd
auto-update: show_update_notice, auto_update, cmd_update
commands:    cmd_list, cmd_switch, cmd_search, cmd_add, cmd_remove, cmd_version, cmd_submit, cmd_help
startup:     broken symlink check → show_update_notice → auto_update
router:      case statement — known commands first, then theme file check, then generic error
```

## Auto-update

- Embeds `VERSION="x.x.x"` at the top
- On each invocation: checks `$THEMES_DIR/.gtheme_last_check` timestamp — skips if < 24h old
- If due: background subshell fetches `VERSION` URL, compares, downloads new binary if newer
- Writes new version string to `.gtheme_updated` — shown as notice on next run
- Skips entirely if `~/.local/bin/gtheme` is a symlink (developer mode)

## Font detection — critical pipefail gotcha

`font_installed()` builds a list of font dirs that actually EXIST before passing to `find`. This is required because `set -euo pipefail` means a pipeline with `find /nonexistent-dir | grep -q .` will fail even if the font was found — `find` exits non-zero and that propagates through the pipeline. Only pass dirs confirmed with `[[ -d "$d" ]]`.

## Key design decisions

- **Unknown input** → generic error ("Unknown command. Run gtheme help."), NOT treated as theme name. Router checks for `.conf` file existence first.
- **One submission path** — `gtheme submit` opens the GitHub issue form. No mention of fork/PR anywhere.
- **Reserved names** — `cmd_add` rejects theme names that match command names (list, search, add, remove, etc.) so they can never conflict with the router.
- **Broken symlink warning** — startup checks if `active.conf` symlink is dangling (points to deleted file) and warns immediately.
- **`gtheme search`** — uses `echo "$index" | GTHEME_QUERY="$query" python3 -c '...'` — JSON piped via stdin, query via env var. Never embedded in heredoc (shell interpolation would corrupt special chars in theme descriptions).
- **`cmd_switch`** — checks `active_name == name` first, exits with "Already using" if same theme.

## Commands reference

```
list     — theme names only, no font info (font info only shown on switch if missing)
<name>   — switches theme via symlink, warns if font not installed
search   — fetches registry/index.json, filters by query, rich python3 output
add      — downloads .conf from registry/themes/, warns if font missing
remove   — deletes local .conf, blocks if theme is currently active
update   — explicit manual update (same logic as auto_update but foreground)
submit   — opens GitHub issue form in browser (open/xdg-open)
version  — prints "gtheme vX.X.X"
help     — usage summary
```
