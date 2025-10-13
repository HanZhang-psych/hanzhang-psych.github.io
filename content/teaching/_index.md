---
title: Teaching
summary: My courses
type: landing
gallery: true

design:
  # Section spacing
  spacing: '0rem'

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
      text: |
        Below is a list of courses I have taught. Click on a specific course to see more information.
      filters:
        folders:
          - teaching
    design:
      view: article-grid
      columns: 2
      spacing:
        padding: ['0rem', '0rem', '1rem', '0rem']

  - block: markdown
    content:
      title: Mentoring
      text: |
        Throughout my career, I have been fortunate to mentor many fabulous undergraduate student research assistants. Here are some of them presenting their work at various conferences.
    design:
      spacing:
        padding: ['0rem', '0rem', '0rem', '0rem']
---
{{< nanogallery directory="media/mentees/*" >}}