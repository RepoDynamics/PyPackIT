---
sd_hide_title: true
html_theme.sidebar_secondary.remove:
---
# {{meta.project.name}}
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

:::{image} /_static/img/logo/logo_light.svg
:alt: Logo
:align: center
:class: only-light homepage-logo
:::
:::{image} /_static/img/logo/logo_dark.svg
:alt: Logo
:align: center
:class: only-dark homepage-logo
:::

[{{ meta.project.tagline }}]{.one-liner}

---

{{ meta.project.description.replace(meta.project.name, 
"[{}]{}".format(meta.project.name, "{.project-name}"), 1) }}


::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Automation
:class-title: sd-text-center
{{ meta.project.name }} streamlines a remarkable portion of the process of creating, 
documenting, testing, publishing, and maintaining Python packages, 
making your project development a pleasant breeze!
:::

:::{grid-item-card} Synchronization
:class-title: sd-text-center
{{ meta.project.name }} gathers all your project's key information and configuration in one place, 
and dynamically updates them throughout your repository, Python package, and documentation website.
:::

:::{grid-item-card} Configuration
:class-title: sd-text-center
:text-align: left
{{ meta.project.name }} elevates your project by providing full configuration for your repository, 
Python package, and documentation website, according to the latest guidelines and best practices.
:::

:::{grid-item-card} Customization
:class-title: sd-text-center
While carefully configured, {{ meta.project.name }} is also fully customizable, 
allowing you to tailor every aspect of your development pipeline to your specific needs.
:::

:::{grid-item-card} Documentation
:class-title: sd-text-center
{{ meta.project.name }} comes with a professional website for your project, that is easily
customizable, and automatically generated and deployed on your preferred platform.
:::

:::{grid-item-card} Production
:class-title: sd-text-center
With {{ meta.project.name }}, the only remaining step to publishing a production-ready
Python project is adding your code, unit-tests and documentation content. 
:::

::::


::::{card-carousel} 1

:::{card} Intro: Discover the Essence of {{meta.project.name}}
:link: intro/index.html
:img-top: /_static/img/icon/background.svg
:class-title: sd-text-center
:class-img-top: dark-light icon-image
Start off with the Introduction section to learn more about 
{{meta.project.name}}'s motivations, objectives and capabilities. 
This section offers a high-level overview of {{meta.project.name}}, highlighting its main features, 
the challenges they address, and the value they bring to your projects. 
Serving as an excellent starting point for new users, 
it also provides a summary of related background information and concepts 
that are essential to fully understanding and utilizing {{meta.project.name}}.
:::


:::{card} Manual: Your Comprehensive Guide
:link: intro/index.html
:img-top: /_static/img/icon/user_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

Dive into our Manual section for detailed step-by-step instructions on using {{meta.project.name}} efficiently. 
From setting up your project to deploying it, this comprehensive guide covers all essential aspects 
of package development and maintenance.

The Manual section contains comprehensive documentation and guides for users to understand 
the various functionalities and how to use PyPackIT effectively. It will provide step-by-step instructions 
for different tasks and explain the available features in detail.

The user guide provides in-depth information on the
key concepts of SciPy with useful background information and explanation.

:::


:::{card} API: Master the {{meta.project.name}} Programming Interface
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


:::{card} News: Stay Informed with {{meta.project.name}} Updates
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
