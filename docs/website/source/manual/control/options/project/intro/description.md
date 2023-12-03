# Description
A description acts as an abstract for your project,
providing new users with a quick overview of the project's main features and functionalities.


## Setting
You can set a description by adding a `description` key to the `project/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `project/intro.yaml`
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

You can use simple HTML formatting elements in the description,
such as `<b>` for bold text, `<i>` for italic text, `<u>` for underlined text, etc.
Also, the description can have multiple paragraphs,
separated by `<br>` tags; do not introduce any newlines in the YAML text directly,
as this will break the formatting.
Notice the use of substitution pattern `${‎{ name }}`
to reference the project name dynamically.


## Usage

The description is used in the main README file of the repository,
as well as the `readme` metadata of your package
(formerly known as `long_description`) displayed on the PyPI homepage of the package,
and the homepage of your project's website.
It serves as a short introduction to your project,
providing new users with a quick overview of the project's purpose and value proposition.
