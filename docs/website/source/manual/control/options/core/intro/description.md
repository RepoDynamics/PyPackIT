# Description
You can add a long description of the project that can have multiple paragraphs,
with Markdown or HTML formatting, by adding a `description` key to the `core/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/intro.yaml`
# Project description
description: >-
  ${‎{ name }} is a free and open-source toolkit
  <b>empowering the development of open-source
  Python projects on GitHub</b>.
  It is a <b>dynamic repository template</b>
  that provides a complete, professional, and
  robust infrastructure for your project,
  where the only thing missing is your code.
  With ${‎{ name }}, you can solely focus on what truly matters:
  implementing your ideas and bringing your vision to life!
:::

This is used in the main README file of the repository, as well as the `readme` metadata of your package
(formerly known as `long_description`) displayed on the PyPI homepage of the package,
and the homepage of your project's website. Notice the use of substitution pattern `${‎{ name }}`
to reference the project name dynamically.