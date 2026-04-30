# gtheme

A lightweight theme switcher for [Ghostty](https://ghostty.org) with a community theme library.

```bash
curl -fsSL https://raw.githubusercontent.com/UnionPAC/gtheme/main/install.sh | bash
```

---

## Commands

```bash
gtheme list                  # list your installed themes
gtheme <name>                # switch to a theme
gtheme search [query]        # search the community registry
gtheme add <name>            # install a theme from the community
gtheme remove <name>         # remove an installed theme
gtheme update                # update gtheme to the latest version
gtheme submit                # share your theme with the community
gtheme version               # show the current version
gtheme help                  # show all commands
```

gtheme checks for updates automatically once a day in the background — you'll see a one-line notice the next time you run any command after an update lands.

After switching, reload Ghostty with `cmd + shift + ,` — no restart needed.

---

## Creating a theme

A gtheme theme is just a Ghostty config file (`.conf`). Anything you can put in your main Ghostty config, you can put in a theme. At minimum, a theme sets some colors and a font.

Here's a starter template:

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

---

## Using a local theme

Once you've created a `.conf` file, drop it into your themes folder and gtheme picks it up automatically:

```bash
cp my-theme.conf ~/.config/ghostty/themes/

# switch to it
gtheme my-theme
```

That's it. Your local themes and community themes live in the same place and work exactly the same way.

---

## Sharing your theme

If you want to share your theme with the community so others can install it with `gtheme add`, run:

```bash
gtheme submit
```

This opens a short form in your browser. Fill in your theme name, description, font, a few accent colors (for the preview swatches on the site), and paste your `.conf`. We'll review it and add it to the registry.

Browse community themes → **[unionpac.github.io/gtheme](https://unionpac.github.io/gtheme)**

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

## How it works

gtheme stores themes in `~/.config/ghostty/themes/` and tracks the active theme with a symlink (`active.conf`). Your Ghostty config loads that symlink via `config-file`. Switching themes just updates the symlink — instant, no manual config editing needed.

The community registry lives in this repo. `gtheme add` pulls `.conf` files directly from GitHub — no server, no package manager, no dependencies beyond `curl` and `bash`.
