# Voltaic for Atuin

Both flavours as Atuin themes: `voltaic-dark` and `voltaic-light`. Atuin has no
light/dark switch, so the two ship side by side and the `name` line picks one.

## Install

Copy the flavour you want into Atuin's theme directory:

```sh
mkdir -p ~/.config/atuin/themes
cp voltaic-dark.toml voltaic-light.toml ~/.config/atuin/themes/
```

Then name it in `~/.config/atuin/config.toml`:

```toml
[theme]
name = "voltaic-dark"
```

Atuin resolves the theme by filename, so `voltaic-dark.toml` has to keep its
name. Check the result with `atuin search -i`.

## Key mapping

Atuin exposes fifteen "meanings" rather than named UI elements. This is where
each one shows up, and the colour it takes from the
[style guide](../docs/style-guide.md):

| Meaning | Where it renders | Colour |
| --- | --- | --- |
| `Base` | Command text, list rows, plain output | `text` |
| `Important` | Selected tab, inspector command heading (bold) | `bright` |
| `Title` | Unused by the current TUI; falls back to `Important` | `arc` |
| `Annotation` | Date, directory, host and user columns, separators, inspector labels | `soft` |
| `Guidance` | Relative time column, key hints | `blue` |
| `Muted` | Duration in non-interactive output, stats bars | `subtle` |
| `AlertInfo` | Duration of a command that exited 0 | `jade` |
| `AlertWarn` | Matched search characters on the selected row | `amber` |
| `AlertError` | Duration of a failed command, selected row's command | `ember` |
| `SyntaxCommand` | Command name | `volt` |
| `SyntaxFlag` | Arguments starting with `-` | `amber` |
| `SyntaxString` | Quoted strings and heredoc bodies | `jade` |
| `SyntaxVariable` | `$VAR` expansions and assignments | `violet` |
| `SyntaxOperator` | `\| & ; < > ( ) { } $ \`` | `ice` |
| `SyntaxComment` | Comments | `subtle` |

Syntax highlighting needs Atuin built with tree-sitter support; without it every
command renders in `Base`.

## Deviations

- **`AlertInfo` is `jade`, not `volt`.** Atuin uses it for the exit-0 duration,
  which is a success readout, and the style guide keeps success on `jade`.
- **`SyntaxCommand` is `volt`.** The command name is the keyword of a shell line
  and the only token that earns the signature accent. Everything else in the
  line is an argument to it.
- **`SyntaxFlag` is `amber`, not `cyan`.** Atuin's default puts flags on dark
  cyan, but `cyan` carries types and constructors in Voltaic. A flag modifies a
  command, which is the `amber` attribute role.
- **`SyntaxVariable` is `violet`, not `text`.** The style guide puts variables on
  `text`, but that is the same colour as `Base`, so an expansion would vanish
  into the surrounding command. `violet` is the substitution colour and matches
  Atuin's magenta default.
- **`Annotation` is `soft`, not `subtle`.** It carries the metadata columns,
  which the style guide reads as listing metadata rather than punctuation. That
  leaves a readable three-step ramp: `text` for commands, `soft` for metadata,
  `subtle` for durations and comments.

## Known limitations

Atuin's meanings are shared across contexts it renders differently. `AlertError`
colours both a failed command's duration and the selected row's command text, so
the selected row reads as an error. `AlertWarn` colours matched search characters
as well as warnings. One key each, no way to split them from a theme file.

## Customising

Do not edit `voltaic-dark.toml` or `voltaic-light.toml`. They are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py` fails
if the two disagree. Change the palette and run `./build.py` from the repository
root.
