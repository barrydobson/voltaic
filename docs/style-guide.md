# Style guide

How to apply the Voltaic palette. Every port should make the same decision for the
same job, so that a status bar in one app means what it means in another.

Swatches show dark then light. Colour names are defined in
[`palette.json`](../palette.json) and tabulated in the [README](../README.md).

Legibility wins over consistency. Where a rule here produces something unreadable
in a particular app, deviate and say so in that port's README.

## Backgrounds and structure

| Function | Colour | |
| --- | --- | --- |
| Editor and terminal canvas | `deep` | <img src="../assets/palette/circles/dark-deep.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-deep.png" width="16" height="16" alt=""/> |
| Application and window background | `base` | <img src="../assets/palette/circles/dark-base.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-base.png" width="16" height="16" alt=""/> |
| Panels, dialogs, elevated surfaces | `surface` | <img src="../assets/palette/circles/dark-surface.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-surface.png" width="16" height="16" alt=""/> |
| Borders, hover states, active row | `overlay` | <img src="../assets/palette/circles/dark-overlay.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-overlay.png" width="16" height="16" alt=""/> |
| Focused border, active pane, focus ring | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Indent guides, rules, separators | `muted` | <img src="../assets/palette/circles/dark-muted.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-muted.png" width="16" height="16" alt=""/> |

## Tints and overlays

Translucent fills are the largest single category of colour in an editor theme and
the easiest place for ports to drift. The hand-built themes used ten different
opacity values; these five replace them. Do not invent a sixth.

| Step | Opacity | `volt` as 8-digit | `volt` over `base` (dark) | Typical use |
| --- | --- | --- | --- | --- |
| `faint` | 8% | `#c8ff0014` | `#181d0a` | Scrollbar thumbs, drop targets, inactive marks |
| `wash` | 14% | `#c8ff0024` | `#242b09` | Scrollbar thumb hover, subtle row highlight |
| `tint` | 20% | `#c8ff0033` | `#2f3a09` | Selections, search matches, read highlights, diff backgrounds |
| `veil` | 30% | `#c8ff004c` | `#425308` | Active line, write highlights, stronger emphasis |
| `heavy` | 50% | `#c8ff0080` | `#688406` | Overview ruler marks, find-match borders. Never behind text |

Ports that accept an alpha channel take the 8-digit form directly. Ports that do
not, which is most terminal tooling, take the composited opaque value instead.
`build.py` provides `rgba()` and `composite()` for both. Compositing blends in
sRGB rather than linear light, matching what the consuming applications do.

Two constraints are load-bearing, and `check.py` enforces the first:

**Nothing readable sits on `heavy`.** At 50% over dark `base`, `volt` drops body
text to 2.90:1. It is for marks and borders, never a background behind text.

**In light, tint with a foreground tone or step the background, never tint with a
background tone.** `overlay` at any alpha composites to within a hair of `base`,
because the top of the light ramp is compressed. Two things that do work: `text`
at `faint`, or `overlay` as an opaque fill. The active line uses the latter, a
1.21:1 step off the `deep` canvas.

Expect that band. A light-theme active line lands somewhere around 1.1-1.3:1
whichever technique is used, and Catppuccin Latte sits at 1.11:1 doing the same
job with `text` at 7%. It is a genre constraint, not a defect to engineer away.

## Typography

| Function | Colour | |
| --- | --- | --- |
| Body copy, primary text | `text` | <img src="../assets/palette/circles/dark-text.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-text.png" width="16" height="16" alt=""/> |
| Emphasised text, headings | `bright` | <img src="../assets/palette/circles/dark-bright.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-bright.png" width="16" height="16" alt=""/> |
| Secondary text, hints, labels | `soft` | <img src="../assets/palette/circles/dark-soft.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-soft.png" width="16" height="16" alt=""/> |
| Comments, punctuation, ignored files | `subtle` | <img src="../assets/palette/circles/dark-subtle.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-subtle.png" width="16" height="16" alt=""/> |
| Placeholders, disabled text, line numbers | `dim` | <img src="../assets/palette/circles/dark-dim.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-dim.png" width="16" height="16" alt=""/> |
| Accent text and icons | `arc` | <img src="../assets/palette/circles/dark-arc.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-arc.png" width="16" height="16" alt=""/> |
| Text on an accent fill | `deep` | <img src="../assets/palette/circles/dark-deep.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-deep.png" width="16" height="16" alt=""/> |
| Links and URLs | `blue` | <img src="../assets/palette/circles/dark-blue.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-blue.png" width="16" height="16" alt=""/> |

