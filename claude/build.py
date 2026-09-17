#!/usr/bin/env python3
"""Generate the Claude Code themes from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent

# Every override is one palette colour, or a (colour, alpha step) pair that gets
# composited over `base`. Claude Code paints into a terminal cell, so a
# translucent value has nothing underneath it to blend with.
KEYS = {
    "autoAccept": "volt",
    "bashBorder": "volt",
    "claude": "volt",
    "claudeShimmer": "arc",
    "claudeBlue_FOR_SYSTEM_SPINNER": "volt",
    "claudeBlueShimmer_FOR_SYSTEM_SPINNER": "arc",
    "permission": "volt",
    "permissionShimmer": "arc",
    "planMode": "jade",
    "ide": "arc",
    "promptBorder": "subtle",
    "promptBorderShimmer": "soft",
    "text": "text",
    "inverseText": "deep",
    "inactive": "subtle",
    "inactiveShimmer": "soft",
    "subtle": "dim",
    "suggestion": "volt",
    "remember": "volt",
    "background": "volt",
    "success": "jade",
    "error": "ember",
    "warning": "amber",
    "merged": "jade",
    "warningShimmer": "gold",
    "diffAdded": ("jade", "tint"),
    "diffRemoved": ("ember", "tint"),
    "diffAddedDimmed": ("jade", "wash"),
    "diffRemovedDimmed": ("ember", "wash"),
    "diffAddedWord": "jade",
    "diffRemovedWord": "ember",
    "professionalBlue": "arc",
    "chromeYellow": "volt",
    "clawd_body": "volt",
    "clawd_background": "deep",
    "userMessageBackground": "surface",
    "userMessageBackgroundHover": "overlay",
    "messageActionsBackground": "surface",
    "selectionBg": ("volt", "tint"),
    "bashMessageBackgroundColor": "surface",
    "memoryBackgroundColor": "surface",
    "rate_limit_fill": "volt",
    "rate_limit_empty": "overlay",
    "fastMode": "volt",
    "fastModeShimmer": "arc",
    "briefLabelYou": "soft",
    "briefLabelClaude": "volt",
}


def theme(palette, flavour):
    data = palette["flavours"][flavour]
    c = {k: v["hex"] for k, v in data["colours"].items()}
    a = palette["alpha"]
    return json.dumps({
        "name": f"voltaic-{flavour}",
        "base": data["appearance"],
        "overrides": {
            key: c[spec] if isinstance(spec, str)
            else core.composite(c[spec[0]], a[spec[1]], c["base"])
            for key, spec in KEYS.items()
        },
    }, indent=2) + "\n"


def generate(palette):
    return {f"voltaic-{f}.json": theme(palette, f) for f in palette["flavours"]}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"claude/{name}")
