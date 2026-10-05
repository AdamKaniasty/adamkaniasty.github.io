---
layout: page
title: xLungs
permalink: /projects/xlungs/
description: Java + React application for AI model inference and CT image analysis
importance: 3
category: work
related_publications: false
---

**xLungs** is a medical imaging research project from the MI².AI team at Warsaw University of Technology, focused on AI-assisted analysis of chest CT scans. The team developed **CTSegMate**, a model trained using approximately 40,000 CT studies, to support clinicians in analysing anatomical structures and disease-related changes.

I created the **Java + React fullstack application that performed inference for the model**, connecting the research system to a web interface for radiologists. My work covered a **Java Spring backend** and a **React TypeScript frontend**, supporting CT image processing, organ segmentation, and report generation.

The application coordinated a multistep inference pipeline using **RabbitMQ**. I deployed and tested it on a **GPU-powered Kubernetes cluster**, integrating model inference with the application's processing and reporting workflow.

Read more about the research and its clinical goals in [ITwiz's coverage of xLungs](https://itwiz.pl/xlungs-polscy-naukowcy-stworzyli-model-ai-ktory-moze-zrewolucjonizowac-diagnostyke-chorob-pluc/).
