# Voltaic for Ghostty

One file per flavour, `voltaic-dark` and `voltaic-light`.

## Install

Copy both into Ghostty's themes directory:

```sh
mkdir -p ~/.config/ghostty/themes
cp voltaic-dark voltaic-light ~/.config/ghostty/themes/
```

On macOS `~/Library/Application Support/com.mitchellh.ghostty/themes/` works too.

## Apply

In `~/.config/ghostty/config`, either pick one:

```
theme = voltaic-dark
```

or follow the system appearance:

```
theme = dark:voltaic-dark,light:voltaic-light
```

Ghostty reloads the config with `cmd+shift+,` on macOS, `ctrl+shift+,` on Linux.

## Customising

Do not edit the theme files. They are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`
fails if the two disagree. Change the palette and run `./build.py` from the
repository root.

For a one-off tweak, set the key again in your own `config` below the `theme`
line; the later value wins.

## Coverage

Sixteen ANSI slots plus background, foreground, cursor, selection, search,
split divider and unfocused split fill.

Ghostty takes no alpha, so the search-match background is `volt` at the `tint`
step composited onto the canvas rather than left translucent. Everything else
is a palette colour as-is.

Colour choices follow the [style guide](../docs/style-guide.md). One thing
worth knowing, because it differs from the hand-maintained theme this replaces:

- **The background is `deep`, not `base`.** `deep` is the terminal canvas in
  every port; `base` is the application background, and here it dims the
  unfocused split instead.

`window-titlebar-background` and `window-titlebar-foreground` are not set. They
only apply on GTK with `window-theme = ghostty`, and nothing in the palette
distinguishes a titlebar from the `base` you would give it.
