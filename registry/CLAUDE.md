# Registry Notes

## index.json schema

```json
{
  "name":        "theme-name",          — lowercase, hyphens only
  "author":      "GitHubUsername",
  "description": "One sentence vibe.",
  "font":        "FontName Nerd Font",
  "tags":        ["dark", "neon"],      — from: dark, light, neon, minimal, warm, cool, nature, retro, monochrome, pastel
  "colors": {
    "background": "#rrggbb",            — theme background
    "foreground": "#rrggbb",            — main text color
    "prompt":     "#rrggbb",            — shell prompt / cursor color
    "directory":  "#rrggbb",            — ls directory color (usually palette 4)
    "success":    "#rrggbb",            — success output (usually palette 2)
    "error":      "#rrggbb"             — error output (usually palette 1)
  }
}
```

## Adding a community theme (after PR review)

1. Copy `.conf` from the PR to `registry/themes/<name>.conf`
2. Add entry to `registry/index.json` with all 6 named color fields
3. Commit and push — marketplace updates automatically (no deploy step needed)

## Important distinction

The `colors` fields in index.json are **display-only** — used by the marketplace for swatches and the preview modal. They are NOT pulled from the `.conf` file automatically. Submitters declare them separately in the issue form.

## Registry vs bundled themes

- `registry/themes/` — community themes, also includes copies of the 4 bundled themes
- `themes/` — the 4 bundled themes shipped with `install.sh`

Both directories should stay in sync for the bundled 4.
