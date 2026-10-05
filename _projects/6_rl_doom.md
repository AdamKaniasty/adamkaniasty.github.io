---
layout: project
title: RL Doom — Reinforcement Learning in VizDoom
slug: rl-doom
permalink: /projects/rl-doom/
description: Team project comparing PPO and A2C agents in VizDoom, with image preprocessing, reward functions and TensorBoard evaluation.
importance: 6
github: https://github.com/AdamKaniasty/RL-Doom
programming_languages: [Python]
contributors: [Igor Kołodziej, Hubert Kowalski, Norbert Frydrysiak, Krzysztof Sawicki]
related_projects: [kubernetes-autoscaling]
---

## What did RL Doom investigate?

RL Doom trained and evaluated reinforcement learning agents in VizDoom scenarios using Proximal Policy Optimization (PPO) and Advantage Actor-Critic (A2C).

## My role

I led a five-person team for this Data Science research-workshops project. The repository identifies the team and contains its implementation and reports.

## Architecture and evaluation

Python modules separate game integration, models, reward functions, preprocessing and training. VizDoom connects to Gymnasium, with TensorBoard metrics for reward, ammunition use, episode length and kill count. Experiments covered Basic, Defend Center and Death Corridor scenarios.

## Reported findings

The repository reports that PPO trained more stably and efficiently than A2C, and that image-only CNN inputs worked better than combining images with scalar game state. These are qualitative findings from this project's experiments; no numerical comparison is reproduced here.

## Links

- [RL Doom source, methodology and reports](https://github.com/AdamKaniasty/RL-Doom)
