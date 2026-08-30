---
# Leave the homepage title empty to use the site title
title: ""
date: 2026-08-30
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
        - **Aug 2026:** Student mentee Nithya Rajan's poster **Can Machine Learning Predict L3 Driving Takeover Performance from Gaze and Cognitive Traits?** won the 1st place in the UMTRI Poster Competition. 🎉
        - **Aug 2026:** Student mentee Bianca Done's poster **Who Can Re-Enter the Loop? A Scoping Review** won the 2nd place in the UMTRI Poster Competition. 🎉
        - **Aug 2026:** Student mentee Stefanie Schneider presented her poster **Who Can Reengage Better During Level-3 Automated Driving?** at the SURE symposium. 🎉
        - **Aug 2026:** Paper **Does Global Slowing Explain Age Effects in Inhibitory Control?** accepted by _Psychological Science_! :tada: Shared first authorship with Jacob Sellers.
        - **Jul 2026:** Helped organize a session named **SAE Level 3 Features: Coming Soon to a Vehicle Owned by You** at ATS 2026.
        - **May 2026:** Gave an invited talk at Mcity's annual research review: **Measurement of Drivers' Re-Engagement Readiness**. Watch it [here](https://www.youtube.com/watch?v=0DVUirUmZik)!
        - **Apr 2026:** Gave an invited talk at Lawrence Tech University: [What can we learn from eye movements?](https://ltu.edu/academics-calendar/coas-seminar-series-april-2026/)
        - **Apr 2026:** First-author paper [I’m trying to read here! How does irrelevant speech affect how you read?](https://link.springer.com/article/10.1007/s10339-026-01346-4) accepted by _Cognitive Processing_!

    design:
      css_class: recent-updates
      columns: '2'
      spacing:
        padding: ['2rem', '0rem', '2rem', '0rem']

  - block: collection
    content:
      title: Featured Work
      filters:
        folders:
          - journal-articles
          - preprints
        featured_only: true
      count: 6
      archive:
        enable: true
        text: See all publications
        link: publication/
    design:
      view: featured-publication
      columns: 1
      spacing:
        padding: ['2rem', '0rem', '2rem', '0rem']

  # - block: collection
  #   content:
  #     title: Selected Preprints
  #     filters:
  #       folders:
  #         - preprints
  #       featured_only: false
  #     count: 4
  #     archive:
  #       enable: true
  #       text: See all preprints
  #       link: preprints/
  #   design:
  #     view: citation
  #     columns: 1
  #     spacing:
  #       padding: ['0rem', '0rem', '2rem', '0rem']

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
