#!/usr/bin/env python3
"""Generate the Starship palettes from palette.json."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent
OUTPUT = "voltaic.toml"

HEADER = """\
# Voltaic for Starship. Generated from palette.json, do not edit.
#
# Paste into ~/.config/starship/starship.toml. The `palette` line must sit above
# every table in the file, and the palette tables below it. Delete the flavour
# you are not using, or keep both and swap the `palette` value.

palette = "voltaic_dark"\
"""


def generate(palette):
    out = [HEADER]
    for flavour, data in palette["flavours"].items():
        ordered = sorted(data["colours"].items(), key=lambda kv: kv[1]["order"])
        out.append(f"[palettes.voltaic_{flavour}]\n"
                   + "\n".join(f'{name} = "{c["hex"]}"' for name, c in ordered))
    return {OUTPUT: "\n\n".join(out) + "\n"}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"starship/{name}")
