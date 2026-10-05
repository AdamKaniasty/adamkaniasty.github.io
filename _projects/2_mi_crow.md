---
layout: project
title: Mi-Crow — Mechanistic Interpretability for LLMs
slug: mi-crow
permalink: /projects/mi-crow/
description: Python library connecting sparse autoencoder training, activation analysis, concept discovery and language-model steering.
importance: 1
selected: true
github: https://github.com/mi-crow-team/Mi-Crow
contributors: [Hubert Kowalski]
programming_languages: [Python]
related_projects: [rl-doom, appi-marketplace]
---

## What is Mi-Crow?

Mi-Crow is a Python library for mechanistic interpretability experiments on large language models. It connects activation analysis, concept discovery and model steering in a unified research workflow.

## My role

I co-developed Mi-Crow with Hubert Kowalski for our engineering thesis at Warsaw University of Technology. Vladimir Zaigrajew and Przemysław Biecek supervised the thesis.

## Architecture and implementation

A unified Hugging Face model interface connects to activation hooks. Detectors observe activations; controllers modify model behavior. Sparse autoencoders, including TopK and L1 variants, extract features for concept exploration and steering. Tensor storage and experiment metadata support the research workflow.

## Technologies

Python, PyTorch, Transformers, Accelerate and Datasets.

## Reproducing an experiment

The source repository and documentation include notebooks for training an autoencoder, collecting activating texts, and loading concepts. Use their current setup instructions and model requirements when reproducing an experiment.

## Links

- [Mi-Crow source code](https://github.com/mi-crow-team/Mi-Crow)
- [Mi-Crow documentation and examples](https://mi-crow-team.github.io/Mi-Crow/)
- [Research and thesis context]({{ '/publications/' | relative_url }})
