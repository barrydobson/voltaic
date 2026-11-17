#!/usr/bin/env python3
"""Generate the Orca theme plugin from palette.json."""
import importlib.util, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))
import build as core
import check

# Reuse the VS Code token rules so code reads the same in both. Loaded by path
# because every port's module is called build.
_spec = importlib.util.spec_from_file_location("vscode_build", ROOT / "vscode" / "build.py")
vscode = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vscode)

# xterm.js names for the sixteen slots, in palette `ansi` key order.
SLOTS = {"black": "black", "red": "red", "green": "green", "yellow": "yellow",
         "blue": "blue", "magenta": "magenta", "cyan": "cyan", "white": "white",
         "bright_black": "brightBlack", "bright_red": "brightRed",
         "bright_green": "brightGreen", "bright_yellow": "brightYellow",
         "bright_blue": "brightBlue", "bright_magenta": "brightMagenta",
         "bright_cyan": "brightCyan", "bright_white": "brightWhite"}


def tokens(palette, flavour):
    c = {k: v["hex"] for k, v in palette["flavours"][flavour]["colours"].items()}
    a = palette["alpha"]
    return {
        "--background": c["base"],
        "--editor-surface": c["deep"],
        "--foreground": c["text"],
        "--card": c["surface"],
        "--card-foreground": c["text"],
        "--popover": c["surface"],
        "--popover-foreground": c["text"],
        "--primary": c["volt"],
        "--primary-foreground": c["deep"],
        "--secondary": c["overlay"],
        "--secondary-foreground": c["text"],
        "--muted": c["overlay"],
        "--muted-foreground": c["soft"],
        "--accent": c["overlay"],
        "--accent-foreground": c["text"],
        "--border": c["overlay"],
        "--input": c["muted"],
        "--ring": c["volt"],
        **{f"--chart-{i}": c[n] for i, n in enumerate(
            ["blue", "teal", "bronze", "ice", "lilac"], 1)},
        "--sidebar": c["surface"],
        "--sidebar-foreground": c["text"],
        "--sidebar-accent": c["overlay"],
        "--sidebar-accent-foreground": c["text"],
        "--sidebar-border": c["overlay"],
        "--worktree-sidebar": c["surface"],
        "--worktree-sidebar-active": core.rgba(c["volt"], a["tint"]),
        "--worktree-sidebar-active-border": c["volt"],
        "--tab-bar": c["base"],
        "--tab-active": c["deep"],
        "--tab-active-foreground": c["bright"],
        "--tab-active-indicator": c["volt"],
        "--tab-inactive": c["base"],
        "--tab-inactive-foreground": c["soft"],
        "--split-divider": c["overlay"],
        "--split-divider-hover": c["volt"],
        "--chat-inline-code-foreground": c["amber"],
        "--text-link": c["blue"],
        "--editor-selection": core.rgba(c["volt"], a["tint"]),
        "--diff-added": c["jade"],
        "--diff-removed": c["ember"],
        "--git-decoration-added": c["jade"],
        "--git-decoration-modified": c["amber"],
        "--git-decoration-deleted": c["ember"],
        "--git-decoration-renamed": c["amber"],
        "--git-decoration-untracked": c["jade"],
        "--git-decoration-copied": c["jade"],
        "--git-decoration-ignored": c["subtle"],
    }


def token_colours(palette, flavour):
    c = {k: v["hex"] for k, v in palette["flavours"][flavour]["colours"].items()}
    rules = []
    for name, colour, font, scopes in vscode.SYNTAX:
        # Orca ignores descendant selectors, so drop them rather than ship dead rules.
        scopes = [s for s in scopes if " " not in s]
        if not scopes:
            continue
        settings = {"foreground": c[colour]}
        if font:
            settings["fontStyle"] = font
        rules.append({"name": name, "scope": scopes, "settings": settings})
    return rules


def app_theme(palette, flavour):
    t = tokens(palette, flavour)
    rules = token_colours(palette, flavour)
    # Orca silently drops pairs under these floors, so fail the build instead.
    pairs = [("--foreground", "--background", 4.5), ("--card-foreground", "--card", 4.5),
             ("--primary-foreground", "--primary", 4.5), ("--muted-foreground", "--muted", 4.5),
             ("--accent-foreground", "--accent", 4.5), ("--text-link", "--editor-surface", 4.5),
             ("--tab-inactive-foreground", "--tab-inactive", 4.5)]
    pairs += [(k, "--sidebar", 3.0) for k in t if k.startswith("--git-decoration-")]
    for fg, bg, floor in pairs:
        ratio = check.contrast(t[fg], t[bg])
        assert ratio >= floor, f"orca/{flavour}: {fg} on {bg} is {ratio:.2f}:1"
    for rule in rules:
        ratio = check.contrast(rule["settings"]["foreground"], t["--editor-surface"])
        assert ratio >= 3.0, f"orca/{flavour}: {rule['name']} is {ratio:.2f}:1"
    theme = {"schemaVersion": 1, "base": palette["flavours"][flavour]["appearance"],
             "tokens": t, "tokenColors": rules}
    return json.dumps(theme, indent=2) + "\n"


def terminal_theme(palette, flavour):
    data = palette["flavours"][flavour]
    c = {k: v["hex"] for k, v in data["colours"].items()}
    terminal = {"background": c["deep"], "foreground": c["text"],
                "cursor": c["volt"], "cursorAccent": c["deep"],
                "selectionBackground": c["volt"], "selectionForeground": c["deep"]}
    terminal |= {SLOTS[slot]: c[name] for slot, name in data["ansi"].items()}
    return json.dumps({"schemaVersion": 1, "mode": data["appearance"],
                       "terminal": terminal}, indent=2) + "\n"


def manifest(palette):
    entries = lambda folder: [
        {"id": f"voltaic-{f}", "title": palette["flavours"][f]["name"],
         "path": f"{folder}/voltaic-{f}.json"} for f in palette["flavours"]]
    return json.dumps({
        "manifestVersion": 2,
        "id": "voltaic-theme",
        "name": palette["name"],
        "version": "1.0.0",
        "execution": "data",
        "description": "Voltaic dark and light app themes, with matching code and terminal colours.",
        "license": palette["licence"],
        "repository": "https://github.com/barrydobson/voltaic/tree/main/orca",
        "engines": {"orca": ">=1.4.246"},
        "contributes": {"themes": entries("themes"), "terminalThemes": entries("terminal")},
        "capabilities": [],
    }, indent=2) + "\n"


def generate(palette):
    out = {"orca-plugin.json": manifest(palette)}
    for f in palette["flavours"]:
        out[f"themes/voltaic-{f}.json"] = app_theme(palette, f)
        out[f"terminal/voltaic-{f}.json"] = terminal_theme(palette, f)
    # Orca refuses theme files over 16 KiB.
    assert all(len(v.encode()) <= 16384 for v in out.values()), "orca: theme over 16 KiB"
    return out


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        path = HERE / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"orca/{name}")
