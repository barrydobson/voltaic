# Voltaic for Neovim

Both flavours as Neovim colour schemes: `voltaic-dark` and `voltaic-light`. Each
is a single Lua file of `nvim_set_hl` calls with no setup function and no
options. Needs Neovim 0.10 or later for the Tree-sitter capture names.

## Install

Copy the schemes into your config's `colors` directory:

```sh
mkdir -p ~/.config/nvim/colors
cp colors/voltaic-dark.lua colors/voltaic-light.lua ~/.config/nvim/colors/
```

Or, with this repository cloned, put the port on the runtime path instead:

```lua
vim.opt.rtp:prepend("~/_git/barrydobson/voltaic/nvim")
```

Then load one in `init.lua`:

```lua
vim.cmd.colorscheme("voltaic-dark")
```

Each scheme sets `background` itself. Setting `background` afterwards reloads the
same scheme, so switch flavour with `:colorscheme`, not `:set background`.

## Coverage

Based on [catppuccin/nvim](https://github.com/catppuccin/nvim)'s core groups:
the editor UI, legacy syntax groups, Tree-sitter captures, diagnostics, LSP
references and the sixteen `terminal_color_*` slots, which follow the ANSI
mapping in the [README](../README.md#terminal-ansi).

Only groups that need a Voltaic colour are set. Neovim links most Tree-sitter
captures, every `@lsp.type.*` token and most legacy groups (`Conditional`,
`Keyword`, `Macro`) to a parent, and those links are left alone. Plugins that
link their groups to core ones, such as gitsigns, telescope and which-key, pick
up the scheme the same way. Catppuccin's per-plugin integrations are not ported.

## Deviations

- **Neovim takes no alpha.** Every tint is composited onto `deep`, the editor
  canvas, with `composite()` from the root `build.py`.
- **The active line steps to `overlay` in light**, as in the Zed port. The light
  ramp is compressed at the top, so a translucent `overlay` would not show.
- **Selection is `volt` at `tint` (20%)**, matching Zed, rather than the style
  guide's "roughly 15%".
- **`DiffChange` is `amber` at `faint`, `DiffText` at `tint`.** The changed line
  stays quieter than the changed text inside it.
- **`Special` is `ember`.** Neovim routes escape sequences, `self`/`this` and
  string interpolation punctuation through it, and escapes are `ember`.

## Known limitations

Light floats sit on `surface` (`#ffffff`) over a `deep` (`#faf9f7`) canvas, which
is barely a step. Set `vim.o.winborder = "rounded"` (Neovim 0.11+) to give them
an edge.

## Customising

Do not edit the files in `colors/`. They are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py` fails
if the two disagree. Change the palette and run `./build.py` from the repository
root. For a one-off tweak, call `vim.api.nvim_set_hl` after `:colorscheme` in
your own config.
