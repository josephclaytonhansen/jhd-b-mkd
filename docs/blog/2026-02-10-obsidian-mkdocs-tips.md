---
title: Writing Better Docs with Obsidian and MkDocs
date: 2026-02-10 10:30:00
slug: writing-better-docs-obsidian-mkdocs
publish: true
description: Tips for using Obsidian's linking and tagging features to build a well-structured knowledge base that builds cleanly with MkDocs Publisher.
tags:
  - obsidian
  - workflow
  - markdown
categories:
  - guides
---

# Writing Better Docs with Obsidian and MkDocs

Obsidian and MkDocs make a surprisingly good pair. Obsidian gives you a rich local editing experience with backlinks, graph view, and templates — while MkDocs Publisher takes care of publishing it cleanly.

<!-- more -->

## WikiLinks

Instead of `[Page Title](../some/path/page.md)`, just write `[[Page Title]]`. Publisher resolves these at build time.

You can also alias them: `[[Actual Page Name|display text]]`.

## Callouts → Admonitions

Obsidian callouts use this syntax:

```
> [!note]
> This is a note callout.

> [!warning] Watch out!
> Collapsible callouts use `> [!warning]+` or `> [!warning]-`.
```

MkDocs Publisher converts these to standard admonitions automatically.

## Figure Captions

The `mkdocs-caption` plugin adds proper `<figure>` and `<figcaption>` elements. Just add a `Figure:` line immediately after an image:

```markdown
![A descriptive alt text](../assets/screenshot.png)

Figure: This is the figure caption.
```

## Frontmatter Checklist

Every blog post needs:

- `title` — displayed in navigation and page header
- `date` — format `YYYY-MM-DD HH:MM:SS` (must be unique per post)
- `slug` — clean URL segment
- `publish: true` — required to appear in the built site
- `description` — used for SEO and post teasers

> [!info] Default publish status
> Files default to `draft` (not published). Directories default to `published`. This is configured in `mkdocs.yml` under `pub-meta`.
