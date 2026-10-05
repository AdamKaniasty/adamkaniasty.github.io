---
layout: project
title: Reinforcement Learning for Kubernetes Autoscaling
slug: kubernetes-autoscaling
permalink: /projects/kubernetes-autoscaling/
description: Nokia engineering work on DDQN reinforcement learning, time-series prediction and configurable training pipelines for Kubernetes pod autoscaling.
importance: 4
selected: true
related_projects: [rl-doom, xlungs]
---

## What did the autoscaling work address?

At Nokia, I worked on models for Kubernetes pod autoscaling, including a DDQN reinforcement learning model, PyTorch deep learning models and tuned open-source time-series predictors. The work connected machine learning experiments with cluster infrastructure.

## My role

During my Nokia roles (2022–2025), I designed, created and deployed models, built configurable training pipelines, and configured CI/CD and lab deployments.

## Training and deployment architecture

Training pipelines and model registries ran in a remote GPU-powered lab. Jenkins pipelines supported CI/CD, while Helm charts configured deployments in OpenShift labs. The work involved both model development and the infrastructure needed to train and deploy those models.

## Technologies

Reinforcement learning, DDQN, Python, PyTorch, Kubernetes, Jenkins, Helm and OpenShift.

## Scope of available evidence

This description is based on my professional experience recorded in the CV. No public code, workload traces or comparative benchmark is linked, so I do not claim a quantified resource saving or advantage over other autoscalers.

## Links

- [Nokia experience in my CV]({{ '/cv/' | relative_url }}#work)
- [Public reinforcement learning experiments in VizDoom]({{ '/projects/rl-doom/' | relative_url }})
