#!/usr/bin/env python3
"""Generate the Obsidian theme from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent
THEME = "theme.css"
MANIFEST = "manifest.json"

# Obsidian compares this against the installed copy to offer an update, so bump
# it on a rebuild that is meant to ship.
VERSION = "1.0.0"
# Callout type colours take a colour value rather than an RGB triplet from 1.13.
MIN_APP_VERSION = "1.13.0"

# Obsidian's neutral ramp, background end to foreground end. Both flavours take
# the same palette names; only the hexes run the other way.
RAMP = {"00": "deep", "05": "base", "10": "base", "20": "base", "25": "surface",
        "30": "overlay", "35": "muted", "40": "muted", "50": "dim", "60": "subtle",
        "70": "soft", "100": "text"}

# The eight named slots. Callouts, Canvas colours and several plugins resolve
# through these, so mapping them once covers most of the app.
NAMED = {"red": "ember", "orange": "bronze", "yellow": "amber", "green": "jade",
         "cyan": "cyan", "blue": "blue", "purple": "violet", "pink": "flare"}

# Syntax highlighting. Obsidian groups tokens more coarsely than an editor does;
# each variable's own description decides which style guide row it takes.
CODE = {"normal": "text", "comment": "subtle", "function": "blue",
        "important": "amber", "keyword": "volt", "operator": "ice",
        "property": "blue", "punctuation": "subtle", "string": "jade",
        "tag": "ember", "value": "ember"}

RULES = """/* Code blocks and inline chips take an outline rather than a fill. Every tone
   lighter than the canvas drops `subtle` comments under 4.5:1 on dark: 4.05 on
   `surface`, 3.41 on `overlay`. The border costs nothing and still reads. */
body {
  --code-border-width: 1px;
}

/* Inline code has no variable of its own: `--code-normal` is also the plain
   text inside a fenced block, which has to stay neutral. Obsidian's own
   `.markdown-rendered code` and `.cm-s-obsidian span.cm-inline-code` outrank a
   bare element selector, so these match their shape to win on order. */
.markdown-rendered :not(pre) > code,
.cm-s-obsidian span.cm-inline-code {
  color: var(--color-yellow);
}

/* Menus and suggestion popups take `--background-secondary`, which is the
   sidebar tone. The style guide floats them on `surface` instead. */
