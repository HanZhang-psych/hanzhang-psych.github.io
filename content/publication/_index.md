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
      text: Select a publication type
      filters:
        folders:
          - publication/journal-articles
    design:
      view: article-grid
      fill_image: false
      columns: 1
  - block: collection
    content:
      title: Preprints
      text: Select a publication type
      filters:
        folders:
          - publication/preprints
    design:
      view: article-grid
      fill_image: false
      columns: 1
---