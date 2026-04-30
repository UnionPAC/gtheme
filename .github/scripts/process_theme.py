#!/usr/bin/env python3
"""
Parses a gtheme theme submission issue and opens a PR.
Runs inside GitHub Actions — expects env vars:
  ISSUE_BODY, ISSUE_NUMBER, ISSUE_USER, GH_TOKEN
"""

import os
import re
import json
import subprocess
import sys

ISSUE_BODY   = os.environ["ISSUE_BODY"]
ISSUE_NUMBER = os.environ["ISSUE_NUMBER"]
ISSUE_USER   = os.environ["ISSUE_USER"]

# ── helpers ───────────────────────────────────────────────────────────────────

def extract_field(body, label):
    """Pull the value under a '### Label' heading."""
    pattern = rf"### {re.escape(label)}\s*\n\n(.*?)(?=\n\n###|\Z)"
    m = re.search(pattern, body, re.DOTALL)
    return m.group(1).strip() if m else ""

def strip_code_fence(text):
    """Remove ``` or ```shell fences if present."""
    text = re.sub(r"^```[a-z]*\n?", "", text.strip())
    text = re.sub(r"\n?```$", "", text)
    return text.strip()

def is_hex(value):
    return bool(re.match(r"^#[0-9a-fA-F]{6}$", value.strip()))

def comment(msg):
    subprocess.run(
        ["gh", "issue", "comment", ISSUE_NUMBER, "--body", msg],
        check=False,
    )

def fail(msg):
    comment(f"❌ **Theme submission failed**\n\n{msg}\n\nPlease edit your issue to fix the problem.")
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)

# ── parse fields ──────────────────────────────────────────────────────────────

name        = extract_field(ISSUE_BODY, "Theme name")
description = extract_field(ISSUE_BODY, "Description")
font        = extract_field(ISSUE_BODY, "Font family")
tags_raw    = extract_field(ISSUE_BODY, "Tags")
config      = strip_code_fence(extract_field(ISSUE_BODY, "Theme config (.conf)"))

# Named preview colors
color_background = extract_field(ISSUE_BODY, "Background color")
color_foreground = extract_field(ISSUE_BODY, "Foreground color")
color_prompt     = extract_field(ISSUE_BODY, "Prompt color")
color_directory  = extract_field(ISSUE_BODY, "Directory color")
color_success    = extract_field(ISSUE_BODY, "Success color")
color_error      = extract_field(ISSUE_BODY, "Error color")

# ── validate ──────────────────────────────────────────────────────────────────

if not name:
    fail("Could not read **Theme name** from the submission form.")

if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", name):
    fail(
        f"**Theme name** `{name}` is invalid.\n\n"
        "Names must be lowercase letters, numbers, and hyphens only "
        "(e.g. `my-cool-theme`)."
    )

if os.path.exists(f"registry/themes/{name}.conf"):
    fail(
        f"A theme named `{name}` already exists in the registry.\n\n"
        "Please choose a unique name."
    )

if not config:
    fail("Could not read the **Theme config** from the submission form.")

color_fields = {
    "Background color": color_background,
    "Foreground color": color_foreground,
    "Prompt color":     color_prompt,
    "Directory color":  color_directory,
    "Success color":    color_success,
    "Error color":      color_error,
}

for field_name, value in color_fields.items():
    if not value or not is_hex(value):
        fail(
            f"**{field_name}** `{value}` doesn't look like a valid hex color.\n\n"
            "Use 6-digit hex format, e.g. `#0b0d1a`."
        )

# Parse tags
tags = [t.strip() for t in re.split(r"[,\n]", tags_raw) if t.strip()]

# ── write files ───────────────────────────────────────────────────────────────

conf_path = f"registry/themes/{name}.conf"
with open(conf_path, "w") as f:
    f.write(config + "\n")

with open("registry/index.json", "r") as f:
    index = json.load(f)

index.append({
    "name":        name,
    "author":      ISSUE_USER,
    "description": description,
    "font":        font,
    "tags":        tags,
    "colors": {
        "background": color_background.strip(),
        "foreground": color_foreground.strip(),
        "prompt":     color_prompt.strip(),
        "directory":  color_directory.strip(),
        "success":    color_success.strip(),
        "error":      color_error.strip(),
    },
})

with open("registry/index.json", "w") as f:
    json.dump(index, f, indent=2)
    f.write("\n")

# ── create branch and PR ──────────────────────────────────────────────────────

branch = f"theme-submission/issue-{ISSUE_NUMBER}-{name}"

subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

# Close any existing PR for this issue (re-submission after an edit)
existing = subprocess.run(
    ["gh", "pr", "list", "--search", f"issue-{ISSUE_NUMBER}", "--json", "number,headRefName"],
    capture_output=True, text=True,
)
for pr in json.loads(existing.stdout or "[]"):
    if f"issue-{ISSUE_NUMBER}" in pr["headRefName"]:
        subprocess.run(["gh", "pr", "close", str(pr["number"]), "--delete-branch"], check=False)

subprocess.run(["git", "checkout", "-b", branch], check=True)
subprocess.run(["git", "add", conf_path, "registry/index.json"], check=True)
subprocess.run(["git", "commit", "-m", f"Add theme: {name} (submitted by @{ISSUE_USER})"], check=True)
subprocess.run(["git", "push", "origin", branch], check=True)

pr_body = f"""## {name}

Submitted by @{ISSUE_USER} via issue #{ISSUE_NUMBER}.

**Description:** {description}
**Font:** {font}
**Tags:** {", ".join(tags)}

| Color | Hex |
|-------|-----|
| Background | `{color_background}` |
| Foreground | `{color_foreground}` |
| Prompt | `{color_prompt}` |
| Directory | `{color_directory}` |
| Success | `{color_success}` |
| Error | `{color_error}` |

---

Closes #{ISSUE_NUMBER}
"""

result = subprocess.run(
    [
        "gh", "pr", "create",
        "--title", f"Add theme: {name}",
        "--body", pr_body,
        "--head", branch,
        "--base", "main",
        "--label", "theme-submission",
    ],
    capture_output=True,
    text=True,
)

pr_url = result.stdout.strip()

comment(
    f"✅ **Theme received!** A PR has been opened for review: {pr_url}\n\n"
    f"Once merged, `{name}` will appear on the marketplace and be installable with:\n"
    f"```\ngtheme add {name}\n```\n\n"
    f"_If you need to make changes, just edit this issue and a new PR will be created automatically._"
)

print(f"PR created: {pr_url}")
