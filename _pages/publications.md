---
layout: page
permalink: /publications/
title: Research & Publications
nav: true
nav_title: Research
nav_order: 2
schema_type: CollectionPage
research_index: true
description: Adam Kaniasty's research includes a 2025 radiomic medical data publication and Mi-Crow, an engineering thesis on mechanistic interpretability of language models.
---

My research-related work includes medical imaging software and tooling for interpreting language models.

{% for paper in site.data.research %}

<section aria-labelledby="radiomic-medical-data">
<h2 id="radiomic-medical-data">{{ paper.title }}</h2>
<p>{{ paper.authors | join: ', ' }}.</p>
<p><strong>{{ paper.venue }}</strong>, {{ paper.year }}. {{ paper.type }}.</p>
<p>The research presents a CT processing pipeline that converts images, segments organs, extracts features and renders reports for radiologists. I co-authored the paper; my application engineering role is described in the xLungs case study.</p>
<p><a href="{{ paper.doi_url }}">DOI: {{ paper.doi }}</a> · <a href="{{ paper.url }}">Publication record and paper</a> · <a href="{{ paper.project_url | relative_url }}">xLungs application architecture and my role</a></p>
</section>
{% endfor %}

## Engineering thesis: Mi-Crow

I co-developed Mi-Crow with Hubert Kowalski at Warsaw University of Technology, supervised by Vladimir Zaigrajew and Przemysław Biecek. It provides Python tools for activation analysis, sparse autoencoder training and concept-based model steering.

[Mi-Crow project and technical details]({{ '/projects/mi-crow/' | relative_url }}) · [Source and thesis context](https://github.com/mi-crow-team/Mi-Crow)
