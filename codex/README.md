# Voltaic for the Codex CLI

Both flavours as TextMate themes for the Codex CLI's terminal UI:
`voltaic-dark` and `voltaic-light`.

## Install

Copy the themes into Codex's theme directory:

```sh
mkdir -p ~/.codex/themes
cp voltaic-dark.tmTheme voltaic-light.tmTheme ~/.codex/themes/
```

Use `$CODEX_HOME/themes` instead if you have set `CODEX_HOME`. Then run
`/theme` in Codex, preview, and pick one. That saves it to `config.toml`:

```toml
[tui]
theme = "voltaic-dark"
```

Codex resolves the theme by filename, so the files have to keep their names.

## What Codex reads

A `.tmTheme` is a full editor theme, but Codex uses only part of it:

| Theme part | Where it renders | Colour |
| --- | --- | --- |
| Token foregrounds and bold | Fenced code blocks and diffs | Same rules as the [VS Code](../vscode/) port |
| `markup.inserted` background | Added lines in diffs | `jade` at `wash`, flattened onto `deep` |
| `markup.deleted` background | Removed lines in diffs | `ember` at `wash`, flattened onto `deep` |
| `codex.accent` | Codex's accent colour (always bold) | `volt` |
| `markup.quote` | Block quotes in replies | `subtle` |
| `entity.name.type` | Mermaid nodes, the activity chart | `cyan` |
| `comment` | Mermaid edges | `subtle` |

Codex ignores token backgrounds, italic and underline, and it keeps the
terminal's own background. The global `background` is there for other
TextMate consumers only.

## Deviations

- **Diff backgrounds are opaque.** Codex keeps the RGB of a scope background and
  drops its alpha, so `wash` is composited onto `deep` rather than written as an
  8-digit hex. On a terminal background other than `deep`, they will look
  slightly off.
- **Codex adjusts diff text for contrast.** It repaints token colours against
  the line background it draws, so a diff line may not show the exact hex.

## Customising

Do not edit the `.tmTheme` files. They are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`
fails if the two disagree. Change the palette and run `./build.py` from the
repository root. Token rules live in [`vscode/build.py`](../vscode/build.py).
