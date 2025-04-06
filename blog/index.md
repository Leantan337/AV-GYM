---
layout: default
title: AV-GYM Blog
---

# Latest Blog Posts

Welcome to the AV-GYM blog, where we share fitness tips, workout plans, and success stories.

{% for post in site.posts %}
  <article>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <time datetime="{{ post.date | date: "%Y-%m-%d" }}">{{ post.date | date: "%B %d, %Y" }}</time>
    {{ post.excerpt }}
  </article>
{% endfor %}