`arc` rather than `volt` carries accent *text*. In light it is the darker of the
two and clears AA comfortably, where `volt` only just does. Reserve `volt` for
fills, cursors and focus rings, where it is a shape rather than a glyph.

## Status and version control

| Function | Colour | |
| --- | --- | --- |
| Success, passing, merged | `jade` | <img src="../assets/palette/circles/dark-jade.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-jade.png" width="16" height="16" alt=""/> |
| Error, failure, killed | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |
| Warning, pending | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Information, new | `blue` | <img src="../assets/palette/circles/dark-blue.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-blue.png" width="16" height="16" alt=""/> |
| Hint | `soft` | <img src="../assets/palette/circles/dark-soft.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-soft.png" width="16" height="16" alt=""/> |
| Merge conflict | `violet` | <img src="../assets/palette/circles/dark-violet.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-violet.png" width="16" height="16" alt=""/> |
| Added, created, untracked | `jade` | <img src="../assets/palette/circles/dark-jade.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-jade.png" width="16" height="16" alt=""/> |
| Modified, renamed | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Deleted | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |
| Ignored, hidden | `subtle` | <img src="../assets/palette/circles/dark-subtle.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-subtle.png" width="16" height="16" alt=""/> |

Success is `jade`, not `volt`. The accent colour has to stay readable as "this is
Voltaic" rather than "this worked", and it is already doing duty as the cursor,
the focus ring and the keyword colour. The Zed and VS Code themes currently use
`volt` for success and created, which is drift to fix when they are regenerated.

## Ordered series

Charts, gauges and sparklines ask for several colours at once. Two rules cover it.

**A series that means something is not a series.** Pass and fail take `jade` and
`ember`. Normal, warning and critical take `jade`, `amber`, `ember`. Reach for the
rotation below only when the entries differ in identity rather than in state.

**Otherwise take the rotation in order**, stopping when you have enough:

| # | Colour | |
| --- | --- | --- |
| 1 | `blue` | <img src="../assets/palette/circles/dark-blue.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-blue.png" width="16" height="16" alt=""/> |
| 2 | `teal` | <img src="../assets/palette/circles/dark-teal.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-teal.png" width="16" height="16" alt=""/> |
| 3 | `bronze` | <img src="../assets/palette/circles/dark-bronze.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-bronze.png" width="16" height="16" alt=""/> |
| 4 | `ice` | <img src="../assets/palette/circles/dark-ice.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ice.png" width="16" height="16" alt=""/> |
| 5 | `lilac` | <img src="../assets/palette/circles/dark-lilac.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-lilac.png" width="16" height="16" alt=""/> |

Every pair is at least 15.3 dE apart in both flavours, so any prefix of the
rotation stays separated. The status colours are absent so that a categorical
series never reads as a state it does not have, and `volt` and `arc` are absent
because they carry chrome in every port and a series in them reads as furniture.

**The bright tier is not a second step.** `arc` and `lime`, `amber` and `gold`,
`teal` and `aqua` are the same hex in the dark flavour. A second series takes the
next entry in the rotation, never a lighter version of the first.

## File kinds

For anything that colours a directory listing.

