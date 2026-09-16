#!/usr/bin/env python3
"""Generate the Ghostty themes from palette.json."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent

# Terminal slot order is fixed by the spec, not by the palette, so it is spelled
# out here rather than taken from the key order of `ansi`.
SLOTS = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
         "bright_black", "bright_red", "bright_green", "bright_yellow",
         "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]


def theme(palette, flavour):
    data = palette["flavours"][flavour]
    c = {k: v["hex"] for k, v in data["colours"].items()}
    lines = [
        f"# {data['name']}. Generated from palette.json, do not edit.",
        "",
        f"background = {c['deep']}",
        f"foreground = {c['text']}",
        "",
        f"cursor-color = {c['volt']}",
        f"cursor-text = {c['deep']}",
        "",
        f"selection-background = {c['volt']}",
        f"selection-foreground = {c['deep']}",
        "",
        # Ghostty takes no alpha, so the search tint is flattened onto the canvas.
        f"search-background = {core.composite(c['volt'], palette['alpha']['tint'], c['deep'])}",
        f"search-foreground = {c['text']}",
        f"search-selected-background = {c['volt']}",
        f"search-selected-foreground = {c['deep']}",
        "",
        f"split-divider-color = {c['overlay']}",
        f"unfocused-split-fill = {c['base']}",
        "",
    ]
    lines += [f"palette = {i}={c[data['ansi'][slot]]}" for i, slot in enumerate(SLOTS)]
    return "\n".join(lines) + "\n"


def generate(palette):
    out = {f"voltaic-{f}": theme(palette, f) for f in palette["flavours"]}
    # An 8-digit hex from rgba() would make Ghostty reject the whole theme.
    assert not re.search(r"#[0-9a-f]{8}", "".join(out.values())), "Ghostty takes no alpha"
    return out


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"ghostty/{name}")
