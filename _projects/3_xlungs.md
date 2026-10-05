---
layout: project
title: xLungs — Medical Imaging Inference Application
slug: xlungs
permalink: /projects/xlungs/
description: Java Spring and React application coordinating CT image processing, model inference and radiology reports through RabbitMQ on GPU-powered Kubernetes.
importance: 2
selected: true
related_projects: [kubernetes-autoscaling, mi-crow]
---

## What did the xLungs application do?

xLungs is a medical imaging research project from MI².AI at Warsaw University of Technology. I created the Java and React application that connected the model's inference pipeline to an interface for radiologists.

## My role

My work covered the Java Spring backend, React TypeScript frontend, inference integration, deployment and testing on a GPU-powered Kubernetes cluster during 2024–2025.

## Architecture and implementation

The application coordinated CT image processing, organ segmentation and report generation through a multistep RabbitMQ inference pipeline. The backend and frontend connected that processing workflow to the radiologist-facing application.

## Technologies

Java, Spring, React, TypeScript, RabbitMQ and Kubernetes with GPU infrastructure.

## Research evidence

I co-authored the ISD2025 poster _Radiomic Medical Data Transformation for Radiologists Support_. It describes image conversion, segmentation, feature extraction and report rendering. The paper reports 89.09% DICE across five organs and processing in under five and a half minutes. These are results of the published research system, rather than separate measurements of my web application.

## Links

- [Publication, authors and DOI]({{ '/publications/' | relative_url }}#radiomic-medical-data)
- [Primary publication record](https://aisel.aisnet.org/isd2014/proceedings2025/transformation/28/)
