---
title: "Intrepid Couch Co-Op Duel Devlogs #2"
date: 2026-09-14 20:36:06
slug: iccd-devlogs-2
publish: true
description: "Building a fun, dumb, split-screen battle game, day 2- fixing divider gaps"
featured_image: "images/iccd_day2_fig1.png"
tags: [game-development, insanity, csharp]
categories:
  - iccd-devlogs
---

# Intrepid Couch Co-Op Duel Devlogs #2

Building a fun, dumb, split-screen battle game, day 2- fixing divider gaps

<!-- more -->

_Song of the day:_

<iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/track/4JWgZ7yOhvASm9lRTkcrzC?utm_source=generator&si=d8fe21e93e85463b" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

## The Gaps
Yesterday, I left off with a predictable but annoying geometrical problem I thought I already knew how to solve- specifically, the density of divider blocks decreasing with increased space between blocks. There's an inverse linear relationship between "things moving farther apart" and "how far apart things are", which is exceedingly obvious and so doesn't warrant a figure.

For discussion's sake, let the unaltered space between two blocks be N. In an unperturbed divider, all blocks are N apart, but as the wall reacts to impacts, the space between any two blocks will never be N again unless the entire wall has fully returned to a neutral position. I think. Not that it impacts the game- call it a geometric brainteaser?

> [!note] 
> I'm the furthest thing from a mathematician, but despite my lack of savvy in this area, it seems simple enough to say that if two points are N apart, and they can only move on the _x_ axis, any movement by either block will change the distance between them. The only way the distance could stay constant is through circular motion or if both moved the same amount in time and space, which isn't possible with my setup. 


## Filling Them In
My plan, coming from a 3D modeling background, was adaptive subdivision: if the space between two blocks (N) increases by 3x (_3N_), add another block between them. Update the block to reflect the new neighbors, then recurse in both directions. 

![Adaptive Subdivision with Recursive Neighbor Assignments](images/iccd_day2_fig1.png)

While this works well enough for _adding_ filler blocks, it is of course also necessary to _remove_ them as needed to prevent both overlapping blocks when density shrinks and massive piles of garbage. I didn't want to remove filler bocks when their adjacent distance was exactly N, since it's unlikely that that will happen at all (see above); I settled for _1.5N_ as a value after messing around; I don't have a scientific reason for that number, it just felt good. 

My first test ran into two major problems:

1. Filler blocks didn't have anywhere near the right position, but clumped at one side, far from the center. Baffling! The math is simple enough- take neighbor A and neighbor B and average their position (A+B)/2. This is middle school-level geometry, and yet repeated failures had me seriously wondering if I needed remedial courses, an  idea that filled me with dread, as I prefer to keep as much distance between myself and middle school as possible. More on that in a moment. 

2. Creating and deleting essentially dozens of the same game object over and over again is sloppy. Technically less of a "problem" and more of a "I can do better than this" situation- a problem for my pride and peace of mind, if you will. 

### Why aren't the blocks in the right place? 
I spent more time than I'd like to admit puzzling over this. I was doing everything right, after all, look at this beautiful code:
```csharp
private void UpdateFillers()
        {
            int fillerIndex = 0;

            for (int i = 0; i < Blocks.Length - 1; i++)
            {
                Vector3 a = Blocks[i].transform.position;
                Vector3 b = Blocks[i + 1].transform.position;
                float gap = Vector3.Distance(a, b);

                int count = Mathf.Max(0, Mathf.FloorToInt(gap / YDistanceBetweenBlocks) - 1);

                for (int j = 0; j < count; j++)
                {
                    float t = (j + 1f) / (count + 1f);
                    Vector3 pos = Vector3.Lerp(a, b, t);

                    if (fillerIndex >= _fillers.Count)
                        _fillers.Add(SpawnFiller(_fillers.Count));

                    _fillers[fillerIndex].transform.position = pos;
                    _fillers[fillerIndex].SetActive(true);
                    fillerIndex++;
                }
            }

            for (int i = fillerIndex; i < _fillers.Count; i++)
                _fillers[i].SetActive(false);
        }
```
Simplicity itself- all I have to do is call UpdateFillers() from Update() and watch in hapless dismay as the filler blocks _are in the wrong place_.

If you've already figured out the problem, good job. You're faster than me, though I attribute temporary cognitive delays on my part to the toddler and 1-month-old. 

If you haven't, there's no reason you should have to sit around as long as I did thinking about it, especially since this isn't your code, so without further ado...

The divider block positions change based on _physics_ (collisions from projectiles).

Sadly, I'm the first game developer in my family line, so I didn't hear any faint, ghostly whispers from those who have passed on, guiding me from beyond, saying "FixedUpdate, you foooooool..." Rather, I think those guiding me from beyond were more interested in the concept of a computer generally and wouldn't know the difference between FixedUpdate and Update if it were to dance on their grave. 

_I_ know the difference. I haven't blamed the toddler and the 1-month-old yet in this paragraph, so they take the fall here. I did get there, eventually. 

### How to do handle things cleanly?

With a pool.

If I need more fillers than are in the pool, add to the pool. Otherwise, disable unneeded blocks and keep them in the pool, repositioning and reusing. Less allocation, less mess. That's it!