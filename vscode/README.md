# Voltaic for VS Code

Both flavours, as VS Code colour themes. Selectable as **Voltaic Dark** and
**Voltaic Light**.

VS Code accepts 8-digit hex everywhere, so the tint scale is applied directly
rather than composited. Nothing in these files is flattened.

Everything the extension needs is generated here: both theme files and the
`package.json` that packages them. There is no separate extension repository.

## Install

This directory is the extension. `build.py` writes `package.json` alongside the
themes, so it packages and installs in place with no second repository and no
hand-written manifest:

```sh
npx @vscode/vsce package --no-dependencies
code --install-extension voltaic-theme-*.vsix --force
```

Reload the window, then run `Preferences: Color Theme` from the command palette.
`vsce` warns that it cannot find a `LICENSE`; the repository licence is
[`LICENCE`](../LICENCE) and the manifest declares `MIT`, so the warning is
cosmetic.

**Copying a folder into `~/.vscode/extensions` does not work.** Since profiles
landed, VS Code scans user extensions from the profile index at
`~/.vscode/extensions/extensions.json` and only falls back to listing the
directory when that file is missing. A hand-placed folder is never indexed, so
it is silently ignored with no error anywhere. `code --install-extension` writes
the index entry, which is what makes it the supported route.

Installing over the same version needs `--force`, so bump `VERSION` in
[`build.py`](build.py) when a rebuild is meant to ship. For a throwaway look
without touching the index at all, `code --extensionDevelopmentPath=$PWD` opens
a second window with the theme loaded.

## Following the system appearance

Set both flavours in `settings.json` and let VS Code switch:

```json
{
  "window.autoDetectColorScheme": true,
  "workbench.preferredDarkColorTheme": "Voltaic Dark",
  "workbench.preferredLightColorTheme": "Voltaic Light"
}
```

## Mapping

575 workbench colour keys, 44 TextMate rules covering 173 scopes, and 28
semantic token rules per flavour. The workbench keys are the full set VS Code
registers for the editor, terminal, panels, git, testing, debugging, merge,
minimap and symbol icons; extension-specific keys are not included.

