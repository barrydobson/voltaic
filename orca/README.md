# Voltaic for Orca

Both flavours as an Orca theme plugin. It adds two app themes, which also
colour the code editor, and two matching terminal themes.

## Install

The plugin is content only, so Orca installs it without an approval prompt.
From this repository's root:

```sh
orca plugin install "$PWD/orca"
```

Or, once this folder is pushed, install straight from GitHub:

```sh
orca plugin install https://github.com/barrydobson/voltaic/tree/main/orca
```

Then:

1. In **Settings → Appearance**, choose **Voltaic Dark** as the dark theme and
   **Voltaic Light** as the light theme.
2. In **Settings → Terminal**, choose the **Voltaic Dark** and **Voltaic Light**
   terminal themes.

To try a change without reinstalling, run `orca plugin dev watch orca`. It
reloads the themes each time `./build.py` rewrites them.

## What it covers

| File | Orca contribution |
| --- | --- |
| `themes/voltaic-{dark,light}.json` | App theme: interface tokens and `tokenColors` |
| `terminal/voltaic-{dark,light}.json` | Terminal theme: the sixteen ANSI slots, cursor and selection |
| `orca-plugin.json` | The manifest listing both |

Interface tokens follow the style guide. `base` is the app canvas and tab
strip, `deep` the editor and active tab, `surface` the sidebars, cards and
menus, and `overlay` borders and hover fills. `volt` carries primary buttons,
focus rings, the active tab line and the current workspace row. Charts take the
ordered series rotation. Git decorations and diff lines take the status
colours.

Code colours are the same rules as the [VS Code](../vscode/) port.

## Differences from the style guide

- **Editor selection is `volt` at `tint` (20%), not `wash`.** It matches the
  VS Code port. Orca shows it at half that opacity in an unfocused editor.
- **Descendant scopes are dropped.** Orca does not read selectors with spaces,
  such as `string.template variable`, so those rules from the VS Code port are
  left out rather than shipped dead.

## Checks

Orca silently drops any text/surface pair under 4.5:1, any git decoration under
3:1 on the sidebar, and any code colour under 3:1 on the editor. `build.py`
asserts the same floors, so a palette change that breaks one fails the build
instead of quietly falling back to Orca's defaults. It also asserts Orca's
16 KiB limit per theme file; the app themes are near 14 KB.

`orca plugin validate orca` runs Orca's own schema check.
