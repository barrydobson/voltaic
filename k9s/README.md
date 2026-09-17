# Voltaic for k9s

Both flavours, as k9s skins. Tested against k9s 0.51.0.

k9s takes no alpha, so every value here is an opaque palette colour. Nothing in
the skin needed a tint, so nothing is composited.

## Install

Copy both skins into the k9s skins directory:

```sh
OUT="${XDG_CONFIG_HOME:-$HOME/Library/Application Support}/k9s/skins"   # macOS
OUT="${XDG_CONFIG_HOME:-$HOME/.config}/k9s/skins"                       # Linux
mkdir -p "$OUT" && cp voltaic-dark.yaml voltaic-light.yaml "$OUT"
```

`k9s info` prints the directories k9s is actually using, which is the quickest
way to settle where they belong on your machine.

## Applying the theme

Set the skin by filename without the extension, in `config.yaml`:

```yaml
k9s:
  ui:
    skin: voltaic-dark
    # skin: voltaic-light
```

Per context instead, in
`<config dir>/clusters/<cluster>/<context>/config.yaml`:

```yaml
k9s:
  skin: voltaic-dark
```

k9s reloads skins while running, so editing the file is enough to see a change.

## Mapping

| Key | Job | Colour |
| --- | --- | --- |
| `body.fgColor` / `bgColor` | Application canvas | `text` on `base` |
| `body.logoColor` | Logo | `volt` |
| `body.logoColor{Msg,Info,Warn,Error}` | Logo tint per flash level | `text`, `blue`, `amber`, `ember` |
| `prompt.bgColor` | Command bar | `surface` |
| `prompt.suggestColor` | Inline completion | `subtle` |
| `prompt.border.command` / `.default` | Command bar border, filter bar border | `volt`, `teal` |
| `help.sectionColor` | Help headings | `volt` |
| `help.keyColor` / `numKeyColor` | Shortcut keys | `blue`, `amber` |
| `info.fgColor` | Cluster info labels | `soft` |
| `info.sectionColor` | Cluster info values | `text` |
| `info.cpuColor` / `memColor` | Header CPU and memory readouts | `blue`, `teal` |
| `info.k9sRevColor` | k9s version | `subtle` |
| `frame.title.fgColor` | Panel titles | `arc` |
| `frame.title.counterColor` | Item counts | `blue` |
| `frame.title.filterColor` | Active filter | `teal` |
| `frame.border.fgColor` / `focusColor` | Inactive, focused border | `overlay`, `volt` |
| `frame.crumbs.*` | Breadcrumb chips, current chip | `deep` on `soft`, `deep` on `volt` |
| `frame.status.addColor` | Added | `jade` |
| `frame.status.newColor` | New | `blue` |
| `frame.status.modifyColor` / `pendingColor` | Modified, pending | `amber` |
| `frame.status.errorColor` / `killColor` | Error, killed | `ember` |
| `frame.status.highlightColor` | Active namespace, initialised pod | `arc` |
| `frame.status.completedColor` | Completed | `subtle` |
| `views.table.cursor*` | Cursor row | `deep` on `volt` |
| `views.table.markColor` | Marked rows | `amber` |
| `views.table.header.*` | Column headers, sorter, sorted column | `soft`, `volt`, `arc` |
| `views.xray.graphicColor` | Tree connector lines | `muted` |
| `views.charts.default{Chart,Dial}Colors` | Total, faults | `jade`, `ember` |
| `views.charts.resourceColors.cpu` / `.mem` | CPU, memory sparklines | `blue`, `teal` |
| `views.yaml.*` | Keys, values, colons | `blue`, `text`, `subtle` |
| `views.logs.bgColor` | Log canvas | `deep` |
| `views.logs.indicator.toggleOn/OffColor` | Toggle states | `jade`, `subtle` |
| `dialog.bgColor` | Dialogs | `surface` |
| `dialog.buttonFocusBgColor` | Focused button | `deep` on `volt` |

Series colours follow the new [ordered series](../docs/style-guide.md#ordered-series)
rule: the chart and dial pairs mean pass and fail, so they take the status
colours, and CPU against memory is the only genuinely categorical pair in the
skin, so it takes the first two entries of the rotation.

## Deviations

- **The cursor row is a solid `volt` fill, not `overlay`.** The style guide gives
  the active row to `overlay`, but a k9s cursor is a single transient line the
  whole interface navigates by, which is the terminal-selection case: `deep` on
  `volt` at 16.7:1 in dark and 4.93:1 in light.
- **`resourceColors` pairs stop at two entries.** k9s indexes them by severity
  level, so three would map normal, warning and critical exactly. It also builds
  the pulse legend by reverse-looking-up each series colour in `tcell`'s colour
  name table, falls back to a safe default below three entries, and panics on an
  empty lookup above it. A hex matches no name, so two is the only safe length.
  Critical therefore renders in the normal colour, which is a k9s limitation.
- **Modified and pending are both `amber`.** The style guide gives that colour to
  both jobs, and in k9s the two never label the same cell.
- **`info.fgColor` is `soft` and `info.sectionColor` is `text`.** The names are
  the wrong way round in k9s: `fgColor` paints the label column and the header
  context string, `sectionColor` paints the values.
- **`views.xray.fgColor` is `overlay`.** k9s uses it for the xray panel border
  only, never for text. Node text comes from `cursorColor`, which is applied to
  every node rather than just the cursor, so that takes `text`.
- **`views.xray.cursorTextColor` is set but unused.** k9s 0.51.0 reads it into
  the skin and never draws with it. It takes `deep`, the colour it would need if
  k9s ever paints text on the accent.

## Resolved drift

The hand-maintained skin carried two colours from outside the palette, and had no
light flavour:

| Was | Now |
| --- | --- |
| `#caea28` (accent, throughout) | `volt`, `#c8ff00` |
| `#71717a` (prompt suggestions) | `subtle`, `#787881` |

Three jobs also moved to match the style guide: the xray tree graphics from the
accent to `muted`, the log indicator from a solid accent bar to `surface`, and
status `addColor` from the accent to `jade`.

## Customising

Do not edit the YAML. It is generated from [`palette.json`](../palette.json) by
[`build.py`](build.py), and `check.py` fails if the two disagree. Change the
palette and run `./build.py` from the repository root.
