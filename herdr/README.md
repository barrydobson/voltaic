# Voltaic for herdr

The dark flavour as a `[theme.custom]` block. herdr layers custom tokens on top of
a built-in theme, so this overrides every token it exposes and the base theme
underneath only matters if herdr adds a new one.

Dark only. herdr can switch flavours with `theme.auto_switch` and the
`[theme.custom.light]` / `[theme.custom.dark]` subtables, but this port ships the
dark values in the shared table, so leave `auto_switch` off.

## Install

Append [`voltaic.toml`](voltaic.toml) to `~/.config/herdr/config.toml`:

```sh
cat voltaic.toml >> ~/.config/herdr/config.toml
```

`[theme.custom]` is a table header, so it is valid wherever it lands, as long as
your config does not already declare one. Pick a dark base theme above it:

```toml
[theme]
name = "terminal"
auto_switch = false
```

Apply it to a running server, or restart:

```sh
herdr server reload-config
herdr config check
```

Themes come from the client's local config, so when you attach to a remote
machine the theme still comes from the machine you are sitting at.

## Applying the theme

herdr's token names are Catppuccin's hue names, but each one has a fixed job in
the UI. The job is what the mapping follows:

| Token | Job | Colour |
| --- | --- | --- |
| `accent` | Highlights, active borders | `volt` |
| `panel_bg` | Tab bar, floating panels, overlays, modals | `surface` |
| `sidebar_bg` | Desktop sidebar background | `base` |
| `active_row_bg` | Active space and focused agent rows | `overlay` |
| `selection_bg` | Navigate-mode cursor row | `volt` at `tint` over `base` |
| `surface0` | Selected and focused items | `overlay` |
| `surface1` | Hover and active states | `muted` |
| `surface_dim` | Separators | `muted` |
| `overlay0` | Muted text: secondary info, numbers | `subtle` |
| `overlay1` | Slightly brighter muted text | `subtle` |
| `text` | Primary text | `text` |
| `subtext0` | Unfocused rows, dim labels | `soft` |
| `mauve` | Git branch and other secondary labels | `violet` |
| `green` | Agent idle | `jade` |
| `yellow` | Agent working | `amber` |
| `red` | Agent blocked | `ember` |
| `blue` | Unseen notifications | `blue` |
| `teal` | Agent done | `teal` |
| `peach` | Agent interrupted | `bronze` |

herdr takes no alpha, so the cursor row's `tint` is flattened onto `base` as
`#2f3a09`, the value the [style guide](../docs/style-guide.md) lists for it.

## Deviations

- **`overlay0` and `overlay1` are both `subtle`.** herdr has four text steps where
  Voltaic's ramp offers `dim`, `subtle`, `soft` and `text`. Taking `dim` for
  `overlay0` puts agent index numbers and the unknown-agent status at 2.29:1 on
  `panel_bg`, below even the 3:1 non-text floor, so both overlay steps take
  `subtle` at 4.05:1 and the distinction is dropped.
- **`surface_dim` is `muted`, not a near-background tone.** Despite the name it
  only ever renders as a foreground: the sidebar divider line, and the fallback
  colour when `panel_bg` is unset. That is the style guide's separator job. It
  shares `muted` with `surface1`, which is only ever a background, so the two
  never meet.
- **`mauve` is `violet`, not `arc`.** The style guide and the Starship port put a
  git branch on `arc`, but a focused workspace row carries `volt` accents beside
  the branch label and `arc` sits 7.5 dE from `volt`, under the ~13 dE this
  palette treats as distinguishable. `violet` keeps the label a separate colour.
- **Idle keeps `jade` and done keeps `teal`.** herdr splits agent states that the
  style guide has one success colour for. The two sit 15.5 dE apart, so the
  hue-faithful mapping stays legible as two states rather than one.
- **`peach` is `bronze`.** herdr documents it as the interrupted state and 0.9.1
  renders nothing with it. `amber` is already the working state, so the warm
  neutral takes it rather than a second yellow.

## Resolved drift

The hand-maintained config carried four values from outside the palette:

| Was | Now |
| --- | --- |
| `#f59e0b` (`yellow`) | `amber` |
| `#ff6b80` (`red`) | `ember` |
| `rgb(30,48,5)` (`selection_bg`) | `volt` at `tint` over `base` |
| `#a3e635` (`blue`) | `blue` |

The `blue` token is the unseen-notification accent, not a literal blue, so a lime
there was a legitimate reading of the name. It now takes `blue`, which is the
style guide's colour for information and new items.

## Customising

Do not edit `voltaic.toml`. It is generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py` fails
if the two disagree. Change the palette and run `./build.py` from the repository
root.
