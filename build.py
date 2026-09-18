#!/usr/bin/env python3
"""Generate the palette swatches and the README colour tables from palette.json."""
import importlib.util, json, pathlib, struct, zlib

ROOT = pathlib.Path(__file__).parent
PALETTE = ROOT / "palette.json"
README = ROOT / "README.md"
CIRCLES = ROOT / "assets" / "palette" / "circles"

SIZE = 48        # rendered at 20px, so retina displays get a clean downscale
SAMPLES = 4      # supersampling grid per pixel, for the anti-aliased edge


def circle_png(hexv):
    """A solid anti-aliased circle on a transparent background, as PNG bytes."""
    r, g, b = [int(hexv[i:i + 2], 16) for i in (1, 3, 5)]
    centre = SIZE / 2
    radius = centre - 0.5
    rows = bytearray()
    for y in range(SIZE):
        rows.append(0)  # filter type: none
        for x in range(SIZE):
            hits = sum(
                (x + (sx + 0.5) / SAMPLES - centre) ** 2
                + (y + (sy + 0.5) / SAMPLES - centre) ** 2 <= radius ** 2
                for sy in range(SAMPLES) for sx in range(SAMPLES)
            )
            rows += bytes((r, g, b, round(255 * hits / SAMPLES ** 2)))

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data)))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
            + chunk(b"IEND", b""))


def rgba(hexv, alpha):
    """8-digit hex, for ports that accept alpha directly."""
    return f"{hexv}{round(alpha * 255):02x}"


def composite(hexv, alpha, over):
    """Flatten a translucent colour onto an opaque one, for ports with no alpha.

    Blends in sRGB rather than linear light, matching what the editors and
    terminals consuming these values actually do.
    """
    fg = [int(hexv[i:i + 2], 16) for i in (1, 3, 5)]
    bg = [int(over[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(f * alpha + b * (1 - alpha)) for f, b in zip(fg, bg))


def swatches(palette):
    """Every swatch this palette needs, as {relative path: png bytes}."""
    return {
        f"{flavour}-{name}.png": circle_png(colour["hex"])
        for flavour, data in palette["flavours"].items()
        for name, colour in data["colours"].items()
    }


def table(palette, flavour, accent):
    cols = palette["flavours"][flavour]["colours"]
    picked = sorted((c for c in cols.items() if c[1]["accent"] == accent),
                    key=lambda kv: kv[1]["order"])
    out = ["| Colour | Hex | RGB | HSL | Role |", "| --- | --- | --- | --- | --- |"]
    for name, c in picked:
        r, s = c["rgb"], c["hsl"]
        swatch = (f'<img src="assets/palette/circles/{flavour}-{name}.png" '
                  f'width="20" height="20" alt=""/>')
        out.append(f"| {swatch} `{name}` | `{c['hex']}` | `rgb({r[0]}, {r[1]}, {r[2]})` "
                   f"| `hsl({s[0]}, {s[1]}%, {s[2]}%)` | {c['role']} |")
    return out


def render_readme(palette, text):
    """Replace every colour table in the README, leaving the prose untouched."""
    lines = text.splitlines()
    out, flavour, accent, i = [], None, None, 0
    while i < len(lines):
        line = lines[i]
        # Any heading closes the previous flavour's scope, so a `| Colour |` table
        # elsewhere in the file is left alone rather than overwritten.
        if line.startswith("#"):
            flavour = line.split()[-1].lower() if line.startswith("### Voltaic ") else None
        if line.strip() == "Accents:":
            accent = True
        if line.strip() == "Monochrome ramp:":
            accent = False
        if line.startswith("| Colour |") and flavour:
            out += table(palette, flavour, accent)
            while i < len(lines) and lines[i].startswith("|"):
                i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out) + "\n"


def ports():
    """Port directories, each owning a build.py with generate(palette) -> {name: text}."""
    for path in sorted(ROOT.glob("*/build.py")):
        spec = importlib.util.spec_from_file_location(f"port_{path.parent.name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        yield path.parent, module


def main():
    palette = json.loads(PALETTE.read_text())
    CIRCLES.mkdir(parents=True, exist_ok=True)
    written = swatches(palette)
    for name, data in written.items():
        (CIRCLES / name).write_bytes(data)
    for stale in CIRCLES.glob("*.png"):
        if stale.name not in written:
            stale.unlink()
    README.write_text(render_readme(palette, README.read_text()))
    print(f"{len(written)} swatches, README tables rebuilt")
    for directory, module in ports():
        generated = module.generate(palette)
        for name, content in generated.items():
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        # One line per file is fine for a handful; the icon port writes 1300.
        listing = (", ".join(sorted(generated)) if len(generated) <= 4
                   else f"{len(generated)} files")
        print(f"{directory.name}/: {listing}")


if __name__ == "__main__":
    main()
