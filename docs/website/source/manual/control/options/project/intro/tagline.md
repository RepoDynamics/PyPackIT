# Tagline
A tagline is a single-sentence description or slogan for your project,
used to summarize its purpose and/or its value proposition.


## Setting

You can set a tagline by adding a `tagline` key
to the `project/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `project/intro.yaml`
# Project tagline
tagline: The Best Python Project Ever
:::


## Usage

The tagline is used in several places, such as the `description` metadata of your package
(displayed at the top of the PyPI page of your package),
and by default the `description` field of your GitHub repository
displayed under the `About` section of your repository homepage.
However, the latter can be also set to a different value in the `dev/repo.yaml` file.
