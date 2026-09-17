#!/usr/bin/env python3
"""Generate the k9s skins from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HERE = pathlib.Path(__file__).parent


def skin(palette, flavour):
    data = palette["flavours"][flavour]
    c = {k: f"'{v['hex']}'" for k, v in data["colours"].items()}
    return f"""\
# {data['name']}. Generated from palette.json, do not edit.
k9s:
  body:
    fgColor: {c['text']}
    bgColor: {c['base']}
    logoColor: {c['volt']}
    logoColorMsg: {c['text']}
    logoColorInfo: {c['blue']}
    logoColorWarn: {c['amber']}
    logoColorError: {c['ember']}
  prompt:
    fgColor: {c['text']}
    bgColor: {c['surface']}
    suggestColor: {c['subtle']}
    border:
      command: {c['volt']}
      default: {c['teal']}
  help:
    fgColor: {c['text']}
    bgColor: {c['base']}
    sectionColor: {c['volt']}
    keyColor: {c['blue']}
    numKeyColor: {c['amber']}
  info:
    fgColor: {c['soft']}
    sectionColor: {c['text']}
    cpuColor: {c['blue']}
    memColor: {c['teal']}
    k9sRevColor: {c['subtle']}
  frame:
    title:
      fgColor: {c['arc']}
      bgColor: {c['base']}
      highlightColor: {c['volt']}
      counterColor: {c['blue']}
      filterColor: {c['teal']}
    border:
      fgColor: {c['overlay']}
      focusColor: {c['volt']}
    menu:
      fgColor: {c['text']}
      keyColor: {c['blue']}
      numKeyColor: {c['amber']}
    crumbs:
      fgColor: {c['deep']}
      bgColor: {c['soft']}
      activeColor: {c['volt']}
    status:
      newColor: {c['blue']}
      modifyColor: {c['amber']}
      addColor: {c['jade']}
      pendingColor: {c['amber']}
      errorColor: {c['ember']}
      highlightColor: {c['arc']}
      killColor: {c['ember']}
      completedColor: {c['subtle']}
  views:
    table:
      fgColor: {c['text']}
      bgColor: {c['base']}
      cursorFgColor: {c['deep']}
      cursorBgColor: {c['volt']}
      markColor: {c['amber']}
      header:
        fgColor: {c['soft']}
        bgColor: {c['base']}
        sorterColor: {c['volt']}
        selectedSortColumnColor: {c['arc']}
    xray:
      fgColor: {c['overlay']}
      bgColor: {c['base']}
      cursorColor: {c['text']}
      cursorTextColor: {c['deep']}
      graphicColor: {c['muted']}
    charts:
      bgColor: {c['base']}
      chartBgColor: {c['base']}
      dialBgColor: {c['base']}
      focusFgColor: {c['deep']}
      focusBgColor: {c['volt']}
      defaultDialColors:
        - {c['jade']}
        - {c['ember']}
      defaultChartColors:
        - {c['jade']}
        - {c['ember']}
      # Exactly two entries. k9s reverse-looks-up these by tcell colour name to
      # build the pulse legend, falls back to a safe default under three, and a
      # hex matches no name, so a third entry empties the lookup and panics.
      resourceColors:
        cpu:
          - {c['blue']}
          - {c['amber']}
        mem:
          - {c['teal']}
          - {c['amber']}
    yaml:
      keyColor: {c['blue']}
      valueColor: {c['text']}
      colonColor: {c['subtle']}
    picker:
      mainColor: {c['text']}
      focusColor: {c['volt']}
      shortcutColor: {c['blue']}
    logs:
      fgColor: {c['text']}
      bgColor: {c['deep']}
      indicator:
        fgColor: {c['soft']}
        bgColor: {c['surface']}
        toggleOnColor: {c['jade']}
        toggleOffColor: {c['subtle']}
  dialog:
    fgColor: {c['text']}
    bgColor: {c['surface']}
    buttonFgColor: {c['text']}
    buttonBgColor: {c['overlay']}
    buttonFocusFgColor: {c['deep']}
    buttonFocusBgColor: {c['volt']}
    labelFgColor: {c['arc']}
    fieldFgColor: {c['text']}
"""


def generate(palette):
    return {f"voltaic-{f}.yaml": skin(palette, f) for f in palette["flavours"]}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"k9s/{name}")
