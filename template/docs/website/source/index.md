---
sd_hide_title: true
html_theme.sidebar_secondary.remove:
---

# {{ccc.name}}

<!-- Project Logo -->
{% for theme in ["light", "dark"] %}
{% set key = "logo_full_" + theme %}
:::{image} {{ ccc.web.file[key].rel_path }}
:alt: {{ccc.name}}
:align: center
:class: only-{{theme}} homepage-logo
:::
{% endfor %}


---


<!-- Project Abstract -->
{{ ccc.abstract.replace(ccc.name, "[{}]{}".format(ccc.name, "{.sd-font-weight-bold .pst-color-primary}"), 1) }}


<!-- 'Key Features' Button -->
:::{button-ref} intro/overview/index
:ref-type: myst
:color: primary
:expand:
:class: homepage-button

[Key Features]{.homepage-button-text}
:::


<!-- Project Highlights -->
::::{card-carousel} 2
{% for point in ccc.highlights %}
:::{card} {{point.title}}
:class-title: sd-text-center
{{point.description}}
:::
{% endfor %}
::::


<br>


<!-- 'Learn More' Button -->
:::{button-ref} intro/index
:ref-type: myst
:color: primary
:expand:

[Learn More]{.homepage-button-text}
:::


<!-- Sections Overview -->
::::{card-carousel} 1

:::{card} Introduction
:link: intro/index.html
:img-top: /_media/icon/background.svg
:class-title: sd-text-center
:class-img-top: dark-light black-svg-icon icon-as-card-img-top

Begin with the Introduction section
to learn more about {{ccc.name}}'s motivations,
objectives, and capabilities.
This high-level overview highlights key features of {{ ccc.name }},
the challenges they address, and how they can enhance your work.
The Introduction section is the perfect starting point for new users,
summarizing essential information to help you get started with {{ccc.name}}.
:::


:::{card} User Manual
:link: manual/index.html
:img-top: /_media/icon/user_guide.svg
:text-align: center
:class-img-top: dark-light black-svg-icon icon-as-card-img-top

Explore the Manual for a comprehensive guide to using {{ccc.name}}.
Start with the installation guide for a seamless setup in various environments,
then move on to the quickstart guide for step-by-step instructions
to start using {{ ccc.name }} immediately.
The Manual features detailed tutorials with executable examples,
providing hands-on experience with
{{ccc.name}}'s core concepts and functionalities.
:::


:::{card} API Reference
:link: api/index.html
:img-top: /_media/icon/api.svg
:text-align: center
:class-img-top: dark-light black-svg-icon icon-as-card-img-top

Explore the complete Python package documentation and learn to interact programmatically with {{ccc.name}}.
This section provides a full reference of {{ccc.name}}'s application programming interface (API),
including all its packages, modules, classes, methods, functions, and attributes.
:::


:::{card} News Blog
:link: news/index.html
:img-top: /_media/icon/news.svg
:text-align: center
:class-img-top: dark-light black-svg-icon icon-as-card-img-top

Check out our blog to stay up to date with the latest announcements
and developments of the {{ccc.name}} project.
This section keeps you informed about {{ccc.name}}'s new releases with detailed changelogs,
and provides insights into the project's roadmap
and the team's plans for the future of {{ccc.name}}.
Being the main source of information about {{ccc.name}}'s latest developments,
the news section is a full-fledged blog with RSS feed support that you can subscribe to,
so you never miss out on any important updates.
:::


:::{card} Contribution Guide
:link: contribute/index.html
:img-top: /_media/icon/dev_guide.svg
:text-align: center
:class-img-top: dark-light black-svg-icon icon-as-card-img-top

{{ ccc.name }} is a free and open-source project that can only survive
and grow through the help and support of great members like you.
If you are interested in joining the {{ ccc.name }} community,
head over to our contribution guide to learn more about how you can help.
From sharing your feedback and ideas or becoming a collaborator and helping us develop the project,
to spreading the word and helping us reach more people
or becoming a sponsor and supporting the project financially,
we highly appreciate all your contributions!
:::


:::{card} About {{ ccc.name }}
:link: about/index.html
:img-top: /_media/icon/about.svg
:text-align: center
:class-img-top: dark-light black-svg-icon icon-as-card-img-top

Learn more about the team behind {{ ccc.name }} and the project's history.
The About section offers insights into our mission, core values,
and the dedication driving {{ ccc.name }}'s success.
:::


:::{card} Support Guide
:link: help/index.html
:img-top: /_media/icon/faq.svg
:text-align: center
:class-img-top: dark-light black-svg-icon icon-as-card-img-top

The Help section is your go-to resource for assistance with any challenges you encounter.
Explore FAQs, troubleshoot common issues, and connect with our support team for personalized solutions.
:::

::::
