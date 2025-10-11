---
title: Publications
type: landing

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
          - journal-articles/
    design:
      view: article-grid
      fill_image: false
      columns: 1
  - block: collection
    content:
      title: Preprints
      filters:
        folders:
          - preprints/
    design:
      view: article-grid
      fill_image: false
      columns: 1
---