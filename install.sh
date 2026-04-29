#!/usr/bin/env bash
# gtheme installer
# curl -fsSL https://raw.githubusercontent.com/UnionPAC/gtheme/main/install.sh | bash

set -euo pipefail

REPO="https://raw.githubusercontent.com/UnionPAC/gtheme/main"
THEMES_DIR="$HOME/.config/ghostty/themes"
BIN_DIR="$HOME/.local/bin"
GHOSTTY_CONFIG="$HOME/.config/ghostty/config"

echo "Installing gtheme..."

# Create dirs
mkdir -p "$THEMES_DIR" "$BIN_DIR"

# Download CLI
curl -fsSL "$REPO/bin/gtheme" -o "$BIN_DIR/gtheme"
chmod +x "$BIN_DIR/gtheme"

# Download bundled themes (skip if already exists)
for theme in synthwave-noir ocean-depths ember-ash forest-dark; do
  dest="$THEMES_DIR/$theme.conf"
  if [[ ! -f "$dest" ]]; then
    echo "  + theme: $theme"
    curl -fsSL "$REPO/themes/$theme.conf" -o "$dest"
  else
    echo "  ~ theme: $theme (already exists, skipping)"
  fi
done

# Set default active theme if none set
if [[ ! -L "$THEMES_DIR/active.conf" ]]; then
  ln -sf "$THEMES_DIR/synthwave-noir.conf" "$THEMES_DIR/active.conf"
  echo "  * default theme: synthwave-noir"
fi

# Wire up Ghostty config if not already done
if [[ ! -f "$GHOSTTY_CONFIG" ]] || ! grep -q "config-file.*themes/active.conf" "$GHOSTTY_CONFIG" 2>/dev/null; then
  mkdir -p "$(dirname "$GHOSTTY_CONFIG")"
  echo "config-file = $THEMES_DIR/active.conf" >> "$GHOSTTY_CONFIG"
  echo "  * updated: $GHOSTTY_CONFIG"
fi

# PATH check
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
  echo ""
  echo "  Add gtheme to your PATH by adding this to your ~/.zshrc or ~/.bashrc:"
  echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "Done! gtheme is installed."
echo ""
echo "  gtheme list        — see available themes"
echo "  gtheme <name>      — switch theme"
echo "  gtheme search      — browse community themes"
echo ""
echo "Reload Ghostty after switching: cmd + shift + ,"
