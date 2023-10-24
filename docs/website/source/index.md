---
sd_hide_title: true
html_theme.sidebar_secondary.remove:
---
# {{pp_meta.name}}
:::{toctree}
:includehidden:
:hidden:
:numbered:
intro/index
manual/index
api/index
news/index
contribute/index
about/index
help/index
:::

{% for theme in ["light", "dark"] %}
:::{image} {{pp_meta.url.website.base}}/_static/full_{{theme}}.svg
:alt: {{pp_meta.name}}
:align: center
:class: only-{{theme}} homepage-logo
:::
{% endfor %}

[{{ pp_meta.tagline }}]{.one-liner}

---

{{ pp_meta.description.replace(pp_meta.name,
"[{}]{}".format(pp_meta.name, "{.project-name}"), 1) }}


::::{grid} 1 2 2 2
:gutter: 3
{% for point in pp_meta.keynotes %}
:::{grid-item-card} {{point.title}}
:class-title: sd-text-center
{{point.description}}
:::
{% endfor %}
::::


::::{card-carousel} 1

:::{card} Intro: Discover the Essence of {{pp_meta.name}}
:link: intro/index.html
:img-top: /_static/img/icon/background.svg
:class-title: sd-text-center
:class-img-top: dark-light icon-image
Start off with the Introduction section to learn more about
{{pp_meta.name}}'s motivations, objectives and capabilities.
This section offers a high-level overview of {{pp_meta.name}}, highlighting its main features,
the challenges they address, and the value they bring to your projects.
Serving as an excellent starting point for new users,
it also provides a summary of related background information and concepts
that are essential to fully understanding and utilizing {{pp_meta.name}}.
:::


:::{card} Manual: Your Comprehensive Guide
:link: intro/index.html
:img-top: /_static/img/icon/user_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

Dive into our Manual section for detailed step-by-step instructions on using {{pp_meta.name}} efficiently.
From setting up your project to deploying it, this comprehensive guide covers all essential aspects
of package development and maintenance.

The Manual section contains comprehensive documentation and guides for users to understand
the various functionalities and how to use PyPackIT effectively. It will provide step-by-step instructions
for different tasks and explain the available features in detail.

The user guide provides in-depth information on the
key concepts of SciPy with useful background information and explanation.

:::


:::{card} API: Master the {{pp_meta.name}} Programming Interface
:link: intro/index.html
:img-top: /_static/img/icon/api.svg
:text-align: center
:class-img-top: dark-light icon-image

For advanced users seeking deeper insights into PyPackIT,
our API section provides a thorough reference guide.
Explore the complete Python package documentation and learn to interact programmatically with PyPackIT.

This section is likely dedicated to providing a comprehensive API reference for PyPackIT.
It will be beneficial for more advanced users who want to interact with PyPackIT programmatically
and need detailed information about the available functions and methods.
:::


:::{card} News: Stay Informed with {{pp_meta.name}} Updates
:link: intro/index.html
:img-top: /_static/img/icon/news.svg
:text-align: center
:class-img-top: dark-light icon-image

Stay up-to-date with the latest news, announcements, and developments related to PyPackIT.
The News section keeps you informed about new features, bug fixes, and enhancements that make your
Python journey even smoother.

The News section will likely keep users updated with the latest developments, updates,
and announcements related to PyPackIT. It's essential for users to stay informed about new features,
bug fixes, and other project-related news.
:::


:::{card} Contribute: Join the PyPackIT Community
:link: intro/index.html
:img-top: /_static/img/icon/dev_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

We believe in collaboration and value contributions from our users.
In the Contribute section, you'll find guidelines on how to get involved,
report issues, and actively participate in making PyPackIT even better.
:::


:::{card} About: Unveiling the PyPackIT Story
:link: intro/index.html
:img-top: /_static/img/icon/about.svg
:text-align: center
:class-img-top: dark-light icon-image

Learn more about the people behind PyPackIT and the project's history.
The About section offers insights into our mission, core values, and the dedication driving PyPackIT's success.

The About section will likely provide more in-depth information about the PyPackIT project,
including its history, the team behind it, its mission, and any notable achievements.
:::


:::{card} Help: Find Support When You Need It
:link: intro/index.html
:img-top: /_static/img/icon/faq.svg
:text-align: center
:class-img-top: dark-light icon-image

The Help section is your go-to resource for assistance with any challenges you encounter.
Explore FAQs, troubleshoot common issues, and connect with our support team for personalized solutions.

The Help section can serve as a user support hub, offering assistance to users facing challenges or
seeking answers to common questions. It may include FAQs, troubleshooting guides, and ways to reach out
to the support team.
:::

:::{card} Miscellaneous
:link: intro/index.html
:text-align: center
:img-top: /_static/img/icon/misc.svg
:class-img-top: dark-light icon-image

* Item one
* item two
* uwrgw wowinwnwfw wrgww egeg eg eerg e erheh
* gegethe
:::

::::
