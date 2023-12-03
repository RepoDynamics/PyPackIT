# Options

:::{toctree}
:hidden:

extensions/index
config/index
path/index
project/index
dev/index
package/index
ui/index
custom/index
:::


This section contains a full reference and detailed explanation of all
available options in your repository's control center.
These are divided into two categories: **non-extendable** and **extendable** options.
Non-extendable options are those that are required by {{ pp_meta.name }}
during the processing of your control center, and thus cannot be extended from other repositories.
These are all stored in YAML files at the root of your repository's control center directory.
Extendable options, on the other hand, are those that can be freely extended from other repositories,
and are organized into subdirectories within your repository's control center.

[Non-Extendable Options]{.centered-text-h2}

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} Extensions
:class-title: sd-text-center
:link: extensions/index
:link-type: doc

Extension definitions for your control center's contents.
:::

:::{grid-item-card} Base Config
:class-title: sd-text-center
:link: config/index
:link-type: doc

Base configurations for the control center itself.
:::

:::{grid-item-card} Paths
:class-title: sd-text-center
:link: path/index
:link-type: doc

Path definitions for your repository's main directories.
:::

::::


[Extendable Options]{.centered-text-h2}

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Project
:class-title: sd-text-center
:link: project/index
:link-type: doc

Core information about your project,
including name and various descriptions,
license and copytight information,
credits and funding options, etc.
:::

:::{grid-item-card} Development
:class-title: sd-text-center
:link: dev/index
:link-type: doc

Configurations and metadata
for your software development process,
GitHub/Git repository, CI/CD/CT workflows,
and most of {{ pp_meta.name }}-specific options and settings.
:::

:::{grid-item-card} Package
:class-title: sd-text-center
:link: package/index
:link-type: doc

Configurations and metadata specific to your Python package and its test suite,
including build settings, PEP 621 metadata, dependencies, entry points, etc.
:::

:::{grid-item-card} User Interfaces
:class-title: sd-text-center
:link: ui/index
:link-type: doc

Configurations, metadata, and media files for your project's user interfaces,
including documentation website, README files, health files, themes and branding, etc.
:::

:::{grid-item-card} Custom
:class-title: sd-text-center
:link: custom/index
:link-type: doc
:margin: 3 3 auto auto

User-defined custom variables that can be used
throughout your repository's control center and documentation website.
:::

::::
