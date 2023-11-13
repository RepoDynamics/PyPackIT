### Project Introduction
- File: `core/intro.yaml`

#### `name`
Name of the project.
- Type: string
- Default: name of the repository after replacing hyphens with spaces

The name can only contain ASCII alphanumeric characters, spaces, periods (.), underscores (_) and hyphens (-).
Additionally, it must start and end with an alphanumeric character.

Example:
```yaml
name: PyPackIT
```

:::{note}
The package name is derived from the name of the project, via normalization[^name-normalization]:
The project name is lowercased, with all runs of spaces, periods (.), underscores (_) and hyphens (-)
replaced with a single hyphen.
That is why we enforce the restrictions of a valid non-normalized package name here,
otherwise the project name is only used in documents to refer to the project,
and so could have contained any unicode character.
:::
[^name-normalization]: [Python Packaging User Guide > PyPA specifications > Package name normalization](https://packaging.python.org/en/latest/specifications/name-normalization/)

#### `tagline`
A single-line tagline, slogan, or description of the project.
- Type: string
- Default: ""

Example:
```yaml
tagline: >-
  Python Projects Perfected: Innovate, Develop, and Deploy Effortlessly!
```

#### `description`
A long description of the project that can have multiple paragraphs, with Markdown or HTML formatting.
- Type: string
- Default: ""

Example:
```yaml
description: >-
  PyPackIT is a free and open-source toolkit
  <b>empowering the development of open-source Python projects on GitHub</b>.
  It is a <b>dynamic repository template</b> that provides a complete, professional, and
  robust infrastructure for your project, where the only thing missing is your code.
  With PyPackIT, you can solely focus on what truly matters:
  implementing your ideas and bringing your vision to life!
```

#### `keywords`
Keywords to describe the project.
- Type: list of strings
- Default: []

Each keyword must only contain 50 or less ASCII alphanumeric characters, spaces, and hyphens (-).
Additionally, it must start and end with an alphanumeric character.

Example:
```yaml
keywords:
  - python
  - github
  - packaging
  - template
  - dynamic repository
  - repository template
```

#### `keynotes`
A list of keynotes about the project.
- list of dictionaries
- Default: []

Each keynote is a dictionary with the following keys:
- `title`: string, required\
Title of the keynote.
- `description`: string, required\
Description of the keynote.


Example:
```yaml
keynotes:
  - title: Automation
    description: >-
      PyPackIT streamlines a remarkable portion of the process of creating,
      documenting, testing, publishing, and maintaining Python packages,
      making your project development a pleasant breeze!
  - title: Synchronization
    description: >-
      PyPackIT gathers all your project's key information and configuration in one place,
      and dynamically updates them throughout your repository, Python package, and documentation website.
  - title: Configuration
    description: >-
      PyPackIT elevates your project by providing full configuration for your repository,
      Python package, and documentation website, according to the latest guidelines and best practices.
  - title: Customization
    description: >-
      While carefully configured, PyPackIT is also fully customizable,
      allowing you to tailor every aspect of your development pipeline to your specific needs
```
