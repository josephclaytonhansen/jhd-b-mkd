---
title: "Intrepid Couch Co-Op Duel Devlogs #6"
date: 2026-09-20 20:36:06
slug: iccd-devlogs-6
publish: true
description: "Building my couch co-op battle game, day 7- winning gauge"
featured_image: "images/iccd_day7_fig1.png"
tags: [game-development, insanity, csharp]
categories:
  - iccd-devlogs
---

# Intrepid Couch Co-Op Duel Devlogs #6- winning gauge

Building my couch co-op battle game, day 7- winning gauge

<!-- more -->

_Song of the day:_
<iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/track/0AAMnNeIc6CdnfNU85GwCH?utm_source=generator&si=066fc08135c84ac2" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

I'm skipping lightly over day 6- it was architectural grunt work, and since I've written about the major systems, I'm going to only write logs about things that are of particular interest (at least, to me) to avoid having thousands of these. Today was about a simple but very important component- the winning gauge. The players need to be able to see at a glance who is winning. Technically, you can see at a glance how far you've pushed the divider, but it's still nice to have something simpler to parse. I settled on a gauge:

![The gauge (without needle)](images/iccd_day7_fig1.png)

The advantage of this is that you don't have to guess when you're in serious trouble- if the needle goes into the red, you know you're about to lose, and you should probably use anything super powerful you've been holding onto immediately. 

Initially, I was only looking at how far the divider had been pushed, taking an average of the blocks' distance from center. This had an outlier problem. You can skew the average by focusing on just one section of the divider and pushing it very far. This would be annoying in actual gameplay, there would be no need to strategize. To make things more tactical and interesting, I decided to also consider the closest block to the center in the equation. This way, focusing solely on one area won't have as much of an impact as pushing all of the divider. It's still possible to skip parts of the divider and win, but if you were to just keep firing at one block over and over again, you would not be able to win. 


```csharp
public float WhoIsWinning
{
    get
    {
        float averageDistance = Blocks.Average(block => block.DistanceFromCenter);
        float minDistance = Blocks.Min(block => block.DistanceFromCenter);
        return ((2f * averageDistance) + minDistance) / 2f;
    }
}
```

Then, the gauge looks at that number and rotates the needle accordingly:

```csharp
public class WinningGauge : MonoBehaviour
{
    public Divider.Divider divider;
    public SpriteRenderer needleRenderer;

    void Update()
    {
        var w = divider.WhoIsWinning;
        var minRotation = Quaternion.Euler(0f, 0f, 90f);
        var maxRotation = Quaternion.Euler(0f, 0f, -90f);
        float minW = -5.65f;
        float maxW = 5.65f;
        needleRenderer.transform.rotation = Quaternion.Lerp(
            minRotation,
            maxRotation,
            (w - minW) / (maxW - minW)
        );
    }
}
```