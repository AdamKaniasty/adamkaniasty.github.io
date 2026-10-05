---
layout: about
title: About
heading: Adam Kaniasty — Software Engineer
permalink: /
schema_type: ProfilePage
description: Adam Kaniasty is a software engineer at Google working on agent development, with experience in RAG, machine learning, Java backends and cloud infrastructure.
subtitle: Software engineering, AI agents and machine learning systems.
profile:
  align: right
  image: personal/me.jpg
  image_circular: false
  more_info: >
    <p>Warsaw, Poland</p>
    <p><a href="mailto:adam.kaniasty@gmail.com">Email Adam</a></p>
social: false
---

I am a **Software Engineer at {{ site.data.resume.work.first.name }}**, on the Agent Development Lifecycle team. My work spans AI agents, document retrieval, machine learning pipelines and backend applications.

I work with **Python, Java, React TypeScript and cloud infrastructure**, including Azure, GCP and Kubernetes. My projects range from knowledge graph-based RAG to reinforcement learning for autoscaling and medical imaging inference.

[GitHub](https://github.com/AdamKaniasty) · [LinkedIn](https://www.linkedin.com/in/adam-kaniasty/) · [Experience and CV]({{ '/cv/' | relative_url }})

<section aria-labelledby="selected-projects">
<h2 id="selected-projects">Selected projects</h2>
<ul class="selected-work">
{% assign selected_projects = site.projects | where: 'selected', true | sort: 'importance' %}
{% for project in selected_projects %}
<li><a href="{{ project.url | relative_url }}"><strong>{{ project.title }}</strong></a> — {{ project.description }}</li>
{% endfor %}
</ul>
<p><a href="{{ '/projects/' | relative_url }}">Explore all engineering projects</a></p>
</section>

<section aria-labelledby="about-adam">
<h2 id="about-adam">About Adam</h2>
<p>Previously, I built a Java and GraphQL workflow platform at Box, an agentic claims application at Capgemini, and medical imaging applications at MI².AI. As APPI's co-founder and CTO, I developed knowledge graph-based retrieval systems. At Nokia, I worked on reinforcement learning for Kubernetes pod autoscaling and configurable ML training pipelines.</p>
<p>I completed a bachelor's degree in Data Science at Warsaw University of Technology and am pursuing a master's degree in Data Science there. Outside engineering, I train tennis and martial arts.</p>
<p><a href="{{ '/cv/' | relative_url }}#work">Professional experience</a> · <a href="{{ '/cv/' | relative_url }}#education">Education</a> · <a href="{{ "/news/" | relative_url }}">Professional updates</a></p>
</section>

<section aria-labelledby="research-teaching">
<h2 id="research-teaching">Research and teaching</h2>
<p>I co-developed Mi-Crow with Hubert Kowalski for our engineering thesis and co-authored a 2025 publication on radiomic data transformation for radiologists. <a href="{{ '/publications/' | relative_url }}">Read the publication and related research</a>.</p>
<p>I have given talks on RAG, fine-tuning and embeddings, and mentored AI teams at BEST Hacking League. <a href="{{ '/talks/' | relative_url }}">Talks and mentoring</a>.</p>
</section>
