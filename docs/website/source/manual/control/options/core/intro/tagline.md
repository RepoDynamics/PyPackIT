# Tagline
You can define a single-line tagline, slogan, or description of the project by adding a `tagline` key
to the `core/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/intro.yaml`
# Project tagline
tagline: >-
  Python Projects Perfected: Innovate, Develop, and Deploy Effortlessly!
:::

This is used in several places, such as the `description` metadata of your package
(displayed at the top of the PyPI page of your package),
and by default the `description` field of your GitHub repository
displayed under the `About` section of your repository homepage.
However, the latter can be also set to a different value in the `dev/repo.yaml` file.
