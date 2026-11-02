#!/usr/bin/env python3
"""Generate the Herdr app themes from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent

# Terminal slot order is fixed by the spec, not by the palette, so it is spelled
# out here rather than taken from the key order of `ansi`.
SLOTS = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
         "bright_black", "bright_red", "bright_green", "bright_yellow",
         "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]

# Herdr derives its panel colours from the terminal ones, then lets `colors`
# override them by name. Every name it documents is set, so nothing is derived.
COLORS = [
    ("canvas", "base"),             # behind cards
    ("chrome", "base"),             # sidebars and bars
    ("surface", "surface"),         # panels
    ("popover", "surface"),         # menus, dialogs
    ("raised", "overlay"),          # elevated controls, disabled buttons
    ("hover", "muted"),             # hover over a row or control
    ("selected", "overlay"),        # selected row
    ("border", "overlay"),          # dividers, inactive borders
    ("input", "muted"),             # input borders, stronger than `border`
    ("foreground", "text"),         # primary text
    ("muted", "soft"),              # secondary text
    ("dim", "subtle"),              # hints, numbers, key captions
    ("accent", "volt"),             # highlights, active borders
    ("accent_foreground", "deep"),  # text on an accent fill
    ("solid", "volt"),              # primary button
    ("solid_foreground", "deep"),   # primary button text
    ("ring", "volt"),               # focus ring
    ("working", "amber"),
    ("blocked", "ember"),
    ("done", "teal"),
    ("idle", "jade"),
    ("unknown", "subtle"),
]


def theme(palette, flavour):
    data = palette["flavours"][flavour]
    c = {k: v["hex"] for k, v in data["colours"].items()}
    return {
        "background": c["deep"],
        "foreground": c["text"],
        # Herdr keeps the text colour under a selection, so a solid `volt` fill
        # would hide `volt` text. The tint over the canvas keeps every colour legible.
        "selection": core.composite(c["volt"], palette["alpha"]["tint"], c["deep"]),
        "cursor": c["volt"],
        "ansi": [c[data["ansi"][slot]] for slot in SLOTS],
        "colors": {name: c[colour] for name, colour in COLORS},
    }


def generate(palette):
    return {f"voltaic-{f}.json": json.dumps(theme(palette, f), indent=2) + "\n"
            for f in palette["flavours"]}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"herdr-app/{name}")
