---
layout: page
title: Projects
permalink: /projects/
nav: true
nav_order: 3
schema_type: CollectionPage
description: Engineering projects by Adam Kaniasty covering mechanistic interpretability, RAG, medical imaging and reinforcement learning, with architecture and evidence links.
---

These case studies describe my role, the systems I worked on, and the available source code or research. They include open-source projects, university work and professional applications.

<div class="projects row row-cols-1 row-cols-md-2">
{% assign sorted_projects = site.projects | sort: 'importance' %}
{% for project in sorted_projects %}
  {% include projects.liquid %}
{% endfor %}
</div>

[Research and publications]({{ '/publications/' | relative_url }}) · [Professional experience]({{ '/cv/' | relative_url }})
