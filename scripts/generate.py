#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.tmTheme from the shared palette.

The scopes come from the Neovim plugin's old generator, which was based on the
tokyonight.nvim exporter.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import hashlib
import json
import plistlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]

# Editor colors -> palette role. These keep the roles of the old Neovim generator,
# so the colors do not change. Some differ from STYLE-GUIDE.md (selection is
# ui.bg_visual there); change them in a separate fix.
GLOBALS = {
    "background": "ui.bg_dim",
    "foreground": "ui.fg",
    "caret": "ui.fg_dim",
    "invisibles": "ui.bg_gutter",
    "lineHighlight": "ui.bg_search",
    "selection": "ui.bg_search",
    "selectionBorder": "ui.bg_m1",
    "gutterForeground": "ui.bg_gutter",
}

# Rule name -> (palette role, scopes).
RULES = {
    "Comment": ("syn.comment", ["comment", "markup.quote"]),
    "Constant": ("syn.constant", ["constant", "markup.bold", "markup.italic", "markup.raw.inline"]),
    "String": (
        "syn.string",
        [
            "string",
            "meta.structure.dictionary.value.json string.quoted.double.json",
            "source.yaml string.unquoted",
        ],
    ),
    "Number": ("syn.number", ["constant.numeric"]),
    "Boolean": ("syn.constant", ["constant.language.boolean"]),
    "Identifier": (
        "syn.identifier",
        [
            "variable",
            "support.type.property-name.yaml",
            "support.type.property-name.toml",
            "support.type.property-name.table.toml",
            "support.type.property-name.array.toml",
        ],
    ),
    "Keyword": ("syn.keyword", ["keyword", "storage"]),
    "Function": ("syn.fun", ["entity.name.function", "meta.link.inline.description"]),
    "Statement": ("syn.statement", ["keyword.control"]),
    "Type": ("syn.type", ["support.type", "entity.name.type"]),
    "Special": ("syn.special1", ["markup.underline.link.markdown", "markup.raw.code-fence"]),
    "Operator": (
        "syn.operator",
        [
            "keyword.operator",
            "markup.list",
            "punctuation.definition.string.begin.json",
            "punctuation.definition.string.end.json",
            "punctuation.support.type.property-name.toml",
        ],
    ),
    "Tag": ("syn.fun", ["entity.name.tag"]),
    "Attribute": ("syn.identifier", ["entity.other.attribute-name"]),
    "HtmlTag": (
        "syn.fun",
        ["entity.name.tag", "entity.name.tag.html", "meta.tag.js", "meta.tag.jsx", "entity.name.tag.jsx"],
    ),
    "HtmlAttribute": (
        "syn.identifier",
        ["entity.other.attribute-name", "entity.other.attribute-name.html", "variable.other.attribute.jsx"],
    ),
}


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}


def theme(variant, colors):
    settings = [{"settings": {k: colors[role] for k, role in GLOBALS.items()}}]
    settings += [
        {"name": name, "scope": ", ".join(scopes), "settings": {"foreground": colors[role]}}
        for name, (role, scopes) in RULES.items()
    ]
    return plistlib.dumps(
        {
            "name": f"Kanagawa {variant.capitalize()}",
            "uuid": hashlib.sha256(variant.encode()).hexdigest()[:36],
            "settings": settings,
            "colorSpaceName": "sRGB",
            "semanticClass": f"theme.kanagawa.{variant}",
        }
    )


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.tmTheme"
        out.parent.mkdir(exist_ok=True)
        out.write_bytes(theme(v, roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
