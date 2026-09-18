#!/usr/bin/env python3
"""Generate the Zed icon theme from palette.json.

The artwork is vendored from catppuccin/vscode-icons (MIT, see
src/LICENCE.catppuccin). Its `css-variables` set tags every stroke with a
Catppuccin colour name rather than a hex, so porting is a name-to-name map
rather than a redraw. `src/mapping.json` is the same project's generated Zed
mapping with the flavour directory replaced by a placeholder.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent
SRC = HERE / "src"
OUTPUT = "icon_themes/voltaic-icons.json"

VARIABLE = re.compile(r"var\(--vscode-ctp-([a-z0-9]+)\)")

# Catppuccin colour name to Voltaic colour name. Hue first, then the style
# guide's job for that colour: directories land on `blue`, plain files on
# `text`, de-emphasised detail strokes on `subtle`.
#
# Four Catppuccin names merge in pairs. `red`/`maroon` and `pink`/`flamingo`
# are near-neighbours upstream and Voltaic has one colour in each band, so the
# pairs share one. Neither pair ever appears in the same icon, so nothing that
# was two colours becomes one; `collisions()` below proves it.
COLOURS = {
    "text": "text",
    "overlay1": "subtle",
    "rosewater": "soft",
    "flamingo": "flare",
    "pink": "flare",
    "mauve": "violet",
    "red": "ember",
    "maroon": "ember",
    "peach": "bronze",
    "yellow": "amber",
    "green": "jade",
    "teal": "teal",
    "sky": "cyan",
    "sapphire": "sky",
    "blue": "blue",
    "lavender": "lilac",
}


# The style guide puts directories on `blue`. Upstream draws the generic folder
# in its text colour, the same as the generic file; the named folder icons
# already carry colours of their own and are left alone.
OVERRIDES = {"_folder.svg": "blue", "_folder_open.svg": "blue"}


def sources():
    """Every vendored icon, as {filename: svg text}."""
    return {path.name: path.read_text() for path in sorted(SRC.glob("icons/*.svg"))}


def recolour(name, svg, colours):
    """Resolve an icon's colour variables against one flavour."""
    forced = OVERRIDES.get(name)
    return VARIABLE.sub(
        lambda m: colours[forced or COLOURS[m.group(1)]]["hex"], svg)


def collisions(icons, colours):
    """Icons where two upstream colours resolve to the same hex.

    A merge is only safe while the merged names stay out of each other's icons.
    An upstream redraw, or a palette change that flattens two Voltaic colours
    into one hex, would silently turn a two-tone icon into a solid one.
    """
    for name, svg in icons.items():
        if name in OVERRIDES:
            continue
        seen = {}
        for variable in set(VARIABLE.findall(svg)):
            hexv = colours[COLOURS[variable]]["hex"]
            if hexv in seen:
                yield f"{name}: {seen[hexv]} and {variable} both resolve to {hexv}"
            seen[hexv] = variable


def theme(palette, flavour, mapping):
    return {
        "name": palette["flavours"][flavour]["name"],
        "appearance": palette["flavours"][flavour]["appearance"],
        **json.loads(json.dumps(mapping).replace("{flavour}", flavour)),
    }


def generate(palette):
    icons = sources()
    mapping = json.loads((SRC / "mapping.json").read_text())
    out = {}
    for flavour in ("dark", "light"):
        colours = palette["flavours"][flavour]["colours"]
        clashes = list(collisions(icons, colours))
        if clashes:
            raise ValueError(f"{flavour}: " + "; ".join(clashes))
        for name, svg in icons.items():
            out[f"icons/{flavour}/{name}"] = recolour(name, svg, colours)
    out[OUTPUT] = json.dumps({
        "$schema": "https://zed.dev/schema/icon_themes/v0.2.0.json",
        "name": f"{palette['name']} Icons",
        "author": palette["author"],
        "themes": [theme(palette, f, mapping) for f in ("dark", "light")],
    }, indent=2) + "\n"
    return out


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        path = HERE / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    print(f"zed-icons/: {len(sources()) * 2} icons, {OUTPUT}")
