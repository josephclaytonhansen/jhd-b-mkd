---
title: "Intrepid Couch Co-Op Duel Devlogs #4"
date: 2026-09-16 20:36:06
slug: iccd-devlogs-4
publish: true
description: "Building my couch co-op battle game, day 4- splitscreen cameras"
featured_image: "images/iccd_day4_fig1.png"
tags: [game-development, insanity, csharp]
categories:
  - iccd-devlogs
---

# Intrepid Couch Co-Op Duel Devlogs #4

Building my couch co-op battle game, day 4- splitscreen cameras

<!-- more -->

_Song of the day:_

<iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/track/2alTBUhWXocEWJM64hs7Ip?utm_source=generator&si=d9d67f2a29974d07" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

Making a splitscreen setup in Unity is not difficult. Making a splitscreen setup where the border between screens is dynamic and constantly changing is, surprisingly, also not too bad. There's an added layer of complexity required, but in terms of time and effort, getting the [filler blocks in the right place](2026-09-14-iccd-devlogs-2.md) was at least five times more wretched.

Here's how it works:

- Two cameras both render the full screen, with culling layers and overlays as needed, to render textures

- A main camera sees a big quad in front of it, which has a material from a compute shader that combines the render textures

- A fourth camera renders universal overlays (for example, the divider)

Four cameras does have an impact on performance, I wouldn't do this in 3D, but in 2D, it's negligible- I dropped from 550 FPS to 520 FPS in testing.

On the C# sharp side, I'm sending a list of points to the compute shader on *Fixed*Update. I learned my lesson about that already.

Here's the compute shader:

```c
#pragma kernel CSMain

RWTexture2D<float> _Result;

StructuredBuffer<float2> _Points;

int  _PointCount;
int2 _MaskSize;
int2 _ScreenSize;

// Given a screen-space Y, walk the point list and return the divider X at that Y
float InterpolateDividerX(float screenY)
{
    float minY  =  1e9;
    float maxY  = -1e9;
    float2 lower = _Points[0];
    float2 upper = _Points[0];

    for (int i = 0; i < _PointCount; i++)
    {
        float2 p = _Points[i];
        if (p.y < minY) { minY = p.y; lower = p; }
        if (p.y > maxY) { maxY = p.y; upper = p; }
    }

    if (screenY <= minY) return lower.x;
    if (screenY >= maxY) return upper.x;

    float2 before = lower;
    float2 after  = upper;

    for (int j = 0; j < _PointCount; j++)
    {
        float2 p = _Points[j];
        if (p.y <= screenY && p.y > before.y) before = p;
        if (p.y >= screenY && p.y < after.y)  after  = p;
    }

    float span = after.y - before.y;
    if (abs(span) < 1e-5) return before.x;

    float t = (screenY - before.y) / span;
    return lerp(before.x, after.x, t);
}

[numthreads(8, 8, 1)]
void CSMain(uint3 id : SV_DispatchThreadID)
{
    if ((int)id.x >= _MaskSize.x || (int)id.y >= _MaskSize.y)
        return;

    float screenX = ((float)id.x / (float)(_MaskSize.x - 1)) * (float)_ScreenSize.x;
    float screenY = ((float)id.y / (float)(_MaskSize.y - 1)) * (float)_ScreenSize.y;

    float dividerX = InterpolateDividerX(screenY);

    _Result[id.xy] = screenX < dividerX ? 1.0 : 0.0;
}
```

The end result is a black and white mask between the two cameras:
![Dynamic split screen](images/iccd_day4_fig1.png)
