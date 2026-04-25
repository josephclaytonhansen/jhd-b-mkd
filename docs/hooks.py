"""
MkDocs hooks for Joseph Hansen's blog.

Handles:
- Category color bars on blog list pages (index, archive, category, tag pages)
- Featured images on list pages (half-width) and post pages (full-width banner)
- Clickable tag badges on individual post pages
"""

import json
import re
import yaml
from datetime import datetime
from pathlib import Path

_category_colors: dict[str, str] = {}
_slug_categories: dict[str, list[str]] = {}   # url-slug -> [categories]
_slug_featured: dict[str, str] = {}            # url-slug -> image path/url

_DEFAULT_COLOR = "#94a3b8"

_ORDINAL_SUFFIXES = {1: "st", 2: "nd", 3: "rd"}


def _ordinal(day: int) -> str:
    if 11 <= day <= 13:
        return "th"
    return _ORDINAL_SUFFIXES.get(day % 10, "th")


def _format_date(raw: str) -> str:
    """Turn '2026-04-23 14:41:00' into 'April 23rd, 2026'."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(raw.strip(), fmt)
            suffix = _ordinal(dt.day)
            return f"{dt.strftime('%B')} {dt.day}{suffix}, {dt.year}"
        except ValueError:
            pass
    return raw  # fallback: return as-is


_DATE_PATTERN = re.compile(
    r'<p class="post-date">([^<]+)</p>'
)


def on_pre_build(config):
    """Scan blog posts and load config before the build starts."""
    global _category_colors, _slug_categories, _slug_featured

    docs_dir = Path(config["docs_dir"])

    # Load category → color mapping
    colors_file = docs_dir / "category-colors.json"
    if colors_file.exists():
        _category_colors = json.loads(colors_file.read_text(encoding="utf-8"))

    # Scan all blog markdown files for frontmatter
    _slug_categories = {}
    _slug_featured = {}
    blog_dir = docs_dir / "blog"
    if not blog_dir.exists():
        return

    for md_file in sorted(blog_dir.glob("*.md")):
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
            slug = str(front.get("slug", md_file.stem))
            cats = front.get("categories") or []
            if cats:
                _slug_categories[slug] = [str(c) for c in cats]
            fi = front.get("featured_image")
            if fi:
                _slug_featured[slug] = str(fi)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# List page: wrap each post card with a category bar + optional featured image
# ---------------------------------------------------------------------------

_CARD_PATTERN = re.compile(
    # Capture the slug from the first href inside the <h2>
    r'<h2 id="[^"]+"><a href="[^"]*?/blog/([^/"]+)/"[^>]*>.*?'
    r'<div class="post-link">.*?</div>',
    re.DOTALL,
)


def _process_list_page(html: str) -> str:
    def replace_card(m: re.Match) -> str:
        slug = m.group(1)
        original = m.group(0)

        cats = _slug_categories.get(slug, [])
        primary = cats[0] if cats else ""
        color = _category_colors.get(primary, _DEFAULT_COLOR) if primary else _DEFAULT_COLOR
        cat_url = f"/blog/categories/{primary}/" if primary else "#"

        # Thin clickable bar on the left edge
        bar = (
            f'<a class="post-category-bar"'
            f' href="{cat_url}"'
            f' style="background-color:{color}"'
            f' title="{primary}"'
            f' aria-label="Category: {primary}"></a>'
        )

        featured = _slug_featured.get(slug, "")
        if featured:
            img_div = (
                f'<div class="post-card-image">'
                f'<img src="{featured}" alt="Featured image" loading="lazy">'
                f"</div>"
            )
            text_div = f'<div class="post-card-text">{original}</div>'
            body = f'<div class="post-card-body">{img_div}{text_div}</div>'
        else:
            body = f'<div class="post-card-body"><div class="post-card-text">{original}</div></div>'

        return f'<div class="post-card" data-category="{primary}">{bar}{body}</div>'

    html = _CARD_PATTERN.sub(replace_card, html)
    # Format all dates on the list page
    html = _DATE_PATTERN.sub(
        lambda m: f'<p class="post-date">{_format_date(m.group(1))}</p>',
        html,
    )
    return html


# ---------------------------------------------------------------------------
# Post page: inject tags bar and featured image banner
# ---------------------------------------------------------------------------

def _process_post_page(html: str, page) -> str:
    injected = ""

    # Featured image banner (full-width, above everything)
    featured = page.meta.get("featured_image", "")
    if featured:
        injected += (
            f'<div class="featured-image-banner">'
            f'<img src="{featured}" alt="Featured image">'
            f"</div>"
        )

    # Clickable tag badges
    tags = page.meta.get("tags") or []
    if tags:
        tag_links = "".join(
            f'<a class="post-tag-link" href="/blog/tags/{tag}/">{tag}</a>'
            for tag in tags
        )
        injected += f'<div class="post-tags-bar">{tag_links}</div>'

    if injected:
        html = injected + html

    return html


def _inject_cusdis(html: str, page, cusdis_cfg: dict) -> str:
    """Append Cusdis comment widget to the bottom of a post page."""
    host = cusdis_cfg.get("host", "https://cusdis.com").rstrip("/")
    app_id = cusdis_cfg.get("app_id", "")
    lang = cusdis_cfg.get("lang", "en")
    if not app_id:
        return html

    page_id = page.abs_url or page.url or ""
    page_url = page.canonical_url or page_id
    page_title = page.title or ""

    widget = (
        f'<div class="cusdis-comments">'
        f'<div id="cusdis_thread"'
        f' data-host="{host}"'
        f' data-app-id="{app_id}"'
        f' data-page-id="{page_id}"'
        f' data-page-url="{page_url}"'
        f' data-page-title="{page_title}">'
        f"</div>"
        f'<script async defer src="{host}/js/widget/lang/{lang}.js"></script>'
        f"</div>"
    )
    return html + widget


# ---------------------------------------------------------------------------
# Strip external-link icon from same-domain links
# (link-marker plugin treats all http URLs as external, including our own)
# ---------------------------------------------------------------------------

_EXTERNAL_ICON_PATTERN = re.compile(
    r'(&nbsp;|\u00a0)\u29c9'  # &nbsp;⧉  (the link-marker icon)
)


def _strip_internal_icons(html: str, site_url: str) -> str:
    """Remove the ⧉ icon from links that point to the same domain as site_url."""
    # Normalise: ensure trailing slash, strip scheme for comparison
    own_domain = re.sub(r'^https?://', '', site_url.rstrip('/').lower())

    def _clean(m: re.Match) -> str:
        href = m.group(1).lower()
        href_bare = re.sub(r'^https?://', '', href)
        if href_bare.startswith(own_domain):
            # Remove the trailing &nbsp;⧉ that link-marker appended
            content = _EXTERNAL_ICON_PATTERN.sub('', m.group(2))
            return f'<a href="{m.group(1)}">{content}</a>'
        return m.group(0)

    return re.sub(
        r'<a href="(https?://[^"]+)">(.+?)</a>',
        _clean,
        html,
        flags=re.DOTALL,
    )


# ---------------------------------------------------------------------------
# MkDocs hook entry point
# ---------------------------------------------------------------------------

def on_page_content(html, page, config, files):
    is_list_page = "post-extra" in html
    # A post page has a date in meta and is not a list page
    is_post_page = bool(page.meta.get("date")) and not is_list_page

    if is_list_page:
        html = _process_list_page(html)

    if is_post_page:
        html = _process_post_page(html, page)
        cusdis_cfg = config.get("extra", {}).get("cusdis", {})
        if cusdis_cfg:
            html = _inject_cusdis(html, page, cusdis_cfg)

    site_url = config.get("site_url", "")
    if site_url:
        html = _strip_internal_icons(html, site_url)

    return html
