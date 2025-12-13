---
layout: default
title: Handbook — Index
---

# Welcome to My Technical Handbook

<p class="intro">Hi! I'm Rilov Paloly Kulankara, and this is where I share everything I'm learning in the world of technology. As a software engineering leader, I'm constantly exploring new concepts in data engineering, cloud architecture, security, and scalability. This handbook is my way of documenting these learnings in simple, beginner-friendly guides with diagrams and real-world examples. Whether you're a seasoned engineer or just starting out, I hope you find these notes helpful on your own learning journey!</p>

<div class="search-bar">
  <input id="topic-search" placeholder="Search topics, tags, or categories..." />
</div>

<div class="main-grid">
  <nav class="categories" aria-label="Categories">
  <h3>Categories</h3>
  <ul>
    {% assign grouped = site.topics | group_by: "category" | sort: "name" %}
    {% for cat in grouped %}
      {% assign cat_slug = cat.name | slugify %}
      <li><a href="{{ '/categories/' | append: cat_slug | relative_url }}">{{ cat.name }} ({{ cat.items | size }})</a></li>
    {% endfor %}
  </ul>
  </nav>

  <section class="topics-list">
  <h3>All Topics</h3>
  {% for topic in site.topics | sort: "title" %}
  {% assign topic_category_slug = topic.category | slugify %}
  <article class="topic-list-item">
    <h4><a href="{{ topic.url | relative_url }}">{{ topic.title }}</a></h4>
    {% if topic.summary %}
      <p class="summary">{{ topic.summary }}</p>
    {% endif %}
    <p class="meta">Category: <a href="{{ '/categories/' | append: topic_category_slug | relative_url }}">{{ topic.category }}</a> | Tags: {% if topic.tags %}{{ topic.tags | join: ", " }}{% else %}—{% endif %}</p>
  </article>
  {% endfor %}

  {% if site.topics == empty %}
    <p>No topics yet — add one under <code>_topics</code> and commit. Example: <code>_topics/hashing-vs-encryption.md</code>.</p>
  {% endif %}
  </section>
</div>