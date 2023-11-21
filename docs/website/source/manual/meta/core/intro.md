# Project Introduction

:::::{tab-set}
::::{tab-item} Info
- **Relative Path**: `{{ pp_meta.custom.meta[docname].path }}`
- **Pre-configured**: {{ pp_meta.custom.meta[docname].pre_config }}
::::
::::{tab-item} Schema
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].schema_str }}
:::
::::
::::{tab-item} Default
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].default_str }}
:::
::::
::::{tab-item} Example
:::{code-block} yaml
{{ pp_meta.custom.meta[docname].example_str }}
:::
::::
:::::

All metadata describing your project are stored in the `core/intro.yaml` file
in the repository's `meta` directory.


## Name
By default, that is when the `core/intro.yaml` file is not present or doesn't contain a `name` key,
the name of the project is derived from the name of the repository,
by replacing each hyphen in the repository name with a space:
```python
def derive_project_name(repo_name: str) -> str:
    project_name = repo_name.replace("-", " ")
    return project_name
```
It is recommended that you keep this default behavior, in order to avoid any confusion
and make it easier for others to find your project. However, if you need to define another name
for your project, you can do so by adding a `name` key to the `core/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/intro.yaml`
# Name of the project
name: PyPackIT
:::

The project name on itself has no restrictions and can be any valid unicode string.
However, by default, {{pp_meta.name}} also derives the package name from the project name,
which has to conform to the
[Python Packaging Authority (PyPA)](https://packaging.python.org/en/latest/specifications/name-normalization/)
guidelines. Therefore, if you do not define the package name manually,
your project name can only contain ASCII alphanumeric characters,
spaces, periods `.`, underscores `_` and hyphens `-`.
Additionally, it must start and end with an alphanumeric character,
meaning that the name must match the following regex:
```regex
^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9])$
```

:::{note}
The package name is derived from the name of the project, via normalization[^name-normalization]:
The project name is lowercased, with all runs of spaces, periods, underscores and hyphens
replaced with a single hyphen.
:::
[^name-normalization]: [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)


## Tagline
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


## Description
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


## Keywords
You can add a list of keywords to describe the project by adding a `keywords` key
to the `core/intro.yaml` file:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/intro.yaml`
# Project keywords
keywords:
  - python
  - github
  - packaging
  - template
  - dynamic repository
  - repository template
:::

These keywords are used in the `keywords` metadata of your package,
and by default, the `topics` section of your GitHub repository, displayed under the `About` section.
While PyPA doesn't impose any restrictions on the keywords,
GitHub requires that each keyword only contains 50 or less ASCII alphanumeric characters and hyphens.
Additionally, it must start with an alphanumeric character.
You can define other keywords in the `dev/repo.yaml` file to be used for the GitHub repository topics instead.
If you do not do so, the keywords defined in the `core/intro.yaml` file will be used instead,
and any keyword that does not conform to the GitHub requirements
will be omitted from the GitHub repository topics.


## Keynotes
Keynotes are bullet points that describe the main features of your project.
They are shown in the main README file of the repository, as well as the homepage of your project's website
and your package's PyPI homepage.
You can add a list of keynotes by adding a `keynotes` key to the `core/intro.yaml` file.
Each keynote is an object with a `title` and a short `description`:

:::{code-block} yaml
:caption: 🗂 `./.meta/core/intro.yaml`
# Project keynotes
keynotes:
  - title: Automation
    description: >-
      ${‎{ name }} streamlines a remarkable portion of the process of creating,
      documenting, testing, publishing, and maintaining Python packages,
      making your project development a pleasant breeze!
  - title: Synchronization
    description: >-
      ${‎{ name }} gathers all your project's key information
      and configuration in one place,
      and dynamically updates them throughout your repository,
      Python package, and documentation website.
  - title: Configuration
    description: >-
      ${‎{ name }} elevates your project by providing
      full configuration for your repository,
      Python package, and documentation website,
      according to the latest guidelines and best practices.
  - title: Customization
    description: >-
      While carefully configured, ${‎{ name }} is also fully customizable,
      allowing you to tailor every aspect of your development pipeline
      to your specific needs.
:::
