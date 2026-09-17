# Voltaic for Obsidian

Both flavours, as one Obsidian theme. Obsidian picks the flavour from the base
colour scheme in **Settings → Appearance**, so there is a single entry in the
theme list rather than a light and a dark one.

Obsidian is a browser, so the tint scale is applied as 8-digit hex directly.
Nothing in `theme.css` is composited.

Built against Obsidian 1.13. The manifest declares `minAppVersion` 1.13.0
because the callout type colours below take a colour value rather than the RGB
triplet older releases expected.

## Install

The theme is the two files in this directory, in a folder named for the theme:

```sh
OUT="/path/to/vault/.obsidian/themes/Voltaic"
mkdir -p "$OUT" && cp theme.css manifest.json "$OUT"
```

Or symlink the directory, so a rebuild lands without copying:

```sh
ln -s "$PWD" /path/to/vault/.obsidian/themes/Voltaic
```

Then pick **Voltaic** under Settings → Appearance → Themes. Obsidian reloads
`theme.css` when it changes, so a rebuild shows up without restarting.

## Mapping

Around 100 custom properties per flavour, covering the neutral ramp, the eight
named colours, and every variable Obsidian exposes for text, chrome, markup,
code, callouts and the graph. Anything not listed here derives from the ramp:
`--background-primary` is `--color-base-00`, `--background-secondary` is
`--color-base-20`, and so on.

