# Web App Notes — docs/index.html

Single-file GitHub Pages site. Fetches `registry/index.json` from raw GitHub URL on load. No build step, no framework.

## Color schema

Each theme in index.json has 6 named color fields used exclusively for the marketplace display:

```json
"colors": {
  "background": "#0d0010",   — card background
  "foreground": "#f0e8ff",   — card text
  "prompt":     "#ff006e",   — prompt char, card name, swatch, border tints
  "directory":  "#00e5ff",   — ls directory color in preview modal
  "success":    "#00ff9f",   — success line in preview modal
  "error":      "#ff006e"    — error line in preview modal
}
```

These are separate from the actual `.conf` file — they exist purely to drive the UI. Community submitters fill them in manually on the issue form.

## Card design

- Card background = `colors.background`
- Swatch bar = `[prompt, directory, success, error, foreground]` — 5 swatches
- Card name, Preview button, add command = `colors.prompt`
- Description text = `colors.foreground` at 80% opacity
- Border = `colors.prompt` at ~13% opacity
- Hover = `box-shadow` only (no translateY — translateY caused a blue flash by revealing page background)

## Preview modal

Opened by the Preview button on each card. Looks like a macOS terminal window:
- Fake titlebar with traffic light dots + theme name
- `ls` output: directories in `colors.directory`, files in `colors.foreground`
- `git log` with hashes in `colors.prompt`
- Success line in `colors.success`
- Error line in `colors.error`
- Blinking cursor block in `colors.prompt`
- Close: click outside or press Escape

## Known limitation

Positional color assignment works well for the 4 bundled themes but community themes might use their colors differently. The named schema (`prompt`, `directory`, etc.) was introduced to make this explicit — submitters declare which of their palette colors serves each role.

## Page background

`--bg: #0d0d14` — very dark blue-black. Theme card backgrounds that are also very dark (synthwave `#0d0010`, ocean `#020810`) can look similar to the page. This is expected — the swatch bar and colored name/text differentiate them.
