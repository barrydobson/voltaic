# Voltaic for Zed

Both flavours in one file, selectable from Zed's theme picker as **Voltaic Dark**
and **Voltaic Light**.

## Install

Copy the theme into Zed's themes directory and restart:

```sh
mkdir -p ~/.config/zed/themes
cp voltaic.json ~/.config/zed/themes/
```

Then open the command palette and run `theme selector: toggle`.

To follow your system appearance, set both in `~/.config/zed/settings.json`:

```json
{
  "theme": {
    "mode": "system",
    "light": "Voltaic Light",
    "dark": "Voltaic Dark"
  }
}
```

## Customising

Do not edit `voltaic.json`. It is generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`
fails if the two disagree. Change the palette and run `./build.py` from the
repository root.

For a one-off tweak that should not live in the palette, use Zed's theme
overrides in your own `settings.json`:

```json
{
  "theme_overrides": {
    "Voltaic Dark": {
      "syntax": {
        "comment": { "color": "#8a8a94" }
      }
    }
  }
}
```

## Coverage

175 style keys and 104 syntax captures per flavour, matching the key set Zed's
schema supports: editor and terminal surfaces, ANSI including the dim row,
version control, diagnostics, minimap, debugger, indent-guide accents and the
vim mode indicator.

Colour choices follow the [style guide](../docs/style-guide.md). Two worth
knowing about, because they differ from the hand-maintained theme this replaces:

- **Success and created are `jade`, not `volt`.** The accent colour is already
  the cursor, the focus ring and the keyword colour, so it cannot also mean
  "this worked".
- **The light active line steps the background tone instead of tinting it.**
  Tinting `overlay` over `base` in light composites to within a hair of the
  background and does not show.
