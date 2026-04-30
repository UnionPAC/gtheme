# GitHub Actions & Templates Notes

## Submission pipeline overview

1. User runs `gtheme submit` → browser opens issue form
2. User fills out form, submits → GitHub creates issue with `theme-submission` label (auto-applied by template)
3. Action triggers → `.github/scripts/process_theme.py` runs
4. Script validates, creates `.conf` + updates `index.json`, opens PR
5. Script comments on issue with PR link or error message
6. If user edits the issue → action re-triggers, closes old PR, opens new one
7. Reviewer merges PR → theme live on marketplace

## Workflow trigger

`.github/workflows/process-theme-submission.yml` triggers on:
- `issues: [opened, labeled, edited]`
- Filtered by: `contains(github.event.issue.labels.*.name, 'theme-submission')`

The `theme-submission` label **must exist** on the repo — it was created with color `#7B6FFF`. Without it, the template can't apply it and the action never fires.

## process_theme.py — what it does

- Parses issue body by `### Field Label` headings
- Validates: name format (lowercase/hyphens), name uniqueness, valid hex for all 6 color fields, non-empty config
- On failure: comments on issue with specific error, exits — no PR created
- On success: creates branch `theme-submission/issue-{N}-{name}`, commits files, opens PR, comments with PR link
- On re-edit: finds and closes existing PR for this issue before opening a new one

## Issue template fields

```
Theme name         — lowercase, hyphens only
Description        — one sentence
Font family        — font-family value from .conf
Background color   — hex
Foreground color   — hex
Prompt color       — hex (cursor-color or bright accent)
Directory color    — hex (usually palette = 4)
Success color      — hex (usually palette = 2)
Error color        — hex (usually palette = 1)
Tags               — multi-select dropdown
Theme config       — full .conf pasted as code block
Checklist          — 3 required confirmations
```

## PR description format

The auto-generated PR includes a color table (all 6 named colors), author, description, tags, and `Closes #N` to auto-close the issue on merge.
