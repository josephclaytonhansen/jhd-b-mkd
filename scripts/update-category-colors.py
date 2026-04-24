#!/usr/bin/env python3
"""
Update category-colors.json with any new categories found in blog posts.

Usage:
    python scripts/update-category-colors.py

Existing colors are preserved. New categories get colors from a default
palette (cycling through if there are more categories than palette entries).
"""

import json
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
BLOG_DIR = DOCS / "blog"
COLORS_FILE = DOCS / "category-colors.json"

# Default color palette — add more if needed
DEFAULT_PALETTE = [
    "#7c3aed",  # violet
    "#2563eb",  # blue
    "#059669",  # emerald
    "#d97706",  # amber
    "#dc2626",  # red
    "#0891b2",  # cyan
    "#7c3aed",  # violet (cycles)
    "#db2777",  # pink
    "#65a30d",  # lime
    "#9333ea",  # purple
]


def gather_categories() -> set[str]:
    """Collect all unique category names from blog post frontmatter."""
    found: set[str] = set()
    if not BLOG_DIR.exists():
        return found

    for md_file in sorted(BLOG_DIR.glob("*.md")):
        if md_file.name.upper() == "README.MD":
            continue
        text = md_file.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        try:
            end_idx = text.index("---", 3)
            front = yaml.safe_load(text[3:end_idx])
            if not front:
                continue
            cats = front.get("categories") or []
            found.update(str(c) for c in cats)
        except Exception as exc:
            print(f"  Warning: could not parse {md_file.name}: {exc}", file=sys.stderr)

    return found


def main():
    # Load existing colors
    existing: dict[str, str] = {}
    if COLORS_FILE.exists():
        existing = json.loads(COLORS_FILE.read_text(encoding="utf-8"))

    all_categories = gather_categories()
    new_categories = sorted(all_categories - set(existing.keys()))

    if not new_categories:
        print("No new categories found. Nothing to update.")
        return

    # Assign colors to new categories from the palette
    used_colors = set(existing.values())
    available = [c for c in DEFAULT_PALETTE if c not in used_colors]
    if not available:
        available = DEFAULT_PALETTE  # cycle if all used

    updated = dict(existing)
    for i, cat in enumerate(new_categories):
        color = available[i % len(available)]
        updated[cat] = color
        print(f"  Added: {cat!r} -> {color}")

    COLORS_FILE.write_text(
        json.dumps(updated, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nSaved {COLORS_FILE.relative_to(ROOT)}")
    print(
        "\nEdit docs/category-colors.json to change any color, "
        "then rebuild with: .venv/Scripts/mkdocs build"
    )


if __name__ == "__main__":
    main()
