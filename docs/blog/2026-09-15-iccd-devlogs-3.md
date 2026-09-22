---
title: "Intrepid Couch Co-Op Duel Devlogs #3"
date: 2026-09-15 20:36:06
slug: iccd-devlogs-3
publish: true
description: "Building a fun, dumb, split-screen battle game, day 3- rendering the divider as a smooth line"
featured_image:
tags: [game-development, insanity, csharp, catmull-rom]
categories:
  - iccd-devlogs
---

# Intrepid Couch Co-Op Duel Devlogs #3

Building a fun, dumb, split-screen battle game, day 3- rendering the divider as a smooth line

<!-- more -->

_Song of the day:_

<iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/track/0qWoOHqTirzo59FQ9eoECH?utm_source=generator&si=0094546d15b344bb" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

![The divider as a smooth rendered line](images/iccd_day3_fig1.png)
Today, I made this- a smooth continous line between divider blocks. It's done with a shader and a dynamic mesh. A snippet is worth at least a thousand words here, so I'll share some code rather than editorializing it. I'm doing as much as this project as possible myself, teaching myself things I don't know, using what I do know, and solving problems as they come up. In this case, I got some help from Claude for dynamic mesh handling, as I had no idea how to do that with Unity and I wasn't having much luck finding answers. 

The relevant code:

```csharp
void Rebuild()
{
    if (_mesh == null || _points.Count < 2)
    {
        _mesh?.Clear();
        return;
    }

    List<Vector2> smooth =
        smoothingSteps > 0
            ? CatmullRomChain(_points, smoothingSteps, tension)
            : new List<Vector2>(_points);

    BuildMesh(smooth);
}

void BuildMesh(List<Vector2> pts)
{
    // Disclosure: I had help from Claude for this
    int n = pts.Count;
    if (n < 2)
        return;

    // Two vertices per point (top / bottom of the line ribbon).
    var vertices = new Vector3[n * 2];
    var uvs = new Vector2[n * 2];
    var colors = new Color32[n * 2];
    var triangles = new int[(n - 1) * 6];

    Color32 c32 = color;
    float half = thickness * 0.5f;

    for (int i = 0; i < n; i++)
    {
        // Direction at this point (forward along the line).
        Vector2 dir;
        if (i == 0)
            dir = (pts[1] - pts[0]).normalized;
        else if (i == n - 1)
            dir = (pts[n - 1] - pts[n - 2]).normalized;
        else
            dir = (pts[i + 1] - pts[i - 1]).normalized;

        // Perpendicular (normal across the width).
        Vector2 perp = new Vector2(-dir.y, dir.x) * half;

        float t = n > 1 ? (float)i / (n - 1) : 0f;

        // Top edge
        vertices[i * 2] = (Vector3)(pts[i] + perp);
        uvs[i * 2] = new Vector2(t, 0f);
        colors[i * 2] = c32;

        // Bottom edge
        vertices[i * 2 + 1] = (Vector3)(pts[i] - perp);
        uvs[i * 2 + 1] = new Vector2(t, 1f);
        colors[i * 2 + 1] = c32;
    }

    // Build triangle indices (two tris per quad segment).
    for (int i = 0; i < n - 1; i++)
    {
        int bi = i * 6;
        int vi = i * 2;
        // First tri
        triangles[bi] = vi;
        triangles[bi + 1] = vi + 2;
        triangles[bi + 2] = vi + 1;
        // Second tri
        triangles[bi + 3] = vi + 1;
        triangles[bi + 4] = vi + 2;
        triangles[bi + 5] = vi + 3;
    }

    _mesh.Clear();
    _mesh.SetVertices(vertices);
    _mesh.SetUVs(0, uvs);
    _mesh.SetColors(colors);
    _mesh.SetTriangles(triangles, 0);
    _mesh.RecalculateBounds();
}

static List<Vector2> CatmullRomChain(List<Vector2> pts, int steps, float alpha)
{
    var result = new List<Vector2>(pts.Count * steps);

    for (int i = 0; i < pts.Count - 1; i++)
    {
        Vector2 p0 = pts[Mathf.Max(i - 1, 0)];
        Vector2 p1 = pts[i];
        Vector2 p2 = pts[i + 1];
        Vector2 p3 = pts[Mathf.Min(i + 2, pts.Count - 1)];

        for (int s = 0; s <= steps; s++)
        {
            if (s == 0 && i > 0)
                continue;

            float t = (float)s / steps;
            result.Add(CatmullRom(p0, p1, p2, p3, t, alpha));
        }
    }

    return result;
}

static Vector2 CatmullRom(
    Vector2 p0,
    Vector2 p1,
    Vector2 p2,
    Vector2 p3,
    float t,
    float alpha
)
{
    float t2 = t * t;
    float t3 = t2 * t;

    Vector2 m1 = (p2 - p0) * alpha;
    Vector2 m2 = (p3 - p1) * alpha;

    return (2f * t3 - 3f * t2 + 1f) * p1
        + (t3 - 2f * t2 + t) * m1
        + (-2f * t3 + 3f * t2) * p2
        + (t3 - t2) * m2;
}
```

One thing of note with Catmull-Rom splines- they don't extend to the boundaries of the point set. That is to say, a Catmull-Rom spline will have gaps at the beginning and end as a result of the smoothing. I could compensate for this with fancy calculations, but instead, I fill the vertical screen space with divider blocks, then add ten more. It's not fancy at all- it's a McDonald's fries alongside the Catmull-Rom, which is at least Olive Garden caliber- but it gets the job done. 