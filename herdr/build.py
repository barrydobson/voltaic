#!/usr/bin/env python3
"""Generate the herdr custom theme from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent
OUTPUT = "voltaic.toml"

HEADER = """\
# Voltaic for herdr. Generated from palette.json, do not edit.
#
# Paste into ~/.config/herdr/config.toml, below the rest of the [theme] table.
# Dark only: these are the dark flavour's values, so leave theme.auto_switch off.\
"""

# herdr's token names are Catppuccin hue names, but its Palette doc comments give
# each one a job. The job is what is mapped here, not the name.
TOKENS = [
    ("accent", "volt"),           # highlight, active borders
    ("panel_bg", "surface"),      # tab bar, floating panels, overlays, modals
    ("sidebar_bg", "base"),       # desktop sidebar background
    ("active_row_bg", "overlay"),  # active space and focused agent rows
    ("selection_bg", "volt at tint over base"),  # navigate-mode cursor row in the sidebar
    ("surface0", "overlay"),      # selected and focused items
    ("surface1", "muted"),        # hover and active states
    ("surface_dim", "muted"),     # separators
    ("overlay0", "subtle"),       # muted text: secondary info, numbers
    ("overlay1", "subtle"),       # slightly brighter muted text
    ("text", "text"),             # primary text
    ("subtext0", "soft"),         # unfocused rows, dim labels
    ("mauve", "violet"),          # git branch and other secondary labels
    ("green", "jade"),            # idle
    ("yellow", "amber"),          # working
    ("red", "ember"),             # blocked
    ("blue", "blue"),             # unseen notifications
    ("teal", "teal"),             # done
    ("peach", "bronze"),          # interrupted
]


def generate(palette):
    c = {k: v["hex"] for k, v in palette["flavours"]["dark"]["colours"].items()}
    # herdr takes no alpha, so the cursor row's accent tint is flattened onto base.
    c["volt at tint over base"] = core.composite(c["volt"], palette["alpha"]["tint"], c["base"])
    lines = [HEADER, "", "[theme.custom]"]
    lines += [f'{token} = "{c[colour]}"  # {colour}' for token, colour in TOKENS]
    return {OUTPUT: "\n".join(lines) + "\n"}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"herdr/{name}")
