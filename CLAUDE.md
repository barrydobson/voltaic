# Voltaic

One palette, many app ports. British English throughout, including JSON keys
(`colours`, `flavours`, `licence`).

## Source of truth

`palette.json` is the only file to hand-edit. Generated: `README.md` colour
tables, `assets/palette/circles/*.png`, and each port's output (`zed/voltaic.json`).

Workflow: edit `palette.json` → `./build.py` → `./check.py`. `check.py` regenerates
everything in memory and diffs, so hand-edited output is caught, not silently kept.

## Gotchas

- **Odd hexes are deliberate.** Light `volt` is `#4c790f`, not Tailwind's `#4d7a0f`;
  light `amber` is `#9c5f07`, not `#a16207`. They are the contrast floor, not typos.
- **`rgb`/`hsl` in `palette.json` are derived** from `hex` and must be recomputed on change.
- **Stdlib only.** PNG swatches use `zlib` + `struct`. Do not add Pillow.
- **Measure, don't eyeball.** WCAG 2.1 contrast and CIEDE2000 separation. Colour
  intuition has been wrong repeatedly here, in both directions.
- **The light flavour is full.** On `#f0efed` there is no room for another accent
  clearing 4.5:1 while staying ~13 dE from `cyan`, `blue` and `teal`. Verify before adding.
- **`heavy` (50%) never sits behind text** — drops body text under 3:1 on dark.

## Contrast floors (enforced)

- 4.5:1 on `base` for anything rendering as text
- 3:1 for the six ANSI bright accents: `lime` `gold` `aqua` `flare` `sky` `lilac`
- `base` `deep` `surface` `overlay` `muted` `dim` exempt; low contrast is their job

## Ports

Each `<app>/build.py` exposes `generate(palette) -> {filename: text}`; root
`build.py` discovers `*/build.py`. Each port dir also needs a `README.md` with
install instructions. `docs/style-guide.md` decides which colour does which job —
read it before writing a port.

Ten so far: `atuin` `claude` `eza` `ghostty` `herdr` `k9s` `obsidian`
`starship` `vscode` `zed`.

## Reference material

- Hand-maintained originals: `~/_git/barrydobson/dotfiles/packages/{zed,k9s,ghostty,eza,starship,herdr,claude}/`.
  They predate the contrast fixes, so they record *decisions*, not current values.
  The VS Code original lived in a `vscode-theme-my-brand` repo, now retired; the
  `vscode/` port records what it used to do under "Resolved drift".
- The Obsidian original is `~/_git/barrydobson/delta-obsidian-theme`, a separate
  theme rather than a hand-maintained Voltaic. Its fonts and page styles are not
  ported; `obsidian/` records the colour side under "Resolved drift".
- Obsidian's CSS variables are only listed in full in the docs source. The
  published site is client-rendered, so `curl` returns an empty page; read the
  markdown instead:
  `gh api "repos/obsidianmd/obsidian-developer-docs/contents/en/Reference/CSS variables/<page>.md" --jq '.content' | base64 -d`
- Catppuccin is the structural reference for port layout and key coverage:
  `gh api repos/catppuccin/<port>/contents/<path> --jq '.content' | base64 -d`
  Files over 1 MB come back empty from that call; fetch those from
  `raw.githubusercontent.com` instead.
