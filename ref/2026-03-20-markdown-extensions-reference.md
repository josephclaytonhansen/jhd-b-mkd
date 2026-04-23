---
title: Markdown Extensions Reference
date: 2026-03-20 14:00:00
slug: markdown-extensions-reference
publish: false
description: A reference for all Markdown extensions configured in this project.
tags:
  - markdown
  - reference
categories:
  - reference
---

# Markdown Extensions Reference

A quick reference for all Markdown extensions available in this project.

<!-- more -->

## Admonitions

!!! note "A note"
    Notes provide extra context without interrupting flow.

!!! warning "Be careful"
    Warnings draw attention to potential issues.

!!! tip "Pro tip"
    Tips share useful shortcuts or best practices.

## Collapsible Details

??? note "Click to expand"
    This content is hidden until the user expands it.

## Tabbed Content

=== "Python"
    ```python
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    ```

=== "TypeScript"
    ```typescript
    function greet(name: string): string {
        return `Hello, ${name}!`;
    }
    ```

## Tables

| Extension | Package | Purpose |
|---|---|---|
| `admonition` | built-in | Note/warning/tip blocks |
| `caption` (plugin) | `mkdocs-caption` | Image figure captions |
| `link-marker` | `mkdocs-link-marker` | External link icons |
| `pymdownx.tabbed` | `pymdownx` | Tabbed code/content blocks |

## Footnotes

You can add footnotes[^1] inline throughout the text.

[^1]: This is the footnote content, rendered at the bottom of the page.
