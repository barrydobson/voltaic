#!/usr/bin/env python3
"""Generate the Neovim colour schemes from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent

# Terminal slot order is fixed by the spec, not by the palette.
SLOTS = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
         "bright_black", "bright_red", "bright_green", "bright_yellow",
         "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]


def groups(palette, flavour):
    """Highlight group -> nvim_set_hl spec. Groups Neovim already links sensibly
    (most `@` captures, `@lsp.type.*`, plugin groups) are left to their defaults."""
    c = {k: v["hex"] for k, v in palette["flavours"][flavour]["colours"].items()}
    a = palette["alpha"]

    def over(name, step):
        """Neovim takes no alpha, so tints are flattened onto the editor canvas."""
        return core.composite(c[name], a[step], c["deep"])

    # Same reasoning as the Zed port: the light ramp is compressed at the top, so
    # step to `overlay` rather than tinting with it.
    active_line = over("overlay", "veil") if flavour == "dark" else c["overlay"]
    fg = lambda name, **attrs: {"fg": c[name], **attrs}
    undercurl = lambda name: {"sp": c[name], "undercurl": True}

    return {
        # Editor
        "Normal": {"fg": c["text"], "bg": c["deep"]},
        "NormalNC": {"link": "Normal"},
        "NormalFloat": {"fg": c["text"], "bg": c["surface"]},
        "FloatBorder": {"fg": c["overlay"], "bg": c["surface"]},
        "FloatTitle": {"fg": c["arc"], "bg": c["surface"], "bold": True},
        "Cursor": {"fg": c["deep"], "bg": c["volt"]},
        "lCursor": {"link": "Cursor"},
        "CursorIM": {"link": "Cursor"},
        "TermCursor": {"link": "Cursor"},
        "CursorLine": {"bg": active_line},
        "CursorColumn": {"bg": active_line},
        "ColorColumn": {"bg": c["surface"]},
        "LineNr": fg("dim"),
        "CursorLineNr": fg("volt", bold=True),
        "SignColumn": {},
        "FoldColumn": fg("dim"),
        "Folded": {"fg": c["soft"], "bg": c["surface"]},
        "NonText": fg("muted"),
        "EndOfBuffer": fg("muted"),
        "Whitespace": fg("muted"),
        "SpecialKey": fg("subtle"),
        "Conceal": fg("subtle"),
        "Directory": fg("blue"),
        "Title": fg("bright", bold=True),
        "WinSeparator": fg("overlay"),
        "VertSplit": {"link": "WinSeparator"},
        "StatusLine": {"fg": c["text"], "bg": c["surface"]},
        "StatusLineNC": {"fg": c["subtle"], "bg": c["base"]},
        "TabLine": {"fg": c["subtle"], "bg": c["base"]},
        "TabLineFill": {"bg": c["base"]},
        "TabLineSel": {"fg": c["bright"], "bg": c["deep"], "bold": True},
        "WinBar": fg("soft", bold=True),
        "WinBarNC": fg("subtle"),
        "Visual": {"bg": over("volt", "tint")},
        "VisualNOS": {"link": "Visual"},
        "Search": {"fg": c["text"], "bg": over("volt", "tint")},
        "IncSearch": {"fg": c["deep"], "bg": c["volt"]},
        "CurSearch": {"link": "IncSearch"},
        "Substitute": {"fg": c["text"], "bg": over("ember", "tint")},
        "MatchParen": {"bg": c["overlay"], "bold": True},
        "QuickFixLine": {"bg": active_line, "bold": True},
        "Pmenu": {"fg": c["text"], "bg": c["surface"]},
        "PmenuSel": {"fg": c["bright"], "bg": c["overlay"]},
        "PmenuMatch": fg("arc", bold=True),
        "PmenuMatchSel": fg("arc", bold=True),
        "PmenuKind": fg("blue"),
        "PmenuExtra": fg("subtle"),
        "PmenuSbar": {"bg": c["surface"]},
        "PmenuThumb": {"bg": c["muted"]},
        "ModeMsg": fg("bright", bold=True),
        "MoreMsg": fg("blue"),
        "Question": fg("blue"),
        "OkMsg": fg("jade"),
        "WarningMsg": fg("amber"),
        "ErrorMsg": fg("ember"),
        "SpellBad": undercurl("ember"),
        "SpellCap": undercurl("amber"),
        "SpellLocal": undercurl("blue"),
        "SpellRare": undercurl("violet"),

        # Diff and version control
        "Added": fg("jade"),
        "Changed": fg("amber"),
        "Removed": fg("ember"),
        "DiffAdd": {"bg": over("jade", "tint")},
        "DiffChange": {"bg": over("amber", "faint")},
        "DiffText": {"bg": over("amber", "tint")},
        "DiffDelete": {"bg": over("ember", "tint")},

        # Syntax. Neovim links the other legacy groups to these.
        "Comment": fg("subtle"),
        "Constant": fg("amber"),
        "String": fg("jade"),
        "Character": fg("jade"),
        "Number": fg("ember"),
        "Boolean": fg("ember"),
        "Identifier": fg("text"),
        "Function": fg("blue"),
        "Statement": fg("volt"),
        "Operator": fg("ice"),
        "PreProc": fg("violet"),
        "Include": fg("volt"),
        "Type": fg("cyan"),
        "StorageClass": fg("volt"),
        "Structure": fg("volt"),
        "Special": fg("ember"),
        "Tag": fg("ember"),
        "Delimiter": fg("subtle"),
        "Underlined": {"underline": True},
        "Todo": {"fg": c["deep"], "bg": c["amber"], "bold": True},
        "Error": fg("ember"),

        # Tree-sitter, where Neovim's default link misses the style guide.
        "@variable": fg("text"),
        "@variable.member": fg("bronze"),
        "@property": fg("blue"),
        "@module": fg("jade"),
        "@constant.builtin": {"link": "Constant"},
        "@string.regexp": fg("amber"),
        "@string.special.url": fg("blue", underline=True),
        "@type.builtin": {"link": "Type"},
        "@constructor": fg("cyan"),
        "@function.builtin": {"link": "Function"},
        "@attribute": fg("amber"),
        "@keyword.directive": {"link": "PreProc"},
        "@punctuation.bracket": fg("soft"),
        "@tag.attribute": fg("amber"),
        "@tag.delimiter": fg("subtle"),
        "@markup": fg("text"),
        "@markup.heading": fg("volt", bold=True),
        "@markup.italic": fg("jade", italic=True),
        "@markup.strong": fg("amber", bold=True),
        "@markup.raw": fg("amber"),
        "@markup.link": fg("blue"),
        "@markup.link.url": fg("cyan", underline=True),
        "@markup.list": fg("ember"),
        "@markup.quote": fg("subtle"),

        # Diagnostics and LSP
        "DiagnosticError": fg("ember"),
        "DiagnosticWarn": fg("amber"),
        "DiagnosticInfo": fg("blue"),
        "DiagnosticHint": fg("soft"),
        "DiagnosticOk": fg("jade"),
        "DiagnosticUnderlineError": undercurl("ember"),
        "DiagnosticUnderlineWarn": undercurl("amber"),
        "DiagnosticUnderlineInfo": undercurl("blue"),
        "DiagnosticUnderlineHint": undercurl("soft"),
        "DiagnosticUnderlineOk": undercurl("jade"),
        "DiagnosticDeprecated": {"sp": c["subtle"], "strikethrough": True},
        "LspReferenceText": {"bg": over("volt", "tint")},
        "LspReferenceRead": {"bg": over("volt", "tint")},
        "LspReferenceWrite": {"bg": over("volt", "veil")},
        "LspInlayHint": fg("subtle"),
        "LspCodeLens": fg("subtle"),
    }


def lua(value):
    return "true" if value is True else f'"{value}"'


def scheme(palette, flavour):
    data = palette["flavours"][flavour]
    colours = data["colours"]
    lines = [
        f"-- {data['name']} for Neovim. Generated from palette.json, do not edit.",
        "",
        # 'background' goes first: setting it once colors_name exists reloads the scheme.
        f'vim.o.background = "{data["appearance"]}"',
        'vim.cmd.highlight("clear")',
        f'vim.g.colors_name = "voltaic-{flavour}"',
        "",
        "local hl = vim.api.nvim_set_hl",
    ]
    for name, spec in groups(palette, flavour).items():
        body = ", ".join(f"{k} = {lua(v)}" for k, v in spec.items())
        lines.append(f'hl(0, "{name}", {{ {body} }})' if body else f'hl(0, "{name}", {{}})')
    lines.append("")
    lines += [f'vim.g.terminal_color_{i} = "{colours[data["ansi"][slot]]["hex"]}"'
              for i, slot in enumerate(SLOTS)]
    return "\n".join(lines) + "\n"


def generate(palette):
    return {f"colors/voltaic-{f}.lua": scheme(palette, f) for f in palette["flavours"]}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).parent.mkdir(exist_ok=True)
        (HERE / name).write_text(content)
        print(f"nvim/{name}")
