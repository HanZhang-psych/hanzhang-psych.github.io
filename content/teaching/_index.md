---
title: Teaching
summary: My courses
type: landing

cascade:
  - _target:
      kind: page
    params:
      show_breadcrumb: true

sections:
  - block: collection
    id: teaching
    content:
      title: Teaching
      filters:
        folders:
          - teaching
    design:
      view: article-grid
      columns: 2

  - block: markdown
    content:
      title: Mentoring
      text: |
        Throughout my career, I have been fortunate to mentor many fabulous undergraduate student research assistants. Here are some of them presenting their work at various conferences.

        {{< nanogallery directory="media/mentees/*" >}}
---
