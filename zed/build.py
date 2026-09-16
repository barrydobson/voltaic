#!/usr/bin/env python3
"""Generate the Zed theme from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent
OUTPUT = "voltaic.json"

# Indent-guide colouring. Zed cycles these, so they want to be walkable around the
# wheel rather than ordered by importance.
RAINBOW = ["ember", "amber", "volt", "jade", "teal", "blue", "violet"]

ITALIC = {"comment", "comment.doc", "comment.documentation", "predoc", "attribute",
          "boolean", "variable.special", "variable.builtin", "predictive"}
BOLD = {"string.escape", "title", "emphasis.strong"}

# Syntax captures grouped by the style guide's colour for that job.
SYNTAX = {
    "volt": ["keyword", "keyword.conditional", "keyword.conditional.ternary",
             "keyword.coroutine", "keyword.debug", "keyword.directive",
             "keyword.directive.define", "keyword.exception", "keyword.export",
             "keyword.function", "keyword.import", "keyword.modifier",
             "keyword.operator", "keyword.repeat", "keyword.return", "keyword.type",
             "title"],
    "jade": ["string", "string.doc", "string.documentation", "namespace", "module",
             "emphasis", "character", "diff.plus"],
    "ember": ["number", "number.float", "float", "boolean", "tag", "tag.delimiter",
              "tag.doctype", "string.escape", "punctuation.special",
              "punctuation.special.symbol", "punctuation.list_marker",
              "variable.special", "variable.builtin", "character.special",
              "diff.minus", "comment.error"],
    "amber": ["constant", "constant.builtin", "constant.macro", "attribute",
              "tag.attribute", "label", "string.regex", "string.regexp",
              "string.special", "string.special.symbol", "string.special.path",
              "string.special.url", "variant", "text.literal", "emphasis.strong",
              "comment.warn", "comment.warning"],
    "blue": ["function", "function.builtin", "function.call", "function.method",
             "function.method.call", "function.decorator", "function.macro",
             "link_text", "comment.todo", "comment.note", "comment.info"],
    "cyan": ["type", "type.builtin", "type.definition", "type.class.definition",
             "type.interface", "type.super", "constructor", "enum", "link_uri"],
    "ice": ["operator", "selector.pseudo"],
    "bronze": ["property", "field", "variable.member"],
    "violet": ["preproc", "concept"],
    "text": ["variable", "embedded", "primary", "text", "symbol", "parameter",
             "variable.parameter", "parent"],
    "soft": ["punctuation.bracket", "hint", "comment.hint"],
    "subtle": ["comment", "comment.doc", "comment.documentation", "predoc",
               "punctuation", "punctuation.delimiter", "predictive", "unreachable"],
}


def style(palette, flavour):
    c = {k: v["hex"] for k, v in palette["flavours"][flavour]["colours"].items()}
    a = palette["alpha"]
    dark = flavour == "dark"

    def over(name, step, base="base"):
        """Composited, for anything that has to read as a solid fill."""
        return core.composite(c[name], a[step], c[base])

    def tint(name, step):
        """Translucent, for anything Zed layers over changing content."""
        return core.rgba(c[name], a[step])

    # The light ramp is compressed at the top, so tinting the active line with
    # `overlay` would not show. Step the background tone instead.
    active_line = tint("overlay", "veil") if dark else c["base"]

    s = {
        "background.appearance": "opaque",
        "accents": [c[n] for n in RAINBOW],

        "border": c["overlay"],
        "border.variant": c["overlay"],
        "border.focused": c["volt"],
        "border.selected": c["volt"],
        "border.transparent": "#00000000",
        "border.disabled": c["overlay"],

        "elevated_surface.background": c["surface"],
        "surface.background": c["base"],
        "background": c["base"],
        "element.background": c["surface"],
        "element.hover": c["surface"],
        "element.active": c["overlay"],
        "element.selected": c["overlay"],
        "element.disabled": c["surface"],
        "drop_target.background": tint("volt", "tint"),
        "ghost_element.background": "#00000000",
        "ghost_element.hover": c["surface"],
        "ghost_element.active": c["overlay"],
        "ghost_element.selected": c["overlay"],
        "ghost_element.disabled": "#00000000",

        "text": c["text"],
        "text.muted": c["soft"],
        "text.placeholder": c["dim"],
        "text.disabled": c["dim"],
        "text.accent": c["arc"],
        "icon": c["arc"],
        "icon.muted": c["subtle"],
        "icon.disabled": c["muted"],
        "icon.placeholder": c["subtle"],
        "icon.accent": c["volt"],

        "status_bar.background": c["base"],
        "title_bar.background": c["base"],
        "title_bar.inactive_background": c["base"],
        "toolbar.background": c["deep"],
        "tab_bar.background": c["base"],
        "tab.inactive_background": c["base"],
        "tab.active_background": c["surface"],
        "search.match_background": tint("volt", "tint"),
        "search.active_match_background": tint("volt", "veil"),

        "panel.background": c["base"],
        "panel.overlay_background": c["surface"],
        "panel.focused_border": c["volt"],
        "panel.indent_guide": c["overlay"],
        "panel.indent_guide_active": c["muted"],
        "panel.indent_guide_hover": c["muted"],
        "pane.focused_border": c["volt"],
        "pane_group.border": c["overlay"],

        "scrollbar.thumb.background": tint("volt", "faint"),
        "scrollbar.thumb.hover_background": tint("volt", "wash"),
        "scrollbar.thumb.active_background": tint("volt", "tint"),
        "scrollbar.thumb.border": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.track.border": c["overlay"],
        "minimap.thumb.background": tint("volt", "faint"),
        "minimap.thumb.hover_background": tint("volt", "wash"),
        "minimap.thumb.active_background": tint("volt", "tint"),
        "minimap.thumb.border": "#00000000",

        "editor.foreground": c["text"],
        "editor.background": c["deep"],
        "editor.gutter.background": c["deep"],
        "editor.subheader.background": c["surface"],
        "editor.active_line.background": active_line,
        "editor.highlighted_line.background": active_line,
        "editor.debugger_active_line.background": tint("amber", "tint"),
        "editor.line_number": c["dim"],
        "editor.active_line_number": c["volt"],
        "editor.invisible": c["overlay"],
        "editor.wrap_guide": c["overlay"],
        "editor.active_wrap_guide": c["muted"],
        "editor.indent_guide": c["overlay"],
        "editor.indent_guide_active": c["muted"],
        "editor.document_highlight.read_background": tint("volt", "tint"),
        "editor.document_highlight.write_background": tint("volt", "veil"),
        "editor.document_highlight.bracket_background": tint("volt", "wash"),

        "terminal.background": c["base"],
        "terminal.ansi.background": c["base"],
        "terminal.foreground": c["text"],
        "terminal.bright_foreground": c["bright"],
        "terminal.dim_foreground": c["soft"],

        "link_text.hover": c["arc"],
        "debugger.accent": c["ember"],
    }

    for slot, name in palette["flavours"][flavour]["ansi"].items():
        s[f"terminal.ansi.{slot}"] = c[name]
    # Zed's dim row is a third tier below normal; the palette has no dim accents,
    # so reuse the normals and let the two greys carry the distinction.
    for slot in ("red", "green", "yellow", "blue", "magenta", "cyan"):
        s[f"terminal.ansi.dim_{slot}"] = c[palette["flavours"][flavour]["ansi"][slot]]
    s["terminal.ansi.dim_black"] = c["dim"]
    s["terminal.ansi.dim_white"] = c["soft"]

    status = {
        "error": "ember", "warning": "amber", "info": "blue", "hint": "soft",
        "success": "jade", "conflict": "violet", "created": "jade",
        "modified": "amber", "renamed": "amber", "deleted": "ember",
        "ignored": "subtle", "hidden": "subtle", "predictive": "subtle",
        "unreachable": "subtle",
    }
    for key, name in status.items():
        s[key] = c[name]
        s[f"{key}.border"] = c[name]
        # Quiet roles get a flat surface; states that need to read as a state get
        # a tint of themselves.
        s[f"{key}.background"] = (c["surface"] if name == "subtle" or key == "hint"
                                  else tint(name, "wash"))

    s.update({
        "version_control.added": c["jade"],
        "version_control.deleted": c["ember"],
        "version_control.modified": c["amber"],
        "version_control.renamed": c["amber"],
        "version_control.conflict": c["violet"],
        "version_control.ignored": c["subtle"],
        "version_control.conflict_marker.ours": tint("jade", "tint"),
        "version_control.conflict_marker.theirs": tint("blue", "tint"),
    })

    modes = {"normal": "volt", "helix_normal": "volt", "insert": "jade",
             "visual": "violet", "helix_select": "violet", "visual_line": "violet",
             "visual_block": "violet", "replace": "ember"}
    s["vim.mode.text"] = c["deep"]
    for mode, name in modes.items():
        s[f"vim.{mode}.background"] = c[name]
        s[f"vim.{mode}.foreground"] = c["deep"]

    s["players"] = [{"cursor": c["volt"], "background": c["volt"],
                     "selection": tint("volt", "tint")}]

    syntax = {}
    for name, captures in SYNTAX.items():
        for capture in captures:
            entry = {"color": c[name]}
            if capture in ITALIC:
                entry["font_style"] = "italic"
            if capture in BOLD:
                entry["font_weight"] = 700
            syntax[capture] = entry
    s["syntax"] = dict(sorted(syntax.items()))
    return s


def generate(palette):
    return {OUTPUT: json.dumps({
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": palette["name"],
        "author": palette["author"],
        "themes": [
            {"name": palette["flavours"][f]["name"],
             "appearance": palette["flavours"][f]["appearance"],
             "style": style(palette, f)}
            for f in ("dark", "light")
        ],
    }, indent=2) + "\n"}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"zed/{name}")
