# Voltaic for Claude Code

One file per flavour, `voltaic-dark.json` and `voltaic-light.json`.

## Install

Copy both into Claude Code's themes directory:

```sh
mkdir -p ~/.claude/themes
cp voltaic-dark.json voltaic-light.json ~/.claude/themes/
```

## Apply

Set the theme in `~/.claude/settings.json`. The value is `custom:` followed by
the file name without the extension:

```json
{
  "theme": "custom:voltaic-dark"
}
```

Claude Code has no system-appearance switch, so swap the line to
`custom:voltaic-light` to change flavour. Restart the session to pick it up.

## Customising

Do not edit the theme files. They are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`
fails if the two disagree. Change the palette and run `./build.py` from the
repository root.

For a one-off tweak, copy a generated file under a new name and edit that; the
`theme` setting picks whichever name you point it at.

## Coverage

All 47 override keys the hand-maintained theme set: the Claude mark and its
spinner, mode indicators, prompt and bash borders, message and memory surfaces,
diff and selection backgrounds, status colours and the rate-limit meter.

Claude Code paints into terminal cells, so nothing can be translucent. The diff
and selection backgrounds are accents composited onto `base` at a
[tint step](../docs/style-guide.md#tints-and-overlays) rather than left with an
alpha channel.

## Deviations

Colour choices follow the [style guide](../docs/style-guide.md). Four worth
knowing about:

- **`volt` carries accent text here, not just fills.** The guide reserves `volt`
  for fills, cursors and focus rings and puts accent text on `arc`. In a terminal
  UI almost everything is text, so that rule would leave `volt` unused. `volt`
  takes the signature marks and chrome (the Claude glyph, borders, mode
  indicators, the rate-limit fill) and `arc` takes the shimmer half of every
  accent pair, which is the role `palette.json` already gives it.
- **The `text` key is `text`, not `bright`.** The hand-maintained theme used
  `#fafafa`, which is `bright`. That is the emphasis tone; body copy is `text`.
- **The prompt border is `subtle`, not `muted`.** Same reason as the Starship
  port: the guide puts rules and separators on `muted`, but that is for drawn
  guides on a filled surface. As a box-drawing glyph on the terminal canvas
  `muted` is 1.89:1 in dark and 1.40:1 in light.
- **The warning shimmer only moves in light.** `warningShimmer` is `gold`, the
  bright partner of `amber`, but the dark flavour maps both to `#e0af68`, so the
  dark shimmer is static. Giving it a separate dark tone would mean a new palette
  entry for one animation frame.

## Resolved drift

The hand-maintained theme carried four colours from outside the palette, plus
three `rgb()` literals:

| Was | Now |
| --- | --- |
| `#f59e0b` (warning) | `amber` |
| `#ff6b80` (error) | `ember` |
| `#fcd34d` (warning shimmer) | `gold` |
| `#71717a` (inactive) | `subtle` |
| `rgb(30,48,5)` (selection) | `volt` at `tint` over `base` |
| `rgb(20,70,50)` / `rgb(90,20,30)` (diff) | `jade` / `ember` at `tint` over `base` |
| `rgb(30,55,42)` / `rgb(70,30,35)` (dimmed diff) | `jade` / `ember` at `wash` over `base` |

`#caea28` became `volt` (`#c8ff00`) and `#a3e635` became `arc`, along with every
other port.
