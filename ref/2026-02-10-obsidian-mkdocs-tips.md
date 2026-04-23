---
title: Writing Better Docs with Obsidian and MkDocs
date: 2026-02-10 10:30:00
slug: writing-better-docs-obsidian-mkdocs
publish: false
description: Tips for using Obsidian features that work seamlessly with MkDocs Publisher.
tags:
  - obsidian
  - workflow
  - markdown
categories:
  - guides
---

# Writing Better Docs with Obsidian and MkDocs

Obsidian and MkDocs make a good pair. Obsidian gives you a rich local editing
experience; MkDocs Publisher handles the publishing.

<!-- more -->

## WikiLinks

Instead of writing full relative paths, use Obsidian's double-bracket wikilink syntax.
Publisher resolves these to the correct page URL at build time.
You can also add a pipe character followed by display text to alias the link.

## Callouts

Obsidian callouts are automatically converted to MkDocs admonitions:

```markdown
> [!warning] Watch out
> This becomes a warning admonition.
```

## Figure Captions

The `mkdocs-caption` plugin turns images into proper HTML `<figure>` elements.
Add a line starting with `Figure:` immediately after any image line,
and it will be wrapped in `<figcaption>` tags automatically.

## Frontmatter Checklist

Every blog post needs:

- `title` - displayed in navigation and page header
- `date` - format `YYYY-MM-DD HH:MM:SS` (must be unique per post)
- `slug` - clean URL segment
- `publish: true` - required to appear in the built site

> [!info] Default publish status
> Files default to draft (not published). Set `publish: true` to include them.
