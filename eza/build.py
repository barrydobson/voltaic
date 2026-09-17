#!/usr/bin/env python3
"""Generate the eza themes from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HERE = pathlib.Path(__file__).parent

# Every value is a palette colour name. Nested dicts become nested YAML blocks.
THEME = {
    "filekinds": {
        "normal": "text",
        "directory": "blue",
        "symlink": "teal",
        "pipe": "subtle",
        "block_device": "flare",
        "char_device": "flare",
        "socket": "dim",
        "special": "violet",
        "executable": "volt",
        "mount_point": "sky",
    },
    # Read carries the ownership tier by weight, write warns, execute matches the
    # executable file kind.
    "perms": {
        "user_read": "bright",
        "user_write": "amber",
        "user_execute_file": "volt",
        "user_execute_other": "volt",
        "group_read": "text",
        "group_write": "amber",
        "group_execute": "volt",
        "other_read": "soft",
        "other_write": "amber",
        "other_execute": "volt",
        "special_user_file": "violet",
        "special_other": "dim",
        "attribute": "soft",
    },
    "size": {
        "major": "text",
        "minor": "soft",
        "number_byte": "soft",
        "number_kilo": "text",
        "number_mega": "blue",
        "number_giga": "amber",
        "number_huge": "ember",
        "unit_byte": "soft",
        "unit_kilo": "text",
        "unit_mega": "blue",
        "unit_giga": "amber",
        "unit_huge": "ember",
    },
    "users": {
        "user_you": "bright",
        "user_root": "ember",
        "user_other": "soft",
        "group_yours": "text",
        "group_other": "soft",
        "group_root": "ember",
    },
    "links": {
        "normal": "teal",
        "multi_link_file": "sky",
    },
    "git": {
        "new": "jade",
        "modified": "amber",
        "deleted": "ember",
        "renamed": "amber",
        "typechange": "cyan",
        "ignored": "subtle",
        "conflicted": "violet",
    },
    "git_repo": {
        "branch_main": "text",
        "branch_other": "violet",
        "git_clean": "jade",
        "git_dirty": "amber",
    },
    # eza nests the SELinux fields under `selinux`; a flat block is silently
    # dropped, because serde leaves the unset fields at their defaults.
    "security_context": {
        "none": "subtle",
        "selinux": {
            "colon": "subtle",
            "user": "text",
            "role": "violet",
            "typ": "dim",
            "range": "violet",
        },
    },
    # These override the filename colour, so they avoid the file-kind colours that
    # would make an ordinary file read as a directory, a symlink or an executable.
    "file_type": {
        "image": "amber",
        "video": "ember",
        "music": "jade",
        "lossless": "teal",
        "crypto": "bronze",
        "document": "text",
        "compressed": "lilac",
        "temp": "subtle",
        "compiled": "flare",
        "build": "soft",
        "source": "cyan",
    },
    "punctuation": "subtle",
    "date": "soft",
    "inode": "soft",
    "blocks": "soft",
    "header": "bright",
    "octal": "soft",
    "flags": "violet",
    "symlink_path": "teal",
    "control_char": "amber",
    "broken_symlink": "ember",
    "broken_path_overlay": "dim",
}


def render(node, colours, indent=0):
    lines, after_block = [], False
    for key, value in node.items():
        pad = "  " * indent
        nested = isinstance(value, dict)
        if indent == 0 and lines and (nested or after_block):
            lines.append("")
        if nested:
            lines.append(f"{pad}{key}:")
            lines += render(value, colours, indent + 1)
        else:
            lines.append(f'{pad}{key}: {{foreground: "{colours[value]}"}}')
        after_block = nested
    return lines


def theme(palette, flavour):
    data = palette["flavours"][flavour]
    colours = {k: v["hex"] for k, v in data["colours"].items()}
    head = [f"# {data['name']} for eza. Generated from palette.json, do not edit.",
            "colourful: true", ""]
    return "\n".join(head + render(THEME, colours)) + "\n"


def generate(palette):
    return {f"voltaic-{f}.yml": theme(palette, f) for f in palette["flavours"]}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"eza/{name}")
