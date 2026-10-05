---
layout: project
title: CanSat Terrain Image Classification
slug: cansat-terrain
permalink: /projects/cansat-terrain/
description: Python terrain-image processing for Project Trailblazer, with image tiling, a random forest baseline and a transferred ResNet18 classifier.
importance: 7
github: https://github.com/AdamKaniasty/Picture-Segmentation
programming_languages: [Python]
related_projects: [xlungs, rl-doom]
---

## What did the terrain project do?

The Project Trailblazer CanSat project processed images taken by a probe into terrain categories such as forest, grass and sand. The public repository calls it picture segmentation and describes image classification pipelines.

## My role

I developed the image-processing models as a member of the Project Trailblazer team. The repository lists me as the author.

## Implementation

Data preparation resized large images and divided them into 224 × 224 pixel tiles. One notebook trained a random forest classifier; another adapted a pretrained ResNet18 by replacing its final dense layer. Inference notebooks loaded images and saved weights to produce the output.

## Technologies and evidence

Python notebooks, NumPy, PIL and PyTorch. The repository includes model notebooks and example outputs.

## Links

- [CanSat source notebooks and example output](https://github.com/AdamKaniasty/Picture-Segmentation)
