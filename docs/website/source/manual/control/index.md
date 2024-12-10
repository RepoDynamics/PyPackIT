# Control Center

<!--
Your repository's control center is the singular interface
from which you can manage your entire project,
and even multiple projects at once.

It contains all available settings for {{ ccc.name }} itself,
along with all information, configurations, and metadata of your project and all its components,
gathered in one place and presented in a clear, consistent, and concise format.

All available options are already provided in the `.meta` directory,
where all general configurations and settings are set to sensible default values.
Therefore, as the first step, you only need to add some basic information about your project,
and provide some project-specific configurations:

where all configurations, metadata, and settings for your GitHub repository (and its corresponding git repository),
package, website, development pipeline, and other tools are stored in one place.

Any change applied to the control center is automatically propagated throughout your repository,
Python package, test suite, documentation website, and all other supported tools and external services.
Therefore, instead of having to deal with multiple interfaces and diverse configuration
and metadata files scattered across your repository and each with its own format and syntax,
you can simply manage your entire project from within the control center,
using a single, unified, and consistent interface;
{{ ccc.name }} automatically translates your changes into the appropriate formats,
generates all necessary files in the required locations, and updates them dynamically.


Therefore, besides your source code, unit tests, and documentation content,
all other aspects of your project are automatically managed by {{ ccc.name }} according to your specifications
in the `meta` directory.
-->


::::{grid} 1
:margin: 0
:gutter: 0
:padding: 4 0 0 4


:::{grid-item-card} Location and Structure
:class-title: sd-text-center
:link: structure/index
:link-type: doc

An overview of the location, general structure,
and constituents of your repository's control center,
along with instructions on how to customize them.
:::


:::{grid-item-card} Templating
:class-title: sd-text-center
:link: templating/index
:link-type: doc

Instructions on how to use templating
in your repository's control center files.
:::


:::{grid-item-card} Inheritance
:class-title: sd-text-center
:link: inheritance/index
:link-type: doc

Instructions on how to dynamically inherit
specific configurations from external resources.
:::

<!--

:::{grid-item-card} Validation
:class-title: sd-text-center
:link: validation/index
:link-type: doc

Instructions on how to use substitutions (aka templating) in your repository's control center
and documentation website.
:::


:::{grid-item-card} Options
:class-title: sd-text-center
:link: options/index
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

-->

::::
