# Keynotes
Keynotes are bullet points that describe the main features of your project.


## Setting
You can add a list of keynotes by adding a `keynotes` key to the `project/intro.yaml` file.
Each keynote must be an object with a `title` and a short `description`:

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


## Usage
Keynotes are shown in the main README file of the repository,
as well as the homepage of your project's website
and your package's PyPI homepage.
