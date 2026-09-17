#!/usr/bin/env python3
"""Generate the VS Code colour themes from palette.json."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build as core

HERE = pathlib.Path(__file__).parent
OUTPUT = {"dark": "voltaic-dark-color-theme.json",
          "light": "voltaic-light-color-theme.json"}

NONE = "#00000000"

# Bracket pair colourisation walks the wheel rather than ranking by importance.
# `ember` is absent because it marks the unexpected bracket.
RAINBOW = ["amber", "volt", "jade", "teal", "blue", "violet"]

# The categorical rotation from the style guide, for the commit graph.
SERIES = ["blue", "teal", "bronze", "ice", "lilac"]

# TextMate rules, one per entry: (name, colour, font style, scopes). VS Code
# resolves these by scope specificity rather than list order, so a longer scope
# always wins over a shorter one and the order here is for reading only.
SYNTAX = [
    ("Variables and plain text", "text", "", [
        "text", "source", "variable", "variable.other", "variable.other.readwrite",
        "punctuation.definition.variable", "meta.template.expression",
        "string.template variable", "string variable"]),
    ("Punctuation and delimiters", "subtle", "", [
        "punctuation", "punctuation.separator", "punctuation.terminator",
        "punctuation.definition.tag", "meta.tag.sgml"]),
    ("Brackets and braces", "soft", "", [
        "punctuation.definition.block", "punctuation.definition.parameters",
        "punctuation.definition.array", "punctuation.section",
        "meta.brace.round", "meta.brace.square", "meta.brace.curly"]),
    ("Comments", "subtle", "italic", [
        "comment", "punctuation.definition.comment",
        "comment.block.documentation", "string.quoted.docstring"]),
    ("Documentation tags", "soft", "italic", [
        "comment.block.documentation storage.type.class.jsdoc",
        "comment.block.documentation entity.name.type.instance.jsdoc",
        "comment.block.documentation variable.other.jsdoc",
        "punctuation.definition.block.tag.jsdoc"]),
    ("Strings", "jade", "", [
        "string", "string.quoted", "string.template", "string.heredoc",
        "punctuation.definition.string", "string.quoted.other.lt-gt.include"]),
    ("Escape sequences", "ember", "bold", [
        "constant.character.escape", "constant.character.entity",
        "punctuation.definition.entity"]),
    ("Template interpolation punctuation", "ember", "", [
        "punctuation.definition.template-expression",
        "punctuation.section.embedded"]),
    ("Regular expressions", "amber", "", [
        "string.regexp", "constant.other.character-class.regexp",
        "keyword.operator.quantifier.regexp", "keyword.operator.or.regexp",
        "keyword.control.anchor.regexp", "keyword.other.back-reference.regexp"]),
    ("Regex groups and character classes", "ice", "", [
        "punctuation.definition.group.regexp",
        "punctuation.definition.character-class.regexp"]),
    ("Numbers", "ember", "", [
        "constant.numeric", "keyword.other.unit.user-defined",
        "keyword.other.unit.suffix.floating-point"]),
    ("Booleans and language constants", "ember", "italic", [
        "constant.language", "constant.language.boolean",
        "constant.language.null", "constant.language.undefined"]),
    ("Constants and enum members", "amber", "", [
        "constant.other", "variable.other.constant", "entity.name.constant",
        "support.constant", "variable.other.enummember",
        "meta.enum variable.other.readwrite"]),
    ("Keywords", "volt", "", [
        "keyword", "keyword.control", "keyword.other", "storage", "storage.type",
        "storage.modifier", "keyword.operator.word", "keyword.operator.new",
        "keyword.operator.expression", "punctuation.definition.keyword"]),
    ("Operators", "ice", "", [
        "keyword.operator", "keyword.operator.assignment",
        "keyword.operator.comparison", "keyword.operator.relational",
        "keyword.operator.arithmetic", "keyword.operator.logical",
        "keyword.operator.ternary", "punctuation.accessor",
        "punctuation.separator.key-value", "storage.type.function.arrow"]),
    ("Functions and methods", "blue", "", [
        "entity.name.function", "entity.name.function.call",
        "entity.name.function.member", "meta.function-call entity.name.function",
        "meta.function-call.method", "support.function", "variable.function"]),
    ("Types, classes and constructors", "cyan", "", [
        "entity.name.type", "entity.name.class", "entity.name.struct",
        "entity.name.enum", "entity.name.type.parameter",
        "entity.other.inherited-class", "support.class", "support.type",
        "meta.type", "meta.type-alias", "meta.function-call.constructor"]),
    ("Object properties and config keys", "blue", "", [
        "support.type.property-name", "support.type.vendored.property-name",
        "meta.object-literal.key", "meta.property.object",
        "variable.other.property", "variable.other.object.property",
        "entity.name.tag.yaml", "variable.key.toml"]),
    ("Struct fields and members", "bronze", "", [
        "variable.other.member", "variable.other.field",
        "entity.name.variable.field"]),
    ("Parameters", "text", "", [
        "variable.parameter", "meta.parameter", "meta.function.parameters"]),
    ("Builtin and special variables", "ember", "italic", [
        "variable.language", "variable.language.this", "variable.language.self",
        "variable.language.super", "support.variable",
        "variable.parameter.function.language.special"]),
    ("Namespaces and modules", "jade", "", [
        "entity.name.namespace", "entity.name.module", "entity.name.package",
        "entity.name.import", "entity.name.section",
        "entity.name.type.namespace", "entity.name.type.module",
        "entity.other.attribute-name.table.toml"]),
    ("Tags", "ember", "", ["entity.name.tag"]),
    ("Attributes", "amber", "italic", ["entity.other.attribute-name"]),
    ("Annotations, decorators and macros", "violet", "italic", [
        "meta.annotation", "meta.attribute", "meta.decorator",
        "meta.function.decorator", "entity.name.function.decorator",
        "entity.name.function.macro", "punctuation.decorator",
        "punctuation.definition.annotation", "punctuation.definition.attribute",
        "punctuation.definition.decorator", "storage.type.annotation"]),
    ("Preprocessor directives", "violet", "", [
        "keyword.control.directive", "punctuation.definition.directive",
        "meta.preprocessor"]),
    ("CSS pseudo-classes and elements", "ice", "", [
        "entity.other.attribute-name.pseudo-class",
        "entity.other.attribute-name.pseudo-element"]),
    ("Markdown headings", "volt", "bold", [
        "markup.heading", "punctuation.definition.heading"]),
    ("Markdown emphasis", "jade", "italic", ["markup.italic"]),
    ("Markdown strong emphasis", "amber", "bold", ["markup.bold"]),
    ("Markdown strikethrough", "subtle", "strikethrough", ["markup.strikethrough"]),
    ("Markdown link text", "blue", "", [
        "string.other.link.title", "string.other.link.description"]),
    ("Markdown link URL", "cyan", "underline", ["markup.underline.link"]),
    ("Inline code and literals", "amber", "", [
        "markup.inline.raw", "text.literal", "fenced_code.block.language"]),
    ("Code blocks", "text", "", ["markup.fenced_code", "markup.raw.block"]),
    ("List markers", "ember", "", [
        "punctuation.definition.list.begin", "markup.list punctuation.definition"]),
    ("Block quotes", "subtle", "italic", [
        "markup.quote", "punctuation.definition.quote.begin"]),
    ("Horizontal rules", "subtle", "", ["meta.separator"]),
    ("Diff header", "blue", "", ["meta.diff.header", "meta.diff.range"]),
    ("Diff added", "jade", "", ["markup.inserted", "meta.diff.header.to-file"]),
    ("Diff removed", "ember", "", ["markup.deleted", "meta.diff.header.from-file"]),
    ("Diff changed", "amber", "", ["markup.changed"]),
    ("Invalid", "ember", "underline", ["invalid", "invalid.illegal"]),
    ("Deprecated", "amber", "strikethrough", ["invalid.deprecated"]),
]

# Semantic tokens win over TextMate scopes where the language server supplies
# them, so they repeat the same decisions rather than adding new ones.
SEMANTIC = {
    "variable": ("text", ""),
    "variable.readonly": ("amber", ""),
    "variable.defaultLibrary": ("ember", "italic"),
    "parameter": ("text", ""),
    "property": ("blue", ""),
    "property.readonly": ("amber", ""),
    "enumMember": ("amber", ""),
    "namespace": ("jade", ""),
    "type": ("cyan", ""),
    "type.defaultLibrary": ("cyan", ""),
    "class": ("cyan", ""),
    "interface": ("cyan", ""),
    "struct": ("cyan", ""),
    "enum": ("cyan", ""),
    "typeParameter": ("cyan", ""),
    "function": ("blue", ""),
    "method": ("blue", ""),
    "macro": ("violet", ""),
    "decorator": ("violet", "italic"),
    "keyword": ("volt", ""),
    "selfKeyword": ("ember", "italic"),
    "operator": ("ice", ""),
    "string": ("jade", ""),
    "number": ("ember", ""),
    "boolean": ("ember", "italic"),
    "comment": ("subtle", "italic"),
    "event": ("violet", ""),
    "label": ("amber", ""),
}

# Symbols in the outline, breadcrumbs and completion list. Same jobs as the
# syntax table, named by symbol kind instead of by scope.
SYMBOLS = {
    "text": "text", "variable": "text", "array": "soft", "object": "soft",
    "null": "ember", "boolean": "ember", "number": "ember", "string": "jade",
    "constant": "amber", "enumerator": "amber", "enumeratorMember": "amber",
    "unit": "amber", "snippet": "amber", "class": "cyan", "interface": "cyan",
    "struct": "cyan", "typeParameter": "cyan", "constructor": "cyan",
    "function": "blue", "method": "blue", "property": "blue", "key": "blue",
    "reference": "blue", "field": "bronze", "keyword": "volt",
    "operator": "ice", "module": "jade", "namespace": "jade",
    "package": "jade", "event": "violet", "color": "violet",
    "file": "arc", "folder": "arc",
}


def colours(palette, flavour):
    c = {k: v["hex"] for k, v in palette["flavours"][flavour]["colours"].items()}
    a = palette["alpha"]

    def tint(name, step):
        """8-digit hex. VS Code composites these itself, over whatever is beneath."""
        return core.rgba(c[name], a[step])

    def lift(name):
        """A hover step on an accent fill. `bright` at `faint` moves the fill away
        from the `deep` text on top of it in both flavours, where the bright tier
        moves towards it and drops the pair under AA in light."""
        return core.composite(c["bright"], a["faint"], c[name])

    # The light ramp is compressed at the top, so tinting `overlay` over the
    # editor canvas would not show. Step the background tone instead.
    active_line = tint("overlay", "veil") if flavour == "dark" else c["overlay"]

    s = {
        "focusBorder": c["volt"],
        "foreground": c["text"],
        "disabledForeground": c["dim"],
        "descriptionForeground": c["soft"],
        "errorForeground": c["ember"],
        "widget.border": c["overlay"],
        "widget.shadow": tint("overlay", "heavy"),
        "selection.background": tint("volt", "tint"),
        "icon.foreground": c["arc"],
        "sash.hoverBorder": c["volt"],

        "textBlockQuote.background": c["surface"],
        "textBlockQuote.border": c["overlay"],
        "textCodeBlock.background": c["surface"],
        "textLink.foreground": c["blue"],
        "textLink.activeForeground": c["arc"],
        "textPreformat.foreground": c["amber"],
        "textSeparator.foreground": c["muted"],

        "activityBar.background": c["base"],
        "activityBar.foreground": c["arc"],
        "activityBar.inactiveForeground": c["dim"],
        "activityBar.border": c["overlay"],
        "activityBar.activeBorder": c["volt"],
        "activityBar.activeBackground": NONE,
        "activityBar.activeFocusBorder": c["volt"],
        "activityBar.dropBorder": c["volt"],
        "activityBarBadge.background": c["volt"],
        "activityBarBadge.foreground": c["deep"],
        "activityBarTop.background": c["base"],
        "activityBarTop.foreground": c["arc"],
        "activityBarTop.inactiveForeground": c["dim"],
        "activityBarTop.activeBorder": c["volt"],
        "activityBarTop.dropBorder": c["volt"],

        "badge.background": c["volt"],
        "badge.foreground": c["deep"],

        "banner.background": c["surface"],
        "banner.foreground": c["text"],
        "banner.iconForeground": c["arc"],

        "breadcrumb.background": c["base"],
        "breadcrumb.foreground": c["soft"],
        "breadcrumb.focusForeground": c["text"],
        "breadcrumb.activeSelectionForeground": c["arc"],
        "breadcrumbPicker.background": c["surface"],

        "button.background": c["volt"],
        "button.foreground": c["deep"],
        "button.hoverBackground": c["arc"],
        "button.border": NONE,
        "button.separator": tint("deep", "veil"),
        "button.secondaryBackground": c["overlay"],
        "button.secondaryForeground": c["text"],
        "button.secondaryHoverBackground": c["muted"],
        "checkbox.background": c["surface"],
        "checkbox.border": c["overlay"],
        "checkbox.foreground": c["arc"],

        "dropdown.background": c["surface"],
        "dropdown.listBackground": c["surface"],
        "dropdown.border": c["overlay"],
        "dropdown.foreground": c["text"],

        "commandCenter.background": c["surface"],
        "commandCenter.foreground": c["soft"],
        "commandCenter.activeForeground": c["text"],
        "commandCenter.inactiveForeground": c["dim"],
        "commandCenter.activeBackground": c["overlay"],
        "commandCenter.border": c["overlay"],
        "commandCenter.inactiveBorder": c["overlay"],
        "commandCenter.activeBorder": c["volt"],
        "commandCenter.debuggingBackground": tint("amber", "tint"),

        "debugToolBar.background": c["surface"],
        "debugToolBar.border": c["overlay"],
        "debugExceptionWidget.background": c["surface"],
        "debugExceptionWidget.border": c["ember"],
        "debugTokenExpression.name": c["bronze"],
        "debugTokenExpression.value": c["text"],
        "debugTokenExpression.string": c["jade"],
        "debugTokenExpression.number": c["ember"],
        "debugTokenExpression.boolean": c["ember"],
        "debugTokenExpression.error": c["ember"],
        "debugIcon.breakpointForeground": c["ember"],
        "debugIcon.breakpointDisabledForeground": tint("ember", "veil"),
        "debugIcon.breakpointUnverifiedForeground": c["subtle"],
        "debugIcon.breakpointCurrentStackframeForeground": c["amber"],
        "debugIcon.breakpointStackframeForeground": c["muted"],
        "debugIcon.startForeground": c["jade"],
        "debugIcon.pauseForeground": c["amber"],
        "debugIcon.stopForeground": c["ember"],
        "debugIcon.disconnectForeground": c["ember"],
        "debugIcon.restartForeground": c["jade"],
        "debugIcon.continueForeground": c["jade"],
        "debugIcon.stepOverForeground": c["blue"],
        "debugIcon.stepIntoForeground": c["blue"],
        "debugIcon.stepOutForeground": c["blue"],
        "debugIcon.stepBackForeground": c["blue"],
        "debugConsole.infoForeground": c["blue"],
        "debugConsole.warningForeground": c["amber"],
        "debugConsole.errorForeground": c["ember"],
        "debugConsole.sourceForeground": c["soft"],
        "debugConsoleInputIcon.foreground": c["arc"],

        "testing.runAction": c["arc"],
        "testing.iconPassed": c["jade"],
        "testing.iconFailed": c["ember"],
        "testing.iconErrored": c["ember"],
        "testing.iconQueued": c["blue"],
        "testing.iconUnset": c["soft"],
        "testing.iconSkipped": c["subtle"],
        "testing.peekBorder": c["volt"],
        "testing.peekHeaderBackground": c["surface"],
        "testing.messagePeekBorder": c["volt"],
        "testing.messagePeekHeaderBackground": c["surface"],
        "testing.message.error.lineBackground": tint("ember", "tint"),
        "testing.message.info.lineBackground": tint("jade", "tint"),
        "testing.message.info.decorationForeground": c["jade"],
        "testing.coveredBackground": tint("jade", "tint"),
        "testing.coveredGutterBackground": tint("jade", "tint"),
        "testing.coveredBorder": NONE,
        "testing.uncoveredBackground": tint("ember", "tint"),
        "testing.uncoveredBranchBackground": tint("ember", "tint"),
        "testing.uncoveredGutterBackground": tint("ember", "tint"),
        "testing.uncoveredBorder": NONE,
        "testing.coverCountBadgeBackground": c["overlay"],
        "testing.coverCountBadgeForeground": c["arc"],

        "diffEditor.border": c["overlay"],
        "diffEditor.insertedTextBackground": tint("jade", "tint"),
        "diffEditor.removedTextBackground": tint("ember", "tint"),
        "diffEditor.insertedLineBackground": tint("jade", "wash"),
        "diffEditor.removedLineBackground": tint("ember", "wash"),
        "diffEditor.diagonalFill": c["overlay"],
        "diffEditor.unchangedRegionBackground": c["surface"],
        "diffEditor.unchangedRegionForeground": c["soft"],
        "diffEditorOverview.insertedForeground": tint("jade", "heavy"),
        "diffEditorOverview.removedForeground": tint("ember", "heavy"),

        "editor.background": c["deep"],
        "editor.foreground": c["text"],
        "editor.lineHighlightBackground": active_line,
        "editor.lineHighlightBorder": NONE,
        "editor.selectionBackground": tint("volt", "tint"),
        "editor.selectionHighlightBackground": tint("volt", "wash"),
        "editor.selectionHighlightBorder": NONE,
        "editor.inactiveSelectionBackground": tint("volt", "faint"),
        "editor.wordHighlightBackground": tint("volt", "tint"),
        "editor.wordHighlightStrongBackground": tint("volt", "veil"),
        "editor.findMatchBackground": tint("volt", "veil"),
        "editor.findMatchBorder": tint("volt", "heavy"),
        "editor.findMatchHighlightBackground": tint("volt", "tint"),
        "editor.findMatchHighlightBorder": NONE,
        "editor.findRangeHighlightBackground": tint("volt", "faint"),
        "editor.findRangeHighlightBorder": NONE,
        "editor.hoverHighlightBackground": tint("volt", "wash"),
        "editor.rangeHighlightBackground": tint("volt", "faint"),
        "editor.rangeHighlightBorder": NONE,
        "editor.foldBackground": tint("volt", "faint"),
        "editor.snippetTabstopHighlightBackground": tint("volt", "faint"),
        "editor.snippetFinalTabstopHighlightBorder": c["volt"],
        "editor.stackFrameHighlightBackground": tint("amber", "tint"),
        "editor.focusedStackFrameHighlightBackground": tint("jade", "tint"),
        "editor.linkedEditingBackground": tint("volt", "wash"),
        "editorPane.background": c["base"],

        "editorBracketMatch.background": tint("volt", "wash"),
        "editorBracketMatch.border": tint("volt", "heavy"),
        "editorCodeLens.foreground": c["dim"],
        "editorCursor.foreground": c["volt"],
        "editorCursor.background": c["deep"],
        "editorGhostText.foreground": c["dim"],
        "editorGroup.border": c["overlay"],
        "editorGroup.dropBackground": tint("volt", "tint"),
        "editorGroup.emptyBackground": c["base"],
        "editorGroupHeader.tabsBackground": c["base"],
        "editorGroupHeader.tabsBorder": c["overlay"],
        "editorGroupHeader.noTabsBackground": c["base"],
        "editorGutter.background": c["deep"],
        "editorGutter.addedBackground": c["jade"],
        "editorGutter.modifiedBackground": c["amber"],
        "editorGutter.deletedBackground": c["ember"],
        "editorGutter.foldingControlForeground": c["dim"],
        "editorGutter.commentRangeForeground": c["muted"],
        "editorGutter.commentGlyphForeground": c["arc"],
        "editorHoverWidget.background": c["surface"],
        "editorHoverWidget.foreground": c["text"],
        "editorHoverWidget.border": c["overlay"],
        "editorHoverWidget.highlightForeground": c["arc"],
        "editorIndentGuide.background1": c["overlay"],
        "editorIndentGuide.activeBackground1": c["muted"],
        "editorInlayHint.background": tint("overlay", "veil"),
        "editorInlayHint.foreground": c["subtle"],
        "editorInlayHint.typeBackground": tint("overlay", "veil"),
        "editorInlayHint.typeForeground": c["cyan"],
        "editorInlayHint.parameterBackground": tint("overlay", "veil"),
        "editorInlayHint.parameterForeground": c["soft"],
        "editorLineNumber.foreground": c["dim"],
        "editorLineNumber.activeForeground": c["volt"],
        "editorLink.activeForeground": c["arc"],
        "editorMarkerNavigation.background": c["surface"],
        "editorMarkerNavigationError.background": c["ember"],
        "editorMarkerNavigationWarning.background": c["amber"],
        "editorMarkerNavigationInfo.background": c["blue"],
        "editorRuler.foreground": c["muted"],
        "editorStickyScroll.background": c["base"],
        "editorStickyScrollHover.background": c["surface"],
        "editorSuggestWidget.background": c["surface"],
        "editorSuggestWidget.foreground": c["text"],
        "editorSuggestWidget.border": c["overlay"],
        "editorSuggestWidget.highlightForeground": c["arc"],
        "editorSuggestWidget.focusHighlightForeground": c["arc"],
        "editorSuggestWidget.selectedBackground": c["overlay"],
        "editorSuggestWidget.selectedForeground": c["text"],
        "editorSuggestWidget.selectedIconForeground": c["arc"],
        "editorWhitespace.foreground": c["muted"],
        "editorWidget.background": c["surface"],
        "editorWidget.foreground": c["text"],
        "editorWidget.border": c["overlay"],
        "editorWidget.resizeBorder": c["volt"],
        "editorLightBulb.foreground": c["amber"],
        "editorLightBulbAutoFix.foreground": c["jade"],

        "editorError.foreground": c["ember"],
        "editorError.border": NONE,
        "editorError.background": NONE,
        "editorWarning.foreground": c["amber"],
        "editorWarning.border": NONE,
        "editorWarning.background": NONE,
        "editorInfo.foreground": c["blue"],
        "editorInfo.border": NONE,
        "editorInfo.background": NONE,
        "editorHint.foreground": c["soft"],
        "editorHint.border": NONE,
        "problemsErrorIcon.foreground": c["ember"],
        "problemsWarningIcon.foreground": c["amber"],
        "problemsInfoIcon.foreground": c["blue"],

        "editorOverviewRuler.background": c["deep"],
        "editorOverviewRuler.border": c["overlay"],
        "editorOverviewRuler.findMatchForeground": tint("volt", "heavy"),
        "editorOverviewRuler.selectionHighlightForeground": tint("volt", "heavy"),
        "editorOverviewRuler.wordHighlightForeground": tint("volt", "heavy"),
        "editorOverviewRuler.wordHighlightStrongForeground": tint("volt", "heavy"),
        "editorOverviewRuler.rangeHighlightForeground": tint("volt", "heavy"),
        "editorOverviewRuler.bracketMatchForeground": tint("volt", "heavy"),
        "editorOverviewRuler.addedForeground": tint("jade", "heavy"),
        "editorOverviewRuler.modifiedForeground": tint("amber", "heavy"),
        "editorOverviewRuler.deletedForeground": tint("ember", "heavy"),
        "editorOverviewRuler.errorForeground": tint("ember", "heavy"),
        "editorOverviewRuler.warningForeground": tint("amber", "heavy"),
        "editorOverviewRuler.infoForeground": tint("blue", "heavy"),

        "extensionButton.prominentBackground": c["volt"],
        "extensionButton.prominentForeground": c["deep"],
        "extensionButton.prominentHoverBackground": c["arc"],
        "extensionButton.separator": c["overlay"],
        "extensionBadge.remoteBackground": c["blue"],
        "extensionBadge.remoteForeground": c["deep"],
        "extensionIcon.starForeground": c["amber"],
        "extensionIcon.verifiedForeground": c["jade"],
        "extensionIcon.preReleaseForeground": c["bronze"],
        "extensionIcon.sponsorForeground": c["violet"],

        "gitDecoration.addedResourceForeground": c["jade"],
        "gitDecoration.untrackedResourceForeground": c["jade"],
        "gitDecoration.modifiedResourceForeground": c["amber"],
        "gitDecoration.renamedResourceForeground": c["amber"],
        "gitDecoration.stageModifiedResourceForeground": c["amber"],
        "gitDecoration.deletedResourceForeground": c["ember"],
        "gitDecoration.stageDeletedResourceForeground": c["ember"],
        "gitDecoration.conflictingResourceForeground": c["violet"],
        "gitDecoration.ignoredResourceForeground": c["subtle"],
        "gitDecoration.submoduleResourceForeground": c["teal"],
        "scmGraph.historyItemRefColor": c["blue"],
        "scmGraph.historyItemBaseRefColor": c["teal"],
        "scmGraph.historyItemRemoteRefColor": c["violet"],

        "input.background": c["surface"],
        "input.foreground": c["text"],
        "input.border": c["overlay"],
        "input.placeholderForeground": c["dim"],
        "inputOption.activeBackground": tint("volt", "tint"),
        "inputOption.activeBorder": c["volt"],
        "inputOption.activeForeground": c["text"],
        "inputOption.hoverBackground": tint("volt", "wash"),
        "inputValidation.errorBackground": tint("ember", "tint"),
        "inputValidation.errorBorder": c["ember"],
        "inputValidation.errorForeground": c["text"],
        "inputValidation.warningBackground": tint("amber", "tint"),
        "inputValidation.warningBorder": c["amber"],
        "inputValidation.warningForeground": c["text"],
        "inputValidation.infoBackground": tint("blue", "tint"),
        "inputValidation.infoBorder": c["blue"],
        "inputValidation.infoForeground": c["text"],

        "keybindingLabel.background": c["overlay"],
        "keybindingLabel.foreground": c["text"],
        "keybindingLabel.border": c["muted"],
        "keybindingLabel.bottomBorder": c["muted"],
        "keybindingTable.headerBackground": c["surface"],
        "keybindingTable.rowsBackground": c["base"],

        "list.activeSelectionBackground": c["overlay"],
        "list.activeSelectionForeground": c["text"],
        "list.activeSelectionIconForeground": c["arc"],
        "list.inactiveSelectionBackground": c["surface"],
        "list.inactiveSelectionForeground": c["text"],
        "list.inactiveSelectionIconForeground": c["soft"],
        "list.hoverBackground": c["surface"],
        "list.hoverForeground": c["text"],
        "list.focusBackground": c["overlay"],
        "list.focusForeground": c["text"],
        "list.focusOutline": c["volt"],
        "list.highlightForeground": c["arc"],
        "list.focusHighlightForeground": c["arc"],
        "list.dropBackground": tint("volt", "tint"),
        "list.errorForeground": c["ember"],
        "list.warningForeground": c["amber"],
        "listFilterWidget.background": c["surface"],
        "listFilterWidget.outline": c["volt"],
        "listFilterWidget.noMatchesOutline": c["ember"],
        "listFilterWidget.shadow": tint("overlay", "heavy"),
        "tree.indentGuidesStroke": c["muted"],
        "tree.inactiveIndentGuidesStroke": c["overlay"],
        "tree.tableColumnsBorder": c["overlay"],
        "tree.tableOddRowsBackground": c["surface"],

        "menu.background": c["surface"],
        "menu.foreground": c["text"],
        "menu.border": c["overlay"],
        "menu.selectionBackground": c["overlay"],
        "menu.selectionForeground": c["text"],
        "menu.selectionBorder": NONE,
        "menu.separatorBackground": c["overlay"],
        "menubar.selectionBackground": c["overlay"],
        "menubar.selectionForeground": c["text"],
        "menubar.selectionBorder": NONE,

        "merge.border": c["overlay"],
        "merge.currentHeaderBackground": tint("jade", "veil"),
        "merge.currentContentBackground": tint("jade", "tint"),
        "merge.incomingHeaderBackground": tint("blue", "veil"),
        "merge.incomingContentBackground": tint("blue", "tint"),
        "merge.commonHeaderBackground": tint("violet", "veil"),
        "merge.commonContentBackground": tint("violet", "tint"),

        "minimap.findMatchHighlight": tint("volt", "heavy"),
        "minimap.selectionHighlight": tint("volt", "veil"),
        "minimap.selectionOccurrenceHighlight": tint("volt", "tint"),
        "minimap.errorHighlight": tint("ember", "heavy"),
        "minimap.warningHighlight": tint("amber", "heavy"),
        "minimap.infoHighlight": tint("blue", "heavy"),
        "minimapSlider.background": tint("volt", "faint"),
        "minimapSlider.hoverBackground": tint("volt", "wash"),
        "minimapSlider.activeBackground": tint("volt", "tint"),
        "minimapGutter.addedBackground": c["jade"],
        "minimapGutter.modifiedBackground": c["amber"],
        "minimapGutter.deletedBackground": c["ember"],

        "notificationCenter.border": c["overlay"],
        "notificationCenterHeader.background": c["surface"],
        "notificationCenterHeader.foreground": c["text"],
        "notificationToast.border": c["overlay"],
        "notifications.background": c["surface"],
        "notifications.foreground": c["text"],
        "notifications.border": c["overlay"],
        "notificationLink.foreground": c["blue"],
        "notificationsErrorIcon.foreground": c["ember"],
        "notificationsWarningIcon.foreground": c["amber"],
        "notificationsInfoIcon.foreground": c["blue"],

        "panel.background": c["base"],
        "panel.border": c["overlay"],
        "panel.dropBorder": c["volt"],
        "panelInput.border": c["overlay"],
        "panelSection.border": c["overlay"],
        "panelSection.dropBackground": tint("volt", "tint"),
        "panelSectionHeader.background": c["surface"],
        "panelSectionHeader.foreground": c["text"],
        "panelSectionHeader.border": c["overlay"],
        "panelTitle.activeBorder": c["volt"],
        "panelTitle.activeForeground": c["text"],
        "panelTitle.inactiveForeground": c["soft"],

        "peekView.border": c["volt"],
        "peekViewEditor.background": c["surface"],
        "peekViewEditorGutter.background": c["surface"],
        "peekViewEditor.matchHighlightBackground": tint("volt", "tint"),
        "peekViewEditor.matchHighlightBorder": NONE,
        "peekViewResult.background": c["base"],
        "peekViewResult.fileForeground": c["text"],
        "peekViewResult.lineForeground": c["soft"],
        "peekViewResult.matchHighlightBackground": tint("volt", "tint"),
        "peekViewResult.selectionBackground": c["overlay"],
        "peekViewResult.selectionForeground": c["text"],
        "peekViewTitle.background": c["surface"],
        "peekViewTitleLabel.foreground": c["text"],
        "peekViewTitleDescription.foreground": c["soft"],

        "pickerGroup.border": c["overlay"],
        "pickerGroup.foreground": c["arc"],
        "quickInput.background": c["surface"],
        "quickInput.foreground": c["text"],
        "quickInputTitle.background": c["overlay"],
        "quickInputList.focusBackground": c["overlay"],
        "quickInputList.focusForeground": c["text"],
        "quickInputList.focusIconForeground": c["arc"],

        "progressBar.background": c["volt"],

        "scrollbar.shadow": tint("overlay", "heavy"),
        "scrollbarSlider.background": tint("volt", "faint"),
        "scrollbarSlider.hoverBackground": tint("volt", "wash"),
        "scrollbarSlider.activeBackground": tint("volt", "tint"),

        "settings.headerForeground": c["text"],
        "settings.modifiedItemIndicator": c["volt"],
        "settings.focusedRowBackground": tint("volt", "faint"),
        "settings.focusedRowBorder": tint("volt", "tint"),
        "settings.rowHoverBackground": c["surface"],
        "settings.dropdownBackground": c["surface"],
        "settings.dropdownBorder": c["overlay"],
        "settings.dropdownListBorder": c["overlay"],
        "settings.textInputBackground": c["surface"],
        "settings.textInputBorder": c["overlay"],
        "settings.numberInputBackground": c["surface"],
        "settings.numberInputBorder": c["overlay"],
        "settings.checkboxBackground": c["surface"],
        "settings.checkboxBorder": c["overlay"],

        "sideBar.background": c["base"],
        "sideBar.foreground": c["text"],
        "sideBar.border": c["overlay"],
        "sideBar.dropBackground": tint("volt", "tint"),
        "sideBarTitle.foreground": c["text"],
        "sideBarSectionHeader.background": c["surface"],
        "sideBarSectionHeader.foreground": c["text"],
        "sideBarSectionHeader.border": c["overlay"],

        "statusBar.background": c["base"],
        "statusBar.foreground": c["soft"],
        "statusBar.border": c["overlay"],
        "statusBar.focusBorder": c["volt"],
        "statusBar.noFolderBackground": c["base"],
        "statusBar.noFolderForeground": c["soft"],
        "statusBar.noFolderBorder": c["overlay"],
        "statusBar.debuggingBackground": c["amber"],
        "statusBar.debuggingForeground": c["deep"],
        "statusBar.debuggingBorder": c["overlay"],
        "statusBarItem.activeBackground": tint("volt", "tint"),
        "statusBarItem.hoverBackground": tint("volt", "wash"),
        "statusBarItem.hoverForeground": c["text"],
        "statusBarItem.focusBorder": c["volt"],
        "statusBarItem.compactHoverBackground": c["muted"],
        "statusBarItem.prominentBackground": c["overlay"],
        "statusBarItem.prominentForeground": c["arc"],
        "statusBarItem.prominentHoverBackground": c["muted"],
        "statusBarItem.remoteBackground": c["blue"],
        "statusBarItem.remoteForeground": c["deep"],
        "statusBarItem.remoteHoverBackground": lift("blue"),
        "statusBarItem.remoteHoverForeground": c["deep"],
        "statusBarItem.errorBackground": c["ember"],
        "statusBarItem.errorForeground": c["deep"],
        "statusBarItem.errorHoverBackground": lift("ember"),
        "statusBarItem.errorHoverForeground": c["deep"],
        "statusBarItem.warningBackground": c["amber"],
        "statusBarItem.warningForeground": c["deep"],
        "statusBarItem.warningHoverBackground": lift("amber"),
        "statusBarItem.warningHoverForeground": c["deep"],

        "tab.activeBackground": c["surface"],
        "tab.activeForeground": c["text"],
        "tab.activeBorder": NONE,
        "tab.activeBorderTop": c["volt"],
        "tab.activeModifiedBorder": c["amber"],
        "tab.inactiveBackground": c["base"],
        "tab.inactiveForeground": c["soft"],
        "tab.inactiveModifiedBorder": tint("amber", "veil"),
        "tab.hoverBackground": c["surface"],
        "tab.hoverForeground": c["text"],
        "tab.hoverBorder": NONE,
        "tab.border": c["overlay"],
        "tab.lastPinnedBorder": c["overlay"],
        "tab.dragAndDropBorder": c["volt"],
        "tab.unfocusedActiveBackground": c["base"],
        "tab.unfocusedActiveForeground": c["soft"],
        "tab.unfocusedActiveBorder": NONE,
        "tab.unfocusedActiveBorderTop": tint("volt", "veil"),
        "tab.unfocusedInactiveBackground": c["base"],
        "tab.unfocusedInactiveForeground": c["dim"],
        "tab.unfocusedHoverBackground": c["surface"],
        "tab.unfocusedHoverForeground": c["text"],

        "terminal.background": c["base"],
        "terminal.foreground": c["text"],
        "terminal.border": c["overlay"],
        "terminal.dropBackground": tint("volt", "tint"),
        "terminal.selectionBackground": c["volt"],
        "terminal.selectionForeground": c["deep"],
        "terminal.inactiveSelectionBackground": tint("volt", "tint"),
        "terminal.findMatchBackground": tint("volt", "veil"),
        "terminal.findMatchBorder": tint("volt", "heavy"),
        "terminal.findMatchHighlightBackground": tint("volt", "tint"),
        "terminal.findMatchHighlightBorder": NONE,
        "terminal.tab.activeBorder": c["volt"],
        "terminalCursor.foreground": c["volt"],
        "terminalCursor.background": c["deep"],
        "terminalCommandDecoration.defaultBackground": c["muted"],
        "terminalCommandDecoration.successBackground": c["jade"],
        "terminalCommandDecoration.errorBackground": c["ember"],
        "terminalStickyScroll.background": c["base"],
        "terminalStickyScrollHover.background": c["surface"],

        "titleBar.activeBackground": c["base"],
        "titleBar.activeForeground": c["text"],
        "titleBar.inactiveBackground": c["base"],
        "titleBar.inactiveForeground": c["soft"],
        "titleBar.border": c["overlay"],

        "welcomePage.background": c["deep"],
        "welcomePage.tileBackground": c["surface"],
        "welcomePage.tileHoverBackground": c["overlay"],
        "welcomePage.tileBorder": c["overlay"],
        "welcomePage.progress.background": c["overlay"],
        "welcomePage.progress.foreground": c["volt"],
        "walkThrough.embeddedEditorBackground": c["surface"],
        "walkthrough.stepTitle.foreground": c["text"],

        "charts.foreground": c["text"],
        "charts.lines": c["soft"],
        "charts.red": c["ember"],
        "charts.orange": c["bronze"],
        "charts.yellow": c["amber"],
        "charts.green": c["jade"],
        "charts.blue": c["blue"],
        "charts.purple": c["violet"],
    }

    for slot, name in palette["flavours"][flavour]["ansi"].items():
        key = "".join(w.capitalize() for w in slot.split("_"))
        s[f"terminal.ansi{key}"] = c[name]

    for i, name in enumerate(RAINBOW, start=1):
        s[f"editorBracketHighlight.foreground{i}"] = c[name]
        s[f"editorBracketPairGuide.background{i}"] = tint(name, "wash")
        s[f"editorBracketPairGuide.activeBackground{i}"] = c[name]
    s["editorBracketHighlight.unexpectedBracket.foreground"] = c["ember"]

    for i, name in enumerate(SERIES, start=1):
        s[f"scmGraph.foreground{i}"] = c[name]

    for kind, name in SYMBOLS.items():
        s[f"symbolIcon.{kind}Foreground"] = c[name]

    return s


def token_colours(palette, flavour):
    c = {k: v["hex"] for k, v in palette["flavours"][flavour]["colours"].items()}
    rules = []
    for name, colour, font, scopes in SYNTAX:
        settings = {"foreground": c[colour]}
        if font:
            settings["fontStyle"] = font
        rules.append({"name": name, "scope": scopes, "settings": settings})
    return rules


def semantic_tokens(palette, flavour):
    c = {k: v["hex"] for k, v in palette["flavours"][flavour]["colours"].items()}
    out = {}
    for token, (colour, font) in SEMANTIC.items():
        out[token] = {"foreground": c[colour]}
        if font:
            out[token]["fontStyle"] = font
    return out


def theme(palette, flavour):
    data = palette["flavours"][flavour]
    return {
        "name": data["name"],
        "type": data["appearance"],
        "semanticHighlighting": True,
        "semanticTokenColors": semantic_tokens(palette, flavour),
        "colors": colours(palette, flavour),
        "tokenColors": token_colours(palette, flavour),
    }


def generate(palette):
    return {name: json.dumps(theme(palette, flavour), indent=2) + "\n"
            for flavour, name in OUTPUT.items()}


if __name__ == "__main__":
    palette = json.loads((ROOT / "palette.json").read_text())
    for name, content in generate(palette).items():
        (HERE / name).write_text(content)
        print(f"vscode/{name}")
