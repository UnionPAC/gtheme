# Themes Notes

## The sync issue — important

`themes/` in this repo and `~/.config/ghostty/themes/` are completely separate files. The installer copies them once. After any theme edit in the repo, always sync locally:

```bash
cp themes/synthwave-noir.conf ~/.config/ghostty/themes/
cp themes/ocean-depths.conf ~/.config/ghostty/themes/
cp themes/ember-ash.conf ~/.config/ghostty/themes/
cp themes/forest-dark.conf ~/.config/ghostty/themes/
# reload Ghostty: cmd + shift + ,
```

Failing to sync = terminal shows old theme, card on marketplace shows new one. Confusing.

## Bundled themes

| Name | Vibe | Font | Background | Prompt |
|------|------|------|------------|--------|
| synthwave-noir | Rain-soaked neon city, hot pink + electric purple | JetBrainsMono Nerd Font | `#0d0010` deep purple-black | `#ff006e` hot pink |
| ocean-depths | Bioluminescent abyss, cold and dark | CaskaydiaCove Nerd Font | `#020810` near-black blue | `#00ffee` aqua |
| ember-ash | Forge heat, smoldering coal, warm cream | FiraCode Nerd Font | `#100a04` dark charcoal | `#ff7700` ember orange |
| forest-dark | Old growth canopy, green-tinted everything | Hack Nerd Font | `#050c05` forest black | `#00ff41` lime |

## Font cask names (Homebrew)

```
JetBrainsMono Nerd Font  → font-jetbrains-mono-nerd-font
CaskaydiaCove Nerd Font  → font-caskaydia-cove-nerd-font
FiraCode Nerd Font       → font-fira-code-nerd-font
Hack Nerd Font           → font-hack-nerd-font
```

## Color philosophy

Each theme should have a distinct personality visible at a glance:
- **synthwave-noir**: electric, dangerous — purple-black bg, all neon accents
- **ocean-depths**: cold, sparse — near-black bg, mostly muted except bioluminescent teal glow
- **ember-ash**: warm, crafted — charcoal bg, warm cream foreground, amber/orange accents. Most distinct of the four.
- **forest-dark**: organic — the "white" (palette 7) is pale leaf green `#a0cc88`. Makes it unmistakably different.

## What fixed color 7 (white)

All themes previously had color 7 too dark — nearly invisible against the background. Each theme now has a color 7 that matches its personality: lavender-white (synthwave), cold blue-grey (ocean), warm parchment (ember), pale leaf green (forest).
