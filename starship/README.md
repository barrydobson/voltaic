# Voltaic for Starship

Both flavours as named palettes: `voltaic_dark` and `voltaic_light`. Starship has
no light/dark switch, so the two ship side by side and the `palette` line picks
one.

## Install

Starship has no include mechanism, so the palette has to live in your config.
Append [`voltaic.toml`](voltaic.toml) to `~/.config/starship/starship.toml`, then
move the `palette` line it brings with it to the top of the file, above every
table:

```sh
cat voltaic.toml >> ~/.config/starship/starship.toml
```

TOML assigns a bare key to whichever table precedes it, so `palette = "..."` left
part-way down the file ends up inside the last table. Starship then warns
`Error in 'Character' at 'palette': Unknown key` and falls back to its default
colours. Everything from `[palettes.voltaic_dark]` onwards can stay where it lands.

To switch flavour, change the one line:

```toml
palette = "voltaic_light"
```

Reload the prompt with `exec $SHELL` and check the result with
`starship explain`.

## Applying the theme

The palette only supplies names. Module styles stay in your own config, so
layout and colours remain separable. This is the mapping the
[style guide](../docs/style-guide.md) gives for a prompt:

| Prompt element | Colour |
| --- | --- |
| Frame, prompt character on success | `volt` |
| Segment separators, punctuation | `subtle` |
| OS glyph, username, accent text | `arc` |
| Directory | `blue` |
| Read-only directory, error character, exit status | `ember` |
| Git branch | `arc` |
| Git status (dirty, modified) | `amber` |
| Git staged count | `jade` |
| Kubernetes context, cloud profile | `blue` |
| Hostname | `violet` |

As a starting point:

```toml
[character]
success_symbol = "[╰⎯](volt)"
error_symbol = "[╰⎯](ember)"

[directory]
style = "blue"
read_only_style = "ember"

[git_branch]
style = "bold arc"

[git_status]
style = "bold amber"
staged = "[++\($count\)](jade)"

[kubernetes]
format = '[//](subtle) [$symbol$context](bold blue) '
```

## Deviations

- **Separators are `subtle`, not `muted`.** The style guide puts rules and
  separators on `muted`, but that is for drawn guides on a filled surface. As a
  glyph on the terminal canvas `muted` is 1.89:1 in dark and 1.40:1 in light.
  A `//` separator is punctuation, so it takes the punctuation colour: 4.52:1
  and 4.94:1.
- **The prompt character keeps `volt` on success, not `jade`.** It is the
  signature mark of the prompt rather than a status readout, and the error state
  is already carried by `ember`. Modules that genuinely report success or
  failure use `jade` and `ember`.
- **Language and runtime versions have no assigned role.** The style guide is
  silent on them. Go stays on `teal`, Node on `arc` and Python on `amber`,
  carried over from the hand-maintained config.
- **Avoid the bright tier for module text in light.** `gold` and `lime` sit at
  3.36:1 and 3.34:1 on the light canvas, which is the emphasis floor, not the
  text floor.

## Resolved drift

The hand-maintained config carried three colours from outside the palette:

| Was | Now |
| --- | --- |
| `#f59e0b` (aws) | `amber` |
| `#f7768e` (errors) | `ember` |
| `#d97757` (Claude marker) | `bronze` |

`#d97757` is Anthropic's brand orange and is not part of this theme. `bronze` is
the warm neutral and is otherwise unused in a prompt, so a Claude marker reads as
a marker rather than as an `amber` warning. Keep the literal instead if the brand
colour is the point.

## Customising

Do not edit `voltaic.toml`. It is generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py` fails
if the two disagree. Change the palette and run `./build.py` from the repository
root.