.menu,
.suggestion-container {
  background-color: var(--color-base-25);
}
"""


def variables(palette, flavour):
    """The flavour's custom properties, as (section title, {property: value})."""
    colours = palette["flavours"][flavour]["colours"]
    c = {k: v["hex"] for k, v in colours.items()}
    a = palette["alpha"]
    h, s, l = colours["volt"]["hsl"]

    def tint(name, step):
        """8-digit hex. Obsidian is a browser, so alpha needs no compositing."""
        return core.rgba(c[name], a[step])

    def triplet(name):
        return ", ".join(str(v) for v in colours[name]["rgb"])

    ramp = {f"--color-base-{step}": c[name] for step, name in RAMP.items()}
    named = {f"--color-{slot}": c[name] for slot, name in NAMED.items()}
    named |= {f"--color-{slot}-rgb": triplet(name) for slot, name in NAMED.items()}
    return [
        ("Neutral ramp", ramp),
        # The -rgb pairs are deprecated as of 1.13 but still read by plugins and
        # by Obsidian's own error and success fills.
        ("Named colours", named),
        ("Accent", {
            "--accent-h": str(h),
            "--accent-s": f"{s}%",
            "--accent-l": f"{l}%",
            "--color-accent": c["volt"],
            "--color-accent-1": c["volt"],
            "--color-accent-2": c["arc"],
            "--color-accent-hsl": f"{h}, {s}%, {l}%",
            "--interactive-accent": c["volt"],
            "--interactive-accent-hover": c["arc"],
            "--interactive-accent-hsl": f"{h}, {s}%, {l}%",
            "--text-on-accent": c["deep"],
            "--text-on-accent-inverted": c["bright"],
        }),
        ("Surfaces", {
            "--background-modifier-hover": c["overlay"],
            "--background-modifier-active-hover": c["muted"],
            "--background-modifier-border": c["overlay"],
            "--background-modifier-border-hover": c["muted"],
            "--background-modifier-border-focus": c["volt"],
            "--background-modifier-error": c["ember"],
            "--background-modifier-error-rgb": triplet("ember"),
            "--background-modifier-error-hover": c["flare"],
            "--background-modifier-success": c["jade"],
            "--background-modifier-success-rgb": triplet("jade"),
            "--background-modifier-message": c["surface"],
            "--background-modifier-form-field": c["surface"],
            "--modal-background": c["surface"],
            "--interactive-normal": c["surface"],
            "--interactive-hover": c["overlay"],
        }),
        ("Text", {
            "--text-normal": c["text"],
            "--text-muted": c["soft"],
            "--text-faint": c["dim"],
            "--text-success": c["jade"],
            "--text-warning": c["amber"],
            "--text-error": c["ember"],
            "--text-accent": c["arc"],
            "--text-accent-hover": c["volt"],
            "--text-selection": tint("volt", "tint"),
            "--text-highlight-bg": tint("amber", "tint"),
            "--caret-color": c["volt"],
        }),
        ("Icons, scrollbars and guides", {
            "--icon-color": c["soft"],
            "--icon-color-hover": c["text"],
            "--icon-color-active": c["arc"],
            "--icon-color-focused": c["text"],
            "--collapse-icon-color": c["dim"],
            "--collapse-icon-color-collapsed": c["soft"],
            "--scrollbar-bg": "transparent",
            "--scrollbar-thumb-bg": tint("volt", "faint"),
            "--scrollbar-active-thumb-bg": tint("volt", "wash"),
            "--indentation-guide-color": c["overlay"],
            "--indentation-guide-color-active": c["muted"],
        }),
        ("File explorer", {
            "--nav-item-color": c["soft"],
            "--nav-item-color-hover": c["text"],
            "--nav-item-color-active": c["text"],
            "--nav-item-color-selected": c["text"],
            "--nav-item-color-highlighted": c["arc"],
            "--nav-item-background-hover": c["overlay"],
            "--nav-item-background-active": tint("volt", "tint"),
            "--nav-item-background-selected": tint("volt", "tint"),
        }),
        ("Markup", {
            "--heading-formatting": c["dim"],
            **{f"--h{level}-color": c["volt"] for level in range(1, 7)},
            # The markup table's amber and jade are markdown *tokens* in an
            # editor. As prose weights they flood the page, and inside a
            # highlight they fall to 3.76:1 and 3.98:1 on light. Emphasised
            # text takes `bright` from the typography table instead.
            "--bold-color": c["bright"],
            "--italic-color": c["text"],
            "--list-marker-color": c["ember"],
            "--blockquote-border-color": c["subtle"],
            "--tag-color": c["arc"],
            "--tag-color-hover": c["volt"],
            "--tag-background": tint("volt", "faint"),
            "--tag-background-hover": tint("volt", "wash"),
            "--link-color": c["blue"],
            "--link-color-hover": c["blue"],
            "--link-external-color": c["cyan"],
            "--link-external-color-hover": c["cyan"],
            "--link-unresolved-color": c["subtle"],
            "--link-unresolved-opacity": "1",
            "--link-unresolved-decoration-color": c["ember"],
        }),
        ("Code", {f"--code-{key}": c[name] for key, name in CODE.items()}),
        ("Callouts", {
            # Everything else resolves through the named colours already.
            "--callout-warning": c["amber"],
            "--callout-question": c["bronze"],
            "--callout-quote": c["subtle"],
        }),
        ("Graph", {
            "--graph-text": c["text"],
            "--graph-line": c["overlay"],
            "--graph-node": c["soft"],
            "--graph-node-unresolved": c["dim"],
            "--graph-node-focused": c["volt"],
            "--graph-node-tag": c["arc"],
            "--graph-node-attachment": c["blue"],
        }),
    ]


def css(palette):
    lines = [f"/* {palette['name']} for Obsidian.",
             "   Generated from palette.json; edit that, not this. */"]
    for flavour in ("dark", "light"):
        lines += ["", f"/* {palette['flavours'][flavour]['name']} */",
                  f".theme-{flavour} {{"]
        for index, (title, group) in enumerate(variables(palette, flavour)):
            lines += ([""] if index else []) + [f"  /* {title} */"]
            lines += [f"  {key}: {value};" for key, value in group.items()]
        lines.append("}")
    return "\n".join(lines) + "\n\n" + RULES


def generate(palette):
    return {
        THEME: css(palette),
        MANIFEST: json.dumps({
            "name": palette["name"],
            "version": VERSION,
            "minAppVersion": MIN_APP_VERSION,
            "author": palette["author"],
        }, indent=2) + "\n",
    }


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"obsidian/{name}")
