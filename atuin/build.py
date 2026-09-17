#!/usr/bin/env python3
"""Generate the Atuin themes from palette.json."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent

# Atuin's fifteen meanings, in the order its `Meaning` enum declares them.
# Values are palette colour names.
MEANINGS = {
    "AlertInfo": "jade",
    "AlertWarn": "amber",
    "AlertError": "ember",
    "Annotation": "soft",
    "Base": "text",
    "Guidance": "blue",
    "Important": "bright",
    "Title": "arc",
    "Muted": "subtle",
    "SyntaxCommand": "volt",
    "SyntaxFlag": "amber",
    "SyntaxString": "jade",
    "SyntaxVariable": "violet",
    "SyntaxOperator": "ice",
    "SyntaxComment": "subtle",
}


def theme(palette, flavour):
    data = palette["flavours"][flavour]
    colours = data["colours"]
    return "\n".join([
        f"# {data['name']} for Atuin. Generated from palette.json, do not edit.",
        "",
        "[theme]",
        f'name = "voltaic-{flavour}"',
        "",
        "[colors]",
        *(f'{key} = "{colours[name]["hex"]}"' for key, name in MEANINGS.items()),
    ]) + "\n"


def generate(palette):
    return {f"voltaic-{f}.toml": theme(palette, f) for f in palette["flavours"]}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"atuin/{name}")
