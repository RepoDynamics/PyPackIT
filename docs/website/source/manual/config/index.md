(manual-cc)=
# Configuration

As described in the [Introduction](#overview-cc) section,
the control center is a powerful DevOps tool
that enables Continuous configuration automation and 
renders your entire project highly dynamic.
For most cases, it is the only interface you need to interact
with to configure, customize, and manage your entire project.
This interface is a [directory](#manual-cc-location) in your repository,
containing [YAML configuration files](#manual-cc-structure) as well as
optional [Python modules](#manual-cc-hooks) for advanced customizations.
They contain all metadata, settings, and variables
for your project and its workflows, organized in a structured format.
|{{ ccc.name }}| uses these configuration files
to automatically maintain your project in various ways:

1. Instead of manually configuring tools and platforms using different user interface,
   |{{ ccc.name }}| automatically configures them via APIs.
   Examples include various GitHub repository settings, e.g., project metadata,
   branch/tag names and protection rules, issue labels, GitHub Pages settings.
2. Instead of creating and maintaining different configuration files for tools and services,
   |{{ ccc.name }}| automatically generates and updates them.
   Examples include Python package configuration files (e.g., `pyproject.toml`, conda recipes),
   GitHub configuration files (e.g., issue and discussion forms, pull request templates, code owners),
   and environment files (e.g., pip `requirements.txt`, conda `environment.yaml`).
3. License, citation, and various documentation files like READMEs and community health files
   are all automatically generated and maintained from simple inputs. For example,
   |{{ ccc.name }}| can generate license files from any SPDX license expression,
   with support for multiple Markdown formats.
4. Any other file can be dynamically generated or augmented. Examples include injecting
   docstrings, comments, or any arbitrary piece of code into Python source files.
   For example, by default the project's license and copyright information are added as comments
   to the top of all modules, and the main module's docstring
   is automatically generated from project descriptors.
5. All project workflows and pipelines are fully customizable,
   with more than four thousand available [options](#manual-cc-options). These include
   team configurations for automatic task assignment and governance,
   issue management and version control settings, configurations for
   Continuous integration and deployment pipelines, metadata for indexing repositories, and many more.

Therefore, the control center configurations act as a single comprehensive
source of data from which most of your project can be automatically generated and maintained.
In fact, since the control center is able to dynamically generate any file,
it is possible to include your entire project (with all Python codes,
test cases, and documentation) in the control center as (static or dynamic) configurations,
so that everything can be dynamically updated.
Changes to control center configurations are automatically propagated throughout your repository
and all supported tools and services during so-called [synchronization](#manual-cc-sync) events that trigger the CCA pipeline.
These are carried out automatically on GHA, but can also be invoked locally using |{{ ccc.name }}|'s CLI.


::::{grid} 1
:margin: 0
:gutter: 0
:padding: 4 0 0 4


:::{grid-item-card} Location
:class-title: sd-text-center
:link: location/index
:link-type: doc

Learn more about the location of
your project's control center directory
and how to customize it.
:::


:::{grid-item-card} Structure
:class-title: sd-text-center
:link: structure/index
:link-type: doc

An overview of the general structure
and content of your project's control center directory,
and ways you can customize them.
:::


:::{grid-item-card} Options
:class-title: sd-text-center
:link: options/index
:link-type: doc

A summary of the available control center options
and their default values, as well as
instructions on adding additional custom configurations.
:::


:::{grid-item-card} Templating
:class-title: sd-text-center
:link: templating/index
:link-type: doc

Instructions on how to use templating
in your repository's control center files
to dynamically generate and reuse data.
:::


:::{grid-item-card} Inheritance
:class-title: sd-text-center
:link: inheritance/index
:link-type: doc

Learn how to dynamically inherit
specific configurations from online resources
and simultaneously manage multiple projects.
:::


:::{grid-item-card} Hooks
:class-title: sd-text-center
:link: hooks/index
:link-type: doc

Instructions on how to add custom plugins
that can hook into specific workflow steps
to extend |{{ ccc.name }}|'s functionalities.
:::


:::{grid-item-card} Synchronization
:class-title: sd-text-center
:link: synchronization/index
:link-type: doc

A full reference and in-depth explanation of all available options
in your repository's control center.
:::


:::{grid-item-card} Outputs
:class-title: sd-text-center
:link: outputs/index
:link-type: doc

A full reference and in-depth explanation of all dynamic files that are
automatically generated and updated by your repository's control center.
:::


:::{grid-item-card} Caching
:class-title: sd-text-center
:link: caching/index
:link-type: doc

Instructions on how to use substitutions (aka templating) in your repository's control center
and documentation website.
:::

::::
