#!/usr/bin/env python3
"""Validate palette.json: derived values match hex, ANSI resolves, contrast floors
hold, and the generated swatches and README tables are current."""
import colorsys, json, pathlib, re, sys

import build

PALETTE = pathlib.Path(__file__).parent / "palette.json"

# ANSI bright slots are emphasis and chrome, not body text, so they sit at the
# WCAG non-text floor. Everything else that renders as text sits at AA.
BRIGHT = {"lime", "gold", "aqua", "flare", "sky", "ice", "lilac"}
# Backgrounds and deliberately low-emphasis tones (placeholders, line numbers).
EXEMPT = {"base", "deep", "surface", "overlay", "muted", "dim"}

# Tints the style guide recommends as backgrounds. Text sits on top of these, so
# they have to survive being composited over base. `heavy` is absent on purpose:
# at 50% it drops text below 3:1 on dark, so it is for marks and borders only.
TINTED = [("volt", "tint"), ("volt", "veil"), ("overlay", "veil"),
          ("ember", "tint"), ("jade", "tint")]


def rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def hsl(h):
    r, g, b = [c / 255 for c in rgb(h)]
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return [round(hh * 360), round(ss * 100), round(ll * 100)]


def luminance(h):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [lin(c / 255) for c in rgb(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def check():
    palette = json.loads(PALETTE.read_text())
    errors = []
    for flavour, data in palette["flavours"].items():
        colours = data["colours"]
        base = colours["base"]["hex"]
        for name, c in colours.items():
            if c["rgb"] != rgb(c["hex"]) or c["hsl"] != hsl(c["hex"]):
                errors.append(f"{flavour}/{name}: rgb or hsl does not match {c['hex']}")
            if name in EXEMPT:
                continue
            floor = 3.0 if name in BRIGHT else 4.5
            ratio = contrast(c["hex"], base)
            if ratio < floor:
                errors.append(
                    f"{flavour}/{name}: {c['hex']} is {ratio:.2f}:1 on base, needs {floor}:1")
        for slot, target in data["ansi"].items():
            if target not in colours:
                errors.append(f"{flavour}/ansi/{slot}: unknown colour '{target}'")

        for name, step in TINTED:
            tinted = build.composite(colours[name]["hex"], palette["alpha"][step], base)
            ratio = contrast(colours["text"]["hex"], tinted)
            if ratio < 4.5:
                errors.append(f"{flavour}: text on {name} at {step} over base "
                              f"({tinted}) is {ratio:.2f}:1, needs 4.5:1")

    steps = list(palette["alpha"].values())
    if steps != sorted(steps) or len(set(steps)) != len(steps):
        errors.append("alpha: steps must be unique and ordered low to high")
    if not all(0 < s < 1 for s in steps):
        errors.append("alpha: steps must sit between 0 and 1 exclusive")

    for name, data in build.swatches(palette).items():
        path = build.CIRCLES / name
        if not path.exists():
            errors.append(f"{path.relative_to(build.ROOT)}: missing, run ./build.py")
        elif path.read_bytes() != data:
            errors.append(f"{path.relative_to(build.ROOT)}: stale, run ./build.py")
    for extra in sorted(build.CIRCLES.glob("*.png")):
        if extra.name not in build.swatches(palette):
            errors.append(f"{extra.relative_to(build.ROOT)}: no such colour, run ./build.py")

    readme = build.README.read_text()
    if build.render_readme(palette, readme) != readme:
        errors.append("README.md: colour tables are stale, run ./build.py")

    # Prose documents reference swatches by path, so a renamed or removed colour
    # breaks them silently.
    for doc in sorted(build.ROOT.glob("docs/*.md")):
        for ref in set(re.findall(r"assets/palette/circles/([a-z0-9-]+\.png)", doc.read_text())):
            if not (build.CIRCLES / ref).exists():
                errors.append(f"{doc.relative_to(build.ROOT)}: references missing swatch {ref}")

    return errors


if __name__ == "__main__":
    problems = check()
    for p in problems:
        print(p, file=sys.stderr)
    print(f"{len(problems)} problem(s)" if problems else "palette ok")
    sys.exit(1 if problems else 0)
