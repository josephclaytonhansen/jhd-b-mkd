---
title: "Markdown Extensions Reference"
date: 2026-03-20 14:00:00
slug: markdown-extensions-reference
publish: true
description: A reference for all the Markdown extensions configured in this project — admonitions, tabs, code blocks, footnotes, and more.
tags:
  - markdown
  - reference
categories:
  - reference
---

# Markdown Extensions Reference

A quick reference for all the Markdown extensions available in this project.

<!-- more -->

## Admonitions

Standard admonitions from the `admonition` extension:

!!! note "A note"
    Notes provide extra context without interrupting the flow.

!!! warning "Be careful"
    Warnings draw attention to potential issues.

!!! danger "Danger zone"
    Danger blocks highlight critical information.

!!! tip "Pro tip"
    Tips share useful shortcuts or best practices.

## Collapsible Details

Using `pymdownx.details`:

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

=== "Rust"
    ```rust
    fn greet(name: &str) -> String {
        format!("Hello, {}!", name)
    }
    ```

## Tables

| Extension | Package | Purpose |
|---|---|---|
| `admonition` | built-in | Note/warning/tip blocks |
| `captions` (plugin) | `mkdocs-caption` | Image figure captions |
| `link-marker` | `mkdocs-link-marker` | External link icons |
| `pymdownx.tabbed` | `pymdownx` | Tabbed code/content blocks |

## Footnotes

You can add footnotes[^1] inline throughout the text.

[^1]: This is the footnote content, rendered at the bottom of the page.

## Figure Captions

`mkdocs-caption` adds figure captions automatically — just add a caption line below an image:

![Placeholder image](https://via.placeholder.com/800x400?text=Example+Figure)

Figure: An example figure with a caption using the mkdocs-caption plugin.
