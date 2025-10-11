---
title: Publications
type: landing
cms_exclude: true

# Optional header image (relative to `static/media/` folder).
banner:
  caption: ''
  image: ''

design:
  # Section spacing
  spacing: '2rem'

# Page sections
sections:
  - block: collection
    content:
      title: Journal Articles
      filters:
        folders:
          - publication/journal-articles
    design:
      view: citation
      fill_image: false
      columns: 1
  - block: collection
    content:
      title: Preprints
      filters:
        folders:
          - publication/preprints
    design:
      view: citation
      fill_image: false
      columns: 1
---