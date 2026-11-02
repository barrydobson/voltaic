#!/usr/bin/env python3
"""Generate the Codex CLI .tmTheme files from palette.json."""
import importlib.util, json, pathlib, plistlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))
import build as core

# Reuse the VS Code token rules so code reads the same in both. Loaded by path
# because every port's module is called build.
_spec = importlib.util.spec_from_file_location("vscode_build", ROOT / "vscode" / "build.py")
vscode = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vscode)


def theme(palette, flavour):
    data = palette["flavours"][flavour]
    c = {k: v["hex"] for k, v in data["colours"].items()}
    # Codex drops alpha from diff backgrounds, so flatten onto the terminal canvas.
    line = lambda name: core.composite(c[name], palette["alpha"]["wash"], c["deep"])
    rules = [{"settings": {"foreground": c["text"], "background": c["deep"],
                           "caret": c["volt"], "selection": core.composite(
                               c["volt"], palette["alpha"]["tint"], c["deep"])}}]
    for name, colour, font, scopes in vscode.SYNTAX:
        settings = {"foreground": c[colour]}
        if font:
            settings["fontStyle"] = font
        rules.append({"name": name, "scope": ", ".join(scopes), "settings": settings})
    rules += [
        # Later rules add to earlier matches, so these keep the jade/ember text.
        {"name": "Diff added line", "scope": "markup.inserted, diff.inserted",
         "settings": {"background": line("jade")}},
        {"name": "Diff removed line", "scope": "markup.deleted, diff.deleted",
         "settings": {"background": line("ember")}},
        {"name": "Codex accent", "scope": "codex.accent",
         "settings": {"foreground": c["volt"]}},
    ]
    plist = {"name": data["name"], "author": palette["author"],
             "semanticClass": f"theme.{data['appearance']}.voltaic", "settings": rules}
    return plistlib.dumps(plist).decode()


def generate(palette):
    return {f"voltaic-{f}.tmTheme": theme(palette, f) for f in palette["flavours"]}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"codex/{name}")
