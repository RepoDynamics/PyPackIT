---
sd_hide_title: true
html_theme.sidebar_secondary.remove:
---
# Homepage
:::{toctree}
:includehidden:
:hidden:
:numbered:
intro/index
manual/index
api/index
news/index
help/index
contribute/index
about/index
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

[{{ env.config.rd_meta.project.tagline }}]{.one-liner}

---

{{ env.config.rd_meta.project.description.replace(name, "[{}]{}".format(name, "{.project-name}"), 1) }}

::::{card-carousel} 1

:::{card} Introduction
:link: pages/intro/index.html
:img-top: /_static/img/icon/background.svg
:class-title: sd-text-center
:class-img-top: dark-light icon-image

As a starting point for new users, this section provides an **overview**
of {{name}}, describing the **motivations** behind it, 
and highlighting its **objectives** and **capabilities**.
A summary of related background **information** is provided as well, 

**theoretical** and **technical** essential to ... and fully utilizing its

After reading this section, you will have a solid understanding of what {{name}} is and does, 
:::


:::{card} User Guide
:link: intro/index.html
:img-top: /_static/img/icon/user_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

The user guide 
:::


:::{card} API Reference
:link: intro/index.html
:img-top: /_static/img/icon/api.svg
:text-align: center
:class-img-top: dark-light icon-image

The user guide provides in-depth information on the
key concepts of SciPy with useful background information and explanation.

This is the second paragraph.

And a third one.
:::


:::{card} News
:link: intro/index.html
:img-top: /_static/img/icon/news.svg
:text-align: center
:class-img-top: dark-light icon-image

The user guide provides in-depth information on the
key concepts of SciPy with useful background information and explanation.

This is the second paragraph.

And a third one.
:::


:::{card} Developer Guide
:link: intro/index.html
:img-top: /_static/img/icon/dev_guide.svg
:text-align: center
:class-img-top: dark-light icon-image

The user guide provides in-depth information on the
key concepts of SciPy with useful background information and explanation.

This is the second paragraph.

And a third one.
:::


:::{card} About
:link: intro/index.html
:img-top: /_static/img/icon/about.svg
:text-align: center
:class-img-top: dark-light icon-image

The user guide provides in-depth information on the
key concepts of SciPy with useful background information and explanation.

This is the second paragraph.

And a third one.
:::


:::{card} Frequently Asked Questions
:link: intro/index.html
:img-top: /_static/img/icon/faq.svg
:text-align: center
:class-img-top: dark-light icon-image

The user guide provides in-depth information on the
key concepts of SciPy with useful background information and explanation.

This is the second paragraph.

And a third one.
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

## Getting Started

:::{tip}
You can simply copy the contents of each presented code/command block in this documentation
(like the one below), by hovering your mouse over that block, and clicking on the copy button
that appears on the right side of the block.
:::
