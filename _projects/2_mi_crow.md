---
layout: page
title: Mi-Crow
permalink: /projects/mi-crow/
description: Engineering thesis on mechanistic interpretability for large language models
importance: 2
category: work
github: https://github.com/mi-crow-team/Mi-Crow
related_publications: false
---

**Mi-Crow** is a Python library for investigating how large language models work internally. I developed it with Hubert Kowalski as part of my engineering thesis at the Faculty of Mathematics and Information Science, Warsaw University of Technology.

The project connects activation analysis, concept discovery, and model steering in a unified research workflow. Sparse autoencoders extract interpretable features from model activations, while activation hooks let researchers observe and modify model behavior.

Mi-Crow supports:

- A consistent interface for Hugging Face language models.
- Training sparse autoencoders, including TopK and L1 variants.
- Capturing and manipulating activations through detectors and controllers.
- Discovering learned concepts and using them to steer model outputs.
- Storing tensors and experiment metadata for large-scale research workflows.

The library uses **Python, PyTorch, Transformers, Accelerate, and Datasets**, with example notebooks and documentation for interpretability experiments.

The thesis was supervised by Vladimir Zaigrajew and Przemysław Biecek.

Explore the [GitHub repository](https://github.com/mi-crow-team/Mi-Crow) and [project documentation](https://mi-crow-team.github.io/Mi-Crow/).
