# Voltaic for the Herdr app

Both flavours as Herdr app theme files. This is the desktop app (`herdr-app`),
not the herdr TUI; that one is the [herdr](../herdr/) port.

## Install

Copy both files into the app's themes folder:

```sh
cp voltaic-dark.json voltaic-light.json ~/.config/herdr-app/themes/
```

Then set both in `~/.config/herdr-app/settings.json` to follow the system appearance:

```json
{
  "theme": { "light": "voltaic-light", "dark": "voltaic-dark" }
}
```

The app reloads on save. A layout that sets its own `theme` (the shipped
Terminals and Herdr 98 layouts do) ignores this; the default `main` layout does not.

## Applying the theme

A theme file gives the terminal colours, and Herdr derives its panel colours from
them. `colors` overrides the derived colours by name. This port sets every name
the app documents, so nothing is derived:

| Name | Job | Colour |
| --- | --- | --- |
| `background` | Terminal canvas | `deep` |
| `canvas` | Behind cards | `base` |
| `chrome` | Sidebars and bars | `base` |
| `surface` | Panels | `surface` |
| `popover` | Menus, dialogs | `surface` |
| `raised` | Elevated controls | `overlay` |
| `hover` | Hover over a row or control | `muted` |
| `selected` | Selected row | `overlay` |
| `border` | Dividers, inactive borders | `overlay` |
| `input` | Input borders | `muted` |
| `foreground` | Primary text | `text` |
| `muted` | Secondary text | `soft` |
| `dim` | Hints, numbers, key captions | `subtle` |
| `accent` | Highlights, active borders | `volt` |
| `accent_foreground` | Text on an accent fill | `deep` |
| `solid` | Primary button | `volt` |
| `solid_foreground` | Primary button text | `deep` |
| `ring` | Focus ring | `volt` |
| `working` | Agent working | `amber` |
| `blocked` | Agent blocked | `ember` |
| `done` | Agent done | `teal` |
| `idle` | Agent idle | `jade` |
| `unknown` | Agent state unknown | `subtle` |

## Deviations

- **Selection is `volt` at `tint` over `deep`, not a solid `volt` fill.** Herdr
  takes no selection text colour, so text keeps its own colour under a selection
  and `volt` text would vanish into a `volt` fill. The tint is the same value
  Ghostty uses for search matches.
- **`dim` and `unknown` are `subtle`, not `dim`.** Same reason as the herdr port:
  `dim` falls under 3:1 on `surface`.
- **`hover` is `muted` and `selected` is `overlay`.** This keeps the herdr port's
  choice: rows already sit on `overlay` when selected, so hover steps one further.
- **`accent` is `volt`, not `arc`, wherever it renders as text.** Herdr uses one
  name for accent fills and accent text. `volt` clears AA in both flavours, only
  just in light.
- **Idle keeps `jade` and done keeps `teal`**, as in the herdr port.

## Customising

Do not edit the JSON files. They are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py` fails
if the two disagree. Change the palette and run `./build.py` from the repository
root.
