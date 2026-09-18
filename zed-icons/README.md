# Voltaic Icons for Zed

File and folder icons for Zed's project panel and tabs, in both flavours:
`Voltaic Dark` and `Voltaic Light`. Separate from the [`zed`](../zed/) colour
theme; Zed picks an icon theme and a colour theme independently.

The artwork is not ours. It is vendored from
[catppuccin/vscode-icons](https://github.com/catppuccin/vscode-icons) (MIT, see
[`src/LICENCE.catppuccin`](src/LICENCE.catppuccin)), which draws 656 icons on a
16px grid as stroke-only paths. Only the colours are Voltaic.

## Install

Zed loads icon themes from extensions, not from a settings directory, so this
one installs as a dev extension:

1. Command palette → `zed: install dev extension`.
2. Pick this directory (`zed-icons/`).
3. Command palette → `icon theme selector: toggle`, choose `Voltaic Dark` or
   `Voltaic Light`.

Zed rebuilds the extension on each launch, so a `./build.py` at the repository
root plus a restart is enough to pick up a palette change.

## How it works

Upstream ships a `css-variables` icon set where every stroke is tagged with a
Catppuccin colour name rather than a hex:

```svg
<path fill="none" stroke="var(--vscode-ctp-peach)" d="..." />
```

That makes a port a name-to-name map. [`build.py`](build.py) substitutes each
variable for the Voltaic hex and writes `icons/dark/` and `icons/light/`.
`src/mapping.json` is upstream's generated Zed mapping, 1810 file suffixes and
421 named directories, with the flavour directory replaced by a placeholder.

## Colour mapping

| Catppuccin | Voltaic | Where it lands |
| --- | --- | --- |
| `text` | `text` | Generic file, and any icon with no colour of its own |
| `blue` | `blue` | Folders, TypeScript, Docker, Helm, C# |
| `sapphire` | `sky` | Go, Kotlin, Nix, Markdown, images |
| `sky` | `cyan` | Caddy, Flutter, Tauri, macOS, cloud folders |
| `teal` | `teal` | Prisma, Renovate, test and type folders |
| `green` | `jade` | Bash, Vue, Nuxt, Django, `package.json` |
| `yellow` | `amber` | JavaScript, JSON, certificates |
| `peach` | `bronze` | Rust, Git, Svelte |
| `red` `maroon` | `ember` | Ruby, Java, npm, audio, TOML |
| `pink` `flamingo` | `flare` | Sass, GraphQL, Storybook, fonts, security |
| `mauve` | `violet` | CSS, Terraform, Astro, Haskell, Vite |
| `lavender` | `lilac` | ESLint, Azure Pipelines, moonrepo |
| `rosewater` | `soft` | Bun, editorconfig, Husky, Pug |
| `overlay1` | `subtle` | Lockfiles, ignore files, tool config, generated output |

Every colour in that table already clears a contrast floor in `check.py`, so no
icon needs a separate one.

Four upstream names merge into two. Catppuccin's `red` and `maroon` are
neighbouring reds and its `pink` and `flamingo` are neighbouring pinks; Voltaic
has one colour in each band. Neither pair ever appears in the same icon, so
nothing that was two-tone becomes solid. `build.py` proves this on every run by
resolving each icon's colours and failing if two upstream names collide on one
hex, which also catches a future palette change that flattens two Voltaic
colours together.

## Deviations

- **The generic folder is `blue`, not `text`.** Upstream draws `_folder` and
  `_folder_open` in its text colour, the same as the generic file. The style
  guide's [file kinds](../docs/style-guide.md#file-kinds) table puts directories
  on `blue`, which is also what the [`eza`](../eza/) port does. The named folder
  icons carry their own colours and are left alone.
- **`file_icons.default` is set.** Zed falls back to `file_icons["default"]` for
  anything unmatched. Upstream leaves it unset, so the generic file icon it
  draws never renders and Zed's own default shows instead. This port points it
  at `_file.svg`.

## Known limitations

- **No monochrome variant.** Catppuccin ships one per flavour, every icon in the
  flavour's text colour, so that coloured diagnostic badges stand out. Adding it
  is a third and fourth theme over the same sources.
- **Zed's published schema is behind.** `named_directory_icons` is in Zed's
  source and works, but not in the `v0.2.0` schema the file declares. Upstream
  has the same mismatch.
- **Orphans are not swept.** `check.py` catches a stale or missing generated
  file but not an extra one, so an icon dropped from `src/icons/` leaves its
  output behind until it is deleted by hand.

## Updating the artwork

The vendored sources track upstream by hand. To refresh:

```sh
tmp=$(mktemp -d)
curl -sL https://github.com/catppuccin/vscode-icons/archive/refs/heads/main.tar.gz \
  | tar xz -C "$tmp" --strip-components=1
rm -f src/icons/*.svg
cp "$tmp"/icons/css-variables/*.svg src/icons/
cp "$tmp"/LICENSE src/LICENCE.catppuccin
```

`src/mapping.json` comes from
[catppuccin/zed-icons](https://github.com/catppuccin/zed-icons), which generates
it from the same project's TypeScript definitions:

```sh
curl -sL https://raw.githubusercontent.com/catppuccin/zed-icons/main/icon_themes/catppuccin-icons.json \
  | python3 -c '
import json, sys
theme = [t for t in json.load(sys.stdin)["themes"] if t["name"] == "Catppuccin Mocha"][0]
keys = ("directory_icons", "named_directory_icons", "chevron_icons",
        "file_stems", "file_suffixes", "file_icons")
text = json.dumps({k: theme[k] for k in keys}).replace("./icons/mocha/", "./icons/{flavour}/")
mapping = json.loads(text)
mapping["file_icons"]["default"] = {"path": "./icons/{flavour}/_file.svg"}
mapping["file_icons"] = dict(sorted(mapping["file_icons"].items()))
print(json.dumps(mapping, indent=2))' > src/mapping.json
```

Then run `./build.py` and `./check.py` from the repository root. `build.py`
fails if a refreshed icon introduces a colour collision, and `check.py` fails if
the generated icons no longer match the palette.

## Customising

Do not edit anything under `icons/` or `icon_themes/`. They are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`
fails if the two disagree. Change the palette, or the mapping in `build.py`,
and run `./build.py` from the repository root.
