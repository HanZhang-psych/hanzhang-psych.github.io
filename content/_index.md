---
# Leave the homepage title empty to use the site title
title: ""
date: 2025-06-21
type: landing

design:
  # Default section spacing
  spacing: "2rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Download CV
        url: uploads/CV_HanZhang.pdf
    design:
      css_class: dark
      background:
        color: black
        image:
          # Add your image background to `assets/media/`.
          #filename: stacked-peaks.svg
          filename: dileepa-nipun-5bakUnqvBo0-unsplash.jpg
          filters:
            brightness: 0.3
          size: cover
          position: center
          parallax: false

  # - block: markdown
  #   content:
  #     title: 'My Research'
  #     subtitle: ''
  #     text: |-
  #       Use this area to speak to your mission. I'm a research scientist in the Moonshot team at DeepMind. I blog about machine learning, deep learning, and moonshots.

  #       I apply a range of qualitative and quantitative methods to comprehensively investigate the role of science and technology in the economy.
        
  #       Please reach out to collaborate 😃
  #   design:
  #     columns: '1'

  - block: markdown
    id: updates
    content:
      title: Recent Updates
      subtitle: ''
      text: |-
        - **October 2025:** [_PupEyes: An Interactive Python Library for Eye Movement Data Processing_](/journal-articles/zhang-pupeyes-2025/) was published in *Behavior Research Methods*.
        - **October 2025:** Launched a UMTRI and Mcity Integration Fund project on takeover performance in urgent Level-3 driving situations.
        - **July 2025:** Posted a preprint on how irrelevant speech affects reading eye movements: [_I'm Trying to Read Here!_](/preprints/zhang-im-2025/)
        - **June 2025:** Started as an Assistant Research Scientist at the University of Michigan Transportation Research Institute.
        - **April 2025:** [_The temporal dynamics of visual attention_](/journal-articles/zhang-temporal-2025/) was published in *Journal of Experimental Psychology: General*.
    design:
      columns: '1'
      spacing:
        padding: ['2rem', '0rem', '1rem', '0rem']

  - block: collection
    content:
      title: Selected Publications
      filters:
        folders:
          - journal-articles
        featured_only: true
      count: 6
      archive:
        enable: true
        text: See all journal articles
        link: journal-articles/
    design:
      view: citation
      columns: 1
      spacing:
        padding: ['2rem', '0rem', '2rem', '0rem']

  - block: collection
    content:
      title: Selected Preprints
      filters:
        folders:
          - preprints
        featured_only: false
      count: 4
      archive:
        enable: true
        text: See all preprints
        link: preprints/
    design:
      view: citation
      columns: 1
      spacing:
        padding: ['0rem', '0rem', '2rem', '0rem']

  # - block: collection
  #   id: talks
  #   content:
  #     title: Recent & Upcoming Talks
  #     filters:
  #       folders:
  #         - event
  #   design:
  #     view: article-grid
  #     columns: 1

  # - block: collection
  #   id: news
  #   content:
  #     title: Recent News
  #     subtitle: ''
  #     text: ''
  #     # Page type to display. E.g. post, talk, publication...
  #     page_type: post
  #     # Choose how many pages you would like to display (0 = all pages)
  #     count: 5
  #     # Filter on criteria
  #     filters:
  #       author: ""
  #       category: ""
  #       tag: ""
  #       exclude_featured: false
  #       exclude_future: false
  #       exclude_past: false
  #       publication_type: ""
  #     # Choose how many pages you would like to offset by
  #     offset: 0
  #     # Page order: descending (desc) or ascending (asc) date.
  #     order: desc
  #   design:
  #     # Choose a layout view
  #     view: date-title-summary
  #     # Reduce spacing
  #     spacing:
  #       padding: [0, 0, 0, 0]
---
