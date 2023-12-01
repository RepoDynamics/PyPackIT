# Control Center

:::{toctree}
:hidden:

structure/index
substitutions/index
options/index
outputs/index
:::

Your repository's control center is the singular interface from which you can manage your entire project.
It contains all available settings for {{ pp_meta.name }} itself,
along with all information, configurations, and metadata of your project and all its components,
gathered in one place and presented in a clear, consistent, and concise format.
Any change applied to the control center is automatically propagated throughout your repository,
Python package, test suite, documentation website, and all other supported tools and external services.
Therefore, instead of having to deal with multiple interfaces and diverse configuration
and metadata files scattered across your repository and each with its own format and syntax,
you can simply manage your entire project from within the control center,
using a single, unified, and consistent interface;
{{ pp_meta.name }} automatically translates your changes into the appropriate formats,
generates all necessary files in the required locations, and updates them dynamically.


::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Structure and Location
:class-title: sd-text-center
:link: structure/index
:link-type: doc

An overview of the general structure and location of your repository's control center,
and instructions on how to customize its location.
:::

:::{grid-item-card} Substitutions
:class-title: sd-text-center
:link: substitutions/index
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

::::
