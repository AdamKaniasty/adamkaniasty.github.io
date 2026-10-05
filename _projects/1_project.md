---
layout: project
title: APPI Marketplace — Knowledge Graph RAG
slug: appi-marketplace
permalink: /projects/appi-marketplace/
description: AI agent platform for technical documents, with knowledge graph-based context retrieval, a FastAPI backend and Azure deployment.
importance: 3
selected: true
related_projects: [appi-synapse, mi-crow]
---

## What did APPI Marketplace do?

APPI Marketplace was an AI agent platform for technical and engineering documents. It aimed to answer questions using retrieved document context, with an emphasis on retaining relationships between pieces of technical information.

## My role

As APPI's co-founder and CTO (2023–2025), I designed and built the knowledge graph-based retrieval-augmented generation system and integrated it into the application.

## Retrieval architecture

The system parsed documents, retrieved relevant context and evaluated that context before passing it to AI agents. LlamaIndex and LangChain supported the document workflows; Pinecone provided vector storage. The application exposed a FastAPI backend deployed on Azure.

The central engineering concern was selecting useful, connected evidence from complex documentation. This portfolio records the implementation; no public retrieval benchmark is available here.

## Technologies

Python, FastAPI, LlamaIndex, LangChain, Pinecone and Azure.

## Links

- [APPI role in my CV]({{ '/cv/' | relative_url }}#work)
- [APPI Synapse information retrieval application]({{ '/projects/appi-synapse/' | relative_url }})
