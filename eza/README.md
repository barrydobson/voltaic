# Voltaic for eza

Both flavours, as eza themes. Tested against eza 0.23.5.

eza's theme format takes no alpha, so every value here is an opaque palette
colour. Nothing in the theme needed a tint, so nothing is composited.

## Install

Copy the flavour you want into eza's config directory as `theme.yml`:

```sh
OUT="${EZA_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/eza}"
mkdir -p "$OUT" && cp voltaic-dark.yml "$OUT/theme.yml"
```

eza reads exactly one `theme.yml`, so switching flavour means copying the other
file over it. A symlink works if you would rather flip it in one command:

```sh
ln -sf "$PWD/voltaic-light.yml" "$OUT/theme.yml"
```

`EZA_CONFIG_DIR` overrides the location. Without it, eza looks in
`$XDG_CONFIG_HOME/eza`, falling back to `~/.config/eza`.

## Applying the theme

Nothing to enable: eza picks the file up on the next run. `eza -l --git` exercises
most of what the theme colours. If a listing comes back monochrome, `NO_COLOR` is
set or `--color=never` is in an alias.

`EZA_COLORS` and `LS_COLORS` are applied after the theme, so anything set there
overrides these values for the keys it names.

## Mapping

| Key | Job | Colour |
| --- | --- | --- |
| `filekinds.*` | File kinds | [Per the style guide](../docs/style-guide.md#file-kinds) |
| `perms.*_read` | Read bit, by owner tier | `bright`, `text`, `soft` |
| `perms.*_write` | Write bit | `amber` |
| `perms.*_execute*` | Execute bit | `volt` |
| `perms.special_user_file` / `special_other` | setuid and setgid, sticky | `violet`, `dim` |
| `perms.attribute` | Extended attribute marker | `soft` |
| `size.number_*` / `unit_*` | Size ramp, bytes to terabytes | `soft`, `text`, `blue`, `amber`, `ember` |
| `size.major` / `minor` | Whole and fractional digits, uncoloured sizes | `text`, `soft` |
| `users.user_you` / `group_yours` | Owned by you | `bright`, `text` |
| `users.user_other` / `group_other` | Owned by someone else | `soft` |
| `users.user_root` / `group_root` | Owned by root | `ember` |
| `links.normal` | Hard link count | `teal` |
| `links.multi_link_file` | Count above one | `sky` |
| `git.new` | Added, untracked | `jade` |
| `git.modified` / `renamed` | Modified, renamed | `amber` |
| `git.deleted` | Deleted | `ember` |
| `git.typechange` | File became a directory or a symlink | `cyan` |
| `git.ignored` | Ignored | `subtle` |
| `git.conflicted` | Merge conflict | `violet` |
| `git_repo.branch_main` / `branch_other` | Repository branch | `text`, `violet` |
| `git_repo.git_clean` / `git_dirty` | Working tree state | `jade`, `amber` |
| `security_context.*` | SELinux context | `subtle`, `text`, `violet`, `dim` |
| `file_type.*` | Extension-based overrides | See below |
| `punctuation` | Column separators, tree lines | `subtle` |
| `date`, `inode`, `blocks`, `octal` | Metadata columns | `soft` |
| `header` | Column headings | `bright` |
| `flags` | BSD file flags | `violet` |
| `symlink_path` | Symlink target | `teal` |
| `control_char` | Control character in a filename | `amber` |
| `broken_symlink` / `broken_path_overlay` | Dangling link, missing segment | `ember`, `dim` |

`file_type` repaints the filename, so it shares a column with `filekinds` and its
colours are chosen to stay clear of it:

| Type | Colour | | Type | Colour |
| --- | --- | --- | --- | --- |
| Image | `amber` | | Compressed | `lilac` |
| Video | `ember` | | Temporary | `subtle` |
| Lossy audio | `jade` | | Compiled | `flare` |
| Lossless audio | `teal` | | Build | `soft` |
| Cryptography | `bronze` | | Source | `cyan` |
| Document | `text` | | | |

Ownership, permissions, sizes and the git columns follow the
[listing metadata](../docs/style-guide.md#listing-metadata) rules, which this port
added to the style guide.

## Deviations

- **Source files are `cyan`, not `blue`.** The style guide gives directories to
  `blue`, and directories and source files are the two most common things in a
  listing. `cyan` is the syntax colour for types, so code keeps a code colour.
- **Lossless audio shares `teal` with symlinks.** The style guide gives symlinks
  `teal`, and the light flavour has nothing else left in that band: `ice` collapses
  onto `soft` in light, `aqua` is a hair from `teal`. eza prints a symlink as
  `name -> target`, so the arrow disambiguates what the hue does not.
- **Compiled artefacts share `flare` with block and character devices.** Devices
  never appear in a project listing, and temporary files share `subtle` with pipes
  on the same reasoning.
- **`date` is `soft`, not an accent.** Most eza themes colour the date column.
  Here it is metadata beside the size and inode columns, and the style guide puts
  secondary text on `soft`.
- **`git.modified` and `git.renamed` are both `amber`.** The style guide gives
  that colour to both jobs, and eza already prints a distinct letter for each.
- **`security_context` is nested under `selinux`.** eza's schema is
  `security_context.selinux.{colon,user,role,typ,range}` with a sibling `none`.
  A flat block parses without error and is silently discarded, which is what the
  Catppuccin port does.

## Resolved drift

The hand-maintained theme carried three colours from outside the palette, and had
no light flavour:

| Was | Now |
| --- | --- |
| `#caea28` (executables, execute bits, git new) | `volt`, `#c8ff00` |
| `#71717a` (pipes, ignored, punctuation) | `subtle`, `#787881` |
| `#d4bff0` (compressed) | `lilac`, unchanged in dark, now correct in light |

Four jobs also moved to match the style guide: git `new` and `git_clean` from the
accent to `jade`, `git_dirty` from `ember` to `amber`, the size ramp from a
blue-violet scatter to an escalating ramp, and `date` from `amber` to `soft`.

## Customising

Do not edit the YAML. It is generated from [`palette.json`](../palette.json) by
[`build.py`](build.py), and `check.py` fails if the two disagree. Change the
palette and run `./build.py` from the repository root.
