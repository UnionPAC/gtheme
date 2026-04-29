# gtheme

A lightweight Ghostty theme switcher with a community theme library.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/UnionPAC/gtheme/main/install.sh | bash
```

## Usage

```bash
gtheme list                  # list installed themes
gtheme <name>                # switch to a theme
gtheme search [query]        # search the community registry
gtheme add <name>            # install a theme from the registry
gtheme remove <name>         # remove an installed theme
gtheme submit                # how to share your theme
```

After switching, reload Ghostty with `cmd + shift + ,` — no restart needed.

## Bundled themes

| Name | Vibe | Font |
|------|------|------|
| `synthwave-noir` | neon city nights | JetBrainsMono Nerd Font |
| `ocean-depths` | bioluminescent abyss | CaskaydiaCove Nerd Font |
| `ember-ash` | forge heat, smoldering coal | FiraCode Nerd Font |
| `forest-dark` | old growth canopy, moss & rain | Hack Nerd Font |

Install all fonts at once:

```bash
brew install --cask font-jetbrains-mono-nerd-font font-caskaydia-cove-nerd-font font-fira-code-nerd-font font-hack-nerd-font
```

## Share your theme

1. Fork this repo
2. Add your theme to `registry/themes/<your-theme-name>.conf`
3. Add an entry to `registry/index.json`
4. Open a pull request

Any valid [Ghostty config](https://ghostty.org/docs/config/reference) works as a theme file.

## How it works

gtheme stores themes in `~/.config/ghostty/themes/` and uses a symlink (`active.conf`) to track the active theme. Your main Ghostty config loads that symlink via `config-file`. Switching themes is just updating the symlink — instant, no config editing needed.

The community registry lives in this repo. `gtheme add` pulls theme files directly from GitHub — no server, no package manager, no dependencies beyond `curl` and `bash`.