| Kind | Colour | |
| --- | --- | --- |
| Regular files | `text` | <img src="../assets/palette/circles/dark-text.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-text.png" width="16" height="16" alt=""/> |
| Directories | `blue` | <img src="../assets/palette/circles/dark-blue.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-blue.png" width="16" height="16" alt=""/> |
| Symlinks | `teal` | <img src="../assets/palette/circles/dark-teal.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-teal.png" width="16" height="16" alt=""/> |
| Executables | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Pipes and FIFOs | `subtle` | <img src="../assets/palette/circles/dark-subtle.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-subtle.png" width="16" height="16" alt=""/> |
| Sockets | `dim` | <img src="../assets/palette/circles/dark-dim.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-dim.png" width="16" height="16" alt=""/> |
| Block and character devices | `flare` | <img src="../assets/palette/circles/dark-flare.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-flare.png" width="16" height="16" alt=""/> |
| Special files | `violet` | <img src="../assets/palette/circles/dark-violet.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-violet.png" width="16" height="16" alt=""/> |
| Mount points | `sky` | <img src="../assets/palette/circles/dark-sky.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-sky.png" width="16" height="16" alt=""/> |

## Listing metadata

The columns beside the filename: ownership, permission bits, size and age.

| Function | Colour | |
| --- | --- | --- |
| Your user and group | `bright`, `text` | <img src="../assets/palette/circles/dark-bright.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-bright.png" width="16" height="16" alt=""/> |
| Another user's | `soft` | <img src="../assets/palette/circles/dark-soft.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-soft.png" width="16" height="16" alt=""/> |
| Root | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |
| Write bit | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Execute bit | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Dates, inodes, block counts, octal modes | `soft` | <img src="../assets/palette/circles/dark-soft.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-soft.png" width="16" height="16" alt=""/> |

Permissions read as a grid rather than a sentence, so the read bit takes the owner
tier from the table above and the other two carry their own meaning: `amber` warns
that something is writable, `volt` matches the executable file kind.

**The size ramp escalates.** A file size is ordinal, not categorical, so it takes
one colour per magnitude and gets louder as the number grows. The unit takes the
same colour as its number, so `4.2M` reads as one token.

| Magnitude | Colour | |
| --- | --- | --- |
| Bytes | `soft` | <img src="../assets/palette/circles/dark-soft.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-soft.png" width="16" height="16" alt=""/> |
| Kilo | `text` | <img src="../assets/palette/circles/dark-text.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-text.png" width="16" height="16" alt=""/> |
| Mega | `blue` | <img src="../assets/palette/circles/dark-blue.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-blue.png" width="16" height="16" alt=""/> |
| Giga | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Tera and beyond | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |

