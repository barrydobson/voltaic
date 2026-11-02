#!/usr/bin/env python3
"""Generate the Slack theme README from palette.json.

Slack themes are four hex codes pasted into the app, so the README is the
whole port. Generating it keeps the codes in step with the palette.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent

# Slack's four theme slots, in the order its Share button emits them.
# Values are palette colour names.
SLOTS = {
    "System navigation": "base",
    "Selected items": "volt",
    "Presence indication": "jade",
    "Notifications": "ember",
}


def flavour_section(palette, flavour):
    data = palette["flavours"][flavour]
    hexes = [data["colours"][name]["hex"].upper() for name in SLOTS.values()]
    rows = [
        f'| {slot} | `{name}` | <img src="../assets/palette/circles/{flavour}-{name}.png" '
        f'width="16" height="16" alt=""/> `{hexv}` |'
        for (slot, name), hexv in zip(SLOTS.items(), hexes)
    ]
    return [
        f"## {data['name']}",
        "",
        "Theme string:",
        "",
        "```text",
        ", ".join(hexes),
        "```",
        "",
        "| Slack setting | Colour | Hex |",
        "| --- | --- | --- |",
        *rows,
        "",
    ]


def readme(palette):
    sections = [line for f in palette["flavours"] for line in flavour_section(palette, f)]
    return "\n".join([
        "<!-- Generated from palette.json by slack/build.py, do not edit. -->",
        "# Voltaic for Slack",
        "",
        "Slack has no theme files. A custom theme is four colours set in the app,",
        "so this README is the whole port.",
        "",
        "## Install",
        "",
        "1. Open **Preferences > Appearance > Custom theme**.",
        "2. Click **Import** and paste the theme string for your flavour.",
        "3. Set Slack's own light/dark mode to match the flavour.",
        "",
        "Or set each colour by hand with the pencil button beside it.",
        "",
        "Slack warns that it may adjust imported colours for contrast, but both",
        "strings import unchanged. Untick **Window gradient** to keep the sidebar",
        "a flat `base`.",
        "",
        *sections,
        "## Mapping",
        "",
        "- **System navigation is `base`**, the application background in the",
        "  [style guide](../docs/style-guide.md).",
        "- **Selected items is `volt`**, the focus and active-state colour.",
        "- **Presence is `jade`**, because being online is a success state.",
        "- **Notifications is `ember`**, so unread badges read as needing attention.",
        "",
        "## Customising",
        "",
        "Do not edit this README. It is generated from",
        "[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`",
        "fails if the two disagree. Change the palette and run `./build.py` from the",
        "repository root.",
    ]) + "\n"


def generate(palette):
    return {"README.md": readme(palette)}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"slack/{name}")
