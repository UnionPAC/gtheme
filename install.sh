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

# PATH setup — auto-add to shell config if needed
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
  # Pick the right shell config file
  if [[ "$SHELL" == */zsh ]]; then
    SHELL_RC="$HOME/.zshrc"
  elif [[ "$SHELL" == */bash ]]; then
    SHELL_RC="$HOME/.bashrc"
  else
    SHELL_RC="$HOME/.profile"
  fi

  PATH_LINE="export PATH=\"\$HOME/.local/bin:\$PATH\""

  # Create the file if it doesn't exist, then append if the line isn't already there
  touch "$SHELL_RC"
  if ! grep -qF '.local/bin' "$SHELL_RC"; then
    echo "" >> "$SHELL_RC"
    echo "# Added by gtheme installer" >> "$SHELL_RC"
    echo "$PATH_LINE" >> "$SHELL_RC"
    echo "  * PATH updated in $SHELL_RC"
  fi

  echo ""
  echo "  To use gtheme right now, run:"
  echo "    source $SHELL_RC"
  echo "  (Or just open a new terminal — it'll work automatically)"
fi

echo ""
echo "Done! gtheme is installed."
echo "Run 'gtheme help' to see what you can do."