| Area | Job | Colour |
| --- | --- | --- |
| `editor.background` | Editor canvas | `deep` |
| `sideBar` `activityBar` `statusBar` `titleBar` `panel` | Application chrome | `base` |
| `editorWidget` `menu` `notifications` `quickInput` `peekViewEditor` | Dialogs and popups | `surface` |
| `*.border` | Borders and separators | `overlay` |
| `focusBorder` `*.activeBorder` `progressBar` | Focus ring, active edges | `volt` |
| `editorIndentGuide.activeBackground1` `tree.indentGuidesStroke` | Guides and rules | `muted` |
| `editorLineNumber.foreground` `input.placeholderForeground` | Line numbers, placeholders | `dim` |
| `*.inactiveForeground` `statusBar.foreground` | Secondary text | `soft` |
| `gitDecoration.ignoredResourceForeground` `editorInlayHint.foreground` | Ignored, inlay hints | `subtle` |
| `icon.foreground` `list.highlightForeground` `activityBar.foreground` | Accent text and icons | `arc` |
| `button.foreground` `badge.foreground` `terminal.selectionForeground` | Text on an accent fill | `deep` |
| `textLink.foreground` `notificationLink.foreground` | Links | `blue` |
| `editorCursor.foreground` `terminalCursor.foreground` | Cursor | `volt` |
| `editor.selectionBackground` | Editor selection | `volt` at `tint` |
| `terminal.selectionBackground` | Terminal selection | solid `volt`, `deep` text |
| `scrollbarSlider` `minimapSlider` | Scrollbar and minimap thumb | `volt` at `faint`/`wash`/`tint` |
| `editor.findMatchBackground` | Current search match | `volt` at `veil` |
| `editorOverviewRuler.*` `minimap.*Highlight` | Ruler and minimap marks | the mark colour at `heavy` |
| `editorError` `editorWarning` `editorInfo` `editorHint` | Diagnostics | `ember` `amber` `blue` `soft` |
| `testing.icon{Passed,Failed,Queued,Skipped}` | Test results | `jade` `ember` `blue` `subtle` |
| `gitDecoration.{added,untracked}ResourceForeground` | Added, untracked | `jade` |
| `gitDecoration.{modified,renamed}ResourceForeground` | Modified, renamed | `amber` |
| `gitDecoration.deletedResourceForeground` | Deleted | `ember` |
| `gitDecoration.conflictingResourceForeground` | Merge conflict | `violet` |
| `diffEditor.insertedLineBackground` | Diff added | `jade` at `wash`, text at `tint` |
| `diffEditor.removedLineBackground` | Diff removed | `ember` at `wash`, text at `tint` |
| `merge.{current,incoming,common}*Background` | Merge regions | `jade` `blue` `violet` at `tint`/`veil` |
| `inputValidation.{error,warning,info}Background` | Validation messages | `ember` `amber` `blue` at `tint` |
| `terminal.ansi*` | The sixteen ANSI slots | the palette's ANSI mapping |
| `scmGraph.foreground1-5` | Commit graph branches | the [ordered series](../docs/style-guide.md#ordered-series) rotation |
| `charts.*` | Chart colours | named by meaning: `ember` `bronze` `amber` `jade` `blue` `violet` |

Syntax follows the [style guide](../docs/style-guide.md#syntax) directly:
keywords `volt`, strings `jade`, numbers and booleans `ember`, constants and
enum members `amber`, functions `blue`, types `cyan`, operators `ice`,
properties and config keys `blue`, struct fields `bronze`, namespaces `jade`,
tags `ember`, attributes `amber`, preprocessor and macros `violet`, comments and
punctuation `subtle`, brackets `soft`.

Font styles match the Zed port: italic for comments, attributes, booleans,
decorators and builtin variables; bold for escape sequences, headings and strong
emphasis. Nothing else is styled.

## Bracket pair colourisation

`editorBracketHighlight.foreground1-6` walk the colour wheel rather than ranking
by importance: `amber` `volt` `jade` `teal` `blue` `violet`. `ember` is held back
for `unexpectedBracket.foreground`, where it means the same thing it means
everywhere else. The bracket pair guides take the same six at `wash`, and the
active guide takes them opaque.

## Deviations

- **`terminal.background` is `base`, not `deep`.** The style guide gives the
  terminal canvas to `deep`, but in VS Code the terminal fills the bottom panel
  rather than owning a window. Matching `panel.background` keeps the panel one
  surface; a `deep` terminal reads as an inset editor, which in the light
  flavour is a visible seam.
- **`editorIndentGuide.background1` is `overlay`, not `muted`.** The guide gives
  indent guides to `muted`, which here is the *active* guide. The inactive one
  steps a tone quieter so the pair reads as a pair. The Zed port does the same.
- **The light active line is opaque `overlay`.** Tinting `overlay` over the light
  canvas composites to within a hair of the background and does not show, so the
  background tone is stepped instead. This is the case the style guide describes
  under [tints and overlays](../docs/style-guide.md#tints-and-overlays).
- **Hovering a coloured status bar item lifts the fill with `bright` at
  `faint`.** The obvious move is the bright sibling (`flare` for `ember`, `gold`
  for `amber`, `sky` for `blue`), but the bright tier sits at the 3:1 floor and
  in light it drops the `deep` text on the item to 3.4:1. Eight per cent of
  `bright` moves the fill away from its own text in both flavours instead.
- **`semanticTokenColors.property` is `blue`, covering struct fields too.** VS
  Code uses one semantic token type for both object properties and struct
  members, so it cannot split them the way the style guide does. `bronze` still
  reaches struct fields through the TextMate scopes (`variable.other.member`),
  which is where most languages resolve them.
- **The `.retired` testing icons are left at VS Code's defaults.** VS Code fades
  them from the live colours; setting them explicitly would flatten the
  distinction between a current and a stale result.

## Resolved drift

The hand-maintained theme carried nine colours from outside the palette:

| Was | Where | Now |
| --- | --- | --- |
| `#caea28` (84 uses) / `#4d7a0f` (99) | Accent, throughout | `volt` |
| `#a16207` (53 uses, light) | Warnings and constants | `amber`, `#9c5f07` |
| `#71717a` (29 uses) | Comments, inactive text | `subtle` |
| `#c0a36e` (5 uses, dark) | Properties and struct members | `bronze` |
| `#f5f5f4` (4 uses, light) | Tab and chrome background | `base` |
| `#6d28d9` (4 uses, light) | Constants and readonly variables | `amber` |
| `#2a0a0a` `#2a1a0a` `#0a1a2a` | Dark validation backgrounds | `ember` `amber` `blue` at `tint` |
| `#fff1f2` `#fefce8` `#eff6ff` | Light validation backgrounds | the same three at `tint` |
| `#2b2c45` | Dark active line border | Dropped; the fill carries it |
| `#65a30d` `#ca8a04` `#14b8a6` `#fafafa` | Light ANSI bright green, yellow, cyan, white | `lime` `gold` `aqua` `text` |

Three jobs also moved to match the style guide:

- **Success and created are `jade`, not `volt`.** The accent is already the
  cursor, the focus ring and the keyword colour, so it cannot also mean "this
  worked". That covers `editorGutter.addedBackground`, `debugIcon.startForeground`,
  `testing.iconPassed` and the git decorations.
- **Constants are `amber`, not a violet.** The old theme put them on `lilac` in
  dark and `#6d28d9` in light. `lilac` is an ANSI bright slot at the 3:1 floor,
  which is not a text colour, and the violet family belongs to macros.
- **ANSI bright white is `text`, not near-white.** In the light flavour the old
  theme mapped it to `#fafafa`, which is invisible on any light background. The
  greyscale ends run dark in light; this is the palette's ANSI map, not a
  per-port choice.
- **JSON keys are one colour.** The old theme rotated five colours by nesting
  depth. Every key in a JSON file is a property, so they are all `blue`.

## Customising

Do not edit the theme JSON or `package.json`. All three are generated from
[`palette.json`](../palette.json) by [`build.py`](build.py), and `check.py`
fails if they disagree. Change the palette and run `./build.py` from the
repository root. The theme labels in the manifest come from the flavour names in
the palette, so the picker and the palette cannot drift apart.

For a one-off tweak that should not live in the palette, override it in your own
`settings.json`:

```json
{
  "workbench.colorCustomizations": {
    "[Voltaic Dark]": {
      "editorInlayHint.foreground": "#8a8a94"
    }
  },
  "editor.tokenColorCustomizations": {
    "[Voltaic Dark]": {
      "comments": "#8a8a94"
    }
  }
}
```
