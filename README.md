# gtheme

A lightweight theme switcher for [Ghostty](https://ghostty.org) with a community theme library.

---

- [Installation](#installation)
- [Commands](#commands)
- [How it works](#how-it-works)
- [Bundled themes](#bundled-themes)
- [Creating your own theme](#creating-your-own-theme)
- [Sharing your theme](#sharing-your-theme)

---

## Installation

Run the following command in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/UnionPAC/gtheme/main/install.sh | bash
```

---

## Commands

```bash
gtheme list                  # browse and switch themes (interactive picker)
gtheme <name>                # switch directly to a named theme
gtheme search                # browse the community registry (opens browser)
gtheme add <name>            # install a theme from the community
gtheme remove <name>         # remove an installed theme
gtheme update                # update gtheme to the latest version
gtheme uninstall             # remove gtheme from your system
gtheme submit                # share your theme with the community
gtheme version               # show the current version
gtheme help                  # show all commands
```

After switching, reload Ghostty with `cmd + shift + ,` — no restart needed.

---

## How it works

gtheme stores themes in `~/.config/ghostty/themes/` and tracks the active theme with a symlink (`active.conf`). Your Ghostty config loads that symlink via `config-file`. Switching themes just updates the symlink — instant, no manual config editing needed.

The community registry lives in this repo. `gtheme add` pulls `.conf` files directly from GitHub — no server, no package manager, no dependencies beyond `curl` and `bash`.

---

## Bundled themes

gtheme ships with four themes to get you started:

| Name | Vibe | Font |
|------|------|------|
| `synthwave-noir` | neon city nights | JetBrainsMono Nerd Font |
| `ocean-depths` | bioluminescent abyss | CaskaydiaCove Nerd Font |
| `ember-ash` | forge heat, smoldering coal | FiraCode Nerd Font |
| `forest-dark` | old growth canopy, moss & rain | Hack Nerd Font |

---

## Creating your own theme

A gtheme theme is a plain Ghostty config file (`.conf`). Create a new file — name it whatever you want — and fill it in. At minimum, a theme sets some colors and a font. Here's a starter template:

```ini
# ── Font ──────────────────────────────────
font-family = JetBrainsMono Nerd Font
font-size = 13.5
font-feature = +calt
font-feature = +liga

# ── Cursor ────────────────────────────────
cursor-style = block
cursor-style-blink = true
cursor-color = #your-color

# ── Colors ────────────────────────────────
background = #your-bg
foreground = #your-fg

# 16 palette colors (0=black ... 15=bright white)
palette = 0=#...
palette = 1=#...   # red
palette = 2=#...   # green
palette = 3=#...   # yellow
palette = 4=#...   # blue
palette = 5=#...   # magenta
palette = 6=#...   # cyan
palette = 7=#...   # white
palette = 8=#...   # bright black
palette = 9=#...   # bright red
palette = 10=#...  # bright green
palette = 11=#...  # bright yellow
palette = 12=#...  # bright blue
palette = 13=#...  # bright magenta
palette = 14=#...  # bright cyan
palette = 15=#...  # bright white

# ── Window ────────────────────────────────
background-opacity = 0.90
background-blur = 20
window-padding-x = 16
window-padding-y = 12
window-padding-color = extend
window-theme = dark
window-colorspace = display-p3
```

Full list of available options: [ghostty.org/docs/config/reference](https://ghostty.org/docs/config/reference)

Once your file is ready, drop it into `~/.config/ghostty/themes/` and switch to it — the filename without `.conf` is the theme name:

```bash
cp my-theme.conf ~/.config/ghostty/themes/
gtheme my-theme
```

Already have a `.conf` from somewhere else? Same steps — just copy it in and switch.

---

## Sharing your theme

If you want to share your theme with the community so others can install it with `gtheme add`, run:

```bash
gtheme submit
```

This opens a submission form in your browser. The form has two distinct parts:

**Part 1 — Your theme config**
Paste your full `.conf` file. This is what gets added to the registry and loaded into Ghostty when someone installs your theme.

**Part 2 — Preview colors**
A small set of named colors picked from your `.conf` — background, foreground, prompt, directory, success, and error. These are used purely to render the live terminal preview and color swatches on the marketplace. They aren't pulled automatically from your config, so you'll fill them in manually. Each field explains which palette slot to look at.

Once submitted, the form auto-generates a PR. After it's reviewed and merged, your theme appears on the marketplace and is installable with `gtheme add <your-theme-name>`.

Browse community themes → **[unionpac.github.io/gtheme](https://unionpac.github.io/gtheme)**
