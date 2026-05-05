# CLI Notes — bin/gtheme

Pure bash, `set -euo pipefail`. No dependencies beyond `curl`.

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
- **Reserved names** — `cmd_add` rejects theme names that match command names (list, search, add, remove, uninstall, etc.) so they can never conflict with the router.
- **Broken symlink warning** — startup checks if `active.conf` symlink is dangling (points to deleted file) and warns immediately.
- **`cmd_switch`** — checks `active_name == name` first, exits with "Already using" if same theme.

## bash arithmetic + set -e gotcha

`(( selected++ ))` evaluates to the old value — when `selected` is 0, `(( 0 ))` returns exit code 1, and `set -e` kills the script. Same trap with `(( selected-- ))` when result is 0. Always use `selected=$(( selected + 1 ))` form inside the picker loop.

`read -t 0.1` (fractional timeout) is bash 4+ only. macOS ships bash 3.2. Use integer `-t 1` for the escape-sequence reads after detecting `\x1b`. `-t 0` (non-blocking) is also unreliable — arrow key bytes aren't always in the buffer atomically.

## Interactive list picker — design note

`cmd_list` uses an arrow-key picker (raw terminal via `stty -echo -icanon`). This was a deliberate UX choice — low risk for Ghostty users (consistent terminal, bounded list size). If it causes issues in practice, revert `cmd_list` to the plain loop (print names, mark active with `*`) and update the README/help descriptions accordingly. The rest of the codebase is unaffected.

`gtheme search` was simplified to just open the web app (`open`/`xdg-open`). The old JSON/python3 search logic was removed — too many failure modes for little gain.

## Commands reference

```
list     — interactive arrow-key picker; Enter switches, q/Esc cancels; falls back to "no themes" message if empty
<name>   — switches theme via symlink, warns if font not installed
search   — opens community marketplace in browser (open/xdg-open)
add      — downloads .conf from registry/themes/, warns if font missing
remove   — deletes local .conf, blocks if theme is currently active
update   — explicit manual update (same logic as auto_update but foreground)
uninstall — removes binary, bundled themes, active symlink, Ghostty config line, PATH entry from shell rcs; leaves community themes intact; confirms before acting
submit   — opens GitHub issue form in browser (open/xdg-open)
version  — prints "gtheme vX.X.X"
help     — usage summary
```