| Variable | Job | Colour |
| --- | --- | --- |
| `--color-base-00` | Note canvas | `deep` |
| `--color-base-05` `-10` `-20` | Sidebars, ribbon, status bar, tab bar, code blocks | `base` |
| `--color-base-25` | Elevated surfaces | `surface` |
| `--color-base-30` | Borders | `overlay` |
| `--color-base-35` `-40` | Hovered borders, modal and prompt borders | `muted` |
| `--color-base-50` `-60` `-70` `-100` | Faint, ignored, muted and normal text | `dim` `subtle` `soft` `text` |
| `--color-{red,orange,yellow,green}` | Named colour slots | `ember` `bronze` `amber` `jade` |
| `--color-{cyan,blue,purple,pink}` | Named colour slots | `cyan` `blue` `violet` `flare` |
| `--accent-h/s/l` `--color-accent` `--interactive-accent` | Accent fills, focus rings | `volt` |
| `--color-accent-2` `--interactive-accent-hover` | Accent hover | `arc` |
| `--text-accent` | Accent text and active icons | `arc` |
| `--text-on-accent` | Text on an accent fill | `deep` |
| `--caret-color` | Caret | `volt` |
| `--text-selection` | Selection | `volt` at `tint` |
| `--text-highlight-bg` | `==highlight==` | `amber` at `tint` |
| `--background-modifier-{hover,border}` | Hover, borders | `overlay` |
| `--background-modifier-border-focus` | Focused input | `volt` |
| `--background-modifier-{error,success}` | Error, success fills | `ember`, `jade` |
| `--modal-background` `--interactive-normal` | Modals, buttons, form fields | `surface` |
| `--text-{success,warning,error}` | Status text | `jade` `amber` `ember` |
| `--scrollbar-thumb-bg` | Scrollbar thumb, hover | `volt` at `faint`, `wash` |
| `--indentation-guide-color` | Indent guides, active guide | `overlay`, `muted` |
| `--nav-item-background-{active,selected}` | Selected file | `volt` at `tint` |
| `--nav-item-color-highlighted` | Highlighted file | `arc` |
| `--h1-color` … `--h6-color` | Headings | `volt` |
| `--heading-formatting` | The `#` marks | `dim` |
| `--bold-color` `--italic-color` | Strong emphasis, emphasis | `amber`, `jade` |
| `--list-marker-color` | Bullets and numbers | `ember` |
| `--blockquote-border-color` | Block quote rule | `subtle` |
| `--tag-color` `--tag-background` | Tag pills | `arc` on `volt` at `faint` |
| `--link-color` | Internal links | `blue` |
| `--link-external-color` | External links | `cyan` |
| `--link-unresolved-{color,decoration-color}` | Unresolved links | `subtle`, `ember` underline |
| `--code-*` | Syntax highlighting | the [style guide](../docs/style-guide.md#syntax) rows |
| `--callout-*` | Callouts | through the named colours |
| `--graph-node` `--graph-node-focused` | Graph nodes, focused node | `soft`, `volt` |
| `--graph-node-{unresolved,tag,attachment}` | Graph node kinds | `dim` `arc` `blue` |

Syntax follows the [style guide](../docs/style-guide.md#syntax), with Obsidian's
coarser grouping resolved by each variable's own description: `--code-tag`
covers tags, symbols and constants, so it takes `ember` for tags;
`--code-important` covers regex and important, so it takes `amber`;
`--code-value` covers booleans and numbers, so it takes `ember` too.

## Deviations

- **The accent colour in Settings → Appearance does nothing.** Obsidian derives
  `--color-accent-1` and `-2` by shifting the picked accent, which would put two
  colours in the theme that are not in the palette. The accent variables are
  pinned to `volt` and `arc` instead.
- **Sidebars are `base`, not `surface`.** Obsidian gives sidebars, the ribbon,
  the status bar, the tab bar and menus one variable between them. Sidebars are
  chrome, so they take `base`, matching the VS Code and Zed ports. Menus and
  suggestion popups get `surface` back through the only two selectors in the
  file, because Obsidian has no variable for them.
- **Inline code needs a selector too.** `--code-normal` is the plain text inside
  a fenced block as well as the colour of inline code, so it stays `text` and a
  rule puts inline code on `amber`, per the markup table. The rule mirrors the
  shape of Obsidian's own `.markdown-rendered code` and
  `.cm-s-obsidian span.cm-inline-code`, because a bare `code` selector loses to
  both on specificity and the theme silently has no effect.
- **Code blocks take an outline, not a fill.** `--code-background` resolves to
  `base`, which is 1.01:1 off the `deep` canvas in dark, so a fenced block has no
  visible edge. Filling it is what everything else does and it is wrong here: on
  dark, `subtle` comments drop to 4.05:1 over `surface` and 3.41:1 over
  `overlay`, because `subtle` is tuned to clear 4.5:1 on `base` exactly.
  `--code-border-width: 1px` draws the block in `overlay` and costs no contrast.
- **Headings are `volt`, bold is `amber`, italic is `jade`.** Straight from the
  [markup table](../docs/style-guide.md#markup). It is louder in a prose app than
  in an editor, but it is the same decision Zed and VS Code make when they open a
  markdown file, and the point of the style guide is that the decision travels.
  Override it in a snippet if a vault of coloured bold is too much.
- **Tags are `arc` on a `volt` pill, not `ember`.** The style guide's tag row is
  about markup tags, `<div>` and friends, which in Obsidian is `--code-tag`. A
  `#tag` is a navigational label, so it takes accent text.
- **Warning callouts are `amber`; question callouts are `bronze`.** Obsidian
  sends `warning` to its orange slot and `question` to yellow. The style guide
  puts warnings on `amber`, so the two swap, which also keeps them apart.
- **`orange` is `bronze` and `pink` is `flare`.** The palette has no true orange
  or magenta. `bronze` is the only warm tan in it, and `flare` is the only tone
  that reads pink. Nothing in Obsidian's defaults places `--color-red` and
  `--color-pink` side by side, so the two reds never collide: Canvas uses red,
  orange, yellow, green, cyan and purple, and no callout type takes pink.
- **The ramp repeats.** Obsidian has twelve neutral steps; the palette has eight
  and spends three of them on text. `--color-base-05`, `-10` and `-20` are all
  `base`, and `-35` and `-40` are both `muted`. Inventing intermediate tones to
  fill the gaps is exactly the drift this repository exists to remove. In the
  light flavour `-25` also runs against the ramp, because `surface` is white:
  elevated things lift off the page rather than sinking into it.
- **Typography and layout are untouched.** Voltaic is a palette. Fonts, sizes,
  spacing and radii stay at Obsidian's defaults, so the theme composes with a
  snippet or another theme's typography rather than arguing with it.

## Resolved drift

The Delta theme in `delta-obsidian-theme` was the previous attempt. It kept
Obsidian's stock extended colours and carried its own neutrals:

| Was | Where | Now |
| --- | --- | --- |
| `#caea28` / `#a3e635` | Accent and accent hover | `volt`, `arc` |
| `#fb464c` `#e9973f` `#e0de71` | Obsidian's stock red, orange, yellow | `ember` `bronze` `amber` |
| `#53dfdd` `#027aff` `#a882ff` `#fa99cd` | Obsidian's stock cyan, blue, purple, pink | `cyan` `blue` `violet` `flare` |
| `#71717a` | Faint text | `subtle` |
| Stone ramp (`#fafaf9` … `#1c1917`) | Light flavour neutrals | The palette's light ramp |
| Lime-tinted hover fills | Hover states | `overlay` |

Delta's five embedded fonts, its `wiki-home` page styles and its Style Settings
block are not ported. They are typography and layout, not palette, so they stay
where they are; running both is a matter of keeping Delta's non-colour rules in
a snippet.

## Customising

Do not edit `theme.css` or `manifest.json`. Both are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`
fails if they disagree. Change the palette and run `./build.py` from the
repository root.

For a one-off tweak that should not live in the palette, put it in
`.obsidian/snippets/` and enable it under Settings → Appearance. Snippets load
after the theme, so a variable set there wins:

```css
.theme-dark,
.theme-light {
  --h1-color: var(--text-normal);
  --h2-color: var(--text-normal);
  --bold-color: var(--text-normal);
  --italic-color: var(--text-normal);
}
```
