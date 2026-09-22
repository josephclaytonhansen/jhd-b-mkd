---
title: "Intrepid Couch Co-Op Duel Devlogs #1"
date: 2026-09-13 20:36:06
slug: iccd-devlogs-1
publish: true
description: "Building a fun, dumb, split-screen battle game, day 1- basic divider structure"
featured_image: "images/iccd_day1_fig2.png"
tags: [game-development, insanity, csharp]
categories:
  - iccd-devlogs
---

# Intrepid Couch Co-Op Duel Devlogs #1

Building a fun, dumb, split-screen battle game, day 1- basic divider structure

<!-- more -->

_Song of the day:_

<iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/track/6u0x5ad9ewHvs3z6u9Oe3c?utm_source=generator&si=2feb2dd4413a430b" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

One morning recently, I woke up with a strange idea. I may have been dreaming about it. With a toddler and a newborn, ish, tracing a train of thought to inception is a feat of immense proportions during the day, let alone when I'm waking up.

_Intrepid Couch Co-Op Duel: Endless Capital Glory_ is primarily intended to be a realization of that vision, as well as a learning exercise and way for me to improve my skills. It's also supposed to be fun. And, it's supposed to be fast- in direct opposition to the massive multi-year projects I'm working on, my goal is to have this ready for serious playtesting by the end of the year.

I'm not going to go into a ton of detail about the game here, rather focusing on what I'm learning and problems I'm solving, but here's the short version: two players push the split screen divider around with various over-the-top projectiles, some from personal weapons, some from powerful attacks purchased with earned resources. Crowd your opponent out of space to win.

## Day 1 - Starting with the divider

The split-screen divider is the most important part of this game, from a systems perspective. As I sat down to work on it today, I knew it needed to be dynamic, respond with high accuracy to collisions, and fast.

I decided to make a seemingly solid wall down the middle actually composed of equally spaced blocks. Blocks are aware of their neighbors; this way, falloff from impact can ripple out through the divider.

Blocks also need to return to center to add any degree of interest or difficulty to gameplay. A natural elastic behavior would make blocks snap back faster the further from center they are- I elected instead for snapback speed to decrease with distance. From a gameplay perspective, this means significant gains are harder to lose, but small bumps to the wall quickly become meaningless. Playtesting will tell, but I believe this incentives more interesting gameplay, prioritizing strategy over spamming.

This is the relevant code (excluding the falloff ripple, which is also straightforward):

```csharp
private void FixedUpdate()
        {
            if (Mathf.Abs(CurrentVelocity) > 0.0001f)
            {
                transform.position += new Vector3(CurrentVelocity * Time.deltaTime, 0f, 0f);
                var damping = DistanceFromCenter > 0 ? FriendlyDamping : EnemyDamping;
                CurrentVelocity = Mathf.Lerp(CurrentVelocity, 0f, Time.deltaTime * damping);
            }
            else
            {
                CurrentVelocity = 0f;
            }

            if (!PositionIsNearCenter)
            {
                SnapBack();
            }
        }

private void SnapBack()

        {
            float s = Mathf.Clamp01(Mathf.Abs(DistanceFromCenter)) * SnapBackSpeed;
            float snapBackDirection = DistanceFromCenter > 0 ? -1f : 1f;
            CurrentVelocity += s * snapBackDirection * Time.deltaTime;

        }
```

With a simple manager to control spawning all the blocks, so that blocks are only aware of themselves and what's happening to them (being self-centered is bad for humans but excellent for object oriented programming), I have exactly what I wanted:
![Divider wall](images/iccd_day1_fig1.png)

I also built a simple spawner that creates projectiles on click, just so there's something to interact with the colliders.

Of course, nothing is ever quite so simple as you plan it to be. I quickly realized that my divider strategy didn't work well as blocks moved away from each other, creating gaps that projectiles can move through:
![Oh no, that's a hole](images/iccd_day1_fig2.png)

That, however, is a tomorrow me problem. Right now my newborn-ish is a today me problem.
