---
layout: default
title: Handbook — Index
---

# Handbook Index

<p class="intro">This is a compact, searchable handbook of small tech notes. Add a new topic by creating a Markdown file under <code>_topics</code> with frontmatter: <code>title</code>, <code>category</code>, <code>tags</code>, and an optional <code>summary</code>.</p>

<div class="search-bar">
  <input id="topic-search" placeholder="Search topics, tags, or categories..." />
</div>

<nav class="categories">
  <h3>Categories</h3>
  <ul>
    {% assign grouped = site.topics | group_by: "category" | sort: "name" %}
    {% for cat in grouped %}
      <li><a href="/categories/{{ cat.name | slugify }}/">{{ cat.name }} ({{ cat.items | size }})</a></li>
    {% endfor %}
  </ul>
</nav>

<section class="topics-list">
  <h3>All Topics</h3>
  {% for topic in site.topics | sort: "title" %}
  <article class="topic-list-item">
    <h4><a href="{{ topic.url }}">{{ topic.title }}</a></h4>
    {% if topic.summary %}
      <p class="summary">{{ topic.summary }}</p>
    {% endif %}
    <p class="meta">Category: <a href="/categories/{{ topic.category | slugify }}/">{{ topic.category }}</a> | Tags: {% if topic.tags %}{{ topic.tags | join: ", " }}{% else %}—{% endif %}</p>
  </article>
  {% endfor %}

  {% if site.topics == empty %}
    <p>No topics yet — add one under <code>_topics</code> and commit. Example: <code>_topics/hashing-vs-encryption.md</code>.</p>
  {% endif %}
</section>