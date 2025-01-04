---
sd_hide_title: true
html_theme.sidebar_secondary.remove:
---

# |{{ccc.name}}|

:::{image} /_media/logo/full_light.svg
:alt: |{{ccc.name}}|
:align: center
:class: dark-light themed homepage-logo
:::
:::{image} /_media/logo/full_dark.svg
:class: hidden
:::

---

{.element-in-page-without-sidebar}
|{{ ccc.abstract.replace(ccc.name, "[{}]{}".format(ccc.name, "{.project-name}"), 1) }}|


<div class="element-in-page-without-sidebar">

:::{button-ref} intro/overview/index
:ref-type: myst
:color: primary
:expand:
:class: homepage-button

[Key Features]{.homepage-button-text}
:::

</div>


::::{card-carousel} 2
:class: element-in-page-without-sidebar
|{% for point in ccc.highlights %}|
:::{card} |{{point.title}}|
:class-title: sd-text-center
|{{point.description}}|
:::
|{% endfor %}|
::::

<br>

<div class="element-in-page-without-sidebar">

:::{button-ref} intro/index
:ref-type: myst
:color: primary
:expand:

[Learn More]{.homepage-button-text}
:::

</div>


::::{card-carousel} 1
:class: element-in-page-without-sidebar


:::{card} Introduction
:link: intro/index.html
:img-top: /_media/icon/background.svg
:class-title: sd-text-center
:class-img-top: dark-light icon-image

Start off with the introduction section to learn more about
|{{ccc.name}}|'s motivations, objectives and capabilities.
This section offers a high-level overview of |{{ccc.name}}|, highlighting its main features,
the challenges they address, and the value they bring to your projects.
Serving as an excellent starting point for new users,
it also provides a summary of fundamental concepts and background information
that are essential to fully understanding and utilizing |{{ccc.name}}|.
:::


:::{card} User Manual
:link: manual/index.html
:img-top: /_media/icon/user_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

Dive into the user manual for in-depth information on the key concepts of |{{ccc.name}}|,
along with detailed explanations of all its features and functionalities.
From step-by-step instructions on setting up |{{ccc.name}}| for the first time
and integrating it into your new or existing project,
to comprehensive guides on how to use its various features and functionalities
in your software development process,
the user manual covers everything you need to know
to fully leverage |{{ccc.name}}|'s capabilities.
:::


:::{card} API Reference
:link: api/index.html
:img-top: /_media/icon/api.svg
:text-align: center
:class-img-top: dark-light icon-image

Refer to the API guide for a complete reference of |{{ccc.name}}| options
and metadata, which act as an interface for managing and customizing your entire project.
This section includes an exhaustive list of all control center configurations, along with their usage,
examples, and other related data. It also contains a full reference of all other data files
in your repository that are used by |{{ccc.name}}| to store and retrieve various information
about your project, such as changelogs, variables, contributors, and cached data.
:::


:::{card} News and Updates
:link: news/index.html
:img-top: /_media/icon/news.svg
:text-align: center
:class-img-top: dark-light icon-image

Check out our blog to stay up to date with the latest announcements
and developments of the |{{ccc.name}}| project.
This section keeps you informed about |{{ccc.name}}|'s new releases with detailed changelogs,
and provides insights into the project's roadmap
and the team's plans for the future of |{{ccc.name}}|.
Being the main source of information about |{{ccc.name}}|'s latest developments,
the news section is a full-fledged blog with RSS feed support that you can subscribe to,
so you never miss out on any important updates.
:::


:::{card} Contribution Guide
:link: contribute/index.html
:img-top: /_media/icon/dev_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

|{{ ccc.name }}| is a free and open-source project that can only survive
and grow through the help and support of great members like you.
If you are interested in joining the |{{ ccc.name }}| community,
head over to our contribution guide to learn more about how you can help.
From sharing feedback and ideas or becoming a collaborator and helping us develop the project,
to spreading the word and helping us reach more people
or becoming a sponsor and supporting the project financially,
we highly appreciate all your contributions!
:::


:::{card} About
:link: about/index.html
:img-top: /_media/icon/about.svg
:text-align: center
:class-img-top: dark-light icon-image

Learn more about the team behind |{{ ccc.name }}| and the project's history.
The About section offers insights into our mission, core values,
and the dedication driving |{{ ccc.name }}|'s success.
:::


:::{card} Help and Support
:link: help/index.html
:img-top: /_media/icon/faq.svg
:text-align: center
:class-img-top: dark-light icon-image

The Help section is your go-to resource for assistance with any challenges you encounter.
Explore FAQs, troubleshoot common issues, and connect with our support team for personalized solutions.
:::

::::
