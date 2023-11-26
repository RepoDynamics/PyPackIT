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
news/index
contribute/index
about/index
help/index
:::

{% for theme in ["light", "dark"] %}
:::{image} _static/logo_full_{{theme}}.svg
:alt: {{pp_meta.name}}
:align: center
:class: only-{{theme}} homepage-logo
:::
{% endfor %}

---

{.homepage}
{{ pp_meta.description.replace(pp_meta.name,
"[{}]{}".format(pp_meta.name, "{.project-name}"), 1) }}


::::{card-carousel} 1
:class: homepage

:::{card} Intro: Discover the Essence of {{pp_meta.name}}
:link: intro/index.html
:img-top: /_static/img/icon/background.svg
:class-title: sd-text-center
:class-img-top: dark-light icon-image

Start off with the introduction section to learn more about
{{pp_meta.name}}'s motivations, objectives and capabilities.
This section offers a high-level overview of {{pp_meta.name}}, highlighting its main features,
the challenges they address, and the value they bring to your projects.
Serving as an excellent starting point for new users,
it also provides a summary of fundamental concepts and background information
that are essential to fully understanding and utilizing {{pp_meta.name}}.
:::


:::{card} Manual: Your Comprehensive Guide
:link: manual/index.html
:img-top: /_static/img/icon/user_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

Dive into the user manual for in-depth information on the key concepts of {{pp_meta.name}},
along with detailed explanations of all its features and functionalities.
From step-by-step instructions on setting up {{pp_meta.name}} for the first time
and integrating it into your new or existing project,
to comprehensive guides on how to use its various features and functionalities
in your software development process,
the user manual covers everything you need to know
to fully leverage {{pp_meta.name}}'s capabilities.
Acting as the main reference for new and experienced users alike,
this section also provides a full overview of all configurations, metadata, and settings
that can be used to fully customize {{pp_meta.name}} to your specific needs.
:::

:::{card} News: Stay Informed with {{pp_meta.name}} Updates
:link: news/index.html
:img-top: /_static/img/icon/news.svg
:text-align: center
:class-img-top: dark-light icon-image

Check out our blog to stay up to date with the latest news, announcements,
and developments of the {{pp_meta.name}} project.
The news section keeps you informed about {{pp_meta.name}}'s new releases,
and their new features, bug fixes, and enhancements that make your software development process even smoother.
Being the main source of information about {{pp_meta.name}}'s latest developments,
this section is a full-fledged blog with RSS feed support that you can subscribe to,
so you never miss out on any important updates.
It also provides insights into the project's roadmap,
and the team's plans for the future of {{pp_meta.name}}.
:::

:::{card} Contribute: Join the PyPackIT Community
:link: contribute/index.html
:img-top: /_static/img/icon/dev_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

We believe in collaboration and value contributions from our users.
In the Contribute section, you'll find guidelines on how to get involved,
report issues, and actively participate in making PyPackIT even better.
:::

:::{card} About: Unveiling the PyPackIT Story
:link: about/index.html
:img-top: /_static/img/icon/about.svg
:text-align: center
:class-img-top: dark-light icon-image

Learn more about the people behind PyPackIT and the project's history.
The About section offers insights into our mission, core values, and the dedication driving PyPackIT's success.

The About section will likely provide more in-depth information about the PyPackIT project,
including its history, the team behind it, its mission, and any notable achievements.
:::

:::{card} Help: Find Support When You Need It
:link: help/index.html
:img-top: /_static/img/icon/faq.svg
:text-align: center
:class-img-top: dark-light icon-image

The Help section is your go-to resource for assistance with any challenges you encounter.
Explore FAQs, troubleshoot common issues, and connect with our support team for personalized solutions.

The Help section can serve as a user support hub, offering assistance to users facing challenges or
seeking answers to common questions. It may include FAQs, troubleshooting guides, and ways to reach out
to the support team.
:::

::::
