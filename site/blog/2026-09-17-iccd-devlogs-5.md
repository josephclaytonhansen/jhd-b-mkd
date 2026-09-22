---
title: "Intrepid Couch Co-Op Duel Devlogs #5"
date: 2026-09-17 20:36:06
slug: iccd-devlogs-5
publish: true
description: "Building my couch co-op battle game, day 5- port simplified brain"
featured_image: "images/iccd_day5_fig1.png"
tags: [game-development, insanity, csharp, noodles]
categories:
  - iccd-devlogs
---

# Intrepid Couch Co-Op Duel Devlogs #5 - port simplified brain

Building my couch co-op battle game, day 5- port simplified brain

<!-- more -->

_Song of the day:_

<iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/track/4jqRdSypASxBTvuAs4g7KI?utm_source=generator&si=b7e35a6acbe0412f" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>

## Abstract architecture
For my projects, I have, after a lot of thought and experimentation, created a reusable system that handles all the connections between different areas. It's a variation of the Observer Pattern. I call it the Brain Pattern, or sometimes the Farfalle Pattern, because it looks like a farfalle noodle:
![yummy systems noodles](images/iccd_day5_fig1.png)

It's not dissimilar to the signal system in Godot, except instead of anything being able to connect to anything, which makes the bad kind of noodles (spaghetti), everything connects to one Brain. The Brain stores references to everything else, so nothing needs to know about anything except itself and the brain. 

Every brain event, or signal, looks like this:
```csharp
public event Action<BrainState> OnPaused;
public void PublishPaused(BrainState prev) => OnPaused?.Invoke(prev);
```

The brain itself is static, so nothing needs a reference to the brain except a BrainLoader- more on that in a moment- rather, everything looks like this:

```csharp
// Let's say this is a UI component that needs to know when the game is paused
void SubscribeToBrainEvents() => Brain.OnPaused += HandlePaused();

void HandlePaused() => DoSomethingWithTheUI();

void UnsubscribeFromBrainEvents() => Brain.OnPaused -=HandlePaused();
```

Then, the game state manager- which is actually a "brain component", a mini brain inside the larger brain (it's a noodles all the way down situtation)- would fire `PublishPaused()` as needed, and the UI would automatically react. 

## BrainLoader
Because I need a constantly alive, functioning brain- in my code as well- my preference is to put the Brain in its own scene, then load that scene into every other scene. I make the Brain a singleton, so there's one source of truth at all times, and this works perfectly. For a smallish project like this, it's probably overkill, but for larger projects, it's an absolute lifesaver. 

```csharp
using Fundamentals.Utilities;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Fundamentals.Brain
{
    public class BrainLoader : MonoBehaviour
    {
        private const string BrainSceneName = "Brain";
        private static bool _brainSceneLoaded = false;

        public Brain BrainInstance { get; private set; }

        private void Start()
        {
            if (!_brainSceneLoaded)
            {
                var result = LoadBrainScene();
                if (result.Success)
                {
                    _brainSceneLoaded = true;
                }
                else
                {
                    "BrainLoader: Failed to load Brain scene. Error: {result.ErrorMessage}".LogError();
                }
            }
        }

        public OperationResult LoadBrainScene()
        {
            try
            {
                var existing = SceneManager.GetSceneByName(BrainSceneName);
                if (existing.IsValid() && existing.isLoaded)
                {
                    BrainInstance = FindFirstObjectByType<Brain>();
                    return OperationResult.Successful();
                }

                SceneManager.LoadScene(BrainSceneName, LoadSceneMode.Additive);
                "BrainLoader: Brain scene loaded successfully.".LogInfo();
                BrainInstance = FindFirstObjectByType<Brain>();
                return OperationResult.Successful();
            }
            catch (System.Exception e)
            {
                var error = $"Failed to load brain scene '{BrainSceneName}': {e.Message}";
                error.LogError();
                return OperationResult.Failure(error);
            }
        }
    }
}
```