Version control columns take the [status colours](#status-and-version-control)
unchanged. Type changes, where a file becomes a directory or a symlink, take
`cyan`: the status table has no entry for them, and the thing that changed is the
file's type.

## Terminal

| Function | Colour | |
| --- | --- | --- |
| Cursor | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Cursor text | `deep` | <img src="../assets/palette/circles/dark-deep.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-deep.png" width="16" height="16" alt=""/> |
| Selection background | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Selection text | `deep` | <img src="../assets/palette/circles/dark-deep.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-deep.png" width="16" height="16" alt=""/> |
| Active border | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Inactive border | `overlay` | <img src="../assets/palette/circles/dark-overlay.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-overlay.png" width="16" height="16" alt=""/> |

Terminal selection is a solid `volt` fill with `deep` text on top, at 16.7:1. That
is deliberately louder than the editor treatment below, because a terminal
selection is transient and usually a single line.

### ANSI

The sixteen slots are mapped in the [README](../README.md#terminal-ansi). Two
rules matter when porting.

**Bright does not mean lighter.** It means bolder and more saturated. Voltaic's
bright accents clear 3:1 rather than 4.5:1, because they carry emphasis and chrome
rather than body text. In the light flavour this is load-bearing: making the
bright tier literally lighter is what put ANSI white at 1.29:1 in the original
hand-built themes.

**The greyscale ends run dark in the light flavour.** Slots 7 and 15 map to `soft`
and `text`, not to near-white. Taking "white" literally on a light background
makes anything printed in it invisible. Catppuccin goes the other way here and
maps Latte's white slots to its light surfaces, so this is a deliberate
divergence, not an oversight.

## Syntax

| Syntax | Colour | |
| --- | --- | --- |
| Keywords | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Strings | `jade` | <img src="../assets/palette/circles/dark-jade.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-jade.png" width="16" height="16" alt=""/> |
| Numbers, booleans | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |
| Constants, enum members | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Functions, methods | `blue` | <img src="../assets/palette/circles/dark-blue.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-blue.png" width="16" height="16" alt=""/> |
| Types, classes, constructors | `cyan` | <img src="../assets/palette/circles/dark-cyan.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-cyan.png" width="16" height="16" alt=""/> |
| Operators | `ice` | <img src="../assets/palette/circles/dark-ice.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ice.png" width="16" height="16" alt=""/> |
| Object properties, config keys | `blue` | <img src="../assets/palette/circles/dark-bronze.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-bronze.png" width="16" height="16" alt=""/> |
| Struct fields, members | `bronze` |
| Variables, identifiers | `text` | <img src="../assets/palette/circles/dark-text.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-text.png" width="16" height="16" alt=""/> |
| Namespaces, modules | `jade` | <img src="../assets/palette/circles/dark-jade.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-jade.png" width="16" height="16" alt=""/> |
| Tags | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |
| Attributes | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Escape sequences | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |
| Regular expressions | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Preprocessor, macros | `violet` | <img src="../assets/palette/circles/dark-violet.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-violet.png" width="16" height="16" alt=""/> |
| Comments | `subtle` | <img src="../assets/palette/circles/dark-subtle.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-subtle.png" width="16" height="16" alt=""/> |
| Punctuation, delimiters | `subtle` | <img src="../assets/palette/circles/dark-subtle.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-subtle.png" width="16" height="16" alt=""/> |
| Brackets, braces | `soft` | <img src="../assets/palette/circles/dark-soft.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-soft.png" width="16" height="16" alt=""/> |

Editor selection is `volt` at roughly 15% over `base`, unlike the solid terminal
fill, because an editor selection can span a whole screen and a solid accent that
size is punishing.

`ice` is the one colour that changes character between flavours. In dark it is a
bright cyan; in light it is the same neutral grey as `soft`, because the light
blue band is already full with `cyan`, `blue` and `teal` and a fourth entry cannot
clear AA while staying distinguishable from all three. Operators are punctuation
more than they are words, so going neutral costs less than going unreadable.

Config keys are `blue`, not `bronze`. In a JSON or YAML file every key is a
`property`, so putting properties on `bronze` leaves whole files rendering in two
colours against `jade` strings. `bronze` keeps struct fields and members, where it
sits beside `amber` constants often enough to need the dE 12.7 separation between
them. Do not nudge either toward the other when porting.

## Markup

| Element | Colour | |
| --- | --- | --- |
| Headings | `volt` | <img src="../assets/palette/circles/dark-volt.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-volt.png" width="16" height="16" alt=""/> |
| Emphasis | `jade` | <img src="../assets/palette/circles/dark-jade.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-jade.png" width="16" height="16" alt=""/> |
| Strong emphasis | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Inline code, literals | `amber` | <img src="../assets/palette/circles/dark-amber.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-amber.png" width="16" height="16" alt=""/> |
| Link text | `blue` | <img src="../assets/palette/circles/dark-blue.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-blue.png" width="16" height="16" alt=""/> |
| Link URL | `cyan` | <img src="../assets/palette/circles/dark-cyan.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-cyan.png" width="16" height="16" alt=""/> |
| List markers | `ember` | <img src="../assets/palette/circles/dark-ember.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-ember.png" width="16" height="16" alt=""/> |
| Block quotes | `subtle` | <img src="../assets/palette/circles/dark-subtle.png" width="16" height="16" alt=""/> <img src="../assets/palette/circles/light-subtle.png" width="16" height="16" alt=""/> |
